import unittest

from core.telemetry_evaluator import ERR, EXEMPT, SUSPECT, TelemetryEvaluator


class TelemetryEvaluatorTest(unittest.TestCase):
    def test_open_switch_with_current_is_error(self):
        evaluator = TelemetryEvaluator({
            "SW001": {"switch_status": 0, "current": 12.3, "active_power": 0}
        })

        result = evaluator.rule_e01_open_switch_has_current("SW001").as_dict()

        self.assertEqual(result["rule_id"], "RULE-E01")
        self.assertEqual(result["label"], ERR)
        self.assertTrue(result["review_required"])

    def test_open_switch_with_active_power_is_error(self):
        evaluator = TelemetryEvaluator({
            "SW002": {"switch_status": "分位", "current": 0, "active_power": 5.0}
        })

        result = evaluator.rule_e06_open_switch_has_active_power("SW002").as_dict()

        self.assertEqual(result["rule_id"], "RULE-E06")
        self.assertEqual(result["label"], ERR)

    def test_reverse_power_device_is_exempt(self):
        evaluator = TelemetryEvaluator({
            "PV001": {"switch_status": 0, "current": 4.0, "device_type": "分布式电源"}
        })

        result = evaluator.rule_e01_open_switch_has_current("PV001").as_dict()

        self.assertEqual(result["label"], EXEMPT)
        self.assertEqual(result["exemption_code"], "EXEMPT_REVERSE_POWER")

    def test_capacitor_transition_is_exempt_within_debounce(self):
        evaluator = TelemetryEvaluator({
            "CAP001": {
                "switch_status": "分位",
                "active_power": 3.0,
                "device_type": "SVG无功补偿",
                "seconds_since_change": 5,
            }
        })

        result = evaluator.rule_e06_open_switch_has_active_power("CAP001").as_dict()

        self.assertEqual(result["label"], EXEMPT)
        self.assertEqual(result["exemption_code"], "EXEMPT_CAP_TRANSITION")

    def test_three_phase_unbalance_is_suspect(self):
        evaluator = TelemetryEvaluator({
            "LOAD001": {"ia": 100, "ib": 50, "ic": 100}
        })

        result = evaluator.rule_e04_three_phase_unbalance("LOAD001").as_dict()

        self.assertEqual(result["label"], SUSPECT)
        self.assertTrue(result["review_required"])


if __name__ == "__main__":
    unittest.main()
