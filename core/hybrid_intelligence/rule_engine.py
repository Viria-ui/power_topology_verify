"""
规则引擎模块 (Rule Engine)
=========================

确定性拓扑规则 + 电气逻辑规则的执行器。

作为"兜底"层：当 GNN / 时空模型无法确定时（置信度不足），
或作为独立验证层（高置信度时直接采用规则结果），确保零漏判。

规则分类：
├── 拓扑规则（确定性，零漏判）
│   ├── R001: 悬空端子 → 设备端子数≠2（开关类）→ 断点
│   ├── R002: 孤岛无源 → 连通分量无电源 → 异常
│   ├── R003: 同馈线跨分量 → 同一馈线设备分布在≥2个连通分量 → 断点
│   ├── R004: 联络开关疑似 → 跨馈线开关（ssjg容器内排除）→ 联络候选
│   ├── R005: 非计划合环 → 联络开关合位但两侧非同源电源 → 合环风险
│   └── R006: 物理断开逻辑误连通 → 拓扑图有边但SVG无连接 → 虚假拓扑
│
├── 电气规则（E01-E07，来自 telemetry_evaluator.py）
│   ├── E01: 分位开关有电流 → 开关OPEN但IA/IB/IC>1A → 异常
│   ├── E02: 合位开关无功率 → 开关CLOSE但AP≈0且UA>0 → 疑似虚接
│   ├── E03: 合位开关无电压 → 开关CLOSE但UA=UB=UC=0 → 端子断线
│   ├── E04: 三相电流不平衡 → max(|Ia|,|Ib|,|Ic|)/avg>30% → 不平衡告警
│   ├── E05: 功率失配 → |AP| > U×I×√3×1.1 → 计量异常
│   ├── E06: 分位开关有功率 → 开关OPEN但|AP|>1kW → 拓扑异常
│   └── E07: 小电流大功率 → I<1A但|AP|>10kW → 计量/拓扑异常
│
└── 图模一致性规则
    ├── G001: SVG有设备但数据库无
    ├── G002: 数据库有设备但SVG无
    ├── G003: SVG有连接但拓扑图不连通
    └── G004: 电压等级不一致
"""

from __future__ import annotations
import logging
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

import numpy as np
import networkx as nx

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# 规则命中结果
# ------------------------------------------------------------------

@dataclass
class RuleHit:
    """单条规则命中结果"""
    rule_id: str            # 规则编号，如 "R001", "E01", "G001"
    equip_id: str
    rule_desc: str         # 规则描述
    detail: str            # 详细说明
    severity: str          # 高/中/低
    confidence: float       # 置信度 [0, 1]，确定性规则=1.0
    is_deterministic: bool  # 是否确定性（规则=1.0，GNN/时空=可学习）
    suggestion: str         # 整改建议
    sql_draft: str = ""    # 修复 SQL（可选）
    anomaly_type: str = ""  # 映射到统一异常类型

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "equip_id": self.equip_id,
            "rule_desc": self.rule_desc,
            "detail": self.detail,
            "severity": self.severity,
            "confidence": round(self.confidence, 4),
            "is_deterministic": self.is_deterministic,
            "suggestion": self.suggestion,
            "sql_draft": self.sql_draft,
            "anomaly_type": self.anomaly_type,
        }


# ------------------------------------------------------------------
# 主规则引擎
# ------------------------------------------------------------------

class HybridRuleEngine:
    """
    混合规则引擎

    融合三类规则（按优先级从高到低）：
      1. 确定性拓扑规则（置信度=1.0）→ 零漏判，直接采用
      2. 确定性电气规则（置信度=1.0）→ 基于遥测的物理定律
      3. 图模一致性规则（置信度=0.9）→ SVG vs 数据库一致性

    参数:
        topo: TopologyGraph
        telemetry_data: {equip_id: [row, ...]}
        svg_document: SvgDocument（可选）
        switch_status_map: {equip_id: "CLOSE"/"OPEN"}
    """

    def __init__(
        self,
        topo,                        # TopologyGraph
        telemetry_data: Optional[dict] = None,
        svg_document=None,            # SvgDocument（可选）
        switch_status_map: Optional[dict] = None,
    ):
        self.topo = topo
        self.telemetry_data = telemetry_data or {}
        self.svg_doc = svg_document
        self.switch_status_map = switch_status_map or {}
        self._rule_hits: List[RuleHit] = []

    # ==================================================================
    # 公共接口
    # ==================================================================

    def run_all_rules(self) -> List[RuleHit]:
        """
        执行全部规则，返回所有命中结果

        返回: List[RuleHit]
        """
        self._rule_hits = []

        logger.info("[规则引擎] 开始执行全部规则...")

        # 1. 拓扑规则
        self._check_r001_hanging_terminal()
        self._check_r002_island_no_source()
        self._check_r003_feed_breakpoint()
        self._check_r004_tie_switch()
        self._check_r005_unplanned_loop()
        self._check_r006_false_topo_edge()

        # 2. 电气规则
        self._check_e01_open_with_current()
        self._check_e02_close_no_power()
        self._check_e03_close_no_voltage()
        self._check_e04_current_imbalance()
        self._check_e05_power_mismatch()
        self._check_e06_open_with_power()
        self._check_e07_small_current_large_power()

        # 3. 图模一致性规则
        if self.svg_doc is not None:
            self._check_g001_svg_not_in_db()
            self._check_g002_db_not_in_svg()
            self._check_g003_connection_mismatch()
            self._check_g004_voltage_mismatch()

        logger.info(
            "[规则引擎] 执行完成: %d 条规则命中（高=%d, 中=%d, 低=%d）",
            len(self._rule_hits),
            sum(1 for h in self._rule_hits if h.severity == "高"),
            sum(1 for h in self._rule_hits if h.severity == "中"),
            sum(1 for h in self._rule_hits if h.severity == "低"),
        )
        return self._rule_hits

    def get_hits_for_equip(self, equip_id: str) -> List[RuleHit]:
        """获取指定设备的所有规则命中"""
        return [h for h in self._rule_hits if h.equip_id == equip_id]

    def get_high_confidence_hits(self, threshold: float = 0.9) -> List[RuleHit]:
        """获取高置信度规则命中（确定性规则）"""
        return [h for h in self._rule_hits if h.confidence >= threshold]

    # ==================================================================
    # R001: 悬空端子 — 设备端子数≠2（开关类）
    # ==================================================================

    def _check_r001_hanging_terminal(self):
        """
        规则：开关类设备（NON_TERMINAL_SWITCH_TYPES）必须有2个端子。
              悬空（≠2）→ 断点风险。
        """
        NON_TERMINAL_SWITCH_TYPES = {"1705", "1706", "1707", "0307", "0201", "0202", "0203", "0209"}
        for equip_id, dev in self.topo.device_map.items():
            etype = dev.equip_type or ""
            if etype not in NON_TERMINAL_SWITCH_TYPES:
                continue
            pts = self.topo.get_device_all_points(equip_id)
            n = len(pts)
            if n == 2:
                continue   # 正常
            self._rule_hits.append(RuleHit(
                rule_id="R001",
                equip_id=equip_id,
                rule_desc="开关类设备端子数异常",
                detail=(
                    f"设备 {equip_id}（类型={etype}）有 {n} 个端子，"
                    f"{'过多' if n > 2 else '不足'}，应为2个端子。"
                    f"这会导致拓扑连接不完整。"
                ),
                severity="高" if n == 0 else "中",
                confidence=1.0,
                is_deterministic=True,
                suggestion="补录缺失端子或删除多余端子，确保每台开关正好2个端子",
                sql_draft=(
                    f"-- R001: {equip_id} 补录缺失端子\n"
                    f"INSERT INTO EQUIP_JBS_PWTERMINAL (TERMINAL_ID,BELONG_EQUIP_ID,FEEDER_ID)"
                    f" VALUES ('PT_{equip_id}_1','{equip_id}','{dev.feeder_id or ''}');"
                ),
                anomaly_type="图模一致性异常",
            ))

    # ==================================================================
    # R002: 孤岛无源 — 连通分量无电源
    # ==================================================================

    def _check_r002_island_no_source(self):
        """规则：每个连通分量必须包含至少一个电源设备。无源分量→拓扑异常"""
        G = self.topo.graph
        if G.number_of_nodes() == 0:
            return

        source_ids = {e.equip_id for e in self.topo.device_map.values() if e.is_source}
        if not source_ids:
            return

        # 只在设备节点上计算连通分量
        device_nodes = set(self.topo.device_map.keys())
        subG = G.subgraph(device_nodes).copy()

        for comp in nx.connected_components(subG):
            comp = set(comp)
            if any(eid in source_ids for eid in comp):
                continue  # 有电源，正常
            # 无电源连通分量
            equip_list = list(comp)[:5]
            self._rule_hits.append(RuleHit(
                rule_id="R002",
                equip_id=",".join(equip_list) + ("..." if len(comp) > 5 else ""),
                rule_desc="孤岛无源",
                detail=(
                    f"连通分量含 {len(comp)} 台设备，无电源接入。"
                    f"设备列表: {', '.join(equip_list)}"
                ),
                severity="高",
                confidence=1.0,
                is_deterministic=True,
                suggestion="检查该区域是否遗漏电源接入点，或拓扑图中缺少上级电源设备",
                anomaly_type="电气逻辑异常",
            ))

    # ==================================================================
    # R003: 同馈线跨分量 — 同一馈线设备分布在≥2个连通分量
    # ==================================================================

    def _check_r003_feed_breakpoint(self):
        """规则：同一馈线设备必须全部在同一个连通分量中，否则存在断点"""
        G = self.topo.graph
        if G.number_of_nodes() == 0:
            return

        device_nodes = set(self.topo.device_map.keys())
        subG = G.subgraph(device_nodes).copy()
        comp_of_node = {}
        for i, comp in enumerate(nx.connected_components(subG)):
            for n in comp:
                comp_of_node[n] = i

        # 按馈线分组
        feeder_to_comps: dict = defaultdict(set)
        for equip_id, dev in self.topo.device_map.items():
            fid = dev.feeder_id
            if not fid or equip_id not in comp_of_node:
                continue
            feeder_to_comps[fid].add(comp_of_node[equip_id])

        for fid, comps in feeder_to_comps.items():
            if len(comps) >= 2:
                # 同馈线跨多个连通分量 → 断点
                equip_ids = [
                    eid for eid, dev in self.topo.device_map.items()
                    if dev.feeder_id == fid
                ][:3]
                self._rule_hits.append(RuleHit(
                    rule_id="R003",
                    equip_id="; ".join(equip_ids),
                    rule_desc="同馈线跨连通分量",
                    detail=(
                        f"馈线 {fid} 的设备分布在 {len(comps)} 个不同连通分量，"
                        f"表明存在未建模的拓扑连接（断点）。"
                    ),
                    severity="高",
                    confidence=1.0,
                    is_deterministic=True,
                    suggestion=f"在馈线 {fid} 的断点处补录 PWFEEDERLINE 和 PWTERMINAL 记录",
                    sql_draft=(
                        f"-- R003: 馈线 {fid} 同馈线跨分量，核查断点处 PWFEEDERLINE"
                    ),
                    anomaly_type="图模一致性异常",
                ))

    # ==================================================================
    # R004: 疑似联络开关 — 跨馈线开关（ssjg容器内排除）
    # ==================================================================

    def _check_r004_tie_switch(self):
        """规则：跨馈线连接的开关设备为联络开关候选（ssjg容器内排除）"""
        from core.constants import STATION_CONTAINER_TYPES, NON_TERMINAL_SWITCH_TYPES

        G = self.topo.graph
        # 按馈线记录每台设备
        feeder_of_dev: dict = {}
        for equip_id, dev in self.topo.device_map.items():
            feeder_of_dev[equip_id] = dev.feeder_id

        for equip_id, dev in self.topo.device_map.items():
            etype = dev.equip_type or ""
            if etype not in NON_TERMINAL_SWITCH_TYPES:
                continue
            # ssjg 容器排除
            ssjg = getattr(dev, "ssjg", None)
            if ssjg and ssjg in STATION_CONTAINER_TYPES:
                continue
            # 邻居馈线
            neighbors = list(G.neighbors(equip_id))
            neighbor_feeders = {
                feeder_of_dev.get(nb, "")
                for nb in neighbors
                if nb in feeder_of_dev and nb != equip_id
            }
            if len(neighbor_feeders) >= 2:
                self._rule_hits.append(RuleHit(
                    rule_id="R004",
                    equip_id=equip_id,
                    rule_desc="疑似联络开关",
                    detail=(
                        f"开关 {equip_id} 跨 {len(neighbor_feeders)} 个馈线连接: "
                        f"{neighbor_feeders}，可能为联络开关。"
                    ),
                    severity="中",
                    confidence=0.85,
                    is_deterministic=True,
                    suggestion="核对是否应为合环运行方式，或分位作联络备用",
                    anomaly_type="疑似联络开关",
                ))

    # ==================================================================
    # R005: 非计划合环 — 联络开关合位但两侧非同源电源
    # ==================================================================

    def _check_r005_unplanned_loop(self):
        """规则：联络开关合位（两侧非同源电源）→ 非计划合环风险"""
        G = self.topo.graph
        source_ids = {e.equip_id for e in self.topo.device_map.values() if e.is_source}

        for equip_id, dev in self.topo.device_map.items():
            etype = dev.equip_type or ""
            status = self.switch_status_map.get(equip_id, dev.switch_status or "")
            if status not in {"CLOSE", "合位", "1"}:
                continue

            neighbors = list(G.neighbors(equip_id))
            neighbor_sources = {nb in source_ids for nb in neighbors}
            if any(neighbor_sources) and not all(neighbor_sources):
                # 部分邻居有电源，部分无 → 合环风险
                self._rule_hits.append(RuleHit(
                    rule_id="R005",
                    equip_id=equip_id,
                    rule_desc="非计划合环风险",
                    detail=(
                        f"开关 {equip_id} 处于合位，但仅部分相邻设备有电源，"
                        f"可能存在非计划合环。"
                    ),
                    severity="高",
                    confidence=1.0,
                    is_deterministic=True,
                    suggestion="核查该开关两侧是否同源，合环运行需经调度批准",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # R006: 物理断开逻辑误连通 — 拓扑图有边但SVG无连接
    # ==================================================================

    def _check_r006_false_topo_edge(self):
        """规则：拓扑图有边但 SVG 无连接 → 虚假拓扑边"""
        if self.svg_doc is None:
            return

        # SVG 连接对集合
        svg_pairs: set = set()
        for conn in self.svg_doc.connections:
            s, e = conn.start_device_id, conn.end_device_id
            if s and e and s != e:
                svg_pairs.add(tuple(sorted([s, e])))

        # 拓扑设备-设备对
        pt2dev = {pid: pt.belong_equip_id
                  for pid, pt in self.topo.point_map.items()}
        device_ids = set(self.topo.device_map.keys())
        topo_pairs: set = set()

        for u, v in self.topo.graph.edges():
            a = pt2dev.get(u, u if u in device_ids else None)
            b = pt2dev.get(v, v if v in device_ids else None)
            if a and b and a != b and a in device_ids and b in device_ids:
                topo_pairs.add(tuple(sorted([a, b])))

        false_edges = topo_pairs - svg_pairs
        for a, b in false_edges:
            edge_data = self.topo.graph.get_edge_data(a, b) or {}
            edge_info = edge_data.get("edge_info") or edge_data.get("edge") or {}
            line_id = (edge_info.get("line_id", "") if isinstance(edge_info, dict) else "") or ""
            if line_id.startswith("INT_"):
                continue  # 内部边不计入
            if a not in self.topo.device_map or b not in self.topo.device_map:
                continue
            self._rule_hits.append(RuleHit(
                rule_id="R006",
                equip_id=f"{a}↔{b}",
                rule_desc="物理断开逻辑误连通",
                detail=(
                    f"拓扑图中 {a} ↔ {b} 存在边（line_id={line_id or 'UNKNOWN'}），"
                    f"但 SVG 图中无对应物理连接。"
                ),
                severity="高",
                confidence=1.0,
                is_deterministic=True,
                suggestion="核实 {a}↔{b} 是否真实连接；若图纸正确则在模型中断开该虚假链路",
                sql_draft=(
                    f"DELETE FROM EQUIP_JBS_PWFEEDERLINE WHERE LINE_ID='{line_id}';"
                    if line_id else f"-- 人工核查 {a}↔{b} 后删除"
                ),
                anomaly_type="图模一致性异常",
            ))

    # ==================================================================
    # E01: 分位开关有电流
    # ==================================================================

    def _check_e01_open_with_current(self):
        """规则：开关分位(OPEN)时，三相电流应≈0（>1A为异常）"""
        for equip_id, rows in self.telemetry_data.items():
            status = self.switch_status_map.get(equip_id, "")
            if status not in {"OPEN", "分位", "0"}:
                continue
            latest = rows[-1] if isinstance(rows, list) else rows
            ia = abs(self._safe_float(latest.get("IA", 0)))
            ib = abs(self._safe_float(latest.get("IB", 0)))
            ic = abs(self._safe_float(latest.get("IC", 0)))
            imax = max(ia, ib, ic)
            if imax > 1.0:  # A
                self._rule_hits.append(RuleHit(
                    rule_id="E01",
                    equip_id=equip_id,
                    rule_desc="分位开关有电流",
                    detail=(
                        f"开关 {equip_id} 处于分位，但测得电流 IA={ia:.2f}A, "
                        f"IB={ib:.2f}A, IC={ic:.2f}A（最大={imax:.2f}A>1A）"
                    ),
                    severity="高",
                    confidence=1.0,
                    is_deterministic=True,
                    suggestion="检查开关实际状态与遥信是否一致，或是否存在违规旁路",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # E02: 合位开关无功率
    # ==================================================================

    def _check_e02_close_no_power(self):
        """规则：开关合位(CLOSE)时，若有电压但功率≈0 → 疑似虚接"""
        for equip_id, rows in self.telemetry_data.items():
            status = self.switch_status_map.get(equip_id, "")
            if status not in {"CLOSE", "合位", "1"}:
                continue
            latest = rows[-1] if isinstance(rows, list) else rows
            ap = abs(self._safe_float(latest.get("AP", 0)))
            ua = self._safe_float(latest.get("UA", 0))
            if ap < 0.1 and ua > 100.0:  # 无功率但有电压
                self._rule_hits.append(RuleHit(
                    rule_id="E02",
                    equip_id=equip_id,
                    rule_desc="合位开关无功率",
                    detail=(
                        f"开关 {equip_id} 处于合位且有电压(UA={ua:.1f}V)，"
                        f"但有功功率接近零(AP={ap:.3f}kW)，疑似虚接或端子未连接。"
                    ),
                    severity="中",
                    confidence=0.95,
                    is_deterministic=True,
                    suggestion="现场核查开关端子连接情况",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # E03: 合位开关无电压
    # ==================================================================

    def _check_e03_close_no_voltage(self):
        """规则：开关合位(CLOSE)时，三相电压应>0；全零 → 端子断线"""
        for equip_id, rows in self.telemetry_data.items():
            status = self.switch_status_map.get(equip_id, "")
            if status not in {"CLOSE", "合位", "1"}:
                continue
            latest = rows[-1] if isinstance(rows, list) else rows
            ua = self._safe_float(latest.get("UA", 0))
            ub = self._safe_float(latest.get("UB", 0))
            uc = self._safe_float(latest.get("UC", 0))
            if ua < 1.0 and ub < 1.0 and uc < 1.0:
                self._rule_hits.append(RuleHit(
                    rule_id="E03",
                    equip_id=equip_id,
                    rule_desc="合位开关无电压",
                    detail=(
                        f"开关 {equip_id} 处于合位但三相电压均为零(UA={ua:.1f}V)，"
                        f"疑似上游断线或端子未接入。"
                    ),
                    severity="高",
                    confidence=1.0,
                    is_deterministic=True,
                    suggestion="检查该开关上游电源和端子连接",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # E04: 三相电流不平衡
    # ==================================================================

    def _check_e04_current_imbalance(self):
        """规则：三相电流不平衡度 > 30% → 告警"""
        for equip_id, rows in self.telemetry_data.items():
            latest = rows[-1] if isinstance(rows, list) else rows
            ia = abs(self._safe_float(latest.get("IA", 0)))
            ib = abs(self._safe_float(latest.get("IB", 0)))
            ic = abs(self._safe_float(latest.get("IC", 0)))
            imax = max(ia, ib, ic)
            i_mean = (ia + ib + ic) / 3.0
            if i_mean < 1.0:
                continue
            imbalance = imax / i_mean
            if imbalance > 1.3:
                self._rule_hits.append(RuleHit(
                    rule_id="E04",
                    equip_id=equip_id,
                    rule_desc="三相电流严重不平衡",
                    detail=(
                        f"设备 {equip_id} 三相电流 IA={ia:.2f}A, IB={ib:.2f}A, "
                        f"IC={ic:.2f}A，不平衡度={imbalance:.2f}（>1.30）"
                    ),
                    severity="中",
                    confidence=0.90,
                    is_deterministic=True,
                    suggestion="检查三相负荷分配或电流互感器接线",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # E05: 功率失配
    # ==================================================================

    def _check_e05_power_mismatch(self):
        """规则：|AP| > U×I×√3×1.1 → 计量异常（允许10%误差）"""
        for equip_id, rows in self.telemetry_data.items():
            latest = rows[-1] if isinstance(rows, list) else rows
            ap = abs(self._safe_float(latest.get("AP", 0)))
            ua = self._safe_float(latest.get("UA", 0))
            ia = abs(self._safe_float(latest.get("IA", 0)))
            if ua < 100.0 or ia < 0.1 or ap < 1.0:
                continue
            ap_theory = ua * ia * 1.732 / 1000.0  # kW
            if ap > ap_theory * 1.1:
                self._rule_hits.append(RuleHit(
                    rule_id="E05",
                    equip_id=equip_id,
                    rule_desc="功率严重失配",
                    detail=(
                        f"设备 {equip_id} 实测AP={ap:.1f}kW，但按 UA={ua:.0f}V, "
                        f"IA={ia:.1f}A 计算理论值={ap_theory:.1f}kW，偏差>{((ap/ap_theory)-1)*100:.0f}%"
                    ),
                    severity="高",
                    confidence=0.95,
                    is_deterministic=True,
                    suggestion="检查功率计量装置和电流互感器变比",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # E06: 分位开关有功率
    # ==================================================================

    def _check_e06_open_with_power(self):
        """规则：开关分位(OPEN)但有功功率>1kW → 拓扑异常（排除电容）"""
        CAPACITOR_TYPES = {"2101", "2102", "2103"}
        for equip_id, rows in self.telemetry_data.items():
            status = self.switch_status_map.get(equip_id, "")
            if status not in {"OPEN", "分位", "0"}:
                continue
            latest = rows[-1] if isinstance(rows, list) else rows
            ap = abs(self._safe_float(latest.get("AP", 0)))
            dev = self.topo.device_map.get(equip_id)
            etype = dev.equip_type if dev else ""
            if etype in CAPACITOR_TYPES:
                continue
            if ap > 1.0:  # kW
                self._rule_hits.append(RuleHit(
                    rule_id="E06",
                    equip_id=equip_id,
                    rule_desc="分位开关有功率",
                    detail=(
                        f"开关 {equip_id} 处于分位但有功功率={ap:.1f}kW(>1kW)，"
                        f"拓扑连接与开关状态矛盾。"
                    ),
                    severity="高",
                    confidence=1.0,
                    is_deterministic=True,
                    suggestion="检查开关实际状态与拓扑模型是否一致",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # E07: 小电流大功率
    # ==================================================================

    def _check_e07_small_current_large_power(self):
        """规则：电流<1A但功率>10kW → 计量/拓扑异常"""
        for equip_id, rows in self.telemetry_data.items():
            latest = rows[-1] if isinstance(rows, list) else rows
            ia = abs(self._safe_float(latest.get("IA", 0)))
            ap = abs(self._safe_float(latest.get("AP", 0)))
            if ia < 1.0 and ap > 10.0:
                self._rule_hits.append(RuleHit(
                    rule_id="E07",
                    equip_id=equip_id,
                    rule_desc="小电流大功率",
                    detail=(
                        f"设备 {equip_id} 电流={ia:.2f}A(<1A)但有功功率={ap:.1f}kW(>10kW)，"
                        f"数据矛盾，疑似计量故障或拓扑错误。"
                    ),
                    severity="高",
                    confidence=1.0,
                    is_deterministic=True,
                    suggestion="检查电流互感器接线和功率计量装置",
                    anomaly_type="电气逻辑异常",
                ))

    # ==================================================================
    # G001-G004: 图模一致性
    # ==================================================================

    def _check_g001_svg_not_in_db(self):
        """SVG 有设备但数据库无"""
        if self.svg_doc is None:
            return
        db_ids = set(self.topo.device_map.keys())
        for elem in self.svg_doc.elements:
            eid = elem.element_id
            if eid and eid not in db_ids:
                self._rule_hits.append(RuleHit(
                    rule_id="G001",
                    equip_id=eid,
                    rule_desc="SVG有设备但数据库无",
                    detail=f"SVG图元 {eid}（{elem.layer_name}）在数据库中不存在",
                    severity="中",
                    confidence=0.90,
                    is_deterministic=True,
                    suggestion=f"在 EQUIP_JBS_PWEQUIPINFO 中补录 {eid} 的设备信息",
                    sql_draft=(
                        f"-- G001: 补录 {eid} 设备\n"
                        f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME, EQUIP_TYPE, VOLTAGE_TYPE)"
                        f" VALUES ('{eid}', 'SVG新增', '1705', '1010');"
                    ),
                    anomaly_type="图模一致性异常",
                ))

    def _check_g002_db_not_in_svg(self):
        """数据库有设备但SVG无"""
        if self.svg_doc is None:
            return
        svg_ids = {e.element_id for e in self.svg_doc.elements if e.element_id}
        for equip_id in self.topo.device_map:
            if equip_id not in svg_ids:
                self._rule_hits.append(RuleHit(
                    rule_id="G002",
                    equip_id=equip_id,
                    rule_desc="数据库有设备但SVG无",
                    detail=f"数据库设备 {equip_id} 在 SVG 图中无对应图元",
                    severity="中",
                    confidence=0.90,
                    is_deterministic=True,
                    suggestion=f"在 SVG 图中补画 {equip_id} 的设备图元",
                    anomaly_type="图模一致性异常",
                ))

    def _check_g003_connection_mismatch(self):
        """SVG有连接但拓扑图不连通"""
        if self.svg_doc is None:
            return
        G = self.topo.graph
        for conn in self.svg_doc.connections:
            s, e = conn.start_device_id, conn.end_device_id
            if not s or not e:
                continue
            if s not in G.nodes or e not in G.nodes:
                self._rule_hits.append(RuleHit(
                    rule_id="G003",
                    equip_id=f"{s}↔{e}",
                    rule_desc="SVG有连接但拓扑图不连通",
                    detail=f"SVG存在 {s}-{e} 连线，但拓扑图中 {s} 或 {e} 节点缺失",
                    severity="高",
                    confidence=0.95,
                    is_deterministic=True,
                    suggestion=f"在拓扑图中补录 {s}/{e} 的端子及连接关系",
                    anomaly_type="图模一致性异常",
                ))

    def _check_g004_voltage_mismatch(self):
        """SVG 与数据库电压等级不一致"""
        if self.svg_doc is None:
            return
        svg_elem_map = {e.element_id: e for e in self.svg_doc.elements}
        for equip_id, dev in self.topo.device_map.items():
            svg_elem = svg_elem_map.get(equip_id)
            if svg_elem is None:
                continue
            svg_vol = str(svg_elem.voltage_level or "").strip().lower()
            db_vol = str(dev.voltage_type or "").strip().lower()
            # 归一化
            svg_vol = "1010" if svg_vol in {"10kv", "10k", "1010"} else svg_vol.replace("kv", "")
            db_vol = "1010" if db_vol in {"10kv", "10k", "1010"} else db_vol.replace("kv", "")
            if svg_vol and db_vol and svg_vol != db_vol:
                self._rule_hits.append(RuleHit(
                    rule_id="G004",
                    equip_id=equip_id,
                    rule_desc="电压等级不一致",
                    detail=f"设备 {equip_id} SVG电压={svg_elem.voltage_level}，数据库={dev.voltage_type}",
                    severity="低",
                    confidence=0.95,
                    is_deterministic=True,
                    suggestion="以 SVG 图纸电压等级为准，更新数据库",
                    sql_draft=f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='{svg_vol}' WHERE EQUIP_ID='{equip_id}';",
                    anomaly_type="图模一致性异常",
                ))

    # ==================================================================
    # 辅助方法
    # ==================================================================

    @staticmethod
    def _safe_float(v) -> float:
        try:
            return float(v) if v is not None else 0.0
        except (TypeError, ValueError):
            return 0.0
