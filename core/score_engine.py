from __future__ import annotations
import logging
from typing import Any

try:
    from core.telemetry_evaluator import TelemetryEvaluator
    _TELE_OK = True
except (ImportError, NameError):
    TelemetryEvaluator = None  # type: ignore
    _TELE_OK = False
from core.constants import SCORE_WEIGHTS, SCORE_CAPS

logger = logging.getLogger(__name__)


class ScoreAndConfidenceEngine:
    """
    评分与置信度引擎（对齐基线规范 v1.1）：
    - 四维权重：拓扑完整性5 / 图模一致性3 / 电气逻辑2 / 接口规范性4
    - 维度扣分上限：SCORE_CAPS 控制单维度不会一次性被扣穿
    - score_after = 基于修复建议推演的修正后评分（不再恒等于score_before）
    """

    DEDUCTION_WEIGHTS = {
        "拓扑完整性": SCORE_WEIGHTS["拓扑完整性"],
        "图模一致性": SCORE_WEIGHTS["图模一致性"],
        "电气逻辑": SCORE_WEIGHTS["电气逻辑"],
        "接口规范性": SCORE_WEIGHTS["接口规范性"],
    }

    DIMENSION_CAPS = SCORE_CAPS

    def __init__(self, tele_evaluator: Any = None):
        if _TELE_OK:
            self.evaluator = tele_evaluator or TelemetryEvaluator()
        else:
            self.evaluator = None
            logger.warning("ScoreEngine: TelemetryEvaluator 未可用，置信度仅采用静态权重")

    def _dimension_of(self, defect: dict) -> str:
        """根据defect维度或类型推断所属评分维度。"""
        if defect.get("dimension") and defect["dimension"] in self.DEDUCTION_WEIGHTS:
            return defect["dimension"]
        d_type = defect.get("defect_type", "")
        if d_type in {"孤岛设备", "飞线-悬空端点", "飞线-端点偏离设备",
                      "虚假连通", "设备重叠", "标注错位"}:
            return "拓扑完整性"
        if d_type in {"图上有模型无", "模型有图上无", "物理连接不一致", "逻辑连接不一致"}:
            return "图模一致性"
        if d_type.startswith("RULE-E") or "电气" in d_type or "合位" in d_type or "分位" in d_type:
            return "电气逻辑"
        if "接口" in d_type or "主配" in d_type or "漏拼" in d_type or "错拼" in d_type:
            return "接口规范性"
        return "拓扑完整性"

    def calculate_defect_confidence(self, defect: dict) -> tuple[float, str]:
        """为单条缺陷计算置信度与可解释性依据。"""
        d_type = defect.get("defect_type", "")
        equip_id = defect.get("equip_id", "")
        rule_code = defect.get("rule_code", "")

        base_confidence = 0.80
        reasons = ["图模静态结构比对 (+0.80)"]

        if self.evaluator is not None:
            if d_type in ("逻辑连接不一致",) or rule_code.startswith("E"):
                try:
                    is_valid, tele_conf, tele_reason = self.evaluator.evaluate_switch_status(
                        equip_id, svg_is_open=False
                    )
                    if not is_valid:
                        base_confidence += 0.15
                        reasons.append(f"遥信校验强化: {tele_reason} (+0.15)")
                except Exception as e:
                    logger.debug("evaluate_switch_status失败: %s", e)
            elif d_type == "物理连接不一致":
                try:
                    is_valid, tele_conf, tele_reason = self.evaluator.evaluate_kcl_conservation(
                        equip_id, []
                    )
                    base_confidence += 0.10 if is_valid else 0.12
                    reasons.append(f"KCL校验加权: {tele_reason} (+0.10)")
                except Exception:
                    reasons.append("KCL数据不可用，沿用静态置信度")
            elif d_type == "图上有模型无":
                base_confidence += 0.12
                reasons.append("SVG图元与SQL主键匹配失败 (+0.12)")
            elif d_type == "模型有图上无":
                base_confidence += 0.10
                reasons.append("SQL设备SVG缺失图元 (+0.10)")
            elif rule_code.startswith("RULE-E"):
                base_confidence += 0.14
                reasons.append(f"遥测{rule_code}直接命中 (+0.14)")

        final_confidence = min(round(base_confidence, 2), 1.00)
        return final_confidence, " | ".join(reasons)

    def evaluate_quality_score(
        self, defects_report: list[dict], total_equip_count: int,
        repaired_defect_ids: list | None = None,
    ) -> dict:
        """
        计算图模质量评分（按维度封顶 + 缺陷率加权扣分 + 缺陷数量惩罚）。
        - repaired_defect_ids: 已闭环修复的defect索引或id，从score_after中扣除其扣分
        - 评分逻辑：
          1. 使用固定基准容量（10000），使评分对缺陷扣分更敏感
          2. 增加缺陷率惩罚：缺陷数量/设备总数 超过阈值时额外扣分
        """
        total_deduction = 0.0
        dim_deduction = {k: 0.0 for k in self.DEDUCTION_WEIGHTS}
        processed_defects = []
        repaired_defect_ids = set(repaired_defect_ids or [])

        for idx, defect in enumerate(defects_report):
            conf, reason = self.calculate_defect_confidence(defect)
            dim = self._dimension_of(defect)
            weight = self.DEDUCTION_WEIGHTS.get(dim, 1.0)

            per_defect_deduction = round(weight * conf, 2)
            cap = self.DIMENSION_CAPS.get(dim, 9999)
            if dim_deduction[dim] + per_defect_deduction > cap:
                per_defect_deduction = round(max(cap - dim_deduction[dim], 0.0), 2)

            dim_deduction[dim] = round(dim_deduction[dim] + per_defect_deduction, 2)
            total_deduction += per_defect_deduction

            defect_copy = dict(defect)
            defect_copy["confidence"] = conf
            defect_copy["confidence_reason"] = reason
            defect_copy["score_deduction"] = per_defect_deduction
            defect_copy["dimension"] = dim
            defect_copy["_idx"] = idx
            processed_defects.append(defect_copy)

        # 使用固定基准容量，使评分对缺陷扣分更敏感
        base_capacity = 10000.0
        penalty_ratio = min(total_deduction / base_capacity, 1.0)

        # 缺陷率惩罚：缺陷数量/设备总数 超过阈值时额外扣分
        defect_count = len(defects_report)
        defect_rate = defect_count / max(total_equip_count, 1)
        # 缺陷率超过 1% 开始惩罚，超过 5% 严重惩罚
        defect_rate_penalty = 0.0
        if defect_rate > 0.05:
            defect_rate_penalty = min((defect_rate - 0.05) * 500, 30.0)  # 最多扣30分
        elif defect_rate > 0.01:
            defect_rate_penalty = (defect_rate - 0.01) * 200

        score_before = round(max((1.0 - penalty_ratio) * 100.0 - defect_rate_penalty, 0.0), 1)

        repaired_sum = 0.0
        for d in processed_defects:
            if d.get("_idx") in repaired_defect_ids or d.get("equip_id") in repaired_defect_ids:
                repaired_sum += d["score_deduction"]
        after_total = round(max(total_deduction - repaired_sum, 0.0), 2)
        after_ratio = min(after_total / base_capacity, 1.0)
        # 修复后也需要重新计算缺陷率惩罚
        repaired_defect_count = len(repaired_defect_ids) if repaired_defect_ids else 0
        after_defect_rate = (defect_count - repaired_defect_count) / max(total_equip_count, 1)
        after_rate_penalty = 0.0
        if after_defect_rate > 0.05:
            after_rate_penalty = min((after_defect_rate - 0.05) * 500, 30.0)
        elif after_defect_rate > 0.01:
            after_rate_penalty = (after_defect_rate - 0.01) * 200
        score_after = round(max((1.0 - after_ratio) * 100.0 - after_rate_penalty, 0.0), 1)
        if not repaired_defect_ids:
            score_after = score_before

        logger.info(
            "评分结果: 设备=%d 缺陷=%d 扣分=%.2f 缺陷率=%.2f%% 缺陷率扣分=%.2f score_before=%.1f score_after=%.1f",
            total_equip_count, defect_count, total_deduction, defect_rate * 100, defect_rate_penalty,
            score_before, score_after,
        )

        return {
            "score_before": score_before,
            "score_after": score_after,
            "total_deduction": round(total_deduction, 2),
            "dimension_deduction": {k: round(v, 2) for k, v in dim_deduction.items()},
            "defect_count": len(defects_report),
            "defect_rate": round(defect_rate * 100, 2),  # 缺陷率百分比
            "defect_rate_penalty": round(defect_rate_penalty, 2),
            "processed_defects": processed_defects,
        }
