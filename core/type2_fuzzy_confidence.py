"""
II型模糊可信度评分与增强异常报告模块
==========================================

基于II型模糊集合理论，为每个数据源和异常评估提供可信度区间，
解决"数据不可靠时如何做判断"的问题：

核心创新：
1. 数据源可信度评估：遥测缺失/延迟/波动 → 可信度下降
2. SVG与数据库匹配度：设备ID可匹配 → 可信度上升
3. 异常判定状态：
   - CONFIRMED: 高可信度异常
   - LIKELY: 疑似异常（待现场复核）
   - PENDING: 数据不足，无法判定
   - FALSE_ALARM: 低可信度异常（可能是数据问题）

报告格式升级：
| 异常对象 | 异常类型 | 综合风险 | 可信度区间 | 物理依据 | 建议 |
"""

from __future__ import annotations
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)


class AnomalyStatus(Enum):
    """异常判定状态"""
    CONFIRMED = "CONFIRMED"       # 确认异常
    LIKELY = "LIKELY"            # 疑似异常
    PENDING = "PENDING"          # 待复核
    FALSE_ALARM = "FALSE_ALARM"  # 误报
    NORMAL = "NORMAL"           # 正常


@dataclass
class ConfidenceInterval:
    """可信度区间"""
    lower: float = 0.0
    upper: float = 1.0
    
    def __post_init__(self):
        self.lower = max(0.0, min(1.0, self.lower))
        self.upper = max(self.lower, min(1.0, self.upper))
    
    @property
    def midpoint(self) -> float:
        return (self.lower + self.upper) / 2
    
    @property
    def width(self) -> float:
        return self.upper - self.lower
    
    @property
    def is_uncertain(self) -> bool:
        """区间宽度超过0.3表示不确定性高"""
        return self.width > 0.3
    
    def to_tuple(self) -> Tuple[float, float]:
        return (round(self.lower, 3), round(self.upper, 3))
    
    def to_dict(self) -> dict:
        return {
            "lower": round(self.lower, 3),
            "upper": round(self.upper, 3),
            "midpoint": round(self.midpoint, 3),
            "width": round(self.width, 3),
            "is_uncertain": self.is_uncertain,
        }


@dataclass
class Type2FuzzyConfidence:
    """II型模糊可信度"""
    # 主可信度（区间）
    primary_confidence: ConfidenceInterval
    # 各数据源的贡献
    source_confidences: Dict[str, ConfidenceInterval] = field(default_factory=dict)
    # 可信度下降原因
    degradation_reasons: List[str] = field(default_factory=list)
    # 状态
    status: AnomalyStatus = AnomalyStatus.PENDING
    
    def get_adjusted_confidence(self, base: float) -> Tuple[float, float]:
        """
        获取调整后的可信度
        
        参数:
            base: 基础可信度（基于规则）
        
        返回:
            (调整后下限, 调整后上限)
        """
        # 根据数据源质量调整
        adjustment = 1.0
        for source, ci in self.source_confidences.items():
            if source == "telemetry":
                # 遥测数据缺失或不完整
                if ci.width > 0.5:
                    adjustment *= 0.6
                    self.degradation_reasons.append(f"{source}数据不完整({ci.width:.1%})")
            elif source == "svg":
                # SVG匹配度低
                if ci.midpoint < 0.7:
                    adjustment *= 0.8
                    self.degradation_reasons.append(f"{source}匹配度低({ci.midpoint:.1%})")
        
        lower = base * self.primary_confidence.lower * adjustment
        upper = min(1.0, base * self.primary_confidence.upper)
        
        return (round(lower, 3), round(upper, 3))
    
    def determine_status(self, base_threshold: float = 0.5) -> AnomalyStatus:
        """
        根据可信度区间确定异常状态
        
        规则：
        - 上限 < threshold: 误报
        - 上限 >= threshold, 下限 < threshold: 疑似
        - 下限 >= threshold: 确认
        - 区间宽度 > 0.4: 待复核
        """
        if self.primary_confidence.is_uncertain and self.primary_confidence.width > 0.4:
            return AnomalyStatus.PENDING
        
        if self.primary_confidence.upper < base_threshold:
            return AnomalyStatus.FALSE_ALARM
        
        if self.primary_confidence.lower >= base_threshold:
            return AnomalyStatus.CONFIRMED
        
        return AnomalyStatus.LIKELY
    
    def to_dict(self) -> dict:
        return {
            "primary_confidence": self.primary_confidence.to_dict(),
            "source_confidences": {
                k: v.to_dict() for k, v in self.source_confidences.items()
            },
            "degradation_reasons": self.degradation_reasons,
            "status": self.status.value,
        }


@dataclass
class EnhancedAnomalyReport:
    """增强异常报告"""
    equip_id: str
    anomaly_type: str
    comprehensive_risk: float = 0.0
    confidence: Type2FuzzyConfidence = None
    physical_basis: str = ""
    suggestion: str = ""
    
    # 原始缺陷信息
    original_defect: dict = None
    
    def __post_init__(self):
        if self.confidence is None:
            self.confidence = Type2FuzzyConfidence(
                primary_confidence=ConfidenceInterval(0.5, 0.8)
            )
        if self.original_defect is None:
            self.original_defect = {}
    
    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "anomaly_type": self.anomaly_type,
            "comprehensive_risk": round(self.comprehensive_risk, 3),
            "confidence_interval": self.confidence.primary_confidence.to_tuple(),
            "confidence_status": self.confidence.status.value,
            "source_confidences": {
                k: v.to_tuple() for k, v in self.confidence.source_confidences.items()
            },
            "degradation_reasons": self.confidence.degradation_reasons,
            "physical_basis": self.physical_basis,
            "suggestion": self.suggestion,
            "original_defect": self.original_defect,
        }


class Type2FuzzyConfidenceEngine:
    """
    II型模糊可信度评估引擎
    
    核心功能：
    1. 评估各数据源的可信度
    2. 计算异常的可信度区间
    3. 生成增强异常报告
    """
    
    def __init__(
        self,
        telemetry_data: dict = None,
        svg_device_map: dict = None,
        database_equips: dict = None,
    ):
        self.telemetry_data = telemetry_data or {}
        self.svg_device_map = svg_device_map or {}
        self.database_equips = database_equips or {}
        
        # 统计信息
        self.telemetry_coverage = 0.0
        self.svg_match_rate = 0.0
        self.data_freshness = 1.0
        
    def _number(self, value, default=0.0) -> float:
        """安全转换为浮点数"""
        try:
            return float(value) if value is not None else default
        except (TypeError, ValueError):
            return default
    
    def evaluate_telemetry_quality(self, equip_id: str) -> Tuple[float, List[str]]:
        """
        评估单个设备遥测数据质量
        
        返回: (可信度, 质量问题列表)
        """
        issues = []
        base_confidence = 1.0
        
        # 1. 数据完整性
        rows = self.telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        
        if not rows:
            base_confidence *= 0.5
            issues.append("遥测数据缺失")
        else:
            # 检查数据时效性
            latest = rows[-1] if rows else {}
            # 简化：假设数据都是新鲜的
            freshness = 1.0
            if freshness < 0.8:
                base_confidence *= 0.9
                issues.append(f"遥测数据可能过期(freshness={freshness:.1%})")
        
        # 2. 数据波动异常
        if len(rows) >= 3:
            values = [self._number(r.get('AP', 0)) for r in rows]
            non_zero = [v for v in values if v != 0]
            if non_zero:
                mean_val = sum(non_zero) / len(non_zero)
                variance = sum((v - mean_val) ** 2 for v in non_zero) / len(non_zero)
                cv = (variance ** 0.5) / max(abs(mean_val), 0.1)
                if cv > 1.0:
                    base_confidence *= 0.8
                    issues.append(f"遥测数据波动异常(cv={cv:.2f})")
        
        # 3. 零值检查
        if rows:
            latest = rows[-1]
            ia = abs(self._number(latest.get('IA', 0)))
            ib = abs(self._number(latest.get('IB', 0)))
            ic = abs(self._number(latest.get('IC', 0)))
            if ia < 0.1 and ib < 0.1 and ic < 0.1:
                base_confidence *= 0.7
                issues.append("三相电流均为零，可能设备停运或采集故障")
        
        return max(0.1, base_confidence), issues
    
    def evaluate_svg_quality(self, equip_id: str) -> Tuple[float, List[str]]:
        """
        评估SVG图模匹配质量
        
        返回: (可信度, 质量问题列表)
        """
        issues = []
        base_confidence = 1.0
        
        # 检查SVG中是否有该设备
        if str(equip_id) not in self.svg_device_map:
            base_confidence *= 0.6
            issues.append("SVG图中无此设备图元")
        
        # 检查设备属性完整性
        svg_elem = self.svg_device_map.get(str(equip_id), {})
        if svg_elem:
            required_attrs = ['element_id', 'object_id']
            missing_attrs = [a for a in required_attrs if not svg_elem.get(a)]
            if missing_attrs:
                base_confidence *= 0.9
                issues.append(f"SVG图元属性不完整: {missing_attrs}")
        
        return max(0.1, base_confidence), issues
    
    def evaluate_database_quality(self, equip_id: str) -> Tuple[float, List[str]]:
        """
        评估数据库数据质量
        
        返回: (可信度, 质量问题列表)
        """
        issues = []
        base_confidence = 1.0
        
        db_dev = self.database_equips.get(str(equip_id), {})
        if not db_dev:
            base_confidence *= 0.5
            issues.append("数据库中无此设备记录")
            return max(0.1, base_confidence), issues
        
        # 检查字段完整性
        important_fields = ['EQUIP_NAME', 'EQUIP_TYPE', 'FEEDER_ID']
        missing_fields = [f for f in important_fields if not db_dev.get(f)]
        if missing_fields:
            base_confidence *= 0.9
            issues.append(f"数据库字段缺失: {missing_fields}")
        
        # 检查设备类型是否有效
        equip_type = db_dev.get('EQUIP_TYPE', '')
        if not equip_type or equip_type == 'None':
            base_confidence *= 0.8
            issues.append("设备类型未定义")
        
        return max(0.1, base_confidence), issues
    
    def calculate_anomaly_confidence(
        self,
        equip_id: str,
        anomaly_type: str,
        base_confidence: float = 0.8,
    ) -> Type2FuzzyConfidence:
        """
        计算异常的可信度区间
        
        参数:
            equip_id: 设备ID
            anomaly_type: 异常类型
            base_confidence: 基础可信度
        
        返回:
            Type2FuzzyConfidence: II型模糊可信度
        """
        result = Type2FuzzyConfidence(
            primary_confidence=ConfidenceInterval(base_confidence - 0.1, base_confidence + 0.1)
        )
        
        # 遥测质量评估
        tele_conf, tele_issues = self.evaluate_telemetry_quality(equip_id)
        result.source_confidences["telemetry"] = ConfidenceInterval(
            tele_conf * 0.8, min(1.0, tele_conf + 0.1)
        )
        result.degradation_reasons.extend(tele_issues)
        
        # SVG质量评估
        svg_conf, svg_issues = self.evaluate_svg_quality(equip_id)
        result.source_confidences["svg"] = ConfidenceInterval(
            svg_conf * 0.8, min(1.0, svg_conf + 0.1)
        )
        result.degradation_reasons.extend(svg_issues)
        
        # 数据库质量评估
        db_conf, db_issues = self.evaluate_database_quality(equip_id)
        result.source_confidences["database"] = ConfidenceInterval(
            db_conf * 0.8, min(1.0, db_conf + 0.1)
        )
        result.degradation_reasons.extend(db_issues)
        
        # 根据异常类型调整
        if anomaly_type == "图上有模型无":
            # 主要依赖SVG，排除遥测影响
            result.primary_confidence = ConfidenceInterval(
                svg_conf * 0.7, min(1.0, svg_conf * 0.9)
            )
        elif anomaly_type == "模型有图上无":
            result.primary_confidence = ConfidenceInterval(
                0.7 * base_confidence, 0.9 * base_confidence
            )
        elif anomaly_type.startswith("电气逻辑") or anomaly_type.startswith("RULE-E"):
            # 电气异常主要依赖遥测
            result.primary_confidence = ConfidenceInterval(
                tele_conf * 0.6, min(1.0, tele_conf * 0.85)
            )
        
        # 确定状态
        result.status = result.determine_status()
        
        return result
    
    def generate_enhanced_anomaly_report(
        self,
        defect: dict,
        comprehensive_risk: float = 0.5,
        physical_basis: str = "",
    ) -> EnhancedAnomalyReport:
        """
        生成增强异常报告
        
        参数:
            defect: 原始缺陷字典
            comprehensive_risk: 综合风险值 (0-1)
            physical_basis: 物理依据
        
        返回:
            EnhancedAnomalyReport: 增强异常报告
        """
        equip_id = defect.get("equip_id", "")
        anomaly_type = defect.get("defect_type", defect.get("description", "未知"))
        
        # 计算可信度
        base_conf = defect.get("confidence", 0.8)
        confidence = self.calculate_anomaly_confidence(
            equip_id, anomaly_type, base_conf
        )
        
        # 生成建议
        suggestion = self._generate_suggestion(defect, confidence)
        
        return EnhancedAnomalyReport(
            equip_id=equip_id,
            anomaly_type=anomaly_type,
            comprehensive_risk=comprehensive_risk,
            confidence=confidence,
            physical_basis=physical_basis or defect.get("confidence_reason", ""),
            suggestion=suggestion,
            original_defect=defect,
        )
    
    def _generate_suggestion(self, defect: dict, confidence: Type2FuzzyConfidence) -> str:
        """根据可信度状态生成建议"""
        status = confidence.status
        
        if status == AnomalyStatus.PENDING:
            return "数据不足，建议补充遥测/图模数据后复核"
        
        if status == AnomalyStatus.FALSE_ALARM:
            return "可信度较低，建议现场核查确认是否存在真实异常"
        
        anomaly_type = defect.get("defect_type", "")
        
        if status == AnomalyStatus.CONFIRMED:
            if anomaly_type == "图上有模型无":
                return "建议在数据库中补充该设备记录，并核查SVG图元与实际设备是否匹配"
            elif anomaly_type == "模型有图上无":
                return "建议现场核查该设备是否已退役，或在SVG图中补充图元"
            elif "电气逻辑" in anomaly_type or "RULE-E" in anomaly_type:
                return "建议现场核查设备状态与遥测数据是否一致"
            else:
                return "建议按物理约束校验结果进行整改"
        
        # LIKELY
        if anomaly_type == "图上有模型无":
            return "疑似图模不一致，建议现场核查图元与数据库记录"
        elif anomaly_type == "模型有图上无":
            return "疑似设备缺失，建议现场确认设备状态"
        elif "电气逻辑" in anomaly_type:
            return "疑似电气逻辑异常，建议现场核查设备状态"
        else:
            return "建议现场核查确认"
    
    def generate_batch_report(
        self,
        defects: List[dict],
        comprehensive_risks: Dict[str, float] = None,
        physical_bases: Dict[str, str] = None,
    ) -> List[EnhancedAnomalyReport]:
        """
        批量生成增强异常报告
        
        参数:
            defects: 缺陷列表
            comprehensive_risks: 设备ID -> 综合风险映射
            physical_bases: 设备ID -> 物理依据映射
        
        返回:
            List[EnhancedAnomalyReport]: 增强异常报告列表
        """
        comprehensive_risks = comprehensive_risks or {}
        physical_bases = physical_bases or {}
        
        reports = []
        for defect in defects:
            equip_id = defect.get("equip_id", "")
            risk = comprehensive_risks.get(equip_id, 0.5)
            basis = physical_bases.get(equip_id, "")
            
            report = self.generate_enhanced_anomaly_report(
                defect, risk, basis
            )
            reports.append(report)
        
        # 按风险等级排序
        reports.sort(
            key=lambda x: (
                0 if x.confidence.status == AnomalyStatus.CONFIRMED else 1,
                -x.comprehensive_risk
            )
        )
        
        logger.info(
            f"[II型模糊可信度] 生成{len(reports)}个增强异常报告, "
            f"确认{sum(1 for r in reports if r.confidence.status == AnomalyStatus.CONFIRMED)}个, "
            f"疑似{sum(1 for r in reports if r.confidence.status == AnomalyStatus.LIKELY)}个, "
            f"待复核{sum(1 for r in reports if r.confidence.status == AnomalyStatus.PENDING)}个"
        )
        
        return reports


def format_enhanced_report_table(reports: List[EnhancedAnomalyReport]) -> str:
    """
    格式化增强异常报告为表格字符串
    
    用于终端输出或文档
    """
    if not reports:
        return "无异常报告"
    
    header = "| 异常对象 | 异常类型 | 综合风险 | 可信度区间 | 可信度状态 | 物理依据 | 建议 |"
    separator = "|---|---|---|---|---|---|---|"
    
    rows = []
    for r in reports[:50]:  # 限制显示50条
        ci = r.confidence.primary_confidence
        physical = r.physical_basis[:50] + "..." if len(r.physical_basis) > 50 else r.physical_basis
        suggestion = r.suggestion[:30] + "..." if len(r.suggestion) > 30 else r.suggestion
        
        rows.append(
            f"| {r.equip_id[:15]} | {r.anomaly_type[:10]} | {r.comprehensive_risk:.2f} | "
            f"[{ci.lower:.2f}, {ci.upper:.2f}] | {r.confidence.status.value} | "
            f"{physical} | {suggestion} |"
        )
    
    return "\n".join([header, separator] + rows)


def calculate_confidence_with_interval(
    base_confidence: float,
    telemetry_quality: float,
    svg_quality: float,
    db_quality: float,
) -> Tuple[float, float]:
    """
    计算带区间的可信度
    
    综合考虑各数据源质量，返回(下限, 上限)
    """
    # 基础区间
    base_interval = (base_confidence - 0.1, base_confidence + 0.1)
    
    # 数据质量加权
    quality_weights = {
        "telemetry": 0.4,
        "svg": 0.3,
        "database": 0.3,
    }
    
    # 计算质量因子
    quality_factor = (
        telemetry_quality * quality_weights["telemetry"] +
        svg_quality * quality_weights["svg"] +
        db_quality * quality_weights["database"]
    )
    
    # 调整区间
    lower = max(0.0, base_interval[0] * quality_factor)
    upper = min(1.0, base_interval[1] * (1 + (1 - quality_factor) * 0.2))
    
    return (round(lower, 3), round(upper, 3))
