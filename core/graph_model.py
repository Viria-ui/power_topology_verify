"""设备/端点/边 拓扑图数据结构定义。"""
from pydantic import BaseModel
import networkx as nx
from typing import Optional


class Device(BaseModel):
    equip_id: str
    equip_name: Optional[str] = None
    equip_type: Optional[str] = None
    voltage_type: Optional[str] = None
    feeder_id: Optional[str] = None
    dsubstation_id: Optional[str] = None


class ConnectPoint(BaseModel):
    point_id: str
    belong_equip_id: str
    feeder_id: Optional[str] = None


class TopoEdge(BaseModel):
    line_id: str
    start_point: str
    end_point: Optional[str] = None
    line_name: Optional[str] = None


class AbnormalItem(BaseModel):
    trace_uuid: str
    equip_id: str
    point_id: str
    line_id: Optional[str] = None
    rule_code: str
    rule_desc: str
    check_result: str
    review_status: str = "待复核"
    detail: str


class BreakpointItem(BaseModel):
    trace_uuid: str
    equip_id: str
    point_id: str
    line_id: Optional[str] = None
    component_size: int
    rule_code: str
    rule_desc: str
    detail: str


class TieLoopItem(BaseModel):
    trace_uuid: str
    equip_id: str
    point_id: str
    line_id: Optional[str] = None
    result_type: str  # 联络 / 合环
    rule_code: str
    rule_desc: str
    detail: str


class TopologyGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.device_map: dict[str, Device] = {}
        self.point_map: dict[str, ConnectPoint] = {}
        self.edge_map: dict[str, TopoEdge] = {}
        self.abnormal_list: list[AbnormalItem] = []
        self.breakpoint_list: list[BreakpointItem] = []
        self.tie_loop_list: list[TieLoopItem] = []

    def add_device(self, dev: Device):
        self.device_map[dev.equip_id] = dev
        self.graph.add_node(dev.equip_id, node_type="device", dev_info=dev.model_dump())

    def add_point(self, pt: ConnectPoint):
        self.point_map[pt.point_id] = pt
        self.graph.add_node(pt.point_id, node_type="point", pt_info=pt.model_dump())

    def add_edge(self, edge: TopoEdge):
        self.edge_map[edge.line_id] = edge
        if edge.end_point:
            self.graph.add_edge(edge.start_point, edge.end_point, edge_info=edge.model_dump())

    def link_device_point(self, equip_id: str, point_id: str):
        if equip_id in self.device_map and point_id in self.point_map:
            self.graph.add_edge(equip_id, point_id, edge_type="terminal")


# 新增：设备内部端点连通生成函数（解决导入报错）
def build_device_internal_edges(topo: TopologyGraph, equip_row, term_list: list[str]):
    """
    为单台设备生成内部连通边
    topo：拓扑容器
    equip_row：设备单行数据（EQUIP_ID,EQUIP_TYPE）
    term_list：该设备全部端点ID列表
    """
    equip_id = equip_row["EQUIP_ID"]
    equip_type = equip_row["EQUIP_TYPE"]
    if len(term_list) < 2:
        return  # 单个端子无内部连接

    # 1.变压器：高压端子 ↔ 低压端子，一条内部边
    if "变压器" in equip_type:
        e = TopoEdge(
            line_id=f"INT_TRAFO_{equip_id}",
            start_point=term_list[0],
            end_point=term_list[1],
            line_name=f"设备{equip_id}内部变压通路"
        )
        topo.add_edge(e)
    # 2.断路器/隔离开关：进线端子 ↔ 出线端子
    elif equip_type in ["断路器", "隔离开关", "负荷开关"]:
        e = TopoEdge(
            line_id=f"INT_SWITCH_{equip_id}",
            start_point=term_list[0],
            end_point=term_list[1],
            line_name=f"设备{equip_id}内部开关通路"
        )
        topo.add_edge(e)
    # 3.母线：所有端子两两互通
    elif "母线" in equip_type:
        for i in range(len(term_list)):
            for j in range(i+1, len(term_list)):
                e = TopoEdge(
                    line_id=f"INT_BUS_{equip_id}_{i}_{j}",
                    start_point=term_list[i],
                    end_point=term_list[j],
                    line_name=f"母线{equip_id}内部连通"
                )
                topo.add_edge(e)
    # 其他设备（负荷、电容器）无内部通路
    else:
        return
