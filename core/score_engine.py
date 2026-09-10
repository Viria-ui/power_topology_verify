from __future__ import annotations
import logging
from typing import Any

try:
    from core.telemetry_evaluator import TelemetryEvaluator
    _TELE_OK = True
except (ImportError, NameError):
    TelemetryEvaluator = None  # type: ignore
    _TELE_OK = False
from core.constants import (
    SCORE_WEIGHTS, SCORE_CAPS,
    RUN_EFFICIENCY_THRESHOLDS, BEAUTY_QUALITY_WEIGHTS,
)

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
        【S7修复】评分公式对齐规范（规范书v1.1 + 电气逻辑校验规则v1.0 第五章）：
            Model_Score = 100 - Σ(W_i × C_i)
          - W_i：维度权重 拓扑5 / 图模3 / 电气2 / 接口4
          - C_i：该维度缺陷**处数**（不再按置信度打折，不再叠加缺陷率惩罚）
          - 单维度扣分上限：拓扑30 / 图模25 / 电气20 / 接口25
          - score_after = 移除已修复缺陷处数后的重算评分
        """
        repaired_defect_ids = set(repaired_defect_ids or [])
        dim_count: dict[str, int] = {k: 0 for k in self.DEDUCTION_WEIGHTS}
        processed_defects = []

        for idx, defect in enumerate(defects_report):
            conf, reason = self.calculate_defect_confidence(defect)
            dim = self._dimension_of(defect)
            weight = self.DEDUCTION_WEIGHTS.get(dim, 1.0)
            dim_count[dim] = dim_count.get(dim, 0) + 1

            defect_copy = dict(defect)
            defect_copy["confidence"] = conf
            defect_copy["confidence_reason"] = reason
            defect_copy["score_deduction"] = round(weight, 2)  # 规范：每处扣W_i分
            defect_copy["dimension"] = dim
            defect_copy["_idx"] = idx
            processed_defects.append(defect_copy)

        def compute(count_map: dict[str, int]):
            total = 0.0
            dim_ded = {}
            for dim, cnt in count_map.items():
                w = self.DEDUCTION_WEIGHTS.get(dim, 1.0)
                cap = self.DIMENSION_CAPS.get(dim, 9999)
                ded = min(cnt * w, cap)
                dim_ded[dim] = round(ded, 2)
                total += ded
            return round(total, 2), dim_ded

        total_deduction, dim_deduction = compute(dim_count)
        defect_count = len(defects_report)
        defect_rate = defect_count / max(total_equip_count, 1)

        # score_before = 100 - Σ(W_i × C_i)（维度封顶）
        score_before = round(max(100.0 - total_deduction, 0.0), 1)

        # score_after：从维度计数中移除已修复缺陷处数后重算
        if repaired_defect_ids:
            after_count = dict(dim_count)
            for d in processed_defects:
                if d.get("_idx") in repaired_defect_ids or d.get("equip_id") in repaired_defect_ids:
                    dim = d["dimension"]
                    after_count[dim] = max(after_count[dim] - 1, 0)
            after_deduction, _ = compute(after_count)
            score_after = round(max(100.0 - after_deduction, 0.0), 1)
        else:
            score_after = score_before

        logger.info(
            "评分结果(规范公式): 设备=%d 缺陷=%d 维度扣分=%.2f score_before=%.1f score_after=%.1f",
            total_equip_count, defect_count, total_deduction,
            score_before, score_after,
        )

        return {
            "score_before": score_before,
            "score_after": score_after,
            "total_deduction": round(total_deduction, 2),
            "dimension_deduction": {k: round(v, 2) for k, v in dim_deduction.items()},
            "defect_count": defect_count,
            "defect_rate": round(defect_rate * 100, 2),  # 缺陷率百分比（仅展示，不参与扣分）
            "defect_rate_penalty": 0.0,  # 【S7修复】规范公式无缺陷率惩罚
            "processed_defects": processed_defects,
        }

    # ──────────────────────────────────────────────────────────────────
    # 【Q44修复】运行效率 + 图形美观性评分（对齐任务书初赛5维度）
    #   - 数据质量分：score_before / score_after（已有）
    #   - 运行效率分：基于端到端执行时长（满分100，>10秒开始扣分）
    #   - 图形美观性分：基于美化后 SVG 4 子项评分（满分100）
    # ──────────────────────────────────────────────────────────────────
    @staticmethod
    def calc_run_efficiency(elapsed_seconds: float) -> dict:
        """【Q44】运行效率评分：≤10s 满分100，每多10s扣5分，封顶扣10分。"""
        th = RUN_EFFICIENCY_THRESHOLDS
        if elapsed_seconds <= th["perfect_seconds"]:
            deduction = 0.0
        else:
            extra_10s = (elapsed_seconds - th["perfect_seconds"]) / 10.0
            deduction = min(extra_10s * th["per_extra_10s"], th["cap_deduction"])
        score = round(max(100.0 - deduction, 0.0), 1)
        return {
            "elapsed_seconds": round(elapsed_seconds, 2),
            "score": score,
            "deduction": round(deduction, 2),
            "grade": "优" if score >= 95 else "良" if score >= 85 else "中" if score >= 70 else "差",
        }

    @staticmethod
    def calc_beauty_quality(svg_quality_report: dict | None) -> dict:
        """【Q44】图形美观性评分：4 子项各25分，满分100。"""
        weights = BEAUTY_QUALITY_WEIGHTS
        sub = {
            "viewbox_ok": 0.0,
            "no_overlap": 0.0,
            "orthogonal_routing": 0.0,
            "metadata_preserved": 0.0,
        }
        if svg_quality_report:
            # 子项1：viewBox 完整且不超界
            vb = svg_quality_report.get("viewbox_ok") or svg_quality_report.get("viewbox")
            if vb is not False and vb != [0, 0, 0, 0]:
                sub["viewbox_ok"] = weights["viewbox_ok"]
            # 子项2：无大面积重叠
            # 【Q44-Fix】支持两种报告格式：
            #   - quality_scorer.evaluate_svg_quality() 输出 overlap_found 布尔
            #   - 美化质量对比报告 输出 overlap_count 数值（>0 = 有重叠）
            overlap_count = svg_quality_report.get("overlap_count", 0)
            has_overlap = overlap_count > 0 or svg_quality_report.get("overlap_found", False)
            if not has_overlap:
                sub["no_overlap"] = weights["no_overlap"]
            # 子项3：正交布线（routing_score > 0.8 即合格）
            routing = svg_quality_report.get("routing_score", 1.0)
            if routing >= 0.8:
                sub["orthogonal_routing"] = weights["orthogonal_routing"]
            elif routing >= 0.5:
                sub["orthogonal_routing"] = weights["orthogonal_routing"] * routing
            # 子项4：元数据保留
            meta = svg_quality_report.get("metadata_preserved", True)
            if meta:
                sub["metadata_preserved"] = weights["metadata_preserved"]
        else:
            # 无 SVG 时按 75% 兜底（不阻断流程）
            sub = {k: v * 0.75 for k, v in sub.items()}

        total = sum(sub.values())
        return {
            "sub_scores": {k: round(v, 2) for k, v in sub.items()},
            "score": round(total, 1),
            "grade": "优" if total >= 90 else "良" if total >= 75 else "中" if total >= 60 else "差",
        }

    def evaluate_comprehensive_score(
        self,
        defects_report: list[dict],
        total_equip_count: int,
        elapsed_seconds: float = 0.0,
        svg_quality_report: dict | None = None,
        repaired_defect_ids: list | None = None,
    ) -> dict:
        """【Q44】综合评分：数据质量40% + 运行效率30% + 图形美观性30%。
        （任务书初赛5维度：完成度/效率/完整性/修复合理性/美观性 — 前4者折算到数据质量）
        """
        base = self.evaluate_quality_score(
            defects_report, total_equip_count, repaired_defect_ids=repaired_defect_ids
        )
        eff = self.calc_run_efficiency(elapsed_seconds)
        beauty = self.calc_beauty_quality(svg_quality_report)
        comprehensive = round(
            base["score_after"] * 0.40
            + eff["score"] * 0.30
            + beauty["score"] * 0.30,
            1,
        )
        result = dict(base)
        result["run_efficiency"] = eff
        result["beauty_quality"] = beauty
        result["comprehensive_score"] = comprehensive
        result["comprehensive_grade"] = (
            "优" if comprehensive >= 90
            else "良" if comprehensive >= 75
            else "中" if comprehensive >= 60
            else "差"
        )
        return result
