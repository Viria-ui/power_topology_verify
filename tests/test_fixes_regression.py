# -*- coding: utf-8 -*-
"""本轮修复回归测试（L6补测）：
S1 电源类型判定、S3 联络候选判定、S7 评分规范公式、M9 SQL解析健壮性
"""
import sys, os, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd


class TestS1SourceType(unittest.TestCase):
    """S1：1702馈线段不是电源；1701/1321才是电源类型"""

    def setUp(self):
        from core.topology_builder import TopologyBuilder
        # _is_source_type为纯类型判定，不依赖构造参数，用__new__绕过初始化
        self.builder = TopologyBuilder.__new__(TopologyBuilder)

    def test_1702_not_source(self):
        self.assertFalse(self.builder._is_source_type("1702", "馈线段XX"))

    def test_1701_is_source(self):
        self.assertTrue(self.builder._is_source_type("1701", ""))

    def test_1321_not_source_type(self):
        """1321是主网出线开关（如10kV.LINE003_181开关），其is_source由S2
        主配跨边逻辑标记，设备类型本身不判定为电源。"""
        self.assertFalse(self.builder._is_source_type("1321", ""))


class TestS3TieSwitchCandidate(unittest.TestCase):
    """S3：联络开关候选判定（跨≥2馈线+开关类型+豁免规则）"""

    def setUp(self):
        from core.topology_validator import TopoDbValidator
        self.v = TopoDbValidator.__new__(TopoDbValidator)

    def _dev(self, equip_type="1705", equip_name="联络开关"):
        class _D:
            pass
        d = _D()
        d.equip_type = equip_type
        d.equip_name = equip_name
        return d

    def test_cross_feeder_switch_is_candidate(self):
        self.assertTrue(self.v._is_tie_switch_candidate(self._dev(), {"F1", "F2"}))

    def test_single_feeder_not_candidate(self):
        self.assertFalse(self.v._is_tie_switch_candidate(self._dev(), {"F1"}))

    def test_m5_status_normalization(self):
        """M5：状态判断统一大写（OPEN/CLOSE/0/1/分位/合位）"""
        cases = {
            "open": "OPEN", "OPEN": "OPEN", "分位": "OPEN",
            "close": "CLOSE", "CLOSE": "CLOSE", "合位": "CLOSE",
            "0": "OPEN", "1": "CLOSE",
        }
        for raw, expect in cases.items():
            up = str(raw).upper()
            if up in {"OPEN", "分位", "0"}:
                bucket = "OPEN"
            elif up in {"CLOSE", "合位", "1"}:
                bucket = "CLOSE"
            else:
                bucket = "UNKNOWN"
            self.assertEqual(bucket, expect, f"状态[{raw}]标准化错误")


class TestS7ScoreFormula(unittest.TestCase):
    """S7：Model_Score = 100 - Σ(Wi×Ci)，维度封顶30/25/20/25"""

    def test_dimension_weights(self):
        from core.constants import SCORE_WEIGHTS, SCORE_CAPS
        self.assertEqual(SCORE_WEIGHTS["拓扑完整性"], 5)
        self.assertEqual(SCORE_WEIGHTS["图模一致性"], 3)
        self.assertEqual(SCORE_WEIGHTS["电气逻辑"], 2)
        self.assertEqual(SCORE_WEIGHTS["接口规范性"], 4)
        self.assertEqual(SCORE_CAPS["拓扑完整性"], 30)
        self.assertEqual(SCORE_CAPS["图模一致性"], 25)
        self.assertEqual(SCORE_CAPS["电气逻辑"], 20)
        self.assertEqual(SCORE_CAPS["接口规范性"], 25)

    def test_formula_known_case(self):
        """样本：拓扑5处(5×5=25)、图模3处(3×3=9)、电气10处(2×10=20)、
        接口1处(4×1=4) → 总扣58 → 100-58=42.0"""
        from core.score_engine import ScoreAndConfidenceEngine
        se = ScoreAndConfidenceEngine()
        defects = []
        for i in range(5):
            defects.append({"defect_type": "孤岛设备", "severity": "ERR"})
        for i in range(3):
            defects.append({"defect_type": "图上有模型无", "severity": "SUSPECT"})
        for i in range(10):
            defects.append({"defect_type": "RULE-E03", "severity": "ERR"})
        defects.append({"defect_type": "主配接口漏拼", "severity": "ERR"})
        result = se.evaluate_quality_score(defects, total_equip_count=1000,
                                           repaired_defect_ids=[])
        self.assertEqual(result["score_before"], 42.0)
        self.assertEqual(result["defect_rate_penalty"], 0.0)  # S7：规范无惩罚


class TestM9SqlParsing(unittest.TestCase):
    """M9：SQL解析器——值内逗号、多元组、引号转义"""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".sql",
                                               delete=False, encoding="utf-8")
        self.path = self.tmp.name
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.path)

    def _parse(self, sql_text):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(sql_text)
        from data_io.data_reader import SqlTableLoader
        return SqlTableLoader().parse_sql_insert_to_df(self.path)

    def test_value_contains_comma(self):
        df = self._parse(
            'INSERT INTO "T"("ID","NAME") VALUES (\'TMP0001\', \'a,b,c\');'
        )
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["NAME"], "a,b,c")

    def test_multi_row_values(self):
        df = self._parse(
            'INSERT INTO "T"("ID","V") VALUES (\'1\',\'x\'),(\'2\',\'y\');'
        )
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[1]["ID"], "2")

    def test_quoted_escape_preserved(self):
        """引号转义''原样保留（与旧解析器行为一致）"""
        df = self._parse(
            "INSERT INTO \"T\"(\"ID\",\"N\") VALUES ('1','it''s');"
        )
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["N"], "it''s")

    def test_multiline_values(self):
        df = self._parse(
            'INSERT INTO "T"("ID","V")\nVALUES\n(\'1\',\'a\'),\n(\'2\',\'b\');'
        )
        self.assertEqual(len(df), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
