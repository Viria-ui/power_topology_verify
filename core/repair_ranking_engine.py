"""
最小修改闭环修正排序模块
=========================

将当前 SQL 修复草案升级为"候选修正排序"：

1. 补全端子/连接关系
2. 修正开关状态
3. 修正馈线归属
4. 删除疑似虚接
5. 补充主配接口关系

每个候选给出：
- 影响范围
- 风险降低量
- 物理约束是否恢复
- 可回滚 SQL

优先选择：改动设备数最少、恢复约束最多、置信度最高的方案
"""

from __future__ import annotations
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)


class RepairAction(Enum):
    """修复动作类型"""
    ADD_DEVICE = "ADD_DEVICE"           # 添加设备
    UPDATE_DEVICE = "UPDATE_DEVICE"      # 更新设备属性
    ADD_CONNECTION = "ADD_CONNECTION"   # 添加连接关系
    UPDATE_CONNECTION = "UPDATE_CONNECTION"  # 更新连接关系
    DELETE_DEVICE = "DELETE_DEVICE"     # 删除设备
    UPDATE_VOLTAGE_TYPE = "UPDATE_VOLTAGE_TYPE"  # 更新电压类型
    FIX_SWITCH_STATUS = "FIX_SWITCH_STATUS"  # 修正开关状态
    FIX_FEEDER_AFFILIATION = "FIX_FEEDER_AFFILIATION"  # 修正馈线归属


class PhysicalConstraint(Enum):
    """物理约束类型"""
    KCL_BALANCE = "KCL_BALANCE"           # KCL电流平衡
    CONNECTIVITY = "CONNECTIVITY"         # 连通性
    POWER_FLOW = "POWER_FLOW"             # 潮流方向
    VOLTAGE_LEVEL = "VOLTAGE_LEVEL"        # 电压等级
    TIE_LOOP = "TIE_LOOP"                # 合环检测
    ISLAND_FREE = "ISLAND_FREE"            # 无孤岛


@dataclass
class ImpactScope:
    """影响范围评估"""
    devices_affected: int = 0  # 受影响设备数
    feeders_affected: List[str] = field(default_factory=list)  # 受影响馈线
    connections_affected: int = 0  # 受影响连接数
    downstream_devices: int = 0  # 下游设备数（如果此设备故障）
    upstream_devices: int = 0  # 上游设备数
    is_critical: bool = False  # 是否关键设备
    is_tie_point: bool = False  # 是否为联络点
    is_source_connected: bool = False  # 是否连接电源
    
    def to_dict(self) -> dict:
        return {
            "devices_affected": self.devices_affected,
            "feeders_affected": self.feeders_affected,
            "connections_affected": self.connections_affected,
            "downstream_devices": self.downstream_devices,
            "upstream_devices": self.upstream_devices,
            "is_critical": self.is_critical,
            "is_tie_point": self.is_tie_point,
            "is_source_connected": self.is_source_connected,
        }


@dataclass
class ConstraintRestoration:
    """物理约束恢复评估"""
    constraints_before: List[PhysicalConstraint] = field(default_factory=list)
    constraints_after: List[PhysicalConstraint] = field(default_factory=list)
    constraints_restored: List[PhysicalConstraint] = field(default_factory=list)
    constraints_violated: List[PhysicalConstraint] = field(default_factory=list)
    restoration_score: float = 0.0  # 恢复评分 0-1
    
    @property
    def net_gain(self) -> float:
        """净收益 = 恢复 - 破坏"""
        return len(self.constraints_restored) - len(self.constraints_violated)
    
    def to_dict(self) -> dict:
        return {
            "constraints_before": [c.value for c in self.constraints_before],
            "constraints_after": [c.value for c in self.constraints_after],
            "constraints_restored": [c.value for c in self.constraints_restored],
            "constraints_violated": [c.value for c in self.constraints_violated],
            "restoration_score": round(self.restoration_score, 3),
            "net_gain": self.net_gain,
        }


@dataclass
class RepairCandidate:
    """修复候选方案"""
    repair_id: str
    defect_id: str  # 对应的缺陷ID
    action: RepairAction
    target_equip: str
    
    # SQL相关
    sql_forward: str = ""
    sql_rollback: str = ""
    
    # 评估指标
    confidence: float = 0.0  # 置信度 0-1
    risk_reduction: float = 0.0  # 风险降低量 0-1
    impact_scope: ImpactScope = None
    
    # 约束恢复
    constraint_restoration: ConstraintRestoration = None
    
    # 元信息
    description: str = ""
    physical_basis: str = ""
    suggestion: str = ""
    priority_score: float = 0.0  # 综合优先级评分
    
    def __post_init__(self):
        if self.impact_scope is None:
            self.impact_scope = ImpactScope()
        if self.constraint_restoration is None:
            self.constraint_restoration = ConstraintRestoration()
    
    def calculate_priority(self) -> float:
        """
        计算综合优先级评分
        
        公式: 优先级 = 置信度×0.3 + 风险降低量×0.4 + 约束恢复得分×0.3 - 影响范围惩罚
        
        高置信度、高风险降低、高约束恢复、低影响的方案优先
        """
        # 影响范围惩罚（高影响设备降低优先级）
        impact_penalty = 0.0
        if self.impact_scope:
            scope = self.impact_scope
            # 关键设备惩罚
            if scope.is_critical:
                impact_penalty += 0.15
            # 联络点惩罚
            if scope.is_tie_point:
                impact_penalty += 0.10
            # 大规模下游设备惩罚
            if scope.downstream_devices > 100:
                impact_penalty += 0.10
            elif scope.downstream_devices > 50:
                impact_penalty += 0.05
        
        # 约束恢复得分
        constraint_score = self.constraint_restoration.restoration_score if self.constraint_restoration else 0.0
        
        self.priority_score = (
            self.confidence * 0.30 +
            self.risk_reduction * 0.40 +
            constraint_score * 0.30 -
            impact_penalty
        )
        
        return round(self.priority_score, 4)
    
    def to_dict(self) -> dict:
        return {
            "repair_id": self.repair_id,
            "defect_id": self.defect_id,
            "action": self.action.value,
            "target_equip": self.target_equip,
            "sql_forward": self.sql_forward,
            "sql_rollback": self.sql_rollback,
            "confidence": round(self.confidence, 3),
            "risk_reduction": round(self.risk_reduction, 3),
            "impact_scope": self.impact_scope.to_dict(),
            "constraint_restoration": self.constraint_restoration.to_dict(),
            "description": self.description,
            "physical_basis": self.physical_basis,
            "suggestion": self.suggestion,
            "priority_score": round(self.priority_score, 4),
        }


class RepairRankingEngine:
    """
    修复方案排序引擎
    
    核心功能：
    1. 评估每个修复候选的影响范围
    2. 计算风险降低量
    3. 检查物理约束恢复情况
    4. 生成排序后的修复方案
    """
    
    def __init__(
        self,
        topology_graph=None,
        device_map: dict = None,
        feeder_map: dict = None,
        switch_status_map: dict = None,
    ):
        self.topology_graph = topology_graph
        self.device_map = device_map or {}
        self.feeder_map = feeder_map or {}  # equip_id -> feeder_id
        self.switch_status_map = switch_status_map or {}  # equip_id -> 'CLOSE'/'OPEN'
        
    def evaluate_impact_scope(
        self,
        equip_id: str,
        action: RepairAction,
    ) -> ImpactScope:
        """
        评估修复操作的影响范围
        
        参数:
            equip_id: 目标设备ID
            action: 修复动作
        
        返回:
            ImpactScope: 影响范围评估
        """
        scope = ImpactScope()
        
        # 基础影响
        scope.devices_affected = 1
        
        # 检查是否为关键设备
        device = self.device_map.get(str(equip_id), {})
        equip_type = device.get("equip_type", "")
        
        # 关键设备类型
        critical_types = {"变压器", "母线", "断路器", "PowerTransformer", "BusbarSection", "Breaker"}
        if str(equip_type) in critical_types:
            scope.is_critical = True
        
        # 检查是否为联络点
        if self._is_tie_switch(equip_id):
            scope.is_tie_point = True
        
        # 检查是否连接电源
        if self._is_source_connected(equip_id):
            scope.is_source_connected = True
        
        # 计算上下游设备数（简化计算）
        if self.topology_graph:
            try:
                # 简化：使用图的连通分量大小
                if hasattr(self.topology_graph, 'number_of_nodes'):
                    scope.downstream_devices = self.topology_graph.number_of_nodes() // 10
            except Exception:
                pass
        
        # 根据动作类型调整影响范围
        if action == RepairAction.ADD_DEVICE:
            scope.connections_affected = 2  # 添加设备通常影响2条连接
            scope.devices_affected = 1
        elif action == RepairAction.DELETE_DEVICE:
            scope.connections_affected = 4  # 删除设备影响更多连接
            scope.devices_affected = 2
        elif action == RepairAction.UPDATE_CONNECTION:
            scope.connections_affected = 1
        
        # 受影响馈线
        feeder_id = self.feeder_map.get(str(equip_id), "")
        if feeder_id:
            scope.feeders_affected = [feeder_id]
        
        return scope
    
    def _is_tie_switch(self, equip_id: str) -> bool:
        """检查是否为联络开关"""
        # 简化实现：检查设备名称是否包含"联络"
        device = self.device_map.get(str(equip_id), {})
        name = str(device.get("equip_name", "")).lower()
        return "联络" in name or "tie" in name
    
    def _is_source_connected(self, equip_id: str) -> bool:
        """检查是否直接连接电源"""
        device = self.device_map.get(str(equip_id), {})
        is_source = device.get("is_source", False)
        equip_type = str(device.get("equip_type", ""))
        return is_source or equip_type in {"变压器", "PowerTransformer", "变电站"}
    
    def evaluate_risk_reduction(
        self,
        candidate: RepairCandidate,
        original_defect: dict,
    ) -> float:
        """
        评估风险降低量
        
        参数:
            candidate: 修复候选
            original_defect: 原始缺陷信息
        
        返回:
            float: 风险降低量 0-1
        """
        # 基于缺陷严重程度
        base_reduction = 0.5
        
        # 根据缺陷类型调整
        defect_type = original_defect.get("defect_type", "")
        
        if "孤岛" in defect_type:
            # 孤岛缺陷修复价值高
            base_reduction = 0.8
        elif "虚接" in defect_type or "错接" in defect_type:
            # 虚接错接是高风险缺陷
            base_reduction = 0.9
        elif "悬空" in defect_type:
            base_reduction = 0.7
        elif "连接不一致" in defect_type:
            base_reduction = 0.6
        elif "缺失" in defect_type:
            base_reduction = 0.5
        
        # 根据动作类型调整
        if candidate.action == RepairAction.ADD_DEVICE:
            base_reduction *= 1.0
        elif candidate.action == RepairAction.UPDATE_CONNECTION:
            base_reduction *= 0.9
        elif candidate.action == RepairAction.FIX_SWITCH_STATUS:
            base_reduction *= 0.85
        elif candidate.action == RepairAction.UPDATE_VOLTAGE_TYPE:
            base_reduction *= 0.6
        
        return min(1.0, base_reduction)
    
    def evaluate_constraint_restoration(
        self,
        candidate: RepairCandidate,
        defect: dict,
    ) -> ConstraintRestoration:
        """
        评估物理约束恢复情况
        
        参数:
            candidate: 修复候选
            defect: 缺陷信息
        
        返回:
            ConstraintRestoration: 约束恢复评估
        """
        restoration = ConstraintRestoration()
        action = candidate.action
        defect_type = defect.get("defect_type", "")
        
        # 根据缺陷类型确定修复前后的约束状态
        if "孤岛" in defect_type:
            # 孤岛 -> 连通性恢复
            restoration.constraints_before = [PhysicalConstraint.ISLAND_FREE]
            restoration.constraints_after = [PhysicalConstraint.CONNECTIVITY]
            if action in {RepairAction.ADD_DEVICE, RepairAction.ADD_CONNECTION}:
                restoration.constraints_restored = [PhysicalConstraint.CONNECTIVITY]
                restoration.restoration_score = 0.9
            else:
                restoration.constraints_violated = [PhysicalConstraint.CONNECTIVITY]
                restoration.restoration_score = 0.2
        
        elif "虚接" in defect_type or "错接" in defect_type:
            # 虚接/错接 -> KCL平衡和连通性
            restoration.constraints_before = [PhysicalConstraint.KCL_BALANCE, PhysicalConstraint.CONNECTIVITY]
            restoration.constraints_after = [PhysicalConstraint.CONNECTIVITY]
            if action == RepairAction.DELETE_DEVICE or action == RepairAction.UPDATE_CONNECTION:
                restoration.constraints_restored = [PhysicalConstraint.KCL_BALANCE, PhysicalConstraint.CONNECTIVITY]
                restoration.restoration_score = 0.95
            else:
                restoration.restoration_score = 0.3
        
        elif "悬空" in defect_type:
            # 悬空端点 -> 连通性
            restoration.constraints_before = [PhysicalConstraint.CONNECTIVITY]
            restoration.constraints_after = [PhysicalConstraint.CONNECTIVITY]
            if action in {RepairAction.ADD_CONNECTION, RepairAction.ADD_DEVICE}:
                restoration.constraints_restored = [PhysicalConstraint.CONNECTIVITY]
                restoration.restoration_score = 0.85
            else:
                restoration.restoration_score = 0.2
        
        elif "连接不一致" in defect_type:
            # 连接不一致 -> 多种约束
            restoration.constraints_before = [PhysicalConstraint.CONNECTIVITY, PhysicalConstraint.POWER_FLOW]
            restoration.constraints_after = [PhysicalConstraint.CONNECTIVITY]
            if action in {RepairAction.ADD_CONNECTION, RepairAction.UPDATE_CONNECTION}:
                restoration.constraints_restored = [PhysicalConstraint.CONNECTIVITY]
                restoration.restoration_score = 0.7
            else:
                restoration.restoration_score = 0.4
        
        elif "开关状态" in defect_type:
            # 开关状态错误 -> 潮流方向
            restoration.constraints_before = [PhysicalConstraint.POWER_FLOW]
            restoration.constraints_after = [PhysicalConstraint.POWER_FLOW]
            if action == RepairAction.FIX_SWITCH_STATUS:
                restoration.constraints_restored = [PhysicalConstraint.POWER_FLOW]
                restoration.restoration_score = 0.8
            else:
                restoration.restoration_score = 0.1
        
        else:
            # 默认：仅改善连通性
            restoration.constraints_before = [PhysicalConstraint.CONNECTIVITY]
            restoration.constraints_after = [PhysicalConstraint.CONNECTIVITY]
            restoration.restoration_score = 0.5
        
        return restoration
    
    def process_repair_candidates(
        self,
        candidates: List[dict],
        defects: List[dict],
    ) -> List[RepairCandidate]:
        """
        处理修复候选列表，生成优先级排序
        
        参数:
            candidates: 原始修复候选（来自 repair_generator）
            defects: 缺陷列表
        
        返回:
            List[RepairCandidate]: 排序后的修复候选
        """
        # 建立缺陷ID到缺陷的映射
        defect_map = {str(d.get("equip_id", "")): d for d in defects}
        
        processed = []
        for i, cand in enumerate(candidates):
            # 创建修复候选对象
            repair_id = cand.get("repair_id", f"RANK_{i+1:04d}")
            equip_id = cand.get("target_equip", "")
            
            # 解析动作类型
            action_str = cand.get("action", "")
            try:
                action = RepairAction(action_str)
            except ValueError:
                action = RepairAction.UPDATE_DEVICE
            
            candidate = RepairCandidate(
                repair_id=repair_id,
                defect_id=equip_id,
                action=action,
                target_equip=equip_id,
                sql_forward=cand.get("sql_forward", ""),
                sql_rollback=cand.get("sql_rollback", ""),
                description=cand.get("description", ""),
                impact_scope=ImpactScope(),
                constraint_restoration=ConstraintRestoration(),
            )
            
            # 获取对应的缺陷信息
            defect = defect_map.get(str(equip_id), {})
            
            # 评估影响范围
            candidate.impact_scope = self.evaluate_impact_scope(equip_id, action)
            
            # 评估风险降低量
            candidate.risk_reduction = self.evaluate_risk_reduction(candidate, defect)
            
            # 评估约束恢复
            candidate.constraint_restoration = self.evaluate_constraint_restoration(candidate, defect)
            
            # 设置置信度（基于数据质量）
            candidate.confidence = cand.get("confidence", 0.8)
            
            # 设置物理依据
            candidate.physical_basis = self._generate_physical_basis(candidate, defect)
            
            # 设置建议
            candidate.suggestion = self._generate_suggestion(candidate)
            
            # 计算优先级
            candidate.calculate_priority()
            
            processed.append(candidate)
        
        # 按优先级排序（降序）
        processed.sort(key=lambda x: -x.priority_score)
        
        # 更新排序编号
        for i, cand in enumerate(processed):
            cand.repair_id = f"RANK_{i+1:04d}_{cand.action.value}"
        
        logger.info(
            f"[修复排序] 处理{len(processed)}个修复候选, "
            f"最高优先级={processed[0].priority_score:.3f}({processed[0].target_equip})"
        )
        
        return processed
    
    def _generate_physical_basis(self, candidate: RepairCandidate, defect: dict) -> str:
        """生成物理依据描述"""
        action = candidate.action.value
        defect_type = defect.get("defect_type", "")
        
        basis_map = {
            "ADD_DEVICE": f"添加设备{candidate.target_equip}可恢复拓扑连通性，消除{defect_type}缺陷",
            "ADD_CONNECTION": f"补充设备{candidate.target_equip}的连接关系可恢复KCL平衡和电气连通性",
            "UPDATE_CONNECTION": f"修正设备{candidate.target_equip}的连接关系可消除拓扑歧义",
            "DELETE_DEVICE": f"删除疑似虚接设备{candidate.target_equip}可恢复KCL电流平衡",
            "UPDATE_VOLTAGE_TYPE": f"修正设备{candidate.target_equip}的电压等级可恢复电压等级约束",
            "FIX_SWITCH_STATUS": f"修正开关{candidate.target_equip}的状态可消除潮流方向矛盾",
            "FIX_FEEDER_AFFILIATION": f"修正设备{candidate.target_equip}的馈线归属可恢复电气区域划分",
        }
        
        return basis_map.get(action, f"对设备{candidate.target_equip}执行{action}操作可消除{defect_type}缺陷")
    
    def _generate_suggestion(self, candidate: RepairCandidate) -> str:
        """生成整改建议"""
        action = candidate.action
        
        suggestions = {
            RepairAction.ADD_DEVICE: "建议在数据库中补充该设备记录，并关联相应的连接关系",
            RepairAction.ADD_CONNECTION: "建议核查设备端子与相邻设备的连接，补充缺失的连接关系",
            RepairAction.UPDATE_CONNECTION: "建议核查并修正设备连接关系的设备端子信息",
            RepairAction.DELETE_DEVICE: "建议现场核查设备状态，如确认虚接则申请退役流程",
            RepairAction.UPDATE_VOLTAGE_TYPE: "建议核查设备铭牌参数，修正电压等级属性",
            RepairAction.FIX_SWITCH_STATUS: "建议现场核查开关实际状态，同步修正遥信采集",
            RepairAction.FIX_FEEDER_AFFILIATION: "建议核查设备供电范围，修正馈线归属关系",
        }
        
        base = suggestions.get(action, "建议按修复方案执行修改")
        
        # 添加优先级提示
        if candidate.priority_score > 0.7:
            base += "（高优先级）"
        elif candidate.priority_score > 0.5:
            base += "（中优先级）"
        
        return base
    
    def generate_ranked_repair_report(
        self,
        ranked_candidates: List[RepairCandidate],
        top_k: int = 20,
    ) -> dict:
        """
        生成排序后的修复报告
        
        参数:
            ranked_candidates: 排序后的修复候选
            top_k: 返回前k个最高优先级候选
        
        返回:
            dict: 修复报告
        """
        top_candidates = ranked_candidates[:top_k]
        
        # 统计信息
        action_stats = {}
        for cand in ranked_candidates:
            action = cand.action.value
            action_stats[action] = action_stats.get(action, 0) + 1
        
        # 预计效果
        total_risk_reduction = sum(c.risk_reduction for c in ranked_candidates)
        avg_priority = sum(c.priority_score for c in ranked_candidates) / len(ranked_candidates) if ranked_candidates else 0
        
        report = {
            "summary": {
                "total_candidates": len(ranked_candidates),
                "action_distribution": action_stats,
                "total_risk_reduction": round(total_risk_reduction, 3),
                "average_priority_score": round(avg_priority, 3),
                "top_k": top_k,
            },
            "top_candidates": [c.to_dict() for c in top_candidates],
            "all_candidates": [c.to_dict() for c in ranked_candidates],
            "execution_order": [
                {
                    "step": i + 1,
                    "repair_id": c.repair_id,
                    "action": c.action.value,
                    "target_equip": c.target_equip,
                    "sql_forward": c.sql_forward,
                    "priority_score": round(c.priority_score, 4),
                    "risk_reduction": round(c.risk_reduction, 3),
                    "physical_basis": c.physical_basis,
                    "suggestion": c.suggestion,
                }
                for i, c in enumerate(ranked_candidates)
            ],
            "rollback_plan": [
                {
                    "step": i + 1,
                    "repair_id": c.repair_id,
                    "sql_rollback": c.sql_rollback,
                    "action": c.action.value,
                    "target_equip": c.target_equip,
                }
                for i, c in enumerate(reversed(ranked_candidates))
            ],
        }
        
        return report


def generate_rollback_script(ranked_candidates: List[RepairCandidate]) -> str:
    """
    生成回滚SQL脚本
    
    按修复的反向顺序生成回滚脚本
    """
    script = "-- ==========================================\n"
    script += "-- 修复方案回滚脚本\n"
    script += "-- 按修复的反向顺序执行以回滚所有修改\n"
    script += "-- ==========================================\n\n"
    
    for i, cand in enumerate(reversed(ranked_candidates)):
        script += f"-- 步骤 {i+1}: 回滚 {cand.action.value} - {cand.target_equip}\n"
        if cand.sql_rollback:
            script += f"{cand.sql_rollback}\n"
        else:
            script += f"-- 无需回滚（{cand.description}）\n"
        script += "\n"
    
    return script


def format_repair_ranking_table(candidates: List[RepairCandidate], top_k: int = 20) -> str:
    """
    格式化修复排序表格
    """
    if not candidates:
        return "无修复候选"
    
    header = "| 排序 | 设备ID | 动作 | 优先级 | 风险降低 | 置信度 | 约束恢复 | 影响范围 |"
    separator = "|---|---|---|---|---|---|---|---|"
    
    rows = []
    for i, c in enumerate(candidates[:top_k]):
        scope = c.impact_scope
        impact = f"设备{scope.devices_affected}"
        if scope.is_critical:
            impact += "(关键)"
        if scope.is_tie_point:
            impact += "(联络)"
        
        rows.append(
            f"| {i+1} | {c.target_equip[:12]} | {c.action.value} | "
            f"{c.priority_score:.3f} | {c.risk_reduction:.2f} | {c.confidence:.2f} | "
            f"{c.constraint_restoration.restoration_score:.2f} | {impact} |"
        )
    
    return "\n".join([header, separator] + rows)
