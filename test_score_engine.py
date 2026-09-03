import unittest

from core.score_engine import ScoreAndConfidenceEngine


class ScoreAndConfidenceEngineTest(unittest.TestCase):
    def test_score_after_is_not_hardcoded_to_100(self):
        engine = ScoreAndConfidenceEngine()
        defects = [
            {
                "equip_id": "EQ001",
                "defect_type": "物理连接不一致",
                "description": "SVG图纸存在物理连接，但数据库拓扑中缺失该连线",
            }
        ]

        summary = engine.evaluate_quality_score(defects, total_equip_count=100)

        self.assertLess(summary["score_before"], 100)
        self.assertLess(summary["score_after"], 100)
        self.assertIn("dimension_deductions", summary)

    def test_score_after_uses_fixed_status_when_no_repaired_list(self):
        engine = ScoreAndConfidenceEngine()
        defects = [
            {
                "equip_id": "EQ001",
                "defect_type": "物理连接不一致",
                "description": "数据库拓扑中缺失连线",
                "status": "已修复",
            }
        ]

        summary = engine.evaluate_quality_score(defects, total_equip_count=100)

        self.assertLess(summary["score_before"], 100)
        self.assertEqual(summary["score_after"], 100)

    def test_dimension_cap_is_applied(self):
        engine = ScoreAndConfidenceEngine()
        defects = [
            {"equip_id": f"EQ{i:03d}", "defect_type": "悬空", "description": "非末端设备单端悬空"}
            for i in range(20)
        ]

        summary = engine.evaluate_quality_score(defects, total_equip_count=1)

        self.assertEqual(summary["dimension_deductions"]["拓扑完整性"], 30.0)
        self.assertEqual(summary["score_before"], 70.0)

    def test_processed_defect_has_dimension_and_confidence(self):
        engine = ScoreAndConfidenceEngine()
        summary = engine.evaluate_quality_score([
            {"equip_id": "IF001", "defect_type": "主配接口缺失", "description": "馈线缺失主网间隔"}
        ])

        processed = summary["processed_defects"][0]
        self.assertEqual(processed["dimension"], "接口规范性")
        self.assertIn("confidence_reason", processed)
        self.assertIn("score_deduction", processed)


if __name__ == "__main__":
    unittest.main()
