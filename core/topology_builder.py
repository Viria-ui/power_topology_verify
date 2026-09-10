# SQL数据构建拓扑图基类
from __future__ import annotations
import sys
import os
import logging
import pandas as pd
from collections import defaultdict
from typing import Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
from config.settings import MAIN_VOLTAGE, DIST_VOLTAGE
from core.graph_model import TopologyGraph, Device, ConnectPoint, TopoEdge, build_device_internal_edges
from core.topology_validator import TopoDbValidator
from core.measure_preprocess import MeasurePreprocessor
from core.constants import SOURCE_TYPES, SWITCH_TYPES

logger = logging.getLogger(__name__)


class TopologyBuilder:
    def __init__(self, table_data: dict):
        self.table_data = table_data
        self.equip_df = table_data.get("equip", pd.DataFrame()).copy()
        self.zw_equip_df = table_data.get("zw_equip", pd.DataFrame()).copy()
        self.line_df = table_data.get("line", pd.DataFrame()).copy()
        # 【P3修复】可选 feeder 过滤：传具体 feeder_id 时，check_electrical_logic 只评估该馈线设备
        self._feeder_filter: Optional[str] = None

        self.pw_terminal_df = table_data.get("pw_terminal")
        self.zw_terminal_df = table_data.get("zw_terminal")
        self.zw_substation_df = table_data.get("zw_substation", pd.DataFrame()).copy()
        self.zw_line_end_df = table_data.get("zw_line_end", pd.DataFrame()).copy()
        self.zw_mea_df = table_data.get("zw_mea", pd.DataFrame()).copy()
        self.zw_signal_df = table_data.get("zw_signal", pd.DataFrame()).copy()
        self.yx_real_df = table_data.get("yx_real", pd.DataFrame()).copy()

        if hasattr(self.zw_substation_df, "columns"):
            self.zw_substation_df.columns = [c.strip() for c in self.zw_substation_df.columns]
        if hasattr(self.zw_line_end_df, "columns"):
            self.zw_line_end_df.columns = [c.strip() for c in self.zw_line_end_df.columns]
        if hasattr(self.zw_mea_df, "columns"):
            self.zw_mea_df.columns = [c.strip() for c in self.zw_mea_df.columns]
        if hasattr(self.zw_signal_df, "columns"):
            self.zw_signal_df.columns = [c.strip() for c in self.zw_signal_df.columns]
        if hasattr(self.yx_real_df, "columns"):
            self.yx_real_df.columns = [c.strip() for c in self.yx_real_df.columns]

        self.main_topo = TopologyGraph()
        self.dist_topo = TopologyGraph()

    def split_voltage_data(self):
        """按数据表来源拆分主配网，避免 1010 电压码导致主网被丢弃。"""
        self.equip_df.columns = [col.strip() for col in self.equip_df.columns]
        self.line_df.columns = [col.strip() for col in self.line_df.columns]
        if self.pw_terminal_df is not None and hasattr(self.pw_terminal_df, "columns"):
            self.pw_terminal_df.columns = [col.strip() for col in self.pw_terminal_df.columns]
        if self.zw_terminal_df is not None and hasattr(self.zw_terminal_df, "columns"):
            self.zw_terminal_df.columns = [col.strip() for col in self.zw_terminal_df.columns]
        if hasattr(self.zw_equip_df, "columns"):
            self.zw_equip_df.columns = [col.strip() for col in self.zw_equip_df.columns]
        self.main_equip = self.zw_equip_df.copy()
        self.dist_equip = self.equip_df.copy()

        self.main_line = self.zw_line_end_df.copy()
        self.dist_line = self.line_df.copy()

        logger.info(
            "主配数据拆分完成：主网设备=%d 配网设备=%d 主网线段=%d 配网线段=%d "
            "主网站=%d 遥信遥测=%d ZWMEA=%d ZWSIGNAL=%d",
            len(self.main_equip), len(self.dist_equip),
            len(self.main_line), len(self.dist_line),
            len(self.zw_substation_df), len(self.yx_real_df),
            len(self.zw_mea_df), len(self.zw_signal_df),
        )
        logger.info(f"主网设备数量：{len(self.main_equip)}")
        logger.info(f"配网设备数量：{len(self.dist_equip)}")
        logger.info(f"主网线路(ZLINEEND)数量：{len(self.main_line)}")
        logger.info(f"配网线路(PWFEEDERLINE)数量：{len(self.dist_line)}")
        logger.info(f"主网站点(ZWSUBSTATION)数量：{len(self.zw_substation_df)}")
        logger.info(f"遥信遥测(PWREAL)记录数：{len(self.yx_real_df)}")
        logger.info(f"主网遥测(ZWMEA)：{len(self.zw_mea_df)} 主网遥信(ZWSIGNAL)：{len(self.zw_signal_df)}")

    def _is_source_type(self, equip_type_val: str, equip_name: str = "") -> bool:
        """电源识别：数值码/中文名/CIM + 设备名称关键字三栖判定，避免0台电源。

        识别逻辑（满足任一即为电源）：
        1. 设备类型码在 SOURCE_TYPES 集合中
        2. 设备名称含变电站/主变/STATION等关键词（不要求类型码同时命中）
        3. 主网侧(ZWEQUIPINFO)设备默认为电源（主网即电源网络）
        """
        if not equip_type_val:
            return False
        t = str(equip_type_val).strip()
        # 1. 类型码精确匹配
        if t in SOURCE_TYPES:
            return True
        name = str(equip_name or "")
        # 2. 名称关键字匹配（不要求类型码同时命中，修复原代码重言式bug）
        keywords = ("变电站", "主变", "SUB", "STATION", "Trafo", "TRANSFORMER",
                    "PowerTransformer", "变电")
        if any(k in name.upper() for k in keywords):
            return True
        # 3. 主网站房类型码（1701）判电源
        # 【S1修复】1702 是"馈线段XX"（数据实测17643台），不是电源！
        # 原代码把1702也判为电源，导致整条馈线的馈线段全部被当作电源，
        # is_source 从真实电源数膨胀到17643（34.8%），孤岛/悬空/合环判定全部失真。
        if t in ("1701",):
            return True
        return False

    def add_all_devices(self):
        """批量添加设备"""
        logger.info(f"[Builder] 正在添加 {len(self.main_equip)} 个主网设备和 {len(self.dist_equip)} 个配网设备...")
        src_cnt_main = 0
        for _, row in self.main_equip.iterrows():
            equip_id = str(row.get("EQUIP_ID", ""))
            if not equip_id:
                continue
            eq_type = str(row.get("EQUIP_TYPE", ""))
            eq_name = str(row.get("EQUIP_NAME", ""))
            is_src = self._is_source_type(eq_type, eq_name)
            src_cnt_main += int(is_src)
            dsub_id = (
                str(row.get("ST_ID", ""))
                or str(row.get("SUBSTATION_ID", ""))
                or str(row.get("SUB_ID", ""))
                or ""
            )
            self.main_topo.add_device(Device(
                equip_id=equip_id, equip_name=eq_name,
                equip_type=eq_type,
                voltage_type=str(row.get("VOLTAGE_TYPE", "")),
                dsubstation_id=dsub_id,
                is_source=is_src,
            ))
        logger.info("主网电源设备数=%d", src_cnt_main)
        logger.info(f"主网电源设备识别: {src_cnt_main} 台")

        src_cnt_dist = 0
        for i, (_, row) in enumerate(self.dist_equip.iterrows()):
            if i % 10000 == 0 and i > 0:
                logger.debug(f"已处理 {i} 个配网设备")

            equip_type_val = str(row.get("EQUIP_TYPE", ""))
            equip_name_val = str(row.get("EQUIP_NAME", ""))
            is_source = self._is_source_type(equip_type_val, equip_name_val)
            src_cnt_dist += int(is_source)

            feeder_raw = row.get("FEEDER_ID", "") if "FEEDER_ID" in row.index else None
            dsub_raw = row.get("DSUBSTATION_ID", "") if "DSUBSTATION_ID" in row.index else None

            dev = Device(
                equip_id=str(row.get("EQUIP_ID", "")),
                equip_name=equip_name_val,
                equip_type=equip_type_val,
                voltage_type=str(row.get("VOLTAGE_TYPE", "")),
                feeder_id=str(feeder_raw) if feeder_raw not in (None, "None") else "",
                dsubstation_id=str(dsub_raw) if dsub_raw not in (None, "None") else "",
                is_source=is_source,
            )
            self.dist_topo.add_device(dev)
        logger.info("配网电源设备数=%d", src_cnt_dist)
        logger.info(f"配网电源设备识别: {src_cnt_dist} 台")
        if src_cnt_main == 0 and src_cnt_dist == 0 and len(self.zw_substation_df) > 0:
            logger.warning("未从设备表识别出任何电源，尝试使用ZWSUBSTATION注入电源点")
            for _, row in self.zw_substation_df.iterrows():
                st_id = str(row.get("ST_ID", "") or row.get("SUBSTATION_ID", "") or row.get("ID", ""))
                if not st_id:
                    continue
                if st_id in self.main_topo.device_map:
                    self.main_topo.device_map[st_id].is_source = True
                    self.main_topo.graph.nodes[st_id]["dev_info"]["is_source"] = True
                else:
                    self.main_topo.add_device(Device(
                        equip_id=st_id,
                        equip_name=str(row.get("ST_NAME", "") or row.get("SUBSTATION_NAME", "") or st_id),
                        equip_type="1701",
                        voltage_type=str(row.get("VOLTAGE_TYPE", MAIN_VOLTAGE)),
                        dsubstation_id=st_id,
                        is_source=True,
                    ))
                src_cnt_main += 1
            logger.info(f"通过ZWSUBSTATION补充注入电源: {src_cnt_main} 台")
            
    def _inject_main_substation_sources(self):
        """主配电源注入 v2（修复 CN 空间不重叠导致 inject=0 的问题）。

        根因：原 v1 代码通过主/配网端子共享 CONNECTIVITYNODE_ID 建立关联，但实际数据中
        ZWTERMINAL 的 CN（格式 1090...）与 PWTERMINAL 的 CN（负数格式）完全不重叠。

        修复方案：改用 ZWLINEEND.LINEEND_NAME（如 "10kV.LINE003_181线"）中嵌入的
        线路编号与 PWFEEDERLINE.LINE_NAME 建立映射，从而建立馈线→主网站关联，
        再将主网站下的设备标记为电源（is_source=True）。
        """
        if len(self.zw_line_end_df) == 0:
            logger.warning("_inject_main_substation_sources: ZWLINEEND 为空，跳过")
            return
        if len(self.main_equip) == 0:
            logger.warning("_inject_main_substation_sources: 主网设备表为空，跳过")
            return

        import re
        # Step 1: 解析 ZWLINEEND.LINEEND_NAME → 主网站 ST_ID
        # 存储 原始名 和 标准化名（去 "10kV.", "_线" 等）
        le_name_to_st_id: dict[str, str] = {}

        def _norm_line_name(name: str) -> str:
            """【P1修复】标准化线路名称用于精确匹配：
            "10kV.LINE003_181线" → "LINE003"
            "10kVLINE003"        → "LINE003"
            "203LINE001_线"      → "LINE001"
            """
            s = name.strip()
            # 去除电压前缀：10kV. / 10kV / 35kV. / 35kV 等
            s = re.sub(r'^(10kV|20kV|35kV|110kV|66kV)\.?', '', s, flags=re.IGNORECASE)
            # 去除末尾后缀：_181线 / _线 / 等（数字+线）
            s = re.sub(r'_\d+线$', '', s)
            s = re.sub(r'_线$', '', s)
            return s.upper()

        for _, lrow in self.zw_line_end_df.iterrows():
            st_id = str(lrow.get("ST_ID") or "").strip()
            le_name = str(lrow.get("LINEEND_NAME") or "").strip()
            if not st_id or not le_name:
                continue
            le_name_to_st_id[le_name] = st_id
            std = _norm_line_name(le_name)
            if std:
                le_name_to_st_id[std] = st_id

        # Step 2: 建立配网 LINE_ID ↔ LINE_NAME 映射
        pw_line_id_to_name: dict[str, str] = {}
        pw_line_name_to_id: dict[str, str] = {}
        if self.line_df is not None and not self.line_df.empty:
            for _, lfrow in self.line_df.iterrows():
                lid = str(lfrow.get("LINE_ID") or "").strip()
                lname = str(lfrow.get("LINE_NAME") or "").strip()
                if lid:
                    pw_line_id_to_name[lid] = lname
                    pw_line_name_to_id[lname] = lid
                    std = _norm_line_name(lname)
                    if std:
                        pw_line_name_to_id[std] = lid

        # Step 3: 【P1修复】通过标准化 LINE_NAME 匹配，建立 馈线LINE_ID → 主网站ST_ID 映射
        # 原问题："10kV.LINE003_181线" 与 "10kVLINE003" 无法精确匹配导致映射数=0
        # 解决：双方标准化后都变成 "LINE003" → 精确匹配
        pw_line_to_zw_st: dict[str, str] = {}
        for le_name, st_id in le_name_to_st_id.items():
            if le_name in pw_line_name_to_id:
                lid = pw_line_name_to_id[le_name]
                if lid not in pw_line_to_zw_st:  # 避免重复覆盖
                    pw_line_to_zw_st[lid] = st_id

        # Step 4: 主网设备本身标记为电源（不再向整条配网馈线注入is_source）
        # 【S1修复】原v2逻辑把"配网馈线对应主网站"下的整条馈线所有设备都标is_source，
        # 配合1702误判导致is_source=17643。真正的电源接入点由S2（重叠CN跨边）
        # 在 build_graph_from_terminal 中把主网边界设备并入dist_topo实现，
        # 配网馈线通过物理连接边自然连到电源，无需整条馈线注入。
        injected = 0
        main_equip_ids_by_st: dict[str, set[str]] = {}
        for _, row in self.main_equip.iterrows():
            eid = str(row.get("EQUIP_ID") or "").strip()
            st_id = str(row.get("ST_ID") or row.get("SUBSTATION_ID") or "").strip()
            if eid and st_id:
                main_equip_ids_by_st.setdefault(st_id, set()).add(eid)

        for st_id, equip_ids in main_equip_ids_by_st.items():
            for eid in equip_ids:
                dev = self.main_topo.device_map.get(eid)
                if dev is not None:
                    dev.is_source = True
                    injected += 1

        logger.info("主配电源注入（S1修复版）: %d 台主网设备标记为电源（不再整条馈线注入）", injected)
        logger.info("  ZWLINEEND 解析出馈线→主网站映射数: %d", len(pw_line_to_zw_st))

    def build_real_terminal_points(self):
        """从端子表生成真实端子ConnectPoint，point_id=TERMINAL_ID"""
        # 配网端子
        if self.pw_terminal_df is None or self.pw_terminal_df.empty:
            logger.warning("未加载配网端子表，跳过配网真实端子生成")
        else:
            for _, row in self.pw_terminal_df.iterrows():
                # ✅ 修改后：自动兼容各种可能的字段列名
                term_id = str(
                    row.get("TERMINAL_ID")
                    or row.get("terminal_id")
                    or row.get("ID")
                    or row.get("id")
                    or ""
                )
                # ✅ 修改后：兼容各种可能的列名拼写
                dev_id = str(
                    row.get("DEVICE_ID")
                    or row.get("device_id")
                    or row.get("EQUIP_ID")
                    or row.get("equip_id")
                    or ""
                )

                if not term_id or dev_id not in self.dist_topo.device_map:
                    continue
                dev = self.dist_topo.device_map[dev_id]
                pt = ConnectPoint(
                    point_id=term_id,
                    belong_equip_id=dev_id,
                    feeder_id=dev.feeder_id
                )
                self.dist_topo.add_point(pt)
                # 设备节点与端子节点建立连接
                self.dist_topo.link_device_point(dev_id, term_id)
        # 主网端子
        # ✅ 修改后：先判断 DataFrame 是否存在且不为空
        if getattr(self, "zw_terminal_df", None) is not None and not self.zw_terminal_df.empty:
            for _, row in self.zw_terminal_df.iterrows():
                # JBS_ZWTERMINAL 的实际字段通常为 ID/EQUIP_ID，兼容
                # TERMINAL_ID/DEVICE_ID 命名，避免读到空端子。
                term_id = str(
                    row.get("TERMINAL_ID") or row.get("terminal_id")
                    or row.get("ID") or row.get("id") or ""
                )
                dev_id = str(
                    row.get("DEVICE_ID") or row.get("device_id")
                    or row.get("EQUIP_ID") or row.get("equip_id") or ""
                )
                if not term_id or not dev_id:
                    continue
                if dev_id not in self.main_topo.device_map:
                    continue
                dev = self.main_topo.device_map[dev_id]
                pt = ConnectPoint(
                    point_id=term_id,
                    belong_equip_id=dev_id,
                    feeder_id=dev.feeder_id
                )
                self.main_topo.add_point(pt)
                self.main_topo.link_device_point(dev_id, term_id)

        logger.info(f"[Builder] 配网真实端子数量:{len(self.dist_topo.point_map)}")
        logger.info(f"[Builder] 主网真实端子数量:{len(self.main_topo.point_map)}")


    def build_graph_from_terminal(self):
        """同CONNECT_NODE_ID下真实端子之间互连，节点为TERMINAL_ID"""
        if self.pw_terminal_df is None or self.pw_terminal_df.empty:
            logger.warning("未加载配网端子表，无法构建配网电气边")
        else:
            # -----配网端子建边-----
            cn_to_terms = defaultdict(list)
            term_to_equip = {}
            for _, row in self.pw_terminal_df.iterrows():
                cn_id = str(row.get("CONNECT_NODE_ID") or row.get("CONNECTIVITYNODE_ID") or "")
                term_id = str(row.get("TERMINAL_ID") or row.get("ID") or "")
                if cn_id and term_id:
                    cn_to_terms[cn_id].append(term_id)
                if term_id:
                    term_to_equip[term_id] = str(row.get("EQUIP_ID") or "")

            for cn, term_list in cn_to_terms.items():
                if len(term_list) < 2:
                    continue
                for i in range(len(term_list)-1):
                    t1 = term_list[i]
                    t2 = term_list[i+1]
                    # 同一设备两端子共享连接点时，设备内部通路由 fill_all_internal_connection
                    # 负责（INT_ 边），此处跳过以避免平行边造成单设备自环误判
                    if term_to_equip.get(t1) and term_to_equip.get(t2) and term_to_equip[t1] == term_to_equip[t2]:
                        continue
                    e = TopoEdge(
                        line_id=f"CN_{cn}_{t1}_{t2}",
                        start_point=t1,
                        end_point=t2,
                        line_name=f"连接节点{cn}端子互连"
                    )
                    self.dist_topo.add_edge(e)

        # -----主网端子建边-----
        if len(self.main_equip) == 0 or len(self.main_topo.point_map) == 0:
            logger.warning(
                "主网设备数或真实端子数为 0，跳过主网拓扑构建："
                f"设备数={len(self.main_equip)}，端子数={len(self.main_topo.point_map)}"
            )
            logger.info(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
            return
        if self.zw_terminal_df is None or self.zw_terminal_df.empty:
            logger.warning("未加载主网端子表，跳过主网电气边构建")
            logger.info(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
            return

        cn_to_terms_zw = defaultdict(list)
        term_to_equip_zw = {}
        for _, row in self.zw_terminal_df.iterrows():
            cn_id = str(row.get("CONNECT_NODE_ID") or row.get("CONNECTIVITYNODE_ID") or "")
            term_id = str(row.get("TERMINAL_ID") or row.get("ID") or "")
            if cn_id and term_id:
                cn_to_terms_zw[cn_id].append(term_id)
            if term_id:
                term_to_equip_zw[term_id] = str(row.get("EQUIP_ID") or "")

        for cn, term_list in cn_to_terms_zw.items():
            if len(term_list) < 2:
                continue
            for i in range(len(term_list)-1):
                t1 = term_list[i]
                t2 = term_list[i+1]
                # 与配网一致：同设备端子对由内部边负责，连接点边跳过
                if term_to_equip_zw.get(t1) and term_to_equip_zw.get(t2) and term_to_equip_zw[t1] == term_to_equip_zw[t2]:
                    continue
                e = TopoEdge(
                    line_id=f"CN_{cn}_{t1}_{t2}",
                    start_point=t1,
                    end_point=t2,
                    line_name=f"主网连接节点{cn}端子互连"
                )
                self.main_topo.add_edge(e)

        # -----S2修复：主配物理连接（147个重叠CN跨边）-----
        # 根因：ZWTERMINAL的CN（正数1090...）与PWTERMINAL的CN（负数）空间本不重叠，
        # 但实测仍有147个CN重叠——这些正是主配接口的真实物理连接点
        # （主网出线开关 如"10kV.LINE003_181开关" ↔ 配网馈线首端设备）。
        # 原代码对主/配各自独立建边，主配之间0跨接边，配网永远连不到主网电源，
        # 电源追溯断裂、孤岛判定失真。
        # 修复：把重叠CN的主网端子并入dist_topo（设备标is_source=True作为电源边界），
        # 并在配网端子↔主网端子之间建跨边，使配网通过物理边连到电源。
        cross_edge_count = 0
        main_dev_injected = 0
        try:
            if self.zw_terminal_df is not None and not self.zw_terminal_df.empty:
                zw_cn_to_terms = cn_to_terms_zw
                zw_term_to_equip = term_to_equip_zw
                for cn, zw_terms in zw_cn_to_terms.items():
                    if cn not in cn_to_terms:
                        continue  # 仅处理与配网重叠的CN
                    # 1) 主网端子并入dist_topo
                    for zt in zw_terms:
                        if zt in self.dist_topo.point_map:
                            continue
                        zdev_id = zw_term_to_equip.get(zt, "")
                        if not zdev_id:
                            continue
                        self.dist_topo.add_point(ConnectPoint(
                            point_id=zt,
                            belong_equip_id=zdev_id,
                            feeder_id="",
                        ))
                        # 2) 主网边界设备并入dist_topo（is_source=True=电源）
                        if zdev_id not in self.dist_topo.device_map:
                            zdev = self.main_topo.device_map.get(zdev_id)
                            if zdev is not None:
                                self.dist_topo.add_device(Device(
                                    equip_id=zdev_id,
                                    equip_name=zdev.equip_name or "",
                                    equip_type=zdev.equip_type or "",
                                    voltage_type=zdev.voltage_type or "",
                                    dsubstation_id=zdev.dsubstation_id or "",
                                    is_source=True,
                                ))
                                main_dev_injected += 1
                        self.dist_topo.link_device_point(zdev_id, zt)
                    # 3) 配网端子↔主网端子跨边
                    pw_terms = cn_to_terms[cn]
                    cross_terms = [t for t in zw_terms if t in self.dist_topo.point_map]
                    all_terms = pw_terms + cross_terms
                    if len(all_terms) >= 2:
                        for i in range(len(all_terms) - 1):
                            t1, t2 = all_terms[i], all_terms[i + 1]
                            # 同设备两端子跳过（设备内部通路负责）
                            e1 = term_to_equip.get(t1, "")
                            e2 = term_to_equip.get(t2, "")
                            if e1 and e2 and e1 == e2:
                                continue
                            e = TopoEdge(
                                line_id=f"CROSS_{cn}_{t1}_{t2}",
                                start_point=t1,
                                end_point=t2,
                                line_name=f"主配接口连接节点{cn}",
                            )
                            self.dist_topo.add_edge(e)
                            cross_edge_count += 1
                logger.info("[S2修复] 主配物理连接跨边建立: %d 条, 主网边界设备并入: %d 台",
                            cross_edge_count, main_dev_injected)
        except Exception as _s2e:
            logger.warning("[S2修复] 主配跨边建立异常（不影响主流程）: %s", _s2e)

        logger.info(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
        logger.info(f"[端子建边完成] 主网拓扑边数量：{self.main_topo.graph.number_of_edges()}")

    def fill_all_internal_connection(self):
        """批量补齐设备内部端子通路，传入真实端子ID列表"""
        # 先按设备聚合端子，避免 5 万设备场景下每台设备都遍历全部端子
        # （原 get_device_all_points 调用链会退化为 O(设备数 × 端子数)）。
        main_terms_by_equip = defaultdict(list)
        for point_id, point in self.main_topo.point_map.items():
            main_terms_by_equip[point.belong_equip_id].append(point_id)
        dist_terms_by_equip = defaultdict(list)
        for point_id, point in self.dist_topo.point_map.items():
            dist_terms_by_equip[point.belong_equip_id].append(point_id)

        # 主网设备
        for _, row in self.main_equip.iterrows():
            equip_id = row["EQUIP_ID"]
            term_ids = main_terms_by_equip[equip_id]
            build_device_internal_edges(self.main_topo, row, term_ids)
        # 配网设备
        for _, row in self.dist_equip.iterrows():
            equip_id = row["EQUIP_ID"]
            term_ids = dist_terms_by_equip[equip_id]
            build_device_internal_edges(self.dist_topo, row, term_ids)

    def check_topo_abnormal(self, topo: TopologyGraph, trace_id="TOPO001", measure_proc=None):
        """拓扑异常检测：悬空、孤岛、断点"""
        from core.topology_validator import run_database_topo_check
        abnormal_list, breakpoint_list, tie_loop_list = run_database_topo_check(topo, trace_id, measure_proc=measure_proc)
        # 将联络合环结果回写到topo对象，方便后续xlsx导出读取
        topo.tie_loop_list = tie_loop_list
        return abnormal_list, breakpoint_list

    def check_electrical_logic(self):
        """对有 PWREAL 的配网设备执行 RULE-E01--E07，并保留结构化结果供评分/Sheet3 导出。
        同时执行 4.1/4.2 主配接口校验并挂载到 abnormal_list。

        【幂等保护】如果已跑过（self.electrical_defects / self.iface_defects 已存在），
        直接返回缓存，避免 main.py 与 build_full_topology() 重复调用导致日志刷屏。
        """
        if getattr(self, '_electrical_logic_done', False):
            logger.debug("[幂等] check_electrical_logic 已执行过，跳过重复运行")
            return getattr(self, 'electrical_defects', [])
        from core.telemetry_evaluator import TelemetryEvaluator
        evaluator = TelemetryEvaluator.from_pwreal(
            self.yx_real_df,
            main_substation_data=None,
            zw_substation_df=self.zw_substation_df,
        )
        self.telemetry_evaluator = evaluator
        results = []
        for equip_id, dev in self.dist_topo.device_map.items():
            # 【P3修复】电气缺陷按设备归属馈线过滤，避免全网3500+缺陷混入单条馈线导致评分=0
            # dist_topo.device_map 中每个 device.feeder_id 已正确归属（PWEQUIPINFO.FEEDER_ID）
            # 对 1 条馈线，传入 feeder_id=None 表示全网（保持向后兼容）；传入具体 feeder_id 则过滤
            if self._feeder_filter and getattr(dev, 'feeder_id', '') != self._feeder_filter:
                continue
            results.extend(evaluator.evaluate_electrical_logic(equip_id, dev.equip_type or "", dev.voltage_type or ""))
        self.dist_topo.electrical_defects = results

                # --- 主配接口校验（v3 修复：按 api_doc Q41 走 CONNECTIVITYNODE_ID 拓扑对接）---
        # 4.1 漏拼：主网站无出线 / 馈线端子CN无主网对应端点（主配未拼接）
        # 4.2 错拼：馈线起始主网站(START_ST_ID)不存在 / CN拓扑对接主网站与START_ST_ID不一致
        #
        # Q41 官方口径：主配拼接通过拓扑节点来，主网线路端点节点可连接到配网节点表的
        # 馈线段；名称是辅助。实测：主网ZWTERMINAL.CN(正数) 与 配网PWTERMINAL.CN(负数)
        # 重叠147个=真实主配物理接口点；147条馈线经CN可对应主网站（0条错拼）。
        # v2 的 LINE_NAME 匹配在真实数据中映射=0（10kV.LINE003_181线 vs 10kVLINE003），
        # 导致 184 条"通过"全为降级放行——v3 改为按 CN 做真实拓扑验证（Q41）。
        from core.graph_model import AbnormalItem
        import uuid as _uuid
        from collections import defaultdict as _dd
        trace_uuid = "MAIN_SUB_IFACE_" + _uuid.uuid4().hex[:8]
        zw_st_ids = set(self.zw_substation_df["ST_ID"].astype(str)) if len(self.zw_substation_df) else set()

        # 1) 配网 CN → 馈线集合（端子→设备→FEEDER_ID）
        pw_cn_to_feeder: dict = _dd(set)
        if self.pw_terminal_df is not None and not self.pw_terminal_df.empty:
            eq_feeder: dict = {}
            if self.equip_df is not None and "FEEDER_ID" in self.equip_df.columns:
                for _, erow in self.equip_df.iterrows():
                    eq_feeder[str(erow.get("EQUIP_ID") or "").strip()] = \
                        str(erow.get("FEEDER_ID") or "").strip()
            for _, trow in self.pw_terminal_df.iterrows():
                cn = str(trow.get("CONNECTIVITYNODE_ID") or "").strip()
                eq = str(trow.get("EQUIP_ID") or "").strip()
                if not cn or not eq:
                    continue
                fid = eq_feeder.get(eq, "")
                if fid:
                    pw_cn_to_feeder[cn].add(fid)

        # 2) 主网 CN → 主网站集合（端子→设备→ST_ID）
        zw_cn_to_st: dict = _dd(set)
        if self.zw_terminal_df is not None and not self.zw_terminal_df.empty:
            zw_eq_st: dict = {}
            if self.zw_equip_df is not None and "ST_ID" in self.zw_equip_df.columns:
                for _, erow in self.zw_equip_df.iterrows():
                    zw_eq_st[str(erow.get("EQUIP_ID") or "").strip()] = \
                        str(erow.get("ST_ID") or "").strip()
            for _, trow in self.zw_terminal_df.iterrows():
                cn = str(trow.get("CONNECTIVITYNODE_ID") or "").strip()
                eq = str(trow.get("EQUIP_ID") or "").strip()
                if not cn or not eq:
                    continue
                st = zw_eq_st.get(eq, "")
                if st:
                    zw_cn_to_st[cn].add(st)

        iface_cnt_ok = 0
        iface_cnt_bad = 0
        iface_cnt_review = 0
        if self.line_df is not None and not self.line_df.empty:
            for _, lrow in self.line_df.iterrows():
                fid = str(lrow.get("LINE_ID") or "").strip()
                start_st = str(lrow.get("START_ST_ID") or "").strip()
                lname = str(lrow.get("LINE_NAME") or "").strip()
                passed = True
                code = ""
                detail = ""

                if not start_st or start_st.lower() in ("null", "nan", "none"):
                    passed, code, detail = False, "R_MAIN_IFACE_41", \
                        f"4.1漏拼：配网馈线{fid}({lname})缺失起始主网站(START_ST_ID为空)"
                elif start_st not in zw_st_ids:
                    passed, code, detail = False, "R_MAIN_IFACE_42", \
                        f"4.2错拼：配网馈线{fid}起始站ID={start_st} 不存在于主网变电站表(共{len(zw_st_ids)}个)"
                else:
                    # 【v3】按 CN 拓扑对接验证（Q41）：馈线端子CN ∩ 主网端子CN → 连接的主网站
                    feeder_cns = {cn for cn, fids in pw_cn_to_feeder.items() if fid in fids}
                    conn_st = set()
                    for cn in feeder_cns:
                        conn_st.update(zw_cn_to_st.get(cn, set()))
                    if not feeder_cns:
                        # 馈线无任何端子CN记录 → 信息缺失，标记"待复核"（Q49③：待确认可不强行修改，不计缺陷）
                        iface_cnt_review += 1
                        logger.debug(
                            "主配接口待复核: 馈线=%s 无端子CN记录，主配拼接关系待人工确认", fid)
                    elif not conn_st:
                        # 馈线有端子CN但主网无对应端点 → 主配未拼接（4.1漏拼）
                        passed, code, detail = False, "R_MAIN_IFACE_41", (
                            f"4.1漏拼：配网馈线{fid}({lname})端子CN({len(feeder_cns)}个)"
                            f"无主网对应端点，主配未拼接"
                        )
                    elif start_st not in conn_st:
                        # 馈线CN拓扑对接出的主网站 ≠ START_ST_ID → 4.2错拼
                        passed, code, detail = False, "R_MAIN_IFACE_42", (
                            f"4.2错拼：配网馈线{fid}({lname})经CN拓扑对接得主网站="
                            f"{sorted(conn_st)[:3]}，与START_ST_ID={start_st}不一致（疑似错拼）"
                        )
                    else:
                        # CN拓扑验证一致 → 真实通过（v2为降级放行，v3为真实验证）
                        logger.debug(
                            "主配接口CN验证通过: 馈线=%s CN=%d个 主网站=%s",
                            fid, len(feeder_cns), sorted(conn_st))

                if passed:
                    iface_cnt_ok += 1
                    continue
                iface_cnt_bad += 1
                item = AbnormalItem(
                    trace_uuid=trace_uuid,
                    equip_id=fid or "UNKNOWN_FEEDER",
                    point_id="",
                    rule_code=code,
                    rule_desc="主配网接口校验(4.1漏拼/4.2错拼)",
                    check_result="ERR",
                    review_status="待复核",
                    detail=detail,
                    dimension="接口规范性",
                    risk_level="高",
                )
                self.dist_topo.abnormal_list.append(item)
        logger.info("主配接口校验：通过=%d 失败=%d", iface_cnt_ok, iface_cnt_bad)
        logger.info(f"[主配接口校验] 4.1/4.2 命中缺陷: {iface_cnt_bad}")
        # 【M3修复】接口缺陷独立挂载（run_all_db_check 会 clear() abnormal_list，
        # 若不单独保存，4.1/4.2 缺陷会在拓扑异常检测阶段被冲掉，无法进入缺陷清单/评分）。
        self.iface_defects = [a for a in self.dist_topo.abnormal_list
                              if '接口' in getattr(a, 'dimension', '')]
        self.dist_topo.iface_defect_list = self.iface_defects
        self._electrical_logic_done = True  # 幂等保护标志
        return results

    def build_full_topology(self):
        """完整构建流程：拆分→加设备→生成真实端子→端子互连→设备内部通路→拓扑校验"""
        table_data = self.table_data

        self.split_voltage_data()
        self.add_all_devices()
        self._inject_main_substation_sources()
        self.build_real_terminal_points()
        self.build_graph_from_terminal()
        self.fill_all_internal_connection()

        # ============【全新遥信预处理调用】============
        from core.measure_preprocess import MeasurePreprocessor
        # ①新构造函数：只传完整table_data
        meas = MeasurePreprocessor(table_data, time_window_sec=5)

        # ②收集全部开关ID集合，从已经建好的topo设备map拿
        # 使用 constants.SWITCH_TYPES（包含数值码 1705/1706/1707/1708/1709 等）
        all_switch_ids = set()
        # 配网开关
        for eid, dev in self.dist_topo.device_map.items():
            if dev.equip_type in SWITCH_TYPES:
                all_switch_ids.add(eid)
        # 主网开关
        if len(self.main_topo.device_map) > 0:
            for eid, dev in self.main_topo.device_map.items():
                if dev.equip_type in SWITCH_TYPES:
                    all_switch_ids.add(eid)

        # ③执行run，把开关ID集合传给run方法
        final_state_map, source_map = meas.run(all_switch_ids)

        # ④回填每个Device的switch_status字段，并同步到图节点
        mounted = 0
        for eid, dev in self.dist_topo.device_map.items():
            if dev.equip_type in SWITCH_TYPES:
                state = final_state_map.get(eid, "CLOSE")
                dev.switch_status = state
                if eid in self.dist_topo.graph.nodes:
                    data = self.dist_topo.graph.nodes[eid]
                    info = data.get("dev_info", {})
                    info["switch_status"] = state
                    data["dev_info"] = info
                mounted += 1
        if len(self.main_topo.device_map) > 0:
            for eid, dev in self.main_topo.device_map.items():
                if dev.equip_type in SWITCH_TYPES:
                    state = final_state_map.get(eid, "CLOSE")
                    dev.switch_status = state
                    if eid in self.main_topo.graph.nodes:
                        data = self.main_topo.graph.nodes[eid]
                        info = data.get("dev_info", {})
                        info["switch_status"] = state
                        data["dev_info"] = info

        # 兼容旧字段保留（不使用，仅防止其他代码报key不存在）
        self.dist_topo.switch_state_map = final_state_map
        self.dist_topo.switch_state_source = source_map
        self.main_topo.switch_state_map = {}  # 主网默认空
        self.main_topo.switch_state_source = {}

        # 把预处理实例存到builder自身属性，后面传给校验器
        self.measure_proc = meas

        logger.info(f"[遥信预处理统计] 总开关状态映射条目:{len(final_state_map)} 实际挂载到设备:{mounted}")
        rtu_cnt = sum(1 for v in source_map.values() if v == "rtu")
        default_cnt = sum(1 for v in source_map.values() if v == "default_rule")
        logger.info(f"遥信实测开关:{rtu_cnt}，赛题默认合位推演开关:{default_cnt}")
        electrical_defects = self.check_electrical_logic()
        logger.info(f"[电气逻辑校验] RULE-E01~E07 命中:{len(electrical_defects)}")
        # ==============================================

        logger.info("开始执行拓扑异常检测：悬空、孤岛、断点")
        main_ready = len(self.main_equip) > 0 and len(self.main_topo.point_map) > 0
        if main_ready:
            main_abnormal, main_break = self.check_topo_abnormal(self.main_topo, trace_id="MAIN_001", measure_proc=self.measure_proc)
        else:
            logger.warning(
                "主网设备数或真实端子数为 0，已跳过主网拓扑构建与校验："
                f"设备数={len(self.main_equip)}，端子数={len(self.main_topo.point_map)}"
            )
            main_abnormal, main_break = [], []

        dist_abnormal, dist_break = self.check_topo_abnormal(self.dist_topo, trace_id="DIST_001", measure_proc=self.measure_proc)

        logger.info(f"主网异常数量：{len(main_abnormal)}，断点数量：{len(main_break)}")
        logger.info(f"配网异常数量：{len(dist_abnormal)}，断点数量：{len(dist_break)}")
        return self.main_topo, self.dist_topo
    
    def get_topo_statistics(self, topo: TopologyGraph, name: str):
        """输出拓扑统计信息（验收指标：节点、边、连通分量、设备清单）"""
        node_count = len(topo.graph.nodes)
        edge_count = len(topo.graph.edges)
        comp_list = list(nx.connected_components(topo.graph))
        comp_count = len(comp_list)
        equip_list = list(topo.device_map.keys())
        stat = {
            "拓扑名称": name,
            "总节点(端点)数": node_count,
            "总边数(线路+内部通路)": edge_count,
            "连通分量数量": comp_count,
            "设备ID清单": equip_list
        }
        return stat
