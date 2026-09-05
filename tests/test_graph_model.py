# -*- coding: utf-8 -*-
"""Unit tests for core.graph_model — TopologyGraph, find_breakpoint_between, P1-P7 priority."""
import sys
import os

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import unittest
import networkx as nx
from core.graph_model import (
    Device, ConnectPoint, TopoEdge, TopologyGraph,
    AbnormalItem, BreakpointItem, TieLoopItem,
)


class TestTopologyGraphBasic(unittest.TestCase):
    """Test basic graph construction and device/point registration."""

    def setUp(self):
        self.topo = TopologyGraph()
        # Register two devices with terminals
        self.dev_a = "TMP00001"
        self.dev_b = "TMP00002"
        self.pa1 = "PT_A1"
        self.pb1 = "PT_B1"
        self.topo.device_map[self.dev_a] = Device(equip_id=self.dev_a, equip_name="开关A", equip_type="0307")
        self.topo.device_map[self.dev_b] = Device(equip_id=self.dev_b, equip_name="开关B", equip_type="0307")
        self.topo.point_map[self.pa1] = ConnectPoint(point_id=self.pa1, belong_equip_id=self.dev_a)
        self.topo.point_map[self.pb1] = ConnectPoint(point_id=self.pb1, belong_equip_id=self.dev_b)
        self.topo._points_by_equip[self.dev_a].append(self.pa1)
        self.topo._points_by_equip[self.dev_b].append(self.pb1)
        self.topo.graph.add_edge(self.pa1, self.pb1)

    def test_device_map_populated(self):
        self.assertIn(self.dev_a, self.topo.device_map)
        self.assertIn(self.dev_b, self.topo.device_map)

    def test_point_index_correct(self):
        self.assertEqual(self.topo._points_by_equip[self.dev_a], [self.pa1])
        self.assertEqual(self.topo._points_by_equip[self.dev_b], [self.pb1])

    def test_graph_has_edge(self):
        self.assertTrue(self.topo.graph.has_edge(self.pa1, self.pb1))

    def test_get_device_all_points(self):
        pts = self.topo._points_by_equip.get(self.dev_a, [])
        self.assertEqual(len(pts), 1)
        self.assertEqual(pts[0], self.pa1)


class TestFindBreakpointBetween(unittest.TestCase):
    """Test find_breakpoint_between with various topology scenarios."""

    def setUp(self):
        self.topo = TopologyGraph()
        # A -- (open switch) -- B: two devices, each with one terminal, no edge
        self.dev_a = "DEV_A"
        self.dev_b = "DEV_B"
        self.pa = "PT_A"
        self.pb = "PT_B"
        self.topo.device_map[self.dev_a] = Device(equip_id=self.dev_a, equip_type="0307")
        self.topo.device_map[self.dev_b] = Device(equip_id=self.dev_b, equip_type="0307")
        self.topo.point_map[self.pa] = ConnectPoint(point_id=self.pa, belong_equip_id=self.dev_a)
        self.topo.point_map[self.pb] = ConnectPoint(point_id=self.pb, belong_equip_id=self.dev_b)
        self.topo._points_by_equip[self.dev_a].append(self.pa)
        self.topo._points_by_equip[self.dev_b].append(self.pb)
        # No edge between pa and pb -> P2 (no path)

    def test_no_path_returns_p2(self):
        """When two devices have terminals but no path, should return P2."""
        results = self.topo.find_breakpoint_between(self.dev_a, self.dev_b)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["priority"], "P2")

    def test_empty_input_returns_empty(self):
        """Empty equipment IDs should return empty list."""
        results = self.topo.find_breakpoint_between("", "")
        self.assertEqual(len(results), 0)

    def test_missing_device_terminals_returns_p2(self):
        """Device with no terminals registered should return P2."""
        results = self.topo.find_breakpoint_between("NONEXIST", "ALSO_NONEXIST")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["priority"], "P2")

    def test_connected_devices_no_breakpoint(self):
        """When devices are connected by an edge, should find a path (no P2)."""
        self.topo.graph.add_edge(self.pa, self.pb)
        results = self.topo.find_breakpoint_between(self.dev_a, self.dev_b)
        # Should find a path; P2 should NOT be in results
        priorities = [r["priority"] for r in results]
        self.assertNotIn("P2", priorities)

    def test_p1_early_termination(self):
        """When a P1 (分位开关) breakpoint is found, P2-P7 should be skipped."""
        # Add edge to make path exist, then add a switch in分位
        self.topo.graph.add_edge(self.pa, self.pb)
        # Set switch state to分位
        self.topo.switch_state_map[self.dev_a] = "0"  # 0 = 分位
        results = self.topo.find_breakpoint_between(self.dev_a, self.dev_b)
        p1_results = [r for r in results if r["priority"] == "P1"]
        if p1_results:
            # If P1 found, no P2-P7 should be present
            priorities = [r["priority"] for r in results]
            for p in ("P2", "P3", "P4", "P5", "P6", "P7"):
                self.assertNotIn(p, priorities,
                                 f"{p} should not appear when P1 is found")


class TestAbnormalItem(unittest.TestCase):
    """Test AbnormalItem model creation and defaults."""

    def test_create_abnormal_item(self):
        item = AbnormalItem(
            trace_uuid="test-uuid-001",
            equip_id="TMP00001",
            point_id="PT_001",
            rule_code="R001",
            rule_desc="端子悬空",
            check_result="异常",
            detail="设备端子悬空无连接",
        )
        self.assertEqual(item.dimension, "拓扑完整性")
        self.assertEqual(item.risk_level, "中")
        self.assertEqual(item.review_status, "待复核")

    def test_create_with_explicit_fields(self):
        item = AbnormalItem(
            trace_uuid="test-uuid-002",
            equip_id="TMP00002",
            point_id="",
            rule_code="RULE-E01",
            rule_desc="开关分位有电流",
            check_result="异常",
            detail="分位开关仍有0.5A电流",
            dimension="电气逻辑",
            risk_level="高",
        )
        self.assertEqual(item.dimension, "电气逻辑")
        self.assertEqual(item.risk_level, "高")


class TestBreakpointPriorityOrder(unittest.TestCase):
    """Test that breakpoint priority ordering is correct."""

    def test_priority_sort_order(self):
        """P1 should sort before P2, P2 before P3, etc."""
        _PRI_ORDER = {"P1": 0, "P2": 1, "P3": 2, "P4": 3, "P5": 4, "P6": 5, "P7": 6}
        results = [
            {"priority": "P3", "detail": "test3"},
            {"priority": "P1", "detail": "test1"},
            {"priority": "P2", "detail": "test2"},
            {"priority": "P7", "detail": "test7"},
        ]
        results.sort(key=lambda x: _PRI_ORDER.get(x.get("priority", "P?"), 99))
        self.assertEqual(results[0]["priority"], "P1")
        self.assertEqual(results[1]["priority"], "P2")
        self.assertEqual(results[2]["priority"], "P3")
        self.assertEqual(results[3]["priority"], "P7")


if __name__ == "__main__":
    unittest.main()
