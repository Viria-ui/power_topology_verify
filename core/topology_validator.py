"""拓扑与SVG质量校验模块。

缺陷条目结构（严格对齐成员2）:
    {
        "equip_id": str,
        "defect_type": str,
        "description": str,
        "suggestion": str,
        "sql_draft": str,
    }
"""
import os
import re
import json
from typing import Tuple, Optional
from collections import defaultdict
from typing import Optional, Union

import networkx as nx

from data_io.svg_reader import SvgDocument, SvgElement, SvgConnection, SvgText
from core.graph_model import TopologyGraph, AbnormalItem, BreakpointItem, TieLoopItem
from core.constants import (
    TERMINAL_EXEMPT_TYPES, NON_TERMINAL_SWITCH_TYPES,
    TIE_EXCLUDE_NAME_KEYS, TEST_LINE_KEYS,
    ERR, SUSPECT, EXEMPT, REVIEW,
    R_TIE_EXCLUDE_001, R_TIE_001, R_TIE_002, R_LOOP_001,
    R001, R002, R003,
    SWITCH_STATUS_MAP
)


_SQL_TODO = "--建议人工核对后补 INSERT/UPDATE"


def _short_has_digit_boundary(haystack: str, needle: str) -> bool:
    """在字符串中查找 needle，要求其左右边界都是非数字（或串首尾）。"""
    if not needle or not haystack:
        return False
    for m in re.finditer(re.escape(needle), haystack):
        left_ok = m.start() == 0 or not haystack[m.start() - 1].isdigit()
        right_ok = m.end() == len(haystack) or not haystack[m.end()].isdigit()
        if left_ok and right_ok:
            return True
    return False


def _find_device_by_short(doc: SvgDocument, short: str,
                           layer: str | None = None) -> SvgElement | None:
    """在 doc.elements 中按短编号精确找设备（避免子串误匹配）。

    匹配优先级：
      1. element_id 末尾 == short（完全尾部）
      2. element_name 含 数字边界包裹的 short + 设备类型关键词前缀
      3. texts 中 content 含数字边界包裹的 short，object_id 对应元素
    """
    if not short:
        return None
    candidates = []  # (score, elem)

    for e in doc.elements:
        if layer and e.layer_name != layer:
            pass
        score = 0
        eid = e.element_id or ""
        ename = e.element_name or ""
        # (1) 末尾完全匹配 = short
        if eid.endswith(short):
            score = 500
            # layer 命中加分
            if layer and e.layer_name == layer:
                score += 100
            candidates.append((score, e))
            continue
        # (2) name 中按数字边界匹配
        if _short_has_digit_boundary(ename, short):
            score = 400
            if layer and e.layer_name == layer:
                score += 100
            candidates.append((score, e))

    # (3) 走 texts
    if not candidates:
        for t in doc.texts:
            if t.object_id and _short_has_digit_boundary(t.content or "", short):
                elem = doc.get_device_by_id(t.object_id)
                if elem is not None:
                    candidates.append((300, elem))
                    break

    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


def _make_defect(equip_id: str, defect_type: str, description: str,
                 suggestion: str, sql_draft: str = _SQL_TODO) -> dict:
    return {
        "equip_id": equip_id,
        "defect_type": defect_type,
        "description": description,
        "suggestion": suggestion,
        "sql_draft": sql_draft,
    }


def _get_max_device_size(doc: SvgDocument) -> float:
    max_s = 0.0
    for e in doc.elements:
        if not isinstance(e, SvgElement):
            continue
        w = e.width if e.width and e.width > 0 else 1.0
        h = e.height if e.height and e.height > 0 else 1.0
        max_s = max(max_s, w, h)
    return max_s if max_s > 0 else 1.0


def _bbox_area(e: SvgElement) -> float:
    w = e.width if e.width and e.width > 0 else 1.0
    h = e.height if e.height and e.height > 0 else 1.0
    return w * h


def _bbox_overlap_area(a: SvgElement, b: SvgElement) -> float:
    ax1, ay1 = a.x, a.y
    ax2, ay2 = ax1 + (a.width if a.width > 0 else 1), ay1 + (a.height if a.height > 0 else 1)
    bx1, by1 = b.x, b.y
    bx2, by2 = bx1 + (b.width if b.width > 0 else 1), by1 + (b.height if b.height > 0 else 1)
    ox1, oy1 = max(ax1, bx1), max(ay1, by1)
    ox2, oy2 = min(ax2, bx2), min(ay2, by2)
    if ox2 <= ox1 or oy2 <= oy1:
        return 0.0
    return (ox2 - ox1) * (oy2 - oy1)


def _point_to_bbox_dist(px: float, py: float, e: SvgElement) -> float:
    w = e.width if e.width and e.width > 0 else 1.0
    h = e.height if e.height and e.height > 0 else 1.0
    cx, cy = e.x + w / 2, e.y + h / 2
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5


# ----------------------------------------------------------------------
# 1) SVG 自洽性校验
# ----------------------------------------------------------------------
def validate_svg_only(doc: SvgDocument, stage: str = "pre") -> Tuple[list, dict]:
    """仅校验 SVG 自身拓扑自洽性。

    Returns:
        (defects: list[dict], summary: dict)
    """
    defects: list[dict] = []
    max_size = _get_max_device_size(doc)

    # ---- a. 孤岛检测 ----
    conn_dev_ids = set()
    g = nx.Graph()
    for conn in doc.connections:
        s, e = conn.start_device_id, conn.end_device_id
        if s:
            conn_dev_ids.add(s)
            g.add_node(s)
        if e:
            conn_dev_ids.add(e)
            g.add_node(e)
        if s and e:
            g.add_edge(s, e)

    components = list(nx.connected_components(g)) if conn_dev_ids else []
    components_count = len(components)
    max_component_size = max((len(c) for c in components), default=0)

    # 孤岛：分量大小=1 且设备非 PoleCode/Substation（允许孤立站房和杆塔）
    for comp in components:
        if len(comp) == 1:
            dev_id = next(iter(comp))
            elem = doc.get_device_by_id(dev_id)
            if elem is None:
                continue
            if elem.layer_name in ("PoleCode", "Substation"):
                continue
            defects.append(_make_defect(
                equip_id=dev_id,
                defect_type="孤岛设备",
                description=f"设备[{elem.element_name or elem.element_type}](ID:{dev_id})为孤立节点，未与其他设备形成有效连通分量",
                suggestion=f"建议核查该设备连接关系，补画连接线或删除孤立图元（stage={stage}）",
            ))

    # ---- b. 悬空端点 / 飞线 ----
    dangling_count = 0
    for conn in doc.connections:
        s_ok = bool(conn.start_device_id)
        e_ok = bool(conn.end_device_id)
        # 空端点
        if not s_ok or not e_ok:
            dangling_count += 1
            defects.append(_make_defect(
                equip_id=conn.connection_id,
                defect_type="飞线-悬空端点",
                description=f"连接线[{conn.connection_id}] 端点缺失: start={conn.start_device_id!r} end={conn.end_device_id!r}",
                suggestion="建议补全连接线端点指向的设备ID，或删除无效飞线",
            ))
            continue
        # 端点离主体设备包围盒过远
        s_dev = doc.get_device_by_id(conn.start_device_id)
        e_dev = doc.get_device_by_id(conn.end_device_id)
        if s_dev and conn.points:
            d = _point_to_bbox_dist(conn.points[0][0], conn.points[0][1], s_dev)
            if d > max_size * 3:
                dangling_count += 1
                defects.append(_make_defect(
                    equip_id=conn.connection_id,
                    defect_type="飞线-端点偏离设备",
                    description=f"连接线[{conn.connection_id}] 起点距设备[{s_dev.element_name}]包围盒距离={d:.2f} > 阈值({max_size*3:.2f})",
                    suggestion="建议调整连接线端点位置或重新匹配端点归属设备",
                ))
        if e_dev and conn.points:
            d = _point_to_bbox_dist(conn.points[-1][0], conn.points[-1][1], e_dev)
            if d > max_size * 3:
                dangling_count += 1
                defects.append(_make_defect(
                    equip_id=conn.connection_id,
                    defect_type="飞线-端点偏离设备",
                    description=f"连接线[{conn.connection_id}] 终点距设备[{e_dev.element_name}]包围盒距离={d:.2f} > 阈值({max_size*3:.2f})",
                    suggestion="建议调整连接线端点位置或重新匹配端点归属设备",
                ))

    # ---- c. 虚假连通 ----
    fake_connect_count = 0
    for conn in doc.connections:
        sid, eid = conn.start_device_id, conn.end_device_id
        if not sid or not eid:
            continue
        s_dev = doc.get_device_by_id(sid)
        e_dev = doc.get_device_by_id(eid)
        if s_dev is None or e_dev is None:
            continue
        # 两端的 glink_refs 互不包含
        if eid not in s_dev.glink_refs and sid not in e_dev.glink_refs:
            w = s_dev.width if s_dev.width and s_dev.width > 0 else 1.0
            h = s_dev.height if s_dev.height and s_dev.height > 0 else 1.0
            sx, sy = s_dev.x + w / 2, s_dev.y + h / 2
            w2 = e_dev.width if e_dev.width and e_dev.width > 0 else 1.0
            h2 = e_dev.height if e_dev.height and e_dev.height > 0 else 1.0
            ex, ey = e_dev.x + w2 / 2, e_dev.y + h2 / 2
            dist = ((sx - ex) ** 2 + (sy - ey) ** 2) ** 0.5
            if dist > max_size * 1:
                fake_connect_count += 1
                defects.append(_make_defect(
                    equip_id=conn.connection_id,
                    defect_type="虚假连通",
                    description=f"连接线[{conn.connection_id}] 连接的两端设备[{s_dev.element_name}]-[{e_dev.element_name}] 无互引GLink，几何距离={dist:.2f} > 阈值({max_size:.2f})，疑似乱凑对",
                    suggestion="建议核对两端设备是否真的物理相连，不对应则删除该连接并补画正确连接",
                ))

    # ---- d. 设备重叠 ----
    overlap_count = 0
    n = len(doc.elements)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = doc.elements[i], doc.elements[j]
            if a.layer_name != b.layer_name and {a.layer_name, b.layer_name} <= {"Substation", "LoadBreakSwitch", "Breaker"}:
                pass
            oa = _bbox_overlap_area(a, b)
            if oa <= 0:
                continue
            area_a = _bbox_area(a)
            area_b = _bbox_area(b)
            if oa > min(area_a, area_b) * 0.5:
                overlap_count += 1
                defects.append(_make_defect(
                    equip_id=a.element_id,
                    defect_type="设备重叠",
                    description=f"设备[{a.element_name or a.element_id}]({a.element_id}) 与 [{b.element_name or b.element_id}]({b.element_id}) bbox重叠率={oa/min(area_a,area_b):.2%} > 50%",
                    suggestion="建议移动其中一台设备，保持设备图元无大面积重叠",
                ))

    # ---- e. 文字-设备关联缺失 ----
    text_missing_count = 0
    valid_elem_ids = {e.element_id for e in doc.elements}
    for txt in doc.texts:
        if not txt.object_id:
            continue
        if txt.object_id not in valid_elem_ids:
            text_missing_count += 1
            defects.append(_make_defect(
                equip_id=txt.object_id,
                defect_type="标注错位",
                description=f"文字标注[{txt.content}](object_id={txt.object_id}) 指向的设备 element_id 在图中不存在",
                suggestion="建议修正文字 PSR_Ref.ObjectID 为真实存在的设备ID，或补充缺失图元",
            ))

    summary = {
        "components_count": components_count,
        "max_component_size": max_component_size,
        "dangling_count": dangling_count,
        "overlap_count": overlap_count,
        "fake_connect_count": fake_connect_count,
        "text_missing_count": text_missing_count,
        "total_defects": len(defects),
        "stage": stage,
    }
    return defects, summary


# ----------------------------------------------------------------------
# 2) SVG vs 逻辑拓扑一致性校验
# ----------------------------------------------------------------------
def validate_svg_vs_topology(doc: SvgDocument, topo: TopologyGraph,
                              stage: str = "post_edit") -> Tuple[list, dict]:
    """校验 SVG 与 TopologyGraph 逻辑拓扑一致性。
    
    实现成员2要求的四类校验：
    1. 图上有模型无
    2. 模型有图无
    3. 物理连接不一致
    4. 逻辑连接不一致 (属性不一致)
    """
    defects: list[dict] = []
    
    # 建立 SVG 设备映射 (object_id -> elem)
    svg_device_map = {}
    for e in doc.elements:
        oid = e.element_id # IR 中 element_id 存放的是 ObjectID
        if oid:
            svg_device_map[oid] = e
            
    topo_device_ids = set(topo.device_map.keys())
    svg_device_ids = set(svg_device_map.keys())

    SVG_EXEMPT_TYPES = {"Junction", "接头", "PoleCode", "杆塔", "Other"}
    feeder_id = doc.feeder_id

    # ---- 1. 图上有模型无 ----
    for oid, e in svg_device_map.items():
        if oid not in topo_device_ids:
            layer = (e.layer_name or "").strip()
            ptype = (e.psr_type or "").strip()
            ename = (e.element_name or "").strip()
            if layer in SVG_EXEMPT_TYPES and not ename:
                continue
            defects.append(_make_defect(
                equip_id=oid,
                defect_type="图上有模型无",
                description=f"SVG图纸存在设备[{ename or e.element_type}](ID:{oid} 图层={layer})，但数据库拓扑模型中缺失",
                suggestion=f"建议核查是否为非设备图元。若非豁免接头/杆塔，在 EQUIP_JBS_PWEQUIPINFO 中补全设备 {oid}",
                sql_draft=f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID,EQUIP_NAME,EQUIP_TYPE,FEEDER_ID,VOLTAGE_TYPE,DSUBSTATION_ID,STATUS) VALUES ('{oid}','{ename or 'SVG补录'}','{ptype or layer}','{feeder_id}','1010','','1');",
            ))

    # ---- 2. 模型有图无 ----
    topo_feeder_devices = {tid: dev for tid, dev in topo.device_map.items()
                           if (dev.feeder_id == feeder_id or not feeder_id)}
    MODEL_EXEMPT = SVG_EXEMPT_TYPES | {"Junction", "1700"}
    for tid, dev in topo_feeder_devices.items():
        if tid in svg_device_ids:
            continue
        dtype = (dev.equip_type or "").strip()
        dname = (dev.equip_name or "").strip()
        if dtype in MODEL_EXEMPT:
            continue
        defects.append(_make_defect(
            equip_id=tid,
            defect_type="模型有图无",
            description=f"数据库模型存在设备[{dname or tid}](ID:{tid} TYPE={dtype})，但SVG图纸中缺失图元",
            suggestion=f"请在SVG图层 {dtype}_Layer 补画设备图元 {tid} 及PSR_Ref元数据标注",
            sql_draft=f"-- SVG图缺失: 请在SVG图层={dtype}_Layer 补画ID={tid} 并添加iec:PSR_Ref元数据",
        ))

    # ---- 3. 物理连接不一致 ----
    # 正确比较：TopologyGraph.graph 是设备节点 + 真实端子(TERMINAL_ID)混合图，
    # 边只存在 TERMINAL-TERMINAL(CONNECT_NODE连接) 和 DEVICE-TERMINAL(挂点)。
    svg_pairs: set[tuple[str, str]] = set()
    for conn in doc.connections:
        s, e = conn.start_device_id, conn.end_device_id
        if s and e and s != e:
            svg_pairs.add(tuple(sorted([s, e])))

    G = topo.graph
    for s, e in svg_pairs:
        if s not in G.nodes or e not in G.nodes:
            defects.append(_make_defect(
                equip_id=f"{s} <-> {e}",
                defect_type="物理连接不一致",
                description=f"SVG存在 {s}-{e} 连线，但一方设备未出现在模型端子图中(缺设备或缺端子)",
                suggestion="核查PWTERMINAL/PWEQUIPINFO是否漏录SVG连接双方设备及端子",
                sql_draft=f"-- 先补EQUIP_JBS_PWTERMINAL的{s}/{e}端子及CONNECT_NODE_ID,再补PWFEEDERLINE边",
            ))
            continue
        pts_s = list(topo._points_by_equip.get(s, [])) if hasattr(topo, "_points_by_equip") else []
        pts_e = list(topo._points_by_equip.get(e, [])) if hasattr(topo, "_points_by_equip") else []
        has_logic_conn = False
        try:
            cand_pairs = []
            if pts_s and pts_e:
                cand_pairs = [(a, b) for a in pts_s if G.has_node(a) for b in pts_e if G.has_node(b)]
            else:
                cand_pairs = [(s, e)]
            for a, b in cand_pairs:
                if nx.has_path(G, a, b):
                    plen = len(nx.shortest_path(G, a, b))
                    if plen <= 10:  # 允许若干跳：设备A-端子A-端子N-...-端子N-设备B
                        has_logic_conn = True
                        break
        except Exception:
            has_logic_conn = False
        if not has_logic_conn:
            defects.append(_make_defect(
                equip_id=f"{s} <-> {e}",
                defect_type="物理连接不一致",
                description=f"SVG存在物理连接{s}-{e}，但模型端子图不连通(候选端子对={len(cand_pairs) if pts_s else '无端子'})",
                suggestion="建议在PWFEEDERLINE补线段记录，或PWTERMINAL补端子并对齐CONNECT_NODE_ID",
                sql_draft=f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (LINE_ID,START_ST_ID,END_ST_ID,FEEDER_ID,VOLTAGE_TYPE,STATUS) VALUES ('LN_{s}_{e}','{s}','{e}','{feeder_id}','1010','1');",
            ))

    # ---- 4. 逻辑连接/属性不一致 ----
    common_ids = svg_device_ids & topo_device_ids
    for oid in common_ids:
        svg_elem = svg_device_map[oid]
        db_dev = topo.device_map[oid]
        
        svg_vol = svg_elem.voltage_level
        db_vol = db_dev.voltage_type
        
        # SVG 使用展示值 10kV，而数据库使用电压类型码 1010，必须归一化后比较。
        def _norm_voltage(value):
            text = str(value).strip().lower().replace(" ", "")
            if text in {"10kv", "10k", "1010"}: return "1010"
            return text.replace("kv", "")
        if svg_vol and db_vol and _norm_voltage(svg_vol) != _norm_voltage(db_vol):
            defects.append(_make_defect(
                equip_id=oid,
                defect_type="逻辑连接不一致",
                description=f"设备 {oid} 电压等级不一致：SVG为[{svg_vol}]，数据库为[{db_vol}]",
                suggestion="校对设备逻辑属性，建议以 SVG 图纸为准更新数据库",
                sql_draft=f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='{svg_vol}' WHERE EQUIP_ID='{oid}';"
            ))

    summary = {
        "stage": stage,
        "feeder_id": feeder_id,
        "topo_device_count": len(topo_feeder_devices),
        "svg_device_count": len(svg_device_ids),
        "defects_by_type": {
            "图上有模型无": len([d for d in defects if d["defect_type"] == "图上有模型无"]),
            "模型有图无": len([d for d in defects if d["defect_type"] == "模型有图无"]),
            "物理连接不一致": len([d for d in defects if d["defect_type"] == "物理连接不一致"]),
            "逻辑连接不一致": len([d for d in defects if d["defect_type"] == "逻辑连接不一致"]),
        },
        "total_defects": len(defects),
    }
    return defects, summary


# ----------------------------------------------------------------------
# 3) 编辑动作增量校验
# ----------------------------------------------------------------------
def validate_edit_action(doc_before: SvgDocument, doc_after: SvgDocument,
                          action: str) -> Tuple[list, dict]:
    """编辑动作增量校验 + 特定断言。"""
    pre_defects, pre_sum = validate_svg_only(doc_before, stage=f"{action}_pre")
    post_defects, post_sum = validate_svg_only(doc_after, stage=f"{action}_post")

    # 集合 diff：after 新增缺陷
    def _key(d):
        return (d["equip_id"], d["defect_type"], d["description"])

    pre_keys = {_key(d) for d in pre_defects}
    new_defects = [d for d in post_defects if _key(d) not in pre_keys]

    # 新增缺陷升级 severity（用 suggestion 前缀标记升级）
    for d in new_defects:
        d["suggestion"] = "[新增编辑缺陷·升级严重度] " + d["suggestion"]

    # ---- 特定动作断言 ----
    assertion_failures: list[dict] = []

    if action == "add_station_000300":
        # 1) 新增 1 个 Substation 名称含 000300
        before_stations = {e.element_id for e in doc_before.elements if e.layer_name == "Substation"}
        after_stations = [e for e in doc_after.elements if e.layer_name == "Substation" and e.element_id not in before_stations]
        target_station = None
        for s in after_stations:
            if (_short_has_digit_boundary(s.element_name or "", "000300")
                    or s.element_id.endswith("000300")):
                target_station = s
                break
        if target_station is None:
            assertion_failures.append(_make_defect(
                equip_id="000300",
                defect_type="编辑断言失败",
                description="add_station_000300: 未检测到新增 Substation 类型图元(名称/ID 含 000300)",
                suggestion="请核对新增站房图元类型与命名",
            ))

        # 2) 3 个 LoadBreakSwitch 00301/00302/00303
        before_sw_ids = {e.element_id for e in doc_before.elements if e.layer_name == "LoadBreakSwitch"}
        after_switches = [e for e in doc_after.elements if e.layer_name == "LoadBreakSwitch" and e.element_id not in before_sw_ids]

        def _has_short_exact(elem, short):
            return ((_short_has_digit_boundary(elem.element_name or "", short))
                    or elem.element_id.endswith(short))

        sw_00301 = next((s for s in after_switches if _has_short_exact(s, "00301")), None)
        sw_00302 = next((s for s in after_switches if _has_short_exact(s, "00302")), None)
        sw_00303 = next((s for s in after_switches if _has_short_exact(s, "00303")), None)
        for tag, sw in [("00301", sw_00301), ("00302", sw_00302), ("00303", sw_00303)]:
            if sw is None:
                assertion_failures.append(_make_defect(
                    equip_id=tag,
                    defect_type="编辑断言失败",
                    description=f"add_station_000300: 未检测到新增 LoadBreakSwitch-{tag}",
                    suggestion=f"请补画或命名开关 {tag}",
                ))

        # 连边上/下游：先按短编号精确找 doc_after 中真实的 00104(upstream)/00102(downstream)
        up_ref = _find_device_by_short(doc_after, "00104", "LoadBreakSwitch")
        down_ref = _find_device_by_short(doc_after, "00102", "LoadBreakSwitch")
        up_ref_id = up_ref.element_id if up_ref is not None else None
        down_ref_id = down_ref.element_id if down_ref is not None else None

        def _have_direct_conn(a_id: str, b_id: str) -> bool:
            if not a_id or not b_id:
                return False
            for conn in doc_after.connections:
                s = conn.start_device_id
                e = conn.end_device_id
                if not s or not e:
                    continue
                if (s == a_id and e == b_id) or (s == b_id and e == a_id):
                    return True
                refs = set(conn.glink_refs)
                if a_id in refs and b_id in refs:
                    return True
            return False

        # 连接断言
        if sw_00301 is not None and up_ref_id is not None:
            if not _have_direct_conn(sw_00301.element_id, up_ref_id):
                assertion_failures.append(_make_defect(
                    equip_id=sw_00301.element_id,
                    defect_type="编辑断言失败",
                    description=f"add_station_000300: 00301({sw_00301.element_id}) 未连接到上游 00104({up_ref_id})",
                    suggestion="请补连线 00104 -> 00301",
                ))
        elif sw_00301 is not None and up_ref_id is None:
            assertion_failures.append(_make_defect(
                equip_id="00104",
                defect_type="编辑断言失败",
                description="add_station_000300: 找不到上游 00104 设备，无法验证 00301 连边",
                suggestion="请确认 00104 图元仍存在于 LINE215 SVG 中",
            ))

        if sw_00303 is not None and down_ref_id is not None:
            if not _have_direct_conn(sw_00303.element_id, down_ref_id):
                assertion_failures.append(_make_defect(
                    equip_id=sw_00303.element_id,
                    defect_type="编辑断言失败",
                    description=f"add_station_000300: 00303({sw_00303.element_id}) 未连接到下游 00102({down_ref_id})",
                    suggestion="请补连线 00303 -> 00102",
                ))
        elif sw_00303 is not None and down_ref_id is None:
            assertion_failures.append(_make_defect(
                equip_id="00102",
                defect_type="编辑断言失败",
                description="add_station_000300: 找不到下游 00102 设备，无法验证 00303 连边",
                suggestion="请确认 00102 图元仍存在于 LINE215 SVG 中",
            ))

        if sw_00302 is not None:
            conn_ids = doc_after.get_connected_devices(sw_00302.element_id)
            # 同时数 connections 对中包含 00302 的条数作为备用
            nconn = 0
            for c in doc_after.connections:
                if (c.start_device_id == sw_00302.element_id
                        or c.end_device_id == sw_00302.element_id
                        or sw_00302.element_id in c.glink_refs):
                    nconn += 1
            if max(len(conn_ids), nconn) < 1:
                assertion_failures.append(_make_defect(
                    equip_id=sw_00302.element_id,
                    defect_type="编辑断言失败",
                    description="add_station_000300: 备用开关 00302 连接数 < 1",
                    suggestion="请保证 00302 至少有 1 条连接线（备用分支）",
                ))

    elif action == "delete_switch_00024":
        # Step0: 先在 doc_before 中用精确方式定位 target（避免 "00024" 作为随机子串）
        target_dev = _find_device_by_short(doc_before, "00024", "LoadBreakSwitch")
        target_ids: set[str] = set()
        target_names_bd: list[str] = []
        if target_dev is not None:
            target_ids.add(target_dev.element_id)
            if target_dev.element_name:
                target_names_bd.append(target_dev.element_name)
        # 文本精确匹配（数字边界）
        for t in doc_before.texts:
            if t.object_id and _short_has_digit_boundary(t.content or "", "00024"):
                if doc_before.get_device_by_id(t.object_id) is not None:
                    target_ids.add(t.object_id)
        # id 末尾精确匹配（00024 作为完整尾号）
        for e in doc_before.elements:
            if e.element_id.endswith("00024"):
                target_ids.add(e.element_id)
            if e.element_name and _short_has_digit_boundary(e.element_name, "00024"):
                target_ids.add(e.element_id)

        if not target_ids and target_dev is None:
            assertion_failures.append(_make_defect(
                equip_id="00024",
                defect_type="编辑断言失败",
                description="delete_switch_00024: 在删除前 SVG 中找不到目标开关 00024（精确匹配失败）",
                suggestion="请确认 LINE216 原始 SVG 中存在 00024 开关",
            ))

        # 1) doc_after 中 0 命中：exact ID + name digit-boundary
        remain_elems = [e for e in doc_after.elements
                        if e.element_id in target_ids
                        or (e.element_name and _short_has_digit_boundary(e.element_name, "00024"))]
        if remain_elems:
            for re in remain_elems:
                assertion_failures.append(_make_defect(
                    equip_id=re.element_id,
                    defect_type="编辑断言失败",
                    description=f"delete_switch_00024: 图元 {re.element_id}({re.element_name}) 仍存在于删除后 SVG",
                    suggestion="请彻底删除 00024 图元与引用",
                ))
        # 文字
        remain_txts = []
        for t in doc_after.texts:
            cond_obj = t.object_id in target_ids
            cond_cnt = _short_has_digit_boundary(t.content or "", "00024")
            if cond_obj or cond_cnt:
                remain_txts.append(t)
        for rt in remain_txts:
            assertion_failures.append(_make_defect(
                equip_id=rt.object_id or rt.text_id,
                defect_type="编辑断言失败",
                description=f"delete_switch_00024: 标注[{rt.content}]仍与 00024 关联",
                suggestion="请移除或修正 00024 标注",
            ))
        # 连接：exact target_id in refs/devices
        remain_conns = []
        for c in doc_after.connections:
            ref_hit = any(t in c.glink_refs for t in target_ids)
            dev_hit = (c.start_device_id in target_ids) or (c.end_device_id in target_ids)
            if ref_hit or dev_hit:
                remain_conns.append(c)
        for rc in remain_conns:
            assertion_failures.append(_make_defect(
                equip_id=rc.connection_id,
                defect_type="编辑断言失败",
                description=f"delete_switch_00024: 连接 [{rc.connection_id}] 仍引用 00024",
                suggestion="请清理连接的 GLink_Ref 或直接删除旧连接",
            ))

        # 2) 两侧原设备现在直连
        neighbors_before: set[str] = set()
        if target_dev is not None:
            tid = target_dev.element_id
            for conn in doc_before.connections:
                refs = list(conn.glink_refs) + [conn.start_device_id, conn.end_device_id]
                if tid in refs:
                    for r in refs:
                        if r and r != tid and doc_before.get_device_by_id(r):
                            neighbors_before.add(r)
            nb_list = list(neighbors_before)
            found_direct = False
            for i in range(len(nb_list)):
                for j in range(i + 1, len(nb_list)):
                    a, b = nb_list[i], nb_list[j]
                    # exact match
                    for conn in doc_after.connections:
                        refs = set(conn.glink_refs) | {conn.start_device_id, conn.end_device_id}
                        if a in refs and b in refs:
                            found_direct = True
                            break
                    if found_direct:
                        break
                if found_direct:
                    break
            if not found_direct and nb_list:
                assertion_failures.append(_make_defect(
                    equip_id="00024",
                    defect_type="编辑断言失败",
                    description=f"delete_switch_00024: 删除后原邻居设备 {nb_list} 之间未形成直接连接",
                    suggestion="请补画两侧原设备之间的直接连接线",
                ))

    all_defects = new_defects + assertion_failures
    summary = {
        "action": action,
        "pre_total": pre_sum["total_defects"],
        "post_total": post_sum["total_defects"],
        "new_defect_count": len(new_defects),
        "assertion_failure_count": len(assertion_failures),
        "assertions_passed": len(assertion_failures) == 0,
        "total_defects": len(all_defects),
        "pre_summary": pre_sum,
        "post_summary": post_sum,
    }
    return all_defects, summary


def validate_rendered_svg(svg_path: str) -> Tuple[list, dict]:
    """针对 Task 阶段3 增加：校验渲染后的 SVG 文件质量。
    
    检查项：
    1. 是否存在坐标为 (0,0) 的关键图元 (解决解析缺失问题)
    2. 是否存在层间坐标大范围偏移 (解决拓扑断裂问题)
    3. 设备重叠率是否超标
    4. 图元是否超出 viewBox 范围
    """
    doc = SvgDocument(svg_path)
    if not doc.parse():
        return [], {"error": "Parse failed"}
    
    defects = []
    
    # 1. (0,0) 坐标检查
    for elem in doc.elements:
        if elem.layer_name in ("ACLineSegment", "BusbarSection") and abs(elem.x) < 0.001 and abs(elem.y) < 0.001:
            defects.append(_make_defect(
                equip_id=elem.element_id,
                defect_type="渲染-坐标缺失",
                description=f"层[{elem.layer_name}] 图元坐标为(0,0)，疑似解析或渲染丢失",
                suggestion="请检查 SvgReader 对 polyline/polygon points 的解析逻辑"
            ))

    # 2. 层间坐标一致性检查
    layer_bounds = {}
    for elem in doc.elements:
        ln = elem.layer_name
        if ln not in layer_bounds: layer_bounds[ln] = [float('inf'), float('inf'), -float('inf'), -float('inf')]
        b = layer_bounds[ln]
        b[0] = min(b[0], elem.x); b[1] = min(b[1], elem.y)
        b[2] = max(b[2], elem.x + elem.width); b[3] = max(b[3], elem.y + elem.height)
    
    if "ACLineSegment" in layer_bounds and "LoadBreakSwitch" in layer_bounds:
        l1, l2 = layer_bounds["ACLineSegment"], layer_bounds["LoadBreakSwitch"]
        # 如果 X 范围完全不交叠且相差很大
        if l1[2] < l2[0] - 100 or l2[2] < l1[0] - 100:
            defects.append(_make_defect(
                equip_id="GLOBAL",
                defect_type="渲染-拓扑断裂",
                description=f"线路层 X=[{l1[0]:.1f},{l1[2]:.1f}] 与开关层 X=[{l2[0]:.1f},{l2[2]:.1f}] 严重脱节，相差超过 100 单位",
                suggestion="请检查 SvgBeautifier 布局算法是否漏掉了某些图层"
            ))

    # 3. 越界检查
    vb = doc.viewbox
    if vb:
        vbx1, vby1, vbx2, vby2 = vb[0], vb[1], vb[0]+vb[2], vb[1]+vb[3]
        for elem in doc.elements:
            if elem.x < vbx1 - 50 or elem.y < vby1 - 50 or (elem.x + elem.width) > vbx2 + 50 or (elem.y + elem.height) > vby2 + 50:
                defects.append(_make_defect(
                    equip_id=elem.element_id,
                    defect_type="渲染-图元越界",
                    description=f"图元 {elem.element_id} 坐标 ({elem.x:.1f},{elem.y:.1f}) 超出 viewBox 范围",
                    suggestion="请优化 viewBox 计算逻辑或布局范围"
                ))

    summary = {
        "total_rendered_defects": len(defects),
        "layers_checked": list(layer_bounds.keys()),
        "viewbox": vb
    }
    return defects, summary


# ----------------------------------------------------------------------
# 4) 报告导出
# ----------------------------------------------------------------------
def export_defect_report(defects: list, summary: dict, out_path: str):
    """导出缺陷报告 JSON（顶级为 list），summary 写入同路径 _summary.json。"""
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(defects, f, ensure_ascii=False, indent=2)
    base, ext = os.path.splitext(out_path)
    sum_path = f"{base}_summary{ext}"
    with open(sum_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"  缺陷报告已导出: {out_path} ({len(defects)} 条)")
    print(f"  汇总报告已导出: {sum_path}")

class TopoDbValidator:
    def __init__(self, topo: TopologyGraph):
        self.topo = topo
        self.G = topo.graph
        self.source_equip_ids = set(topo.get_all_source_equip())
        self.source_point_ids = set()
        # 收集电源设备下属全部端子
        for src_eid in self.source_equip_ids:
            pts = self.topo.get_device_all_points(src_eid)
            self.source_point_ids.update(pts)

    def _is_tie_switch_candidate(self, dev, feeder_set: set):
        """判断设备是否是联络开关候选，读取constants豁免规则"""
        equip_type = dev.equip_type or ""
        equip_name = dev.equip_name or ""
        # 类型豁免
        if equip_type in TERMINAL_EXEMPT_TYPES:
            return False
        # 名称关键字豁免
        for ban_key in TIE_EXCLUDE_NAME_KEYS:
            if ban_key in equip_name:
                return False
        # 跨至少2个馈线
        if len(feeder_set) < 2:
            return False
        # 开关类型
        if equip_type in NON_TERMINAL_SWITCH_TYPES:
            return True
        return False

    def detect_cycle_based_loop(self, trace_uuid: str):
        """基于nx.cycle_basis完整环路检测：区分计划联络环 / 非计划合环"""
        graph = self.G
        for comp_nodes in nx.connected_components(graph):
            subg = graph.subgraph(comp_nodes).copy()
            cycle_list = nx.cycle_basis(subg)
            for one_cycle in cycle_list:
                # one_cycle: list[point_id] 端子ID
                dev_id_set = set()
                feeder_set = set()
                dev_info_map = {}
                for point_id in one_cycle:
                    cp = self.topo.point_map.get(point_id)
                    if cp is None:
                        continue
                    dev_id = cp.belong_equip_id
                    dev_id_set.add(dev_id)
                    if cp.feeder_id:
                        feeder_set.add(cp.feeder_id)
                    dev_info_map[dev_id] = self.topo.device_map.get(dev_id)
                if not dev_id_set:
                    continue

                # 遍历环内所有设备，找联络开关候选
                has_tie_candidate = False
                tie_equip_id = None
                for eid in dev_id_set:
                    d = dev_info_map.get(eid)
                    if d is None:
                        continue
                    if self._is_tie_switch_candidate(d, feeder_set):
                        has_tie_candidate = True
                        tie_equip_id = eid
                        break

                if has_tie_candidate:
                    # 计划联络环：存在联络开关候选 → 标记为待复核
                    dev = dev_info_map[tie_equip_id]
                    item = TieLoopItem(
                        trace_uuid=trace_uuid,
                        equip_id=tie_equip_id,
                        point_id=",".join(one_cycle[:5]),
                        line_id=None,
                        result_type="疑似联络环(需复核)",
                        rule_code=R_TIE_001,
                        rule_desc="检测到计划联络环，需要复核开关实际遥信状态",
                        detail=f"环路跨馈线:{list(feeder_set)}，环内存在联络开关候选：{tie_equip_id}[{dev.equip_name or ''}]",
                        switch_status=None,
                        risk_level="中",
                        review_required=True,
                        left_feeder=next(iter(feeder_set)) if len(feeder_set)>=1 else None,
                        right_feeder=list(feeder_set)[1] if len(feeder_set)>=2 else None,
                        is_planned_loop=True
                    )
                    self.topo.tie_loop_list.append(item)
                else:
                    # 无联络开关：非计划合环故障
                    item = TieLoopItem(
                        trace_uuid=trace_uuid,
                        equip_id=",".join(list(dev_id_set)[:3]),
                        point_id=",".join(one_cycle[:5]),
                        line_id=None,
                        result_type="非计划合环",
                        rule_code=R_LOOP_001,
                        rule_desc="非计划合环，环路内无合法联络开关",
                        detail=f"环路跨馈线:{list(feeder_set)}，环内设备:{list(dev_id_set)[:4]}",
                        switch_status=None,
                        risk_level="高",
                        review_required=True,
                        is_planned_loop=False
                    )
                    self.topo.tie_loop_list.append(item)    

    def find_all_connected_components(self) -> list[set]:
        """获取全部连通分量，只保留端子节点TERMINAL_ID"""
        comps = []
        for comp in nx.connected_components(self.G):
            term_comp = {n for n in comp if n in self.topo.point_map}
            if len(term_comp) > 0:
                comps.append(term_comp)
        return comps

    def _get_feeder_of_terminal(self, term_id: str) -> Optional[str]:
        """获取端子所属馈线"""
        pt = self.topo.point_map.get(term_id)
        if pt:
            return pt.feeder_id
        return None

    def _get_component_equip_and_feeder(self, comp: set):
        """返回该分量：设备集合、馈线集合"""
        equip_set = set()
        feed_set = set()
        for pid in comp:
            pt = self.topo.point_map[pid]
            eid = pt.belong_equip_id
            equip_set.add(eid)
            if pt.feeder_id:
                feed_set.add(pt.feeder_id)
        return equip_set, feed_set

    def detect_hanging_terminal(self, trace_uuid: str):
        """R001 端子悬空：非末端开关设备端子数量不符合要求；末端设备豁免"""
        deg_map = dict(self.G.degree())
        equip_term_cnt = defaultdict(int)
        for pid, pt in self.topo.point_map.items():
            equip_term_cnt[pt.belong_equip_id] += 1

        for equip_id, dev in self.topo.device_map.items():
            if equip_id in self.source_equip_ids:
                continue
            n_terms = equip_term_cnt.get(equip_id, 0)
            dev_type = dev.equip_type or ""
            dev_name = dev.equip_name or ""

            # R_TIE_EXCLUDE_001：末端设备豁免（配变、用户，允许单端子）
            if dev_type in TERMINAL_EXEMPT_TYPES:
                continue
            # 测试设备标记待复核
            if any(k in dev_name for k in TEST_LINE_KEYS):
                    item = AbnormalItem(
                        trace_uuid=trace_uuid,
                        equip_id=equip_id,
                        point_id="",
                        line_id=None,
                        rule_code=R001,
                        rule_desc="测试/虚拟设备，待人工复核",
                        check_result=REVIEW,
                        review_status="待复核",
                        detail=f"设备{equip_id}[{dev_name}]命中测试关键字，跳过自动判定，需人工复核",
                        dimension="拓扑完整性",
                        risk_level="低"
                    )
                    self.topo.abnormal_list.append(item)
                    continue

            # 开关类设备要求2个端子
            if dev_type in NON_TERMINAL_SWITCH_TYPES:
                if n_terms == 1:
                    item = AbnormalItem(
                        trace_uuid=trace_uuid,
                        equip_id=equip_id,
                        point_id="",
                        line_id=None,
                        rule_code=R001,
                        rule_desc="开关设备单端悬空，端子数量不足",
                        check_result=ERR,
                        review_status="待复核",
                        detail=f"开关设备{equip_id}[{dev_name}]仅有{n_terms}个端子，需要2个有效端子",
                        dimension="拓扑完整性",
                        risk_level="中"
                    )
                    self.topo.abnormal_list.append(item)
                elif n_terms == 0:
                    item = AbnormalItem(
                        trace_uuid=trace_uuid,
                        equip_id=equip_id,
                        point_id="",
                        line_id=None,
                        rule_code=R001,
                        rule_desc="开关设备无任何端子，完全悬空",
                        check_result=ERR,
                        review_status="待复核",
                        detail=f"开关设备{equip_id}[{dev_name}]未关联任何端子",
                        dimension="拓扑完整性",
                        risk_level="高"
                    )
                    self.topo.abnormal_list.append(item)

    def detect_island_no_source(self, trace_uuid: str):
        """R002 孤岛：连通分量不含任何电源端子"""
        comps = self.find_all_connected_components()
        for comp in comps:
            if comp & self.source_point_ids:
                continue
            equip_set, _ = self._get_component_equip_and_feeder(comp)
            comp_size = len(comp)
            first_equip = next(iter(equip_set))
            first_pt = next(iter(comp))
            item = BreakpointItem(
                trace_uuid=trace_uuid,
                equip_id=first_equip,
                point_id=first_pt,
                line_id=None,
                component_size=comp_size,
                rule_code=R002,
                rule_desc="拓扑孤岛，该连通分量无供电电源",
                detail=f"本连通分量包含{comp_size}个端子，共{len(equip_set)}台设备，未连通到任何电源设备",
                check_result=ERR,
                dimension="拓扑完整性"
            )
            self.topo.breakpoint_list.append(item)

    def detect_feed_breakpoint(self, trace_uuid: str):
        """R003 馈线断点：同一馈线端子分布在多个连通分量"""
        feed_2_points = defaultdict(set)
        for pid, pt in self.topo.point_map.items():
            fid = pt.feeder_id
            if not fid:
                continue
            feed_2_points[fid].add(pid)

        all_comps = self.find_all_connected_components()
        for feed_id, point_set in feed_2_points.items():
            comp_tag_set = set()
            for comp in all_comps:
                inter = point_set & comp
                if len(inter) > 0:
                    comp_tag_set.add(id(comp))
            if len(comp_tag_set) >= 2:
                item = BreakpointItem(
                    trace_uuid=trace_uuid,
                    equip_id="",
                    point_id="",
                    line_id=None,
                    component_size=len(point_set),
                    rule_code=R003,
                    rule_desc=f"馈线{feed_id}存在断点，拓扑分割为{len(comp_tag_set)}个独立区域",
                    detail=f"馈线{feed_id}内设备端子分散在{len(comp_tag_set)}个互不连通分量，存在断线或开关分断",
                    check_result=ERR,
                    dimension="拓扑完整性"
                )
                self.topo.breakpoint_list.append(item)

    def detect_tie_and_suspect_tie(self, trace_uuid: str):
        """R_TIE_EXCLUDE_001 / R_TIE_001 / R_TIE_002：联络开关、疑似联络识别"""
        comp_map = {}
        for comp in self.find_all_connected_components():
            for pid in comp:
                comp_map[pid] = comp

        for equip_id, dev in self.topo.device_map.items():
            dev_name = dev.equip_name or ""
            dev_type = dev.equip_type or ""
            term_ids = self.topo.get_device_all_points(equip_id)

            # R_TIE_EXCLUDE_001：末端对象直接排除联络识别
            if any(k in dev_name for k in TIE_EXCLUDE_NAME_KEYS):
                continue
            # 只处理开关类设备，端子数量必须等于2
            if dev_type not in NON_TERMINAL_SWITCH_TYPES or len(term_ids) != 2:
                continue

            t1, t2 = term_ids[0], term_ids[1]
            f1 = self._get_feeder_of_terminal(t1)
            f2 = self._get_feeder_of_terminal(t2)

            feeder_set = set()
            if f1:
                feeder_set.add(f1)
            if f2:
                feeder_set.add(f2)
            # 命中豁免/不满足联络候选条件，直接跳过，不生成告警
            if not self._is_tie_switch_candidate(dev, feeder_set):
                continue

            # 两侧馈线至少有一个为空 → 信息缺失，标记疑似联络待复核
            if not f1 or not f2:
                item = TieLoopItem(
                    trace_uuid=trace_uuid,
                    equip_id=equip_id,
                    point_id=",".join(term_ids),
                    line_id=None,
                    result_type="疑似联络",
                    rule_code=R_TIE_002,
                    rule_desc="疑似联络开关，馈线信息缺失，需人工复核",
                    detail=f"设备{equip_id}[{dev_name}]为开关，端子馈线信息不全：馈线A={f1},馈线B={f2}",
                    switch_status=None,
                    risk_level="中",
                    review_required=True,
                    left_feeder=f1,
                    right_feeder=f2,
                    is_planned_loop=False
                )
                self.topo.tie_loop_list.append(item)
                continue

            # 两侧馈线相同：不属于联络
            if f1 == f2:
                continue

            # 两侧馈线不同，联络候选
            sw_status = self.topo.switch_state_map.get(equip_id, "close")
            st_source = self.topo.switch_state_source.get(equip_id, "default_rule")

            if sw_status in {"合位", "close"}:
                 # 合位 → 进一步进入合环风险检查
                self._check_loop_for_switch(equip_id, term_ids, trace_uuid)
                tie_result = "联络"
                rule = R_TIE_001
                desc = f"合规联络开关，跨两条馈线，开关处于{sw_status}，状态来源:{st_source}"
            elif sw_status in {"分位", "open"}:
                tie_result = "联络"
                rule = R_TIE_001
                desc = f"合规联络开关，跨两条馈线，开关处于{sw_status}，状态来源:{st_source}"
            else:
                # 状态未知、无效 → 疑似联络待复核
                item = TieLoopItem(
                    trace_uuid=trace_uuid,
                    equip_id=equip_id,
                    point_id=",".join(term_ids),
                    line_id=None,
                    result_type="疑似联络",
                    rule_code=R_TIE_002,
                    rule_desc="疑似联络开关，开关遥信状态未知，待人工复核",
                    detail=(
                        f"设备{equip_id}[{dev_name}]跨馈线 {f1} / {f2}，"
                        f"开关状态[{sw_status}]，状态来源:{st_source}。"
                        f"{'【提示】本结果由赛题默认规则推演，建议人工复核' if st_source == 'default_rule' else ''}"
                    ),
                    switch_status=sw_status,
                    risk_level="中",
                    review_required=(st_source == "default_rule"), # 默认推演标记待复核
                    left_feeder=f1,
                    right_feeder=f2,
                    is_planned_loop=False
                )
                self.topo.tie_loop_list.append(item)
                continue

            item = TieLoopItem(
                trace_uuid=trace_uuid,
                equip_id=equip_id,
                point_id=",".join(term_ids),
                line_id=None,
                result_type=tie_result,
                rule_code=rule,
                rule_desc=desc,
                detail=(
                    f"设备{equip_id}[{dev_name}]，跨馈线 {f1} / {f2}，"
                    f"开关状态：{sw_status}，状态来源:{st_source}。"
                    f"{'【提示】本结果由赛题默认规则推演，建议人工复核' if st_source == 'default_rule' else ''}"
                ),
                switch_status=sw_status,
                risk_level="中",
                review_required=(st_source == "default_rule"),
                left_feeder=f1,
                right_feeder=f2,
                is_planned_loop=False
            )
            self.topo.tie_loop_list.append(item)

    def _check_loop_for_switch(self, equip_id: str, term_ids: list, trace_uuid: str):
        """R_LOOP_001：开关合位，检测是否产生多电源非计划合环"""
        visited_comp = set()
        sw_status = self.topo.switch_state_map.get(equip_id, "close")
        st_source = self.topo.switch_state_source.get(equip_id, "default_rule")
        for tid in term_ids:
            comp = None
            for c in self.find_all_connected_components():
                if tid in c:
                    comp = c
                    break
            if comp is None:
                continue
            comp_key = id(comp)
            if comp_key in visited_comp:
                continue
            visited_comp.add(comp_key)
            equip_set, _ = self._get_component_equip_and_feeder(comp)
            src_in_comp = equip_set & self.source_equip_ids
            src_cnt = len(src_in_comp)
            if src_cnt >= 2:
                src_list = ",".join(sorted(list(src_in_comp)))
                dev = self.topo.device_map[equip_id]
                item = TieLoopItem(
                    trace_uuid=trace_uuid,
                    equip_id=equip_id,
                    point_id=",".join(term_ids),
                    line_id=None,
                    result_type="非计划合环",
                    rule_code=R_LOOP_001,
                    rule_desc="检测到非计划合环，连通域包含多个电源设备",
                    detail=(
                        f"开关{equip_id}[{dev.equip_name or ''}]合位，环路包含电源：{src_list}，"
                        f"开关状态:{sw_status}，状态来源:{st_source}。"
                        f"{'【提示】本结果由赛题默认规则推演，建议人工复核' if st_source == 'default_rule' else ''}"
                    ),
                    switch_status=sw_status,   # ✅现在使用预处理得来的sw_status
                    risk_level="高",
                    review_required=(st_source == "default_rule"),
                    source_count=src_cnt,
                    is_planned_loop=False
                )
                self.topo.tie_loop_list.append(item)

    def _post_filter_tie_loop_items(self):
        """成员函数：全局去重，消除两套算法重复输出同一设备"""
        seen = set()
        final_list = []
        for item in self.topo.tie_loop_list:
            key = f"{item.equip_id}__{item.result_type}"
            if key in seen:
                continue
            seen.add(key)
            final_list.append(item)
        self.topo.tie_loop_list = final_list

    def run_all_db_check(self, trace_uuid: str = "DB_TOPO_001"):
        """全套数据库拓扑检测入口"""
        self.topo.abnormal_list.clear()
        self.topo.breakpoint_list.clear()
        self.topo.tie_loop_list.clear()

        self.detect_hanging_terminal(trace_uuid)
        self.detect_island_no_source(trace_uuid)
        self.detect_feed_breakpoint(trace_uuid)
        self.detect_tie_and_suspect_tie(trace_uuid)
        self.detect_cycle_based_loop(trace_uuid)
        self._post_filter_tie_loop_items()
        return self.topo.abnormal_list, self.topo.breakpoint_list, self.topo.tie_loop_list


def run_database_topo_check(topo: TopologyGraph, trace_id="DB_TOPO_001"):
    """对外调用入口，供topology_builder.py调用"""
    validator = TopoDbValidator(topo)
    abn, brk, tie = validator.run_all_db_check(trace_uuid=trace_id)
    return abn, brk, tie
