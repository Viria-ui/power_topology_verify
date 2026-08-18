"""SVG 写入器 - 从 SvgDocument 中间模型重新生成 SVG。

闭环流程中的后半段：
    原始 SVG -> SvgDocument.parse() -> 中间模型
    中间模型 -> SvgDocumentWriter.write() -> 新 SVG
    新 SVG -> SvgDocument.parse() -> 验证
"""
import xml.etree.ElementTree as ET
import os
import copy
import re
import uuid
from collections import defaultdict

from data_io.svg_reader import (
    SvgDocument, SvgElement, SvgConnection, SvgText,
    SVG_NS, XLINK_NS, IEC_NS, DEVICE_LAYERS, DEVICE_TYPE_MAP,
)


def _local_tag(tag: str) -> str:
    if "}" in tag:
        return tag.split("}")[-1]
    return tag


def _new_g_id(prefix: str = "TMP") -> str:
    return f"{prefix}_{uuid.uuid4()}"


class SvgDocumentWriter:
    """将 SvgDocument 中间模型写回 SVG 文件。"""

    def __init__(self, doc: SvgDocument):
        self.doc = doc
        self._default_symbol_href: dict[str, str] = {}
        self._infer_default_symbols()

    # ------------------------------------------------------------------
    # 主入口
    # ------------------------------------------------------------------
    def write(self, output_path: str, update_style: bool = False, beautifier=None):
        """写回 SVG - 全量重建模式，确保输出与 IR 严格一致。"""
        abs_path = os.path.abspath(output_path)
        print(f"  [Writer] 正在写入文件: {abs_path}")
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        # 基于原始树深拷贝，保留 <defs> 符号定义和根属性
        if self.doc.tree is None:
            print("  [Writer] 错误: self.doc.tree 为空，无法写入！")
            return
            
        tree = copy.deepcopy(self.doc.tree)
        root = tree.getroot()

        # 更新根属性：viewBox 与 width/height 同步
        vb = self.doc.viewbox
        root.set("viewBox", f"{vb[0]:.6f} {vb[1]:.6f} {vb[2]:.6f} {vb[3]:.6f}")
        root.set("width", self._fmt(self.doc.width))
        root.set("height", self._fmt(self.doc.height))
        
        # 核心修复：移除可能干扰渲染的 coordinateExtent 属性
        if "coordinateExtent" in root.attrib:
            del root.attrib["coordinateExtent"]
        if "preserveAspectRatio" in root.attrib:
            root.set("preserveAspectRatio", "xMidYMid meet")

        # 获取 scale factor（供 style 生成使用）
        scale_factor = 1.0
        if beautifier is not None and hasattr(beautifier, '_vb_scale_factor'):
            scale_factor = beautifier._vb_scale_factor
        elif hasattr(self.doc, '_text_scale_factor'):
            scale_factor = self.doc._text_scale_factor
        self._current_scale_factor = scale_factor

        # ---- c. 建立四大图层索引 ----
        layer_index = {}
        def _norm_layer_id(dl: str) -> str:
            if dl.endswith("_Layer"):
                return dl
            return f"{dl}_Layer"
        device_layer_ids = [_norm_layer_id(dl) for dl in DEVICE_LAYERS]
        all_layer_ids = ["BackGround_Layer"] + device_layer_ids + ["ConnLine_Layer", "Text_Layer"]
        for layer_id in all_layer_ids:
            layer = root.find(f".//{{{SVG_NS}}}g[@id='{layer_id}']")
            if layer is None:
                layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
                layer.set("id", layer_id)
            layer_index[layer_id] = layer

        # ---- g. BackGround_Layer ----
        bg_layer = layer_index["BackGround_Layer"]
        for child in list(bg_layer):
            if _local_tag(child.tag) != "metadata":
                bg_layer.remove(child)
        self._write_background(root)

        # 设备按图层分组
        elements_by_layer = defaultdict(list)
        for elem in self.doc.elements:
            ln = elem.layer_name or ""
            if ln.endswith("_Layer"):
                layer_id = ln
            else:
                layer_id = f"{ln}_Layer"
            elements_by_layer[layer_id].append(elem)

        # ---- d. 设备更新：清空图层并全量重新写入，解决脏数据残留问题 ----
        for layer_id in device_layer_ids:
            layer = layer_index.get(layer_id)
            if layer is None:
                continue
            
            # 核心修复：清理旧图层内容，实现“全量重写”
            for child in list(layer):
                if _local_tag(child.tag) != "metadata":
                    layer.remove(child)
                
            layer_elements = elements_by_layer.get(layer_id, [])
            for elem in layer_elements:
                self._write_element(layer, elem)

        # ---- e. 连接线更新：清空 ConnLine_Layer 重建 ----
        conn_layer = layer_index["ConnLine_Layer"]
        for child in list(conn_layer):
            if _local_tag(child.tag) != "metadata":
                conn_layer.remove(child)
        for conn in self.doc.connections:
            self._write_connection(conn_layer, conn)

        # ---- f. 文字更新：清空 Text_Layer 全量重建 ----
        text_layer = layer_index["Text_Layer"]
        for child in list(text_layer):
            if _local_tag(child.tag) != "metadata":
                text_layer.remove(child)
        for txt in self.doc.texts:
            self._write_text(text_layer, txt)

        # 样式
        if update_style:
            self._write_beautified_style(root)

        # 注册命名空间
        try:
            ET.register_namespace("", SVG_NS)
            ET.register_namespace("xlink", XLINK_NS)
            ET.register_namespace("ns2", IEC_NS)
            ET.register_namespace("cim", IEC_NS)
        except ValueError:
            pass

        # 统一命名空间
        OLD_IEC_NS = "http://iec.ch/TC57/2005/SVG-schema#"
        IEC_NS_URI = IEC_NS 
        for node in tree.iter():
            if node.tag.startswith(f"{{{OLD_IEC_NS}}}"):
                node.tag = node.tag.replace(OLD_IEC_NS, IEC_NS_URI)
            for key in list(node.attrib.keys()):
                if key.startswith(f"{{{OLD_IEC_NS}}}"):
                    val = node.attrib.pop(key)
                    node.attrib[key.replace(OLD_IEC_NS, IEC_NS_URI)] = val

        ET.indent(tree, space="  ")
        tree.write(output_path, xml_declaration=True, encoding="UTF-8")
        return output_path

    def _update_single_shape_inplace(self, shape_elem: ET.Element, elem: SvgElement):
        """直接更新形状图元的属性。"""
        tag = _local_tag(shape_elem.tag)
        if tag == "use":
            shape_elem.set("x", self._fmt(elem.x))
            shape_elem.set("y", self._fmt(elem.y))
            if elem.transform: shape_elem.set("transform", elem.transform)
            if elem.width: shape_elem.set("width", self._fmt(elem.width))
            if elem.height: shape_elem.set("height", self._fmt(elem.height))
        elif tag in ("polygon", "polyline"):
            # 核心修复：优先使用 IR 中的 points 数组（世界坐标）
            if elem.points:
                pts_str = " ".join(f"{px:.4f},{py:.4f}" for px, py in elem.points)
                shape_elem.set("points", pts_str)
                # 由于 points 已经是世界坐标，清除 transform 防止双重平移
                if "transform" in shape_elem.attrib:
                    del shape_elem.attrib["transform"]
            else:
                points = elem.shape_attrs.get("points", "")
                if points: shape_elem.set("points", points)
        elif tag == "rect":
            shape_elem.set("x", self._fmt(elem.x))
            shape_elem.set("y", self._fmt(elem.y))
            shape_elem.set("width", self._fmt(elem.width))
            shape_elem.set("height", self._fmt(elem.height))
        elif tag == "circle":
            r = (elem.width or 0) / 2
            shape_elem.set("cx", self._fmt(elem.x + r))
            shape_elem.set("cy", self._fmt(elem.y + r))
            shape_elem.set("r", self._fmt(r))
        elif tag == "line":
            shape_elem.set("x1", self._fmt(elem.x))
            shape_elem.set("y1", self._fmt(elem.y))
            shape_elem.set("x2", self._fmt(elem.x + elem.width))
            shape_elem.set("y2", self._fmt(elem.y + elem.height))
        
        for child in list(shape_elem):
            if _local_tag(child.tag) == "metadata":
                shape_elem.remove(child)
        self._write_element_metadata(shape_elem, elem)

    def _write_element(self, layer: ET.Element, elem: SvgElement):
        """将单个设备写回 SVG，确保绝对定位与旋转烘焙。"""
        g_outer = ET.SubElement(layer, f"{{{SVG_NS}}}g")
        g_outer.set("id", elem.element_id or _new_g_id("TMP"))
        self._write_element_metadata(g_outer, elem)

        if elem.raw_element is not None:
            shape_elem = copy.deepcopy(elem.raw_element)
            if "id" in shape_elem.attrib:
                del shape_elem.attrib["id"]

            # 核心修复：针对重绘图元（线路、母线、站房），强制使用 IR 中的世界坐标点
            if elem.points and _local_tag(shape_elem.tag) in ("polyline", "polygon"):
                pts_str = " ".join(f"{px:.4f},{py:.4f}" for px, py in elem.points)
                shape_elem.set("points", pts_str)
                # 清除位移变换，因为 points 已经是世界坐标
                if "transform" in shape_elem.attrib: del shape_elem.attrib["transform"]
                # 应用 CSS 类
                if elem.css_class: shape_elem.set("class", elem.css_class)
                # 清除 inline 样式
                for attr in ["stroke", "stroke-width", "fill", "stroke-opacity"]:
                    if attr in shape_elem.attrib: del shape_elem.attrib[attr]
            
            # 核心修复：针对 symbol 引用 (use)，使用绝对坐标 x, y
            elif _local_tag(shape_elem.tag) == "use":
                shape_elem.set("x", self._fmt(elem.x))
                shape_elem.set("y", self._fmt(elem.y))
                shape_elem.set("width", self._fmt(elem.width))
                shape_elem.set("height", self._fmt(elem.height))
                
                # 仅保留必要的旋转和缩放变换
                if elem.transform:
                    shape_elem.set("transform", elem.transform)
                else:
                    if "transform" in shape_elem.attrib: del shape_elem.attrib["transform"]
            
            # 递归清理子图元的 transform，防止嵌套变换导致的位置偏移
            for child in shape_elem.iter():
                if child != shape_elem:
                    # 对于 use 节点，如果是嵌套在 g 里的，保留其内部相对于原点的变换（如果有必要）
                    # 但在我们的归一化模型中，通常应该清理掉
                    if _local_tag(child.tag) in ("use", "rect", "circle", "line"):
                        if "transform" in child.attrib: del child.attrib["transform"]

            g_outer.append(shape_elem)
        else:
            # 如果没有原始元素，则根据 IR 创建新元素
            g_inner = ET.SubElement(g_outer, f"{{{SVG_NS}}}g")
            
            if elem.shape_tag == "polygon":
                shape = ET.SubElement(g_inner, f"{{{SVG_NS}}}polygon")
                if elem.points:
                    pts_str = " ".join(f"{px:.4f},{py:.4f}" for px, py in elem.points)
                    shape.set("points", pts_str)
                else:
                    x1, y1 = 0, 0
                    x2, y2 = elem.width, elem.height
                    shape.set("points", f"{x1:.4f},{y1:.4f} {x2:.4f},{y1:.4f} {x2:.4f},{y2:.4f} {x1:.4f},{y2:.4f}")
                if elem.css_class: shape.set("class", elem.css_class)
            else:
                shape = ET.SubElement(g_inner, f"{{{SVG_NS}}}use")
                href = elem.symbol_href or self._default_symbol_href.get(elem.layer_name, "")
                shape.set(f"{{{XLINK_NS}}}href", href)
                shape.set("x", self._fmt(elem.x))
                shape.set("y", self._fmt(elem.y))
                shape.set("width", self._fmt(elem.width or 20.0))
                shape.set("height", self._fmt(elem.height or 10.0))
                if elem.transform: shape.set("transform", elem.transform)

    def _write_connection(self, layer: ET.Element, conn: SvgConnection):
        g_elem = ET.SubElement(layer, f"{{{SVG_NS}}}g")
        g_elem.set("id", _new_g_id("TMP"))
        polyline = ET.SubElement(g_elem, f"{{{SVG_NS}}}polyline")
        points_str = " ".join(f"{x:.4f},{y:.4f}" for x, y in conn.points)
        polyline.set("points", points_str)
        polyline.set("fill", conn.fill or "none")
        polyline.set("stroke", conn.stroke or "")
        if conn.stroke_width:
            polyline.set("stroke-width", self._fmt(float(conn.stroke_width)))
        polyline.set("stroke-linecap", conn.stroke_linecap or "round")
        polyline.set("stroke-linejoin", conn.stroke_linejoin or "round")
        if conn.stroke_dasharray:
            polyline.set("stroke-dasharray", conn.stroke_dasharray)
        if conn.css_class:
            polyline.set("class", conn.css_class)
        self._write_connection_metadata(g_elem, conn)

    def _write_text(self, layer: ET.Element, txt: SvgText):
        if getattr(txt, "hidden", False):
            return

        if txt.raw_element is not None:
            g_elem = copy.deepcopy(txt.raw_element)
            g_elem.set("id", txt.text_id or g_elem.get("id", ""))
            text_nodes = [c for c in g_elem if _local_tag(c.tag) == "text"]
            if text_nodes:
                text_elem = text_nodes[0]
                text_elem.set("x", self._fmt(txt.x))
                text_elem.set("y", self._fmt(txt.y))
                text_elem.set("font-size", self._fmt(txt.font_size))
                if txt.fill: text_elem.set("fill", txt.fill)
                if txt.font_weight: text_elem.set("font-weight", txt.font_weight)
                text_elem.set("dx", self._fmt(txt.dx))
                text_elem.set("dy", self._fmt(txt.dy))
                text_elem.set("text-anchor", txt.text_anchor)
                text_elem.set("dominant-baseline", txt.dominant_baseline)
                text_elem.text = txt.content

            for child in list(g_elem):
                if _local_tag(child.tag) == "metadata":
                    g_elem.remove(child)
            layer.append(g_elem)
            self._write_text_metadata(g_elem, txt)
        else:
            g_elem = ET.SubElement(layer, f"{{{SVG_NS}}}g")
            g_elem.set("id", txt.text_id or _new_g_id("TXT-TMP"))
            text_elem = ET.SubElement(g_elem, f"{{{SVG_NS}}}text")
            text_elem.set("x", self._fmt(txt.x))
            text_elem.set("y", self._fmt(txt.y))
            text_elem.set("fill", txt.fill if txt.fill else "#262626")
            text_elem.set("font-size", self._fmt(txt.font_size))
            text_elem.set("dx", self._fmt(txt.dx))
            text_elem.set("dy", self._fmt(txt.dy))
            text_elem.set("text-anchor", txt.text_anchor)
            text_elem.set("dominant-baseline", txt.dominant_baseline)
            text_elem.text = txt.content
            self._write_text_metadata(g_elem, txt)

    def _write_background(self, root: ET.Element):
        bg_layer = root.find(f".//{{{SVG_NS}}}g[@id='BackGround_Layer']")
        if bg_layer is None:
            bg_layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
            bg_layer.set("id", "BackGround_Layer")
        rect = ET.SubElement(bg_layer, f"{{{SVG_NS}}}rect")
        vb = self.doc.viewbox
        rect.set("x", self._fmt(vb[0]))
        rect.set("y", self._fmt(vb[1]))
        rect.set("width", self._fmt(vb[2]))
        rect.set("height", self._fmt(vb[3]))
        rect.set("fill", "#FFFFFF")

    def _write_beautified_style(self, root: ET.Element):
        style_elem = root.find(f".//{{{SVG_NS}}}style")
        if style_elem is None:
            defs = root.find(f".//{{{SVG_NS}}}defs") or ET.SubElement(root, f"{{{SVG_NS}}}defs")
            style_elem = ET.SubElement(defs, f"{{{SVG_NS}}}style")
            style_elem.set("type", "text/css")

        new_rules = ["symbol{overflow:visible}"]
        
        # P0-4b: 严格遵循制图规范 v1 色值与线宽
        voltage_colors = {
            "lkv10": "#FF0000",   # 10kV 红色
            "lkv35": "#00C8FF",   # 35kV 天蓝色
            "lkv66": "#FFCC00",   # 66kV 黄色
            "lkv110": "#F04155",  # 110kV 朱红色
            "lkv220": "#800080"   # 220kV 紫色
        }
        for cls, color in voltage_colors.items():
            # 严格遵循规范值：主干线 3px, 支线 1.5px, 母线 5px
            new_rules.append(f".{cls} {{ fill:none; stroke:{color}; stroke-width:3.0; }}")
            new_rules.append(f".{cls}_branch {{ fill:none; stroke:{color}; stroke-width:1.5; }}")
            new_rules.append(f".{cls}_busbar {{ fill:none; stroke:{color}; stroke-width:5.0; }}")
        
        # 站房边框 2px
        new_rules.append(".Substation { fill: #FFFBE6; stroke: #873800; stroke-width: 2.0; }")
        # 连接线 1.5px
        new_rules.append(".ConnLine { fill: none; stroke: #595959; stroke-width: 1.5; }")
        
        # 强制所有标注样式
        new_rules.append("text { font-family: 'Microsoft YaHei', sans-serif; }")
        
        style_elem.text = "\n".join(new_rules)

    def _write_element_metadata(self, g_elem: ET.Element, elem: SvgElement):
        metadata = ET.SubElement(g_elem, f"{{{SVG_NS}}}metadata")
        psr = ET.SubElement(metadata, f"{{{IEC_NS}}}PSR_Ref")
        psr.set("ObjectID", elem.element_id or "")
        if elem.element_name: psr.set("ObjectName", elem.element_name)
        if elem.psr_type: psr.set("PSRType", elem.psr_type)
        if elem.line_type: psr.set("LineType", elem.line_type)
        if elem.voltage_level: psr.set("VoltageLevel", elem.voltage_level)
        for ref in elem.glink_refs:
            ET.SubElement(metadata, f"{{{IEC_NS}}}GLink_Ref").set("ObjectID", ref)

    def _write_connection_metadata(self, g_elem: ET.Element, conn: SvgConnection):
        metadata = ET.SubElement(g_elem, f"{{{SVG_NS}}}metadata")
        psr = ET.SubElement(metadata, f"{{{IEC_NS}}}PSR_Ref")
        psr.set("ObjectID", conn.connection_id or "")
        if conn.connection_name: psr.set("ObjectName", conn.connection_name)
        for ref in conn.glink_refs:
            ET.SubElement(metadata, f"{{{IEC_NS}}}GLink_Ref").set("ObjectID", ref)

    def _write_text_metadata(self, g_elem: ET.Element, txt: SvgText):
        metadata = ET.SubElement(g_elem, f"{{{SVG_NS}}}metadata")
        psr = ET.SubElement(metadata, f"{{{IEC_NS}}}PSR_Ref")
        psr.set("ObjectID", txt.raw_object_id or "")
        if txt.object_name: psr.set("ObjectName", txt.object_name)

    def _infer_default_symbols(self):
        for elem in self.doc.elements:
            if elem.layer_name and elem.symbol_href:
                self._default_symbol_href[elem.layer_name] = elem.symbol_href

    @staticmethod
    def _fmt(value) -> str:
        if isinstance(value, float):
            return f"{value:.6f}".rstrip("0").rstrip(".")
        return str(value)


def write_svg(doc: SvgDocument, output_path: str, update_style: bool = False, beautifier=None) -> str:
    writer = SvgDocumentWriter(doc)
    return writer.write(output_path, update_style=update_style, beautifier=beautifier)
