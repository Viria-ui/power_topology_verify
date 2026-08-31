# SQL数据构建拓扑图基类
import sys
import os
from collections import defaultdict
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
from config.settings import MAIN_VOLTAGE, DIST_VOLTAGE
from core.graph_model import TopologyGraph, Device, ConnectPoint, TopoEdge, build_device_internal_edges
from core.topo_checker import TopoChecker

class TopologyBuilder:
    def __init__(self, table_data: dict):
        self.equip_df = table_data["equip"]
        self.line_df = table_data["line"]
        # =========新增端子表DataFrame=========
        self.pw_terminal_df = table_data.get("pw_terminal", None)
        self.zw_terminal_df = table_data.get("zw_terminal", None)
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
        for _, row in self.pw_terminal_df.iterrows():
            term_id = str(row["TERMINAL_ID"])
            dev_id = str(row["DEVICE_ID"])
            if dev_id not in self.dist_topo.device_map:
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
        for _, row in self.zw_terminal_df.iterrows():
            term_id = str(row["TERMINAL_ID"])
            dev_id = str(row["DEVICE_ID"])
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
        if self.pw_terminal_df is None:
            print("[警告] 未加载配网端子表，无法构建配网电气边")
            return
        if self.zw_terminal_df is None:
            print("[警告] 未加载主网端子表，无法构建主网电气边")
            return

        # -----配网端子建边-----
        cn_to_terms = defaultdict(list)
        for _, row in self.pw_terminal_df.iterrows():
            cn_id = str(row["CONNECT_NODE_ID"])
            term_id = str(row["TERMINAL_ID"])
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
        cn_to_terms_zw = defaultdict(list)
        for _, row in self.zw_terminal_df.iterrows():
            cn_id = str(row["CONNECT_NODE_ID"])
            term_id = str(row["TERMINAL_ID"])
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
        # 主网设备
        for _, row in self.main_equip.iterrows():
            equip_id = row["EQUIP_ID"]
            term_ids = self.main_topo.get_device_all_points(equip_id)
            build_device_internal_edges(self.main_topo, row, term_ids)
        # 配网设备
        for _, row in self.dist_equip.iterrows():
            equip_id = row["EQUIP_ID"]
            term_ids = self.dist_topo.get_device_all_points(equip_id)
            build_device_internal_edges(self.dist_topo, row, term_ids)

    def check_topo_abnormal(self, topo: TopologyGraph, trace_id="TOPO001"):
        """执行悬空、孤岛、断点检测"""
        checker = TopoChecker(topo)
        abnormal_list, breakpoint_list = checker.run_full_check(trace_uuid=trace_id)
        return abnormal_list, breakpoint_list

    def build_full_topology(self):
        """完整构建流程：拆分→加设备→生成真实端子→端子互连→设备内部通路→拓扑校验"""
        self.split_voltage_data()
        self.add_all_devices()
        self.build_real_terminal_points()
        self.build_graph_from_terminal()
        self.fill_all_internal_connection()
        print("开始执行拓扑异常检测：悬空、孤岛、断点")
        main_abnormal, main_break = self.check_topo_abnormal(self.main_topo, trace_id="MAIN_001")
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
