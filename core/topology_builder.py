# SQL数据构建拓扑图基类
from __future__ import annotations
import sys
import os
import logging
import pandas as pd
from collections import defaultdict

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
        print(f"主网设备数量：{len(self.main_equip)}")
        print(f"配网设备数量：{len(self.dist_equip)}")
        print(f"主网线路(ZLINEEND)数量：{len(self.main_line)}")
        print(f"配网线路(PWFEEDERLINE)数量：{len(self.dist_line)}")
        print(f"主网站点(ZWSUBSTATION)数量：{len(self.zw_substation_df)}")
        print(f"遥信遥测(PWREAL)记录数：{len(self.yx_real_df)}")
        print(f"主网遥测(ZWMEA)：{len(self.zw_mea_df)} 主网遥信(ZWSIGNAL)：{len(self.zw_signal_df)}")

    def _is_source_type(self, equip_type_val: str, equip_name: str = "") -> bool:
        """电源识别：数值码/中文名/CIM + 设备名称关键字三栖判定，避免0台电源。"""
        if not equip_type_val:
            return False
        t = str(equip_type_val).strip()
        if t in SOURCE_TYPES:
            return True
        name = str(equip_name or "")
        keywords = ("变电站", "站房", "主变", "变", "SUB", "STATION", "Trafo", "TRANSFORMER")
        if any(k in name for k in keywords) and t in SOURCE_TYPES:
            return True
        # 主网设备默认识别：110kV侧的任何变压器/变电站默认电源
        return False

    def add_all_devices(self):
        """批量添加设备"""
        print(f"  [Builder] 正在添加 {len(self.main_equip)} 个主网设备和 {len(self.dist_equip)} 个配网设备...")
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
        print(f"    - 主网电源设备识别: {src_cnt_main} 台")

        src_cnt_dist = 0
        for i, (_, row) in enumerate(self.dist_equip.iterrows()):
            if i % 10000 == 0 and i > 0:
                print(f"    - 已处理 {i} 个配网设备")

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
        print(f"    - 配网电源设备识别: {src_cnt_dist} 台")
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
            print(f"    - 通过ZWSUBSTATION补充注入电源: {src_cnt_main} 台")
            
    def build_real_terminal_points(self):
        """从端子表生成真实端子ConnectPoint，point_id=TERMINAL_ID"""
        # 配网端子
        if self.pw_terminal_df is None or self.pw_terminal_df.empty:
            print("[警告] 未加载配网端子表，跳过配网真实端子生成")
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

        print(f"[Builder] 配网真实端子数量:{len(self.dist_topo.point_map)}")
        print(f"[Builder] 主网真实端子数量:{len(self.main_topo.point_map)}")


    def build_graph_from_terminal(self):
        """同CONNECT_NODE_ID下真实端子之间互连，节点为TERMINAL_ID"""
        if self.pw_terminal_df is None or self.pw_terminal_df.empty:
            print("[警告] 未加载配网端子表，无法构建配网电气边")
        else:
            # -----配网端子建边-----
            cn_to_terms = defaultdict(list)
            for _, row in self.pw_terminal_df.iterrows():
                cn_id = str(row.get("CONNECT_NODE_ID") or row.get("CONNECTIVITYNODE_ID") or "")
                term_id = str(row.get("TERMINAL_ID") or row.get("ID") or "")
                if cn_id and term_id:
                    cn_to_terms[cn_id].append(term_id)

            for cn, term_list in cn_to_terms.items():
                if len(term_list) < 2:
                    continue
                for i in range(len(term_list)-1):
                    t1 = term_list[i]
                    t2 = term_list[i+1]
                    e = TopoEdge(
                        line_id=f"CN_{cn}_{t1}_{t2}",
                        start_point=t1,
                        end_point=t2,
                        line_name=f"连接节点{cn}端子互连"
                    )
                    self.dist_topo.add_edge(e)

        # -----主网端子建边-----
        if len(self.main_equip) == 0 or len(self.main_topo.point_map) == 0:
            print(
                "[警告] 主网设备数或真实端子数为 0，跳过主网拓扑构建："
                f"设备数={len(self.main_equip)}，端子数={len(self.main_topo.point_map)}"
            )
            print(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
            return
        if self.zw_terminal_df is None or self.zw_terminal_df.empty:
            print("[警告] 未加载主网端子表，跳过主网电气边构建")
            print(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
            return

        cn_to_terms_zw = defaultdict(list)
        for _, row in self.zw_terminal_df.iterrows():
            cn_id = str(row.get("CONNECT_NODE_ID") or row.get("CONNECTIVITYNODE_ID") or "")
            term_id = str(row.get("TERMINAL_ID") or row.get("ID") or "")
            if cn_id and term_id:
                cn_to_terms_zw[cn_id].append(term_id)

        for cn, term_list in cn_to_terms_zw.items():
            if len(term_list) < 2:
                continue
            for i in range(len(term_list)-1):
                t1 = term_list[i]
                t2 = term_list[i+1]
                e = TopoEdge(
                    line_id=f"CN_{cn}_{t1}_{t2}",
                    start_point=t1,
                    end_point=t2,
                    line_name=f"主网连接节点{cn}端子互连"
                )
                self.main_topo.add_edge(e)

        print(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
        print(f"[端子建边完成] 主网拓扑边数量：{self.main_topo.graph.number_of_edges()}")

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
        """
        from core.telemetry_evaluator import TelemetryEvaluator
        evaluator = TelemetryEvaluator.from_pwreal(
            self.yx_real_df,
            main_substation_data=None,
            zw_substation_df=self.zw_substation_df,
        )
        self.telemetry_evaluator = evaluator
        results = []
        for equip_id, dev in self.dist_topo.device_map.items():
            results.extend(evaluator.evaluate_electrical_logic(equip_id, dev.equip_type or ""))
        self.dist_topo.electrical_defects = results

        # --- 主配接口校验（Q41 拓扑节点对齐 + Q42 漏拼/错拼） ---
        from core.graph_model import AbnormalItem
        import uuid as _uuid
        trace_uuid = "MAIN_SUB_IFACE_" + _uuid.uuid4().hex[:8]
        feeder_to_stations: dict[str, set[str]] = defaultdict(set)
        for equip_id, dev in self.dist_topo.device_map.items():
            fid = dev.feeder_id or ""
            sid = dev.dsubstation_id or ""
            if fid and sid:
                feeder_to_stations[fid].add(sid)
        iface_cnt_ok = 0
        iface_cnt_bad = 0
        for fid, station_set in feeder_to_stations.items():
            if not station_set:
                continue
            for station_id in sorted(station_set):
                passed, conf, detail = evaluator.verify_main_substation_interface(
                    fid, station_id,
                    feeder_line_ids=None,
                    zw_lineend_df=self.zw_line_end_df,
                )
                if passed:
                    iface_cnt_ok += 1
                    continue
                iface_cnt_bad += 1
                item = AbnormalItem(
                    trace_uuid=trace_uuid,
                    equip_id=fid or "UNKNOWN_FEEDER",
                    point_id="",
                    rule_code="R_MAIN_IFACE_41" if "漏拼" in detail else "R_MAIN_IFACE_42",
                    rule_desc="主配网接口校验(4.1漏拼/4.2错拼)" if not "漏拼" in detail else detail.split("：")[0],
                    check_result="ERR",
                    review_status="待复核",
                    detail=detail,
                    dimension="接口规范性",
                    risk_level="高",
                )
                self.dist_topo.abnormal_list.append(item)
        logger.info("主配接口校验：通过=%d 失败=%d", iface_cnt_ok, iface_cnt_bad)
        print(f"[主配接口校验] 4.1/4.2 命中缺陷: {iface_cnt_bad}")
        return results

    def build_full_topology(self):
        """完整构建流程：拆分→加设备→生成真实端子→端子互连→设备内部通路→拓扑校验"""
        table_data = self.table_data

        self.split_voltage_data()
        self.add_all_devices()
        self.build_real_terminal_points()
        self.build_graph_from_terminal()
        self.fill_all_internal_connection()

        # ============【全新遥信预处理调用】============
        from core.measure_preprocess import MeasurePreprocessor
        # ①新构造函数：只传完整table_data
        meas = MeasurePreprocessor(table_data, time_window_sec=5)

        # ②收集全部开关ID集合，从已经建好的topo设备map拿（优先，不要从原始equip_df）
        switch_type_set = {"断路器", "隔离开关", "负荷开关", "接地隔离开关"}
        all_switch_ids = set()
        # 配网开关
        for eid, dev in self.dist_topo.device_map.items():
            if dev.equip_type in switch_type_set:
                all_switch_ids.add(eid)
        # 主网开关
        if len(self.main_topo.device_map) > 0:
            for eid, dev in self.main_topo.device_map.items():
                if dev.equip_type in switch_type_set:
                    all_switch_ids.add(eid)

        # ③执行run，把开关ID集合传给run方法
        final_state_map, source_map = meas.run(all_switch_ids)

        # ④回填每个Device的switch_status字段，并同步到图节点
        mounted = 0
        for eid, dev in self.dist_topo.device_map.items():
            if dev.equip_type in switch_type_set:
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
                if dev.equip_type in switch_type_set:
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

        print(f"[遥信预处理统计] 总开关状态映射条目:{len(final_state_map)} 实际挂载到设备:{mounted}")
        rtu_cnt = sum(1 for v in source_map.values() if v == "rtu")
        default_cnt = sum(1 for v in source_map.values() if v == "default_rule")
        print(f"  -->遥信实测开关:{rtu_cnt}，赛题默认合位推演开关:{default_cnt}")
        electrical_defects = self.check_electrical_logic()
        print(f"[电气逻辑校验] RULE-E01~E07 命中:{len(electrical_defects)}")
        # ==============================================

        print("开始执行拓扑异常检测：悬空、孤岛、断点")
        main_ready = len(self.main_equip) > 0 and len(self.main_topo.point_map) > 0
        if main_ready:
            main_abnormal, main_break = self.check_topo_abnormal(self.main_topo, trace_id="MAIN_001", measure_proc=self.measure_proc)
        else:
            print(
                "[警告] 主网设备数或真实端子数为 0，已跳过主网拓扑构建与校验："
                f"设备数={len(self.main_equip)}，端子数={len(self.main_topo.point_map)}"
            )
            main_abnormal, main_break = [], []

        dist_abnormal, dist_break = self.check_topo_abnormal(self.dist_topo, trace_id="DIST_001", measure_proc=self.measure_proc)

        print(f"主网异常数量：{len(main_abnormal)}，断点数量：{len(main_break)}")
        print(f"配网异常数量：{len(dist_abnormal)}，断点数量：{len(dist_break)}")
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
