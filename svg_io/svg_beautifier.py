# -*- coding: utf-8 -*-
"""
SVG美化模块 v2 - 权重树算法集成版（完整功能对齐参考文件 svg_beautifier_v2.py）
基于 SvgDocument IR 解析，内部数据结构与 v2 参考文件完全一致。
修复功能：飞线端点修复 + 拓扑孤岛缝合 + 虚假连接清理
布局功能：权重树梳状布局 + 未入树设备兜底 + 容器纵向排布
渲染功能：正交布线 + 母线加粗 + 标注白底避让 + 符号统一缩放
"""

import os
import re
import copy
import math
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from typing import List, Tuple, Dict, Optional, Set

from data_io.svg_reader import SvgDocument, SvgElement, SvgConnection, SvgText, SVG_NS, XLINK_NS, IEC_NS
from data_io.svg_writer import write_svg

# ═══════════════════════════════════════════════════════════
#  规范常量（与参考文件 v2 对齐，自包含不依赖 core.constants）
# ═══════════════════════════════════════════════════════════
WIRE_MARKERS = ('TMP', 'dxd')
BUSBAR_TYPES = {'0311'}
CONTAINER_TYPES = {'zf01', 'zf06', 'zf07', 'zf08'}
SWITCH_TYPES = {'0307', '0201', '0202', '0203', '0302', '0305', '0306', '0309'}
TRANSFORMER_TYPES = {'0110', '0111'}
KEY_DEV_TYPES = SWITCH_TYPES | TRANSFORMER_TYPES | BUSBAR_TYPES
GARBAGE_PATTERNS = [
    r'[炽始速常个行旁劳著长]',
    r'[歌咱母民急书箱]',
    r'[行县万别央压四说]',
    r'[行县行放导较拉除]',
    r'[毛须然约命了严]',
    r'[明争败诉取教]',
    r'[个行行者劳]',
    r'[假社员教]',
    r'[炽始速常]',
    r'行县', r'个行', r'行者劳',
    r'明\d*#', r'争\d', r'败诉', r'况诉',
]

C_BG = '#FFFFFF'
C_10KV = '#00A854'
C_TIE = '#FF6A00'
C_CROSS_TIE = '#722ED1'
C_SPARE = '#BFBFBF'
C_CONTAINER = '#595959'
C_TEXT = '#262626'
C_BUSBAR = '#00A854'
W_TRUNK = 3.0
W_BRANCH = 1.5
W_TIE = 4.5
W_CONTAINER = 2.0
W_BUSBAR = 4.0
F_TITLE = 21.3
F_KEY = 14.0
F_BRANCH = 12.0
GRID = 10
MARGIN = 40
TITLE_H = 52
CONT_PAD = 24
UNIT_V = 14
SYM_SCALE = 3.5
DEV_HW = 15
DEV_HH = 10

DEVICE_STANDARD_SIZES = {
    "PowerTransformer": (28.0, 20.0),
    "Breaker": (24.0, 12.0),
    "BusbarSection": (32.0, 6.0),
    "LoadBreakSwitch": (20.0, 10.0),
    "Disconnector": (20.0, 10.0),
    "Fuse": (16.0, 8.0),
    "CurrentTransformer": (16.0, 12.0),
    "PotentialTransformer": (16.0, 12.0),
    "Junction": (8.0, 8.0),
    "EnergyConsumer": (20.0, 12.0),
    "RemoteUnit": (16.0, 10.0),
    "PoleCode": (16.0, 10.0),
    "Other": (16.0, 10.0),
    "GroundDisconnector": (20.0, 10.0),
    "CompositeSwitch": (20.0, 10.0),
}


class SvgBeautifier:
    """配电网单线图 SVG 美化重构工具 v2（完整功能版）"""

    def __init__(self, svg_path: str, output_path: str = None):
        self.svg_path = svg_path
        self.svg_filename = os.path.basename(svg_path)
        self.output_path = output_path or svg_path.replace(".svg", "_beautified.svg")

        self.doc: Optional[SvgDocument] = None
        self.devices: Dict[str, Dict] = {}
        self.gl_to_devs: Dict[str, Set[str]] = defaultdict(set)
        self.containers: Dict[str, Dict] = {}
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        self.pos: Dict[str, Tuple[float, float]] = {}
        self.cont_box: Dict[str, Tuple[float, float, float, float]] = {}
        self.tree_parent: Dict[str, Optional[str]] = {}
        self.tree_children: Dict[str, List[str]] = defaultdict(list)
        self.non_tree_edges: List = []
        self.label_rects: List = []
        self.sym_box: Dict[str, Dict] = {}
        self.orig_pos: Dict[str, Tuple[float, float]] = {}
        self.repair_stats: Dict = {}

    # ═══════════════════════════════════════════════════════════
    #  辅助工具函数
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def is_wire(t: str) -> bool:
        return bool(t) and any(m in t for m in WIRE_MARKERS)

    @staticmethod
    def is_real_device(t: str) -> bool:
        if not t or SvgBeautifier.is_wire(t):
            return False
        if t in CONTAINER_TYPES:
            return False
        if t in ('-1', '0'):
            return False
        return True

    @staticmethod
    def is_garbage_text(text: str) -> bool:
        if not text or len(text) < 2:
            return True
        if text.startswith('TMP') or re.match(r'^\d+$', text):
            return True
        for pat in GARBAGE_PATTERNS:
            if re.search(pat, text):
                return True
        if text.startswith('000') and re.search(r'[\u4e00-\u9fff]{2,}', text):
            valid_kw = ['终端头', '电缆', '母线', '线路', '开关站', '环网柜', '配变',
                        '断路器', '隔离开关', '负荷开关', '熔断器', '杆塔', '变压器',
                        '站房', '配电室', 'LINE', 'SUB']
            if not any(kw in text for kw in valid_kw):
                return True
            for pat in GARBAGE_PATTERNS:
                if re.search(pat, text):
                    return True
        if re.search(r'[a-zA-Z]+_[\u4e00-\u9fff]', text) and 'LINE' not in text.upper():
            return True
        return False

    @staticmethod
    def snap(v: float) -> float:
        return round(v / GRID) * GRID

    # ═══════════════════════════════════════════════════════════
    #  核心处理流程
    # ═══════════════════════════════════════════════════════════

    def beautify(self) -> str:
        print(f"\n[Beautifier v2] 正在处理: {self.svg_filename}")
        self._prepare_internal_data()
        self.repair()
        self.layout()
        self.render(self.output_path)
        return self.output_path

    def _prepare_internal_data(self):
        """将 SvgDocument 的 IR 转换为 v2 内部数据结构"""
        if not self.doc:
            self.doc = SvgDocument(self.svg_path)
            self.doc.parse()

        self._collect_symbol_boxes()

        # 从 SVG metadata 直接读取 ssjg（SvgDocument 的 container_id 可能为空）
        ssjg_map = {}
        if self.doc and self.doc.root is not None:
            for g in self.doc.root.iter(f'{{{SVG_NS}}}g'):
                md = g.find(f'{{{SVG_NS}}}metadata')
                if md is None:
                    continue
                psr = md.find(f'{{{IEC_NS}}}PSR_Ref')
                if psr is not None:
                    oid = psr.get('ObjectID', '')
                    sj = psr.get('ssjg', '') or ''
                    if oid and sj:
                        ssjg_map[oid] = sj

        for elem in self.doc.elements:
            pid = elem.element_id
            ptype = elem.psr_type or elem.layer_name
            pname = elem.element_name or ""
            ssjg = elem.container_id or ssjg_map.get(pid, '') or ""
            gls = elem.glink_refs
            sym = elem.symbol_href
            vcls = elem.css_class or "lkv10"
            orig_x, orig_y = elem.x, elem.y
            self.orig_pos[pid] = (orig_x, orig_y)
            self.devices[pid] = {
                'id': pid, 'type': ptype, 'name': pname,
                'ssjg': ssjg, 'glinks': gls, 'symbol': sym, 'vclass': vcls,
                'orig_x': orig_x, 'orig_y': orig_y,
                'layer': elem.layer_name
            }
            for gl in gls:
                self.gl_to_devs[gl].add(pid)

        self._build_adj()
        self._find_containers()
        self._assign_fallback_symbols()

        nd = sum(1 for d in self.devices.values() if self.is_real_device(d['type']))
        print(f"  [解析] 设备 {len(self.devices)} | 真实设备 {nd} | "
              f"GLink {len(self.gl_to_devs)} | 容器 {len(self.containers)} | "
              f"邻接边 {sum(len(v) for v in self.adj.values()) // 2}")

    def _collect_symbol_boxes(self):
        if self.doc.root is None:
            return
        defs = self.doc.root.find(f'{{{SVG_NS}}}defs')
        if defs is None:
            return
        TARGET_W = 28.0
        MAX_ORIG = 50.0
        for s in defs.findall(f'{{{SVG_NS}}}symbol'):
            sid = s.get('id', '')
            vb = s.get('viewBox', '0 0 8 6')
            vb_parts = vb.split()
            vb_w = float(vb_parts[2]) if len(vb_parts) == 4 else 8.0
            vb_h = float(vb_parts[3]) if len(vb_parts) == 4 else 6.0
            xs, ys = [], []
            for child in s.iter():
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                for attr in ('x', 'x1', 'x2', 'cx'):
                    v = child.get(attr)
                    if v:
                        try:
                            fv = float(v)
                            if abs(fv) <= MAX_ORIG:
                                xs.append(fv)
                        except ValueError:
                            pass
                for attr in ('y', 'y1', 'y2', 'cy'):
                    v = child.get(attr)
                    if v:
                        try:
                            fv = float(v)
                            if abs(fv) <= MAX_ORIG:
                                ys.append(fv)
                        except ValueError:
                            pass
                if tag == 'circle':
                    try:
                        cx = float(child.get('cx', 0))
                        cy = float(child.get('cy', 0))
                        r = float(child.get('r', 0))
                        if abs(cx) <= MAX_ORIG and r > 0:
                            xs += [cx - r, cx + r]
                            ys += [cy - r, cy + r]
                    except ValueError:
                        pass
                elif tag == 'ellipse':
                    try:
                        cx = float(child.get('cx', 0))
                        cy = float(child.get('cy', 0))
                        rx = float(child.get('rx', 0))
                        ry = float(child.get('ry', 0))
                        if abs(cx) <= MAX_ORIG and rx > 0:
                            xs += [cx - rx, cx + rx]
                            ys += [cy - ry, cy + ry]
                    except ValueError:
                        pass
                elif tag == 'rect':
                    try:
                        rx = float(child.get('x', 0))
                        ry = float(child.get('y', 0))
                        rw = float(child.get('width', 0))
                        rh = float(child.get('height', 0))
                        if abs(rx) <= MAX_ORIG and rw > 0:
                            xs += [rx, rx + rw]
                            ys += [ry, ry + rh]
                    except ValueError:
                        pass
                pts = child.get('points')
                if pts:
                    for pair in pts.split():
                        try:
                            px, py = pair.split(',')
                            fx, fy = float(px), float(py)
                            if abs(fx) <= MAX_ORIG:
                                xs.append(fx)
                            if abs(fy) <= MAX_ORIG:
                                ys.append(fy)
                        except ValueError:
                            pass
            if xs and ys:
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                w = max_x - min_x
                h = max_y - min_y
                if w < 0.5 or w > MAX_ORIG or h < 0.5 or h > MAX_ORIG:
                    w, h = vb_w, vb_h
                    min_x, max_x = 0, vb_w
                    min_y, max_y = 0, vb_h
            else:
                w, h = vb_w, vb_h
                min_x, max_x = 0, vb_w
                min_y, max_y = 0, vb_h
            cx = (min_x + max_x) / 2
            cy = (min_y + max_y) / 2
            scale = TARGET_W / w if w > 0.1 else SYM_SCALE
            scale = min(scale, 5.0)
            self.sym_box[sid] = {
                'cx': cx, 'cy': cy, 'w': w, 'h': h, 'scale': scale,
                'left': (min_x - cx) * scale, 'right': (max_x - cx) * scale,
                'top': (min_y - cy) * scale, 'bottom': (max_y - cy) * scale,
            }

    def _assign_fallback_symbols(self):
        # 设备类型 -> 符号关键词映射（用于符号归一化，确保同类型设备用同一符号）
        type_map = {
            '0201': 'LoadBreakSwitch', '0202': 'Disconnector',
            '0203': 'GroundDisconnector', '0302': 'Fuse',
            '0305': 'PotentialTransformer', '0306': 'CurrentTransformer',
            '0110': 'PowerTransformer', '0111': 'PowerTransformer',
            '0115': 'PoleCode', '0313': 'Junction', '0314': 'Junction',
            '0307': 'Breaker', '0309': 'CompositeSwitch',
            '370000': 'EnergyConsumer',
        }
        sym_by_kw = {}
        if self.doc and self.doc.root is not None:
            defs = self.doc.root.find(f'{{{SVG_NS}}}defs')
            if defs is not None:
                for s in defs.findall(f'{{{SVG_NS}}}symbol'):
                    sid = s.get('id', '')
                    for kw in set(type_map.values()):
                        if kw in sid and kw not in sym_by_kw:
                            sym_by_kw[kw] = sid
        # 符号归一化：同类型设备统一使用第一个匹配的符号，
        # 避免原始SVG中同类型多个UUID符号导致视觉不一致
        for pid, d in self.devices.items():
            kw = type_map.get(d['type'])
            if kw and kw in sym_by_kw:
                d['symbol'] = '#' + sym_by_kw[kw]

    def _build_adj(self):
        real_set = {pid for pid, d in self.devices.items() if self.is_real_device(d['type'])}
        gl_graph = defaultdict(set)
        for elem in self.doc.elements:
            if self.is_wire(elem.psr_type or elem.layer_name) and len(elem.glink_refs) >= 2:
                gls = elem.glink_refs
                for i in range(len(gls) - 1):
                    gl_graph[gls[i]].add(gls[i + 1])
                    gl_graph[gls[i + 1]].add(gls[i])
        for conn in self.doc.connections:
            if conn.start_device_id and conn.end_device_id:
                self.adj[conn.start_device_id].add(conn.end_device_id)
                self.adj[conn.end_device_id].add(conn.start_device_id)
        for pid in real_set:
            for start_gl in self.devices[pid]['glinks']:
                for other in self.gl_to_devs.get(start_gl, ()):
                    if other != pid and other in real_set:
                        self.adj[pid].add(other)
                        self.adj[other].add(pid)
                visited = {start_gl}
                q = deque([start_gl])
                while q:
                    cur = q.popleft()
                    for nxt in gl_graph.get(cur, ()):
                        if nxt in visited:
                            continue
                        visited.add(nxt)
                        hit = False
                        for other in self.gl_to_devs.get(nxt, ()):
                            if other != pid and other in real_set:
                                self.adj[pid].add(other)
                                self.adj[other].add(pid)
                                hit = True
                        if not hit:
                            q.append(nxt)

    def _find_containers(self):
        for pid, d in self.devices.items():
            if d['type'] in CONTAINER_TYPES:
                cid = d['ssjg'] or pid
                if cid not in self.containers:
                    self.containers[cid] = {'id': cid, 'name': d['name'],
                                            'type': d['type'], 'psr_id': pid, 'members': []}
        for pid, d in self.devices.items():
            s = d.get('ssjg', '')
            if not s or not self.is_real_device(d['type']):
                continue
            if s not in self.containers:
                self.containers[s] = {'id': s, 'name': '', 'type': 'zf08',
                                      'psr_id': None, 'members': []}
            if pid not in self.containers[s]['members']:
                self.containers[s]['members'].append(pid)
        for cid, c in self.containers.items():
            if c['name'] and not self.is_garbage_text(c['name']):
                continue
            best = ''
            for m in c['members']:
                nm = self.devices[m].get('name', '')
                if self.is_garbage_text(nm):
                    continue
                for sep in ['#', '~', '－', '_']:
                    if sep in nm:
                        cand = nm.split(sep)[0].strip('0').strip()
                        if len(cand) > 2 and len(cand) > len(best):
                            best = cand
                if any(k in nm for k in ['开关站', '环网柜', '配电室', '站房']):
                    best = nm
                    break
            c['name'] = best if best else f'柜_{cid[:6]}'
        self.containers = {k: v for k, v in self.containers.items()
                           if v['members'] or v.get('psr_id')}
        # 容器名去重
        name_count = defaultdict(int)
        for cid, c in self.containers.items():
            nm = c['name']
            name_count[nm] += 1
            if name_count[nm] > 1:
                c['name'] = f"{nm}#{name_count[nm]}"

    # ═══════════════════════════════════════════════════════════
    #  拓扑修复（完整：飞线修复 + 孤岛缝合 + 清理）
    # ═══════════════════════════════════════════════════════════

    def repair(self):
        real_set = {pid for pid, d in self.devices.items() if self.is_real_device(d['type'])}
        if not real_set:
            self.repair_stats = {"repaired": 0, "components_before": 0, "components_after": 0}
            return

        def find_components():
            visited = set()
            comps = []
            for start in real_set:
                if start in visited:
                    continue
                comp = set()
                q = deque([start])
                visited.add(start)
                while q:
                    u = q.popleft()
                    comp.add(u)
                    for v in self.adj.get(u, ()):
                        if v not in visited and v in real_set:
                            visited.add(v)
                            q.append(v)
                comps.append(comp)
            return comps

        comps_before = find_components()
        comps_before.sort(key=len, reverse=True)
        main_comp = set(comps_before[0]) if comps_before else set()

        repaired = 0
        DANGLE_THRESHOLD = 150.0
        STITCH_THRESHOLD = 250.0

        for comp in comps_before[1:]:
            if len(comp) != 1:
                continue
            node = next(iter(comp))
            if node not in self.orig_pos:
                continue
            nx, ny = self.orig_pos[node]
            best, best_d = None, float('inf')
            for other in main_comp:
                if other not in self.orig_pos:
                    continue
                ox, oy = self.orig_pos[other]
                d = math.hypot(nx - ox, ny - oy)
                if d < best_d:
                    best_d, best = d, other
            if best and best_d < DANGLE_THRESHOLD:
                self.adj[node].add(best)
                self.adj[best].add(node)
                main_comp.add(node)
                repaired += 1

        comps_mid = find_components()
        comps_mid.sort(key=len, reverse=True)
        for comp in comps_mid[1:]:
            if len(comp) < 2 or len(comp) > 8:
                continue
            best_pair, best_d = (None, None), float('inf')
            for a in comp:
                if a not in self.orig_pos:
                    continue
                ax, ay = self.orig_pos[a]
                for b in main_comp:
                    if b not in self.orig_pos:
                        continue
                    bx, by = self.orig_pos[b]
                    d = math.hypot(ax - bx, ay - by)
                    if d < best_d:
                        best_d, best_pair = d, (a, b)
            if best_pair[0] and best_d < STITCH_THRESHOLD:
                a, b = best_pair
                self.adj[a].add(b)
                self.adj[b].add(a)
                main_comp |= comp
                repaired += 1

        for u in list(self.adj.keys()):
            self.adj[u].discard(u)
            for v in list(self.adj[u]):
                self.adj[v].add(u)
        empty = [k for k, v in self.adj.items() if not v]
        for k in empty:
            del self.adj[k]

        comps_after = find_components()
        isolated = sum(1 for c in comps_after if len(c) == 1)
        self.repair_stats = {
            "repaired": repaired,
            "components_before": len(comps_before),
            "components_after": len(comps_after),
            "isolated_after": isolated,
        }
        print(f"  [修复] 补连 {repaired} 处 | 连通分量 {len(comps_before)}->{len(comps_after)} | 剩余孤立 {isolated}")

    # ═══════════════════════════════════════════════════════════
    #  权重树梳状布局（含未入树设备兜底）
    # ═══════════════════════════════════════════════════════════

    def layout(self):
        root = self._find_root()
        if not root:
            print("  [布局] 无有效根节点")
            return

        self.tree_parent = {root: None}
        level = {root: 0}
        q = deque([root])
        while q:
            u = q.popleft()
            for v in sorted(self.adj.get(u, ())):
                if v not in self.tree_parent:
                    self.tree_parent[v] = u
                    level[v] = level[u] + 1
                    self.tree_children[u].append(v)
                    q.append(v)

        self.non_tree_edges = []
        tree_edge_set = set()
        for child, par in self.tree_parent.items():
            if par is not None:
                tree_edge_set.add(tuple(sorted([child, par])))
        for u, neigh in self.adj.items():
            for v in neigh:
                if u >= v:
                    continue
                key = tuple(sorted([u, v]))
                if key not in tree_edge_set:
                    self.non_tree_edges.append((u, v))

        cont_rep = {}
        for cid, c in self.containers.items():
            ms = [m for m in c['members'] if m in self.tree_parent]
            if not ms:
                continue
            rep = min(ms, key=lambda m: level.get(m, 99999))
            cont_rep[cid] = rep

        DEV_SPAN = 140
        TRUNK_Y0 = MARGIN + 30
        LAYER_H = 150
        GROUP_GAP = 60

        weight = {}

        def calc_weight(node):
            kids = self.tree_children.get(node, [])
            if not kids:
                weight[node] = 1
                return 1
            w = sum(calc_weight(c) for c in kids)
            weight[node] = w
            return w
        calc_weight(root)

        main_child = {}
        for node in self.tree_parent:
            kids = self.tree_children.get(node, [])
            if kids:
                main_child[node] = max(kids, key=lambda c: weight[c])

        trunk_set = set()
        trunk_order = []
        node = root
        while node is not None:
            trunk_set.add(node)
            trunk_order.append(node)
            node = main_child.get(node)

        branch_depth = {}
        for n in self.tree_parent:
            d = 0
            cur = n
            while cur not in trunk_set and cur is not None:
                d += 1
                cur = self.tree_parent.get(cur)
            branch_depth[n] = d

        layers = defaultdict(list)
        for n in self.tree_parent:
            layers[branch_depth[n]].append(n)

        self.pos = {}
        for i, n in enumerate(trunk_order):
            self.pos[n] = (self.snap(MARGIN + i * DEV_SPAN), self.snap(TRUNK_Y0))

        max_depth = max(branch_depth.values()) if branch_depth else 0
        for depth in range(1, max_depth + 1):
            layer_nodes = layers[depth]
            if not layer_nodes:
                continue
            groups = defaultdict(list)
            for n in layer_nodes:
                groups[self.tree_parent[n]].append(n)
            sorted_parents = sorted(groups.keys(),
                                    key=lambda p: self.pos.get(p, (0, 0))[0])
            cur_x = MARGIN
            y = TRUNK_Y0 + depth * LAYER_H
            for par in sorted_parents:
                children = groups[par]
                par_x = self.pos[par][0]
                start_x = max(cur_x, par_x)
                for i, n in enumerate(children):
                    self.pos[n] = (self.snap(start_x + i * DEV_SPAN), self.snap(y))
                cur_x = start_x + len(children) * DEV_SPAN + GROUP_GAP

        # ★ 未入树设备兜底：排列在最下方，防止丢失
        placed = set(self.pos)
        leftover = [p for p, d in self.devices.items()
                    if self.is_real_device(d['type']) and p not in placed]
        if leftover:
            bx = max((p[0] for p in self.pos.values()), default=0) + DEV_SPAN
            by = TRUNK_Y0 + (max_depth + 1) * LAYER_H
            for i, pid in enumerate(leftover):
                self.pos[pid] = (self.snap(bx + i * DEV_SPAN), self.snap(by))

        self._layout_containers(cont_rep)
        self._normalize()

        print(f"  [布局] 放置 {len(self.pos)} | 容器框 {len(self.cont_box)} | "
              f"树深 {max(level.values())} | 根权重 {weight[root]}")

    def _find_root(self):
        buses = [p for p, d in self.devices.items() if d['type'] in BUSBAR_TYPES]
        if buses:
            return max(buses, key=lambda p: len(self.adj.get(p, ())))
        if self.adj:
            return max(self.adj, key=lambda p: len(self.adj[p]))
        return None

    def _layout_containers(self, cont_rep):
        CONT_ROW_H = 130
        CONT_TOP = 75
        CONT_W = 110
        for cid, c in self.containers.items():
            ms = [m for m in c['members'] if m in self.pos]
            if len(ms) < 2:
                continue
            rep = cont_rep.get(cid)
            if rep is None or rep not in self.pos:
                continue
            rx, ry = self.pos[rep]
            type_order = {'0311': 0, '0307': 1, '0201': 2, '0202': 3,
                          '0302': 4, '0306': 5, '0305': 6}
            buses = sorted([m for m in ms if self.devices[m]['type'] in BUSBAR_TYPES],
                           key=lambda m: type_order.get(self.devices[m]['type'], 9))
            rest = sorted([m for m in ms if m not in buses],
                          key=lambda m: type_order.get(self.devices[m]['type'], 9))
            ordered = buses + rest
            for i, pid in enumerate(ordered):
                self.pos[pid] = (self.snap(rx), self.snap(ry + i * CONT_ROW_H))
            xs = [self.pos[m][0] for m in ms]
            ys = [self.pos[m][1] for m in ms]
            cx = sum(xs) / len(xs)
            x1 = cx - CONT_W // 2
            x2 = cx + CONT_W // 2
            y1 = min(ys) - CONT_TOP
            y2 = max(ys) + CONT_PAD + UNIT_V // 2
            self.cont_box[cid] = (self.snap(x1), self.snap(y1), self.snap(x2), self.snap(y2))

        # ---- 容器碰撞避让：按x从左到右，右侧容器若与左侧容器y重叠且x重叠，则整体右移 ----
        sorted_cids = sorted(self.cont_box.keys(), key=lambda c: self.cont_box[c][0])
        GAP = 80  # 容器间最小水平间隙
        for idx, cid in enumerate(sorted_cids):
            if idx == 0:
                continue
            cx1, cy1, cx2, cy2 = self.cont_box[cid]
            # 找左边所有与当前容器y范围重叠的容器，取最大右边界
            need_x = cx1
            for left_cid in sorted_cids[:idx]:
                lx1, ly1, lx2, ly2 = self.cont_box[left_cid]
                # y范围不重叠则跳过
                if cy2 < ly1 or ly2 < cy1:
                    continue
                if lx2 + GAP > need_x:
                    need_x = lx2 + GAP
            if need_x > cx1:
                dx = need_x - cx1
                # 整体右移容器内所有设备
                ms = [m for m in self.containers[cid]['members'] if m in self.pos]
                for m in ms:
                    px, py = self.pos[m]
                    self.pos[m] = (self.snap(px + dx), py)
                # 重新计算容器框
                xs = [self.pos[m][0] for m in ms]
                ys = [self.pos[m][1] for m in ms]
                cxc = sum(xs) / len(xs)
                self.cont_box[cid] = (self.snap(cxc - CONT_W // 2), self.snap(min(ys) - CONT_TOP),
                                       self.snap(cxc + CONT_W // 2), self.snap(max(ys) + CONT_PAD + UNIT_V // 2))

        # ---- 容器顶部避让：检测容器顶部是否伸入上方设备层，有则整体下移 ----
        TOP_GAP = 35  # 容器顶部与上方设备层的最小间距
        # 收集所有设备的y坐标（按层去重，主干线横跨全图，包括其他容器成员）
        all_dev_ys = set()
        for pid, (px, py) in self.pos.items():
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            all_dev_ys.add(py)

        for cid in sorted(self.cont_box.keys(), key=lambda c: self.cont_box[c][1]):
            cx1, cy1, cx2, cy2 = self.cont_box[cid]
            ms = [m for m in self.containers[cid]['members'] if m in self.pos]
            if not ms:
                continue
            min_dev_y = min(self.pos[m][1] for m in ms)
            # 当前容器成员的y层（排除这些，因为它们在容器内部）
            self_ys = set(self.pos[m][1] for m in ms)
            # 找上方最近的设备层（最大y且 < min_dev_y，排除当前容器成员层）
            max_above_y = max((y for y in all_dev_ys if y < min_dev_y and y not in self_ys), default=-999999)
            if max_above_y == -999999:
                continue
            # 容器顶部 = min_dev_y - CONT_TOP，需与上方设备层间距 >= TOP_GAP
            needed_top = max_above_y + TOP_GAP
            current_top = min_dev_y - CONT_TOP
            if current_top < needed_top:
                dy = needed_top - current_top
                for m in ms:
                    px, py = self.pos[m]
                    self.pos[m] = (px, self.snap(py + dy))
                xs = [self.pos[m][0] for m in ms]
                ys = [self.pos[m][1] for m in ms]
                cxc = sum(xs) / len(xs)
                self.cont_box[cid] = (self.snap(cxc - CONT_W // 2), self.snap(min(ys) - CONT_TOP),
                                       self.snap(cxc + CONT_W // 2), self.snap(max(ys) + CONT_PAD + UNIT_V // 2))

        # ---- 非柜箱设备避让：不属于任何柜箱的设备若落在柜箱框内，则水平移出 ----
        cont_member_set = set()
        for cid, cdata in self.containers.items():
            for m in cdata.get('members', []):
                cont_member_set.add(m)
        DEV_HW_LOCAL = 15
        SIDE_GAP = 50  # 移出柜箱后与柜箱边框的最小间距
        for pid, (px, py) in list(self.pos.items()):
            if pid in cont_member_set:
                continue
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            # 检查是否落在某个柜箱框内（含标题栏，留5px余量）
            for cid, (cx1, cy1, cx2, cy2) in self.cont_box.items():
                if (px + DEV_HW_LOCAL > cx1 + 5 and px - DEV_HW_LOCAL < cx2 - 5 and
                        py + DEV_HH > cy1 + 5 and py - DEV_HH < cy2 - 5):
                    # 落在柜箱内，移到较近的一侧
                    dist_left = px - cx1
                    dist_right = cx2 - px
                    if dist_left <= dist_right:
                        new_x = cx1 - DEV_HW_LOCAL - SIDE_GAP
                    else:
                        new_x = cx2 + DEV_HW_LOCAL + SIDE_GAP
                    self.pos[pid] = (self.snap(new_x), py)
                    break

    def _normalize(self):
        if not self.pos:
            return
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        for (a, b, c, d) in self.cont_box.values():
            xs += [a, c]
            ys += [b, d]
        LABEL_PAD_X = 120  # 标注可能放在设备左右侧，预留水平空间防止越界
        ox, oy = -min(xs) + MARGIN + LABEL_PAD_X, -min(ys) + MARGIN
        self.pos = {p: (self.snap(x + ox), self.snap(y + oy)) for p, (x, y) in self.pos.items()}
        self.cont_box = {c: (self.snap(a + ox), self.snap(b + oy),
                            self.snap(c2 + ox), self.snap(d + oy))
                         for c, (a, b, c2, d) in self.cont_box.items()}

    # ═══════════════════════════════════════════════════════════
    #  渲染（正交布线 + 母线 + 标注白底避让）
    # ═══════════════════════════════════════════════════════════

    def render(self, out_path: str):
        if not self.pos:
            print("  [渲染] 无布局数据")
            return
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        for (a, b, c, d) in self.cont_box.values():
            xs += [a, c]
            ys += [b, d]
        LABEL_PAD_X = 120  # 与 _normalize 对齐：右侧标注预留空间
        W = self.snap(max(xs) + MARGIN + LABEL_PAD_X)
        H = self.snap(max(ys) + MARGIN)

        svg = ET.Element(f'{{{SVG_NS}}}svg', {
            'viewBox': f'0 0 {W} {H}',
            'width': str(W), 'height': str(H),
            'style': f'background-color:{C_BG};font-family:"Microsoft YaHei","SimHei",sans-serif;',
        })
        if self.doc and self.doc.root is not None:
            defs = self.doc.root.find(f'{{{SVG_NS}}}defs')
            if defs is not None:
                svg.append(copy.deepcopy(defs))

        cg = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'ConnLine_Layer'})
        self._draw_wires(cg)

        g = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'MainLayer'})
        self._draw_devices(g)
        self._draw_containers(g)
        self._draw_labels(g)

        ET.ElementTree(svg).write(out_path, encoding='utf-8', xml_declaration=True)
        print(f"  [渲染] {out_path}  {W} x {H}")

    def _draw_title(self, svg, W):
        tg = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'TitleBar'})
        ET.SubElement(tg, f'{{{SVG_NS}}}rect', {
            'x': '0', 'y': '0', 'width': str(W), 'height': str(TITLE_H),
            'fill': '#1a3a6b',
        })
        line_name = self.svg_filename.replace('.svg', '')
        t1 = ET.SubElement(tg, f'{{{SVG_NS}}}text', {
            'x': '16', 'y': '34', 'fill': '#fff',
            'font-size': str(F_TITLE), 'font-weight': 'bold',
        })
        t1.text = f'配电网单线图 — {line_name}（标准化美化）'
        ndev = len(self.pos)
        ncont = len(self.cont_box)
        ntie = len(self.non_tree_edges)
        t2 = ET.SubElement(tg, f'{{{SVG_NS}}}text', {
            'x': f'{W - 16}', 'y': '34', 'fill': '#aaccff',
            'font-size': str(F_BRANCH), 'text-anchor': 'end',
        })
        t2.text = f'设备 {ndev} | 柜箱 {ncont} | 联络 {ntie} | 10kV | 权重树算法'

    def _draw_containers(self, g):
        for cid, (x1, y1, x2, y2) in self.cont_box.items():
            c = self.containers.get(cid, {})
            name = c.get('name', f'柜_{cid[:6]}')
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': str(x1), 'y': str(y1),
                'width': str(x2 - x1), 'height': str(y2 - y1),
                'fill': 'none', 'stroke': C_CONTAINER,
                'stroke-width': str(W_CONTAINER), 'rx': '3',
            })
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': str(x1), 'y': str(y1),
                'width': str(x2 - x1), 'height': '16',
                'fill': '#f0f0f0', 'stroke': 'none', 'rx': '3',
            })
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': str(x1 + 4), 'y': str(y1 + 12),
                'fill': C_TEXT, 'font-size': '11', 'font-weight': 'bold',
            })
            t.text = name if len(name) <= 16 else name[:14] + '..'

    def _draw_wires(self, g):
        conn_idx = 0
        # 生成树边（主干+分支）
        for child, par in self.tree_parent.items():
            if par is None or child not in self.pos or par not in self.pos:
                continue
            x1, y1 = self.pos[par]
            x2, y2 = self.pos[child]
            is_trunk = (abs(y1 - y2) < GRID)
            w = W_TRUNK if (is_trunk or self.devices[par]['type'] in BUSBAR_TYPES
                            or self.devices[child]['type'] in BUSBAR_TYPES) else W_BRANCH
            _, r1, _, _ = self._dev_sym_edges(par)
            l2, _, _, _ = self._dev_sym_edges(child)
            conn_idx += 1
            conn_id = f'WIRE_{conn_idx:06d}'
            if is_trunk:
                points = [(x1, y1), (x1 + r1, y1), (x2 + l2, y2), (x2, y2)]
                self._polyline(g, points, C_10KV, w, conn_id=conn_id, from_id=par, to_id=child)
            else:
                points = [(x1, y1), (x1, y2), (x2 + l2, y2), (x2, y2)]
                self._polyline(g, points, C_10KV, w, conn_id=conn_id, from_id=par, to_id=child)

        # 母线：加粗横线
        drawn = set()
        for pid, d in self.devices.items():
            if d['type'] not in BUSBAR_TYPES or pid not in self.pos:
                continue
            conn = [p for p in self.adj.get(pid, ()) if p in self.pos]
            if not conn:
                continue
            xs = [self.pos[p][0] for p in conn]
            y = self.pos[pid][1]
            x1, x2 = min(xs) - 20, max(xs) + 20
            key = (self.snap(x1), self.snap(y))
            if key in drawn:
                continue
            drawn.add(key)
            conn_idx += 1
            self._polyline(g, [(x1, y), (x2, y)], C_BUSBAR, W_BUSBAR, conn_id=f'BUS_{conn_idx:06d}', from_id=pid)

        # ★ 环路补边：非树边（补回生成树算法丢弃的连接）
        # 颜色语义：仅“跨站房/跨馈线”才用联络橙 C_TIE；同容器/无容器/母线参与均属
        # 馈线内部连接，按主干/分支绿色绘制，避免单线图内部连线被误标为联络。
        drawn_pairs = set()
        for child, par in self.tree_parent.items():
            if par is not None:
                drawn_pairs.add(tuple(sorted([child, par])))
        for (u, v) in self.non_tree_edges:
            if u not in self.pos or v not in self.pos:
                continue
            key = tuple(sorted([u, v]))
            if key in drawn_pairs:
                continue
            drawn_pairs.add(key)
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            conn_idx += 1
            u_c = self.devices.get(u, {}).get('ssjg') or ''
            v_c = self.devices.get(v, {}).get('ssjg') or ''
            u_t = self.devices.get(u, {}).get('type', '')
            v_t = self.devices.get(v, {}).get('type', '')
            is_bus_edge = u_t in BUSBAR_TYPES or v_t in BUSBAR_TYPES
            is_internal = is_bus_edge or (not (u_c and v_c)) or (u_c == v_c)
            if is_internal:
                conn_id = f'WIRE_{conn_idx:06d}'
                edge_color = C_10KV
                edge_w = W_TRUNK if (abs(y1 - y2) < GRID or is_bus_edge) else W_BRANCH
            else:
                conn_id = f'TIE_{conn_idx:06d}'
                edge_color = C_TIE
                edge_w = W_TIE
            _, r1, _, _ = self._dev_sym_edges(u)
            l2, _, _, _ = self._dev_sym_edges(v)
            if abs(y1 - y2) < GRID * 2:
                points = [(x1, y1), (x1 + r1, y1), (x2 + l2, y2), (x2, y2)]
            elif abs(x1 - x2) < GRID * 2:
                points = [(x1, y1), (x1, y2), (x2 + l2, y2), (x2, y2)]
            else:
                mid_y = (y1 + y2) / 2
                points = [(x1, y1), (x1 + r1, y1), (x1 + r1, mid_y), (x2 + l2, mid_y), (x2 + l2, y2), (x2, y2)]
            self._polyline(g, points, edge_color, edge_w, conn_id=conn_id, from_id=u, to_id=v)

        # ★ 补充：原始 SVG 连接中未被 adj 图捕获的边（防止连线数量下降）
        for elem in self.doc.connections:
            s_id = elem.start_device_id
            e_id = elem.end_device_id
            if not s_id or not e_id or s_id == e_id:
                continue
            if s_id not in self.pos or e_id not in self.pos:
                continue
            key = tuple(sorted([s_id, e_id]))
            if key in drawn_pairs:
                continue
            drawn_pairs.add(key)
            x1, y1 = self.pos[s_id]
            x2, y2 = self.pos[e_id]
            conn_idx += 1
            conn_id = f'CONN_{conn_idx:06d}'
            _, r1, _, _ = self._dev_sym_edges(s_id)
            l2, _, _, _ = self._dev_sym_edges(e_id)
            if abs(y1 - y2) < GRID * 2:
                points = [(x1, y1), (x1 + r1, y1), (x2 + l2, y2), (x2, y2)]
            elif abs(x1 - x2) < GRID * 2:
                points = [(x1, y1), (x1, y2), (x2 + l2, y2), (x2, y2)]
            else:
                mid_y = (y1 + y2) / 2
                points = [(x1, y1), (x1 + r1, y1), (x1 + r1, mid_y), (x2 + l2, mid_y), (x2 + l2, y2), (x2, y2)]
            self._polyline(g, points, C_10KV, W_BRANCH, conn_id=conn_id, from_id=s_id, to_id=e_id)

    def _draw_devices(self, g):
        # 设备符号：白色背景与符号放在同一个 <g> 内，避免被解析器当作独立设备图元
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d:
                continue
            dg = ET.SubElement(g, f'{{{SVG_NS}}}g', {
                'transform': f'translate({x},{y})',
            })
            # 设备 metadata（ObjectName/PSRType 属性名对齐 IEC 规范）
            self._add_device_metadata(dg, pid)
            if d['type'] in BUSBAR_TYPES:
                # 母线视觉由 BUS_ 母线连线承担，仅输出 metadata 节点（图模一致）
                continue
            # 非母线设备：透明背景，符号独立渲染
            # 保留原始SVG背景色，禁止强制覆盖为纯白
            left, right, top, bottom = self._dev_sym_edges(pid)
            pad = 1.5
            ET.SubElement(dg, f'{{{SVG_NS}}}rect', {
                'x': f'{left - pad:.1f}', 'y': f'{top - pad:.1f}',
                'width': f'{right - left + 2 * pad:.1f}',
                'height': f'{bottom - top + 2 * pad:.1f}',
                'fill': 'none', 'stroke': 'none',  # 不强制白底，尊重原始SVG
            })
            if d.get('symbol'):
                sym = d['symbol'].lstrip('#')
                info = self.sym_box.get(sym)
                if info:
                    tr = f"scale({info['scale']:.4f}) translate({-info['cx']:.4f},{-info['cy']:.4f})"
                else:
                    tr = f'scale({SYM_SCALE}) translate(-4,-1.5)'
                ET.SubElement(dg, f'{{{SVG_NS}}}use', {
                    f'{{{XLINK_NS}}}href': d['symbol'], 'transform': tr,
                })
            else:
                ET.SubElement(dg, f'{{{SVG_NS}}}rect', {
                    'x': str(-DEV_HW), 'y': str(-DEV_HH),
                    'width': str(DEV_HW * 2), 'height': str(DEV_HH * 2),
                    'fill': 'none', 'stroke': C_SPARE, 'stroke-width': '1', 'rx': '2',
                })

    def _draw_labels(self, g):
        seen_names = set()
        # 收集所有设备符号包围盒，用于标注碰撞检测
        dev_bboxes = []
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d:
                continue
            left, right, top, bottom = self._dev_sym_edges(pid)
            dev_bboxes.append((x + left, y + top, x + right, y + bottom))
        # 加入柜箱标题栏作为障碍物，避免标注压标题栏
        for (cx1, cy1, cx2, cy2) in self.cont_box.values():
            dev_bboxes.append((cx1, cy1, cx2, cy1 + 20))

        def _bbox_overlap(a, b, pad=2):
            return not (a[2] + pad < b[0] or b[2] + pad < a[0] or
                        a[3] + pad < b[1] or b[3] + pad < a[1])

        placed_labels = []

        # 母线标注（母线在顶部，冲突少，直接放上方）
        for pid, d in self.devices.items():
            if d['type'] not in BUSBAR_TYPES or pid not in self.pos:
                continue
            name = self._display_name(d)
            if name in seen_names:
                continue
            seen_names.add(name)
            x, y = self.pos[pid]
            ly = y - DEV_HH - 6
            disp = name if len(name) <= 28 else name[:26] + '..'
            tw = max(len(disp) * F_BRANCH * 1.1, 20)
            placed_labels.append((x - tw / 2, ly - F_BRANCH + 2, x + tw / 2, ly + 2))
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': str(x), 'y': str(ly),
                'text-anchor': 'middle', 'font-size': str(F_BRANCH), 'fill': C_TEXT,
                'stroke': '#ffffff', 'stroke-width': '3.5', 'paint-order': 'stroke',
            })
            t.text = disp

        # 设备标注（带碰撞避让：上方 -> 下方 -> 左侧 -> 右侧）
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            name = self._display_name(d)
            if name in seen_names:
                continue
            seen_names.add(name)
            is_key = d['type'] in KEY_DEV_TYPES
            font_size = F_KEY if is_key else F_BRANCH
            weight = 'bold' if is_key else 'normal'
            disp = name if len(name) <= 14 else name[:12] + '..'
            tw = max(len(disp) * font_size * 1.1, 20)

            def _mk_bbox(cx, cy):
                return (cx - tw / 2, cy - font_size + 2, cx + tw / 2, cy + 2)

            def _conflict(bbox):
                for db in dev_bboxes:
                    if _bbox_overlap(bbox, db, pad=2):
                        return True
                for lb in placed_labels:
                    if _bbox_overlap(bbox, lb, pad=2):
                        return True
                return False

            # 候选位置：上方、下方、左侧、右侧、左上、右上、左下、右下
            candidates = [
                (x, y - DEV_HH - 6),
                (x, y + DEV_HH + 6 + font_size),
                (x - tw / 2 - 30, y),
                (x + tw / 2 + 30, y),
                (x - tw / 2 - 20, y - DEV_HH - 6),
                (x + tw / 2 + 20, y - DEV_HH - 6),
                (x - tw / 2 - 20, y + DEV_HH + 6 + font_size),
                (x + tw / 2 + 20, y + DEV_HH + 6 + font_size),
            ]
            lx, ly = candidates[0]
            best_overlap = float('inf')
            for cx, cy in candidates:
                bb = _mk_bbox(cx, cy)
                if not _conflict(bb):
                    lx, ly = cx, cy
                    break
                # 计算重叠面积，记录最小的
                ov = 0
                for db in dev_bboxes:
                    ox = min(bb[2], db[2]) - max(bb[0], db[0])
                    oy = min(bb[3], db[3]) - max(bb[1], db[1])
                    if ox > 0 and oy > 0:
                        ov += ox * oy
                for lb in placed_labels:
                    ox = min(bb[2], lb[2]) - max(bb[0], lb[0])
                    oy = min(bb[3], lb[3]) - max(bb[1], lb[1])
                    if ox > 0 and oy > 0:
                        ov += ox * oy
                if ov < best_overlap:
                    best_overlap = ov
                    lx, ly = cx, cy
            # 如果所有候选都冲突，用重叠最小的（上面已记录）

            placed_labels.append(_mk_bbox(lx, ly))

            lg = ET.SubElement(g, f'{{{SVG_NS}}}g')
            md = ET.SubElement(lg, f'{{{SVG_NS}}}metadata')
            ET.SubElement(md, f'{{{IEC_NS}}}PSR_Ref', {'ObjectID': f'TXT_{pid}'})
            t = ET.SubElement(lg, f'{{{SVG_NS}}}text', {
                'x': str(lx), 'y': str(ly), 'text-anchor': 'middle',
                'font-size': str(font_size), 'fill': C_TEXT, 'font-weight': weight,
                'stroke': '#ffffff', 'stroke-width': '3.5', 'paint-order': 'stroke',
            })
            t.text = disp

    def _dev_sym_edges(self, pid):
        d = self.devices.get(pid, {})
        sym = (d.get('symbol') or '').lstrip('#')
        info = self.sym_box.get(sym)
        if info:
            return info['left'], info['right'], info['top'], info['bottom']
        return -22.0, 22.0, -22.0, 22.0

    @staticmethod
    def _display_name(d):
        name = d.get('name', '')
        if name and not SvgBeautifier.is_garbage_text(name):
            return name if len(name) <= 24 else name[:22] + '..'
        type_names = {
            '0307': '断路器', '0201': '负荷开关', '0202': '隔离开关',
            '0203': '接地刀闸', '0302': '熔断器', '0305': '电压互感器',
            '0306': '电流互感器', '0110': '变压器', '0111': '配变',
            '0115': '杆塔', '0313': '电缆终端', '0314': '电缆终端',
            '370000': '用户', '0309': '避雷器',
        }
        tname = type_names.get(d.get('type', ''), '设备')
        pid = d.get('id', '')
        return f"{tname}_{pid[-4:]}" if pid else tname

    @staticmethod
    def _line(g, x1, y1, x2, y2, color, width):
        if abs(x1 - x2) < 1 and abs(y1 - y2) < 1:
            return
        ET.SubElement(g, f'{{{SVG_NS}}}line', {
            'x1': f'{x1:.0f}', 'y1': f'{y1:.0f}',
            'x2': f'{x2:.0f}', 'y2': f'{y2:.0f}',
            'stroke': color, 'stroke-width': str(width),
            'stroke-linecap': 'round',
        })

    @staticmethod
    def _polyline(g, points, color, width, conn_id=None, from_id=None, to_id=None):
        """用<g>包裹polyline渲染连接线，并添加metadata语义信息。
        端点必须靠近设备中心（距离<5.0），SvgParser才能匹配连接关系。
        """
        if len(points) < 2:
            return
        cg = ET.SubElement(g, f'{{{SVG_NS}}}g', {'id': conn_id or f'WIRE_{id(points):06d}'})
        pts_str = ' '.join(f'{x:.0f},{y:.0f}' for x, y in points)
        pl = ET.SubElement(cg, f'{{{SVG_NS}}}polyline', {
            'points': pts_str,
            'fill': 'none', 'stroke': color, 'stroke-width': str(width),
            'stroke-linecap': 'round', 'stroke-linejoin': 'round',
        })
        if from_id or to_id:
            md = ET.SubElement(cg, f'{{{SVG_NS}}}metadata')
            if from_id:
                ET.SubElement(md, f'{{{IEC_NS}}}Terminal', {'ObjectID': from_id, 'side': 'from'})
            if to_id:
                ET.SubElement(md, f'{{{IEC_NS}}}Terminal', {'ObjectID': to_id, 'side': 'to'})

    def _add_device_metadata(self, g, pid):
        """为设备图元添加metadata语义标签（ObjectID + ObjectName + PSRType + GLink_Ref）。
        对齐SVG制图规范：iec:PSR_Ref 属性名使用 ObjectName / PSRType 而非 Name / Type
        """
        d = self.devices.get(pid, {})
        md = ET.SubElement(g, f'{{{SVG_NS}}}metadata')
        ET.SubElement(md, f'{{{IEC_NS}}}PSR_Ref', {
            'ObjectID': pid,
            'ObjectName': d.get('name', ''),
            'PSRType': d.get('type', ''),
        })
        for gl in d.get('glinks', []):
            ET.SubElement(md, f'{{{IEC_NS}}}GLink_Ref', {'ObjectID': gl})


def beautify_svg_file(svg_path: str, output_path: str = None, quality_report: bool = True) -> str:
    """美化SVG文件，可选生成美化前后质量对比报告。

    Args:
        svg_path: 原始SVG路径
        output_path: 输出SVG路径，默认在同目录下生成 *_beautified.svg
        quality_report: 是否生成质量评分对比报告（任务一算法）
    """
    from data_io.svg_reader import SvgParser
    from svg_io.quality_scorer import evaluate_svg_quality, export_quality_report
    from types import SimpleNamespace

    if output_path is None:
        base, ext = os.path.splitext(svg_path)
        output_path = f"{base}_beautified{ext}"

    before_defects = before_summary = None
    if quality_report:
        try:
            doc_before = SvgParser.parse(svg_path)
            before_defects, before_summary = evaluate_svg_quality(doc_before, stage="美化前")
        except Exception as ex:
            print(f"  [质量] 美化前评估跳过: {ex}")

    beautifier = SvgBeautifier(svg_path, output_path=output_path)
    result = beautifier.beautify()

    if quality_report and before_summary is not None:
        try:
            # 先收集所有连接，为设备补充拓扑GLink互引（美化后连接都是真实拓扑连接）
            conns = []
            seen = set()
            topo_glinks = defaultdict(set)
            for u, neighbors in beautifier.adj.items():
                for v in neighbors:
                    key = tuple(sorted([u, v]))
                    if key in seen or u == v:
                        continue
                    seen.add(key)
                    topo_glinks[u].add(v)
                    topo_glinks[v].add(u)
                    pu = beautifier.pos.get(u, (0, 0))
                    pv = beautifier.pos.get(v, (0, 0))
                    conns.append(SimpleNamespace(
                        from_element_id=u, to_element_id=v,
                        line_id=f"edge_{u}_{v}",
                        points=[(pu[0], pu[1]), (pv[0], pv[1])],
                    ))
            elems = []
            for did, dev in beautifier.devices.items():
                # 【修复】不过滤：质量评分应使用全部设备（含装饰），使缺陷率能反映设备丢失问题
                pos = beautifier.pos.get(did, beautifier.orig_pos.get(did, (0, 0)))
                sym = beautifier.sym_box.get(did, {})
                glinks = set(dev.get('glinks', []))
                glinks.update(topo_glinks.get(did, set()))
                elems.append(SimpleNamespace(
                    element_id=did,
                    object_name=dev.get('name', ''),
                    element_type=dev.get('type', ''),
                    layer=dev.get('layer', ''),
                    x=pos[0], y=pos[1],
                    width=sym.get('w', 20), height=sym.get('h', 20),
                    glink_refs=list(glinks),
                ))
            doc_after = SimpleNamespace(elements=elems, connections=conns, texts={})
            after_defects, after_summary = evaluate_svg_quality(doc_after, stage="美化后")
            line_name = os.path.splitext(os.path.basename(svg_path))[0]
            report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "reports")
            report_path = os.path.join(report_dir, f"{line_name}_美化质量对比报告.json")
            export_quality_report(before_summary, after_summary, before_defects, after_defects, report_path)
        except Exception as ex:
            print(f"  [质量] 美化后评估跳过: {ex}")

    return result
