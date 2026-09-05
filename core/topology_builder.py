# SQL数据构建拓扑图基类
import sys
import os
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


class TopologyBuilder:
    def __init__(self, table_data: dict):
        self.table_data = table_data
        self.equip_df = table_data["equip"]
        self.line_df = table_data["line"]

        self.pw_terminal_df = table_data.get("pw_terminal")
        self.zw_terminal_df = table_data.get("zw_terminal")
        # 初始化两套独立拓扑
        self.main_topo = TopologyGraph()    # 110kV主网
        self.dist_topo = TopologyGraph()    # 10kV配网

    def split_voltage_data(self):
        """直接全部数据归入配网，跳过电压匹配逻辑"""
        # 清理列名防止后续读取报错
        self.equip_df.columns = [col.strip() for col in self.equip_df.columns]
        self.line_df.columns = [col.strip() for col in self.line_df.columns]
        if self.pw_terminal_df is not None:
            self.pw_terminal_df.columns = [col.strip() for col in self.pw_terminal_df.columns]
        if self.zw_terminal_df is not None:
            self.zw_terminal_df.columns = [col.strip() for col in self.zw_terminal_df.columns]
    
        # 主网空，所有设备进配网
        self.main_equip = self.equip_df.iloc[0:0]
        self.dist_equip = self.equip_df.copy()
    
        # 线路同理
        self.main_line = self.line_df.iloc[0:0]
        self.dist_line = self.line_df.copy()
        
        print(f"主网设备数量：{len(self.main_equip)}")
        print(f"配网设备数量：{len(self.dist_equip)}")
        print(f"主网线路数量：{len(self.main_line)}")
        print(f"配网线路数量：{len(self.dist_line)}")

    def add_all_devices(self):
        """批量添加设备"""
        print(f"  [Builder] 正在添加 {len(self.dist_equip)} 个配网设备...")
        source_type_list = ["变电站", "1701"]
        # 配网设备
        for i, (_, row) in enumerate(self.dist_equip.iterrows()):
            if i % 10000 == 0 and i > 0:
                print(f"    - 已处理 {i} 个设备")
                
            equip_type_val = str(row.get("EQUIP_TYPE", ""))
            is_source = equip_type_val in source_type_list
            
            dev = Device(
                equip_id=row["EQUIP_ID"],
                equip_name=row["EQUIP_NAME"],
                equip_type=row["EQUIP_TYPE"],
                voltage_type=row["VOLTAGE_TYPE"],
                feeder_id=str(row["FEEDER_ID"]) if row["FEEDER_ID"] is not None else "",
                dsubstation_id=str(row["DSUBSTATION_ID"]) if row["DSUBSTATION_ID"] is not None else "",
                is_source=is_source
            )
            self.dist_topo.add_device(dev)
            
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

    def check_topo_abnormal(self, topo: TopologyGraph, trace_id="TOPO001"):
        """拓扑异常检测：悬空、孤岛、断点"""
        from core.topology_validator import run_database_topo_check
        abnormal_list, breakpoint_list, tie_loop_list = run_database_topo_check(topo, trace_id)
        # 将联络合环结果回写到topo对象，方便后续xlsx导出读取
        topo.tie_loop_list = tie_loop_list
        return abnormal_list, breakpoint_list

    def build_full_topology(self):
        """完整构建流程：拆分→加设备→生成真实端子→端子互连→设备内部通路→拓扑校验"""
        table_data = self.table_data   # 构造函数传入的原始table_data

        # ①提取全部开关设备ID集合
        equip_df = table_data.get("equip", pd.DataFrame())
        switch_type_list = {"断路器", "负荷开关", "隔离开关", "接地隔离开关"}
        all_switch_ids = set()
        if not equip_df.empty:
            mask_sw = equip_df["EQUIP_TYPE"].isin(switch_type_list)
            sw_rows = equip_df.loc[mask_sw]
            all_switch_ids = set(str(x) for x in sw_rows["EQUIP_ID"].tolist())

        # ②拿到遥信表，永远传DataFrame，不传None
        yx_df = table_data.get("yx_real", pd.DataFrame())

        # ③执行遥信预处理
        from core.measure_preprocess import MeasurePreprocessor
        meas = MeasurePreprocessor(yx_df, all_switch_ids, time_window_sec=5)
        #switch_state_map, state_source_map = meas.run()
        switch_state_map = dict()
        state_source_map = dict()

        # ④挂载到配网拓扑对象 dist_topo（此时dist_topo还没实例化，先不赋值，等new出来再赋值）
        # =====================================================================

        self.split_voltage_data()
        self.add_all_devices()
        self.build_real_terminal_points()
        self.build_graph_from_terminal()
        self.fill_all_internal_connection()

        # ----------------拓扑对象已经创建完成，给dist_topo挂载开关状态字典----------------
        self.dist_topo.switch_state_map = switch_state_map
        self.dist_topo.switch_state_source = state_source_map
        print(f"[遥信预处理统计] 总开关数量:{len(switch_state_map)}")
        rtu_cnt = sum(1 for v in state_source_map.values() if v == "rtu")
        default_cnt = sum(1 for v in state_source_map.values() if v == "default_rule")
        print(f"  -->遥信实测开关:{rtu_cnt}，赛题默认合位推演开关:{default_cnt}")

        print("开始执行拓扑异常检测：悬空、孤岛、断点")
        main_ready = len(self.main_equip) > 0 and len(self.main_topo.point_map) > 0
        if main_ready:
            main_abnormal, main_break = self.check_topo_abnormal(self.main_topo, trace_id="MAIN_001")
        else:
            print(
                "[警告] 主网设备数或真实端子数为 0，已跳过主网拓扑构建与校验："
                f"设备数={len(self.main_equip)}，端子数={len(self.main_topo.point_map)}"
            )
            main_abnormal, main_break = [], []
        dist_abnormal, dist_break = self.check_topo_abnormal(self.dist_topo, trace_id="DIST_001")
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
