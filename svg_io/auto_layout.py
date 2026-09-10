# -*- coding: utf-8 -*-
"""
auto_layout.py - 自动出图布局与渲染内核（配电网单线图/联络图）
================================================================
纯函数模块，供 svg_auto_generator.py 调用：
  1. load_symbol_library(path)      : 从美化 SVG 提取 defs 符号库 + 内容包围盒
  2. symbol_use_xml(boxes, sid, x, y, w, h, target_w) : 生成 <use> 渲染 XML
  3. feeder_tree_layout(sub, roots) : 干线-支线（从左至右树布局，RT 居中）
  4. orthogonal_path(pa, pb)        : 正交布线（Z 形/曼哈顿折线）
  5. tie_grid_layout(...)           : 馈线组全联络简图网格布局（论文算法）
"""
from __future__ import annotations

import re
import math
import xml.etree.ElementTree as ET
from collections import deque, defaultdict

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"


# ----------------------------------------------------------------
# 1. 符号库：解析美化 SVG 的 <defs>，提取每个 symbol 的内容包围盒
# ----------------------------------------------------------------
def _content_box(body: str) -> dict | None:
    """从符号内容体提取包围盒（line/circle/rect/points 坐标）。"""
    xs, ys = [], []
    for tag, attr in re.findall(r"<(\w+)\b([^>]*)>", body):
        for at in ("x1", "x2", "x", "cx"):
            mm = re.search(at + r'="([\d.+-]+)"', attr)
            if mm:
                try:
                    xs.append(float(mm.group(1)))
                except ValueError:
                    pass
        for at in ("y1", "y2", "y", "cy"):
            mm = re.search(at + r'="([\d.+-]+)"', attr)
            if mm:
                try:
                    ys.append(float(mm.group(1)))
                except ValueError:
                    pass
        rm = re.search(r'r="([\d.+-]+)"', attr)
        cmx = re.search(r'cx="([\d.+-]+)"', attr)
        cmy = re.search(r'cy="([\d.+-]+)"', attr)
        if rm and cmx and cmy:
            try:
                r = float(rm.group(1)); cx = float(cmx.group(1)); cy = float(cmy.group(1))
                xs += [cx - r, cx + r]; ys += [cy - r, cy + r]
            except ValueError:
                pass
        pm = re.search(r'points="([^"]*)"', attr)
        if pm:
            for pair in pm.group(1).split():
                try:
                    px, py = pair.split(",")
                    xs.append(float(px)); ys.append(float(py))
                except ValueError:
                    pass
    if not xs or not ys:
        return None
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    w = maxx - minx
    h = maxy - miny
    if w < 0.1:
        w = 1.0
    return {"cx": (minx + maxx) / 2, "cy": (miny + maxy) / 2,
            "w": w, "h": h, "scale_k": 1.0 / w}


def load_symbol_dir(sym_dir: str) -> tuple[str, dict]:
    """从 final_symbols 目录加载标准符号：每个 std_*.svg → <symbol id> + 包围盒。"""
    import os
    if not os.path.isdir(sym_dir):
        return "", {}
    defs_xml = ""
    boxes = {}
    for fn in sorted(os.listdir(sym_dir)):
        if not fn.startswith("std_") or not fn.endswith(".svg"):
            continue
        sid = fn[:-4]
        try:
            content = open(os.path.join(sym_dir, fn), encoding="utf-8").read()
        except OSError:
            continue
        m = re.search(r"<svg\b[^>]*>(.*?)</svg>", content, re.S)
        if not m:
            continue
        inner = m.group(1)
        defs_xml += f'<symbol id="{sid}">{inner}</symbol>'
        box = _content_box(inner)
        vb_w, vb_h = 0.0, 0.0
        vbm = re.search(r'viewBox="([^"]*)"', content)
        if vbm:
            nums = re.findall(r"[\d.+-]+", vbm.group(1))
            if len(nums) >= 4:
                vb_w, vb_h = float(nums[2]), float(nums[3])
        if not box:
            if vb_w > 0 and vb_h > 0:
                boxes[sid] = {"cx": vb_w / 2, "cy": vb_h / 2, "w": vb_w, "h": vb_h,
                              "scale_k": 1.0 / vb_w if vb_w > 0 else 1.0,
                              "vb_w": vb_w, "vb_h": vb_h}
            continue
        box["vb_w"] = vb_w if vb_w > 0 else box["w"]
        box["vb_h"] = vb_h if vb_h > 0 else box["h"]
        boxes[sid] = box
    return defs_xml, boxes


def load_symbol_library(beautified_svg_path: str) -> tuple[str, dict]:
    """返回 (defs_xml, boxes)。
    boxes: {symbol_id: {'cx','cy','w','h','scale_k'}}  scale_k = 1/w（符号内容宽 1 单位对应的放大系数）
    """
    import os
    if not os.path.exists(beautified_svg_path):
        return "", {}
    src = open(beautified_svg_path, encoding="utf-8").read()
    m = re.search(r"<defs>(.*?)</defs>", src, re.S)
    if not m:
        return "", {}
    defs_xml = m.group(1)
    boxes = {}
    for sm in re.finditer(r"<symbol\b([^>]*)>(.*?)</symbol>", defs_xml, re.S):
        attrs, body = sm.group(1), sm.group(2)
        idm = re.search(r'id="([^"]*)"', attrs)
        if not idm:
            continue
        sid = idm.group(1)
        box = _content_box(body)
        if box:
            boxes[sid] = box
            continue
        vb = re.search(r'viewBox="[^"]*"', attrs)
        if vb:
            nums = re.findall(r"[\d.+-]+", vb.group(0))
            if len(nums) >= 4:
                w = float(nums[2]); h = float(nums[3])
                boxes[sid] = {"cx": w / 2, "cy": h / 2, "w": w, "h": h, "scale_k": 1.0 / w if w > 0 else 1.0}
    return defs_xml, boxes


def symbol_use_xml(boxes: dict, sid: str, x: float, y: float, w: float, h: float,
                   target_w: float = 55.0) -> str:
    """生成 <use> 设备符号 XML：以设备框中心为原点，按 viewBox 等比缩放到目标框内。"""
    return _symbol_use_xml_impl(boxes, sid, x, y, w, h, target_w, rot=False)


def symbol_use_xml_rot(boxes: dict, sid: str, x: float, y: float, w: float, h: float,
                       target_w: float = 200.0, rot: bool = True) -> str:
    """旋转版：rot=True 时符号绕中心旋转 90°（横向放置，端子左右），用于水平线路上的设备。"""
    return _symbol_use_xml_impl(boxes, sid, x, y, w, h, target_w, rot=rot)


def _symbol_use_xml_impl(boxes: dict, sid: str, x: float, y: float, w: float, h: float,
                         target_w: float, rot: bool) -> str:
    box = boxes.get(sid)
    if not box:
        return ""
    vb_w = box.get("vb_w") or box.get("w", 1.0)
    vb_h = box.get("vb_h") or box.get("h", 1.0)
    cx = x + w / 2
    cy = y + h / 2
    if rot:
        # 旋转90°后：视觉宽=原高 vb_h、视觉高=原宽 vb_w → 端子左右
        tw = min(w * 0.95, target_w)
        th = h * 0.95
        s = min(tw / vb_h, th / vb_w) if vb_w > 0 and vb_h > 0 else target_w * box["scale_k"]
        if s <= 0 or s > 10:
            s = min(tw / vb_h, th / vb_w)
        return (f'<g transform="translate({cx:.2f},{cy:.2f}) rotate(90)">'
                f'<use xlink:href="#{sid}" transform="scale({s:.3f}) translate({-box["cx"]:.3f},{-box["cy"]:.3f})"/></g>')
    tw = min(w * 0.9, target_w)
    th = h * 0.9
    s = min(tw / vb_w, th / vb_h) if vb_w > 0 and vb_h > 0 else target_w * box["scale_k"]
    if s <= 0 or s > 10:
        s = min(tw / vb_w, th / vb_h)
    return (f'<g transform="translate({cx:.2f},{cy:.2f})">'
            f'<use xlink:href="#{sid}" transform="scale({s:.3f}) translate({-box["cx"]:.3f},{-box["cy"]:.3f})"/></g>')


# ----------------------------------------------------------------
# 2. 干线-支线树布局（从左至右，Reingold-Tilford 居中简化版）
# ----------------------------------------------------------------
def feeder_tree_layout(sub, roots=None, col_gap=150.0, row_gap=70.0, pad=80.0):
    """返回 {node_id: (x, y)}，x 方向为层（电源在左），y 方向子树居中。

    - 建 BFS 树（父指针+children）
    - 后序遍历：叶子分配 y 槽位；内部节点 y = 子节点 y 均值
    - x = depth * col_gap（从左至右）
    - 孤立节点挂到第 0 层
    """
    if not sub.number_of_nodes():
        return {}, 0, 0

    # 选根：优先母线/变电站出口，其次度数最大
    if not roots:
        def _score(n):
            tp = str(sub.nodes[n].get("equip_type") or "")
            nm = str(sub.nodes[n].get("equip_name") or "")
            sc = 0
            if "母线" in tp or "母线" in nm: sc += 1000
            elif "变压" in tp: sc += 500
            elif "断路" in tp: sc += 200
            if str(sub.nodes[n].get("feeder_id") or ""): sc += 30
            return sc + sub.degree(n) * 10
        roots = [max(sub.nodes(), key=_score)]

    parent: dict = {}
    children: dict = defaultdict(list)
    depth: dict = {}
    seen = set()
    q = deque()
    for r in roots:
        if sub.has_node(r) and r not in seen:
            seen.add(r)
            parent[r] = None
            depth[r] = 0
            q.append(r)
    while q:
        cur = q.popleft()
        for nb in sorted(sub.neighbors(cur)):
            if nb not in seen:
                seen.add(nb)
                parent[nb] = cur
                depth[nb] = depth[cur] + 1
                children[cur].append(nb)
                q.append(nb)
    # 孤立节点（不在树里）
    orphans = [n for n in sub.nodes() if n not in seen]
    for i, n in enumerate(orphans):
        seen.add(n)
        parent[n] = None
        depth[n] = 0
        children.setdefault("__root__", [])
        children["__root__"].append(n)

    # 后序计算 y：叶子 y 槽递增；内部 y=子均值
    y_pos: dict = {}
    counter = [0.0]
    max_depth = max(depth.values()) if depth else 0

    def _post(n):
        ch = children.get(n, [])
        if not ch:
            y_pos[n] = counter[0]
            counter[0] += row_gap
        else:
            for c in ch:
                _post(c)
            y_pos[n] = sum(y_pos[c] for c in ch) / len(ch)
    if children.get("__root__"):
        for n in children["__root__"]:
            _post(n)
    for r in roots:
        if r in seen:
            _post(r)

    pos = {}
    for n in seen:
        d = depth.get(n, 0)
        y = y_pos.get(n, 0.0)
        pos[n] = (pad + d * col_gap, pad + y)
    cols = max_depth + 1
    rows = int(counter[0] / row_gap) if row_gap > 0 else 1
    return pos, cols, max(1, rows)


def trunk_branch_layout(sub, col_gap=110.0, row_gap=48.0, pad=56.0):
    """主干-支线布局（单线图）：干线水平从左至右，支线垂直展开。

    - BFS 建树；主干 = 沿最重子树路径（最大子树优先）
    - 主干节点 x 递增（水平干线），y = 0（同一水平线）
    - 支线从主干 T 接点垂直展开（x = 主干 x + 1 列，y 围绕主干上下展开）
    - 支线内链式节点（单子）垂直堆叠（同列）
    返回 {n: (x,y)}, 列数, 行数
    """
    import networkx as nx
    from collections import deque

    if sub.number_of_nodes() == 0:
        return {}, 0, 0

    def _score(n):
        tp = str(sub.nodes[n].get("equip_type") or "")
        nm = str(sub.nodes[n].get("equip_name") or "")
        s = 0
        if "馈线段" in nm or "ACLine" in tp or tp in ("1702", "1714"):
            s += 10
        if "开关" in nm or "断路" in nm:
            s += 4
        if "配变" in nm or "用户" in nm:
            s += 2
        return s

    roots = [max(sub.nodes(), key=_score)]
    parent = {}
    depth = {}
    children = {}
    seen = set()
    q = deque()
    for r in roots:
        if sub.has_node(r) and r not in seen:
            seen.add(r)
            parent[r] = None
            depth[r] = 0
            children[r] = []
            q.append(r)
    while q:
        cur = q.popleft()
        for nb in sorted(sub.neighbors(cur)):
            if nb not in seen:
                seen.add(nb)
                parent[nb] = cur
                depth[nb] = depth[cur] + 1
                children.setdefault(cur, []).append(nb)
                children.setdefault(nb, [])
                q.append(nb)
    orphans = [n for n in sub.nodes() if n not in seen]
    for n in orphans:
        seen.add(n)
        parent[n] = None
        children[n] = []

    def _subtree_size(n):
        return 1 + sum(_subtree_size(c) for c in children.get(n, []))

    root = roots[0]
    # 主干：沿最重子树
    trunk = []
    cur = root
    while cur is not None and cur in seen:
        trunk.append(cur)
        ch = children.get(cur, [])
        if not ch:
            break
        cur = max(ch, key=_subtree_size)
    trunk_set = set(trunk)

    # 列分配：主干 i；支线 = 主干父列+1，支线链沿用父列
    col: dict = {}
    for i, n in enumerate(trunk):
        col[n] = i
    for n in sorted(seen, key=lambda x: depth.get(x, 0)):
        if n in trunk_set:
            continue
        p = parent.get(n)
        if p is None or p not in col:
            col[n] = 0
        elif p in trunk_set:
            # 支线与主干同列、垂直展开（周博曦模型：干线水平、支线上下分支）
            col[n] = col[p]
        else:
            col[n] = col[p]

    # y：全局叶子槽 + 子树区间（支线相对主干垂直展开，全局 counter 保证子树区间分离）
    y_pos: dict = {}
    counter = [0.0]
    done_y: set = set()

    def _post2(n):
        if n in done_y:
            return
        done_y.add(n)
        ch = children.get(n, [])
        if not ch:
            y_pos[n] = counter[0]
            counter[0] += row_gap
        elif len(ch) == 1:
            _post2(ch[0])
            y_pos[n] = y_pos[ch[0]] - row_gap  # 链向上（可能为负，pad 平移兜底）
        else:
            for c in ch:
                _post2(c)
            y_pos[n] = sum(y_pos[c] for c in ch) / len(ch)

    # 先处理所有支线（按主干顺序，确保叶子全局递增、子树区间分离）
    for m in trunk:
        for c in children.get(m, []):
            if c not in trunk_set:
                _post2(c)
    # 主干 = 0 水平线
    for n in trunk:
        y_pos[n] = 0.0
    for n in seen:
        if n not in y_pos:
            y_pos[n] = 0.0

    for n in trunk:
        y_pos[n] = 0.0
    for n in seen:
        if n not in y_pos:
            y_pos[n] = 0.0

    pos = {n: (pad + col.get(n, 0) * col_gap, pad + y_pos.get(n, 0.0)) for n in seen}
    ncols = max(col.values()) + 1 if col else 1
    ys_all = [p[1] for p in pos.values()]
    nrows = max(1, int((max(ys_all) - min(ys_all)) / row_gap) + 2)
    return pos, ncols, nrows


# ----------------------------------------------------------------
# 2b. 馈线分量拼接布局（处理多连通分量 + 配变挂耳压缩高度）
# ----------------------------------------------------------------
def feeder_comp_layout(sub, col_gap=110.0, row_gap=48.0, pad=56.0):
    """返回 {node_id: (x, y)}, (vb_w, vb_h)。

    - 按连通分量分解；大分量(>15)树布局横向拼接，小分量(<=15)链式换行
    - 配变/杆塔/用户等末端节点剥离为"挂耳"，垂直堆叠在父骨架节点旁，大幅压缩高度
    """
    import networkx as nx
    HANG_KW = ("配变", "用电", "用户", "负荷")
    TRUNK_KW = ("馈线段", "母线", "断路", "开关", "刀闸", "接地", "熔断", "接头", "互感", "保险", "CT", "PT")

    def _is_hang(n):
        nm = str(sub.nodes[n].get("equip_name") or "")
        return any(k in nm for k in HANG_KW)

    comps = sorted(nx.connected_components(sub), key=len, reverse=True)
    pos: dict = {}
    x_cursor = pad
    y_cursor = pad
    row_h = 0.0

    def _layout_one(comp_nodes):
        nonlocal x_cursor, y_cursor, row_h
        cg = sub.subgraph(comp_nodes).copy()
        hang = [n for n in cg.nodes() if _is_hang(n)]
        skel = [n for n in cg.nodes() if n not in hang]
        skel_sub = cg.subgraph(skel).copy() if skel else None
        if skel_sub is None or skel_sub.number_of_nodes() == 0:
            # 全是挂耳：直接一排
            yy = y_cursor
            for i, n in enumerate(sorted(hang)):
                pos[n] = (x_cursor + i * (col_gap * 0.9), yy)
            w = len(hang) * col_gap * 0.9 + pad
            row_h = max(row_h, 120)
            x_cursor += w
            return
        # 骨架树布局（主干-支线：干线水平、支线垂直）
        sp, _, _ = trunk_branch_layout(skel_sub, col_gap=col_gap, row_gap=row_gap, pad=0.0)
        if not sp:
            return
        min_x = min(p[0] for p in sp.values())
        min_y = min(p[1] for p in sp.values())
        off_x = x_cursor - min_x
        off_y = y_cursor - min_y
        sp = {n: (px + off_x, py + off_y) for n, (px, py) in sp.items()}
        pos.update(sp)
        # 挂耳：父 = 骨架邻居；垂直堆叠（上下交替）
        hang_counter: dict = {}
        nofa_k = 0
        for n in sorted(hang):
            nb_skel = [m for m in cg.neighbors(n) if m in sp]
            if not nb_skel:
                # 无骨架父：横向排开（避免覆盖）
                yy = y_cursor + row_h + 30 + 60
                pos[n] = (x_cursor + nofa_k * col_gap, yy)
                nofa_k += 1
                continue
            # 选连接数最少的骨架父（T 接点）
            fa = min(nb_skel, key=lambda m: skel_sub.degree(m))
            fx, fy = sp[fa]
            k = hang_counter.get(fa, 0)
            hang_counter[fa] = k + 1
            direction = -1 if k % 2 == 0 else 1
            layer = k // 2
            pos[n] = (fx, fy + direction * (layer + 1) * (row_gap * 1.7))
        w = max(p[0] for p in sp.values()) + pad
        row_h = max(row_h, max(p[1] for p in sp.values()) - y_cursor)
        x_cursor = w

    big = [c for c in comps if len(c) > 15]
    small = [c for c in comps if len(c) <= 15]
    for c in big:
        _layout_one(c)
    # 小分量：每行 6 个换行
    per_row = 6
    for i, c in enumerate(small):
        if i % per_row == 0 and i > 0:
            x_cursor = pad
            y_cursor += row_h + 90
            row_h = 0.0
        _layout_one(c)
    # 后处理：重叠位置沿 y 方向确定性分离（保证视觉不重叠）
    seen_at: dict = {}
    for n in sorted(pos.keys()):
        px, py = pos[n]
        key = (round(px, 2), round(py, 2))
        k = seen_at.get(key, 0)
        seen_at[key] = k + 1
        if k > 0:
            pos[n] = (px, py + k * row_gap * 0.8)
    return pos, (max(p[0] for p in pos.values()) + pad, max(p[1] for p in pos.values()) + pad)


# ----------------------------------------------------------------
# 2b. 专利式分层网格布局（辐射接线模式单线图）
#     参考：CN105117518A《辐射接线模式的配电馈线单线图自动绘制方法》
#     - 主干（0级分支）水平从左至右；1级支线垂直、2级支线水平……奇偶交替
#     - 子树按 leaf_count 分配连续区间 → 天然避让、无重叠
#     - 返回 pos + orient（'H'=符号旋转90°横向 / 'V'=符号纵向）
# ----------------------------------------------------------------
def feeder_grid_layout(sub, col_gap=150.0, row_gap=200.0, pad=120.0):
    """专利式分层网格布局（辐射接线模式单线图）。
    - 主干 = 图最长路径（直径），0 级分支水平从左至右
    - 支线按距主干深度分层：1级垂直、2级水平、3级及以上垂直（限制宽度）
    - 子树按 leaf_count 分配连续区间 → 天然避让、无重叠
    - 返回 pos + orient（'H'=符号旋转90°横向 / 'V'=符号纵向）
    """
    import networkx as nx
    from collections import deque

    def _pick_root(G):
        for n, d in G.nodes(data=True):
            nm = str(d.get("equip_name") or "")
            if any(k in nm for k in ("变电站", "配电室", "开关站", "环网", "母线", "电源", "配电站")):
                return n
        return None

    def _bfs_far(G, s):
        seen = {s: 0}
        dq = deque([s])
        far, fd = s, 0
        while dq:
            cur = dq.popleft()
            for m in G.neighbors(cur):
                if m not in seen:
                    seen[m] = seen[cur] + 1
                    dq.append(m)
                    if seen[m] > fd:
                        far, fd = m, seen[m]
        return far, fd

    if sub.number_of_nodes() == 0:
        return {}, {}, (0.0, 0.0)
    comps = sorted(nx.connected_components(sub), key=len, reverse=True)
    if not comps:
        return {}, {}, (0.0, 0.0)
    Gs = sub.subgraph(comps[0]).copy()

    root = _pick_root(Gs)
    # 配网单线图是辐射树：只保留生成树边，消除折叠产生的跨支线非树长边（它们穿线）
    # BFS 树从电源/变电站根出发，保证每条边沿树路径相连、位置相邻
    _attrs = {_n: dict(Gs.nodes[_n]) for _n in Gs.nodes()}
    if root is not None:
        Gs = nx.bfs_tree(Gs, root).to_undirected()
    else:
        Gs = nx.bfs_tree(Gs, next(iter(Gs.nodes()))).to_undirected()
    nx.set_node_attributes(Gs, _attrs)
    # 主干 = 最长路径（辐射网骨架）
    a, _ = _bfs_far(Gs, next(iter(Gs.nodes())))
    b, _ = _bfs_far(Gs, a)
    trunk_seq = nx.shortest_path(Gs, a, b)
    if root is not None and root not in trunk_seq:
        # 电源点并入主干端（主干从电源出发）
        e = min(trunk_seq, key=lambda t: nx.shortest_path_length(Gs, root, t))
        seg = nx.shortest_path(Gs, root, e)
        trunk_seq = seg[:-1] + trunk_seq
        if root not in trunk_seq:
            trunk_seq = [root] + trunk_seq

    trunk_set = set(trunk_seq)
    # 多源 BFS：距主干深度
    depth = {n: 0 for n in trunk_seq}
    par = {}
    dq = deque(trunk_seq)
    while dq:
        cur = dq.popleft()
        for m in Gs.neighbors(cur):
            if m not in depth:
                depth[m] = depth[cur] + 1
                par[m] = cur
                dq.append(m)

    kids = {n: [m for m in Gs.neighbors(n) if par.get(m) == n] for n in Gs.nodes()}
    # 叶子数（深→浅拓扑序）
    leaf_count = {}
    for n in sorted(Gs.nodes(), key=lambda m: -depth.get(m, 0)):
        ks = kids[n]
        leaf_count[n] = sum(leaf_count[k] for k in ks) if ks else 1

    pos, orient = {}, {}
    for i, n in enumerate(trunk_seq):
        pos[n] = (pad + i * col_gap, pad)
        orient[n] = "H"
    trunk_x = {n: pos[n][0] for n in trunk_seq}

    # 占用检测：网格点 (x,y) 已被其他设备占用时，沿当前方向顺移避让（专利：子树四顶点重叠消除）
    used = {}
    def _occupy(n, x, y, d):
        dx, dy = (col_gap, 0.0) if d % 2 == 0 else (0.0, row_gap)
        while (round(x, 1), round(y, 1)) in used and used[(round(x, 1), round(y, 1))] != n:
            x += dx
            y += dy
        pos[n] = (x, y)
        used[(round(x, 1), round(y, 1))] = n

    def _place(n, x, y, d):
        """专利式分层：0级主干水平；1/3/5级支线垂直；2/4/6级支线水平（方向交错，更紧凑）。"""
        ch = kids.get(n, [])
        if not ch:
            # 叶子：奇数级向下一格、偶数级向右一格
            if d % 2 == 1:
                _occupy(n, x, y + row_gap, d)
            else:
                _occupy(n, x + col_gap, y, d)
            return
        if d % 2 == 1:
            # 奇数级：垂直堆叠（子在父下，同 x 列；按 leaf_count 分配连续区间避让）
            _occupy(n, x, y + row_gap, d)
            yy = y + row_gap * 2
            for c in ch:
                hh = max(leaf_count[c] * row_gap * 0.5, row_gap)
                _place(c, x, yy, d + 1)
                yy += hh
        else:
            # 偶数级：水平堆叠（子在父右，同 y 行）
            _occupy(n, x + col_gap, y, d)
            xx = x + col_gap * 2
            for c in ch:
                ww = max(leaf_count[c] * col_gap * 0.5, col_gap)
                _place(c, xx, y, d + 1)
                xx += ww

    # 主干节点的 1 级支线：垂直向下（同 x 列堆叠，区间分配避让）
    for n in trunk_seq:
        yy = pad
        for c in kids.get(n, []):
            hh = max(leaf_count[c] * row_gap * 0.5, row_gap)
            _place(c, trunk_x[n], yy, 1)
            yy += hh

    # 孤立小分量：底部换行排列（每行有限列，避免宽度爆炸）
    others = [n for comp in comps[1:] for n in comp]
    if others:
        MAX_COL = 24
        ey = pad + (max((p[1] for p in pos.values()), default=pad) + row_gap * 1.5)
        for i, n in enumerate(sorted(others)):
            col = i % MAX_COL
            row = i // MAX_COL
            pos[n] = (pad + col * (col_gap * 0.8), ey + row * row_gap)

    # 设备方向由邻居实际位置决定：水平邻居多 → H（符号旋转90°端子左右）；垂直邻居多 → V（端子上/下）
    # 保证连线从端子进出，避免线穿过符号
    for n in pos:
        cx, cy = pos[n]
        dx = dy = 0.0
        for m in Gs.neighbors(n):
            if m in pos:
                dx += abs(pos[m][0] - cx)
                dy += abs(pos[m][1] - cy)
        orient[n] = "H" if dx >= dy else "V"

    vb_w = max(p[0] for p in pos.values()) + col_gap
    vb_h = max(p[1] for p in pos.values()) + row_gap
    return pos, orient, (vb_w, vb_h)


def orthogonal_path(pa, pb, w=100.0, h=40.0):
    """返回折线点列表 [(x,y), ...]，横平竖直（曼哈顿 Z 形）。"""
    ax, ay = pa[0] + w / 2, pa[1] + h / 2
    bx, by = pb[0] + w / 2, pb[1] + h / 2
    if abs(bx - ax) < 1e-6 and abs(by - ay) < 1e-6:
        return [(ax, ay), (bx, by)]
    dx, dy = bx - ax, by - ay
    if abs(dx) >= abs(dy):
        midx = (ax + bx) / 2
        return [(ax, ay), (midx, ay), (midx, by), (bx, by)]
    else:
        midy = (ay + by) / 2
        return [(ax, ay), (ax, midy), (bx, midy), (bx, by)]


def polyline_xml(points, color, width, dash=None):
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{dash_attr}/>')


def orthogonal_center(ca, cb):
    """中心点间正交折线（联络图馈线↔开关用）。"""
    ax, ay = ca
    bx, by = cb
    if abs(bx - ax) < 1e-6 and abs(by - ay) < 1e-6:
        return [(ax, ay), (bx, by)]
    if abs(bx - ax) >= abs(by - ay):
        midx = (ax + bx) / 2
        return [(ax, ay), (midx, ay), (midx, by), (bx, by)]
    else:
        midy = (ay + by) / 2
        return [(ax, ay), (ax, midy), (bx, midy), (bx, by)]


# ----------------------------------------------------------------
# 4. 馈线组全联络简图网格布局（论文《配网线路馈线组全联络简图的绘制方法及应用》）
# ----------------------------------------------------------------
def tie_grid_layout(feeders: list, ties: list, start_fid: str,
                    col_gap=320.0, row_gap=64.0, pad=90.0):
    """返回 {fid: (x,y)}, {fid: level}, tie 渲染列表。

    feeders: 全部参与馈线列表（含跨站）
    ties:    [(fid_a, fid_b, dev_id, dev_name)]
    start_fid: 起始馈线（0 层）
    网格规则：
      - 起始馈线 0 层；与第 k 层馈线联络的未分层馈线为 k+1 层
      - 层内馈线按 barycenter（上层连接 y 均值）排序避免交叉
      - 联络开关画在两层馈线之间（中点）
    """
    fid_set = set(feeders)
    # 建馈线邻接
    adj = defaultdict(set)
    tie_devs = {}  # (a,b) sorted -> list[(dev_id, name)]
    for a, b, devid, name in ties:
        if a in fid_set and b in fid_set:
            adj[a].add(b)
            adj[b].add(a)
            key = (a, b) if a < b else (b, a)
            tie_devs.setdefault(key, []).append((devid, name))

    # 分层 BFS
    level: dict = {}
    if start_fid in fid_set:
        level[start_fid] = 0
    q = deque([start_fid])
    while q:
        cur = q.popleft()
        for nb in sorted(adj[cur]):
            if nb not in level:
                level[nb] = level[cur] + 1
                q.append(nb)
    for f in fid_set:
        if f not in level:
            level[f] = max(level.values()) + 1 if level else 0
            if f not in level:
                level[f] = 0

    max_level = max(level.values()) if level else 0
    layers = defaultdict(list)
    for f in fid_set:
        layers[level[f]].append(f)
    # 层内排序：barycenter（优先起始馈线）
    ordered: dict = {}
    for lv in range(max_level + 1):
        items = layers[lv]
        # 计算每个馈线的 barycenter（连接上层馈线的 y 均值）
        bary = {}
        for f in items:
            ups = [nb for nb in adj[f] if level.get(nb, -1) < lv]
            ys = []
            for u in ups:
                if u in ordered:
                    ys.append(ordered[u][1])
            bary[f] = (sum(ys) / len(ys)) if ys else (len(ordered) * row_gap * 2 + row_gap)
        items_sorted = sorted(items, key=lambda f: (bary.get(f, 0), f))
        # 逐个放置：y 需 >= 前一馈线 y + row_gap，并尽量贴近 barycenter
        placed = []
        y_cursor = pad
        for f in items_sorted:
            target_y = bary.get(f, y_cursor)
            y = max(y_cursor, target_y)
            x = pad + lv * col_gap
            ordered[f] = (x, y)
            placed.append(f)
            y_cursor = y + row_gap

    # 联络开关位置：两层之间中点；同一配对的多个开关沿垂直通道展开（避免重叠）
    tie_meta = []
    for (a, b), devs in tie_devs.items():
        if a in ordered and b in ordered:
            ax, ay = ordered[a]
            bx, by = ordered[b]
            midx = (ax + bx) / 2
            n = len(devs)
            y0 = min(ay, by) + 26.0
            y1 = max(ay, by) - 26.0
            if y1 - y0 < 24.0:
                y0 = min(ay, by)
                y1 = max(ay, by)
            sw_pos = []
            for k in range(n):
                if n > 1:
                    yy = y0 + (y1 - y0) * k / (n - 1)
                else:
                    yy = (y0 + y1) / 2
                sw_pos.append((devs[k][0], devs[k][1], midx, yy))
            tie_meta.append({"a": a, "b": b, "x": midx, "y": (y0 + y1) / 2, "devs": devs,
                             "sw_pos": sw_pos, "cross": level[a] != level[b]})
    return ordered, level, tie_meta

def symbol_scale(boxes: dict, sid: str, w: float, h: float, rot: bool = False,
                 target_w: float = None) -> float:
    """与 symbol_use_xml / symbol_use_xml_rot 完全一致的符号缩放系数。

    rot=True（旋转90°后视觉宽=原高 vb_h、视觉高=原宽 vb_w）→ 端子左右；
    rot=False → 端子上下。
    """
    box = boxes.get(sid)
    if not box:
        return 0.5
    vb_w = box.get("vb_w") or box.get("w", 1.0)
    vb_h = box.get("vb_h") or box.get("h", 1.0)
    if vb_w <= 0 or vb_h <= 0:
        return 0.5
    if rot:
        tw = min(w * 0.95, target_w if target_w else 200.0)
        th = h * 0.95
        return min(tw / vb_h, th / vb_w)
    tw = min(w * 0.9, target_w if target_w else 150.0)
    th = h * 0.9
    return min(tw / vb_w, th / vb_h)
