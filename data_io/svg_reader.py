"""SVG文件解析器 - 解析配电网单线图SVG，提取图元、连接关系和拓扑数据。

本模块是闭环流程的核心入口：
    原始 SVG -> SvgDocument.parse() -> 中间模型
    中间模型 -> SvgDocumentWriter.write() -> 新 SVG
    新 SVG -> SvgDocument.parse() -> 验证中间模型
"""
import math
import xml.etree.ElementTree as ET
import os
import re
import json
import csv
import copy
import uuid
from collections import defaultdict
from typing import Optional, List, Tuple, Dict, Any

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
IEC_NS = "http://iec.ch/TC57/2005/SVG-schema#"

ET.register_namespace("cim", IEC_NS)
ET.register_namespace("xlink", XLINK_NS)

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

# 设备图层顺序
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

class Matrix:
    """2D 变换矩阵 (3x3)"""
    def __init__(self, a=1.0, b=0.0, c=0.0, d=1.0, e=0.0, f=0.0):
        self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f

    def multiply(self, other: 'Matrix') -> 'Matrix':
        return Matrix(
            self.a * other.a + self.c * other.b,
            self.b * other.a + self.d * other.b,
            self.a * other.c + self.c * other.d,
            self.b * other.c + self.d * other.d,
            self.a * other.e + self.c * other.f + self.e,
            self.b * other.e + self.d * other.f + self.f
        )

    def apply(self, x: float, y: float) -> Tuple[float, float]:
        nx = self.a * x + self.c * y + self.e
        ny = self.b * x + self.d * y + self.f
        return nx, ny

    def get_rotation(self) -> float:
        """从矩阵中提取旋转角度（单位：度）。"""
        return math.degrees(math.atan2(self.b, self.a)) % 360

    def get_scale(self) -> float:
        """从矩阵中提取均匀缩放比例。"""
        return (self.a**2 + self.b**2)**0.5

    @staticmethod
    def translate(tx: float, ty: float) -> 'Matrix':
        return Matrix(1, 0, 0, 1, tx, ty)

    @staticmethod
    def scale(sx: float, sy: Optional[float] = None) -> 'Matrix':
        if sy is None: sy = sx
        return Matrix(sx, 0, 0, sy, 0, 0)

    @staticmethod
    def rotate(angle: float, cx: float = 0, cy: float = 0) -> 'Matrix':
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        m = Matrix.translate(cx, cy)
        m = m.multiply(Matrix(cos_a, sin_a, -sin_a, cos_a, 0, 0))
        return m.multiply(Matrix.translate(-cx, -cy))

def _parse_transform_to_matrix(transform_str: str) -> Matrix:
    res = Matrix()
    if not transform_str:
        return res
    commands = re.findall(r'(\w+)\(([^)]+)\)', transform_str)
    for cmd, args_str in commands:
        args = [float(x.strip()) for x in re.split(r'[,\s]+', args_str.strip()) if x.strip()]
        if cmd == "translate":
            tx = args[0]
            ty = args[1] if len(args) > 1 else 0.0
            res = res.multiply(Matrix.translate(tx, ty))
        elif cmd == "scale":
            sx = args[0]
            sy = args[1] if len(args) > 1 else sx
            res = res.multiply(Matrix.scale(sx, sy))
        elif cmd == "rotate":
            angle = args[0]
            cx = args[1] if len(args) > 1 else 0.0
            cy = args[2] if len(args) > 2 else 0.0
            res = res.multiply(Matrix.rotate(angle, cx, cy))
        elif cmd == "matrix":
            if len(args) == 6:
                res = res.multiply(Matrix(*args))
    return res

class SvgElement:
    """SVG 图元中间模型"""
    def __init__(self):
        self.element_id: str = ""
        self.element_type: str = ""
        self.element_name: str = ""
        self.psr_type: str = ""
        self.x: float = 0.0
        self.y: float = 0.0
        self.raw_x: float = 0.0
        self.raw_y: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.rotation: float = 0.0
        self.symbol_href: str = ""
        self.glink_refs: List[str] = []
        self.container_id: str = ""
        self.voltage_level: str = ""
        self.line_type: str = ""
        self.top_type: str = ""
        self.business_type: str = ""
        self.layer_name: str = ""
        self.points: List[Tuple[float, float]] = []
        self.shape_tag: str = "use"
        self.shape_attrs: Dict = {}
        self.transform: str = ""
        self.raw_transform: str = ""
        self._transform_tx: float = 0.0
        self._transform_ty: float = 0.0
        self._transform_scale: float = 1.0
        self._transform_rotation: float = 0.0
        self._transform_can_rebuild: bool = True
        self.css_class: str = ""
        self.fill: str = ""
        self.stroke: str = ""
        self.stroke_width: str = ""
        self.raw_metadata: Dict = {}
        self.raw_element: Optional[ET.Element] = None

    def to_dict(self) -> Dict:
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
            "container_id": self.container_id,
            "voltage_level": self.voltage_level,
            "line_type": self.line_type,
            "layer_name": self.layer_name,
            "points": self.points
        }

    def rebuild_transform(self):
        if not self._transform_can_rebuild:
            self.transform = self.raw_transform
            return
        parts = []
        # 注意：位移和缩放已经烘焙进 x, y, width, height 中
        # 为了防止双重缩放，transform 中仅保留旋转
        if self.rotation != 0:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            parts.append(f"rotate({self.rotation:.6f},{cx:.6f},{cy:.6f})")
        self.transform = " ".join(parts)

class SvgConnection:
    """SVG 连接线中间模型"""
    def __init__(self):
        self.connection_id: str = ""
        self.connection_name: str = ""
        self.line_type: str = ""
        self.psr_type: str = ""
        self.points: List[Tuple[float, float]] = []
        self.glink_refs: List[str] = []
        self.layer_ref: str = ""
        self.start_device_id: str = ""
        self.end_device_id: str = ""
        self.top_type: str = ""
        self.business_type: str = ""
        self.voltage_level: str = ""
        self.css_class: str = ""
        self.fill: str = "none"
        self.stroke: str = ""
        self.stroke_width: str = ""
        self.stroke_linecap: str = "round"
        self.stroke_linejoin: str = "round"
        self.stroke_dasharray: str = ""
        self.raw_metadata: Dict = {}

    def to_dict(self) -> Dict:
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
        }

class SvgText:
    """SVG 文字标注中间模型"""
    def __init__(self):
        self.text_id: str = ""
        self.content: str = ""
        self.raw_content: str = ""
        self.x: float = 0.0
        self.y: float = 0.0
        self.font_size: float = 0.0
        self.object_id: str = ""
        self.raw_object_id: str = ""
        self.object_name: str = ""
        self.layer_ref: str = ""
        self.line_type: str = ""
        self.business_type: str = ""
        self.top_type: str = ""
        self.dx: float = 0.0
        self.dy: float = 0.0
        self.text_anchor: str = "middle"
        self.dominant_baseline: str = "auto"
        self.text_role: str = ""
        self.hidden: bool = False
        self.fill: str = ""
        self.font_family: str = ""
        self.stroke: str = "none"
        self.style: str = "text-anchor:middle"
        self.font_weight: str = "normal"
        self.raw_metadata: Dict = {}
        self.raw_element: Optional[ET.Element] = None

    def to_dict(self) -> Dict:
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
        }

class SvgDocument:
    """SVG 文档中间模型"""
    def __init__(self, svg_path: str, feeder_id: Optional[str] = None, line_df=None):
        self.svg_path = svg_path
        self.svg_filename = os.path.basename(svg_path)
        base_name = os.path.splitext(self.svg_filename)[0].split("_")[0]
        if feeder_id:
            self.feeder_id = feeder_id
        elif line_df is not None and len(line_df) > 0:
            self.feeder_id = self._resolve_feeder_from_line_df(base_name, line_df)
        else:
            hardcode_map = {"LINE215": "TMP00000188", "LINE216": "TMP00000189"}
            self.feeder_id = hardcode_map.get(base_name, base_name)
        self._line_df = line_df
        self.elements: List[SvgElement] = []
        self.connections: List[SvgConnection] = []
        self.texts: List[SvgText] = []
        self.tree: Optional[ET.ElementTree] = None
        self.root: Optional[ET.Element] = None
        self.viewbox: Tuple = (0, 0, 0, 0)
        self.width: float = 0.0
        self.height: float = 0.0
        self.coordinate_extent: str = ""
        self.preserve_aspect_ratio: str = ""
        self._symbol_defs: Dict[str, Dict] = {}

    @staticmethod
    def _resolve_feeder_from_line_df(base_name: str, line_df) -> str:
        """从馈线表解析 LINE074/10kVLINE074/74 → 真实 LINE_ID (TMPxxxx)。
        对齐 tests/compare.resolve_feeder_id，消除硬编码 FEEDER_MAP。
        """
        import pandas as pd_
        kw = base_name.strip()
        kw_low = kw.lower()
        try:
            if "LINE_NAME" in line_df.columns:
                name_series = line_df["LINE_NAME"].astype(str).str.lower()
                # 1. 精确匹配
                matches = line_df[name_series == kw_low]
                if len(matches) > 0:
                    return str(matches.iloc[0]["LINE_ID"])
            # 2. 提取数字后缀，按末尾N位匹配
            digit_suffix = kw_low
            for prefix in ("10kvline", "35kvline", "110kvline", "kvline", "line"):
                if digit_suffix.startswith(prefix):
                    digit_suffix = digit_suffix[len(prefix):]
            # LINE074 → "074"，尝试匹配 LINE_NAME 中含 074 的记录
            if digit_suffix and len(digit_suffix) >= 2:
                if "LINE_NAME" in line_df.columns:
                    # 提取 LINE_NAME 中的数字部分
                    extracted = line_df["LINE_NAME"].astype(str).str.extract(r"(\d{2,4})", expand=False).fillna("")
                    # 先尝试末尾3位精确匹配
                    last3 = digit_suffix[-3:] if len(digit_suffix) >= 3 else digit_suffix
                    mask = extracted.str.endswith(last3)
                    if mask.any():
                        return str(line_df[mask].iloc[0]["LINE_ID"])
                    # 再尝试末尾2位
                    last2 = digit_suffix[-2:]
                    mask2 = extracted.str.endswith(last2)
                    if mask2.any():
                        return str(line_df[mask2].iloc[0]["LINE_ID"])
        except Exception:
            pass
        return kw

    def parse(self) -> bool:
        try:
            # 每次解析前清除旧数据，防止重复调用导致数据倍增
            self.elements = []
            self.connections = []
            self.texts = []
            self._symbol_defs = {}
            
            self.tree = ET.parse(self.svg_path)
            self.root = self.tree.getroot()
            self._parse_svg_attrs()
            self._parse_symbol_defs()
            
            root_transform = self.root.get("transform", "")
            root_matrix = _parse_transform_to_matrix(root_transform)
            
            self._parse_styles(self.root)
            self._parse_svg_layers(self.root, root_matrix)
            self._resolve_connection_links()
            
            print(f"  解析完成: {len(self.elements)} 个设备, {len(self.connections)} 条连接, {len(self.texts)} 个文字标注")
            return True
        except Exception as e:
            print(f"  解析失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _parse_svg_attrs(self):
        if self.root is None: return
        self.width = float(self.root.get("width", "0"))
        self.height = float(self.root.get("height", "0"))
        self.coordinate_extent = self.root.get("coordinateExtent", "")
        self.preserve_aspect_ratio = self.root.get("preserveAspectRatio", "")
        viewbox = self.root.get("viewBox", "0 0 0 0")
        parts = viewbox.split()
        if len(parts) == 4: self.viewbox = tuple(float(p) for p in parts)

    def _parse_symbol_defs(self):
        if self.root is None: return
        for sym in self.root.iter(f"{{{SVG_NS}}}symbol"):
            sym_id = sym.get("id", "")
            if sym_id:
                viewbox = sym.get("viewBox", "0 0 0 0")
                parts = viewbox.split()
                w, h = 0, 0
                if len(parts) == 4: w, h = float(parts[2]), float(parts[3])
                self._symbol_defs[sym_id] = {"id": sym_id, "width": w, "height": h, "type": self._infer_symbol_type(sym_id)}

    def _infer_symbol_type(self, symbol_id: str) -> str:
        for key, val in DEVICE_TYPE_MAP.items():
            if symbol_id.startswith(key): return val
        return "未知"

    def _parse_styles(self, root: ET.Element):
        pass

    def _parse_svg_layers(self, root: ET.Element, root_matrix: Matrix):
        for child in root:
            tag = _local_tag(child.tag)
            if tag == "g":
                layer_id = child.get("id", "")
                layer_transform = child.get("transform", "")
                layer_matrix = root_matrix.multiply(_parse_transform_to_matrix(layer_transform))
                
                if layer_id in DEVICE_LAYERS:
                    layer_name = layer_id.replace("_Layer", "")
                    self._parse_device_layer(child, layer_name, layer_matrix)
                elif layer_id == "ConnLine_Layer":
                    self._parse_connection_layer(child, layer_matrix)
                elif layer_id == "Text_Layer":
                    self._parse_text_layer(child, layer_matrix)
                else:
                    self._parse_device_layer(child, layer_id, layer_matrix)
            elif tag == "text":
                txt = self._parse_text_element(child, root_matrix)
                if txt: self.texts.append(txt)

    def _parse_device_layer(self, layer_elem: ET.Element, layer_name: str, parent_matrix: Matrix):
        for child in layer_elem:
            tag = _local_tag(child.tag)
            if tag == "g":
                self._parse_device_element(child, layer_name, parent_matrix)
            elif tag in ("use", "rect", "polygon", "polyline", "path", "circle", "line"):
                elem = self._parse_single_shape_element(child, layer_name, parent_matrix)
                if elem: self.elements.append(elem)

    def _parse_single_shape_element(self, shape_elem: ET.Element, layer_name: str, parent_matrix: Matrix) -> Optional[SvgElement]:
        elem = SvgElement()
        elem.layer_name = layer_name
        elem.element_type = DEVICE_TYPE_MAP.get(layer_name, layer_name)
        elem.shape_tag = _local_tag(shape_elem.tag)
        elem.shape_attrs = dict(shape_elem.attrib)
        elem.element_id = shape_elem.get("id") or f"AUTO_{layer_name}_{uuid.uuid4().hex[:8]}"
        self._apply_shape_to_element(shape_elem, elem, layer_name, parent_matrix)
        metadata = shape_elem.find(f"{{{SVG_NS}}}metadata")
        if metadata is not None: self._parse_metadata(metadata, elem)
        elem.raw_element = copy.deepcopy(shape_elem)
        fill = (elem.shape_attrs.get("fill") or elem.fill or "").replace("#", "").replace(" ", "").lower()
        stroke = (elem.shape_attrs.get("stroke") or elem.stroke or "").replace("#", "").replace(" ", "").lower()
        if elem.shape_tag == "rect" and not metadata:
            if fill in {"ffffff", "white", "fff", ""} and stroke in {"none", "ffffff", "white", "fff", ""}:
                return None
        # 额外过滤：无 metadata 且无 element_name 的 rect 在设备 <g> 内为背景装饰
        if elem.shape_tag == "rect" and not metadata and not elem.element_name:
            return None
        if elem.layer_name in {"Junction", "RemoteUnit", "Other"} and not metadata and not elem.element_name:
            pass
        return elem

    def _parse_device_element(self, g_elem: ET.Element, layer_name: str, parent_matrix: Matrix, parent_metadata: Optional[ET.Element] = None):
        g_transform = g_elem.get("transform", "")
        combined_matrix = parent_matrix.multiply(_parse_transform_to_matrix(g_transform))
        local_metadata = g_elem.find(f"{{{SVG_NS}}}metadata")
        current_metadata = local_metadata if local_metadata is not None else parent_metadata
        
        for child in g_elem:
            tag = _local_tag(child.tag)
            if tag == "g":
                self._parse_device_element(child, layer_name, combined_matrix, current_metadata)
            elif tag in ("use", "rect", "polygon", "polyline", "path", "circle", "line"):
                elem = SvgElement()
                elem.layer_name = layer_name
                elem.element_type = DEVICE_TYPE_MAP.get(layer_name, layer_name)
                elem.shape_tag = tag
                elem.shape_attrs = dict(child.attrib)
                elem.element_id = child.get("id") or g_elem.get("id") or f"AUTO_{layer_name}_{uuid.uuid4().hex[:8]}"
                self._apply_shape_to_element(child, elem, layer_name, combined_matrix)
                if current_metadata is not None: self._parse_metadata(current_metadata, elem)
                elem.raw_element = copy.deepcopy(child)
                self.elements.append(elem)
            elif tag == "text":
                txt = self._parse_text_element_direct(child, combined_matrix, current_metadata)
                if txt: self.texts.append(txt)

    def _parse_text_element_direct(self, text_elem: ET.Element, parent_matrix: Matrix, metadata_elem: Optional[ET.Element] = None) -> Optional[SvgText]:
        """直接解析 text 标签，而不假设它被包裹在 g 中。"""
        local_matrix = _parse_transform_to_matrix(text_elem.get("transform", ""))
        full_matrix = parent_matrix.multiply(local_matrix)
        
        txt = SvgText()
        txt.text_id = text_elem.get("id") or f"AUTO_TXT_{uuid.uuid4().hex[:8]}"
        txt.content = (text_elem.text or "").strip()
        txt.x, txt.y = full_matrix.apply(float(text_elem.get("x", "0")), float(text_elem.get("y", "0")))
        world_scale = full_matrix.get_scale()
        txt.font_size = float(text_elem.get("font-size", "12")) * world_scale
        txt.dx = float(text_elem.get("dx", "0")) * world_scale
        txt.dy = float(text_elem.get("dy", "0")) * world_scale
        
        if metadata_elem is not None:
            self._parse_text_metadata(metadata_elem, txt)
        
        txt.raw_element = ET.Element(f"{{{SVG_NS}}}g")
        txt.raw_element.append(copy.deepcopy(text_elem))
        return txt

    def _apply_shape_to_element(self, child: ET.Element, elem: SvgElement, layer_name: str, parent_matrix: Matrix):
        tag = _local_tag(child.tag)
        local_transform = child.get("transform", "")
        full_matrix = parent_matrix.multiply(_parse_transform_to_matrix(local_transform))
        elem.raw_transform = local_transform
        
        local_x, local_y, local_w, local_h = 0.0, 0.0, 0.0, 0.0
        local_points = []
        if tag == "use":
            local_x, local_y = float(child.get("x", "0")), float(child.get("y", "0"))
            local_w, local_h = float(child.get("width", "0")), float(child.get("height", "0"))
            elem.symbol_href = child.get(f"{{{XLINK_NS}}}href", "")
            if local_w <= 0 and local_h <= 0:
                sym = self._symbol_defs.get(elem.symbol_href.lstrip("#"), {})
                local_w, local_h = sym.get("width", 0), sym.get("height", 0)
        elif tag == "rect":
            local_x, local_y = float(child.get("x", "0")), float(child.get("y", "0"))
            local_w, local_h = float(child.get("width", "0")), float(child.get("height", "0"))
        elif tag in ("polygon", "polyline"):
            local_points = self._parse_points(child.get("points", ""))
            if local_points:
                xs, ys = [p[0] for p in local_points], [p[1] for p in local_points]
                local_x, local_y = min(xs), min(ys)
                local_w, local_h = max(xs) - min(xs), max(ys) - min(ys)
        elif tag == "circle":
            r = float(child.get("r", "0"))
            local_x, local_y = float(child.get("cx", "0")) - r, float(child.get("cy", "0")) - r
            local_w, local_h = r * 2, r * 2
        elif tag == "line":
            x1, y1 = float(child.get("x1", "0")), float(child.get("y1", "0"))
            x2, y2 = float(child.get("x2", "0")), float(child.get("y2", "0"))
            local_x, local_y = min(x1, x2), min(y1, y2)
            local_w, local_h = abs(x2 - x1), abs(y2 - y1)
            local_points = [(x1, y1), (x2, y2)]

        # 核心：将坐标变换为世界坐标
        elem.x, elem.y = full_matrix.apply(local_x, local_y)
        world_scale = full_matrix.get_scale()
        elem.width, elem.height = local_w * world_scale, local_h * world_scale
        if local_points: 
            elem.points = [full_matrix.apply(px, py) for px, py in local_points]
        
        # 烘焙旋转和缩放
        elem.rotation = full_matrix.get_rotation()
        elem._transform_scale = world_scale
        elem.rebuild_transform()

    def _parse_connection_layer(self, layer_elem: ET.Element, parent_matrix: Matrix):
        for conn_g in layer_elem.findall(f"{{{SVG_NS}}}g"):
            conn = self._parse_connection_element(conn_g, parent_matrix)
            if conn: self.connections.append(conn)

    def _parse_connection_element(self, g_elem: ET.Element, parent_matrix: Matrix) -> Optional[SvgConnection]:
        conn = SvgConnection()
        conn.connection_id = g_elem.get("id", "")
        g_matrix = parent_matrix.multiply(_parse_transform_to_matrix(g_elem.get("transform", "")))
        for child in g_elem:
            tag = _local_tag(child.tag)
            if tag == "polyline":
                local_points = self._parse_points(child.get("points", ""))
                conn.points = [g_matrix.apply(px, py) for px, py in local_points]
                conn.css_class = child.get("class", "")
                conn.stroke = child.get("stroke", "")
                conn.voltage_level = self._infer_voltage_from_stroke(conn.stroke)
            elif tag == "metadata":
                self._parse_connection_metadata(child, conn)
        return conn

    def _parse_text_layer(self, layer_elem: ET.Element, parent_matrix: Matrix):
        for text_g in layer_elem.findall(f"{{{SVG_NS}}}g"):
            txt = self._parse_text_element(text_g, parent_matrix)
            if txt: self.texts.append(txt)

    def _parse_text_element(self, g_elem: ET.Element, parent_matrix: Matrix) -> Optional[SvgText]:
        g_matrix = parent_matrix.multiply(_parse_transform_to_matrix(g_elem.get("transform", "")))
        text_elem = g_elem.find(f"{{{SVG_NS}}}text")
        if text_elem is None: return None
        txt = SvgText()
        txt.text_id = g_elem.get("id", "")
        txt.content = (text_elem.text or "").strip()
        local_matrix = _parse_transform_to_matrix(text_elem.get("transform", ""))
        full_matrix = g_matrix.multiply(local_matrix)
        txt.x, txt.y = full_matrix.apply(float(text_elem.get("x", "0")), float(text_elem.get("y", "0")))
        world_scale = full_matrix.get_scale()
        txt.font_size = float(text_elem.get("font-size", "12")) * world_scale
        txt.dx = float(text_elem.get("dx", "0")) * world_scale
        txt.dy = float(text_elem.get("dy", "0")) * world_scale
        txt.object_id = g_elem.get("id", "").replace("TXT_", "")
        metadata = g_elem.find(f"{{{SVG_NS}}}metadata")
        if metadata is not None: self._parse_text_metadata(metadata, txt)
        txt.raw_element = copy.deepcopy(g_elem)
        return txt

    def _parse_metadata(self, metadata_elem: ET.Element, elem: SvgElement):
        for child in metadata_elem:
            tag = _local_tag(child.tag)
            if tag == "PSR_Ref":
                # 统一使用 IEC 规范属性名 ObjectName/PSRType
                oid = (child.get("ObjectName") or child.get("objectName")
                       or child.get("ObjectID") or child.get("ObjectId")
                       or child.get("ID") or child.get("id")
                       or elem.element_id)
                elem.element_id = oid or elem.element_id
                name = (child.get("ObjectName")
                        or child.get("objectName")
                        or "")
                elem.element_name = name
                psr_type = (child.get("PSRType")
                            or child.get("PSR_TYPE")
                            or elem.psr_type
                            or "")
                elem.psr_type = psr_type
                self._infer_voltage_from_psr_type(psr_type, elem)
            elif tag == "GLink_Ref":
                gid = child.get("ObjectID") or child.get("ObjectId") or child.get("ID") or ""
                if gid:
                    elem.glink_refs.append(gid)

    def _parse_connection_metadata(self, metadata_elem: ET.Element, conn: SvgConnection):
        for child in metadata_elem:
            tag = _local_tag(child.tag)
            if tag == "PSR_Ref":
                conn.connection_id = child.get("ObjectID", conn.connection_id)
                conn.connection_name = child.get("ObjectName", "")
            elif tag == "GLink_Ref":
                gid = child.get("ObjectID", "")
                if gid: conn.glink_refs.append(gid)

    def _parse_text_metadata(self, metadata_elem: ET.Element, txt: SvgText):
        for child in metadata_elem:
            tag = _local_tag(child.tag)
            if tag == "PSR_Ref":
                txt.object_id = child.get("ObjectID", txt.object_id).replace("TXT_", "")
                txt.object_name = child.get("ObjectName", "")

    def _resolve_connection_links(self):
        device_map = {e.element_id: e for e in self.elements if e.element_id}
        for conn in self.connections:
            if not conn.points: continue
            start_p, end_p = conn.points[0], conn.points[-1]
            for dev_id, dev in device_map.items():
                d_start = ((dev.x + dev.width/2 - start_p[0])**2 + (dev.y + dev.height/2 - start_p[1])**2)**0.5
                if d_start < 5.0: conn.start_device_id = dev_id
                d_end = ((dev.x + dev.width/2 - end_p[0])**2 + (dev.y + dev.height/2 - end_p[1])**2)**0.5
                if d_end < 5.0: conn.end_device_id = dev_id

    def _infer_voltage_from_psr_type(self, psr_type: str, elem: SvgElement):
        """将电压等级归一化为数据库可比较的数值码：10kV -> 1010, 35kV -> 1035 等。"""
        if elem.voltage_level:
            text = elem.voltage_level
        else:
            text = str(psr_type or "")
        t = text.strip().lower().replace(" ", "").replace("kv", "")
        if t in {"10", "1010", "10k", "p10"}:
            elem.voltage_level = "1010"
        elif t in {"35", "1035", "35k"}:
            elem.voltage_level = "1035"
        elif t in {"110", "1110", "110k"}:
            elem.voltage_level = "1110"
        elif t in {"220", "1220", "220k"}:
            elem.voltage_level = "1220"
        elif t in {"6", "1006", "6k"}:
            elem.voltage_level = "1006"
        else:
            if "10" in t or not t:
                elem.voltage_level = "1010"
            else:
                elem.voltage_level = str(text)

    def _infer_voltage_from_stroke(self, stroke: str) -> str:
        """stroke颜色匹配后返回数值码，避免字符串比较误报。"""
        if "185,72,66" in stroke.replace(" ", "") or "ff0000" in stroke.lower():
            return "1010"
        return ""

    def _parse_points(self, points_str: str) -> List[Tuple[float, float]]:
        nums = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", points_str)
        return [(float(nums[i]), float(nums[i+1])) for i in range(0, len(nums) - 1, 2)]

    def dump_ir(self, output_path: str):
        data = {
            "metadata": {"filename": self.svg_filename, "feeder_id": self.feeder_id, "viewbox": self.viewbox},
            "elements": [e.to_dict() for e in self.elements],
            "connections": [c.to_dict() for c in self.connections],
            "texts": [t.to_dict() for t in self.texts]
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_device_by_id(self, device_id: str) -> Optional[SvgElement]:
        if not hasattr(self, "_dev_map"):
            self._dev_map = {e.element_id: e for e in self.elements if e.element_id}
        return self._dev_map.get(device_id)

    def get_connection_by_id(self, conn_id: str) -> Optional[SvgConnection]:
        if not hasattr(self, "_conn_map"):
            self._conn_map = {c.connection_id: c for c in self.connections if c.connection_id}
        return self._conn_map.get(conn_id)

    def get_text_by_id(self, text_id: str) -> Optional[SvgText]:
        if not hasattr(self, "_text_map"):
            self._text_map = {t.text_id: t for t in self.texts if t.text_id}
        return self._text_map.get(text_id)

    def add_connection(self, conn: SvgConnection):
        self.connections.append(conn)
        if hasattr(self, "_conn_map") and conn.connection_id:
            self._conn_map[conn.connection_id] = conn

    def add_element(self, elem: SvgElement):
        self.elements.append(elem)
        if hasattr(self, "_dev_map") and elem.element_id:
            self._dev_map[elem.element_id] = elem

    def add_text(self, text: SvgText):
        self.texts.append(text)

LINE_TYPE_MAP = {
    '#00A854': 'main_line',
    '#FF6A00': 'tie_line',
    '#722ED1': 'inter_station_line',
    '#BFBFBF': 'spare_line',
    '#1890FF': 'trace_path',
}
LINE_TYPE_NAME_MAP = {
    'main_line': '主干线', 'tie_line': '联络线', 'inter_station_line': '站间连线',
    'spare_line': '备用线', 'trace_path': '追踪路径', 'branch_line': '支线',
    'container_border': '容器边界', 'Trunk': '主干', 'Branch': '分支', 'Tie': '联络'
}

class _LegacyDocAdapter:
    def __init__(self, new_doc):
        self.new_doc = new_doc
        self.filename = new_doc.svg_filename
        self.elements = {e.element_id: self._adapt_element(e) for e in new_doc.elements if e.element_id}
        self.lines = {c.connection_id: self._adapt_line(c) for c in new_doc.connections if c.connection_id}
        self.texts = {t.text_id: self._adapt_text(t) for t in new_doc.texts if t.text_id}
        self.symbol_defs = getattr(new_doc, '_symbol_defs', {})
        self.connections = []
        for c in new_doc.connections:
            self.connections.append(type('_Conn', (), {
                'from_element_id': c.start_device_id, 'from_terminal': 1,
                'to_element_id': c.end_device_id, 'to_terminal': 2,
                'line_id': c.connection_id,
                'to_dict': lambda self0: {
                    'from_element_id': self0.from_element_id, 'from_terminal': self0.from_terminal,
                    'to_element_id': self0.to_element_id, 'to_terminal': self0.to_terminal,
                    'line_id': self0.line_id,
                }
            })())

    def _adapt_element(self, e):
        TYPE_NAME_MAP = dict(DEVICE_TYPE_MAP)
        elem_type = e.layer_name if e.layer_name else e.element_type
        el = type('_LgEl', (), {
            'element_id': e.element_id,
            'element_type': elem_type,
            'x': e.x, 'y': e.y,
            'width': e.width, 'height': e.height,
            'object_id': e.element_id,
            'object_name': e.element_name,
            'psr_type': e.psr_type,
            'layer': e.layer_name,
            'layer_id': f'{e.layer_name}_Layer' if e.layer_name else '',
            'symbol_id': e.symbol_href.lstrip('#') if e.symbol_href else '',
            'voltage_level': e.voltage_level,
            'css_class': e.css_class,
            'stroke_color': e.stroke,
            'fill_color': e.fill,
            'stroke_width': e.stroke_width,
            'related_text_ids': [],
            'is_junction': (e.layer_name == 'Junction'),
            'terminals': [],
            'add_related_text': lambda s, tid: s.related_text_ids.append(tid) if tid not in s.related_text_ids else None,
            'add_terminal': lambda s, t: s.terminals.append(t),
        })()
        for t in self.new_doc.texts:
            oid = getattr(t, 'object_id', '') or ''
            if oid and oid == e.element_id: el.related_text_ids.append(t.text_id)
        def _to_dict():
            return {
                'element_id': el.element_id, 'element_type': el.element_type,
                'element_type_cn': TYPE_NAME_MAP.get(el.element_type, el.element_type),
                'x': round(el.x, 4), 'y': round(el.y, 4),
                'width': round(el.width, 4), 'height': round(el.height, 4),
                'object_id': el.object_id, 'object_name': el.object_name,
                'psr_type': el.psr_type, 'layer': el.layer,
                'voltage_level': el.voltage_level, 'css_class': el.css_class,
                'stroke_color': el.stroke_color, 'is_junction': el.is_junction,
                'related_text_ids': el.related_text_ids,
                'terminals': []
            }
        el.to_dict = _to_dict
        return el

    def _adapt_line(self, c):
        line = type('_Ln', (), {
            'line_id': c.connection_id,
            'points': c.points,
            'line_type': c.line_type or '',
            'line_type_cn': LINE_TYPE_NAME_MAP.get(c.line_type or '', c.line_type) if c.line_type not in (None,'') else None,
            'start_point': c.points[0] if c.points else None,
            'end_point': c.points[-1] if c.points else None,
            'object_id': c.connection_id,
            'glink_refs': list(c.glink_refs),
            'voltage_level': c.voltage_level,
            'color': c.stroke or '',
            'stroke_width': c.stroke_width,
            'css_class': c.css_class,
            'inferred_type': None, 'inferred_type_cn': None,
        })()
        def _ld():
            return {
                'line_id': line.line_id,
                'points': [(round(p[0],4), round(p[1],4)) for p in line.points],
                'line_type': line.line_type, 'line_type_cn': line.line_type_cn,
                'inferred_type': line.inferred_type, 'inferred_type_cn': line.inferred_type_cn,
                'start_point': line.start_point, 'end_point': line.end_point,
                'object_id': line.object_id, 'glink_refs': line.glink_refs,
                'color': line.color, 'stroke_width': line.stroke_width,
                'voltage_level': line.voltage_level,
            }
        line.to_dict = _ld
        return line

    def _adapt_text(self, t):
        tx = type('_Tx', (), {
            'text_id': t.text_id,
            'x': t.x, 'y': t.y,
            'content': t.content,
            'font_size': t.font_size,
            'color': getattr(t, 'fill', ''),
            'object_id': t.object_id,
            'object_name': getattr(t, 'object_name', ''),
            'psr_type': '',
            'related_element_id': t.object_id if t.object_id and t.object_id in self.elements else None,
        })()
        def _td():
            return {
                'text_id': tx.text_id, 'x': round(tx.x,4), 'y': round(tx.y,4),
                'content': tx.content, 'font_size': round(tx.font_size,4),
                'color': tx.color, 'object_id': tx.object_id,
                'related_element_id': tx.related_element_id,
            }
        tx.to_dict = _td
        return tx

    def export_elements_json(self, filename='svg_elements.json'):
        from config.settings import OUTPUT_JSON
        import json as _json, os as _os
        data = {
            'filename': self.filename,
            'element_count': len(self.elements),
            'line_count': len(self.lines),
            'text_count': len(self.texts),
            'connection_count': len(self.connections),
            'elements': [e.to_dict() for e in self.elements.values()],
            'texts': [t.to_dict() for t in self.texts.values()],
        }
        save_path = _os.path.join(OUTPUT_JSON, filename)
        _os.makedirs(_os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
        return save_path

    def export_connections_json(self, filename='svg_connections.json'):
        from config.settings import OUTPUT_JSON
        import json as _json, os as _os
        data = {'filename': self.filename, 'connections': [c.to_dict() for c in self.connections]}
        save_path = _os.path.join(OUTPUT_JSON, filename)
        _os.makedirs(_os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
        return save_path

    def export_elements_csv(self, filename='svg_elements.csv'):
        from config.settings import OUTPUT_CSV
        import pandas as pd, os as _os
        rows = []
        TYPE_NAME_MAP = dict(DEVICE_TYPE_MAP)
        for elem in self.elements.values():
            rows.append({
                'element_id': elem.element_id, 'element_type': elem.element_type,
                'element_type_cn': TYPE_NAME_MAP.get(elem.element_type, elem.element_type),
                'x': round(elem.x, 4), 'y': round(elem.y, 4),
                'object_id': elem.object_id, 'object_name': elem.object_name,
                'psr_type': elem.psr_type, 'layer': elem.layer,
                'voltage_level': elem.voltage_level, 'css_class': elem.css_class,
                'stroke_color': elem.stroke_color, 'is_junction': elem.is_junction,
                'related_text_count': len(elem.related_text_ids),
            })
        save_path = _os.path.join(OUTPUT_CSV, filename)
        _os.makedirs(_os.path.dirname(save_path), exist_ok=True)
        pd.DataFrame(rows).to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

    def export_texts_csv(self, filename='svg_texts.csv'):
        from config.settings import OUTPUT_CSV
        import pandas as pd, os as _os
        rows = [{'text_id': t.text_id, 'x': round(t.x,4), 'y': round(t.y,4),
                 'content': t.content, 'font_size': round(t.font_size,4),
                 'color': t.color, 'object_id': t.object_id,
                 'related_element_id': t.related_element_id}
                for t in self.texts.values()]
        save_path = _os.path.join(OUTPUT_CSV, filename)
        _os.makedirs(_os.path.dirname(save_path), exist_ok=True)
        pd.DataFrame(rows).to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

    def export_connections_csv(self, filename='svg_connections.csv'):
        from config.settings import OUTPUT_CSV
        import pandas as pd, os as _os
        rows = []
        for conn in self.connections:
            from_elem = self.elements.get(conn.from_element_id)
            to_elem = self.elements.get(conn.to_element_id)
            line = self.lines.get(conn.line_id) if conn.line_id else None
            rows.append({
                'line_id': conn.line_id, 'line_type': line.line_type if line else '',
                'line_type_cn': line.line_type_cn if line else '',
                'from_element_id': conn.from_element_id,
                'from_element_name': from_elem.object_name if from_elem else '',
                'to_element_id': conn.to_element_id,
                'to_element_name': to_elem.object_name if to_elem else '',
            })
        save_path = _os.path.join(OUTPUT_CSV, filename)
        _os.makedirs(_os.path.dirname(save_path), exist_ok=True)
        pd.DataFrame(rows).to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

class SvgParser:
    @staticmethod
    def parse(file_path):
        doc = SvgDocument(file_path)
        if doc.parse(): return _LegacyDocAdapter(doc)
        return None
