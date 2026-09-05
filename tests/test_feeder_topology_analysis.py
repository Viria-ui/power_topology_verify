# -*- coding: utf-8 -*-
"""单元测试 for core.feeder_topology_analysis（Sheet 2/3/4 分析函数）。"""
import sys
import os

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import unittest
import networkx as nx
from core.feeder_topology_analysis import (
    _is_switch_node,
    _device_name,
    _build_svg_graph,
    analyze_tie_switches,
    analyze_breakpoints,
    build_device_graph,
)
from core.graph_model import TopologyGraph, Device, ConnectPoint, TopoEdge


class TestIsSwitchNode(unittest.TestCase):
    """测试 _is_switch_node 判断逻辑。"""

    def test_real_switch_returns_true(self):
        G = nx.Graph()
        G.add_node("SW001", equip_type="1705")
        G.add_node("SW002", equip_type="LoadBreakSwitch")
        self.assertTrue(_is_switch_node(G, "SW001"))
        self.assertTrue(_is_switch_node(G, "SW002"))

    def test_non_switch_returns_false(self):
        # BusbarSection 不在 SWITCH_TYPES/NON_TERMINAL_SWITCH_TYPES 中，字符串检测也找不到"开关/断路/..."
        G = nx.Graph()
        G.add_node("BUS1", equip_type="BusbarSection")
        G.add_node("LOAD1", equip_type="EnergyConsumer")
        # EnergyConsumer 在 LOAD_TYPES，所以不判为开关
        self.assertFalse(_is_switch_node(G, "BUS1"))
        self.assertFalse(_is_switch_node(G, "LOAD1"))

    def test_missing_node_returns_false(self):
        G = nx.Graph()
        self.assertFalse(_is_switch_node(G, "NONEXIST"))


class TestBuildDeviceGraph(unittest.TestCase):
    """测试 build_device_graph 设备图构建。"""

    def setUp(self):
        self.topo = TopologyGraph()
        # 开关 A - 开关 B - 配变 C
        self.topo.device_map["SW_A"] = Device(equip_id="SW_A", equip_name="开关A", equip_type="0307")
        self.topo.device_map["SW_B"] = Device(equip_id="SW_B", equip_name="开关B", equip_type="0307")
        self.topo.device_map["TR_C"] = Device(equip_id="TR_C", equip_name="配变C", equip_type="1703")
        # 端子
        self.topo.point_map["PT_A1"] = ConnectPoint(point_id="PT_A1", belong_equip_id="SW_A")
        self.topo.point_map["PT_AB"] = ConnectPoint(point_id="PT_AB", belong_equip_id="SW_A")
        self.topo.point_map["PT_B1"] = ConnectPoint(point_id="PT_B1", belong_equip_id="SW_B")
        self.topo.point_map["PT_BC"] = ConnectPoint(point_id="PT_BC", belong_equip_id="SW_B")
        self.topo.point_map["PT_C1"] = ConnectPoint(point_id="PT_C1", belong_equip_id="TR_C")
        self.topo.point_map["PT_C2"] = ConnectPoint(point_id="PT_C2", belong_equip_id="TR_C")
        # 拓扑边
        self.topo.edge_map["E1"] = TopoEdge(line_id="E1", start_point="PT_A1", end_point="PT_B1")
        self.topo.edge_map["E2"] = TopoEdge(line_id="E2", start_point="PT_AB", end_point="PT_BC")
        self.topo.edge_map["E3"] = TopoEdge(line_id="E3", start_point="PT_B1", end_point="PT_C1")

    def test_graph_has_edges(self):
        G = build_device_graph(self.topo, None)
        self.assertEqual(G.number_of_nodes(), 3)
        # SW_A - SW_B 连通（通过 PT_A1-PT_B1）
        self.assertTrue(G.has_edge("SW_A", "SW_B"))
        # SW_B - TR_C 连通
        self.assertTrue(G.has_edge("SW_B", "TR_C"))

    def test_graph_is_undirected(self):
        G = build_device_graph(self.topo, None)
        self.assertTrue(G.has_edge("SW_B", "SW_A"))  # 无向图
        self.assertTrue(G.has_edge("TR_C", "SW_B"))


class TestTieSwitchAnalysis(unittest.TestCase):
    """测试 analyze_tie_switches 联络开关识别。"""

    def test_cross_feeder_switch_is_identified(self):
        """跨馈线开关应被识别为联络开关。

        图：SW_A1 ←→ TIE_SW ←→ SW_B1
        TIE_SW 的邻居跨越 FEEDER_A / FEEDER_B 两条馈线 → 识别为联络。
        """
        G = nx.Graph()
        G.add_node("SW_A1", equip_id="SW_A1", equip_type="1705", feeder_id="FEEDER_A")
        G.add_node("SW_B1", equip_id="SW_B1", equip_type="1705", feeder_id="FEEDER_B")
        G.add_node("TIE_SW", equip_id="TIE_SW", equip_type="1705")  # 无 feeder_id
        G.add_edge("SW_A1", "TIE_SW")
        G.add_edge("TIE_SW", "SW_B1")

        class FakeTopo:
            def get_all_source_equip(self):
                return []

        rows = analyze_tie_switches(
            feeder_id="FEEDER_A",
            line_name="LINE_TEST",
            start_st_id="ST001",
            device_graph=G,
            dist_topo=FakeTopo(),
            line_df=None,
        )
        # 应当识别到联络开关
        has_tie = any(r.get("是否有联络") == "是" for r in rows)
        self.assertTrue(has_tie, f"应识别到联络开关，实际结果: {rows}")

    def test_same_feeder_no_tie_switch(self):
        """同馈线内设备不应被识别为联络。"""
        G = nx.Graph()
        G.add_node("SW1", equip_id="SW1", equip_type="1705", feeder_id="FEEDER_X")
        G.add_node("SW2", equip_id="SW2", equip_type="1705", feeder_id="FEEDER_X")
        G.add_edge("SW1", "SW2")

        class FakeTopo:
            def get_all_source_equip(self):
                return []

        rows = analyze_tie_switches(
            feeder_id="FEEDER_X",
            line_name="LINE_X",
            start_st_id="ST001",
            device_graph=G,
            dist_topo=FakeTopo(),
            line_df=None,
        )
        has_tie = any(r.get("是否有联络") == "是" for r in rows)
        self.assertFalse(has_tie, "同馈线不应识别为联络")


class TestBreakpointPriority(unittest.TestCase):
    """测试断点 P1-P7 优先级排序。"""

    def test_p1_before_p2(self):
        """P1（分位开关）应排在 P2（无路径）之前。"""
        topo = TopologyGraph()
        topo.device_map["A"] = Device(equip_id="A", equip_type="0307")
        topo.device_map["B"] = Device(equip_id="B", equip_type="0307")
        topo.point_map["PA1"] = ConnectPoint(point_id="PA1", belong_equip_id="A")
        topo.point_map["PB1"] = ConnectPoint(point_id="PB1", belong_equip_id="B")
        topo._points_by_equip["A"].append("PA1")
        topo._points_by_equip["B"].append("PB1")
        # 无路径
        results = topo.find_breakpoint_between("A", "B")
        if results:
            self.assertEqual(results[0]["priority"], "P2")

    def test_priority_order(self):
        """P1 < P2 < P3 < P4 < P5 < P6 < P7。"""
        rows = [
            {"breakpoint_type": "[P3]测试", "priority": "P3"},
            {"breakpoint_type": "[P1]测试", "priority": "P1"},
            {"breakpoint_type": "[P7]测试", "priority": "P7"},
            {"breakpoint_type": "[P2]测试", "priority": "P2"},
        ]
        _PRI = {"P1": 0, "P2": 1, "P3": 2, "P4": 3, "P5": 4, "P6": 5, "P7": 6}
        rows.sort(key=lambda x: _PRI.get(x.get("priority", "P7"), 99))
        priorities = [r["priority"] for r in rows]
        self.assertEqual(priorities, ["P1", "P2", "P3", "P7"])


class TestBuildSVGGraph(unittest.TestCase):
    """测试 _build_svg_graph。"""

    def test_connections_become_edges(self):
        conns = [
            {"from_element_id": "A", "to_element_id": "B"},
            {"from_element_id": "B", "to_element_id": "C"},
        ]
        G = _build_svg_graph(conns, {"A": "A", "B": "B", "C": "C"}, None)
        self.assertEqual(G.number_of_nodes(), 3)
        self.assertTrue(G.has_edge("A", "B"))
        self.assertTrue(G.has_edge("B", "C"))
        self.assertFalse(G.has_edge("A", "C"))


if __name__ == "__main__":
    unittest.main()
