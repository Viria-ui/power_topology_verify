# -*- coding: utf-8 -*-
"""馈线拓扑扩展分析：断点定位(P1-P7)、联络开关、合环识别。

对外暴露的 Sheet 导出函数：
  build_feeder_analysis()  → dict  (compare.py 调用，返回 5 个 analysis 分片)

修复说明（9月5日）：
  1. Sheet3 联络开关：改用全库设备图遍历，而非 SVG 局部图。
     根因：SVG 仅含单条馈线设备，永远找不到跨馈线联络开关。
  2. Sheet2 断点：调用 TopologyGraph.find_breakpoint_between() 引擎，
     输出 P1-P7 优先级分类（P1 分位开关 → P7 电源失压）。
"""
from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import TYPE_CHECKING

import networkx as nx

from core.graph_model import TopologyGraph
from core.constants import (
    TERMINAL_EXEMPT_TYPES, NON_TERMINAL_SWITCH_TYPES, SWITCH_TYPES,
    TIE_EXCLUDE_NAME_KEYS,
)
from core.log_config import get_logger

if TYPE_CHECKING:
    import pandas as pd

logger = get_logger(__name__)

# ------------------------------------------------------------------
#  P1-P7 优先级排序
# ------------------------------------------------------------------
_PRIORITY_ORDER = {"P1": 0, "P2": 1, "P3": 2, "P4": 3, "P5": 4, "P6": 5, "P7": 6}
_PRIORITY_RE = re.compile(r"\[(P[1-7])\]")


# ------------------------------------------------------------------
#  设备级图辅助
# ------------------------------------------------------------------
def build_device_graph(
    dist_topo: TopologyGraph,
    table_data: dict | None = None,
) -> nx.Graph:
    """将 TopologyGraph 折叠为设备级无向图（用于联络/合环分析）。"""
    G = nx.Graph()
    for did, dev in dist_topo.device_map.items():
        G.add_node(did, **dev.model_dump())

    pt2dev = {pt_id: pt.belong_equip_id for pt_id, pt in dist_topo.point_map.items()}
    device_ids = set(dist_topo.device_map.keys())

    for edge in dist_topo.edge_map.values():
        sp, ep = edge.start_point, edge.end_point
        if not ep:
            continue
        a = pt2dev.get(sp, sp if sp in device_ids else None)
        b = pt2dev.get(ep, ep if ep in device_ids else None)
        if not a or not b or a == b:
            if sp.startswith("PT_") and sp[3:] in device_ids:
                a = sp[3:]
            if ep and ep.startswith("PT_") and ep[3:] in device_ids:
                b = ep[3:]
            if not a or not b or a == b:
                continue
        G.add_edge(a, b)

    if G.number_of_edges() == 0 and table_data:
        term_df = table_data.get("terminal")
        if term_df is not None and len(term_df) > 0:
            node2devs: dict = {}
            for _, row in term_df.iterrows():
                eid = str(row.get("EQUIP_ID") or "").strip()
                cid = str(row.get("CONNECTIVITYNODE_ID") or "").strip()
                if eid in device_ids and cid:
                    node2devs.setdefault(cid, set()).add(eid)
            for devs in node2devs.values():
                dev_list = list(devs)
                for i in range(len(dev_list)):
                    for j in range(i + 1, len(dev_list)):
                        a, b = dev_list[i], dev_list[j]
                        if a != b:
                            G.add_edge(a, b)
    return G


def _feeder_subgraph(device_graph: nx.Graph, feeder_id: str) -> nx.Graph:
    fid = str(feeder_id)
    nodes = [
        n for n, d in device_graph.nodes(data=True)
        if str(d.get("feeder_id") or "") == fid
    ]
    return device_graph.subgraph(nodes).copy()


def _build_svg_graph(
    svg_connections: list,
    element_to_object_map: dict,
    feeder_device_ids: set | None = None,
) -> nx.Graph:
    G = nx.Graph()
    for conn in svg_connections:
        if not isinstance(conn, dict):
            continue
        a = element_to_object_map.get(str(conn.get("from_element_id") or "").strip())
        b = element_to_object_map.get(str(conn.get("to_element_id") or "").strip())
        if a and b and a != b:
            if feeder_device_ids is None or (a in feeder_device_ids or b in feeder_device_ids):
                G.add_edge(a, b)
                G.add_node(a)
                G.add_node(b)
    return G


def _is_switch_node(device_graph: nx.Graph, node_id: str) -> bool:
    if not device_graph.has_node(node_id):
        return False
    tp = str(device_graph.nodes[node_id].get("equip_type") or "").strip()
    if tp in SWITCH_TYPES or tp in NON_TERMINAL_SWITCH_TYPES:
        return True
    if any(k in tp for k in ("开关", "断路", "熔断", "刀闸", "Fuse", "Breaker", "Switch")):
        return True
    try:
        return int(tp) in (1705, 1706, 1707, 1708, 1709, 111, 115, 307, 201, 202, 203, 302, 309)
    except Exception:
        return False


def _device_name(device_graph: nx.Graph, dev_id: str, fallback: str = "") -> str:
    if device_graph.has_node(dev_id):
        return str(device_graph.nodes[dev_id].get("equip_name") or fallback or dev_id)
    return fallback or dev_id


# ------------------------------------------------------------------
#  Sheet 3：联络开关自动识别（核心修复）
# ------------------------------------------------------------------
def analyze_tie_switches(
    *,
    feeder_id: str,
    line_name: str,
    start_st_id: str,
    device_graph: nx.Graph,
    dist_topo: TopologyGraph,
    line_df,
) -> list[dict]:
    """
    Sheet3 联络开关自动识别：基于全库设备图遍历所有开关，
    判定其邻居是否跨越多条馈线（跨馈线 = 联络）。

    关键修复：不再依赖 SVG 局部图（SVG 只有单条馈线设备，永远找不到联络开关）。
    改用全库 build_device_graph() 构建的设备级无向图。
    """
    fid2name: dict = {}
    fid2station: dict = {}
    if line_df is not None:
        for _, row in line_df.iterrows():
            lid = str(row.get("LINE_ID") or "")
            fid2name[lid] = str(row.get("LINE_NAME") or lid)
            fid2station[lid] = str(row.get("START_ST_ID") or "")

    target = str(feeder_id)
    tie_rows: list = []
    tie_set: set = set()

    def _fid_of(devid: str) -> str:
        if device_graph.has_node(devid):
            return str(device_graph.nodes[devid].get("feeder_id") or "")
        return ""

    def _dev_name(devid: str) -> str:
        if device_graph.has_node(devid):
            return str(device_graph.nodes[devid].get("equip_name") or devid)
        return devid

    for node in device_graph.nodes():
        dev_type = str(device_graph.nodes[node].get("equip_type") or "")
        dev_name = str(device_graph.nodes[node].get("equip_name") or "")

        # R_TIE_EXCLUDE_001：末端设备豁免
        if dev_type in TERMINAL_EXEMPT_TYPES:
            continue
        if any(k in dev_name for k in TIE_EXCLUDE_NAME_KEYS):
            continue

        # 必须是开关类型
        if not _is_switch_node(device_graph, node):
            continue

        # 取邻居节点的馈线 ID 集合；跨越 >= 2 条馈线才可能是联络
        neighbors = list(device_graph.neighbors(node))
        fids = {_fid_of(nb) for nb in neighbors if _fid_of(nb)}
        if len(fids) < 2:
            continue

        my_fids = [f for f in fids if f == target]
        other_fids = [f for f in fids if f != target]
        if not my_fids or not other_fids:
            continue

        for other in other_fids:
            key = (target, other, node)
            if key in tie_set:
                continue
            tie_set.add(key)
            tie_rows.append({
                "线路id": target,
                "线路名称": line_name or fid2name.get(target, target),
                "上级变电站名称": start_st_id or fid2station.get(target, ""),
                "联络开关id": node,
                "联络开关名称": _dev_name(node),
                "是否有联络": "是",
                "联络线路id": other,
                "联络线路名称": fid2name.get(other, other),
                "联络线变电站名称": fid2station.get(other, ""),
            })

    if not tie_rows:
        tie_rows.append({
            "线路id": target,
            "线路名称": line_name or fid2name.get(target, target),
            "上级变电站名称": start_st_id or fid2station.get(target, ""),
            "联络开关id": "",
            "联络开关名称": "",
            "是否有联络": "否",
            "联络线路id": "",
            "联络线路名称": "",
            "联络线变电站名称": "",
        })

    logger.info("Sheet3 联络开关: feeder=%s 识别到 %d 个联络开关", target, len(tie_rows))
    return tie_rows


# ------------------------------------------------------------------
#  Sheet 2：拓扑连通性异常诊断与断点定位（P1-P7 优先级）
# ------------------------------------------------------------------
def analyze_breakpoints(
    *,
    feeder_id: str,
    svg_connections: list,
    element_to_object_map: dict,
    line_db_devices: dict,
    device_graph: nx.Graph,
    defects_report: list,
    dist_topo: TopologyGraph,
) -> list[dict]:
    """
    Sheet2 拓扑连通性异常诊断与断点定位。

    断点按 P1-P7 优先级降序输出（发现即终止，不重复报告）：
      P1: 分位开关（开关分位切断两点间路径）
      P2: 两点间无物理连通路径
      P3: 遥信-遥测矛盾（开关合位但失流/功率不匹配）
      P4: 单端子悬空（degree≤1 且非末端豁免）
      P5: 同馈线分多连通分量
      P6: 虚假连通（有 GLink 但端子图无路径）
      P7: 电源侧失压（E03 合位失压）
    """
    feeder_ids = set(line_db_devices.keys())
    svg_g = _build_svg_graph(svg_connections, element_to_object_map, feeder_ids)
    rows: list = []
    seen: set = set()

    def _append(row: dict) -> None:
        key = (
            row.get("起点设备id"),
            row.get("终点设备id"),
            row.get("本侧疑似断点设备id"),
            row.get("断点类型"),
        )
        if key in seen:
            return
        seen.add(key)
        rows.append(row)

    # -------- 对已知断点设备对调用 P1-P7 引擎（仅查关键对，性能无忧）--------
    brk_count = 0
    seen_brk_pairs: set = set()
    for defect in defects_report:
        if defect.get("defect_type") != "物理连接不一致":
            continue
        equip_key = str(defect.get("equip_id") or "")
        if "<->" not in equip_key:
            continue
        parts = [p.strip() for p in equip_key.split("<->")]
        if len(parts) != 2:
            continue
        a, b = parts
        pair_key = tuple(sorted([a, b]))
        if pair_key in seen_brk_pairs:
            continue
        seen_brk_pairs.add(pair_key)
        brk_list = dist_topo.find_breakpoint_between(a, b)
        for brk in brk_list:
            brk_count += 1
            _append({
                "起点设备id": a,
                "终点设备id": b,
                "断点类型": brk.get("breakpoint_type", "") or "[P2]图形物理连通、拓扑逻辑断开",
                "本侧疑似断点设备id": brk.get("equip_id", a),
                "本侧疑似断点设备名称": _device_name(device_graph, brk.get("equip_id", a)),
                "对侧疑似断点设备id": b,
                "对侧疑似断点设备名称": _device_name(device_graph, b),
                "修正方案": "请根据断点类型[P1-P7]人工核查并修复",
                "修正sql": "-- 待人工确认断点后执行修复 SQL",
            })
    if brk_count:
        logger.debug("P1-P7 引擎产生 %d 条断点候选", brk_count)

    # -------- 图上/模型不一致缺陷补充（P2 类，兜底无 P1-P7 的情况）--------
    for defect in defects_report:
        if defect.get("defect_type") != "物理连接不一致":
            continue
        equip_key = str(defect.get("equip_id") or "")
        if "<->" not in equip_key:
            continue
        parts = [p.strip() for p in equip_key.split("<->")]
        if len(parts) != 2:
            continue
        a, b = parts
        # 已有 P1-P7 结果时跳过（避免重复）
        pair_key = tuple(sorted([a, b]))
        if pair_key in seen_brk_pairs:
            continue
        seen_brk_pairs.add(pair_key)
        _append({
            "起点设备id": a,
            "终点设备id": b,
            "断点类型": "[P2]图形物理连通、拓扑逻辑断开",
            "本侧疑似断点设备id": a,
            "本侧疑似断点设备名称": defect.get("equip_name") or _device_name(device_graph, a),
            "对侧疑似断点设备id": b,
            "对侧疑似断点设备名称": _device_name(device_graph, b),
            "修正方案": defect.get("suggestion", ""),
            "修正sql": defect.get("sql_draft", ""),
        })

    # -------- SVG 孤立节点（P4 类）--------
    for node in svg_g.nodes():
        if svg_g.degree(node) == 0 and node in feeder_ids:
            _append({
                "起点设备id": node,
                "终点设备id": node,
                "断点类型": "[P4]孤立节点",
                "本侧疑似断点设备id": node,
                "本侧疑似断点设备名称": _device_name(device_graph, node),
                "对侧疑似断点设备id": "",
                "对侧疑似断点设备名称": "",
                "修正方案": "SVG 图元未与任何设备建立有效连接，建议补画连接关系",
                "修正sql": "-- SVG 层面补全连接，无需直接修改数据库",
            })

    # -------- 连通分量断裂（P5 类）--------
    components = list(nx.connected_components(svg_g)) if svg_g.number_of_nodes() else []
    if len(components) > 1:
        sorted_comps = sorted(components, key=len, reverse=True)
        main_comp = sorted_comps[0]
        for comp in sorted_comps[1:]:
            a = next(iter(main_comp))
            b = next(iter(comp))
            _append({
                "起点设备id": a,
                "终点设备id": b,
                "断点类型": "[P5]连通分量断裂",
                "本侧疑似断点设备id": a,
                "本侧疑似断点设备名称": _device_name(device_graph, a),
                "对侧疑似断点设备id": b,
                "对侧疑似断点设备名称": _device_name(device_graph, b),
                "修正方案": "SVG 存在多个电气孤岛，需定位中间断点设备并补全连接",
                "修正sql": "-- 请结合图纸定位断点并补全拓扑",
            })

    # -------- 模型有图无（P4 类）--------
    for defect in defects_report:
        if defect.get("defect_type") == "模型有图上无":
            dev_id = str(defect.get("equip_id") or "")
            _append({
                "起点设备id": dev_id,
                "终点设备id": dev_id,
                "断点类型": "[P4]模型有图无",
                "本侧疑似断点设备id": dev_id,
                "本侧疑似断点设备名称": defect.get("equip_name") or _device_name(device_graph, dev_id),
                "对侧疑似断点设备id": "",
                "对侧疑似断点设备名称": "",
                "修正方案": defect.get("suggestion", ""),
                "修正sql": defect.get("sql_draft", ""),
            })

    # 按 P1-P7 优先级排序，序号列
    def _priority_key(row):
        m = _PRIORITY_RE.search(row.get("断点类型", ""))
        if m:
            return _PRIORITY_ORDER.get(m.group(1), 99)
        return 99

    rows.sort(key=_priority_key)
    for idx, row in enumerate(rows, start=1):
        row["序号"] = idx

    logger.info("Sheet2 断点定位: feeder=%s 共 %d 条 (P1-P7 优先级排序)", feeder_id, len(rows))
    return rows


# ------------------------------------------------------------------
#  Sheet 4：非计划性合环拓扑识别
# ------------------------------------------------------------------
def analyze_unplanned_loops(
    *,
    feeder_id: str,
    line_name: str,
    start_st_id: str,
    device_graph: nx.Graph,
    tie_rows: list,
    dist_topo: TopologyGraph,
    line_df,
) -> list[dict]:
    """Sheet4 非计划性合环拓扑识别（所有合环均视为非计划）。"""
    fid2name: dict = {}
    fid2station: dict = {}
    if line_df is not None:
        for _, row in line_df.iterrows():
            lid = str(row.get("LINE_ID") or "")
            fid2name[lid] = str(row.get("LINE_NAME") or lid)
            fid2station[lid] = str(row.get("START_ST_ID") or "")

    rows: list = []
    seen: set = set()

    sub = _feeder_subgraph(device_graph, feeder_id)
    if sub.number_of_nodes() >= 3:
        try:
            cycles = nx.cycle_basis(sub)
        except Exception:
            cycles = []
        for cycle in cycles:
            if len(cycle) < 3:
                continue
            sw_id = next(
                (n for n in cycle if _is_switch_node(device_graph, n)),
                cycle[0]
            )
            key = ("internal", feeder_id, sw_id, tuple(sorted(cycle)))
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "线路id": feeder_id,
                "线路名称": line_name,
                "上级变电站名称": start_st_id,
                "合环线路id": feeder_id,
                "合环线路名称": line_name or fid2name.get(str(feeder_id), str(feeder_id)),
                "合环线变电站名称": start_st_id or fid2station.get(str(feeder_id), ""),
                "疑似联络开关id": sw_id,
                "疑似联络开关名称": _device_name(device_graph, sw_id),
                "修正sql": (
                    f"-- 馈线内部存在合环回路(节点数{len(cycle)})，"
                    f"建议核查开关 {sw_id} 分合状态并断开合环"
                ),
            })

    for tie in tie_rows:
        if tie.get("是否有联络") != "是":
            continue
        other_id = tie.get("联络线路id", "")
        sw_id = tie.get("联络开关id", "")
        key = ("cross", feeder_id, other_id, sw_id)
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "线路id": feeder_id,
            "线路名称": line_name or tie.get("线路名称", ""),
            "上级变电站名称": start_st_id or tie.get("上级变电站名称", ""),
            "合环线路id": other_id,
            "合环线路名称": tie.get("联络线路名称", other_id),
            "合环线变电站名称": tie.get("联络线变电站名称", ""),
            "疑似联络开关id": sw_id,
            "疑似联络开关名称": tie.get("联络开关名称", ""),
            "修正sql": (
                f"UPDATE EQUIP_JBS_PWEQUIPINFO SET STATUS='0' WHERE EQUIP_ID='{sw_id}'; "
                f"-- 断开联络开关以消除 {line_name} 与 {tie.get('联络线路名称')} 间的非计划合环"
            ),
        })

    if not rows:
        rows.append({
            "线路id": feeder_id,
            "线路名称": line_name,
            "上级变电站名称": start_st_id,
            "合环线路id": "",
            "合环线路名称": "",
            "合环线变电站名称": "",
            "疑似联络开关id": "",
            "疑似联络开关名称": "",
            "修正sql": "-- 当前馈线未识别到非计划合环",
        })

    logger.info("Sheet4 合环识别: feeder=%s 共 %d 条", feeder_id, len(rows))
    return rows


# ------------------------------------------------------------------
#  Sheet 5：模型修正质量评分
# ------------------------------------------------------------------
def build_score_rows(
    *,
    line_name: str,
    feeder_id: str,
    start_st_id: str,
    score_summary: dict,
) -> list[dict]:
    """Sheet5 模型修正质量评分任务结果。"""
    rows: list = []
    rows.append({
        "序号": 1,
        "厂站名称": start_st_id or "未知厂站",
        "厂站id": start_st_id,
        "馈线名称": line_name,
        "馈线id": feeder_id,
        "修正前评分": score_summary.get("score_before"),
        "修正后评分": score_summary.get("score_after"),
    })

    type_stats: dict = defaultdict(lambda: {"count": 0, "deduction": 0.0, "confidence": []})
    for item in score_summary.get("processed_defects", []):
        dtype = item.get("defect_type", "其它")
        type_stats[dtype]["count"] += 1
        type_stats[dtype]["deduction"] += float(item.get("score_deduction") or 0)
        type_stats[dtype]["confidence"].append(float(item.get("confidence") or 0))

    seq = 2
    for dtype, stats in sorted(type_stats.items()):
        avg_conf = (
            sum(stats["confidence"]) / len(stats["confidence"])
            if stats["confidence"] else 0
        )
        rows.append({
            "序号": seq,
            "厂站名称": f"{dtype}({stats['count']}处)",
            "厂站id": f"累计扣分{stats['deduction']:.2f}",
            "馈线名称": f"平均置信度{avg_conf:.2f}",
            "馈线id": feeder_id,
            "修正前评分": score_summary.get("score_before"),
            "修正后评分": score_summary.get("score_after"),
        })
        seq += 1

    rows.append({
        "序号": seq,
        "厂站名称": (
            f"汇总: 缺陷{score_summary.get('defect_count', 0)}处 / "
            f"总扣分{score_summary.get('total_deduction', 0)}"
        ),
        "厂站id": start_st_id,
        "馈线名称": line_name,
        "馈线id": feeder_id,
        "修正前评分": score_summary.get("score_before"),
        "修正后评分": score_summary.get("score_after"),
    })
    return rows


# ------------------------------------------------------------------
#  汇总入口（compare.py 调用）
# ------------------------------------------------------------------
def build_feeder_analysis(
    *,
    line_name: str,
    feeder_id: str,
    start_st_id: str,
    dist_topo: TopologyGraph,
    table_data: dict,
    svg_connections: list,
    element_to_object_map: dict,
    line_db_devices: dict,
    defects_report: list,
    score_summary: dict,
) -> dict:
    """
    汇总单馈线全部分析结果，供 Excel 导出使用。
    返回 dict：
      breakpoints  → Sheet2
      tie_switches → Sheet3
      loops        → Sheet4
      scores       → Sheet5
    """
    device_graph = build_device_graph(dist_topo, table_data)
    line_df = table_data.get("line")

    # Sheet3 联络开关（使用全库设备图，修复了 SVG 局部图的问题）
    tie_rows = analyze_tie_switches(
        feeder_id=feeder_id,
        line_name=line_name,
        start_st_id=start_st_id,
        device_graph=device_graph,
        dist_topo=dist_topo,
        line_df=line_df,
    )

    # Sheet2 断点（P1-P7 优先级分类）
    breakpoints = analyze_breakpoints(
        feeder_id=feeder_id,
        svg_connections=svg_connections,
        element_to_object_map=element_to_object_map,
        line_db_devices=line_db_devices,
        device_graph=device_graph,
        defects_report=defects_report,
        dist_topo=dist_topo,
    )

    # Sheet4 合环
    loop_rows = analyze_unplanned_loops(
        feeder_id=feeder_id,
        line_name=line_name,
        start_st_id=start_st_id,
        device_graph=device_graph,
        tie_rows=tie_rows,
        dist_topo=dist_topo,
        line_df=line_df,
    )

    # Sheet5 评分
    score_rows = build_score_rows(
        line_name=line_name,
        feeder_id=feeder_id,
        start_st_id=start_st_id,
        score_summary=score_summary,
    )

    return {
        "breakpoints": breakpoints,
        "tie_switches": tie_rows,
        "loops": loop_rows,
        "scores": score_rows,
        "line_name": line_name,
        "feeder_id": feeder_id,
        "start_st_id": start_st_id,
    }
