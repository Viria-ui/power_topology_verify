# -*- coding: utf-8 -*-
"""馈线拓扑扩展分析：断点定位、联络开关、合环识别。"""
from __future__ import annotations

from collections import defaultdict

import networkx as nx

from core.graph_model import TopologyGraph

SWITCH_TYPES = {"断路器", "负荷开关", "隔离开关", "联络开关", "0307", "0201", "0202", "0203", "0302", "0305", "0306", "0309"}


def build_device_graph(
    dist_topo: TopologyGraph,
    table_data: dict | None = None,
) -> nx.Graph:
    """将 TopologyGraph 折叠为设备级无向图。"""
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
            node2devs: dict[str, set[str]] = {}
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

        line_df = table_data.get("line")
        if line_df is not None and G.number_of_edges() == 0:
            for _, row in line_df.iterrows():
                ss = str(row.get("START_ST_ID") or "").strip()
                ee = str(row.get("END_ST_ID") or "").strip()
                if ss in device_ids and ee in device_ids and ss != ee:
                    G.add_edge(ss, ee)

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
    feeder_device_ids: set[str] | None = None,
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


def _device_name(device_graph: nx.Graph, dev_id: str, fallback: str = "") -> str:
    if device_graph.has_node(dev_id):
        return str(device_graph.nodes[dev_id].get("equip_name") or fallback or dev_id)
    return fallback or dev_id


def _is_switch_node(device_graph: nx.Graph, node_id: str) -> bool:
    if not device_graph.has_node(node_id):
        return False
    tp = str(device_graph.nodes[node_id].get("equip_type") or "")
    if tp in SWITCH_TYPES or "开关" in tp or "断路" in tp:
        return True
    try:
        return int(tp) in (1705, 1706, 1707, 111, 115, 307)
    except Exception:
        return False


def _has_db_path(device_graph: nx.Graph, a: str, b: str) -> bool:
    if not device_graph.has_node(a) or not device_graph.has_node(b):
        return False
    if device_graph.has_edge(a, b):
        return True
    try:
        return nx.has_path(device_graph, a, b)
    except Exception:
        return False


def analyze_breakpoints(
    *,
    feeder_id: str,
    svg_connections: list,
    element_to_object_map: dict,
    line_db_devices: dict,
    device_graph: nx.Graph,
    defects_report: list[dict],
) -> list[dict]:
    """拓扑连通性异常诊断与断点定位。"""
    feeder_ids = set(line_db_devices.keys())
    db_sub = _feeder_subgraph(device_graph, feeder_id)
    svg_g = _build_svg_graph(svg_connections, element_to_object_map, feeder_ids)
    rows: list[dict] = []
    seen: set[tuple] = set()

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
        _append({
            "起点设备id": a,
            "终点设备id": b,
            "断点类型": "图形物理连通、拓扑逻辑断开",
            "本侧疑似断点设备id": a,
            "本侧疑似断点设备名称": defect.get("equip_name") or _device_name(device_graph, a),
            "对侧疑似断点设备id": b,
            "对侧疑似断点设备名称": _device_name(device_graph, b),
            "修正方案": defect.get("suggestion", ""),
            "修正sql": defect.get("sql_draft", ""),
        })

    for a, b in svg_g.edges():
        if a not in feeder_ids and b not in feeder_ids:
            continue
        if not _has_db_path(db_sub, a, b):
            near_id, far_id = a, b
            if _is_switch_node(device_graph, b) and not _is_switch_node(device_graph, a):
                near_id, far_id = b, a
            _append({
                "起点设备id": a,
                "终点设备id": b,
                "断点类型": "SVG连通但模型不连通",
                "本侧疑似断点设备id": near_id,
                "本侧疑似断点设备名称": _device_name(device_graph, near_id),
                "对侧疑似断点设备id": far_id,
                "对侧疑似断点设备名称": _device_name(device_graph, far_id),
                "修正方案": f"建议在模型中补全 {a} 与 {b} 之间的拓扑连接",
                "修正sql": (
                    f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (START_ST_ID, END_ST_ID, FEEDER_ID) "
                    f"VALUES ('{a}', '{b}', '{feeder_id}');"
                ),
            })

    for node in svg_g.nodes():
        if svg_g.degree(node) == 0:
            _append({
                "起点设备id": node,
                "终点设备id": node,
                "断点类型": "孤立节点",
                "本侧疑似断点设备id": node,
                "本侧疑似断点设备名称": _device_name(device_graph, node),
                "对侧疑似断点设备id": "",
                "对侧疑似断点设备名称": "",
                "修正方案": "SVG图元未与任何设备建立有效连接，建议补画连接关系",
                "修正sql": "-- SVG层面补全连接，无需直接修改数据库",
            })

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
                "断点类型": "连通分量断裂",
                "本侧疑似断点设备id": a,
                "本侧疑似断点设备名称": _device_name(device_graph, a),
                "对侧疑似断点设备id": b,
                "对侧疑似断点设备名称": _device_name(device_graph, b),
                "修正方案": "SVG存在多个电气孤岛，需定位中间断点设备并补全连接",
                "修正sql": "-- 请结合图纸定位断点并补全拓扑",
            })

    for defect in defects_report:
        if defect.get("defect_type") == "模型有图上无":
            dev_id = str(defect.get("equip_id") or "")
            _append({
                "起点设备id": dev_id,
                "终点设备id": dev_id,
                "断点类型": "模型有图无",
                "本侧疑似断点设备id": dev_id,
                "本侧疑似断点设备名称": defect.get("equip_name") or _device_name(device_graph, dev_id),
                "对侧疑似断点设备id": "",
                "对侧疑似断点设备名称": "",
                "修正方案": defect.get("suggestion", ""),
                "修正sql": defect.get("sql_draft", ""),
            })

    for idx, row in enumerate(rows, start=1):
        row["序号"] = idx
    return rows


def analyze_tie_switches(
    *,
    feeder_id: str,
    line_name: str,
    start_st_id: str,
    device_graph: nx.Graph,
    line_df,
) -> list[dict]:
    """联络开关自动识别与梳理。"""
    fid2name: dict[str, str] = {}
    fid2station: dict[str, str] = {}
    if line_df is not None:
        for _, row in line_df.iterrows():
            lid = str(row.get("LINE_ID") or "")
            fid2name[lid] = str(row.get("LINE_NAME") or lid)
            fid2station[lid] = str(row.get("START_ST_ID") or "")

    target = str(feeder_id)
    tie_rows: list[dict] = []
    tie_set: set[tuple] = set()

    def _fid_of(devid: str) -> str:
        if device_graph.has_node(devid):
            return str(device_graph.nodes[devid].get("feeder_id") or "")
        return ""

    for node in device_graph.nodes():
        neighbors = list(device_graph.neighbors(node))
        fids = {_fid_of(nb) for nb in neighbors if _fid_of(nb)}
        if len(fids) < 2:
            continue
        my_fids, other_fids = [], []
        for f in fids:
            if f == target:
                my_fids.append(f)
            else:
                other_fids.append(f)
        if not my_fids or not other_fids:
            continue
        if not _is_switch_node(device_graph, node):
            continue
        sw_name = _device_name(device_graph, node)
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
                "联络开关名称": sw_name,
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
    return tie_rows


def analyze_unplanned_loops(
    *,
    feeder_id: str,
    line_name: str,
    start_st_id: str,
    device_graph: nx.Graph,
    tie_rows: list[dict],
    line_df,
) -> list[dict]:
    """非计划性合环拓扑识别（所有合环均视为非计划）。"""
    fid2name: dict[str, str] = {}
    fid2station: dict[str, str] = {}
    if line_df is not None:
        for _, row in line_df.iterrows():
            lid = str(row.get("LINE_ID") or "")
            fid2name[lid] = str(row.get("LINE_NAME") or lid)
            fid2station[lid] = str(row.get("START_ST_ID") or "")

    rows: list[dict] = []
    seen: set[tuple] = set()

    sub = _feeder_subgraph(device_graph, feeder_id)
    if sub.number_of_nodes() >= 3:
        try:
            cycles = nx.cycle_basis(sub)
        except Exception:
            cycles = []
        for cycle in cycles:
            if len(cycle) < 3:
                continue
            sw_id = next((n for n in cycle if _is_switch_node(device_graph, n)), cycle[0])
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
                    f"-- 馈线内部存在合环回路(节点数{len(cycle)})，建议核查开关 {sw_id} 分合状态并断开合环"
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
    return rows


def build_score_rows(
    *,
    line_name: str,
    feeder_id: str,
    start_st_id: str,
    score_summary: dict,
) -> list[dict]:
    """模型修正质量评分任务结果。"""
    rows: list[dict] = []
    rows.append({
        "序号": 1,
        "厂站名称": start_st_id or "未知厂站",
        "厂站id": start_st_id,
        "馈线名称": line_name,
        "馈线id": feeder_id,
        "修正前评分": score_summary.get("score_before"),
        "修正后评分": score_summary.get("score_after"),
    })

    type_stats: dict[str, dict] = defaultdict(lambda: {"count": 0, "deduction": 0.0, "confidence": []})
    for item in score_summary.get("processed_defects", []):
        dtype = item.get("defect_type", "其它")
        type_stats[dtype]["count"] += 1
        type_stats[dtype]["deduction"] += float(item.get("score_deduction") or 0)
        type_stats[dtype]["confidence"].append(float(item.get("confidence") or 0))

    seq = 2
    for dtype, stats in sorted(type_stats.items()):
        avg_conf = sum(stats["confidence"]) / len(stats["confidence"]) if stats["confidence"] else 0
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
    defects_report: list[dict],
    score_summary: dict,
) -> dict:
    """汇总单馈线全部分析结果，供 Excel 导出使用。"""
    device_graph = build_device_graph(dist_topo, table_data)
    line_df = table_data.get("line")

    breakpoints = analyze_breakpoints(
        feeder_id=feeder_id,
        svg_connections=svg_connections,
        element_to_object_map=element_to_object_map,
        line_db_devices=line_db_devices,
        device_graph=device_graph,
        defects_report=defects_report,
    )
    tie_rows = analyze_tie_switches(
        feeder_id=feeder_id,
        line_name=line_name,
        start_st_id=start_st_id,
        device_graph=device_graph,
        line_df=line_df,
    )
    loop_rows = analyze_unplanned_loops(
        feeder_id=feeder_id,
        line_name=line_name,
        start_st_id=start_st_id,
        device_graph=device_graph,
        tie_rows=tie_rows,
        line_df=line_df,
    )
    score_rows = build_score_rows(
        line_name=line_name,
        feeder_id=feeder_id,
        start_st_id=start_st_id,
        score_summary=score_summary,
    )
    return {
        "defects": defects_report,
        "breakpoints": breakpoints,
        "tie_switches": tie_rows,
        "loops": loop_rows,
        "scores": score_rows,
        "line_name": line_name,
        "feeder_id": feeder_id,
        "start_st_id": start_st_id,
    }
