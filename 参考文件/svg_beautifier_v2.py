# -*- coding: utf-8 -*-
"""
配电网单线图 SVG 美化重构工具 v2
================================
基于权重树算法（专利 CN111090792B），严格遵循《SVG制图规范_代码落地闭环版》。

缺陷处理覆盖：
  线路类：正交布线、分层均匀出线、无悬空端点、拓扑连通
  设备类：柜内纵向单列、统一水平摆放、均匀间距
  标注类：字号分层、避让线路/设备、过滤乱码、去重、紧贴不重叠
  站房类：纵向排布、统一底部出线、站房名标注、深灰边框2px
  拓扑类：母线无缝衔接、线段两端有设备

规范数值：
  10kV = #00A854 电网绿 | 联络 = #FF6A00 高亮橙 | 跨站联络 = #722ED1
  主干 3px | 分支 1.5px | 联络 4.5px | 容器边框 2px #595959
  标题 21.3px bold | 关键设备 14px bold | 支线 12px | ID 10px
  网格 10px | 背景 #FFFFFF | 文字 #262626

用法：
  python svg_beautifier.py 输入.svg 输出.svg
"""

import xml.etree.ElementTree as ET
import copy
import sys
import os
import re
from collections import defaultdict, deque

# ═══════════════════════════════════════════════════════════
#  规范常量（严格按 SVG制图规范_代码落地闭环版）
# ═══════════════════════════════════════════════════════════
SVG_NS = 'http://www.w3.org/2000/svg'
XLINK_NS = 'http://www.w3.org/1999/xlink'
CIM_NS = 'http://iec.ch/TC57/2005/SVG-schema#'

# 颜色
C_BG = '#FFFFFF'
C_10KV = '#00A854'       # 电网绿 - 10kV主干
C_TIE = '#FF6A00'        # 高亮橙 - 联络线路/开关
C_CROSS_TIE = '#722ED1'  # 联络紫 - 跨站联络
C_SPARE = '#BFBFBF'      # 浅灰 - 备用间隔
C_CONTAINER = '#595959'  # 深灰 - 站房/容器边框
C_POWER_TRACE = '#1890FF' # 高亮蓝 - 电源追溯
C_TEXT = '#262626'       # 深黑灰 - 文字
C_BUSBAR = '#00A854'     # 母线同10kV色

# 线宽
W_TRUNK = 3.0     # 10kV主干馈线
W_BRANCH = 1.5    # 分支/柜内短线
W_TIE = 4.5       # 联络线路
W_SPARE = 1.0     # 备用间隔引线
W_CONTAINER = 2.0 # 站房/容器边框
W_BUSBAR = 4.0    # 母线加粗

# 字号
F_TITLE = 21.3    # 图纸标题/站房名
F_KEY = 14.0      # 关键一次设备
F_BRANCH = 12.0   # 支线设备/线路名称
F_ID = 10.0       # 设备唯一ID

# 布局
GRID = 10
MARGIN = 40
TITLE_H = 52
NODE_W = 56
UNIT_V = 14
H_GAP = 36
V_GAP = 4
CONT_PAD = 24
CONT_GAP = 16
SYM_SCALE = 3.5

WIRE_MARKERS = ('TMP', 'dxd')
BUSBAR_TYPES = {'0311'}
CONTAINER_TYPES = {'zf01', 'zf06', 'zf07', 'zf08'}
SWITCH_TYPES = {'0307', '0201', '0202', '0203', '0302', '0305', '0306', '0309'}
TRANSFORMER_TYPES = {'0110', '0111'}
KEY_DEV_TYPES = SWITCH_TYPES | TRANSFORMER_TYPES | BUSBAR_TYPES

# 乱码检测：含大量生僻字/无意义组合的标注
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
    r'行县',
    r'个行',
    r'行者劳',
    r'明\d*#',
    r'争\d',
    r'败诉',
    r'况诉',
]


def is_wire(t):
    return bool(t) and any(m in t for m in WIRE_MARKERS)

def is_real_device(t):
    if not t or is_wire(t):
        return False
    if t in CONTAINER_TYPES:
        return False
    if t in ('-1', '0'):
        return False
    return True

def is_garbage_text(text):
    """检测乱码/无意义标注"""
    if not text or len(text) < 2:
        return True
    if text.startswith('TMP') or re.match(r'^\d+$', text):
        return True
    for pat in GARBAGE_PATTERNS:
        if re.search(pat, text):
            return True
    # 00000开头 + 中文乱码组合（如"00000电站102-假社员教SUB020"）
    if text.startswith('000') and re.search(r'[\u4e00-\u9fff]{2,}', text):
        # 检查是否含有效关键词
        valid_kw = ['终端头', '电缆', '母线', '线路', '开关站', '环网柜', '配变',
                    '断路器', '隔离开关', '负荷开关', '熔断器', '杆塔', '变压器',
                    '站房', '配电室', 'LINE', 'SUB']
        if not any(kw in text for kw in valid_kw):
            return True
        # 含乱码模式的即使有关键词也过滤
        for pat in GARBAGE_PATTERNS:
            if re.search(pat, text):
                return True
    # 中英文混杂且含下划线的异常命名（非LINE）
    if re.search(r'[a-zA-Z]+_[\u4e00-\u9fff]', text) and 'LINE' not in text.upper():
        return True
    return False

def snap(v):
    """10px网格吸附"""
    return round(v / GRID) * GRID

def parse_svg_transform(transform_str):
    """解析SVG transform字符串，返回 (translate_x, translate_y)。
    支持 translate(x,y)、translate(x)、matrix(a,b,c,d,e,f)。"""
    if not transform_str:
        return 0.0, 0.0
    m = re.search(r'translate\(\s*([-\d.]+)\s*[, ]\s*([-\d.]+)\s*\)', transform_str)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r'translate\(\s*([-\d.]+)\s*\)', transform_str)
    if m:
        return float(m.group(1)), 0.0
    m = re.search(r'matrix\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)', transform_str)
    if m:
        return float(m.group(5)), float(m.group(6))
    return 0.0, 0.0


# ═══════════════════════════════════════════════════════════
#  主类
# ═══════════════════════════════════════════════════════════
class SVGBeautifier:
    def __init__(self, path):
        self.path = path
        ET.register_namespace('', SVG_NS)
        ET.register_namespace('xlink', XLINK_NS)
        ET.register_namespace('cim', CIM_NS)

        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.defs = self.root.find(f'{{{SVG_NS}}}defs')

        self.devices = {}
        self.gl_to_devs = defaultdict(set)
        self.containers = {}
        self.adj = defaultdict(set)
        self.pos = {}
        self.cont_box = {}
        self.tree_parent = {}
        self.tree_children = defaultdict(list)
        self.non_tree_edges = []
        self.label_rects = []  # 用于标注避让
        self.sym_box = {}      # symbol_id -> (viewBox_width, viewBox_height)
        self.orig_pos = {}     # 设备原始坐标 (x, y)，用于拓扑修复时的几何匹配
        self.repair_stats = {} # 修复统计

    # ────────────────── 1. 解析 ──────────────────
    def parse(self):
        for g in self.root.iter(f'{{{SVG_NS}}}g'):
            md = g.find(f'{{{SVG_NS}}}metadata')
            if md is None:
                continue
            psr = md.find(f'{{{CIM_NS}}}PSR_Ref')
            if psr is None:
                continue
            pid = psr.get('ObjectID', '')
            ptype = psr.get('PSRType', '')
            pname = psr.get('ObjectName', '') or ''
            ssjg = psr.get('ssjg', '') or ''
            gls = [e.get('ObjectID') for e in md.findall(f'{{{CIM_NS}}}GLink_Ref')
                   if e.get('ObjectID')]
            sym = None
            vcls = 'lkv10'
            use_e = g.find(f'{{{SVG_NS}}}use')
            if use_e is not None:
                sym = use_e.get(f'{{{XLINK_NS}}}href') or use_e.get('href')
                vcls = use_e.get('class', 'lkv10')
            else:
                poly_e = g.find(f'{{{SVG_NS}}}polyline')
                if poly_e is not None:
                    vcls = poly_e.get('class', 'lkv10')
            # ---- 读取原始坐标（用于拓扑修复的几何匹配）----
            gx, gy = parse_svg_transform(g.get('transform', ''))
            ux = uy = utx = uty = 0.0
            if use_e is not None:
                try:
                    ux = float(use_e.get('x', 0) or 0)
                    uy = float(use_e.get('y', 0) or 0)
                except (ValueError, TypeError):
                    pass
                utx, uty = parse_svg_transform(use_e.get('transform', ''))
            orig_x = gx + ux + utx
            orig_y = gy + uy + uty
            self.orig_pos[pid] = (orig_x, orig_y)
            self.devices[pid] = {
                'id': pid, 'type': ptype, 'name': pname,
                'ssjg': ssjg, 'glinks': gls, 'symbol': sym, 'vclass': vcls,
                'orig_x': orig_x, 'orig_y': orig_y,
            }
            for gl in gls:
                self.gl_to_devs[gl].add(pid)

        self._find_containers()
        self._build_adj()
        self._assign_fallback_symbols()
        self._collect_symbol_boxes()

        nd = sum(1 for d in self.devices.values() if is_real_device(d['type']))
        print(f"[解析] 元素 {len(self.devices)} | 真实设备 {nd} | "
              f"GLink {len(self.gl_to_devs)} | 容器 {len(self.containers)} | "
              f"邻接边 {sum(len(v) for v in self.adj.values()) // 2}")

    def _find_containers(self):
        for pid, d in self.devices.items():
            if d['type'] in CONTAINER_TYPES:
                cid = d['ssjg'] or pid
                if cid not in self.containers:
                    self.containers[cid] = {'id': cid, 'name': d['name'],
                                            'type': d['type'], 'psr_id': pid,
                                            'members': []}
        for pid, d in self.devices.items():
            s = d.get('ssjg', '')
            if not s or not is_real_device(d['type']):
                continue
            if s not in self.containers:
                self.containers[s] = {'id': s, 'name': '', 'type': 'zf08',
                                      'psr_id': None, 'members': []}
            if pid not in self.containers[s]['members']:
                self.containers[s]['members'].append(pid)
        # 推断名称
        for cid, c in self.containers.items():
            if c['name'] and not is_garbage_text(c['name']):
                continue
            best = ''
            for m in c['members']:
                nm = self.devices[m].get('name', '')
                if is_garbage_text(nm):
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
        # 容器名去重：重名加序号
        name_count = defaultdict(int)
        for cid, c in self.containers.items():
            nm = c['name']
            name_count[nm] += 1
            if name_count[nm] > 1:
                c['name'] = f"{nm}#{name_count[nm]}"

    def _build_adj(self):
        real_set = {pid for pid, d in self.devices.items() if is_real_device(d['type'])}
        gl_graph = defaultdict(set)
        for d in self.devices.values():
            if is_wire(d['type']) and len(d['glinks']) >= 2:
                gls = d['glinks']
                for i in range(len(gls) - 1):
                    gl_graph[gls[i]].add(gls[i + 1])
                    gl_graph[gls[i + 1]].add(gls[i])
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

    def _assign_fallback_symbols(self):
        type_map = {
            '0201': 'Disconnector', '0202': 'Disconnector',
            '0203': 'GroundDisconnector', '0302': 'Fuse',
            '0305': 'PotentialTransformer', '0306': 'CurrentTransformer',
            '0110': 'PowerTransformer', '0111': 'PowerTransformer',
            '0115': 'PoleCode', '0313': 'Junction', '0314': 'Junction',
            '0307': 'Breaker', '370000': 'EnergyConsumer',
        }
        sym_by_kw = {}
        if self.defs is not None:
            for s in self.defs.findall(f'{{{SVG_NS}}}symbol'):
                sid = s.get('id', '')
                for kw in set(type_map.values()):
                    if kw in sid and kw not in sym_by_kw:
                        sym_by_kw[kw] = sid
        for pid, d in self.devices.items():
            if d.get('symbol'):
                continue
            kw = type_map.get(d['type'])
            if kw and kw in sym_by_kw:
                d['symbol'] = '#' + sym_by_kw[kw]

    def _collect_symbol_boxes(self):
        """收集每个symbol的实际图形边界框，过滤异常大坐标，计算居中和缩放。"""
        if self.defs is None:
            return
        TARGET_W = 28.0  # 目标符号宽度（像素）
        MAX_ORIG = 50.0  # 原始坐标最大合理值，超过视为异常
        for s in self.defs.findall(f'{{{SVG_NS}}}symbol'):
            sid = s.get('id', '')
            vb = s.get('viewBox', '0 0 8 6')
            vb_parts = vb.split()
            vb_w = float(vb_parts[2]) if len(vb_parts) == 4 else 8.0
            vb_h = float(vb_parts[3]) if len(vb_parts) == 4 else 6.0
            # 收集所有子元素的坐标（含circle半径、rect宽高等）
            xs, ys = [], []
            for child in s.iter():
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                for attr in ('x', 'x1', 'x2', 'cx'):
                    v = child.get(attr)
                    if v:
                        try:
                            fv = float(v)
                            if abs(fv) <= MAX_ORIG: xs.append(fv)
                        except ValueError: pass
                for attr in ('y', 'y1', 'y2', 'cy'):
                    v = child.get(attr)
                    if v:
                        try:
                            fv = float(v)
                            if abs(fv) <= MAX_ORIG: ys.append(fv)
                        except ValueError: pass
                # circle: 半径扩展
                if tag == 'circle':
                    try:
                        cx = float(child.get('cx', 0))
                        cy = float(child.get('cy', 0))
                        r = float(child.get('r', 0))
                        if abs(cx) <= MAX_ORIG and r > 0:
                            xs += [cx - r, cx + r]
                            ys += [cy - r, cy + r]
                    except ValueError: pass
                # ellipse: rx/ry扩展
                elif tag == 'ellipse':
                    try:
                        cx = float(child.get('cx', 0))
                        cy = float(child.get('cy', 0))
                        rx = float(child.get('rx', 0))
                        ry = float(child.get('ry', 0))
                        if abs(cx) <= MAX_ORIG and rx > 0:
                            xs += [cx - rx, cx + rx]
                            ys += [cy - ry, cy + ry]
                    except ValueError: pass
                # rect: width/height扩展
                elif tag == 'rect':
                    try:
                        rx = float(child.get('x', 0))
                        ry = float(child.get('y', 0))
                        rw = float(child.get('width', 0))
                        rh = float(child.get('height', 0))
                        if abs(rx) <= MAX_ORIG and rw > 0:
                            xs += [rx, rx + rw]
                            ys += [ry, ry + rh]
                    except ValueError: pass
                # polyline/polygon points
                pts = child.get('points')
                if pts:
                    for pair in pts.split():
                        try:
                            px, py = pair.split(',')
                            fx, fy = float(px), float(py)
                            if abs(fx) <= MAX_ORIG: xs.append(fx)
                            if abs(fy) <= MAX_ORIG: ys.append(fy)
                        except ValueError: pass
            # 用图形边界框，异常时回退到viewBox
            if xs and ys:
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                w = max_x - min_x
                h = max_y - min_y
                # 如果图形框太小或太大，回退viewBox
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
            scale = TARGET_W / w if w > 0.1 else 3.5
            # 限制最大缩放
            scale = min(scale, 5.0)
            self.sym_box[sid] = {
                'cx': cx, 'cy': cy, 'w': w, 'h': h,
                'scale': scale,
                'left': (min_x - cx) * scale,
                'right': (max_x - cx) * scale,
                'top': (min_y - cy) * scale,
                'bottom': (max_y - cy) * scale,
            }

    def _dev_sym_edges(self, pid):
        """返回元件符号缩放后的左右上下边缘（相对于元件中心坐标）。"""
        d = self.devices.get(pid, {})
        sym = (d.get('symbol') or '').lstrip('#')
        info = self.sym_box.get(sym)
        if info:
            return info['left'], info['right'], info['top'], info['bottom']
        # fallback: 默认 30x20
        return -15.0, 15.0, -10.0, 10.0

    # ────────────────── 1.5 拓扑修复（集成自 topology_repairer 算法）──────────────────
    def repair(self):
        """拓扑修复流水线：在解析后、布局前运行。
        借鉴 topology_repairer.py 核心算法，基于原始几何坐标补全连接：
          1. 飞线/悬空端点修复：无连接设备匹配最近设备补连
          2. 拓扑孤岛缝合：小连通分量缝合到主分量
          3. 虚假连接清理：去自环、保对称
          4. 连通质量统计
        仅修正内存中的邻接表 self.adj，不修改原始SVG。
        """
        import math
        real_set = {pid for pid, d in self.devices.items() if is_real_device(d['type'])}
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
        DANGLE_THRESHOLD = 150
        STITCH_THRESHOLD = 250

        # 1. 飞线修复：孤立节点连接到最近主分量设备
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

        # 2. 孤岛缝合：2~8节点小分量缝合到主分量
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

        # 3. 清理：去自环、确保对称
        for u in list(self.adj.keys()):
            self.adj[u].discard(u)
            for v in list(self.adj[u]):
                self.adj[v].add(u)
        empty = [k for k, v in self.adj.items() if not v]
        for k in empty:
            del self.adj[k]

        # 4. 统计
        comps_after = find_components()
        isolated = sum(1 for c in comps_after if len(c) == 1)
        self.repair_stats = {
            "repaired": repaired,
            "components_before": len(comps_before),
            "components_after": len(comps_after),
            "isolated_after": isolated,
        }
        print(f"[修复] 补连 {repaired} 处 | 连通分量 {len(comps_before)}->{len(comps_after)} | 剩余孤立 {isolated}")

    # ────────────────── 2. 梳状布局（电路图风格）──────────────────
    def layout(self):
        """梳状布局：主干水平延伸，所有分支在主干下方独立垂直车道排列。
        1. 沿最大权重子节点找到主干路径
        2. 主干设备沿水平线排列
        3. 所有分支（含子分支）在主干下方按车道堆叠
        4. 分支内部递归同样逻辑
        """
        root = self._find_root()
        if not root:
            print("[布局] 无有效根节点")
            return

        # BFS 生成树
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

        # 容器代表节点
        cont_rep = {}
        for cid, c in self.containers.items():
            ms = [m for m in c['members'] if m in self.tree_parent]
            if not ms:
                continue
            rep = min(ms, key=lambda m: level.get(m, 99999))
            cont_rep[cid] = rep

        # 布局参数
        DEV_SPAN = 110   # 同层元件水平间距（增大避免长标注重叠）
        TRUNK_Y0 = MARGIN + TITLE_H + 70
        LAYER_H = 120    # 层间距
        GROUP_GAP = 60   # 同层不同父节点组之间的间隙

        # 子树权重
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

        # 主干子节点 = 权重最大的子节点
        main_child = {}
        for node in self.tree_parent:
            kids = self.tree_children.get(node, [])
            if kids:
                main_child[node] = max(kids, key=lambda c: weight[c])

        # 找出主干路径
        trunk_set = set()
        trunk_order = []
        node = root
        while node is not None:
            trunk_set.add(node)
            trunk_order.append(node)
            node = main_child.get(node)

        # 计算每个节点的分支深度（距离主干的跳数）
        branch_depth = {}
        for n in self.tree_parent:
            d = 0
            cur = n
            while cur not in trunk_set and cur is not None:
                d += 1
                cur = self.tree_parent.get(cur)
            branch_depth[n] = d

        # 按层分组
        layers = defaultdict(list)
        for n in self.tree_parent:
            layers[branch_depth[n]].append(n)

        # 分层布局：每层固定y，元件水平排列，不换行
        self.pos = {}
        # 主干层（depth=0）
        for i, n in enumerate(trunk_order):
            self.pos[n] = (snap(MARGIN + i * DEV_SPAN), snap(TRUNK_Y0))

        # 分支层：每层固定y，按父节点分组排列
        max_depth = max(branch_depth.values()) if branch_depth else 0
        for depth in range(1, max_depth + 1):
            layer_nodes = layers[depth]
            if not layer_nodes:
                continue
            # 按父节点分组
            groups = defaultdict(list)
            for n in layer_nodes:
                groups[self.tree_parent[n]].append(n)
            # 按父节点x排序组
            sorted_parents = sorted(groups.keys(),
                                    key=lambda p: self.pos.get(p, (0, 0))[0])
            cur_x = MARGIN
            y = TRUNK_Y0 + depth * LAYER_H
            for par in sorted_parents:
                children = groups[par]
                par_x = self.pos[par][0]
                # 组起始x不小于父节点x，也不小于当前光标
                start_x = max(cur_x, par_x)
                for i, n in enumerate(children):
                    self.pos[n] = (snap(start_x + i * DEV_SPAN), snap(y))
                cur_x = start_x + len(children) * DEV_SPAN + GROUP_GAP

        # 未入树设备
        placed = set(self.pos)
        leftover = [p for p, d in self.devices.items()
                    if is_real_device(d['type']) and p not in placed]
        if leftover:
            bx = max((p[0] for p in self.pos.values()), default=0) + DEV_SPAN
            by = TRUNK_Y0 + (max_depth + 1) * LAYER_H
            for i, pid in enumerate(leftover):
                self.pos[pid] = (snap(bx + i * DEV_SPAN), snap(by))

        # 容器内部纵向布局
        self._layout_containers(cont_rep)

        # 归一化
        self._normalize()

        print(f"[布局] 放置 {len(self.pos)} | 容器框 {len(self.cont_box)} | "
              f"树深 {max(level.values())} | 根权重 {weight[root]}")

    def _find_root(self):
        buses = [p for p, d in self.devices.items() if d['type'] in BUSBAR_TYPES]
        if buses:
            return max(buses, key=lambda p: len(self.adj.get(p, ())))
        if self.adj:
            return max(self.adj, key=lambda p: len(self.adj[p]))
        return None

    def _layout_containers(self, cont_rep):
        """柜箱内部：纵向单列排布，母线在顶部，开关依次向下，统一底部出线。"""
        CONT_ROW_H = 68   # 容器内每行高度（含标注空间，避免重叠）
        CONT_TOP = 55     # 容器顶部留白（标签栏+首行标注）
        CONT_W = 110      # 容器固定宽度（容纳标注）
        for cid, c in self.containers.items():
            ms = [m for m in c['members'] if m in self.pos]
            if len(ms) < 2:
                continue
            rep = cont_rep.get(cid)
            if rep is None or rep not in self.pos:
                continue
            rx, ry = self.pos[rep]

            # 排序：母线→断路器→负荷开关→隔离开关→其他
            type_order = {'0311': 0, '0307': 1, '0201': 2, '0202': 3,
                          '0302': 4, '0306': 5, '0305': 6}
            buses = sorted([m for m in ms if self.devices[m]['type'] in BUSBAR_TYPES],
                           key=lambda m: type_order.get(self.devices[m]['type'], 9))
            rest = sorted([m for m in ms if m not in buses],
                          key=lambda m: type_order.get(self.devices[m]['type'], 9))
            ordered = buses + rest

            for i, pid in enumerate(ordered):
                self.pos[pid] = (snap(rx), snap(ry + i * CONT_ROW_H))

            xs = [self.pos[m][0] for m in ms]
            ys = [self.pos[m][1] for m in ms]
            cx = sum(xs) / len(xs)
            x1 = cx - CONT_W // 2
            x2 = cx + CONT_W // 2
            y1 = min(ys) - CONT_TOP
            y2 = max(ys) + CONT_PAD + UNIT_V // 2
            self.cont_box[cid] = (snap(x1), snap(y1), snap(x2), snap(y2))

    def _normalize(self):
        if not self.pos:
            return
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        for (a, b, c, d) in self.cont_box.values():
            xs += [a, c]
            ys += [b, d]
        ox, oy = -min(xs) + MARGIN, -min(ys) + MARGIN + TITLE_H
        self.pos = {p: (snap(x + ox), snap(y + oy)) for p, (x, y) in self.pos.items()}
        self.cont_box = {c: (snap(a + ox), snap(b + oy), snap(c2 + ox), snap(d + oy))
                         for c, (a, b, c2, d) in self.cont_box.items()}

    # ────────────────── 3. 渲染 ──────────────────
    # 元件占位半尺寸（符号放大后约 28x20）
    DEV_HW = 15   # 半宽
    DEV_HH = 10   # 半高

    def render(self, out_path):
        if not self.pos:
            print("[渲染] 无布局数据")
            return
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        for (a, b, c, d) in self.cont_box.values():
            xs += [a, c]
            ys += [b, d]
        W = snap(max(xs) + MARGIN)
        H = snap(max(ys) + MARGIN)

        svg = ET.Element(f'{{{SVG_NS}}}svg', {
            'viewBox': f'0 0 {W} {H}',
            'width': f'{W}', 'height': f'{H}',
            'style': f'background-color:{C_BG};font-family:"Microsoft YaHei","SimHei",sans-serif;',
        })
        if self.defs is not None:
            svg.append(copy.deepcopy(self.defs))

        self._draw_title(svg, W, os.path.basename(out_path))

        g = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'MainLayer'})
        self._draw_containers(g)
        self._draw_wires(g)       # 先画导线（接元件边缘）
        self._draw_devices(g)     # 再画元件（白底覆盖）
        self._draw_labels(g)      # 最后画标注（元件上方空白处）

        ET.ElementTree(svg).write(out_path, encoding='utf-8', xml_declaration=True)
        print(f"[渲染] {out_path}  {W} x {H}")

    def _draw_title(self, svg, W, fname):
        tg = ET.SubElement(svg, f'{{{SVG_NS}}}g', {'id': 'TitleBar'})
        ET.SubElement(tg, f'{{{SVG_NS}}}rect', {
            'x': '0', 'y': '0', 'width': f'{W}', 'height': str(TITLE_H),
            'fill': '#1a3a6b',
        })
        line_name = fname.replace('_beautified', '').replace('.svg', '')
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
            # 容器框：深灰2px实线
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': f'{x1}', 'y': f'{y1}',
                'width': f'{x2 - x1}', 'height': f'{y2 - y1}',
                'fill': '#ffffff', 'stroke': C_CONTAINER,
                'stroke-width': str(W_CONTAINER), 'rx': '3',
            })
            # 站房名：框内左上角，带浅底色条
            label_h = 16
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': f'{x1}', 'y': f'{y1}',
                'width': f'{x2 - x1}', 'height': str(label_h),
                'fill': '#f0f0f0', 'stroke': 'none', 'rx': '3',
            })
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': f'{x1 + 4}', 'y': f'{y1 + 12}',
                'fill': C_TEXT, 'font-size': '11',
                'font-weight': 'bold',
            })
            t.text = name if len(name) <= 16 else name[:14] + '..'

    def _draw_wires(self, g):
        """绘制所有导线：端点精确接元件边缘。
        同层：水平线，父右边缘→子左边缘
        跨层：从父中心垂直向下到子层，再水平到子左边缘（T接）
        """
        for child, par in self.tree_parent.items():
            if par is None or child not in self.pos or par not in self.pos:
                continue
            x1, y1 = self.pos[par]
            x2, y2 = self.pos[child]
            is_trunk = (abs(y1 - y2) < GRID)
            w = W_TRUNK if (is_trunk or self.devices[par]['type'] in BUSBAR_TYPES
                            or self.devices[child]['type'] in BUSBAR_TYPES) else W_BRANCH

            _, r1, _, b1 = self._dev_sym_edges(par)
            l2, _, t2, _ = self._dev_sym_edges(child)

            if is_trunk:
                # 同层水平线：父右边缘 → 子左边缘
                self._line(g, x1 + r1, y1, x2 + l2, y2, C_10KV, w)
            else:
                # 跨层T接：从父中心垂直向下到子层，再水平到子左边缘
                self._line(g, x1, y1, x1, y2, C_10KV, w)
                self._line(g, x1, y2, x2 + l2, y2, C_10KV, w)

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
            key = (snap(x1), snap(y))
            if key in drawn:
                continue
            drawn.add(key)
            self._line(g, x1, y, x2, y, C_BUSBAR, W_BUSBAR)

    @staticmethod
    def _display_name(d):
        """返回设备的显示名称：原名有效则用原名，否则用类型名+ID后4位。"""
        name = d.get('name', '')
        if name and not is_garbage_text(name):
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

    def _draw_devices(self, g):
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            dg = ET.SubElement(g, f'{{{SVG_NS}}}g', {
                'transform': f'translate({x},{y})',
            })
            # 白底矩形：精确匹配符号边界框
            left, right, top, bottom = self._dev_sym_edges(pid)
            pad = 1.5  # 稍微大一点确保完全覆盖
            ET.SubElement(dg, f'{{{SVG_NS}}}rect', {
                'x': f'{left - pad:.1f}', 'y': f'{top - pad:.1f}',
                'width': f'{right - left + 2*pad:.1f}', 'height': f'{bottom - top + 2*pad:.1f}',
                'fill': '#ffffff', 'stroke': 'none',
            })
            if d.get('symbol'):
                sym = d['symbol'].lstrip('#')
                info = self.sym_box.get(sym)
                if info:
                    # 先平移到符号中心，再缩放
                    tr = f"scale({info['scale']:.4f}) translate({-info['cx']:.4f},{-info['cy']:.4f})"
                else:
                    tr = f'scale({SYM_SCALE}) translate(-4,-1.5)'
                ET.SubElement(dg, f'{{{SVG_NS}}}use', {
                    f'{{{XLINK_NS}}}href': d['symbol'],
                    'transform': tr,
                })
            else:
                ET.SubElement(dg, f'{{{SVG_NS}}}rect', {
                    'x': f'{-self.DEV_HW}', 'y': f'{-self.DEV_HH}',
                    'width': str(self.DEV_HW * 2), 'height': str(self.DEV_HH * 2),
                    'fill': 'none', 'stroke': C_SPARE, 'stroke-width': '1', 'rx': '2',
                })

    def _draw_labels(self, g):
        """标注：统一放在元件上方空白处，不压线不压元件。"""
        seen_names = set()
        # 母线标注
        for pid, d in self.devices.items():
            if d['type'] not in BUSBAR_TYPES or pid not in self.pos:
                continue
            name = self._display_name(d)
            if name in seen_names:
                continue
            seen_names.add(name)
            x, y = self.pos[pid]
            ly = y - self.DEV_HH - 6
            disp = name if len(name) <= 28 else name[:26] + '..'
            tw = max(len(disp) * F_BRANCH * 0.95, 20)
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': f'{x - tw/2:.1f}', 'y': f'{ly - F_BRANCH + 2:.1f}',
                'width': f'{tw:.1f}', 'height': f'{F_BRANCH + 2:.1f}',
                'fill': '#ffffff', 'stroke': 'none',
            })
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': f'{x}', 'y': f'{ly}',
                'text-anchor': 'middle', 'font-size': str(F_BRANCH),
                'fill': C_TEXT,
            })
            t.text = disp

        # 设备标注：元件正上方
        for pid, (x, y) in self.pos.items():
            d = self.devices.get(pid)
            if not d or d['type'] in BUSBAR_TYPES:
                continue
            name = self._display_name(d)
            if name in seen_names:
                continue
            seen_names.add(name)

            is_key = d['type'] in KEY_DEV_TYPES
            in_cont = any(pid in c['members'] for c in self.containers.values())
            font_size = F_KEY if is_key else F_BRANCH
            weight = 'bold' if is_key else 'normal'

            # 标注位置：元件正上方
            ly = y - self.DEV_HH - 6
            disp = name if len(name) <= 14 else name[:12] + '..'
            # 白底：避免文字和导线视觉重叠
            tw = max(len(disp) * font_size * 0.95, 20)
            ET.SubElement(g, f'{{{SVG_NS}}}rect', {
                'x': f'{x - tw/2:.1f}', 'y': f'{ly - font_size + 2:.1f}',
                'width': f'{tw:.1f}', 'height': f'{font_size + 2:.1f}',
                'fill': '#ffffff', 'stroke': 'none',
            })
            t = ET.SubElement(g, f'{{{SVG_NS}}}text', {
                'x': f'{x}', 'y': f'{ly}', 'text-anchor': 'middle',
                'font-size': str(font_size), 'fill': C_TEXT,
                'font-weight': weight,
            })
            t.text = disp

    # ────────────────── 入口 ──────────────────
    def run(self, out):
        self.parse()
        self.repair()
        self.layout()
        self.render(out)
        return out


def main():
    inp = sys.argv[1] if len(sys.argv) > 1 else 'input.svg'
    out = sys.argv[2] if len(sys.argv) > 2 else 'output.svg'
    if not os.path.exists(inp):
        print(f"错误：找不到 {inp}")
        sys.exit(1)
    SVGBeautifier(inp).run(out)
    print("完成！")


if __name__ == '__main__':
    main()
