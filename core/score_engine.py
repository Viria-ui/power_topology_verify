from __future__ import annotations

from typing import Any

from core.telemetry_evaluator import TelemetryEvaluator


class ScoreAndConfidenceEngine:
    """评分与置信度引擎。

    评分公式按规范直接计算：
        Model_Score = 100 - sum(W_i * C_i)
    其中 W_i 为规则所属维度权重，C_i 为该缺陷的可解释置信度。
    每个维度设置封顶扣分，避免同一类问题无限放大。
    """

    DIMENSION_WEIGHTS = {
        "拓扑完整性": 5.0,
        "图模一致性": 3.0,
        "电气逻辑": 2.0,
        "接口规范性": 4.0,
    }

    DIMENSION_CAPS = {
        "拓扑完整性": 30.0,
        "图模一致性": 25.0,
        "电气逻辑": 20.0,
        "接口规范性": 25.0,
    }

    DEFECT_DIMENSION_KEYWORDS = {
        "拓扑完整性": ["悬空", "孤岛", "断连", "端点缺失", "断点", "拓扑缺失"],
        "图模一致性": ["图上有模型无", "模型有图上无", "物理连接不一致", "逻辑连接不一致", "图模"],
        "电气逻辑": ["遥信", "遥测", "电流", "电压", "功率", "合环", "分位", "合位", "三相不平衡"],
        "接口规范性": ["主配接口", "接口缺失", "馈线归属", "厂站归属", "间隔"],
    }

    # 保留旧字段名语义，供外部调用时仍可按 defect_type 查询基础权重。
    DEDUCTION_WEIGHTS = {
        "图上有模型无": DIMENSION_WEIGHTS["图模一致性"],
        "模型有图上无": DIMENSION_WEIGHTS["图模一致性"],
        "物理连接不一致": DIMENSION_WEIGHTS["图模一致性"],
        "逻辑连接不一致": DIMENSION_WEIGHTS["图模一致性"],
        "主配接口缺失": DIMENSION_WEIGHTS["接口规范性"],
        "悬空": DIMENSION_WEIGHTS["拓扑完整性"],
        "孤岛": DIMENSION_WEIGHTS["拓扑完整性"],
        "断连": DIMENSION_WEIGHTS["拓扑完整性"],
        "电气逻辑异常": DIMENSION_WEIGHTS["电气逻辑"],
    }

    REVIEW_STATUS_VALUES = {"待人工复核", "review", "manual_review", "suspect", "SUSPECT"}
    FIXED_STATUS_VALUES = {"已修复", "修复完成", "fixed", "resolved", "pass", "PASS", "通过"}

    def __init__(self, tele_evaluator=None):
        self.evaluator = tele_evaluator or TelemetryEvaluator()

    def calculate_defect_confidence(self, defect: dict[str, Any]):
        """为单条缺陷计算置信度与可解释性依据。"""
        d_type = str(defect.get("defect_type", "") or "")
        equip_id = str(defect.get("equip_id", "") or "")
        description = str(defect.get("description", "") or "")

        confidence = 0.65
        reasons = ["基础结构/规则命中置信度 0.65"]

        if any(key in d_type for key in ["物理连接不一致", "逻辑连接不一致", "主配接口缺失"]):
            confidence += 0.15
            reasons.append("缺陷类型属于强结构约束 (+0.15)")
        if any(key in d_type + description for key in ["遥信", "遥测", "电流", "电压", "功率"]):
            confidence += 0.10
            reasons.append("包含电气量测辅助证据 (+0.10)")
        if any(key in d_type + description for key in ["SVG", "SQL", "数据库", "图纸"]):
            confidence += 0.08
            reasons.append("包含图纸/数据库交叉证据 (+0.08)")
        if "TMP" in equip_id or "UNKNOWN" in equip_id.upper():
            confidence -= 0.10
            reasons.append("设备ID为临时或未知，需降低置信度 (-0.10)")
        if not equip_id or not d_type:
            confidence -= 0.15
            reasons.append("缺少设备ID或缺陷类型，需人工复核 (-0.15)")

        final_confidence = max(0.20, min(round(confidence, 2), 1.00))
        return final_confidence, " | ".join(reasons)

    def evaluate_quality_score(self, defects_report, total_equip_count=None, repaired_defects=None):
        """计算图模质量评分。

        total_equip_count 参数保留兼容旧调用，但评分不再按设备数归一化。
        repaired_defects 可传入修复后的缺陷清单；未传时按状态字段识别已修复项。
        """
        before = self._score_defects(defects_report or [])
        after_source = repaired_defects if repaired_defects is not None else self._remaining_after_status(defects_report or [])
        after = self._score_defects(after_source or [])

        return {
            "score_before": before["score"],
            "score_after": after["score"],
            "total_deduction": before["total_deduction"],
            "defect_count": len(defects_report or []),
            "dimension_deductions": before["dimension_deductions"],
            "dimension_caps": dict(self.DIMENSION_CAPS),
            "dimension_weights": dict(self.DIMENSION_WEIGHTS),
            "scoring_formula": "Model_Score = 100 - Σ(W_i * C_i), dimension deductions capped at 30/25/20/25",
            "processed_defects": before["processed_defects"],
            "score_after_basis": "repaired_defects" if repaired_defects is not None else "status fields in defects_report",
        }

    def _score_defects(self, defects: list[dict[str, Any]]):
        raw_dimension_deductions = {dimension: 0.0 for dimension in self.DIMENSION_WEIGHTS}
        processed_defects = []

        for defect in defects:
            conf, reason = self.calculate_defect_confidence(defect)
            dimension = self._classify_dimension(defect)
            weight = self.DIMENSION_WEIGHTS[dimension]
            deduction = round(weight * conf, 2)
            raw_dimension_deductions[dimension] += deduction

            defect_copy = dict(defect)
            defect_copy["dimension"] = dimension
            defect_copy["confidence"] = conf
            defect_copy["confidence_reason"] = reason
            defect_copy["score_weight"] = weight
            defect_copy["score_deduction"] = deduction
            defect_copy["review_required"] = self._requires_review(defect)
            processed_defects.append(defect_copy)

        capped = {
            dimension: round(min(value, self.DIMENSION_CAPS[dimension]), 2)
            for dimension, value in raw_dimension_deductions.items()
        }
        total_deduction = round(sum(capped.values()), 2)
        return {
            "score": round(max(0.0, 100.0 - total_deduction), 1),
            "total_deduction": total_deduction,
            "dimension_deductions": capped,
            "processed_defects": processed_defects,
        }

    def _classify_dimension(self, defect: dict[str, Any]) -> str:
        text = " ".join(
            str(defect.get(key, "") or "")
            for key in ["dimension", "rule_dimension", "defect_type", "description", "suggestion"]
        )
        for dimension, keywords in self.DEFECT_DIMENSION_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return dimension
        return "拓扑完整性"

    def _remaining_after_status(self, defects: list[dict[str, Any]]):
        remaining = []
        for defect in defects:
            status = str(defect.get("status", defect.get("result", defect.get("label", ""))) or "")
            if status in self.FIXED_STATUS_VALUES:
                continue
            remaining.append(defect)
        return remaining

    def _requires_review(self, defect: dict[str, Any]) -> bool:
        text = " ".join(str(defect.get(key, "") or "") for key in ["status", "label", "description", "suggestion"])
        if any(value in text for value in self.REVIEW_STATUS_VALUES):
            return True
        return any(key in text for key in ["高风险", "疑似", "不确定", "待人工复核", "禁止直接自动"])
