from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


PASS = "PASS"
ERR = "ERR"
SUSPECT = "SUSPECT"
EXEMPT = "EXEMPT"


@dataclass
class RuleResult:
    rule_id: str
    label: str
    equip_id: str
    description: str
    evidence: dict[str, Any]
    suggestion: str
    review_required: bool = False
    exemption_code: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class TelemetryEvaluator:
    """遥信遥测与主配接口规则评估器。

    新增 RULE-E01~E07 的结构化输出，同时保留旧版 tuple 接口，避免影响
    tests/compare.py 等既有流程。
    """

    CURRENT_EPS = 0.5
    POWER_EPS = 0.5
    VOLTAGE_EPS = 0.5
    UNBALANCE_LIMIT = 0.20
    POWER_MISMATCH_LIMIT = 0.20
    DEBOUNCE_SECONDS = 10

    OPEN_VALUES = {"0", "分", "分位", "分闸", "open", "opened", "off", "false"}
    CLOSED_VALUES = {"1", "合", "合位", "合闸", "closed", "close", "on", "true"}
    OUTAGE_STATES = {"退运", "检修", "备用", "停运", "规划", "outage", "maintenance", "standby"}
    REVERSE_POWER_KEYS = {"新能源", "光伏", "储能", "分布式电源", "pv", "ess", "distributed"}
    CAP_TRANSITION_KEYS = {"电容器", "svg", "无功补偿", "capacitor", "reactive"}

    def __init__(self, telemetry_data=None, main_substation_data=None):
        self.telemetry_data = telemetry_data or {}
        self.main_substation_data = main_substation_data or {}

    # ---- Backward-compatible legacy APIs ---------------------------------
    def evaluate_switch_status(self, equip_id, svg_is_open):
        """校验遥信与图纸开关逻辑状态，返回旧版 (是否通过, 置信度, 原因)。"""
        row = self._row(equip_id)
        tele_status = self._switch_status(row)
        if tele_status is None:
            return True, 0.5, "缺乏遥信实时数据，使用默认概率"

        tele_is_open = tele_status == "open"
        if tele_is_open != bool(svg_is_open):
            return False, 0.95, f"遥信实测状态({self._get_any(row, ['switch_status', 'status', 'position', '遥信状态'])})与图纸标记不一致"
        return True, 0.99, "遥信实测与图纸一致"

    def evaluate_kcl_conservation(self, node_id, connected_lines):
        """根据遥测电流/功率进行 KCL 守恒判断，返回旧版 tuple。"""
        if not connected_lines:
            return True, 0.5, "无遥测线路"

        total_current = 0.0
        has_telemetry = False
        for line_id in connected_lines:
            current = self._current(self._row(line_id))
            if current is not None:
                has_telemetry = True
                total_current += current

        if not has_telemetry:
            return True, 0.6, "未配置遥测表计"

        if abs(total_current) > 10.0:
            return False, 0.90, f"节点 KCL 电流不守恒，残差为 {total_current:.2f}A，可能存在隐形物理断线"
        return True, 0.95, "节点遥测 KCL 电流平衡"

    def verify_main_substation_interface(self, feeder_id, dsubstation_id):
        """校验主配网接口一致性规则，返回旧版 tuple。"""
        if not dsubstation_id or dsubstation_id == "UNKNOWN":
            return False, 0.85, "配网馈线缺失主网变电站间隔挂接信息"
        return True, 0.95, f"主配网变电站接口 [{dsubstation_id}] 校验通过"

    # ---- RULE-E01~E07 structured checks ----------------------------------
    def evaluate_all_rules(self, equip_id: str, svg_is_open: bool | None = None) -> list[dict[str, Any]]:
        """对单个设备执行电气逻辑规则，返回 AI 组可直接落表/落 JSON 的结果。"""
        row = self._row(equip_id)
        checks = [
            self.rule_e01_open_switch_has_current,
            self.rule_e02_closed_switch_no_current,
            self.rule_e03_outage_or_deenergized,
            self.rule_e04_three_phase_unbalance,
            self.rule_e05_power_mismatch,
            self.rule_e06_open_switch_has_active_power,
            self.rule_e07_zero_current_has_active_power,
        ]
        return [check(equip_id, row, svg_is_open).as_dict() for check in checks]

    def rule_e01_open_switch_has_current(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        exempt = self._exemption(row)
        if exempt:
            return self._result("RULE-E01", EXEMPT, equip_id, "开关分位带电流命中豁免条件", row, "记录豁免原因并人工抽查", False, exempt)

        state = self._effective_switch_state(row, svg_is_open)
        current = self._current(row)
        if state is None or current is None:
            return self._suspect("RULE-E01", equip_id, "缺少开关状态或电流数据，无法判定分位带电流", row)
        if state == "open" and abs(current) > self.CURRENT_EPS:
            return self._err("RULE-E01", equip_id, "开关处于分位但存在电流", row, "核对开关遥信、CT量测与拓扑连接，禁止直接自动闭合")
        return self._pass("RULE-E01", equip_id, "未发现分位带电流")

    def rule_e02_closed_switch_no_current(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        state = self._effective_switch_state(row, svg_is_open)
        current = self._current(row)
        voltage = self._voltage(row)
        power = self._active_power(row)
        if state is None or current is None:
            return self._suspect("RULE-E02", equip_id, "缺少开关状态或电流数据，无法判定合位无流", row)
        has_live_evidence = self._above(voltage, self.VOLTAGE_EPS) or self._above(power, self.POWER_EPS)
        if state == "closed" and abs(current) <= self.CURRENT_EPS and has_live_evidence:
            return self._suspect("RULE-E02", equip_id, "开关合位且存在带电/功率证据，但电流近零", row)
        return self._pass("RULE-E02", equip_id, "未发现合位无流异常")

    def rule_e03_outage_or_deenergized(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        if self._is_out_of_service(row):
            return self._result("RULE-E03", EXEMPT, equip_id, "设备处于退运/检修/备用等状态", row, "按计划停电或备用设备归档，不做自动修正", False, "EXEMPT_OUT_OF_SERVICE")

        current = self._current(row)
        voltage = self._voltage(row)
        power = self._active_power(row)
        if current is None and voltage is None and power is None:
            return self._suspect("RULE-E03", equip_id, "遥测缺失，无法确认是否停电或失压", row)
        if self._near_zero(current, self.CURRENT_EPS) and self._near_zero(voltage, self.VOLTAGE_EPS) and self._near_zero(power, self.POWER_EPS):
            return self._suspect("RULE-E03", equip_id, "电流、电压、有功均近零，疑似停电或孤岛失电", row)
        return self._pass("RULE-E03", equip_id, "未发现失压停电异常")

    def rule_e04_three_phase_unbalance(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        currents = self._phase_currents(row)
        if len(currents) < 3:
            return self._suspect("RULE-E04", equip_id, "三相电流数据不完整，无法计算不平衡度", row)
        avg = sum(abs(v) for v in currents) / 3.0
        if avg <= self.CURRENT_EPS:
            return self._pass("RULE-E04", equip_id, "三相电流均接近零，不计算不平衡异常")
        deviation = max(abs(abs(v) - avg) for v in currents) / avg
        if deviation > self.UNBALANCE_LIMIT:
            evidence = dict(row, unbalance_ratio=round(deviation, 4))
            return self._result("RULE-E04", SUSPECT, equip_id, "三相电流不平衡度超过20%", evidence, "核对三相量测、负荷分相与接线关系", True)
        return self._pass("RULE-E04", equip_id, "三相电流不平衡度在阈值内")

    def rule_e05_power_mismatch(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        current = self._current(row)
        voltage = self._voltage(row)
        active_power = self._active_power(row)
        if current is None or voltage is None or active_power is None:
            return self._suspect("RULE-E05", equip_id, "缺少电压、电流或有功功率，无法校验功率匹配", row)
        estimate = abs(voltage * current)
        if estimate <= self.POWER_EPS:
            return self._pass("RULE-E05", equip_id, "电压电流估算功率接近零，不触发功率匹配异常")
        mismatch = abs(abs(active_power) - estimate) / estimate
        if mismatch > self.POWER_MISMATCH_LIMIT:
            evidence = dict(row, power_mismatch_ratio=round(mismatch, 4))
            return self._result("RULE-E05", SUSPECT, equip_id, "有功功率与电压电流估算值偏差超过20%", evidence, "核对PT/CT倍率、计量方向和量测采样时间", True)
        return self._pass("RULE-E05", equip_id, "功率匹配在阈值内")

    def rule_e06_open_switch_has_active_power(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        exempt = self._exemption(row)
        if exempt:
            return self._result("RULE-E06", EXEMPT, equip_id, "开关分位带有功命中豁免条件", row, "记录豁免原因并人工抽查", False, exempt)

        state = self._effective_switch_state(row, svg_is_open)
        power = self._active_power(row)
        if state is None or power is None:
            return self._suspect("RULE-E06", equip_id, "缺少开关状态或有功功率，无法判定分位带有功", row)
        if state == "open" and abs(power) > self.POWER_EPS:
            return self._err("RULE-E06", equip_id, "开关处于分位但存在有功功率", row, "核对开关状态、功率方向与拓扑连接，禁止直接自动修正")
        return self._pass("RULE-E06", equip_id, "未发现分位带有功异常")

    def rule_e07_zero_current_has_active_power(self, equip_id: str, row: dict[str, Any] | None = None, svg_is_open=None):
        row = row or self._row(equip_id)
        current = self._current(row)
        power = self._active_power(row)
        if current is None or power is None:
            return self._suspect("RULE-E07", equip_id, "缺少电流或有功功率，无法判定零流有功", row)
        if abs(current) <= self.CURRENT_EPS and abs(power) > self.POWER_EPS:
            return self._result("RULE-E07", SUSPECT, equip_id, "电流近零但有功功率不为零", row, "核对电流遥测、功率遥测、倍率与采样时间", True)
        return self._pass("RULE-E07", equip_id, "未发现零流有功异常")

    # ---- Helpers ----------------------------------------------------------
    def _row(self, equip_id: str) -> dict[str, Any]:
        row = self.telemetry_data.get(equip_id, {})
        return row if isinstance(row, dict) else {}

    def _result(self, rule_id, label, equip_id, description, evidence, suggestion, review_required=False, exemption_code=""):
        return RuleResult(rule_id, label, equip_id, description, evidence, suggestion, review_required, exemption_code)

    def _pass(self, rule_id, equip_id, description):
        return self._result(rule_id, PASS, equip_id, description, {}, "无需处理")

    def _err(self, rule_id, equip_id, description, evidence, suggestion):
        return self._result(rule_id, ERR, equip_id, description, evidence, suggestion, True)

    def _suspect(self, rule_id, equip_id, description, evidence):
        return self._result(rule_id, SUSPECT, equip_id, description, evidence, "标记待人工复核，不自动修正", True)

    def _get_any(self, row: dict[str, Any], keys: list[str]) -> Any:
        for key in keys:
            if key in row and row[key] not in (None, ""):
                return row[key]
        lower_map = {str(k).lower(): v for k, v in row.items()}
        for key in keys:
            value = lower_map.get(key.lower())
            if value not in (None, ""):
                return value
        return None

    def _to_float(self, value: Any) -> float | None:
        if value in (None, ""):
            return None
        try:
            return float(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return None

    def _switch_status(self, row: dict[str, Any]) -> str | None:
        raw = self._get_any(row, ["switch_status", "遥信状态", "status", "position", "yx_status"])
        if raw is None:
            return None
        value = str(raw).strip().lower()
        if value in self.OPEN_VALUES:
            return "open"
        if value in self.CLOSED_VALUES:
            return "closed"
        return None

    def _effective_switch_state(self, row: dict[str, Any], svg_is_open: bool | None) -> str | None:
        state = self._switch_status(row)
        if state is not None:
            return state
        if svg_is_open is None:
            return None
        return "open" if svg_is_open else "closed"

    def _current(self, row: dict[str, Any]) -> float | None:
        value = self._get_any(row, ["current", "i", "I", "电流", "current_a", "ia"])
        return self._to_float(value)

    def _phase_currents(self, row: dict[str, Any]) -> list[float]:
        keys = [["ia", "Ia", "current_a", "A相电流"], ["ib", "Ib", "current_b", "B相电流"], ["ic", "Ic", "current_c", "C相电流"]]
        values = [self._to_float(self._get_any(row, group)) for group in keys]
        return [v for v in values if v is not None]

    def _voltage(self, row: dict[str, Any]) -> float | None:
        value = self._get_any(row, ["voltage", "u", "U", "电压", "voltage_kv"])
        return self._to_float(value)

    def _active_power(self, row: dict[str, Any]) -> float | None:
        value = self._get_any(row, ["active_power", "p", "P", "power", "有功", "有功功率"])
        return self._to_float(value)

    def _near_zero(self, value: float | None, eps: float) -> bool:
        return value is not None and abs(value) <= eps

    def _above(self, value: float | None, eps: float) -> bool:
        return value is not None and abs(value) > eps

    def _text_blob(self, row: dict[str, Any]) -> str:
        keys = ["device_type", "equip_type", "type", "设备类型", "equip_name", "name", "设备名称", "state", "运行状态"]
        return " ".join(str(self._get_any(row, [key]) or "") for key in keys).lower()

    def _is_out_of_service(self, row: dict[str, Any]) -> bool:
        blob = self._text_blob(row)
        return any(key.lower() in blob for key in self.OUTAGE_STATES)

    def _exemption(self, row: dict[str, Any]) -> str:
        if self._is_out_of_service(row):
            return "EXEMPT_OUT_OF_SERVICE"
        if bool(self._get_any(row, ["reverse_power_exempt", "EXEMPT_REVERSE_POWER"])):
            return "EXEMPT_REVERSE_POWER"
        if any(key in self._text_blob(row) for key in self.REVERSE_POWER_KEYS):
            return "EXEMPT_REVERSE_POWER"
        if bool(self._get_any(row, ["cap_transition_exempt", "EXEMPT_CAP_TRANSITION"])):
            return "EXEMPT_CAP_TRANSITION"
        if any(key in self._text_blob(row) for key in self.CAP_TRANSITION_KEYS) and self._within_debounce(row):
            return "EXEMPT_CAP_TRANSITION"
        return ""

    def _within_debounce(self, row: dict[str, Any]) -> bool:
        seconds = self._to_float(self._get_any(row, ["seconds_since_change", "change_seconds", "变位秒数"]))
        if seconds is not None:
            return seconds <= self.DEBOUNCE_SECONDS

        raw_time = self._get_any(row, ["last_change_time", "change_time", "变位时间"])
        if raw_time is None:
            return False
        try:
            changed_at = datetime.fromisoformat(str(raw_time).replace("Z", "+00:00"))
            if changed_at.tzinfo is None:
                changed_at = changed_at.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - changed_at).total_seconds() <= self.DEBOUNCE_SECONDS
        except ValueError:
            return False
