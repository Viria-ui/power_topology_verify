# SQL数据构建拓扑图基类
import sys
import os
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
        # 主网设备
        for _, row in self.main_equip.iterrows():
            dev = Device(
                equip_id=row["EQUIP_ID"],
                equip_name=row["EQUIP_NAME"],
                equip_type=row["EQUIP_TYPE"],
                voltage_type=row["VOLTAGE_TYPE"],
                feeder_id=str(row["FEEDER_ID"]) if row["FEEDER_ID"] is not None else "",
                dsubstation_id=str(row["DSUBSTATION_ID"]) if row["DSUBSTATION_ID"] is not None else ""
            )
            self.main_topo.add_device(dev)
            # 模拟端点：PT_设备ID
            pt = ConnectPoint(
                point_id=f"PT_{row['EQUIP_ID']}",
                belong_equip_id=row["EQUIP_ID"],
                feeder_id=str(row["FEEDER_ID"]) if row["FEEDER_ID"] is not None else ""
            )
            self.main_topo.add_point(pt)

        # 配网设备
        for _, row in self.dist_equip.iterrows():
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

    def add_external_line_edges(self):
        """添加外部馈线线路（跨设备端点连接）"""
        # 主网线路
        for _, row in self.main_line.iterrows():
            start_st = row.get("START_ST_ID")
            end_st = row.get("END_ST_ID")
            if start_st:
                edge = TopoEdge(
                    line_id=row["LINE_ID"],
                    start_point=f"PT_{start_st}",
                    end_point=f"PT_{end_st}" if end_st else None,
                    line_name=row.get("LINE_NAME", "")
                )
                self.main_topo.add_edge(edge)
        # 配网线路
        for _, row in self.dist_line.iterrows():
            start_st = row.get("START_ST_ID")
            end_st = row.get("END_ST_ID")
            if start_st:
                edge = TopoEdge(
                    line_id=row["LINE_ID"],
                    start_point=f"PT_{start_st}",
                    end_point=f"PT_{end_st}" if end_st else None,
                    line_name=row.get("LINE_NAME", "")
                )
                self.dist_topo.add_edge(edge)

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
        self.add_external_line_edges()
        self.fill_all_internal_connection()
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