<<<<<<< HEAD
import sys
import os
import re
import json
import math
import pandas as pd
from xml.etree import ElementTree as ET

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config.settings import OUTPUT_JSON, OUTPUT_CSV

NS_MAP = {
    'ns0': 'http://www.w3.org/2000/svg',
    'ns1': 'http://www.w3.org/1999/xlink',
    'ns2': 'http://iec.ch/TC57/2005/SVG-schema#'
}

LAYER_TYPE_MAP = {
    'PowerTransformer_Layer': 'PowerTransformer',
    'Breaker_Layer': 'Breaker',
    'Disconnector_Layer': 'Disconnector',
    'LoadBreakSwitch_Layer': 'LoadBreakSwitch',
    'CompositeSwitch_Layer': 'CompositeSwitch',
    'Fuse_Layer': 'Fuse',
    'Junction_Layer': 'Junction',
    'PoleCode_Layer': 'PoleCode',
    'EnergyConsumer_Layer': 'EnergyConsumer',
    'PotentialTransformer_Layer': 'PotentialTransformer',
    'CurrentTransformer_Layer': 'CurrentTransformer',
    'GroundDisconnector_Layer': 'GroundDisconnector',
    'RemoteUnit_Layer': 'RemoteUnit',
    'BusbarSection_Layer': 'BusbarSection',
    'Substation_Layer': 'Substation',
    'ACLineSegment_Layer': 'ACLineSegment',
    'ConnLine_Layer': 'ConnLine',
    'Other_Layer': 'Other',
}

TYPE_NAME_MAP = {
    'Breaker': '断路器',
    'PowerTransformer': '变压器',
    'Disconnector': '隔离开关',
    'LoadBreakSwitch': '负荷开关',
    'CompositeSwitch': '组合开关',
    'Fuse': '熔断器',
    'Junction': '连接点',
    'PoleCode': '杆塔',
    'EnergyConsumer': '负荷',
    'PotentialTransformer': '电压互感器',
    'CurrentTransformer': '电流互感器',
    'GroundDisconnector': '接地刀闸',
    'RemoteUnit': '终端设备',
    'BusbarSection': '母线',
    'Substation': '站房',
    'ACLineSegment': '交流线段',
    'ConnLine': '连接线',
    'Other': '其他'
}


def parse_transform(transform_str, x, y):
    if not transform_str:
        return x, y
    
    current_x, current_y = float(x), float(y)
    
    transforms = re.findall(r'(translate|rotate|scale|matrix)\(([^)]+)\)', transform_str)
    
    for transform_type, params_str in reversed(transforms):
        params = [float(p.strip()) for p in params_str.split(',')]
        
        if transform_type == 'translate':
            current_x += params[0]
            current_y += params[1] if len(params) > 1 else 0
        elif transform_type == 'scale':
            sx = params[0]
            sy = params[1] if len(params) > 1 else params[0]
            current_x *= sx
            current_y *= sy
        elif transform_type == 'rotate':
            angle = math.radians(params[0])
            cx = params[1] if len(params) > 1 else 0
            cy = params[2] if len(params) > 2 else 0
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            dx = current_x - cx
            dy = current_y - cy
            current_x = cx + dx * cos_a - dy * sin_a
            current_y = cy + dx * sin_a + dy * cos_a
        elif transform_type == 'matrix':
            a, b, c, d, e, f = params
            new_x = a * current_x + c * current_y + e
            new_y = b * current_x + d * current_y + f
            current_x, current_y = new_x, new_y
    
    return current_x, current_y


def parse_transform_forward(transform_str, x, y):
    if not transform_str:
        return x, y, 1.0, 0.0, 0.0, 1.0
    
    tx, ty, sx, sy, angle = 0.0, 0.0, 1.0, 1.0, 0.0
    cx, cy = 0.0, 0.0
    has_center = False
    
    transforms = re.findall(r'(translate|rotate|scale)\(([^)]+)\)', transform_str)
    
    for transform_type, params_str in transforms:
        params = [float(p.strip()) for p in params_str.split(',')]
        
        if transform_type == 'translate':
            tx += params[0]
            ty += params[1] if len(params) > 1 else 0
        elif transform_type == 'scale':
            sx *= params[0]
            sy *= params[1] if len(params) > 1 else params[0]
        elif transform_type == 'rotate':
            angle += params[0]
            if len(params) > 1:
                cx = params[1]
                cy = params[2] if len(params) > 2 else 0
                has_center = True
    
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    abs_x = float(x) + tx
    abs_y = float(y) + ty
    
    if has_center:
        dx = abs_x - cx
        dy = abs_y - cy
        final_x = cx + (dx * cos_a - dy * sin_a) * sx
        final_y = cy + (dx * sin_a + dy * cos_a) * sy
    else:
        final_x = abs_x * sx
        final_y = abs_y * sy
    
    return final_x, final_y


class SvgTerminal:
    def __init__(self, index, x, y):
        self.index = int(index)
        self.x = float(x)
        self.y = float(y)
        self.point_id = None

    def to_dict(self):
        return {
            'terminal_index': self.index,
            'x': round(self.x, 4),
            'y': round(self.y, 4),
            'point_id': self.point_id
=======
"""SVG文件解析器 - 解析配电网单线图SVG，提取图元、连接关系和拓扑数据。

本模块是闭环流程的核心入口：
    原始 SVG -> SvgDocument.parse() -> 中间模型
    中间模型 -> SvgDocumentWriter.write() -> 新 SVG
    新 SVG -> SvgDocument.parse() -> 验证中间模型
"""
import xml.etree.ElementTree as ET
import os
import re
import json
import csv
import copy
from collections import defaultdict
from typing import Optional

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
IEC_NS = "http://iec.ch/TC57/2005/SVG-schema#"

NS_MAP = {
    "ns0": SVG_NS,
    "ns1": XLINK_NS,
    "ns2": IEC_NS,
}

# 图层 -> 设备类型名称
DEVICE_TYPE_MAP = {
    "RemoteUnit": "故障指示器",
    "Junction": "接头",
    "PowerTransformer": "变压器",
    "Breaker": "断路器",
    "Fuse": "熔断器",
    "PoleCode": "杆塔",
    "Other": "其他",
    "LoadBreakSwitch": "负荷开关",
    "CurrentTransformer": "电流互感器",
    "GroundDisconnector": "接地隔离开关",
    "Disconnector": "隔离开关",
    "PotentialTransformer": "电压互感器",
    "EnergyConsumer": "负荷",
    "CompositeSwitch": "组合开关",
    "BusbarSection": "母线",
    "Substation": "站房",
    "ACLineSegment": "交流线段",
}

# 设备图层顺序（写回 SVG 时保持）
DEVICE_LAYERS = [
    "RemoteUnit_Layer", "Junction_Layer", "PowerTransformer_Layer",
    "Breaker_Layer", "Fuse_Layer", "PoleCode_Layer", "Other_Layer",
    "LoadBreakSwitch_Layer", "CurrentTransformer_Layer",
    "GroundDisconnector_Layer", "Disconnector_Layer",
    "PotentialTransformer_Layer", "EnergyConsumer_Layer",
    "CompositeSwitch_Layer", "BusbarSection_Layer",
    "Substation_Layer", "ACLineSegment_Layer",
]

PSR_TYPE_MAP = {
    "0203": "接头",
    "0811003": "故障指示器",
    "13TMP00132954": "线路",
}


def _local_tag(tag: str) -> str:
    if "}" in tag:
        return tag.split("}")[-1]
    return tag


class SvgElement:
    """SVG 图元中间模型"""

    def __init__(self):
        self.element_id: str = ""
        self.element_type: str = ""          # 中文类型名
        self.element_name: str = ""
        self.psr_type: str = ""
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.rotation: float = 0.0
        self.symbol_href: str = ""           # #symbol_id
        self.glink_refs: list[str] = []
        self.layer_ref: str = ""
        self.voltage_level: str = ""
        self.line_type: str = ""
        self.layer_name: str = ""            # 英文图层名，如 LoadBreakSwitch
        # 以下字段用于写回 SVG
        self.shape_tag: str = "use"          # use | rect | polygon | path | circle | line
        self.shape_attrs: dict = {}          # 原始图形属性
        self.transform: str = ""
        self.raw_transform: str = ""           # 原始 transform 字符串（无法重建时兜底保留）
        # 解析后的transform分量（用于坐标操作和写回时重建）
        self._transform_tx: float = 0.0
        self._transform_ty: float = 0.0
        self._transform_scale: float = 1.0
        self._transform_rotation: float = 0.0
        self._transform_can_rebuild: bool = True
        self.css_class: str = ""
        self.fill: str = ""
        self.stroke: str = ""
        self.stroke_width: str = ""
        self.raw_metadata: dict = {}         # PSR_Ref/GLink_Ref/Layer_Ref 原始属性
        self.raw_data: dict = {}
        # 原始XML节点深拷贝，用于Writer克隆写回（结构级保真）
        self.raw_element: Optional[ET.Element] = None

    def to_dict(self) -> dict:
        return {
            "element_id": self.element_id,
            "element_type": self.element_type,
            "element_name": self.element_name,
            "psr_type": self.psr_type,
            "x": round(self.x, 3),
            "y": round(self.y, 3),
            "width": round(self.width, 3),
            "height": round(self.height, 3),
            "rotation": round(self.rotation, 3),
            "symbol_href": self.symbol_href,
            "glink_refs": ",".join(self.glink_refs),
            "layer_ref": self.layer_ref,
            "voltage_level": self.voltage_level,
            "line_type": self.line_type,
            "layer_name": self.layer_name,
        }

    def rebuild_transform(self):
        """根据解析后的分量重建 transform 字符串。

        对于 <use> 元素，transform 的 translate 分量应与 x/y 属性保持一致。
        当 x/y 被修改时（如网格吸附），需要同步更新 transform。
        若包含无法重建的变换命令，则保留原始 transform 字符串。
        """
        if not self._transform_can_rebuild:
            self.transform = self.raw_transform
            return

        parts = []
        tx = self._transform_tx
        ty = self._transform_ty
        scale = self._transform_scale
        rot = self._transform_rotation

        if tx != 0 or ty != 0:
            parts.append(f"translate({tx:.6f},{ty:.6f})")
        if scale != 1.0:
            parts.append(f"scale({scale:.6f})")
        if rot != 0:
            parts.append(f"rotate({rot:.6f})")

        self.transform = " ".join(parts)

    def patch_transform_translate(self, old_x: float, old_y: float, new_x: float, new_y: float):
        """在原始 transform 字符串中平移位置相关数值。

        适用于以设备中心为基准的 transform，如：
        rotate(a,cx,cy) translate(cx,cy) scale(sx,sy) translate(-cx,-cy)
        其中 cx/cy 以及对应的正负 translate 值会被 old->new 的偏移替换，
        从而保留 scale/rotate 语义，仅移动设备位置。
        """
        base = self.transform or self.raw_transform
        if not base:
            self.transform = f"translate({new_x:.6f},{new_y:.6f})"
            return

        tol = 1e-3

        def _num_eq(a: float, b: float) -> bool:
            return abs(a - b) < tol

        # 先处理 rotate(angle,cx,cy)：只替换与 old_x/old_y 匹配的 cx/cy
        def repl_rotate(m):
            angle = m.group(1)
            cx = float(m.group(2))
            cy = float(m.group(3))
            cx_new = f"{new_x:.6f}" if _num_eq(cx, old_x) else m.group(2)
            cy_new = f"{new_y:.6f}" if _num_eq(cy, old_y) else m.group(3)
            return f"rotate({angle},{cx_new},{cy_new})"

        s = re.sub(r'rotate\(([-+\d.]+)[,\s]+([-+\d.]+)[,\s]+([-+\d.]+)\)', repl_rotate, base)

        # 处理 translate(a,b)：a/b 与 old_x/old_y 或其相反数匹配时替换
        def repl_translate(m):
            a = float(m.group(1))
            b = float(m.group(2))
            if _num_eq(a, old_x):
                a_new = f"{new_x:.6f}"
            elif _num_eq(a, -old_x):
                a_new = f"{-new_x:.6f}"
            else:
                a_new = m.group(1)
            if _num_eq(b, old_y):
                b_new = f"{new_y:.6f}"
            elif _num_eq(b, -old_y):
                b_new = f"{-new_y:.6f}"
            else:
                b_new = m.group(2)
            return f"translate({a_new},{b_new})"

        s = re.sub(r'translate\(([-+\d.]+)[,\s]+([-+\d.]+)\)', repl_translate, s)

        self.transform = s

    def patch_transform_scale(self, new_scale: float):
        """将 transform 中的 scale 分量替换为新的统一缩放值。

        用于设备尺寸标准化：去掉原始 SVG 中极小的 scale(0.126)，使 use 的
        width/height 直接决定显示尺寸。
        """
        base = self.transform or self.raw_transform
        if not base:
            return
        s = re.sub(
            r'scale\(([-+\d.]+)(?:[,\s]+([-+\d.]+))?\)',
            f'scale({new_scale:.6f},{new_scale:.6f})',
            base,
        )
        self.transform = s


class SvgConnection:
    """SVG 连接线中间模型"""

    def __init__(self):
        self.connection_id: str = ""
        self.connection_name: str = ""
        self.line_type: str = ""
        self.psr_type: str = ""
        self.points: list[tuple[float, float]] = []
        self.glink_refs: list[str] = []
        self.layer_ref: str = ""
        self.start_device_id: str = ""
        self.end_device_id: str = ""
        self.top_type: str = ""
        self.business_type: str = ""
        self.voltage_level: str = ""
        # 以下字段用于写回 SVG
        self.css_class: str = ""
        self.fill: str = "none"
        self.stroke: str = ""
        self.stroke_width: str = ""
        self.stroke_linecap: str = "round"
        self.stroke_linejoin: str = "round"
        self.stroke_dasharray: str = ""
        self.raw_metadata: dict = {}

    def to_dict(self) -> dict:
        return {
            "connection_id": self.connection_id,
            "connection_name": self.connection_name,
            "line_type": self.line_type,
            "psr_type": self.psr_type,
            "points": ";".join([f"{p[0]:.3f},{p[1]:.3f}" for p in self.points]),
            "glink_refs": ",".join(self.glink_refs),
            "layer_ref": self.layer_ref,
            "start_device_id": self.start_device_id,
            "end_device_id": self.end_device_id,
            "top_type": self.top_type,
            "business_type": self.business_type,
            "voltage_level": self.voltage_level,
>>>>>>> 28dd083296963d2896e56ae8eca2483f9a9e66f7
        }


class SvgText:
<<<<<<< HEAD
    def __init__(self, text_id, x, y, content='', font_size=0, color=''):
        self.text_id = text_id
        self.x = float(x)
        self.y = float(y)
        self.content = content
        self.font_size = font_size
        self.color = color
        self.object_id = None
        self.object_name = None
        self.psr_type = None
        self.related_element_id = None

    def to_dict(self):
        return {
            'text_id': self.text_id,
            'x': round(self.x, 4),
            'y': round(self.y, 4),
            'content': self.content,
            'font_size': round(self.font_size, 4),
            'color': self.color,
            'object_id': self.object_id,
            'related_element_id': self.related_element_id
        }


class SvgElement:
    def __init__(self, element_id, element_type, x, y, width=0, height=0):
        self.element_id = element_id
        self.element_type = element_type
        self.x = float(x)
        self.y = float(y)
        self.width = float(width) if width else 0
        self.height = float(height) if height else 0
        self.object_id = None
        self.object_name = None
        self.psr_type = None
        self.terminals = []
        self.layer = None
        self.layer_id = None
        self.symbol_id = None
        self.voltage_level = None
        self.css_class = None
        self.stroke_color = None
        self.fill_color = None
        self.stroke_width = None
        self.related_text_ids = []
        self.is_junction = False

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_related_text(self, text_id):
        if text_id not in self.related_text_ids:
            self.related_text_ids.append(text_id)

    def to_dict(self):
        return {
            'element_id': self.element_id,
            'element_type': self.element_type,
            'element_type_cn': TYPE_NAME_MAP.get(self.element_type, self.element_type),
            'x': round(self.x, 4),
            'y': round(self.y, 4),
            'width': round(self.width, 4),
            'height': round(self.height, 4),
            'object_id': self.object_id,
            'object_name': self.object_name,
            'psr_type': self.psr_type,
            'layer': self.layer,
            'voltage_level': self.voltage_level,
            'css_class': self.css_class,
            'stroke_color': self.stroke_color,
            'is_junction': self.is_junction,
            'related_text_ids': self.related_text_ids,
            'terminals': [t.to_dict() for t in self.terminals]
        }


LINE_TYPE_MAP = {
    '#00A854': 'main_line',
    '#FF6A00': 'tie_line',
    '#722ED1': 'inter_station_line',
    '#BFBFBF': 'spare_line',
    '#1890FF': 'trace_path',
}

LINE_TYPE_NAME_MAP = {
    'main_line': '主干线',
    'tie_line': '联络线',
    'inter_station_line': '站间连线',
    'spare_line': '备用线',
    'trace_path': '追踪路径',
    'branch_line': '支线',
    'container_border': '容器边界',
    'Trunk': '主干',
    'Branch': '分支',
    'Tie': '联络'
}


class SvgLine:
    def __init__(self, line_id, points_str, line_type=None):
        self.line_id = line_id
        self.points = self._parse_points(points_str)
        self.line_type = line_type
        self.line_type_cn = LINE_TYPE_NAME_MAP.get(line_type, line_type) if line_type and line_type not in ('Trunk', 'Branch', 'Tie') else None
        self.start_point = None
        self.end_point = None
        self.object_id = None
        self.glink_refs = []
        self.voltage_level = None
        self.color = None
        self.stroke_width = None
        self.css_class = None
        self.inferred_type = None
        self.inferred_type_cn = None

    def _parse_points(self, points_str):
        coords = []
        point_values = re.split(r'[ ,]+', points_str.strip())
        point_values = [v for v in point_values if v]
        for i in range(0, len(point_values), 2):
            if i + 1 < len(point_values):
                coords.append((float(point_values[i]), float(point_values[i+1])))
        return coords

    def infer_line_type(self):
        inferred = None
        if self.color:
            color_upper = self.color.upper()
            if color_upper in LINE_TYPE_MAP:
                inferred = LINE_TYPE_MAP[color_upper]
        if not inferred and self.stroke_width:
            try:
                width = float(self.stroke_width)
                if width >= 4.0:
                    inferred = 'tie_line'
                elif width >= 2.5:
                    inferred = 'main_line'
                elif width <= 1.2:
                    inferred = 'spare_line'
                else:
                    inferred = 'branch_line'
            except ValueError:
                pass
        self.inferred_type = inferred
        self.inferred_type_cn = LINE_TYPE_NAME_MAP.get(inferred, inferred) if inferred else None
        if not self.line_type and inferred:
            self.line_type = inferred
            self.line_type_cn = self.inferred_type_cn
        return inferred

    def to_dict(self):
        return {
            'line_id': self.line_id,
            'points': [(round(p[0], 4), round(p[1], 4)) for p in self.points],
            'line_type': self.line_type,
            'line_type_cn': self.line_type_cn,
            'inferred_type': self.inferred_type,
            'inferred_type_cn': self.inferred_type_cn,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'object_id': self.object_id,
            'glink_refs': self.glink_refs,
            'color': self.color,
            'stroke_width': self.stroke_width,
            'voltage_level': self.voltage_level
        }


class SvgConnection:
    def __init__(self, from_element_id, from_terminal, to_element_id, to_terminal, line_id=None):
        self.from_element_id = from_element_id
        self.from_terminal = from_terminal
        self.to_element_id = to_element_id
        self.to_terminal = to_terminal
        self.line_id = line_id

    def to_dict(self):
        return {
            'from_element_id': self.from_element_id,
            'from_terminal': self.from_terminal,
            'to_element_id': self.to_element_id,
            'to_terminal': self.to_terminal,
            'line_id': self.line_id
=======
    """SVG 文字标注中间模型"""

    def __init__(self):
        self.text_id: str = ""
        self.content: str = ""
        self.x: float = 0.0
        self.y: float = 0.0
        self.font_size: float = 0.0
        self.object_id: str = ""          # 去掉TXT_前缀的设备ID
        self.raw_object_id: str = ""       # 保留原始TXT_前缀的ID（往返保真）
        self.object_name: str = ""
        self.layer_ref: str = ""
        # 元数据属性
        self.line_type: str = ""
        self.business_type: str = ""
        self.top_type: str = ""
        # 文字定位属性（规范B.4）
        self.dx: float = 0.0
        self.dy: float = 0.0
        self.text_anchor: str = "middle"
        self.dominant_baseline: str = "auto"
        self.text_role: str = ""               # title | name | line | id
        self.hidden: bool = False              # 是否被过滤隐藏
        # 以下字段用于写回 SVG
        self.fill: str = ""
        self.font_family: str = ""
        self.stroke: str = "none"
        self.style: str = "text-anchor:middle"
        self.font_weight: str = "normal"
        self.raw_metadata: dict = {}
        # 原始XML节点深拷贝，用于Writer克隆写回（结构级保真）
        self.raw_element: Optional[ET.Element] = None

    def to_dict(self) -> dict:
        return {
            "text_id": self.text_id,
            "content": self.content,
            "x": round(self.x, 3),
            "y": round(self.y, 3),
            "font_size": round(self.font_size, 3),
            "dx": round(self.dx, 3),
            "dy": round(self.dy, 3),
            "text_anchor": self.text_anchor,
            "object_id": self.object_id,
            "object_name": self.object_name,
            "layer_ref": self.layer_ref,
>>>>>>> 28dd083296963d2896e56ae8eca2483f9a9e66f7
        }


class SvgDocument:
<<<<<<< HEAD
    def __init__(self):
        self.elements = {}
        self.lines = {}
        self.texts = {}
        self.connections = []
        self.symbol_defs = {}
        self.filename = ''

    def add_element(self, element):
        self.elements[element.element_id] = element

    def add_line(self, line):
        self.lines[line.line_id] = line

    def add_text(self, text):
        self.texts[text.text_id] = text

    def add_connection(self, connection):
        self.connections.append(connection)

    def load_symbol_defs(self, root):
        for symbol in root.findall('.//ns0:symbol', NS_MAP):
            symbol_id = symbol.get('id', '')
            terminals = []
            for use in symbol.findall('.//ns0:use', NS_MAP):
                term_index = use.get('terminal-index')
                x = use.get('x', '0')
                y = use.get('y', '0')
                if term_index:
                    terminals.append(SvgTerminal(term_index, x, y))
            self.symbol_defs[symbol_id] = terminals

    def parse_elements(self, root):
        for layer_id, elem_type in LAYER_TYPE_MAP.items():
            if elem_type in ('ConnLine', 'Other'):
                continue
            
            layer = root.find(f'.//ns0:g[@id="{layer_id}"]', NS_MAP)
            if layer is None:
                continue
            
            for group in layer.findall('.//ns0:g', NS_MAP):
                group_id = group.get('id', '')
                
                use_elem = group.find('.//ns0:use', NS_MAP)
                if use_elem is not None:
                    href = use_elem.get('{http://www.w3.org/1999/xlink}href', '')
                    if href.startswith('#'):
                        symbol_id = href[1:]
                    else:
                        symbol_id = href
                    
                    x = use_elem.get('x', '0')
                    y = use_elem.get('y', '0')
                    width = use_elem.get('width', '0')
                    height = use_elem.get('height', '0')
                    transform = use_elem.get('transform', '')
                    css_class = use_elem.get('class', '')
                    
                    abs_x, abs_y = parse_transform_forward(transform, x, y)
                    
                    element = SvgElement(group_id, elem_type, abs_x, abs_y, width, height)
                    element.layer = layer_id
                    element.layer_id = layer_id
                    element.symbol_id = symbol_id
                    element.voltage_level = self._class_to_voltage(css_class)
                    element.css_class = css_class
                    element.is_junction = elem_type == 'Junction'
                    
                    polyline_elem = group.find('.//ns0:polyline', NS_MAP)
                    if polyline_elem is not None:
                        element.stroke_color = polyline_elem.get('stroke', '')
                        element.stroke_width = polyline_elem.get('stroke-width', '')
                    
                    if symbol_id in self.symbol_defs:
                        for term in self.symbol_defs[symbol_id]:
                            term_x, term_y = parse_transform_forward(transform, 
                                float(x) + term.x, float(y) + term.y)
                            element.add_terminal(SvgTerminal(term.index, term_x, term_y))
                    
                    self._parse_metadata(group, element)
                    self.add_element(element)
                
                polygon_elem = group.find('.//ns0:polygon', NS_MAP)
                if polygon_elem is not None and elem_type == 'Substation':
                    points_str = polygon_elem.get('points', '')
                    points = self._parse_points_str(points_str)
                    if points:
                        min_x = min(p[0] for p in points)
                        min_y = min(p[1] for p in points)
                        max_x = max(p[0] for p in points)
                        max_y = max(p[1] for p in points)
                        element = SvgElement(
                            group_id, elem_type,
                            (min_x + max_x) / 2, (min_y + max_y) / 2,
                            max_x - min_x, max_y - min_y
                        )
                        element.layer = layer_id
                        element.layer_id = layer_id
                        element.stroke_color = polygon_elem.get('stroke', '')
                        self._parse_metadata(group, element)
                        self.add_element(element)

    def parse_texts(self, root):
        text_layer = root.find('.//ns0:g[@id="Text_Layer"]', NS_MAP)
        if text_layer is None:
            return
        
        for group in text_layer.findall('.//ns0:g', NS_MAP):
            group_id = group.get('id', '')
            
            text_elems = group.findall('.//ns0:text', NS_MAP)
            if not text_elems:
                continue
            
            for text_elem in text_elems:
                x = text_elem.get('x', '0')
                y = text_elem.get('y', '0')
                content = text_elem.text or ''
                font_size = text_elem.get('font-size', '0')
                color = text_elem.get('fill', '')
                
                if not content.strip():
                    continue
                
                text = SvgText(group_id, x, y, content.strip(), float(font_size), color)
                
                self._parse_text_metadata(group, text)
                self.add_text(text)
        
        self._associate_texts_with_elements()

    def _parse_text_metadata(self, group, text):
        metadata = group.find('.//ns0:metadata', NS_MAP)
        if metadata is not None:
            psr_ref = metadata.find('.//ns2:PSR_Ref', NS_MAP)
            if psr_ref is not None:
                text.object_id = psr_ref.get('ObjectID')
                text.object_name = psr_ref.get('ObjectName')
                text.psr_type = psr_ref.get('PSRType')

    def _associate_texts_with_elements(self):
        for text_id, text in self.texts.items():
            elem_id = None
            
            if text_id.startswith('TXT-'):
                candidate_id = text_id[4:]
                if candidate_id in self.elements:
                    elem_id = candidate_id
            
            if elem_id is None and text.object_id:
                for eid, elem in self.elements.items():
                    if elem.object_id == text.object_id:
                        elem_id = eid
                        break
            
            if elem_id is None and text.object_name:
                for eid, elem in self.elements.items():
                    if elem.object_name == text.object_name:
                        elem_id = eid
                        break
            
            if elem_id is None:
                for eid, elem in self.elements.items():
                    dist = ((text.x - elem.x) ** 2 + (text.y - elem.y) ** 2) ** 0.5
                    if dist < 30:
                        elem_id = eid
                        break
            
            if elem_id:
                text.related_element_id = elem_id
                self.elements[elem_id].add_related_text(text_id)

    def _class_to_voltage(self, css_class):
        if not css_class:
            return None
        match = re.search(r'lkv(\d+(?:\.\d+)?)', css_class)
        if match:
            return match.group(1) + 'kV'
        match = re.search(r'kv(\d+(?:\.\d+)?)', css_class)
        if match:
            return match.group(1) + 'kV'
        return None

    def _parse_points_str(self, points_str):
        coords = []
        pairs = re.findall(r'([\d.]+),([\d.]+)', points_str)
        for x, y in pairs:
            coords.append((float(x), float(y)))
        return coords

    def _parse_metadata(self, group, element):
        metadata = group.find('.//ns0:metadata', NS_MAP)
        if metadata is not None:
            psr_ref = metadata.find('.//ns2:PSR_Ref', NS_MAP)
            if psr_ref is not None:
                element.object_id = psr_ref.get('ObjectID')
                element.object_name = psr_ref.get('ObjectName')
                element.psr_type = psr_ref.get('PSRType')
            
            layer_ref = metadata.find('.//ns2:Layer_Ref', NS_MAP)
            if layer_ref is not None:
                element.layer = layer_ref.get('ObjectName')

    def parse_lines(self, root):
        for layer_id in ['ConnLine_Layer', 'ACLineSegment_Layer']:
            layer = root.find(f'.//ns0:g[@id="{layer_id}"]', NS_MAP)
            if layer is None:
                continue
            
            for group in layer.findall('.//ns0:g', NS_MAP):
                group_id = group.get('id', '')
                polyline = group.find('.//ns0:polyline', NS_MAP)
                line_elem = group.find('.//ns0:line', NS_MAP)
                
                if polyline is not None:
                    points_str = polyline.get('points', '')
                    line_class = polyline.get('class', '')
                    stroke = polyline.get('stroke', '')
                    stroke_width = polyline.get('stroke-width', '')
                    
                    line = SvgLine(group_id, points_str, line_class)
                    line.voltage_level = self._class_to_voltage(line_class)
                    line.color = stroke
                    line.stroke_width = stroke_width
                    line.css_class = line_class
                    line.infer_line_type()
                    
                    self._parse_line_metadata(group, line)
                    self.add_line(line)
                
                elif line_elem is not None:
                    x1 = line_elem.get('x1', '0')
                    y1 = line_elem.get('y1', '0')
                    x2 = line_elem.get('x2', '0')
                    y2 = line_elem.get('y2', '0')
                    points_str = f"{x1},{y1} {x2},{y2}"
                    line_class = line_elem.get('class', '')
                    stroke = line_elem.get('stroke', '')
                    stroke_width = line_elem.get('stroke-width', '')
                    
                    line = SvgLine(group_id, points_str, line_class)
                    line.voltage_level = self._class_to_voltage(line_class)
                    line.color = stroke
                    line.stroke_width = stroke_width
                    line.css_class = line_class
                    line.infer_line_type()
                    
                    self._parse_line_metadata(group, line)
                    self.add_line(line)

    def _parse_line_metadata(self, group, line):
        metadata = group.find('.//ns0:metadata', NS_MAP)
        if metadata is not None:
            psr_ref = metadata.find('.//ns2:PSR_Ref', NS_MAP)
            if psr_ref is not None:
                line.object_id = psr_ref.get('ObjectID')
                meta_line_type = psr_ref.get('LineType')
                if meta_line_type:
                    line.line_type = meta_line_type
                    line.line_type_cn = LINE_TYPE_NAME_MAP.get(meta_line_type, meta_line_type)
            
            for glink in metadata.findall('.//ns2:GLink_Ref', NS_MAP):
                line.glink_refs.append(glink.get('ObjectID'))

    def build_connections(self):
        skipped = 0
        for line_id, line in self.lines.items():
            if not line.points:
                continue
            
            start_coords = line.points[0]
            end_coords = line.points[-1]
            
            start_elem, start_term = self._find_nearest_element(start_coords, exclude_element_id=None)
            end_elem, end_term = self._find_nearest_element(end_coords, exclude_element_id=start_elem.element_id if start_elem else None)
            
            if start_elem and end_elem:
                if start_elem.element_id == end_elem.element_id and start_term == end_term:
                    skipped += 1
                    continue
                
                conn = SvgConnection(
                    start_elem.element_id, start_term,
                    end_elem.element_id, end_term,
                    line_id
                )
                self.add_connection(conn)
        
        if skipped > 0:
            print(f"  跳过自连接(同设备同端子): {skipped}条")

    def _find_nearest_element(self, coords, exclude_element_id=None):
        nearest = None
        min_dist = float('inf')
        nearest_term = 1
        x, y = coords
        
        for elem in self.elements.values():
            if exclude_element_id and elem.element_id == exclude_element_id:
                continue
            
            if elem.terminals:
                for term in elem.terminals:
                    dist = ((x - term.x) ** 2 + (y - term.y) ** 2) ** 0.5
                    if dist < min_dist and dist < 3:
                        min_dist = dist
                        nearest = elem
                        nearest_term = term.index
            else:
                dist = ((x - elem.x) ** 2 + (y - elem.y) ** 2) ** 0.5
                if dist < min_dist and dist < 8:
                    min_dist = dist
                    nearest = elem
                    nearest_term = 1
        
        if nearest is None:
            nearest, min_dist, nearest_term = self._find_best_match(coords, exclude_element_id)
        
        return nearest, nearest_term

    def _find_best_match(self, coords, exclude_element_id=None):
        nearest = None
        min_dist = float('inf')
        nearest_term = 1
        x, y = coords
        
        for elem in self.elements.values():
            if exclude_element_id and elem.element_id == exclude_element_id:
                continue
            
            if elem.terminals:
                for term in elem.terminals:
                    dist = ((x - term.x) ** 2 + (y - term.y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        nearest = elem
                        nearest_term = term.index
            else:
                dist = ((x - elem.x) ** 2 + (y - elem.y) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest = elem
                    nearest_term = 1
        
        return nearest, min_dist, nearest_term

    def export_elements_json(self, filename='svg_elements.json'):
        data = {
            'filename': self.filename,
            'element_count': len(self.elements),
            'line_count': len(self.lines),
            'text_count': len(self.texts),
            'connection_count': len(self.connections),
            'elements': [e.to_dict() for e in self.elements.values()],
            'texts': [t.to_dict() for t in self.texts.values()]
        }
        save_path = os.path.join(OUTPUT_JSON, filename)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return save_path

    def export_connections_json(self, filename='svg_connections.json'):
        data = {
            'filename': self.filename,
            'connections': [c.to_dict() for c in self.connections]
        }
        save_path = os.path.join(OUTPUT_JSON, filename)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return save_path

    def export_elements_csv(self, filename='svg_elements.csv'):
        rows = []
        for elem in self.elements.values():
            for term in elem.terminals:
                rows.append({
                    'element_id': elem.element_id,
                    'element_type': elem.element_type,
                    'element_type_cn': TYPE_NAME_MAP.get(elem.element_type, elem.element_type),
                    'x': round(elem.x, 4),
                    'y': round(elem.y, 4),
                    'object_id': elem.object_id,
                    'object_name': elem.object_name,
                    'psr_type': elem.psr_type,
                    'layer': elem.layer,
                    'voltage_level': elem.voltage_level,
                    'css_class': elem.css_class,
                    'stroke_color': elem.stroke_color,
                    'is_junction': elem.is_junction,
                    'related_text_count': len(elem.related_text_ids),
                    'terminal_index': term.index,
                    'terminal_x': round(term.x, 4),
                    'terminal_y': round(term.y, 4)
                })
            if not elem.terminals:
                rows.append({
                    'element_id': elem.element_id,
                    'element_type': elem.element_type,
                    'element_type_cn': TYPE_NAME_MAP.get(elem.element_type, elem.element_type),
                    'x': round(elem.x, 4),
                    'y': round(elem.y, 4),
                    'object_id': elem.object_id,
                    'object_name': elem.object_name,
                    'psr_type': elem.psr_type,
                    'layer': elem.layer,
                    'voltage_level': elem.voltage_level,
                    'css_class': elem.css_class,
                    'stroke_color': elem.stroke_color,
                    'is_junction': elem.is_junction,
                    'related_text_count': len(elem.related_text_ids),
                    'terminal_index': '',
                    'terminal_x': '',
                    'terminal_y': ''
                })
        
        df = pd.DataFrame(rows)
        save_path = os.path.join(OUTPUT_CSV, filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

    def export_texts_csv(self, filename='svg_texts.csv'):
        rows = []
        for text in self.texts.values():
            rows.append({
                'text_id': text.text_id,
                'x': round(text.x, 4),
                'y': round(text.y, 4),
                'content': text.content,
                'font_size': round(text.font_size, 4),
                'color': text.color,
                'object_id': text.object_id,
                'related_element_id': text.related_element_id
            })
        
        df = pd.DataFrame(rows)
        save_path = os.path.join(OUTPUT_CSV, filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

    def export_connections_csv(self, filename='svg_connections.csv'):
        rows = []
        for conn in self.connections:
            from_elem = self.elements.get(conn.from_element_id)
            to_elem = self.elements.get(conn.to_element_id)
            line = self.lines.get(conn.line_id) if conn.line_id else None
            rows.append({
                'line_id': conn.line_id,
                'line_type': line.line_type if line else '',
                'line_type_cn': line.line_type_cn if line else '',
                'inferred_type': line.inferred_type if line else '',
                'inferred_type_cn': line.inferred_type_cn if line else '',
                'line_color': line.color if line else '',
                'line_stroke_width': line.stroke_width if line else '',
                'from_element_id': conn.from_element_id,
                'from_element_type': from_elem.element_type if from_elem else '',
                'from_element_name': from_elem.object_name if from_elem else '',
                'from_terminal': conn.from_terminal,
                'to_element_id': conn.to_element_id,
                'to_element_type': to_elem.element_type if to_elem else '',
                'to_element_name': to_elem.object_name if to_elem else '',
                'to_terminal': conn.to_terminal
            })
        
        df = pd.DataFrame(rows)
        save_path = os.path.join(OUTPUT_CSV, filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path


class SvgParser:
    @staticmethod
    def parse(file_path):
        doc = SvgDocument()
        doc.filename = os.path.basename(file_path)
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            doc.load_symbol_defs(root)
            doc.parse_elements(root)
            doc.parse_texts(root)
            doc.parse_lines(root)
            doc.build_connections()
            
            print(f"SVG解析完成: {doc.filename}")
            print(f"  图元数量: {len(doc.elements)}")
            print(f"  线路数量: {len(doc.lines)}")
            print(f"  文字标注: {len(doc.texts)}")
            print(f"  连接关系: {len(doc.connections)}")
            
            type_counts = {}
            for elem in doc.elements.values():
                t = elem.element_type
                type_counts[t] = type_counts.get(t, 0) + 1
            print(f"  设备类型分布: {type_counts}")
            
            return doc
        except Exception as e:
            import traceback
            print(f"SVG解析失败: {e}")
            traceback.print_exc()
            return None


if __name__ == "__main__":
    
    svg_dir = r"D:\挑战杯\挑战杯\数据集更新版\数据集更新版20260729\配网 svg"
    
    for fname in ['LINE215.svg', 'LINE216.svg']:
        fpath = os.path.join(svg_dir, fname)
        if os.path.exists(fpath):
            print(f"\n=== 解析 {fname} ===")
            doc = SvgParser.parse(fpath)
            if doc:
                doc.export_elements_json(f'{fname}_elements.json')
                doc.export_elements_csv(f'{fname}_elements.csv')
                doc.export_texts_csv(f'{fname}_texts.csv')
                doc.export_connections_json(f'{fname}_connections.json')
                doc.export_connections_csv(f'{fname}_connections.csv')
                print(f"  导出完成")
        else:
            print(f" 文件不存在: {fname}")
=======
    """SVG 文档中间模型"""

    def __init__(self, svg_path: str):
        self.svg_path = svg_path
        self.svg_filename = os.path.basename(svg_path)
        self.feeder_id = os.path.splitext(self.svg_filename)[0]
        self.elements: list[SvgElement] = []
        self.connections: list[SvgConnection] = []
        self.texts: list[SvgText] = []
        self.tree: Optional[ET.ElementTree] = None
        self.root: Optional[ET.Element] = None
        self.viewbox: tuple = (0, 0, 0, 0)
        self.width: float = 0.0
        self.height: float = 0.0
        self.coordinate_extent: str = ""
        self.preserve_aspect_ratio: str = ""
        self._symbol_defs: dict[str, dict] = {}

    # ------------------------------------------------------------------
    # 解析
    # ------------------------------------------------------------------
    def parse(self) -> bool:
        try:
            self.tree = ET.parse(self.svg_path)
            self.root = self.tree.getroot()
            self._parse_svg_attrs()
            self._parse_symbol_defs()
            self._parse_devices()
            self._parse_connections()
            self._parse_texts()
            self._resolve_connection_links()
            print(f"  解析完成: {len(self.elements)} 个设备, {len(self.connections)} 条连接, {len(self.texts)} 个文字标注")
            return True
        except Exception as e:
            print(f"  解析失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _parse_svg_attrs(self):
        if self.root is None:
            return
        self.width = float(self.root.get("width", "0"))
        self.height = float(self.root.get("height", "0"))
        self.coordinate_extent = self.root.get("coordinateExtent", "")
        self.preserve_aspect_ratio = self.root.get("preserveAspectRatio", "")
        viewbox = self.root.get("viewBox", "0 0 0 0")
        parts = viewbox.split()
        if len(parts) == 4:
            self.viewbox = tuple(float(p) for p in parts)

    def _parse_symbol_defs(self):
        if self.root is None:
            return
        for sym in self.root.iter(f"{{{SVG_NS}}}symbol"):
            sym_id = sym.get("id", "")
            if sym_id:
                viewbox = sym.get("viewBox", "0 0 0 0")
                parts = viewbox.split()
                w, h = 0, 0
                if len(parts) == 4:
                    w = float(parts[2])
                    h = float(parts[3])
                symbol_type = self._infer_symbol_type(sym_id)
                self._symbol_defs[sym_id] = {
                    "id": sym_id,
                    "width": w,
                    "height": h,
                    "type": symbol_type,
                }

    def _infer_symbol_type(self, symbol_id: str) -> str:
        for key, val in DEVICE_TYPE_MAP.items():
            if symbol_id.startswith(key):
                return val
        if "_TMP_" in symbol_id:
            base_id = symbol_id.split("_TMP_")[0]
            return DEVICE_TYPE_MAP.get(base_id, "未知")
        return "未知"

    def _parse_devices(self):
        if self.root is None:
            return
        for layer_id in DEVICE_LAYERS:
            layer_elem = self.root.find(f".//{{{SVG_NS}}}g[@id='{layer_id}']")
            if layer_elem is None:
                continue
            layer_name = layer_id.replace("_Layer", "")
            for device_g in layer_elem.findall(f"{{{SVG_NS}}}g"):
                elem = self._parse_device_element(device_g, layer_name)
                if elem:
                    self.elements.append(elem)

    def _parse_device_element(self, g_elem: ET.Element, layer_name: str) -> Optional[SvgElement]:
        elem = SvgElement()
        elem.layer_name = layer_name
        elem.element_type = DEVICE_TYPE_MAP.get(layer_name, layer_name)

        shape_parsed = False
        for child in g_elem:
            tag = _local_tag(child.tag)
            if tag == "metadata":
                self._parse_metadata(child, elem)
            elif tag in ("use", "rect", "polygon", "path", "circle", "line") and not shape_parsed:
                elem.shape_tag = tag
                elem.shape_attrs = dict(child.attrib)
                if tag == "use":
                    elem.x = float(child.get("x", "0"))
                    elem.y = float(child.get("y", "0"))
                    raw_w = float(child.get("width", "0"))
                    raw_h = float(child.get("height", "0"))
                    elem.width = raw_w
                    elem.height = raw_h
                    href = child.get(f"{{{XLINK_NS}}}href", "")
                    elem.symbol_href = href
                    elem.css_class = child.get("class", "")
                    elem.transform = child.get("transform", "")
                    elem.raw_transform = elem.transform
                    # 解析transform分量
                    tx, ty, scale, rot, can_rebuild = self._parse_transform(elem.transform)
                    elem._transform_tx = tx
                    elem._transform_ty = ty
                    elem._transform_scale = scale
                    elem._transform_rotation = rot
                    elem._transform_can_rebuild = can_rebuild
                    elem.rotation = rot
                    # 如果use没有指定width/height，从symbol的viewBox获取
                    if raw_w <= 0 and raw_h <= 0:
                        sym_id = href.lstrip("#")
                        if sym_id in self._symbol_defs:
                            sym = self._symbol_defs[sym_id]
                            elem.width = sym.get("width", 0)
                            elem.height = sym.get("height", 0)
                    self._infer_voltage_from_class(elem.css_class, elem)
                elif tag == "rect":
                    elem.x = float(child.get("x", "0"))
                    elem.y = float(child.get("y", "0"))
                    elem.width = float(child.get("width", "0"))
                    elem.height = float(child.get("height", "0"))
                    elem.fill = child.get("fill", "")
                    elem.stroke = child.get("stroke", "")
                    elem.stroke_width = child.get("stroke-width", "")
                elif tag == "polygon":
                    points_str = child.get("points", "")
                    elem.shape_attrs["points"] = points_str
                    coords = self._parse_points(points_str)
                    if coords:
                        xs = [c[0] for c in coords]
                        ys = [c[1] for c in coords]
                        elem.x = min(xs)
                        elem.y = min(ys)
                        elem.width = max(xs) - min(xs)
                        elem.height = max(ys) - min(ys)
                    elem.fill = child.get("fill", "")
                    elem.stroke = child.get("stroke", "")
                    elem.stroke_width = child.get("stroke-width", "")
                elif tag == "path":
                    elem.stroke = child.get("stroke", "")
                    elem.stroke_width = child.get("stroke-width", "")
                elif tag == "circle":
                    elem.x = float(child.get("cx", "0"))
                    elem.y = float(child.get("cy", "0"))
                    r = float(child.get("r", "0"))
                    elem.width = r * 2
                    elem.height = r * 2
                elif tag == "line":
                    x1 = float(child.get("x1", "0"))
                    y1 = float(child.get("y1", "0"))
                    x2 = float(child.get("x2", "0"))
                    y2 = float(child.get("y2", "0"))
                    elem.x, elem.y = x1, y1
                    elem.width, elem.height = x2 - x1, y2 - y1
                shape_parsed = True

        if not elem.element_id:
            elem.element_id = g_elem.get("id", "")
        # 保存原始XML节点深拷贝（结构级保真写回用）
        elem.raw_element = copy.deepcopy(g_elem)
        return elem

    def _parse_connections(self):
        if self.root is None:
            return
        conn_layer = self.root.find(f".//{{{SVG_NS}}}g[@id='ConnLine_Layer']")
        if conn_layer is None:
            return
        for conn_g in conn_layer.findall(f"{{{SVG_NS}}}g"):
            conn = self._parse_connection_element(conn_g)
            if conn:
                self.connections.append(conn)

    def _parse_connection_element(self, g_elem: ET.Element) -> Optional[SvgConnection]:
        conn = SvgConnection()
        conn.connection_id = g_elem.get("id", "")
        for child in g_elem:
            tag = _local_tag(child.tag)
            if tag == "polyline":
                points_str = child.get("points", "")
                conn.points = self._parse_points(points_str)
                conn.css_class = child.get("class", "")
                conn.fill = child.get("fill", "none")
                conn.stroke = child.get("stroke", "")
                conn.stroke_width = child.get("stroke-width", "")
                conn.stroke_linecap = child.get("stroke-linecap", "round")
                conn.stroke_linejoin = child.get("stroke-linejoin", "round")
                conn.stroke_dasharray = child.get("stroke-dasharray", "")
                stroke = child.get("stroke", "")
                conn.voltage_level = self._infer_voltage_from_stroke(stroke)
            elif tag == "metadata":
                self._parse_connection_metadata(child, conn)
        return conn

    def _parse_texts(self):
        if self.root is None:
            return
        text_layer = self.root.find(f".//{{{SVG_NS}}}g[@id='Text_Layer']")
        if text_layer is None:
            return
        for text_g in text_layer.findall(f"{{{SVG_NS}}}g"):
            txt = self._parse_text_element(text_g)
            if txt:
                self.texts.append(txt)

    def _parse_text_element(self, g_elem: ET.Element) -> Optional[SvgText]:
        """解析文字组，支持组内多个<text>节点（取第一个有效节点）。"""
        txt = SvgText()
        txt.text_id = g_elem.get("id", "")

        text_nodes = []
        for child in g_elem:
            tag = _local_tag(child.tag)
            if tag == "text":
                text_nodes.append(child)

        if not text_nodes:
            return None

        # 取第一个有效<text>节点作为主数据
        primary = text_nodes[0]
        txt.content = (primary.text or "").strip()
        if not txt.content:
            return None

        txt.x = float(primary.get("x", "0"))
        txt.y = float(primary.get("y", "0"))
        txt.font_size = float(primary.get("font-size", "0"))
        txt.fill = primary.get("fill", "")
        txt.font_family = primary.get("font-family", "")
        txt.stroke = primary.get("stroke", "none")
        txt.style = primary.get("style", "text-anchor:middle")
        txt.font_weight = primary.get("font-weight", "normal")
        txt.dx = float(primary.get("dx", "0"))
        txt.dy = float(primary.get("dy", "0"))
        txt.text_anchor = primary.get("text-anchor", "middle")
        txt.dominant_baseline = primary.get("dominant-baseline", "auto")

        # 如果第一个节点是白色fill，尝试用第二个节点覆盖（深/浅背景切换）
        if len(text_nodes) > 1 and txt.fill and "255,255,255" in txt.fill.replace(" ", ""):
            alt = text_nodes[1]
            alt_content = (alt.text or "").strip()
            if alt_content:
                txt.x = float(alt.get("x", str(txt.x)))
                txt.y = float(alt.get("y", str(txt.y)))
                txt.font_size = float(alt.get("font-size", str(txt.font_size)))
                txt.fill = alt.get("fill", txt.fill)
                txt.style = alt.get("style", txt.style)
                txt.font_weight = alt.get("font-weight", txt.font_weight)
                txt.text_anchor = alt.get("text-anchor", txt.text_anchor)

        # 解析元数据
        for child in g_elem:
            tag = _local_tag(child.tag)
            if tag == "metadata":
                for meta_child in child:
                    meta_tag = _local_tag(meta_child.tag)
                    if meta_tag == "PSR_Ref":
                        raw_obj_id = meta_child.get("ObjectID", "")
                        # 保留原始ID（含TXT_前缀），同时提取真实设备ID
                        txt.raw_object_id = raw_obj_id
                        if raw_obj_id.startswith("TXT_"):
                            txt.object_id = raw_obj_id[4:]
                        else:
                            txt.object_id = raw_obj_id
                        txt.object_name = meta_child.get("ObjectName", "")
                        txt.line_type = meta_child.get("LineType", "")
                        txt.business_type = meta_child.get("businessType", "")
                        txt.top_type = meta_child.get("TopType", "")
                        txt.raw_metadata["PSR_Ref"] = dict(meta_child.attrib)
                    elif meta_tag == "Layer_Ref":
                        txt.layer_ref = meta_child.get("ObjectName", "")
                        txt.raw_metadata["Layer_Ref"] = dict(meta_child.attrib)

        # 保存原始XML节点深拷贝（结构级保真写回用）
        txt.raw_element = copy.deepcopy(g_elem)
        return txt

    def _parse_metadata(self, metadata_elem: ET.Element, elem: SvgElement):
        for child in metadata_elem:
            tag = _local_tag(child.tag)
            if tag == "PSR_Ref":
                elem.element_id = child.get("ObjectID", "")
                elem.element_name = child.get("ObjectName", "")
                elem.psr_type = child.get("PSRType", "")
                elem.line_type = child.get("LineType", "")
                elem.top_type = child.get("TopType", "")
                elem.business_type = child.get("businessType", "")
                elem.raw_metadata["PSR_Ref"] = dict(child.attrib)
                self._infer_voltage_from_psr_type(elem.psr_type, elem)
            elif tag == "GLink_Ref":
                gid = child.get("ObjectID", "")
                if gid:
                    elem.glink_refs.append(gid)
                if "GLink_Ref" not in elem.raw_metadata:
                    elem.raw_metadata["GLink_Ref"] = []
                elem.raw_metadata["GLink_Ref"].append(dict(child.attrib))
            elif tag == "Layer_Ref":
                elem.layer_ref = child.get("ObjectName", "")
                elem.raw_metadata["Layer_Ref"] = dict(child.attrib)

    def _parse_connection_metadata(self, metadata_elem: ET.Element, conn: SvgConnection):
        for child in metadata_elem:
            tag = _local_tag(child.tag)
            if tag == "PSR_Ref":
                conn.connection_id = child.get("ObjectID", conn.connection_id)
                conn.connection_name = child.get("ObjectName", "")
                conn.line_type = child.get("LineType", "")
                conn.psr_type = child.get("PSRType", "")
                conn.top_type = child.get("TopType", "")
                conn.business_type = child.get("businessType", "")
                conn.raw_metadata["PSR_Ref"] = dict(child.attrib)
            elif tag == "GLink_Ref":
                gid = child.get("ObjectID", "")
                if gid:
                    conn.glink_refs.append(gid)
                if "GLink_Ref" not in conn.raw_metadata:
                    conn.raw_metadata["GLink_Ref"] = []
                conn.raw_metadata["GLink_Ref"].append(dict(child.attrib))
            elif tag == "Layer_Ref":
                conn.layer_ref = child.get("ObjectName", "")
                conn.raw_metadata["Layer_Ref"] = dict(child.attrib)

    def compute_adaptive_viewbox(self, margin: float = 24.0):
        """基于所有图元计算带边距的 viewBox。"""
        if not self.elements and not self.connections and not self.texts:
            return self.viewbox

        xs, ys = [], []
        for elem in self.elements:
            xs.extend([elem.x, elem.x + elem.width])
            ys.extend([elem.y, elem.y + elem.height])
        for conn in self.connections:
            for x, y in conn.points:
                xs.append(x)
                ys.append(y)
        for txt in self.texts:
            xs.append(txt.x)
            ys.append(txt.y)

        if not xs or not ys:
            return self.viewbox

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = max_x - min_x + 2 * margin
        h = max_y - min_y + 2 * margin
        self.viewbox = (min_x - margin, min_y - margin, w, h)
        self.width = w
        self.height = h
        return self.viewbox

    def _resolve_connection_links(self):
        device_by_id = {}
        for elem in self.elements:
            if elem.element_id:
                device_by_id[elem.element_id] = elem

        conn_by_id = {}
        for conn in self.connections:
            if conn.connection_id:
                conn_by_id[conn.connection_id] = conn

        glink_to_device_ids = defaultdict(set)
        for elem in self.elements:
            for ref in elem.glink_refs:
                glink_to_device_ids[ref].add(elem.element_id)

        glink_to_conn_ids = defaultdict(set)
        for conn in self.connections:
            for ref in conn.glink_refs:
                glink_to_conn_ids[ref].add(conn.connection_id)

        direct_device_refs = defaultdict(set)
        for conn in self.connections:
            for ref in conn.glink_refs:
                if ref in device_by_id:
                    direct_device_refs[conn.connection_id].add(ref)

        conn_chain = defaultdict(set)
        for conn in self.connections:
            for ref in conn.glink_refs:
                if ref in conn_by_id and ref != conn.connection_id:
                    conn_chain[conn.connection_id].add(ref)

        visited = set()
        for conn_id in conn_by_id:
            if conn_id in visited:
                continue
            chain_component = set()
            stack = [conn_id]
            while stack:
                cid = stack.pop()
                if cid in visited:
                    continue
                visited.add(cid)
                chain_component.add(cid)
                for next_cid in conn_chain.get(cid, set()):
                    if next_cid not in visited:
                        stack.append(next_cid)

            if len(chain_component) > 1:
                all_devices = set()
                for cid in chain_component:
                    all_devices.update(direct_device_refs.get(cid, set()))
                # 稳定排序：按设备坐标排序，避免 set→list 顺序不稳定
                dev_list = sorted(all_devices, key=lambda d: (
                    device_by_id.get(d, SvgElement()).x,
                    device_by_id.get(d, SvgElement()).y
                ))
                for cid in chain_component:
                    conn = conn_by_id[cid]
                    if len(dev_list) >= 2:
                        conn.start_device_id = dev_list[0]
                        conn.end_device_id = dev_list[1]
                    elif len(dev_list) == 1:
                        conn.start_device_id = dev_list[0]

        for conn in self.connections:
            if not conn.start_device_id and not conn.end_device_id:
                dev_refs = direct_device_refs.get(conn.connection_id, set())
                ref_device_ids = set()
                for ref in conn.glink_refs:
                    if ref in glink_to_device_ids:
                        ref_device_ids.update(glink_to_device_ids[ref])
                dev_list = sorted(dev_refs | ref_device_ids, key=lambda d: (
                    device_by_id.get(d, SvgElement()).x,
                    device_by_id.get(d, SvgElement()).y
                ))
                if len(dev_list) >= 2:
                    conn.start_device_id = dev_list[0]
                    conn.end_device_id = dev_list[1]
                elif len(dev_list) == 1:
                    conn.start_device_id = dev_list[0]

    # ------------------------------------------------------------------
    # 模型查询
    # ------------------------------------------------------------------
    def get_device_by_id(self, device_id: str) -> Optional[SvgElement]:
        for elem in self.elements:
            if elem.element_id == device_id:
                return elem
        return None

    def get_connections_for_device(self, device_id: str) -> list[SvgConnection]:
        result = []
        for conn in self.connections:
            if device_id in conn.glink_refs:
                result.append(conn)
        return result

    def get_connected_devices(self, device_id: str) -> list[str]:
        connected = set()
        for conn in self.connections:
            if device_id in conn.glink_refs:
                for ref in conn.glink_refs:
                    if ref and ref != device_id:
                        connected.add(ref)
        return list(connected)

    def get_text_for_device(self, device_id: str) -> Optional[SvgText]:
        for txt in self.texts:
            if txt.object_id == device_id or txt.object_id == f"TXT_{device_id}":
                return txt
            if txt.content and device_id in txt.content:
                return txt
        return None

    # ------------------------------------------------------------------
    # 模型修改
    # ------------------------------------------------------------------
    def add_element(self, elem: SvgElement):
        self.elements.append(elem)

    def remove_element(self, device_id: str) -> bool:
        elem = self.get_device_by_id(device_id)
        if elem is None:
            return False
        self.elements.remove(elem)
        return True

    def add_connection(self, conn: SvgConnection):
        self.connections.append(conn)

    def remove_connection(self, conn: SvgConnection):
        if conn in self.connections:
            self.connections.remove(conn)

    def add_text(self, txt: SvgText):
        self.texts.append(txt)

    def remove_text(self, txt: SvgText):
        if txt in self.texts:
            self.texts.remove(txt)

    # ------------------------------------------------------------------
    # 导出
    # ------------------------------------------------------------------
    def export_elements_json(self, output_path: str):
        data = [e.to_dict() for e in self.elements]
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  图元JSON已导出: {output_path}")

    def export_elements_csv(self, output_path: str):
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        if not self.elements:
            print(f"  无图元数据，跳过CSV导出")
            return
        fieldnames = list(self.elements[0].to_dict().keys())
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for elem in self.elements:
                writer.writerow(elem.to_dict())
        print(f"  图元CSV已导出: {output_path}")

    def export_connections_json(self, output_path: str):
        data = [c.to_dict() for c in self.connections]
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  连接JSON已导出: {output_path}")

    def export_connections_csv(self, output_path: str):
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        if not self.connections:
            print(f"  无连接数据，跳过CSV导出")
            return
        fieldnames = list(self.connections[0].to_dict().keys())
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for conn in self.connections:
                writer.writerow(conn.to_dict())
        print(f"  连接CSV已导出: {output_path}")

    def export_texts_csv(self, output_path: str):
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        if not self.texts:
            print(f"  无文字数据，跳过CSV导出")
            return
        fieldnames = list(self.texts[0].to_dict().keys())
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for txt in self.texts:
                writer.writerow(txt.to_dict())
        print(f"  文字CSV已导出: {output_path}")

    # ------------------------------------------------------------------
    # 辅助
    # ------------------------------------------------------------------
    def _infer_voltage_from_class(self, class_str: str, elem: SvgElement):
        voltage_map = {
            "lkv10": "10kV", "lkv6": "6kV", "lkv3": "3kV",
            "lkv15.75": "15.75kV", "lkv13.8": "13.8kV",
            "lkv20": "20kV", "lkv35": "35kV", "lkv66": "66kV",
            "lkv110": "110kV", "lkv220": "220kV", "lkv330": "330kV",
            "lkv500": "500kV", "lkv750": "750kV", "lkv1000": "1000kV",
            "lv380": "380V", "lv220": "220V", "lv110": "110V",
            "lvdc": "直流",
        }
        for cls, v in voltage_map.items():
            if cls in class_str:
                elem.voltage_level = v
                return

    def _infer_voltage_from_psr_type(self, psr_type: str, elem: SvgElement):
        if psr_type in PSR_TYPE_MAP:
            elem.element_type = PSR_TYPE_MAP[psr_type]

    def _infer_voltage_from_stroke(self, stroke: str) -> str:
        voltage_colors = {
            "rgb(128,0,128)": "220kV", "rgb(240,65,85)": "110kV",
            "rgb(0,200,255)": "35kV", "rgb(255,204,0)": "66kV",
            "rgb(0,128,0)": "15.75kV", "rgb(0,210,0)": "13.8kV",
            "rgb(185,72,66)": "10kV", "rgb(0,0,139)": "6kV",
            "rgb(0,100,0)": "3kV",
        }
        return voltage_colors.get(stroke, "")

    @staticmethod
    def _extract_rotation(transform: str) -> float:
        if not transform:
            return 0.0
        match = re.search(r"rotate\(([-\d.]+)", transform)
        if match:
            return float(match.group(1))
        return 0.0

    @staticmethod
    def _parse_transform(transform: str) -> tuple:
        """解析SVG transform字符串，返回 (tx, ty, scale, rotation, can_rebuild)。

        支持 translate(x,y)、scale(s) / scale(sx,sy)、rotate(angle) /
        rotate(angle,cx,cy)。若解析失败或遇到无法识别的变换命令
        （skew/matrix），can_rebuild=False，写回时原样保留原始 transform 字符串。
        """
        tx, ty = 0.0, 0.0
        scale = 1.0
        rotation = 0.0
        if not transform:
            return tx, ty, scale, rotation, True

        # 无法重建的变换命令
        if re.search(r'(skew|matrix)\s*\(', transform, re.IGNORECASE):
            return tx, ty, scale, rotation, False

        m = re.search(r'translate\(([-\d.]+)[,\s]+([-\d.]+)\)', transform)
        if m:
            tx, ty = float(m.group(1)), float(m.group(2))
        m = re.search(r'scale\(([-\d.]+)(?:[,\s]+([-\d.]+))?\)', transform)
        if m:
            sx = float(m.group(1))
            sy = float(m.group(2)) if m.group(2) else sx
            scale = (sx + sy) / 2.0
        m = re.search(r'rotate\(([-\d.]+)(?:[,\s]+([-\d.]+)[,\s]+([-\d.]+))?\)', transform)
        if m:
            rotation = float(m.group(1))
        return tx, ty, scale, rotation, True

    @staticmethod
    def _parse_points(points_str: str) -> list[tuple[float, float]]:
        points = []
        if not points_str:
            return points
        for pt in points_str.strip().split():
            parts = pt.split(",")
            if len(parts) == 2:
                try:
                    points.append((float(parts[0]), float(parts[1])))
                except ValueError:
                    continue
        return points


# ----------------------------------------------------------------------
# 便捷函数
# ----------------------------------------------------------------------
def run_parse_test():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    svg_dir = os.path.join(project_root, "数据集更新版20260729", "配网 svg")
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    for fname in ["LINE215.svg", "LINE216.svg"]:
        fpath = os.path.join(svg_dir, fname)
        if not os.path.exists(fpath):
            print(f"文件不存在: {fpath}")
            continue

        print(f"\n{'='*60}")
        print(f"解析 {fname}")
        print(f"{'='*60}")

        doc = SvgDocument(fpath)
        if doc.parse():
            base_name = os.path.splitext(fname)[0]
            csv_dir = os.path.join(output_dir, "csv")
            json_dir = os.path.join(output_dir, "json")
            os.makedirs(csv_dir, exist_ok=True)
            os.makedirs(json_dir, exist_ok=True)

            doc.export_elements_csv(os.path.join(csv_dir, f"{base_name}_elements.csv"))
            doc.export_elements_json(os.path.join(json_dir, f"{base_name}_elements.json"))
            doc.export_connections_csv(os.path.join(csv_dir, f"{base_name}_connections.csv"))
            doc.export_connections_json(os.path.join(json_dir, f"{base_name}_connections.json"))
            doc.export_texts_csv(os.path.join(csv_dir, f"{base_name}_texts.csv"))

            print(f"\n--- 设备类型统计 ---")
            type_counts = defaultdict(int)
            for elem in doc.elements:
                type_counts[elem.element_type] += 1
            for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
                print(f"  {t}: {c}")

            print(f"\n--- 连接统计 ---")
            connected_count = sum(1 for c in doc.connections if c.start_device_id or c.end_device_id)
            print(f"  总连接数: {len(doc.connections)}")
            print(f"  已解析设备连接: {connected_count}")


if __name__ == "__main__":
    run_parse_test()
>>>>>>> 28dd083296963d2896e56ae8eca2483f9a9e66f7
