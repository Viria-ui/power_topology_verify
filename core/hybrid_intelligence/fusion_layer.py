"""
融合决策层模块 (Fusion Layer)
============================

三路信号（GNNGAT / 时空模型 / 规则引擎）的加权融合 + 置信度计算。

融合策略（优先级递减）：
  1. 规则命中 → 高置信度直接输出（确定性规则零误判）
  2. 三路全阳性 → 高置信度确认（协同验证）
  3. 两路阳性 → 中高置信度（部分验证）
  4. 单路阳性 → 中等置信度（单一来源）
  5. 三路矛盾 → 降级为"需人工复核"（低置信度）
  6. 全部阴性 → 正常（置信度=0.95）

置信度计算公式：
  confidence = max(rule_conf, gnn_conf×w_gnn + temporal_conf×w_temp + rule_conf×w_rule)
  其中 w_gnn + w_temp + w_rule = 1

异常等级（综合分数）：
  - ≥ 0.75 → 高（高风险，需立即处理）
  - ≥ 0.45 → 中（中风险，需跟踪）
  - ≥ 0.25 → 低（低风险，建议关注）
  - < 0.25 → 正常
"""

from __future__ import annotations
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

import numpy as np

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# 融合结果数据结构
# ------------------------------------------------------------------

@dataclass
class FusionResult:
    """单设备融合决策结果"""
    equip_id: str

    # 三路独立信号
    gnn_score: float           # GNN 异常分数 [0, 1]
    temporal_score: float      # 时空模型异常分数 [0, 1]
    rule_score: float         # 规则命中置信度 [0, 1]

    # 融合结果
    fused_score: float        # 融合异常分数 [0, 1]
    confidence: float         # 融合置信度 [0, 1]
    risk_level: str          # 高/中/低/正常
    status: str              # CONFIRMED / LIKELY / SUSPECTED / NEED_REVIEW / NORMAL

    # 异常信息
    anomaly_type: str         # 异常类型（取最高置信度路数的类型）
    detail: str              # 详细说明
    evidence: dict           # 证据字典（各路输出）

    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "gnn_score": round(self.gnn_score, 4),
            "temporal_score": round(self.temporal_score, 4),
            "rule_score": round(self.rule_score, 4),
            "fused_score": round(self.fused_score, 4),
            "confidence": round(self.confidence, 4),
            "risk_level": self.risk_level,
            "status": self.status,
            "anomaly_type": self.anomaly_type,
            "detail": self.detail,
        }


@dataclass
class FusionSummary:
    """全局融合摘要"""
    total_devices: int
    gnn_anomaly_count: int
    temporal_anomaly_count: int
    rule_anomaly_count: int
    fused_anomaly_count: int
    high_risk_count: int
    medium_risk_count: int
    confirmed_count: int
    need_review_count: int
    results: List[FusionResult]

    def to_dict(self) -> dict:
        return {
            "total_devices": self.total_devices,
            "gnn_anomaly_count": self.gnn_anomaly_count,
            "temporal_anomaly_count": self.temporal_anomaly_count,
            "rule_anomaly_count": self.rule_anomaly_count,
            "fused_anomaly_count": self.fused_anomaly_count,
            "high_risk_count": self.high_risk_count,
            "medium_risk_count": self.medium_risk_count,
            "confirmed_count": self.confirmed_count,
            "need_review_count": self.need_review_count,
        }


# ------------------------------------------------------------------
# 融合决策器
# ------------------------------------------------------------------

class FusionLayer:
    """
    三路融合决策器

    参数:
        gnn_weight: GNN 路权重（默认 0.30）
        temporal_weight: 时空模型权重（默认 0.25）
        rule_weight: 规则引擎权重（默认 0.45）
        rule_confidence_override: 规则命中时置信度下限（默认 0.90）
    """

    # 异常分数阈值
    THRESHOLD_HIGH = 0.75
    THRESHOLD_MEDIUM = 0.45
    THRESHOLD_LOW = 0.25

    # 异常类型优先级（数值越高越优先展示）
    ANOMALY_TYPE_PRIORITY = {
        "电气逻辑异常": 5,
        "图模一致性异常": 4,
        "疑似联络开关": 3,
        "正常": 0,
    }

    def __init__(
        self,
        gnn_weight: float = 0.30,
        temporal_weight: float = 0.25,
        rule_weight: float = 0.45,
        rule_confidence_override: float = 0.90,
    ):
        self.gnn_weight = gnn_weight
        self.temporal_weight = temporal_weight
        self.rule_weight = rule_weight
        self.rule_confidence_override = rule_confidence_override

        # 权重归一化
        total = gnn_weight + temporal_weight + rule_weight
        self.gnn_weight /= total
        self.temporal_weight /= total
        self.rule_weight /= total

    def fuse(
        self,
        gnn_results: List,    # List[GNNAnomalyResult]
        temporal_results: List,  # List[TemporalAnomalyResult]
        rule_hits: List,       # List[RuleHit]
    ) -> FusionSummary:
        """
        执行三路融合，返回所有设备的综合决策

        融合逻辑：
        1. 规则引擎命中 → 置信度上界为 rule_confidence_override（确定性）
        2. GNN + 时空 + 规则全阳性 → 高置信度确认
        3. 权重加权融合
        4. 三路矛盾时降级为 NEED_REVIEW
        """
        # Step 1: 规则命中按设备聚合
        rule_by_equip: Dict[str, List] = {}
        for hit in rule_hits:
            eid = hit.equip_id
            if eid not in rule_by_equip:
                rule_by_equip[eid] = []
            rule_by_equip[eid].append(hit)

        # Step 2: GNN / 时空结果按设备建立索引
        gnn_by_equip: Dict[str, object] = {}
        for r in gnn_results:
            gnn_by_equip[r.equip_id] = r

        temp_by_equip: Dict[str, object] = {}
        for r in temporal_results:
            temp_by_equip[r.equip_id] = r

        # Step 3: 收集所有设备ID
        all_ids = set(gnn_by_equip.keys())
        all_ids |= set(temp_by_equip.keys())
        all_ids |= set(rule_by_equip.keys())

        results: List[FusionResult] = []

        for equip_id in all_ids:
            gr = gnn_by_equip.get(equip_id)
            tr = temp_by_equip.get(equip_id)
            rh_list = rule_by_equip.get(equip_id, [])

            fused = self._fuse_single(
                equip_id, gr, tr, rh_list
            )
            results.append(fused)

        # Step 4: 汇总
        summary = FusionSummary(
            total_devices=len(results),
            gnn_anomaly_count=sum(
                1 for r in results if r.gnn_score >= self.THRESHOLD_MEDIUM
            ),
            temporal_anomaly_count=sum(
                1 for r in results if r.temporal_score >= self.THRESHOLD_MEDIUM
            ),
            rule_anomaly_count=sum(
                1 for r in results if r.rule_score >= self.THRESHOLD_MEDIUM
            ),
            fused_anomaly_count=sum(
                1 for r in results if r.fused_score >= self.THRESHOLD_LOW
            ),
            high_risk_count=sum(1 for r in results if r.risk_level == "高"),
            medium_risk_count=sum(1 for r in results if r.risk_level == "中"),
            confirmed_count=sum(1 for r in results if r.status == "CONFIRMED"),
            need_review_count=sum(1 for r in results if r.status == "NEED_REVIEW"),
            results=results,
        )

        logger.info(
            "[融合层] 完成: %d 设备, GNN异常=%d, 时空异常=%d, 规则异常=%d, "
            "融合异常=%d, 高风险=%d, 确认=%d, 待复核=%d",
            summary.total_devices,
            summary.gnn_anomaly_count,
            summary.temporal_anomaly_count,
            summary.rule_anomaly_count,
            summary.fused_anomaly_count,
            summary.high_risk_count,
            summary.confirmed_count,
            summary.need_review_count,
        )

        return summary

    def _fuse_single(
        self,
        equip_id: str,
        gnn_result,     # GNNAnomalyResult | None
        temp_result,    # TemporalAnomalyResult | None
        rule_hits: List,
    ) -> FusionResult:
        """融合单设备的三路信号"""

        # 提取分数
        gnn_score = gnn_result.anomaly_prob if gnn_result else 0.0
        gnn_type = gnn_result.anomaly_type if gnn_result else "正常"

        temporal_score = temp_result.anomaly_score if temp_result else 0.0
        temp_type = temp_result.anomaly_type if temp_result else "NORMAL"

        # 规则分数：取命中规则中最高置信度
        rule_score = 0.0
        rule_type = "正常"
        if rule_hits:
            rule_score = max(hit.confidence for hit in rule_hits)
            # 取最高优先级的异常类型
            hit_types = [hit.anomaly_type for hit in rule_hits if hit.anomaly_type]
            rule_type = max(
                hit_types,
                key=lambda t: self.ANOMALY_TYPE_PRIORITY.get(t, 0)
            ) if hit_types else "正常"

        # === 融合策略 ===

        # 策略 A: 确定性规则命中 → 直接以规则为准
        has_deterministic_rule = any(hit.is_deterministic and hit.confidence >= 0.9
                                      for hit in rule_hits)
        if has_deterministic_rule:
            fused_score = max(gnn_score, temporal_score, rule_score)
            confidence = self.rule_confidence_override
            status = "CONFIRMED"
            anomaly_type = rule_type
            detail = (
                f"确定性规则命中（{len(rule_hits)}条），置信度 override={confidence:.2f}。"
                f"规则类型: {rule_type}"
            )
        else:
            # 策略 B: 加权融合
            gnn_contrib = gnn_score * self.gnn_weight
            temp_contrib = temporal_score * self.temporal_weight
            rule_contrib = rule_score * self.rule_weight
            fused_score = gnn_contrib + temp_contrib + rule_contrib

            # 策略 C: 多路协同验证（提升置信度）
            active_signals = sum(1 for s in [gnn_score, temporal_score, rule_score]
                                if s >= self.THRESHOLD_LOW)
            if active_signals >= 3:
                confidence = 0.90
                status = "CONFIRMED"
                anomaly_type = self._best_type(gnn_type, temp_type, rule_type)
                detail = "三路信号全阳性，协同验证确认异常"
            elif active_signals == 2:
                confidence = 0.75
                status = "LIKELY"
                anomaly_type = self._best_type(gnn_type, temp_type, rule_type)
                detail = "两路信号阳性，部分验证"
            elif active_signals == 1:
                confidence = 0.55
                status = "SUSPECTED"
                anomaly_type = gnn_type if gnn_score > 0 else (temp_type if temporal_score > 0 else rule_type)
                detail = "单路信号阳性，置信度降级"
            else:
                confidence = 0.95
                status = "NORMAL"
                anomaly_type = "正常"
                detail = "三路信号均为阴性，判定正常"

            # 策略 D: 三路矛盾检测（降级）
            if active_signals >= 1:
                scores = [gnn_score, temporal_score, rule_score]
                mean_s = sum(scores) / len(scores)
                std_s = np.std(scores) if len(scores) > 1 else 0.0
                if std_s > 0.35 and mean_s > 0.3:
                    # 三路差异大，矛盾 → 降级为 NEED_REVIEW
                    confidence = 0.40
                    status = "NEED_REVIEW"
                    detail = (
                        f"三路信号矛盾（GNN={gnn_score:.2f}, 时空={temporal_score:.2f}, "
                        f"规则={rule_score:.2f}），需人工复核"
                    )

        # === 风险等级 ===
        if fused_score >= self.THRESHOLD_HIGH:
            risk_level = "高"
        elif fused_score >= self.THRESHOLD_MEDIUM:
            risk_level = "中"
        elif fused_score >= self.THRESHOLD_LOW:
            risk_level = "低"
        else:
            risk_level = "正常"

        return FusionResult(
            equip_id=equip_id,
            gnn_score=gnn_score,
            temporal_score=temporal_score,
            rule_score=rule_score,
            fused_score=fused_score,
            confidence=confidence,
            risk_level=risk_level,
            status=status,
            anomaly_type=anomaly_type,
            detail=detail,
            evidence={
                "gnn": gnn_result.to_dict() if gnn_result else None,
                "temporal": temp_result.to_dict() if temp_result else None,
                "rule_hits": [h.to_dict() for h in rule_hits],
            },
        )

    @staticmethod
    def _best_type(t1: str, t2: str, t3: str) -> str:
        """选择最高优先级的异常类型"""
        priority = FusionLayer.ANOMALY_TYPE_PRIORITY
        types = [t1, t2, t3]
        return max(
            types,
            key=lambda t: priority.get(t, 0)
        )

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def get_high_risk_results(self, summary: FusionSummary) -> List[FusionResult]:
        """获取高风险融合结果"""
        return [r for r in summary.results if r.risk_level == "高"]

    def get_need_review_results(self, summary: FusionSummary) -> List[FusionResult]:
        """获取需要人工复核的结果"""
        return [r for r in summary.results if r.status == "NEED_REVIEW"]

    def get_abnormal_results(
        self,
        summary: FusionSummary,
        min_score: float = 0.45,
    ) -> List[FusionResult]:
        """获取异常结果（分数≥min_score）"""
        return [r for r in summary.results if r.fused_score >= min_score]
