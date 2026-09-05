"""电气逻辑规则 E01--E07 与主配接口校验。"""
from __future__ import annotations
from datetime import timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class TelemetryEvaluator:
    DEBOUNCE_SECONDS = 10
    CAPACITOR_MASK_SECONDS = 30
    NEW_ENERGY_WHITELIST = {"光伏", "储能", "分布式电源", "新能源", "风电", "PV", "ESS", "DG"}
    CAPACITOR_WHITELIST = {"电容器", "SVG", "无功补偿", "电容", "电抗器", "Filter", "CAP"}
    FA_TRIP_TOKENS = {"1", "TRUE", "FA_TRIP", "TRIP", "保护动作", "跳闸", "FAULT"}

    def __init__(self, telemetry_data=None, main_substation_data=None, zw_substation_ids=None):
        self.telemetry_data = telemetry_data or {}
        self.main_substation_data = main_substation_data or {}
        self.zw_substation_ids = set(str(x) for x in (zw_substation_ids or []))

    @classmethod
    def from_pwreal(cls, df: pd.DataFrame, main_substation_data=None, zw_substation_df=None):
        data = {}
        if df is not None and not df.empty and "TRAN_ID" in df:
            for eid, group in df.groupby("TRAN_ID"):
                g = group.copy()
                g["_time"] = pd.to_datetime(g.get("DATA_DATE"), errors="coerce")
                data[str(eid)] = [r.to_dict() for _, r in g.sort_values("_time").iterrows()]
        zw_ids = []
        if zw_substation_df is not None and not zw_substation_df.empty:
            if "ST_ID" in zw_substation_df.columns:
                zw_ids = zw_substation_df["ST_ID"].astype(str).tolist()
            elif "SUBSTATION_ID" in zw_substation_df.columns:
                zw_ids = zw_substation_df["SUBSTATION_ID"].astype(str).tolist()
        return cls(data, main_substation_data, zw_ids)

    @staticmethod
    def _number(row, field):
        try:
            v = row.get(field, 0)
            if v is None:
                return 0.0
            return float(v)
        except (TypeError, ValueError):
            return 0.0

    def _latest(self, equip_id):
        rows = self.telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            return rows
        return rows[-1] if rows else {}

    def _rows_window(self, equip_id, seconds: int):
        rows = self.telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        if not rows:
            return []
        last_time = pd.to_datetime(rows[-1].get("DATA_DATE"), errors="coerce")
        if pd.isna(last_time):
            return rows
        window_rows = []
        for row in reversed(rows):
            t = pd.to_datetime(row.get("DATA_DATE"), errors="coerce")
            if pd.isna(t):
                continue
            if last_time - t <= timedelta(seconds=seconds):
                window_rows.append(row)
            else:
                break
        return list(reversed(window_rows))

    def _is_fa_trip(self, row) -> bool:
        fa_val = str(row.get("FA_TRIP", row.get("EVENT_TYPE", row.get("POINT_QUALITY", "")))).upper()
        return any(tok in fa_val for tok in self.FA_TRIP_TOKENS)

    def _stable_status(self, equip_id):
        rows = self.telemetry_data.get(str(equip_id), [])
        if isinstance(rows, dict):
            rows = [rows]
        if not rows:
            return None
        last = rows[-1]
        status = str(last.get("POINT", last.get("switch_status", last.get("VAL", ""))))
        if self._is_fa_trip(last):
            logger.debug("设备%s触发FA_TRIP保护动作，跳过防抖直接采用状态%s", equip_id, status)
            return status
        last_time = pd.to_datetime(last.get("DATA_DATE"), errors="coerce")
        for row in reversed(rows[:-1]):
            t = pd.to_datetime(row.get("DATA_DATE"), errors="coerce")
            if pd.isna(t) or pd.isna(last_time) or (last_time - t) > timedelta(seconds=self.DEBOUNCE_SECONDS):
                break
            if str(row.get("POINT", row.get("switch_status", row.get("VAL", "")))) != status:
                return None
        return status

    def _in_capacitor_transition(self, equip_id, equip_type: str) -> bool:
        if not any(x in str(equip_type) for x in self.CAPACITOR_WHITELIST):
            return False
        window_rows = self._rows_window(equip_id, self.CAPACITOR_MASK_SECONDS)
        if len(window_rows) < 2:
            return True
        first_status = str(window_rows[0].get("POINT", ""))
        last_status = str(window_rows[-1].get("POINT", ""))
        if first_status != last_status:
            logger.debug("设备%s处于电容投切30s过渡屏蔽窗", equip_id)
            return True
        return False

    def _is_new_energy(self, equip_type: str) -> bool:
        t = str(equip_type)
        return any(x in t for x in self.NEW_ENERGY_WHITELIST)

    def _is_capacitor_type(self, equip_type: str) -> bool:
        t = str(equip_type)
        return any(x in t for x in self.CAPACITOR_WHITELIST)

    def evaluate_switch_status(self, equip_id, svg_is_open):
        status = self._stable_status(equip_id)
        if status is None:
            return True, .5, "缺乏稳定遥信(10s防抖未通过)，按默认合位并标记待复核"
        if status not in {"0", "1", "分位", "合位", "open", "close"}:
            return True, .5, "遥信品质无效，待复核"
        real_open = status in {"0", "分位", "open"}
        if real_open != bool(svg_is_open):
            return False, .95, f"遥信稳定状态({status})与图纸开关状态(分={svg_is_open})不一致"
        return True, .99, "遥信与图纸一致"

    def evaluate_kcl_conservation(self, node_id, connected_lines):
        values_a = [self._number(self._latest(x), "IA") for x in connected_lines]
        values_b = [self._number(self._latest(x), "IB") for x in connected_lines]
        values_c = [self._number(self._latest(x), "IC") for x in connected_lines]
        all_v = values_a + values_b + values_c
        if not any(all_v):
            return True, .6, "无有效电流遥测"
        residual_a = sum(values_a)
        residual_b = sum(values_b)
        residual_c = sum(values_c)
        max_res = max(abs(residual_a), abs(residual_b), abs(residual_c))
        return max_res <= 10, .9, (
            f"节点 KCL 三相电流残差 IA={residual_a:.2f}A IB={residual_b:.2f}A IC={residual_c:.2f}A"
        )

    def evaluate_electrical_logic(self, equip_id, equip_type=""):
        """
        执行 E01--E07；
        - 遥信状态经 10 秒防抖（FA_TRIP 保护动作不防抖）
        - 电容器类投切 30 秒过渡屏蔽窗内豁免 E01/E02/E06/E07
        - 新能源（光伏/储能/分布式电源）E05/E07 豁免
        """
        row = self._latest(equip_id)
        if not row:
            return []
        status = self._stable_status(equip_id)
        ia, ib, ic = (self._number(row, x) for x in ("IA", "IB", "IC"))
        p, q, s = self._number(row, "AP"), self._number(row, "RP"), self._number(row, "SP")
        current = max(abs(ia), abs(ib), abs(ic))
        u = [self._number(row, x) for x in ("UA", "UB", "UC")]
        out = []

        def add(code, detail):
            out.append({
                "rule_code": code,
                "equip_id": str(equip_id),
                "equip_type": str(equip_type),
                "dimension": "电气逻辑",
                "detail": detail,
            })

        cap_transition = self._in_capacitor_transition(equip_id, equip_type)
        is_new_energy = self._is_new_energy(equip_type)
        is_cap = self._is_capacitor_type(equip_type)

        status_open = status in {"0", "分位", "open"}
        status_close = status in {"1", "合位", "close"}

        if not cap_transition:
            if status_open and current > 1:
                add("RULE-E01", f"开关分位仍有电流 {current:.2f}A(IA={ia:.2f} IB={ib:.2f} IC={ic:.2f})")
            if status_close and current < 0.1 and any(v > 1 for v in u):
                add("RULE-E02", f"开关合位失流：电流={current:.3f}A，三相电压={u}")
        if status_close and max(u, default=0) < 1:
            add("RULE-E03", f"开关合位但三相均失压：U={u}")

        avg = (ia + ib + ic) / 3 if (ia or ib or ic) else 0
        if abs(avg) > 0.1:
            unbalance = max(abs(x - avg) for x in (ia, ib, ic)) / abs(avg)
            if unbalance > 0.3:
                add("RULE-E04",
                    f"三相电流不平衡{unbalance:.1%} > 30%：IA={ia:.2f} IB={ib:.2f} IC={ic:.2f} 均值={avg:.2f}")

        if not is_new_energy:
            u_avg = sum(u) / 3 if any(u) else 0
            i_avg = (ia + ib + ic) / 3
            expected_p = u_avg * i_avg * 1.732 * 0.9 if (u_avg and i_avg) else 0
            if expected_p > 1 and abs(p) > 1:
                mismatch = abs(abs(p) - expected_p) / max(abs(expected_p), 1e-6)
                if mismatch > 0.5:
                    add("RULE-E05",
                        f"有功功率与电压电流不匹配：AP={p:.2f} 推算≈{expected_p:.2f}"
                        f" (U_avg={u_avg:.2f} I_avg={i_avg:.2f}) 偏差{mismatch:.1%}")

        if not cap_transition:
            if status_open and abs(p) > 1:
                add("RULE-E06", f"开关分位仍有有功功率 AP={p:.2f} RP={q:.2f} SP={s:.2f}")

        if not (cap_transition or is_cap or is_new_energy):
            if current < 1 and abs(p) > 10:
                add("RULE-E07",
                    f"小电流大功率疑似异常：I_max={current:.3f}A AP={p:.2f}"
                    f" (电容器/新能源已由白名单豁免)")

        return out

    def verify_main_substation_interface(self, feeder_id, dsubstation_id,
                                          feeder_line_ids=None, zw_lineend_df=None):
        """
        主配接口校验（4.1 漏拼 / 4.2 错拼）。
        输入：
          feeder_id: 配网馈线ID
          dsubstation_id: 配网设备挂接的主网变电站ID（DSUBSTATION_ID）
          feeder_line_ids: 该馈线的 PWFEEDERLINE 记录集，用于检查接口端点
          zw_lineend_df: 主网 ZWLINEEND 表DataFrame，用于查主网侧端点
        返回：(passed, confidence, detail)
        """
        interface_ok = True
        detail_parts = []
        conf = 0.85

        if not dsubstation_id or str(dsubstation_id) in {"", "UNKNOWN", "nan", "None"}:
            detail_parts.append("4.1漏拼：配网馈线缺失主网变电站间隔挂接信息(DSUBSTATION_ID为空)")
            return False, 0.85, "；".join(detail_parts)

        dsubstation_id = str(dsubstation_id)

        if self.zw_substation_ids:
            if dsubstation_id not in self.zw_substation_ids:
                interface_ok = False
                detail_parts.append(
                    f"4.2错拼：配网挂接站ID={dsubstation_id} 不存在于主网变电站表(ZWSUBSTATION)"
                    f" (共{len(self.zw_substation_ids)}个主网站)"
                )
                conf = 0.92
        elif self.main_substation_data and dsubstation_id not in self.main_substation_data:
            interface_ok = False
            detail_parts.append(
                f"4.2错拼：配网挂接站 {dsubstation_id} 不存在于主网变电站数据"
            )
            conf = 0.9

        if zw_lineend_df is not None and not zw_lineend_df.empty and feeder_line_ids:
            sub_col = None
            for c in ("ST_ID", "SUBSTATION_ID", "SUB_ID"):
                if c in zw_lineend_df.columns:
                    sub_col = c
                    break
            if sub_col:
                main_ends = zw_lineend_df[zw_lineend_df[sub_col].astype(str) == dsubstation_id]
                if main_ends.empty:
                    detail_parts.append(f"4.1漏拼：主网站{dsubstation_id}未在ZWLINEEND中发现出线记录")
                    interface_ok = False

        if not detail_parts:
            detail_parts.append(
                f"4.1/4.2主配变电站接口校验通过：配网馈线[{feeder_id}] ↔ 主网站[{dsubstation_id}]"
            )
            conf = 0.95

        return interface_ok, conf, "；".join(detail_parts)
