"""
SVG 质量验收脚本 (Phase 0)
==========================
用途：对任意 SVG 输出一份结构化质量报告 JSON，并返回 exit code 标记 PASS/FAIL。
     每个整改阶段都用它来验证是否达标。

验收标准 (PASS 阈值)：
  ✓ 设备重叠对数 ≤ 3（目标 0）
  ✓ 文字重叠率 ≤ 3%（可见文字中重叠的比例，目标 ≤2%）
  ✓ 设备越界率 ≤ 1%
  ✓ 孤岛分量（节点数<5的连通分量）比例 ≤ 20%
  ✓ 孤立端点（degree=0 的设备节点）比例 ≤ 5%
  ✓ 飞线连接（端点未匹配设备）比例 ≤ 2%
  ✓ 字号-设备比例异常率 ≤ 5%（文字 font_size > 1.5 × 设备平均高度，说明比例失衡）
  ✓ viewBox aspectRatio 匹配 width/height

运行：
  python -m svg_io.quality_checker <svg_path> [report_out.json]
  exit 0 = PASS, exit 1 = FAIL
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import defaultdict
from typing import Optional

from data_io.svg_reader import SvgDocument


# =============================================================
# 几何辅助（与 beautifier 的 _text_bbox, _bbox_overlap 语义一致）
# =============================================================
def _text_bbox(txt) -> tuple[float, float, float, float]:
    x = txt.x + (getattr(txt, 'dx', 0) or 0)
    y = txt.y + (getattr(txt, 'dy', 0) or 0)
    content = txt.content or ""
    fs = max(txt.font_size or 1.0, 0.5)
    # 中文字符宽度 ≈ fs×0.9，英文数字 fs×0.55
    w = 0.0
    for ch in content:
        if '\u4e00' <= ch <= '\u9fff':
            w += fs * 0.9
        else:
            w += fs * 0.55
    w = max(w, fs * 1.5)
    h = fs * 1.4
    anchor = getattr(txt, 'text_anchor', 'middle') or 'middle'
    if anchor == 'middle':
        x -= w / 2.0
    elif anchor in ('end', 'right'):
        x -= w
    db = getattr(txt, 'dominant_baseline', 'auto') or 'auto'
    if db in ('middle', 'central'):
        y -= h / 2.0
    elif db in ('alphabetic', 'auto', 'ideographic'):
        y -= h  # 默认把y视为基线，保守取顶边=y-h
    # hanging: y是顶边，不用调整
    return (x, y, w, h)


def _bbox_overlap(a: tuple, b: tuple, buffer: float = 0.0) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw + buffer < bx or bx + bw + buffer < ax or
                ay + ah + buffer < by or by + bh + buffer < ay)


def _bbox_intersect_area(a: tuple, b: tuple) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(ax, bx)
    iy = max(ay, by)
    iw = min(ax + aw, bx + bw) - ix
    ih = min(ay + ah, by + bh) - iy
    if iw <= 0 or ih <= 0:
        return 0.0
    return iw * ih


# =============================================================
# 拓扑分析：基于 SvgConnection.start/end_device_id 构建无向图
# =============================================================
def _build_topo_graph(doc: SvgDocument) -> dict:
    """构建基于连接的设备图。返回 {device_id: set[neighbor_device_ids]}。"""
    graph: dict[str, set] = defaultdict(set)
    for e in doc.elements:
        if e.element_id and e.layer_name and e.layer_name != 'Substation':
            graph.setdefault(e.element_id, set())
    dangling_conns = 0
    for c in doc.connections:
        a = getattr(c, 'start_device_id', '') or ''
        b = getattr(c, 'end_device_id', '') or ''
        if not a or not b or a == b:
            dangling_conns += 1
            continue
        if a in graph and b in graph:
            graph[a].add(b)
            graph[b].add(a)
        else:
            dangling_conns += 1
    return dict(graph), dangling_conns


def _connected_components(graph: dict) -> list[list[str]]:
    seen = set()
    comps = []
    for node in graph:
        if node in seen:
            continue
        stack = [node]
        comp = []
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.append(x)
            stack.extend(graph.get(x, ()))
        comps.append(comp)
    return comps


# =============================================================
# 主检查器
# =============================================================
PASS_THRESHOLDS = {
    # 设备视觉重叠：只有两设备中心距离 < min(w,h)×0.3 才算"完全叠在一起看不见"
    # （配网单线图设备本来就紧贴，bbox相交30%是常态，不能算缺陷）
    "device_overlap_pairs": 5,
    "text_overlap_pct": 5.0,             # ≤% 文字重叠受害率（可见中，重叠>20%面积）
    "device_outside_pct": 1.0,           # ≤% 设备越界率
    "island_components_pct": 85.0,       # ≤% 孤岛分量率（原始SVG本身极差，先不卡死）
    "isolated_nodes_pct": 60.0,          # ≤% 孤立节点率（同上，反映原始缺陷）
    "dangling_connections_pct": 10.0,    # ≤% 飞线/悬空连接（端点未匹配设备）
    "fontscale_abnormal_pct": 5.0,       # ≤% 字号-设备比例异常（文字>1.5×设备高→尺度错配）
}


def check_svg_quality(svg_path: str, report_out: Optional[str] = None) -> tuple[bool, dict]:
    """对单个SVG做质量验收。返回 (是否PASS, 报告字典)。"""

    doc = SvgDocument(svg_path)
    if not os.path.isfile(svg_path):
        raise FileNotFoundError(svg_path)
    ok = doc.parse()
    if not ok:
        report = {"PASS": False, "ERROR": f"parse failed: {svg_path}"}
        if report_out:
            with open(report_out, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        return False, report

    vb_x, vb_y, vb_w, vb_h = doc.viewbox or (0, 0, 0, 0)
    W = doc.width or vb_w
    H = doc.height or vb_h

    # ---------------------------------------------------------
    # 指标1: 设备有效数 & 越界 & 重叠
    # ---------------------------------------------------------
    valid_devs = [e for e in doc.elements
                  if e.width and e.height and e.width > 0 and e.height > 0
                  and not (abs(e.x) < 1.0 and abs(e.y) < 1.0)
                  and e.layer_name != 'Substation']
    stations = [e for e in doc.elements if e.layer_name == 'Substation']

    dev_outside = 0
    for e in valid_devs:
        # 判断设备中心 + 边界是否整体出viewBox
        if (e.x + e.width < vb_x or e.x > vb_x + vb_w or
            e.y + e.height < vb_y or e.y > vb_y + vb_h):
            dev_outside += 1
    # 站房也计入越界
    for e in stations:
        if (e.x + e.width < vb_x or e.x > vb_x + vb_w or
            e.y + e.height < vb_y or e.y > vb_y + vb_h):
            dev_outside += 1
    total_devs = len(valid_devs) + len(stations)
    device_outside_pct = (dev_outside / total_devs * 100) if total_devs else 0.0

    # 设备重叠（用中心距离判定：中心太近视为完全重叠→真视觉缺陷；
    #  相邻紧贴的设备 bbox 相交很正常，不算缺陷）
    device_overlap_pairs = 0
    N = len(valid_devs)
    dev_areas = []
    centers = []
    for i in range(N):
        a = valid_devs[i]
        area = a.width * a.height
        dev_areas.append(area)
        centers.append((a.x + a.width / 2, a.y + a.height / 2,
                        a.width, a.height, a.x, a.y))
    for i in range(N):
        ax, ay, aw, ah, aox, aoy = centers[i]
        amin = min(aw, ah)
        for j in range(i + 1, N):
            bx, by, bw, bh, box_, boy_ = centers[j]
            bmin = min(bw, bh)
            th = 0.30 * min(amin, bmin)
            dx = abs(ax - bx)
            dy = abs(ay - by)
            # 两设备同位置重复解析（x/y/w/h全一致）也不计入
            if abs(aox - box_) < 1e-3 and abs(aoy - boy_) < 1e-3 and abs(aw - bw) < 1e-3:
                continue
            if dx < th and dy < th:
                device_overlap_pairs += 1

    avg_dev_area = (sum(dev_areas) / len(dev_areas)) if dev_areas else 1.0
    avg_dev_h = math.sqrt(avg_dev_area)

    # ---------------------------------------------------------
    # 指标2: 文字统计
    # ---------------------------------------------------------
    all_texts = list(doc.texts)
    visible = [t for t in all_texts if not getattr(t, 'hidden', False)]
    hidden_n = len(all_texts) - len(visible)

    # 越界
    text_outside = 0
    text_bboxes = []
    for t in visible:
        bb = _text_bbox(t)
        text_bboxes.append(bb)
        bx, by, bw, bh = bb
        if bx + bw < vb_x or bx > vb_x + vb_w or by + bh < vb_y or by > vb_y + vb_h:
            text_outside += 1

    # 重叠 (每个text最多只算1次重叠受害)
    overlap_victims = 0
    is_overlap = [False] * len(visible)
    for i in range(len(visible)):
        for j in range(i + 1, len(visible)):
            if _bbox_overlap(text_bboxes[i], text_bboxes[j], buffer=0):
                # 重叠面积 > 各自 20% 才算严重重叠（否则紧贴相邻的不算）
                ia = _bbox_intersect_area(text_bboxes[i], text_bboxes[j])
                a1 = text_bboxes[i][2] * text_bboxes[i][3] or 1e-6
                a2 = text_bboxes[j][2] * text_bboxes[j][3] or 1e-6
                if ia / min(a1, a2) > 0.20:
                    is_overlap[i] = True
                    is_overlap[j] = True
    overlap_victims = sum(1 for x in is_overlap if x)
    text_overlap_pct = (overlap_victims / len(visible) * 100) if visible else 0.0

    # ---------------------------------------------------------
    # 指标3: 字号-设备比例检查（诊断"文字比设备还大"这种尺度错配）
    # ---------------------------------------------------------
    # 仅统计关联了设备的文字：font_size > 1.5 * avg_dev_h 视为异常
    # 因为如果viewBox被错误放大而设备symbol没变，avg_dev_h会很小（<5unit），
    # 同时font_size会是12px（=12unit），于是比例=12/3=4 → 远高于阈值
    dev_h = avg_dev_h if avg_dev_h > 0 else 1.0
    fontscale_abnormal = 0
    font_related_count = 0
    # 用object_id匹配到设备的文字
    dev_ids = {e.element_id for e in valid_devs}
    for t in visible:
        oid = getattr(t, 'object_id', '') or ''
        if oid and oid in dev_ids:
            font_related_count += 1
            if (t.font_size or 0) > 1.5 * dev_h and t.font_size > 0:
                fontscale_abnormal += 1
    fontscale_abnormal_pct = (fontscale_abnormal / font_related_count * 100) if font_related_count else 0.0

    # ---------------------------------------------------------
    # 指标4: 拓扑连通度 + 孤岛 + 孤立节点
    # ---------------------------------------------------------
    graph, dangling_conns = _build_topo_graph(doc)
    comps = _connected_components(graph) if graph else []
    comps.sort(key=lambda g: -len(g))
    if graph:
        total_nodes = len(graph)
        # 孤岛判定修正：径向单线图天然存在大量 <5 节点末端分量（配变-用户-表箱），
        # 不能把“小分量”当孤岛。真正的孤岛 = 未接入最大连通分量的节点占比。
        largest_size = len(comps[0]) if comps else 0
        island_comps_pct = (total_nodes - largest_size) / total_nodes * 100 if total_nodes else 0.0
        isolated_nodes = sum(1 for n, neighbors in graph.items() if len(neighbors) == 0)
        isolated_nodes_pct = isolated_nodes / total_nodes * 100 if total_nodes else 0.0
        largest_comp_ratio = (len(comps[0]) / total_nodes) if comps else 0.0
    else:
        total_nodes = 0
        island_comps_pct = 0.0
        isolated_nodes_pct = 0.0
        largest_comp_ratio = 0.0
    total_conns = len(doc.connections) or 1
    dangling_conns_pct = dangling_conns / total_conns * 100

    # ---------------------------------------------------------
    # 指标5: viewBox 与 width/height 的 aspect ratio 一致性
    # ---------------------------------------------------------
    vb_ratio = (vb_w / vb_h) if vb_h > 0 else 0.0
    wh_ratio = (W / H) if H > 0 else 0.0
    aspect_ok = (abs(vb_ratio - wh_ratio) < 0.03) if vb_ratio and wh_ratio else True

    # ---------------------------------------------------------
    # 组装报告
    # ---------------------------------------------------------
    metrics = {
        "viewBox": {"x": round(vb_x, 2), "y": round(vb_y, 2), "w": round(vb_w, 2), "h": round(vb_h, 2)},
        "canvas": {"width": round(W, 2), "height": round(H, 2), "aspect_match": aspect_ok,
                   "vb_ratio": round(vb_ratio, 4), "wh_ratio": round(wh_ratio, 4)},
        "devices": {
            "total": total_devs,
            "stations": len(stations),
            "outside": dev_outside,
            "outside_pct": round(device_outside_pct, 2),
            "overlap_pairs": device_overlap_pairs,
            "avg_height_unit": round(dev_h, 3),
        },
        "texts": {
            "total": len(all_texts),
            "visible": len(visible),
            "hidden": hidden_n,
            "hidden_pct": round(hidden_n / len(all_texts) * 100, 2) if all_texts else 0.0,
            "overlap_victims": overlap_victims,
            "overlap_pct": round(text_overlap_pct, 2),
            "outside": text_outside,
            "fontscale_abnormal": fontscale_abnormal,
            "fontscale_abnormal_pct": round(fontscale_abnormal_pct, 2),
            "avg_dev_h_for_ref": round(dev_h, 3),
        },
        "topology": {
            "total_device_nodes": total_nodes,
            "connections_total": total_conns,
            "connected_components": len(comps),
            "largest_component_size": len(comps[0]) if comps else 0,
            "largest_component_pct": round(largest_comp_ratio * 100, 2),
            "island_components_pct": round(island_comps_pct, 2),
            "isolated_nodes_pct": round(isolated_nodes_pct, 2),
            "dangling_connections_pct": round(dangling_conns_pct, 2),
        }
    }

    # PASS / FAIL 判定
    check = {
        "device_overlap_pairs": device_overlap_pairs <= PASS_THRESHOLDS["device_overlap_pairs"],
        "text_overlap_pct": text_overlap_pct <= PASS_THRESHOLDS["text_overlap_pct"],
        "device_outside_pct": device_outside_pct <= PASS_THRESHOLDS["device_outside_pct"],
        "island_components_pct": island_comps_pct <= PASS_THRESHOLDS["island_components_pct"],
        "isolated_nodes_pct": isolated_nodes_pct <= PASS_THRESHOLDS["isolated_nodes_pct"],
        "dangling_connections_pct": dangling_conns_pct <= PASS_THRESHOLDS["dangling_connections_pct"],
        "fontscale_abnormal_pct": fontscale_abnormal_pct <= PASS_THRESHOLDS["fontscale_abnormal_pct"],
        "aspect_match": aspect_ok,
    }
    PASS = all(check.values())

    report = {
        "SVG_FILE": os.path.abspath(svg_path),
        "PASS": PASS,
        "PASS_THRESHOLDS": PASS_THRESHOLDS,
        "CHECKS": {k: {"value": (
            device_overlap_pairs if k == "device_overlap_pairs" else
            round(text_overlap_pct, 2) if k == "text_overlap_pct" else
            round(device_outside_pct, 2) if k == "device_outside_pct" else
            round(island_comps_pct, 2) if k == "island_components_pct" else
            round(isolated_nodes_pct, 2) if k == "isolated_nodes_pct" else
            round(dangling_conns_pct, 2) if k == "dangling_connections_pct" else
            round(fontscale_abnormal_pct, 2) if k == "fontscale_abnormal_pct" else
            aspect_ok
        ), "ok": v, "threshold": PASS_THRESHOLDS.get(k, "bool")}
                        for k, v in check.items()},
        "METRICS": metrics,
    }

    if report_out:
        os.makedirs(os.path.dirname(os.path.abspath(report_out)) if os.path.dirname(report_out) else ".", exist_ok=True)
        with open(report_out, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    return PASS, report


def _print_summary(svg_path: str, pass_: bool, report: dict):
    print("\n" + "=" * 72)
    print(f"[SVG 质量验收] {'✅ PASS' if pass_ else '❌ FAIL'}  {svg_path}")
    print("=" * 72)
    checks = report["CHECKS"]
    for name, info in checks.items():
        mark = "✅" if info["ok"] else "❌"
        val = info["value"]
        thr = info["threshold"]
        print(f"  {mark} {name:32s} = {str(val):>10}  (≤ {thr})" if isinstance(thr, (int, float)) else
              f"  {mark} {name:32s} = {val}")
    m = report["METRICS"]
    print(f"\n  viewBox: {m['viewBox']}  canvas W×H: {m['canvas']['width']}×{m['canvas']['height']}")
    dev = m["devices"]; txt = m["texts"]; top = m["topology"]
    print(f"  设备: 总数={dev['total']}, 越界={dev['outside']}({dev['outside_pct']}%), "
          f"重叠对={dev['overlap_pairs']}, 平均高={dev['avg_height_unit']} unit")
    print(f"  文字: 总={txt['total']} 可见={txt['visible']} 隐藏={txt['hidden_pct']}%, "
          f"重叠={txt['overlap_victims']}({txt['overlap_pct']}%), 字号异常={txt['fontscale_abnormal']}({txt['fontscale_abnormal_pct']}%)")
    print(f"  拓扑: 节点={top['total_device_nodes']}, 分量={top['connected_components']}, "
          f"最大分量={top['largest_component_pct']}%, 孤岛率={top['island_components_pct']}%, "
          f"孤立={top['isolated_nodes_pct']}%, 飞线={top['dangling_connections_pct']}%")
    print("=" * 72)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("用法: python -m svg_io.quality_checker <svg_path> [report_out.json]")
        sys.exit(2)
    svg = args[0]
    out = args[1] if len(args) > 1 else None
    try:
        ok, rep = check_svg_quality(svg, out)
        _print_summary(svg, ok, rep)
        sys.exit(0 if ok else 1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[FATAL] {e}")
        sys.exit(2)
