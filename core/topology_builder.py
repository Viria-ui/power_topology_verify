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
        """批量添加设备、绑定模拟端点（后续对接端子表替换真实端点）"""
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
                dsubstation_id=str(row["DSUBSTATION_ID"]) if row["DSUBSTATION_ID"] is not None else ""
            )
            self.dist_topo.add_device(dev)
            pt = ConnectPoint(
                point_id=f"PT_{row['EQUIP_ID']}",
                belong_equip_id=row["EQUIP_ID"],
                feeder_id=str(row["FEEDER_ID"]) if row["FEEDER_ID"] is not None else ""
            )
            self.dist_topo.add_point(pt)

    def build_graph_from_terminal(self):
        """【核心】端子表构建真实电气连通边"""
        if self.pw_terminal_df is None:
            print("[警告] 未加载配网端子表，无法构建配网电气边！")
            return
        if self.zw_terminal_df is None:
            print("[警告] 未加载主网端子表，无法构建主网电气边！")
            return

        # -----配网端子建边-----
        node_to_devs = defaultdict(list)
        for _, row in self.pw_terminal_df.iterrows():
            dev_id = str(row["DEVICE_ID"])
            cn_id = str(row["CONNECT_NODE_ID"])
            node_to_devs[cn_id].append(dev_id)

        for cn, dev_list in node_to_devs.items():
            if len(dev_list) < 2:
                continue
            for i in range(len(dev_list)-1):
                pt_a = f"PT_{dev_list[i]}"
                pt_b = f"PT_{dev_list[i+1]}"
                self.dist_topo.graph.add_edge(pt_a, pt_b)

        # -----主网端子建边-----
        node_to_devs_zw = defaultdict(list)
        for _, row in self.zw_terminal_df.iterrows():
            dev_id = str(row["DEVICE_ID"])
            cn_id = str(row["CONNECT_NODE_ID"])
            node_to_devs_zw[cn_id].append(dev_id)

        for cn, dev_list in node_to_devs_zw.items():
            if len(dev_list) < 2:
                continue
            for i in range(len(dev_list)-1):
                pt_a = f"PT_{dev_list[i]}"
                pt_b = f"PT_{dev_list[i+1]}"
                self.main_topo.graph.add_edge(pt_a, pt_b)

        print(f"[端子建边完成] 配网拓扑边数量：{self.dist_topo.graph.number_of_edges()}")
        print(f"[端子建边完成] 主网拓扑边数量：{self.main_topo.graph.number_of_edges()}")

    def fill_all_internal_connection(self):
        """批量补齐所有设备内部端点连通关系"""
        # 主网设备补内部边
        for _, row in self.main_equip.iterrows():
            dev_pts = [f"PT_{row['EQUIP_ID']}"]
            build_device_internal_edges(self.main_topo, row, dev_pts)
        # 配网设备补内部边
        for _, row in self.dist_equip.iterrows():
            dev_pts = [f"PT_{row['EQUIP_ID']}"]
            build_device_internal_edges(self.dist_topo, row, dev_pts)

    def build_full_topology(self):
        """完整构建流程：拆分→加设备→加外部线路→补内部连通"""
        self.split_voltage_data()
        self.add_all_devices()
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
