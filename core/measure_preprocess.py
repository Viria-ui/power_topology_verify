"""
遥信预处理：去重、状态映射、取最新遥信
赛题规则：
1. PWREAL：TRAN_ID + DATA_DATE 联合去重，保留最新一条
2. JBS_ZWSIGNAL主网遥信为快照数据，无时间戳
3. 无遥信开关默认 close（合位）Q38
注意：data_reader读出全部字段为字符串
数据集说明：本数据集无QUALITY_CODE质量字段；E07时序去抖受数据源限制仅保留框架
"""
import logging
import pandas as pd

logger = logging.getLogger(__name__)
from typing import Dict, Set, Tuple, Optional


class MeasurePreprocessor:
    def __init__(self, table_data: dict, time_window_sec: int = 5):
        """
        :param table_data: data_reader返回完整table_data字典
        :param time_window_sec: 时间窗口，本数据集缺少连续时序，仅保留参数占位
        """
        self.table_data = table_data
        self.time_window_sec = time_window_sec

        self.df_pwreal: pd.DataFrame = self.table_data.get("yx_real", pd.DataFrame())
        self.df_zwsignal: pd.DataFrame = self.table_data.get("zw_signal", pd.DataFrame())

        self.final_switch_state: Dict[str, str] = {}   # equip_id -> "CLOSE"/"OPEN" 大写统一口径
        self.state_source: Dict[str, str] = {}          # "rtu"实测 / "default_rule"默认合位

    @staticmethod
    def point_2_status(raw_val) -> str:
        """
        POINT字段转换状态: 0 → OPEN分闸，1 → CLOSE合闸
        """
        try:
            v = int(raw_val)
        except (ValueError, TypeError):
            return "CLOSE"
        if v == 0:
            return "OPEN"
        elif v == 1:
            return "CLOSE"
        return "CLOSE"

    def pwreal_deduplicate(self) -> pd.DataFrame:
        """Q8 配网遥信：TRAN_ID + DATA_DATE 联合去重，保留时间最后一条"""
        df = self.df_pwreal.copy()
        if df.empty:
            return df
        # 去重
        df = df.drop_duplicates(subset=["TRAN_ID", "DATA_DATE"], keep="last")
        return df

    def pwreal_get_latest(self, dedup_df: pd.DataFrame) -> Dict[str, str]:
        """配网PWREAL：按TRAN_ID分组，取DATA_DATE最新遥信"""
        rtu_map: Dict[str, str] = {}
        if dedup_df.empty:
            return rtu_map

        for equip_id, group in dedup_df.groupby("TRAN_ID"):
            # 按采集时间排序取最后一条
            group_sorted = group.sort_values("DATA_DATE", ascending=True)
            last_row = group_sorted.iloc[-1]
            pt_val = last_row.get("POINT")
            eid = str(equip_id).strip()
            rtu_map[eid] = self.point_2_status(pt_val)
        return rtu_map

    def zwsignal_parse(self) -> Dict[str, str]:
        """主网遥信 JBS_ZWSIGNAL：快照数据，无时间戳，直接读取POINT"""
        sig_map: Dict[str, str] = {}
        df = self.df_zwsignal
        if df.empty:
            return sig_map
        for _, row in df.iterrows():
            eid = str(row.get("ID", "")).strip()
            if not eid:
                continue
            pt_val = row.get("POINT")
            sig_map[eid] = self.point_2_status(pt_val)
        return sig_map

    def run(self, all_switch_ids: Set[str]) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        执行完整遥信预处理
        :param all_switch_ids: 全部开关设备ID集合（从拓扑设备中提取）
        :return: (final_switch_state, state_source)
            final_switch_state: equip_id -> CLOSE / OPEN
            state_source: rtu(遥信实测) / default_rule(无遥信默认合位 Q38)
        """
        # 1 处理配网PWREAL
        dedup_pw = self.pwreal_deduplicate()
        pw_map = self.pwreal_get_latest(dedup_pw)
        # 2 处理主网ZWSIGNAL
        zw_map = self.zwsignal_parse()

        # 合并：配网+主网遥信，同设备ID配网优先
        combined_rtu: Dict[str, str] = {}
        combined_rtu.update(zw_map)
        combined_rtu.update(pw_map)

        # Q38规则：遍历全部开关，有遥信用rtu，无遥信默认CLOSE
        for sw_id in all_switch_ids:
            sw_id = str(sw_id).strip()
            if sw_id in combined_rtu:
                self.final_switch_state[sw_id] = combined_rtu[sw_id]
                self.state_source[sw_id] = "rtu"
            else:
                self.final_switch_state[sw_id] = "CLOSE"
                self.state_source[sw_id] = "default_rule"

        logger.info(f"[MeasurePreprocess] 遥信实测开关数量：{len([k for k,v in self.state_source.items() if v=='rtu'])}")
        logger.info(f"[MeasurePreprocess] 默认合位开关数量：{len([k for k,v in self.state_source.items() if v=='default_rule'])}")
        return self.final_switch_state, self.state_source

    def get_switch_final_status(self, equip_id: str) -> str:
        """对外查询接口，供topology_validator电气校验调用，返回 CLOSE / OPEN"""
        eid = str(equip_id).strip()
        return self.final_switch_state.get(eid, "CLOSE")

