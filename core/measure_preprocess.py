"""
遥信预处理：去重、坏数据剔除、状态映射、时间窗口去抖
赛题规则：TRAN_ID + DATA_DATE 联合去重；无遥信开关默认 close（合位）
注意：data_reader读出全部字段为字符串，代码内部做int转换
"""
import pandas as pd
from typing import Dict, Set, Tuple


class MeasurePreprocessor:
    def __init__(self, yx_df: pd.DataFrame, all_switch_ids: Set[str], time_window_sec: int = 5):
        """
        :param yx_df: JBS_PWREAL原始表，允许空DataFrame，**禁止传None**
        :param all_switch_ids: 全部开关设备equip_id集合
        :param time_window_sec: 时间窗口，单位秒
        """
        self.yx_df = yx_df
        self.all_switch_ids = all_switch_ids
        self.time_window_sec = time_window_sec
        self.final_switch_state: Dict[str, str] = {}
        self.state_source: Dict[str, str] = {}

    def deduplicate(self) -> pd.DataFrame:
        """赛题Q8：TRAN_ID + DATA_DATE 联合去重，保留最后一条"""
        if self.yx_df.empty or not {"TRAN_ID", "DATA_DATE"}.issubset(self.yx_df.columns):
            return pd.DataFrame()
        df = self.yx_df.copy()
        df = df.drop_duplicates(subset=["TRAN_ID", "DATA_DATE"], keep="last")
        return df

    def filter_bad_quality(self, df: pd.DataFrame) -> pd.DataFrame:
        """兼容标准遥信表及赛题 PWREAL（POINT 是分/合位）。"""
        if df.empty:
            return df
        value_col = "VAL" if "VAL" in df.columns else "POINT"
        df["VAL_INT"] = pd.to_numeric(df[value_col], errors="coerce")
        mask = df["VAL_INT"].isin([0, 1])
        if "QUALITY_CODE" in df.columns:
            df["QUALITY_CODE_INT"] = pd.to_numeric(df["QUALITY_CODE"], errors="coerce")
            mask &= df["QUALITY_CODE_INT"].fillna(0).eq(0)
        good_df = df.loc[mask].copy()
        return good_df

    @staticmethod
    def val_2_status(raw_val: int) -> str:
        """0=open分闸；1=close合闸"""
        if raw_val == 1:
            return "close"
        elif raw_val == 0:
            return "open"
        return "close"

    def debounce_get_latest(self, good_df: pd.DataFrame) -> Dict[str, str]:
        """时间窗口去抖：按TRAN_ID分组，取时间DATA_DATE最新一条有效遥信"""
        rtu_map: Dict[str, str] = {}
        if good_df.empty:
            return rtu_map

        for equip_id, group in good_df.groupby("TRAN_ID"):
            # 按采集时间排序，取最新
            group = group.sort_values("DATA_DATE", ascending=True)
            last = group.iloc[-1]
            val = int(last["VAL_INT"])
            rtu_map[str(equip_id)] = self.val_2_status(val)
        return rtu_map

    def run(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        :return: (final_switch_state, state_source)
            final_switch_state: equip_id -> "close"/"open"
            state_source: "rtu"来自遥信实测 / "default_rule"赛题默认合位
        """
        dedup_df = self.deduplicate()
        good_df = self.filter_bad_quality(dedup_df)
        rtu_state = self.debounce_get_latest(good_df)

        # 赛题强制规则：没有遥信记录的开关全部默认 close
        for sw_id in self.all_switch_ids:
            if sw_id in rtu_state:
                self.final_switch_state[sw_id] = rtu_state[sw_id]
                self.state_source[sw_id] = "rtu"
            else:
                self.final_switch_state[sw_id] = "close"
                self.state_source[sw_id] = "default_rule"

        return self.final_switch_state, self.state_source
