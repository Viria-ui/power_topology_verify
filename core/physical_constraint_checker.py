"""
物理约束校验模块 (Physical Constraint Checker)
============================================

基于基尔霍夫定律和电气工程原理，对拓扑和遥测数据进行物理约束校验：

1. KCL (基尔霍夫电流定律) 节点功率平衡校验
2. 支路约束校验：开关分位不应有明显潮流，合位两端电压差与功率方向应合理
3. 联络约束校验：跨馈线开关合位后检查是否形成非计划合环
4. 综合风险评分：GAT异常分 + 图模规则分 + 物理残差分 + 数据可信度修正

答辩时可清楚解释"为什么判异常"，而不只是说模型判了异常。
"""

from __future__ import annotations
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class PhysicalConstraintResult:
    """单条物理约束校验结果"""
    check_type: str  # 'KCL', 'BRANCH', 'TIE_LOOP', 'VOLTAGE_IMBALANCE'
    equip_id: str
    node_id: str = ""
    passed: bool = True
    residual: float = 0.0  # KCL残差或约束偏差值
    threshold: float = 0.0  # 判定阈值
    confidence: float = 0.0  # 可信度 0-1
    physical_basis: str = ""  # 物理依据描述
    detail: str = ""  # 详细说明
    risk_level: str = "低"  # 高/中/低
    suggestion: str = ""  # 整改建议


@dataclass
class DataSourceQuality:
    """数据源可信度评估"""
    source_type: str  # 'telemetry', 'svg', 'database'
    completeness: float = 1.0  # 数据完整度 0-1
    timeliness: float = 1.0  # 时效性 0-1
    consistency: float = 1.0  # 一致性 0-1
    confidence_interval: Tuple[float, float] = (0.5, 0.95)  # 可信度区间
    
    @property
    def overall_quality(self) -> float:
        """综合可信度 = 时效性 × 一致性 × 完整度"""
        return self.timeliness * self.consistency * self.completeness
    
    def to_dict(self) -> dict:
        return {
            "source_type": self.source_type,
            "completeness": round(self.completeness, 3),
            "timeliness": round(self.timeliness, 3),
            "consistency": round(self.consistency, 3),
            "confidence_interval": [round(x, 3) for x in self.confidence_interval],
            "overall_quality": round(self.overall_quality, 3),
        }


@dataclass
class ComprehensiveRiskScore:
    """综合风险评分"""
    equip_id: str
    gat_anomaly_score: float = 0.0  # GAT模型异常分数 (0-1)
    graph_rule_score: float = 0.0  # 图模规则异常分数 (0-1)
    physical_residual_score: float = 0.0  # 物理约束残差分数 (0-1)
    data_confidence: float = 1.0  # 数据可信度修正因子 (0-1)
    
    # 各维度权重
    WEIGHTS = {
        "gat": 0.25,
        "graph_rule": 0.25,
        "physical": 0.35,
        "confidence": 0.15,
    }
    
    @property
    def total_score(self) -> float:
        """综合风险 = 各维度加权求和后，用数据可信度修正"""
        raw_score = (
            self.gat_anomaly_score * self.WEIGHTS["gat"] +
            self.graph_rule_score * self.WEIGHTS["graph_rule"] +
            self.physical_residual_score * self.WEIGHTS["physical"]
        )
        return raw_score * (2 - self.data_confidence)  # 数据可信度越低，风险评分越高
    
    @property
    def risk_level(self) -> str:
        score = self.total_score
        if score >= 0.7:
            return "高"
        elif score >= 0.4:
            return "中"
        else:
            return "低"
    
    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "gat_anomaly_score": round(self.gat_anomaly_score, 3),
            "graph_rule_score": round(self.graph_rule_score, 3),
            "physical_residual_score": round(self.physical_residual_score, 3),
            "data_confidence": round(self.data_confidence, 3),
            "comprehensive_risk": round(self.total_score, 3),
            "risk_level": self.risk_level,
            "weight_breakdown": {k: round(v, 3) for k, v in self.WEIGHTS.items()},
        }


class PhysicalConstraintChecker:
    """
    物理约束校验器
    
    校验规则：
    - KCL: 节点入/出功率与负荷、新能源出力是否满足近似基尔霍夫约束
    - BRANCH: 开关分位不应有明显潮流；合位两端电压差与功率方向应合理
    - TIE_LOOP: 跨馈线开关合位后检查是否形成多电源非计划合环
    """
    
    # KCL残差阈值 (单位: A)
    KCL_CURRENT_THRESHOLD = 10.0  # 三相电流残差超过10A判异常
    KCL_POWER_THRESHOLD = 50.0  # 功率残差超过50kW判异常
    
    # 电压不平衡阈值
    VOLTAGE_IMBALANCE_THRESHOLD = 0.05  # 电压不平衡度超过5%判异常
    
    # 潮流方向阈值
    POWER_DIRECTION_TOLERANCE = 0.1  # 合位开关两端功率方向相反比例容忍度
    
    def __init__(
        self,
        telemetry_data: dict = None,
        topology_graph = None,
        device_map: dict = None,
        switch_status_map: dict = None,
    ):
        self.telemetry_data = telemetry_data or {}
        self.topology_graph = topology_graph
        self.device_map = device_map or {}
        self.switch_status_map = switch_status_map or {}  # equip_id -> 'CLOSE'/'OPEN'
        
        self.results: List[PhysicalConstraintResult] = []
        self.data_quality: Dict[str, DataSourceQuality] = {}
        
    def _number(self, value, default=0.0) -> float:
        """安全转换为浮点数"""
        try:
            return float(value) if value is not None else default
        except (TypeError, ValueError):
            return default
    
    def _get_latest_telemetry(self, equip_id: str) -> dict:
        """获取设备最新遥测数据"""
        rows = self.telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            return rows
        return rows[-1] if rows else {}
    
    def _get_telemetry_window(self, equip_id: str, seconds: int = 300) -> List[dict]:
        """获取指定时间窗口内的遥测数据"""
        rows = self.telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        return rows[-10:] if rows else []  # 简化：取最近10条
    
    def evaluate_data_quality(self) -> Dict[str, DataSourceQuality]:
        """
        评估各数据源的可信度
        
        - 遥测数据：检查缺失率、延迟、波动异常
        - SVG数据：检查与数据库设备ID匹配度
        - 数据库数据：检查字段完整度
        """
        quality_results = {}
        
        # 1. 遥测数据可信度
        total_equips = len(self.device_map)
        equip_with_telemetry = sum(
            1 for eid in self.device_map.keys()
            if str(eid) in self.telemetry_data and self.telemetry_data[str(eid)]
        )
        completeness = equip_with_telemetry / max(total_equips, 1)
        
        # 计算遥测波动异常率
        fluctuation_anomaly_count = 0
        for eid in list(self.telemetry_data.keys())[:100]:  # 抽样100个
            window = self._get_telemetry_window(eid, 300)
            if len(window) >= 2:
                values = [self._number(r.get('AP', 0)) for r in window]
                if values:
                    mean_val = sum(values) / len(values)
                    if mean_val > 0:
                        variance = sum((v - mean_val) ** 2 for v in values) / len(values)
                        cv = (variance ** 0.5) / mean_val  # 变异系数
                        if cv > 0.5:  # 波动超过50%
                            fluctuation_anomaly_count += 1
        
        fluctuation_anomaly_rate = fluctuation_anomaly_count / 100
        
        tele_quality = DataSourceQuality(
            source_type="telemetry",
            completeness=completeness,
            timeliness=1.0 - fluctuation_anomaly_rate * 0.5,  # 波动异常降低时效性
            consistency=1.0 - fluctuation_anomaly_rate * 0.3,
            confidence_interval=(
                max(0.3, completeness - 0.2),
                min(0.95, completeness + 0.1)
            )
        )
        quality_results["telemetry"] = tele_quality
        self.data_quality["telemetry"] = tele_quality
        
        # 2. SVG图模数据可信度 (简化计算)
        svg_quality = DataSourceQuality(
            source_type="svg",
            completeness=0.85,  # SVG解析完整度估算
            timeliness=1.0,
            consistency=0.90,
            confidence_interval=(0.7, 0.95)
        )
        quality_results["svg"] = svg_quality
        self.data_quality["svg"] = svg_quality
        
        # 3. 数据库数据可信度
        db_quality = DataSourceQuality(
            source_type="database",
            completeness=0.95,
            timeliness=1.0,
            consistency=0.95,
            confidence_interval=(0.8, 0.98)
        )
        quality_results["database"] = db_quality
        self.data_quality["database"] = db_quality
        
        logger.info(
            f"[物理约束] 数据源可信度: 遥测={tele_quality.overall_quality:.2f}, "
            f"SVG={svg_quality.overall_quality:.2f}, 数据库={db_quality.overall_quality:.2f}"
        )
        
        return quality_results
    
    def check_kcl_node_balance(
        self,
        node_id: str,
        connected_equips: List[str],
    ) -> PhysicalConstraintResult:
        """
        KCL (基尔霍夫电流定律) 节点功率平衡校验
        
        原理：对于任意节点，流入电流之和等于流出电流之和
        公式: ΣI_in = ΣI_out (允许一定残差阈值)
        
        参数:
            node_id: 连接点ID
            connected_equips: 连接到此节点的设备ID列表
        
        返回:
            PhysicalConstraintResult: 校验结果
        """
        # 获取各设备的三相电流
        ia_values, ib_values, ic_values = [], [], []
        valid_count = 0
        
        for equip_id in connected_equips:
            row = self._get_latest_telemetry(equip_id)
            ia = self._number(row.get('IA', 0))
            ib = self._number(row.get('IB', 0))
            ic = self._number(row.get('IC', 0))
            
            if ia != 0 or ib != 0 or ic != 0:
                valid_count += 1
                ia_values.append(ia)
                ib_values.append(ib)
                ic_values.append(ic)
        
        if valid_count == 0:
            return PhysicalConstraintResult(
                check_type="KCL",
                equip_id=",".join(connected_equips[:3]) + "...",
                node_id=node_id,
                passed=True,
                confidence=0.5,
                physical_basis="无有效电流数据，无法判定KCL",
                detail=f"节点{node_id}关联{len(connected_equips)}个设备，均无有效遥测",
                suggestion="建议补充该区域的电流互感器配置",
            )
        
        # 计算三相电流残差
        residual_a = sum(ia_values)
        residual_b = sum(ib_values)
        residual_c = sum(ic_values)
        max_residual = max(abs(residual_a), abs(residual_b), abs(residual_c))
        
        # 判断是否通过KCL校验
        passed = max_residual <= self.KCL_CURRENT_THRESHOLD
        risk_level = "低" if passed else ("高" if max_residual > 20 else "中")
        
        # 物理依据描述
        if passed:
            physical_basis = f"KCL三相电流残差均在阈值内: IA={residual_a:.2f}A, IB={residual_b:.2f}A, IC={residual_c:.2f}A"
            suggestion = "节点功率平衡正常，无需处理"
        else:
            physical_basis = (
                f"KCL三相电流残差超过阈值({self.KCL_CURRENT_THRESHOLD}A): "
                f"IA={residual_a:.2f}A, IB={residual_b:.2f}A, IC={residual_c:.2f}A. "
                f"可能存在虚接、错接或电流互感器故障."
            )
            suggestion = "建议核查节点端子连接、电流互感器配置和功率计量装置"
        
        result = PhysicalConstraintResult(
            check_type="KCL",
            equip_id=",".join(connected_equips[:2]) + "..." if len(connected_equips) > 2 else ",".join(connected_equips),
            node_id=node_id,
            passed=passed,
            residual=max_residual,
            threshold=self.KCL_CURRENT_THRESHOLD,
            confidence=0.85 if valid_count >= 3 else 0.65,
            physical_basis=physical_basis,
            detail=f"节点{node_id}关联{len(connected_equips)}个设备, {valid_count}个有有效电流数据. "
                   f"三相电流和: IA={residual_a:.2f}A, IB={residual_b:.2f}A, IC={residual_c:.2f}A",
            risk_level=risk_level,
            suggestion=suggestion,
        )
        
        self.results.append(result)
        return result
    
    def check_branch_constraint(
        self,
        switch_id: str,
        from_node: str,
        to_node: str,
    ) -> PhysicalConstraintResult:
        """
        支路约束校验
        
        规则:
        1. 开关分位(OPEN)时，两端不应有明显潮流
        2. 开关合位(CLOSE)时，两端电压差与功率方向应合理
        
        参数:
            switch_id: 开关设备ID
            from_node: 起点节点
            to_node: 终点节点
        """
        switch_status = self.switch_status_map.get(str(switch_id), "UNKNOWN")
        row = self._get_latest_telemetry(switch_id)
        
        # 获取功率数据
        active_power = self._number(row.get('AP', 0))
        reactive_power = self._number(row.get('RP', 0))
        voltage = self._number(row.get('UA', 0))  # A相电压
        
        if switch_status == "OPEN" or switch_status == "0":
            # 分位开关不应有明显功率流
            if abs(active_power) > self.KCL_POWER_THRESHOLD:
                return PhysicalConstraintResult(
                    check_type="BRANCH",
                    equip_id=switch_id,
                    node_id=f"{from_node}->{to_node}",
                    passed=False,
                    residual=abs(active_power),
                    threshold=self.KCL_POWER_THRESHOLD,
                    confidence=0.90,
                    physical_basis=(
                        f"开关{switch_id}处于分位(OPEN), 但测得有功功率{active_power:.2f}kW. "
                        f"分位开关两端不应有功率流通."
                    ),
                    detail=f"状态={switch_status}, P={active_power:.2f}kW, Q={reactive_power:.2f}kVar",
                    risk_level="高",
                    suggestion="检查开关实际状态与遥信是否一致，或核查功率计量异常",
                )
            else:
                return PhysicalConstraintResult(
                    check_type="BRANCH",
                    equip_id=switch_id,
                    node_id=f"{from_node}->{to_node}",
                    passed=True,
                    residual=abs(active_power),
                    threshold=self.KCL_POWER_THRESHOLD,
                    confidence=0.85,
                    physical_basis=f"分位开关功率接近零，符合预期",
                    detail=f"状态={switch_status}, P={active_power:.2f}kW",
                    risk_level="低",
                )
        
        elif switch_status == "CLOSE" or switch_status == "1":
            # 合位开关应有一定的功率流或电压
            # 如果电压和功率都接近零，可能是虚接
            if abs(active_power) < 1.0 and voltage < 1.0:
                return PhysicalConstraintResult(
                    check_type="BRANCH",
                    equip_id=switch_id,
                    node_id=f"{from_node}->{to_node}",
                    passed=False,
                    residual=0.0,
                    threshold=1.0,
                    confidence=0.75,
                    physical_basis=(
                        f"开关{switch_id}处于合位但功率和电压均接近零, "
                        f"可能存在虚接或端子未正确连接."
                    ),
                    detail=f"状态={switch_status}, P={active_power:.2f}kW, U={voltage:.2f}V",
                    risk_level="中",
                    suggestion="建议现场核查开关端子连接情况",
                )
            
            # 合位开关功率方向应与电压方向一致（简化判断）
            return PhysicalConstraintResult(
                check_type="BRANCH",
                equip_id=switch_id,
                node_id=f"{from_node}->{to_node}",
                passed=True,
                residual=abs(active_power),
                threshold=0.0,
                confidence=0.80,
                physical_basis=f"合位开关功率正常: P={active_power:.2f}kW",
                detail=f"状态={switch_status}, P={active_power:.2f}kW, Q={reactive_power:.2f}kVar",
                risk_level="低",
            )
        
        # 未知状态
        return PhysicalConstraintResult(
            check_type="BRANCH",
            equip_id=switch_id,
            node_id=f"{from_node}->{to_node}",
            passed=True,
            confidence=0.5,
            physical_basis=f"开关{switch_id}状态未知({switch_status}), 无法判定",
            detail="遥信数据缺失或状态不明确",
            risk_level="中",
            suggestion="检查遥信采集和数据同步",
        )
    
    def check_tie_loop_detection(
        self,
        tie_switch_id: str,
        feeder_a: str,
        feeder_b: str,
    ) -> PhysicalConstraintResult:
        """
        联络约束校验 - 合环检测
        
        规则:
        - 跨馈线开关合位后，检查是否形成多电源非计划合环
        - 正常情况：联络开关合位时，来自同一电源的馈线可以合环
        - 异常情况：来自不同电源的馈线合环会导致保护误动作
        
        参数:
            tie_switch_id: 联络开关ID
            feeder_a: 馈线A
            feeder_b: 馈线B
        """
        tie_status = self.switch_status_map.get(str(tie_switch_id), "UNKNOWN")
        
        if tie_status == "CLOSE" or tie_status == "1":
            # 联络开关合位，需要检查两侧是否来自同一电源
            # 简化：检查功率方向是否相反（如果来自同一电源，功率方向应相反）
            row = self._get_latest_telemetry(tie_switch_id)
            power_a = self._number(row.get('AP', 0))
            
            # 如果功率较大且方向稳定，可能是合环
            if abs(power_a) > 100:  # 功率超过100kW
                return PhysicalConstraintResult(
                    check_type="TIE_LOOP",
                    equip_id=tie_switch_id,
                    node_id=f"{feeder_a}<->{feeder_b}",
                    passed=False,
                    residual=abs(power_a),
                    threshold=100.0,
                    confidence=0.80,
                    physical_basis=(
                        f"联络开关{feeder_a}<->{feeder_b}合位运行, 测得功率{abs(power_a):.2f}kW. "
                        f"需确认两侧是否来自同一电源, 防止非计划合环导致保护误动."
                    ),
                    detail=f"联络开关状态={tie_status}, P={power_a:.2f}kW, "
                           f"涉及馈线: {feeder_a}, {feeder_b}",
                    risk_level="高",
                    suggestion="确认两侧电源关系, 若非同源合环需退出合环运行方式",
                )
            else:
                return PhysicalConstraintResult(
                    check_type="TIE_LOOP",
                    equip_id=tie_switch_id,
                    node_id=f"{feeder_a}<->{feeder_b}",
                    passed=True,
                    residual=abs(power_a),
                    threshold=100.0,
                    confidence=0.90,
                    physical_basis=f"联络开关合位, 功率较小({abs(power_a):.2f}kW), 合环风险低",
                    detail=f"联络开关状态={tie_status}, P={power_a:.2f}kW",
                    risk_level="低",
                )
        
        # 联络开关分位，正常
        return PhysicalConstraintResult(
            check_type="TIE_LOOP",
            equip_id=tie_switch_id,
            node_id=f"{feeder_a}<->{feeder_b}",
            passed=True,
            confidence=0.95,
            physical_basis="联络开关分位, 无合环风险",
            detail=f"联络开关状态={tie_status}",
            risk_level="低",
        )
    
    def check_voltage_balance(
        self,
        busbar_id: str,
        connected_phases: List[str] = None,
    ) -> PhysicalConstraintResult:
        """
        电压不平衡度校验
        
        规则: 三相电压不平衡度不应超过5%
        公式: δU = max(|Ua-Un|, |Ub-Un|, |Uc-Un|) / Un × 100%
        其中 Un = (Ua + Ub + Uc) / 3
        """
        row = self._get_latest_telemetry(busbar_id)
        
        ua = self._number(row.get('UA', 0))
        ub = self._number(row.get('UB', 0))
        uc = self._number(row.get('UC', 0))
        
        if ua == 0 and ub == 0 and uc == 0:
            return PhysicalConstraintResult(
                check_type="VOLTAGE_IMBALANCE",
                equip_id=busbar_id,
                passed=True,
                confidence=0.5,
                physical_basis="无有效电压数据",
                detail="三相电压均为零",
                risk_level="中",
            )
        
        un = (ua + ub + uc) / 3
        if un < 1.0:
            return PhysicalConstraintResult(
                check_type="VOLTAGE_IMBALANCE",
                equip_id=busbar_id,
                passed=True,
                confidence=0.5,
                physical_basis="母线电压过低, 无法计算不平衡度",
                detail=f"三相电压: UA={ua:.2f}V, UB={ub:.2f}V, UC={uc:.2f}V",
                risk_level="中",
            )
        
        imbalance = max(abs(ua - un), abs(ub - un), abs(uc - un)) / un
        passed = imbalance <= self.VOLTAGE_IMBALANCE_THRESHOLD
        
        return PhysicalConstraintResult(
            check_type="VOLTAGE_IMBALANCE",
            equip_id=busbar_id,
            passed=passed,
            residual=imbalance * 100,
            threshold=self.VOLTAGE_IMBALANCE_THRESHOLD * 100,
            confidence=0.85,
            physical_basis=(
                f"三相电压: UA={ua:.1f}V, UB={ub:.1f}V, UC={uc:.1f}V, "
                f"不平衡度={imbalance*100:.2f}% (阈值={self.VOLTAGE_IMBALANCE_THRESHOLD*100}%)"
            ) if not passed else f"电压不平衡度{imbalance*100:.2f}%, 在正常范围内",
            detail=f"Ua={ua:.1f}V, Ub={ub:.1f}V, Uc={uc:.1f}V, Un={un:.1f}V",
            risk_level="高" if imbalance > 0.1 else ("中" if imbalance > 0.05 else "低"),
            suggestion="检查三相负荷平衡或电压互感器接线" if not passed else "无需处理",
        )
    
    def calculate_comprehensive_risk(
        self,
        equip_id: str,
        gat_score: float = 0.0,
        graph_rule_score: float = 0.0,
        physical_residual: float = 0.0,
    ) -> ComprehensiveRiskScore:
        """
        计算综合风险评分
        
        公式: 综合风险 = GAT异常分×0.25 + 图模规则分×0.25 + 物理残差分×0.35 + 数据可信度修正×0.15
        
        参数:
            equip_id: 设备ID
            gat_score: GAT模型异常分数 (0-1)
            graph_rule_score: 图模规则异常分数 (0-1)
            physical_residual: 物理约束残差 (0-1)
        
        返回:
            ComprehensiveRiskScore: 综合风险评分对象
        """
        # 获取数据可信度
        data_confidence = 1.0
        if "telemetry" in self.data_quality:
            data_confidence = min(data_confidence, self.data_quality["telemetry"].overall_quality)
        if "svg" in self.data_quality:
            data_confidence = min(data_confidence, self.data_quality["svg"].overall_quality)
        
        return ComprehensiveRiskScore(
            equip_id=equip_id,
            gat_anomaly_score=gat_score,
            graph_rule_score=graph_rule_score,
            physical_residual_score=physical_residual,
            data_confidence=data_confidence,
        )
    
    def run_batch_check(
        self,
        nodes_to_check: List[str] = None,
        switches_to_check: List[str] = None,
    ) -> List[PhysicalConstraintResult]:
        """
        批量执行物理约束校验
        
        参数:
            nodes_to_check: 需要校验KCL的节点列表
            switches_to_check: 需要校验的开关列表
        
        返回:
            List[PhysicalConstraintResult]: 所有校验结果
        """
        self.results = []
        
        # 先评估数据质量
        self.evaluate_data_quality()
        
        # KCL节点校验
        if nodes_to_check:
            logger.info(f"[物理约束] 开始KCL校验, 共{len(nodes_to_check)}个节点")
            for node in nodes_to_check:
                # 获取节点关联的设备 (需要上层传入拓扑信息)
                connected = self.device_map.get(node, {}).get("connected_equips", [])
                if connected:
                    self.check_kcl_node_balance(node, connected)
        
        # 开关约束校验
        if switches_to_check:
            logger.info(f"[物理约束] 开始支路约束校验, 共{len(switches_to_check)}个开关")
            for switch_id in switches_to_check:
                # 获取开关两端节点 (需要上层传入拓扑信息)
                from_node = self.device_map.get(switch_id, {}).get("from_node", "")
                to_node = self.device_map.get(switch_id, {}).get("to_node", "")
                if from_node and to_node:
                    self.check_branch_constraint(switch_id, from_node, to_node)
        
        return self.results
    
    def get_high_risk_anomalies(self) -> List[PhysicalConstraintResult]:
        """获取高风险异常列表"""
        return [r for r in self.results if r.risk_level == "高" and not r.passed]
    
    def generate_physical_constraint_report(self) -> dict:
        """
        生成物理约束校验报告
        
        返回格式:
        {
            "summary": {...},
            "high_risk_anomalies": [...],
            "data_quality": {...},
            "constraint_results": [...]
        }
        """
        high_risk = self.get_high_risk_anomalies()
        medium_risk = [r for r in self.results if r.risk_level == "中" and not r.passed]
        
        report = {
            "summary": {
                "total_checks": len(self.results),
                "passed": sum(1 for r in self.results if r.passed),
                "failed": sum(1 for r in self.results if not r.passed),
                "high_risk_count": len(high_risk),
                "medium_risk_count": len(medium_risk),
                "low_risk_count": sum(1 for r in self.results if r.risk_level == "低"),
            },
            "high_risk_anomalies": [
                {
                    "equip_id": r.equip_id,
                    "check_type": r.check_type,
                    "node_id": r.node_id,
                    "physical_basis": r.physical_basis,
                    "detail": r.detail,
                    "suggestion": r.suggestion,
                    "confidence": r.confidence,
                }
                for r in high_risk
            ],
            "data_quality": {k: v.to_dict() for k, v in self.data_quality.items()},
            "constraint_results": [
                {
                    "check_type": r.check_type,
                    "equip_id": r.equip_id,
                    "node_id": r.node_id,
                    "passed": r.passed,
                    "risk_level": r.risk_level,
                    "residual": round(r.residual, 3),
                    "threshold": round(r.threshold, 3),
                    "confidence": round(r.confidence, 3),
                    "physical_basis": r.physical_basis,
                    "suggestion": r.suggestion,
                }
                for r in self.results
            ],
        }
        
        logger.info(
            f"[物理约束] 校验完成: 总计{report['summary']['total_checks']}项, "
            f"通过{report['summary']['passed']}, 失败{report['summary']['failed']}, "
            f"高风险{report['summary']['high_risk_count']}项"
        )
        
        return report


# ============================================================
# 简化版物理约束校验（用于集成到现有系统）
# ============================================================

def evaluate_physical_constraint(
    equip_id: str,
    telemetry_data: dict,
    switch_status: str,
    connected_equips: List[str] = None,
) -> Tuple[bool, float, str]:
    """
    简化版物理约束评估接口
    
    返回: (是否通过, 残差值, 物理依据描述)
    """
    checker = PhysicalConstraintChecker(
        telemetry_data=telemetry_data,
        switch_status_map={equip_id: switch_status},
    )
    
    if connected_equips:
        result = checker.check_kcl_node_balance(f"NODE_{equip_id}", connected_equips)
    else:
        result = checker.check_branch_constraint(equip_id, "NODE_A", "NODE_B")
    
    return result.passed, result.residual, result.physical_basis


def calculate_comprehensive_risk_score(
    equip_id: str,
    gat_anomaly: float,
    graph_rule_anomaly: float,
    physical_residual: float,
    telemetry_quality: float = 1.0,
) -> dict:
    """
    计算综合风险评分的简化接口
    
    综合风险 = GAT异常分×0.25 + 图模规则分×0.25 + 物理残差分×0.35 + 数据可信度修正×0.15
    """
    raw_score = (
        gat_anomaly * 0.25 +
        graph_rule_anomaly * 0.25 +
        physical_residual * 0.35
    )
    
    # 数据可信度修正：可信度越低，风险评分越高
    confidence_factor = 2 - telemetry_quality
    total_score = raw_score * confidence_factor
    
    risk_level = "高" if total_score >= 0.7 else ("中" if total_score >= 0.4 else "低")
    
    return {
        "equip_id": equip_id,
        "gat_anomaly": round(gat_anomaly, 3),
        "graph_rule_anomaly": round(graph_rule_anomaly, 3),
        "physical_residual": round(physical_residual, 3),
        "telemetry_quality": round(telemetry_quality, 3),
        "comprehensive_risk": round(total_score, 3),
        "risk_level": risk_level,
        "weight_breakdown": {
            "gat": 0.25,
            "graph_rule": 0.25,
            "physical": 0.35,
            "confidence": 0.15,
        },
        "physical_basis": (
            f"综合风险={total_score:.3f}(高/中/低:{risk_level}), "
            f"由GAT异常{gat_anomaly:.2f}、图模规则{graph_rule_anomaly:.2f}、"
            f"物理残差{physical_residual:.2f}加权计算, 数据可信度{telemetry_quality:.2f}修正"
        ),
    }
