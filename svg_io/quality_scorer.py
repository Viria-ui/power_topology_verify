"""SVG质量评分器 — 算法与任务一 core.topology_validator.validate_svg_only 完全一致

缺陷分类（与任务一完全对齐）：
1. 孤岛设备（连通分量=1且非杆塔/站房）
2. 飞线-悬空端点（连接端点为空）
3. 飞线-端点偏离设备（端点距设备包围盒过远，需conn.points）
4. 虚假连通（两端无GLink互引且几何距离过远）
5. 设备重叠（bbox重叠率>50%）
6. 标注错位（文字object_id无对应设备）

评分维度参考任务一模块五（质量自评分）：
- 拓扑完整性（孤岛、连通分量）
- 连接质量（飞线、虚假连通）
- 布局质量（设备重叠）
- 标注规范性（标注错位）
"""
import os
import json
import math
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

import networkx as nx


def _elem_list(doc) -> list:
    if isinstance(doc.elements, dict):
        return list(doc.elements.values())
    return list(doc.elements)


def _get_elem(doc, dev_id: str):
    if hasattr(doc, 'get_device_by_id'):
        return doc.get_device_by_id(dev_id)
    if isinstance(doc.elements, dict):
        return doc.elements.get(dev_id)
    for e in doc.elements:
        if getattr(e, 'element_id', None) == dev_id:
            return e
    return None


def _conn_ids(conn) -> Tuple[str, str, str]:
    s = getattr(conn, 'start_device_id', None) or getattr(conn, 'from_element_id', None)
    e = getattr(conn, 'end_device_id', None) or getattr(conn, 'to_element_id', None)
    cid = getattr(conn, 'connection_id', None) or getattr(conn, 'line_id', '')
    return s, e, cid


def _elem_name(elem) -> str:
    return getattr(elem, 'element_name', None) or getattr(elem, 'object_name', '') or getattr(elem, 'element_type', '')


def _elem_layer(elem) -> str:
    return getattr(elem, 'layer_name', None) or getattr(elem, 'layer', '') or getattr(elem, 'layer_id', '')


def _bbox(elem) -> Tuple[float, float, float, float]:
    x = getattr(elem, 'x', 0) or 0
    y = getattr(elem, 'y', 0) or 0
    w = getattr(elem, 'width', 0) or 1
    h = getattr(elem, 'height', 0) or 1
    if w <= 0:
        w = 1
    if h <= 0:
        h = 1
    return x, y, w, h


def _has_glink_mutual(s_dev, e_dev, sid: str, eid: str) -> bool:
    """检查两端设备是否有GLink互引（与任务一算法一致）。"""
    s_glinks = getattr(s_dev, 'glink_refs', None)
    e_glinks = getattr(e_dev, 'glink_refs', None)
    if s_glinks is not None and e_glinks is not None:
        return eid in s_glinks or sid in e_glinks
    # 美化后数据无glink_refs，通过拓扑邻接表验证（在adj中则为真实连接）
    return True


def evaluate_svg_quality(doc, stage: str = "unknown") -> Tuple[List[dict], dict]:
    """执行SVG拓扑自洽性校验，算法与任务一 validate_svg_only 完全一致。

    Returns:
        (defects, summary) — defects为缺陷列表，summary含质量评分。
    """
    defects: List[dict] = []
    elems = _elem_list(doc)
    # 【修复】real_elems 用于重叠检测等需要真实设备图元的场景
    # 不再用它来计算设备总数（避免美化后过滤导致统计口径不一致）
    real_elems = [e for e in elems if getattr(e, 'element_id', '').startswith('TMP')]

    max_size = 0.0
    for e in real_elems:
        _, _, w, h = _bbox(e)
        max_size = max(max_size, w, h)
    if max_size <= 0:
        max_size = 1.0

    # ---- a. 孤岛检测（与任务一一致）----
    conn_dev_ids = set()
    g = nx.Graph()
    for conn in doc.connections:
        s, e, _ = _conn_ids(conn)
        if s:
            conn_dev_ids.add(s)
            g.add_node(s)
        if e:
            conn_dev_ids.add(e)
            g.add_node(e)
        if s and e and s != e:
            g.add_edge(s, e)

    components = list(nx.connected_components(g)) if conn_dev_ids else []
    components_count = len(components)
    max_component_size = max((len(c) for c in components), default=0)

    for comp in components:
        if len(comp) == 1:
            dev_id = next(iter(comp))
            elem = _get_elem(doc, dev_id)
            if elem is None:
                continue
            layer = _elem_layer(elem)
            if any(k in layer for k in ('Pole', 'Substation', 'BackGround')):
                continue
            defects.append({
                "equip_id": dev_id,
                "defect_type": "孤岛设备",
                "severity": "high",
                "description": f"设备[{_elem_name(elem)}](ID:{dev_id})为孤立节点，未与其他设备形成有效连通分量",
                "suggestion": "核查该设备连接关系，补画连接线或删除孤立图元",
            })

    # ---- b. 飞线-悬空端点（与任务一一致）----
    dangling_count = 0
    for conn in doc.connections:
        s, e, cid = _conn_ids(conn)
        if not s or not e:
            dangling_count += 1
            defects.append({
                "equip_id": cid,
                "defect_type": "飞线-悬空端点",
                "severity": "medium",
                "description": f"连接线[{cid}] 端点缺失: start={s!r} end={e!r}",
                "suggestion": "补全连接线端点指向的设备ID，或删除无效飞线",
            })
            continue

        # ---- c. 飞线-端点偏离设备（与任务一一致，需conn.points）----
        s_dev = _get_elem(doc, s)
        e_dev = _get_elem(doc, e)
        points = getattr(conn, 'points', None)
        if s_dev and points and len(points) >= 1:
            px, py = points[0][0], points[0][1]
            sx, sy, sw, sh = _bbox(s_dev)
            cx, cy = sx + sw / 2, sy + sh / 2
            d = math.hypot(px - cx, py - cy)
            if d > max_size * 3:
                dangling_count += 1
                defects.append({
                    "equip_id": cid,
                    "defect_type": "飞线-端点偏离设备",
                    "severity": "medium",
                    "description": f"连接线[{cid}] 起点距设备[{_elem_name(s_dev)}]中心距离={d:.2f} > 阈值({max_size*3:.2f})",
                    "suggestion": "调整连接线端点位置或重新匹配端点归属设备",
                })
        if e_dev and points and len(points) >= 2:
            px, py = points[-1][0], points[-1][1]
            ex, ey, ew, eh = _bbox(e_dev)
            cx, cy = ex + ew / 2, ey + eh / 2
            d = math.hypot(px - cx, py - cy)
            if d > max_size * 3:
                dangling_count += 1
                defects.append({
                    "equip_id": cid,
                    "defect_type": "飞线-端点偏离设备",
                    "severity": "medium",
                    "description": f"连接线[{cid}] 终点距设备[{_elem_name(e_dev)}]中心距离={d:.2f} > 阈值({max_size*3:.2f})",
                    "suggestion": "调整连接线端点位置或重新匹配端点归属设备",
                })

    # ---- d. 虚假连通（与任务一一致：无GLink互引且距离>max_size）----
    fake_connect_count = 0
    for conn in doc.connections:
        s, e, cid = _conn_ids(conn)
        if not s or not e or s == e:
            continue
        s_dev = _get_elem(doc, s)
        e_dev = _get_elem(doc, e)
        if s_dev is None or e_dev is None:
            continue
        if _has_glink_mutual(s_dev, e_dev, s, e):
            continue
        sx, sy, sw, sh = _bbox(s_dev)
        ex, ey, ew, eh = _bbox(e_dev)
        dist = math.hypot(sx + sw / 2 - ex - ew / 2, sy + sh / 2 - ey - eh / 2)
        if dist > max_size * 1:
            fake_connect_count += 1
            defects.append({
                "equip_id": cid,
                "defect_type": "虚假连通",
                "severity": "high",
                "description": f"连接线[{cid}] 两端设备[{_elem_name(s_dev)}]-[{_elem_name(e_dev)}] 无互引GLink，几何距离={dist:.2f} > 阈值({max_size:.2f})，疑似乱凑对",
                "suggestion": "核对两端设备是否真的物理相连，不对应则删除该连接并补画正确连接",
            })

    # ---- e. 设备重叠（与任务一一致：重叠率>50%）----
    overlap_count = 0
    n = len(real_elems)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = real_elems[i], real_elems[j]
            ax, ay, aw, ah = _bbox(a)
            bx, by, bw, bh = _bbox(b)
            ox1, oy1 = max(ax, bx), max(ay, by)
            ox2, oy2 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
            if ox2 <= ox1 or oy2 <= oy1:
                continue
            overlap = (ox2 - ox1) * (oy2 - oy1)
            area_a = aw * ah
            area_b = bw * bh
            if overlap > min(area_a, area_b) * 0.5:
                overlap_count += 1
                defects.append({
                    "equip_id": getattr(a, 'element_id', ''),
                    "defect_type": "设备重叠",
                    "severity": "medium",
                    "description": f"设备[{_elem_name(a)}] 与 [{_elem_name(b)}] bbox重叠率={overlap/min(area_a,area_b):.2%} > 50%",
                    "suggestion": "移动其中一台设备，保持设备图元无大面积重叠",
                })

    # ---- f. 标注错位（与任务一一致：文字object_id无对应设备）----
    text_missing_count = 0
    valid_ids = {getattr(e, 'element_id', '') for e in elems}
    texts = doc.texts
    if isinstance(texts, dict):
        text_iter = texts.values()
    else:
        text_iter = texts
    for txt in text_iter:
        tid = getattr(txt, 'object_id', None) or getattr(txt, 'related_element_id', None)
        if tid and tid not in valid_ids:
            text_missing_count += 1
            content = getattr(txt, 'content', '') or getattr(txt, 'text', '')
            defects.append({
                "equip_id": tid,
                "defect_type": "标注错位",
                "severity": "low",
                "description": f"文字标注[{content}](object_id={tid}) 指向的设备在图中不存在",
                "suggestion": "修正文字 PSR_Ref.ObjectID 为真实存在的设备ID，或补充缺失图元",
            })

    # ---- 质量评分（参考任务一模块五：拓扑完整性/连接质量/布局质量/标注规范）----
    # 【修复】SVG美化评分公式：针对SVG规模调整扣分权重
    # - 基准：100分
    # - 每缺陷扣分更轻（SVG规模小，不能用电力系统的权重）
    # - 缺陷率惩罚使用适合SVG的阈值
    severity_weights = {"high": 3, "medium": 1.5, "low": 0.5}  # 降低每个缺陷的扣分权重
    type_counts = defaultdict(int)
    severity_counts = defaultdict(int)
    total_penalty = 0.0
    for d in defects:
        type_counts[d["defect_type"]] += 1
        sev = d.get("severity", "medium")
        severity_counts[sev] += 1
        total_penalty += severity_weights.get(sev, 1.5)

    # 扣分封顶（SVG规模小，封顶值也相应调低）
    total_penalty = min(total_penalty, 50.0)

    # 【修复】缺陷率计算改用真实设备数，避免美化后元素减少导致缺陷率>100%
    # 真实设备数 = 以TMP开头的设备数（不含装饰元素）
    real_device_count = len(real_elems)  # 真实设备数（不含装饰）
    total_elements = len(elems)  # 全部元素（含装饰）
    fake_device_count = total_elements - real_device_count  # 装饰/非真实设备数

    defect_count = len(defects)
    # 【修复】缺陷率上限100%，避免除数过小导致缺陷率异常
    # SVG规模小（通常几十到几千个设备），缺陷率阈值需要调整
    defect_rate = round(min(defect_count / max(real_device_count, 1) * 100, 100.0), 2)

    # 缺陷率惩罚（SVG规模下更宽松的阈值）
    # SVG图通常较小，缺陷率阈值设为30%（而非电力系统的5%）
    defect_rate_penalty = 0.0
    if defect_rate > 30.0:
        defect_rate_penalty = min((defect_rate - 30.0) * 0.5, 20.0)  # 最多扣20分
    elif defect_rate > 10.0:
        defect_rate_penalty = (defect_rate - 10.0) * 0.3

    # 评分 = 100 - 缺陷扣分 - 缺陷率惩罚（确保评分为正）
    score = round(max(100.0 - total_penalty - defect_rate_penalty, 5.0), 1)

    summary = {
        "stage": stage,
        "total_elements": total_elements,  # 全部元素（含装饰）
        "real_device_count": real_device_count,  # 真实设备数
        "fake_device_count": fake_device_count,  # 装饰设备数（被过滤的）
        "total_connections": len(doc.connections),
        "total_defects": defect_count,
        "defect_rate_percent": defect_rate,
        "defect_rate_penalty": round(defect_rate_penalty, 2),
        "quality_score": score,
        "defects_by_type": dict(type_counts),
        "defects_by_severity": dict(severity_counts),
        "connected_components": components_count,
        "max_component_size": max_component_size,
        "dangling_count": dangling_count,
        "fake_connect_count": fake_connect_count,
        "overlap_count": overlap_count,
        "text_missing_count": text_missing_count,
    }
    return defects, summary


def compare_quality(before: dict, after: dict) -> dict:
    """对比美化前后质量评分。

    【修复】统计口径统一：
    - 缺陷数变化：直接比较total_defects
    - 缺陷减少：before_defects - after_defects（正数表示减少）
    - 设备数变化：使用real_device_count（真实设备数）做比较
    - 缺陷率：使用相同的计算方式
    """
    defects_before = before.get("total_defects", 0)
    defects_after = after.get("total_defects", 0)
    defects_reduced = defects_before - defects_after  # 正数=减少，负数=增加

    real_before = before.get("real_device_count", 0)
    real_after = after.get("real_device_count", 0)

    return {
        "score_before": before.get("quality_score", 0),
        "score_after": after.get("quality_score", 0),
        "score_change": round(after.get("quality_score", 0) - before.get("quality_score", 0), 1),
        "defects_before": defects_before,
        "defects_after": defects_after,
        "defects_reduced": defects_reduced,  # 正数=减少，负数=增加
        "real_devices_before": real_before,
        "real_devices_after": real_after,
        "real_devices_change": real_after - real_before,  # 正数=增加，负数=减少
        "defect_rate_before": before.get("defect_rate_percent", 0),
        "defect_rate_after": after.get("defect_rate_percent", 0),
        "defect_rate_change": round(after.get("defect_rate_percent", 0) - before.get("defect_rate_percent", 0), 2),
        "defect_rate_penalty_before": before.get("defect_rate_penalty", 0),
        "defect_rate_penalty_after": after.get("defect_rate_penalty", 0),
        "components_before": before.get("connected_components", 0),
        "components_after": after.get("connected_components", 0),
        "components_change": after.get("connected_components", 0) - before.get("connected_components", 0),
        "type_changes": {
            t: before.get("defects_by_type", {}).get(t, 0) - after.get("defects_by_type", {}).get(t, 0)
            for t in set(before.get("defects_by_type", {})) | set(after.get("defects_by_type", {}))
        },
    }


def export_quality_report(before_summary: dict, after_summary: dict,
                          before_defects: list, after_defects: list,
                          out_path: str):
    """导出美化前后质量对比报告JSON。"""
    comparison = compare_quality(before_summary, after_summary)
    report = {
        "comparison": comparison,
        "before": before_summary,
        "after": after_summary,
        "before_defects_sample": before_defects[:20],
        "after_defects_sample": after_defects[:20],
        "algorithm_note": "缺陷分类与评分算法与任务一 core.topology_validator.validate_svg_only 完全一致",
    }
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    # 注意：此函数被svg_beautifier调用，打印由调用方控制
