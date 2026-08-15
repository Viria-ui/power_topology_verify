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
    def write(self, output_path: str, update_style: bool = False):
        """写回 SVG。

        Args:
            output_path: 输出文件路径
            update_style: 是否用规范样式覆盖 <defs> 中的 CSS（美化时使用）
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        # 基于原始树深拷贝，保留 <defs> 符号定义和根属性
        tree = copy.deepcopy(self.doc.tree)
        root = tree.getroot()

        # 清空内容图层
        all_layers = ["BackGround_Layer"] + DEVICE_LAYERS + ["ConnLine_Layer", "Text_Layer"]
        for layer_id in all_layers:
            layer = root.find(f".//{{{SVG_NS}}}g[@id='{layer_id}']")
            if layer is not None:
                for child in list(layer):
                    layer.remove(child)
            else:
                layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
                layer.set("id", layer_id)

        # 更新根属性：viewBox 与 width/height 同步，避免拉伸或黑边
        vb = self.doc.viewbox
        root.set("viewBox", f"{vb[0]:.6f} {vb[1]:.6f} {vb[2]:.6f} {vb[3]:.6f}")
        root.set("width", self._fmt(self.doc.width))
        root.set("height", self._fmt(self.doc.height))
        if self.doc.coordinate_extent:
            root.set("coordinateExtent", self.doc.coordinate_extent)

        # 背景
        self._write_background(root)

        # 设备按图层分组
        elements_by_layer = defaultdict(list)
        for elem in self.doc.elements:
            layer_id = f"{elem.layer_name}_Layer"
            elements_by_layer[layer_id].append(elem)

        # 写设备图层
        for layer_id in DEVICE_LAYERS:
            layer = root.find(f".//{{{SVG_NS}}}g[@id='{layer_id}']")
            if layer is None:
                continue
            for elem in elements_by_layer.get(layer_id, []):
                self._write_element(layer, elem)

        # 写连接线
        conn_layer = root.find(f".//{{{SVG_NS}}}g[@id='ConnLine_Layer']")
        if conn_layer is not None:
            for conn in self.doc.connections:
                self._write_connection(conn_layer, conn)

        # 写文字
        text_layer = root.find(f".//{{{SVG_NS}}}g[@id='Text_Layer']")
        if text_layer is not None:
            for txt in self.doc.texts:
                self._write_text(text_layer, txt)

        # 样式
        if update_style:
            self._write_beautified_style(root)

        # 注册命名空间，输出使用规范前缀
        try:
            ET.register_namespace("", SVG_NS)
        except ValueError:
            pass
        try:
            ET.register_namespace("xlink", XLINK_NS)
        except ValueError:
            pass
        try:
            ET.register_namespace("ns2", IEC_NS)
        except ValueError:
            pass

        ET.indent(tree, space="  ")
        tree.write(output_path, xml_declaration=True, encoding="UTF-8")
        return output_path

    # ------------------------------------------------------------------
    # 元素写入
    # ------------------------------------------------------------------
    def _write_element(self, layer: ET.Element, elem: SvgElement):
        """写回设备图元：克隆原始XML节点，只覆盖被修改的属性。

        结构级保真：未被明确修改的属性（如use的xlink:href、class、
        原始子节点结构等）原样保留，防止因属性重建导致图元变形。
        """
        if elem.raw_element is not None:
            # 克隆原始g元素（保留所有子节点、属性、class、transform等）
            g_elem = copy.deepcopy(elem.raw_element)
            g_elem.set("id", elem.element_id or elem.shape_attrs.get("id", ""))

            # 找到主要图形节点（use/rect/polygon等）
            shape_tag = elem.shape_tag
            shape_elem = None
            for child in g_elem:
                tag = _local_tag(child.tag)
                if tag in ("use", "rect", "polygon", "path", "circle", "line"):
                    shape_elem = child
                    break

            if shape_elem is not None:
                tag = _local_tag(shape_elem.tag)
                if tag == "use":
                    # x/y 属性控制位置，transform 仅保留 rotate（由 beautifier 设置）
                    # 始终使用 elem.transform，不回退到原始 transform（避免残留 scale/translate）
                    shape_elem.set("x", self._fmt(elem.x))
                    shape_elem.set("y", self._fmt(elem.y))
                    if elem.transform:
                        shape_elem.set("transform", elem.transform)
                    elif 'transform' in shape_elem.attrib:
                        del shape_elem.attrib['transform']
                    if elem.width:
                        shape_elem.set("width", self._fmt(elem.width))
                    if elem.height:
                        shape_elem.set("height", self._fmt(elem.height))
                    # 保留原始href和class，不覆盖
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
                # polygon/path: 更新points/d属性（如果shape_attrs已被修改）
                elif tag == "polygon":
                    points = elem.shape_attrs.get("points", "")
                    if points:
                        shape_elem.set("points", points)
                    # 如果shape_attrs中没有points，根据x/y/width/height重建
                    elif elem.width and elem.height:
                        x1, y1 = elem.x, elem.y
                        x2, y2 = elem.x + elem.width, elem.y + elem.height
                        reconstructed = (
                            f"{x1:.6f},{y1:.6f} {x1:.6f},{y2:.6f} "
                            f"{x2:.6f},{y2:.6f} {x2:.6f},{y1:.6f}"
                        )
                        shape_elem.set("points", reconstructed)
                elif tag == "path":
                    d = elem.shape_attrs.get("d", "")
                    if d:
                        shape_elem.set("d", d)

            # 清理原始metadata，重新写入
            for child in list(g_elem):
                if _local_tag(child.tag) == "metadata":
                    g_elem.remove(child)

            layer.append(g_elem)
            self._write_element_metadata(g_elem, elem)
        else:
            # 回退：原始没有raw_element（如新增设备），按原逻辑重建
            g_elem = ET.SubElement(layer, f"{{{SVG_NS}}}g")
            g_elem.set("id", elem.shape_attrs.get("id", _new_g_id("TMP")))

            if elem.shape_tag == "use":
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}use")
                href = elem.symbol_href or self._default_symbol_href.get(elem.layer_name, "")
                shape.set(f"{{{XLINK_NS}}}href", href)
                shape.set("x", self._fmt(elem.x))
                shape.set("y", self._fmt(elem.y))
                shape.set("width", self._fmt(elem.width or 8.1))
                shape.set("height", self._fmt(elem.height or 1.444))
                if elem.css_class:
                    shape.set("class", elem.css_class)
                # 新增设备：x/y 已直接定位，transform 仅保留已有内容
                if elem.transform:
                    shape.set("transform", elem.transform)
            elif elem.shape_tag == "rect":
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}rect")
                shape.set("x", self._fmt(elem.x))
                shape.set("y", self._fmt(elem.y))
                shape.set("width", self._fmt(elem.width))
                shape.set("height", self._fmt(elem.height))
                shape.set("fill", elem.fill if elem.fill else "none")
                shape.set("stroke", elem.stroke if elem.stroke else "none")
                if elem.stroke_width:
                    shape.set("stroke-width", self._fmt(float(elem.stroke_width)))
            elif elem.shape_tag == "polygon":
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}polygon")
                points = elem.shape_attrs.get("points", "")
                if points:
                    shape.set("points", points)
                shape.set("fill", elem.fill if elem.fill else "none")
                shape.set("stroke", elem.stroke if elem.stroke else "none")
                if elem.stroke_width:
                    shape.set("stroke-width", self._fmt(float(elem.stroke_width)))
            elif elem.shape_tag == "path":
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}path")
                if "d" in elem.shape_attrs:
                    shape.set("d", elem.shape_attrs["d"])
                shape.set("fill", elem.fill if elem.fill else "none")
                shape.set("stroke", elem.stroke if elem.stroke else "none")
                if elem.stroke_width:
                    shape.set("stroke-width", self._fmt(float(elem.stroke_width)))
            elif elem.shape_tag == "circle":
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}circle")
                r = (elem.width or 0) / 2
                shape.set("cx", self._fmt(elem.x + r))
                shape.set("cy", self._fmt(elem.y + r))
                shape.set("r", self._fmt(r))
            elif elem.shape_tag == "line":
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}line")
                shape.set("x1", self._fmt(elem.x))
                shape.set("y1", self._fmt(elem.y))
                shape.set("x2", self._fmt(elem.x + elem.width))
                shape.set("y2", self._fmt(elem.y + elem.height))
            else:
                shape = ET.SubElement(g_elem, f"{{{SVG_NS}}}use")
                href = elem.symbol_href or self._default_symbol_href.get(elem.layer_name, "")
                shape.set(f"{{{XLINK_NS}}}href", href)
                shape.set("x", self._fmt(elem.x))
                shape.set("y", self._fmt(elem.y))
                shape.set("width", self._fmt(elem.width or 8.1))
                shape.set("height", self._fmt(elem.height or 1.444))

            self._write_element_metadata(g_elem, elem)

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
        """写回文字：克隆原始XML节点，只覆盖被美化修改的属性。

        结构级保真：未被明确修改的属性（style/transform/letter-spacing等）
        原样保留，避免因属性级重建导致的布局崩坏。
        """
        # 被过滤隐藏的文字不再写入 SVG
        if getattr(txt, "hidden", False):
            return

        if txt.raw_element is not None:
            # 克隆原始g元素（保留所有子节点、属性、style等）
            g_elem = copy.deepcopy(txt.raw_element)
            g_elem.set("id", txt.text_id or g_elem.get("id", ""))

            # 找到第一个<text>节点，只覆盖被修改的属性
            text_nodes = []
            for child in g_elem:
                tag = _local_tag(child.tag)
                if tag == "text":
                    text_nodes.append(child)

            if text_nodes:
                text_elem = text_nodes[0]

                # 坐标：如果x/y被修改（美化可能移动文字）
                if abs(txt.x - float(text_elem.get("x", str(txt.x)))) > 0.001:
                    text_elem.set("x", self._fmt(txt.x))
                if abs(txt.y - float(text_elem.get("y", str(txt.y)))) > 0.001:
                    text_elem.set("y", self._fmt(txt.y))

                # 字号：如果被规范化修改
                orig_fs = float(text_elem.get("font-size", str(txt.font_size)))
                if abs(txt.font_size - orig_fs) > 0.001:
                    text_elem.set("font-size", self._fmt(txt.font_size))

                # 填充色
                if txt.fill and txt.fill != text_elem.get("fill", ""):
                    text_elem.set("fill", txt.fill)

                # 字重
                if txt.font_weight and txt.font_weight != text_elem.get("font-weight", ""):
                    text_elem.set("font-weight", txt.font_weight)

                # 定位属性（B.4规范）：始终写入
                text_elem.set("dx", self._fmt(txt.dx))
                text_elem.set("dy", self._fmt(txt.dy))
                text_elem.set("text-anchor", txt.text_anchor)
                text_elem.set("dominant-baseline", txt.dominant_baseline)
                text_elem.set("font-family", txt.font_family or "Microsoft YaHei, SimHei, sans-serif")

                # 文本内容
                text_elem.text = txt.content

            # 删除同 group 下除主 text 外的其他 text 节点（原始 SVG 中常见的
            # 双层/标记文字），避免画面脏叠。
            for child in list(g_elem):
                tag = _local_tag(child.tag)
                if tag == "text" and child is not text_elem:
                    g_elem.remove(child)

            # 清理原始metadata，重新写入（保持TXT_前缀保真）
            for child in list(g_elem):
                if _local_tag(child.tag) == "metadata":
                    g_elem.remove(child)

            layer.append(g_elem)
            self._write_text_metadata(g_elem, txt)
        else:
            # 回退：原始没有raw_element（如新增文字），按原逻辑重建
            g_elem = ET.SubElement(layer, f"{{{SVG_NS}}}g")
            g_elem.set("id", txt.text_id or _new_g_id("TXT-TMP"))

            text_elem = ET.SubElement(g_elem, f"{{{SVG_NS}}}text")
            text_elem.set("x", self._fmt(txt.x))
            text_elem.set("y", self._fmt(txt.y))
            text_elem.set("fill", txt.fill if txt.fill else "#262626")
            text_elem.set("font-family", txt.font_family if txt.font_family else "Microsoft YaHei, SimHei, sans-serif")
            text_elem.set("font-size", self._fmt(txt.font_size))
            text_elem.set("stroke", txt.stroke if txt.stroke else "none")
            if txt.font_weight and txt.font_weight != "normal":
                text_elem.set("font-weight", txt.font_weight)
            text_elem.set("dx", self._fmt(txt.dx))
            text_elem.set("dy", self._fmt(txt.dy))
            text_elem.set("text-anchor", txt.text_anchor)
            text_elem.set("dominant-baseline", txt.dominant_baseline)
            text_elem.set("style", f"text-anchor:{txt.text_anchor}")
            text_elem.text = txt.content

            self._write_text_metadata(g_elem, txt)

    # ------------------------------------------------------------------
    # 元数据
    # ------------------------------------------------------------------
    def _write_element_metadata(self, g_elem: ET.Element, elem: SvgElement):
        metadata = ET.SubElement(g_elem, f"{{{SVG_NS}}}metadata")

        psr_attrs = elem.raw_metadata.get("PSR_Ref", {})
        psr = ET.SubElement(metadata, f"{{{IEC_NS}}}PSR_Ref")
        psr.set("ObjectID", elem.element_id or psr_attrs.get("ObjectID", ""))
        if elem.element_name or psr_attrs.get("ObjectName"):
            psr.set("ObjectName", elem.element_name or psr_attrs.get("ObjectName", ""))
        if elem.psr_type or psr_attrs.get("PSRType"):
            psr.set("PSRType", elem.psr_type or psr_attrs.get("PSRType", ""))
        if elem.line_type or psr_attrs.get("LineType"):
            psr.set("LineType", elem.line_type or psr_attrs.get("LineType", ""))
        if elem.top_type or psr_attrs.get("TopType"):
            psr.set("TopType", elem.top_type or psr_attrs.get("TopType", "02"))
        if elem.business_type or psr_attrs.get("businessType"):
            psr.set("businessType", elem.business_type or psr_attrs.get("businessType", "3"))
        for k, v in psr_attrs.items():
            if k not in ("ObjectID", "ObjectName", "PSRType", "LineType", "TopType", "businessType") and v:
                psr.set(k, str(v))

        for ref in elem.glink_refs:
            glink = ET.SubElement(metadata, f"{{{IEC_NS}}}GLink_Ref")
            glink.set("ObjectID", ref)

        layer_attrs = elem.raw_metadata.get("Layer_Ref", {})
        if elem.layer_ref or layer_attrs.get("ObjectName"):
            layer_ref = ET.SubElement(metadata, f"{{{IEC_NS}}}Layer_Ref")
            layer_ref.set("ObjectName", elem.layer_ref or layer_attrs.get("ObjectName", ""))

    def _write_connection_metadata(self, g_elem: ET.Element, conn: SvgConnection):
        metadata = ET.SubElement(g_elem, f"{{{SVG_NS}}}metadata")

        psr_attrs = conn.raw_metadata.get("PSR_Ref", {})
        psr = ET.SubElement(metadata, f"{{{IEC_NS}}}PSR_Ref")
        psr.set("ObjectID", conn.connection_id or psr_attrs.get("ObjectID", ""))
        if conn.connection_name or psr_attrs.get("ObjectName"):
            psr.set("ObjectName", conn.connection_name or psr_attrs.get("ObjectName", ""))
        if conn.line_type or psr_attrs.get("LineType"):
            psr.set("LineType", conn.line_type or psr_attrs.get("LineType", "Trunk"))
        if conn.psr_type or psr_attrs.get("PSRType"):
            psr.set("PSRType", conn.psr_type or psr_attrs.get("PSRType", ""))
        if conn.top_type or psr_attrs.get("TopType"):
            psr.set("TopType", conn.top_type or psr_attrs.get("TopType", "02"))
        if conn.business_type or psr_attrs.get("businessType"):
            psr.set("businessType", conn.business_type or psr_attrs.get("businessType", "3"))
        for k, v in psr_attrs.items():
            if k not in ("ObjectID", "ObjectName", "LineType", "PSRType", "TopType", "businessType") and v:
                psr.set(k, str(v))

        for ref in conn.glink_refs:
            glink = ET.SubElement(metadata, f"{{{IEC_NS}}}GLink_Ref")
            glink.set("ObjectID", ref)

        layer_attrs = conn.raw_metadata.get("Layer_Ref", {})
        if conn.layer_ref or layer_attrs.get("ObjectName"):
            layer_ref = ET.SubElement(metadata, f"{{{IEC_NS}}}Layer_Ref")
            layer_ref.set("ObjectName", conn.layer_ref or layer_attrs.get("ObjectName", ""))

    def _write_text_metadata(self, g_elem: ET.Element, txt: SvgText):
        metadata = ET.SubElement(g_elem, f"{{{SVG_NS}}}metadata")

        psr_attrs = txt.raw_metadata.get("PSR_Ref", {})
        psr = ET.SubElement(metadata, f"{{{IEC_NS}}}PSR_Ref")
        # 使用raw_object_id保留TXT_前缀，确保Reader→Writer→Reader闭环一致
        obj_id = txt.raw_object_id or psr_attrs.get("ObjectID", "")
        psr.set("ObjectID", obj_id)
        if txt.object_name or psr_attrs.get("ObjectName"):
            psr.set("ObjectName", txt.object_name or psr_attrs.get("ObjectName", ""))
        if psr_attrs.get("PSRType"):
            psr.set("PSRType", psr_attrs.get("PSRType", ""))
        if psr_attrs.get("LineType"):
            psr.set("LineType", psr_attrs.get("LineType", "Trunk"))
        if psr_attrs.get("TopType"):
            psr.set("TopType", psr_attrs.get("TopType", "02"))
        if psr_attrs.get("businessType"):
            psr.set("businessType", psr_attrs.get("businessType", "3"))

        layer_attrs = txt.raw_metadata.get("Layer_Ref", {})
        if txt.layer_ref or layer_attrs.get("ObjectName"):
            layer_ref = ET.SubElement(metadata, f"{{{IEC_NS}}}Layer_Ref")
            layer_ref.set("ObjectName", txt.layer_ref or layer_attrs.get("ObjectName", ""))

    # ------------------------------------------------------------------
    # 背景与样式
    # ------------------------------------------------------------------
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
        """生成规范化 CSS（美化模式）"""
        style_elem = root.find(f".//{{{SVG_NS}}}style")
        if style_elem is None:
            defs = root.find(f".//{{{SVG_NS}}}defs")
            if defs is None:
                defs = ET.SubElement(root, f"{{{SVG_NS}}}defs")
                root.insert(0, defs)
            style_elem = ET.SubElement(defs, f"{{{SVG_NS}}}style")
            style_elem.set("type", "text/css")

        new_rules = ["symbol{overflow:visible}"]

        voltage_class_map = {
            "lkv1000": "#00A854", "lkv750": "#00A854", "lkv500": "#00A854",
            "lkv330": "#00A854", "lkv220": "#00A854", "lkv110": "#00A854",
            "lkv66": "#00A854", "lkv35": "#00A854", "lkv20": "#00A854",
            "lkv15.75": "#00A854", "lkv13.8": "#00A854",
            "lkv10": "#00A854", "lkv6": "#00A854", "lkv3": "#00A854",
            "lv380": "#FF6A00", "lv220": "#FF6A00", "lv110": "#FF6A00",
            "lvdc": "#FF6A00",
        }
        widths = {
            "lkv1000": 3.0, "lkv750": 3.0, "lkv500": 3.0, "lkv330": 3.0,
            "lkv220": 3.0, "lkv110": 3.0, "lkv66": 3.0, "lkv35": 3.0,
            "lkv20": 3.0, "lkv15.75": 3.0, "lkv13.8": 3.0, "lkv10": 3.0,
            "lkv6": 1.5, "lkv3": 1.5, "lv380": 1.5, "lv220": 1.5,
            "lv110": 1.5, "lvdc": 1.5,
        }
        for cls, color in voltage_class_map.items():
            dev_cls = cls[1:] if cls.startswith("l") else cls
            w = widths.get(cls, 1.5)
            new_rules.append(f".{cls} {{fill:none;stroke:{color};stroke-width:{w:.6f}}}")
            new_rules.append(f".{dev_cls} {{fill:{color};stroke:{color};stroke-width:{w:.6f}}}")

        style_elem.text = "\n".join(new_rules)

    # ------------------------------------------------------------------
    # 辅助
    # ------------------------------------------------------------------
    def _infer_default_symbols(self):
        """从已有图元推断每类设备的默认符号 href。"""
        for elem in self.doc.elements:
            if elem.layer_name and elem.symbol_href:
                self._default_symbol_href[elem.layer_name] = elem.symbol_href

    @staticmethod
    def _fmt(value) -> str:
        if isinstance(value, float):
            return f"{value:.6f}".rstrip("0").rstrip(".")
        return str(value)


def write_svg(doc: SvgDocument, output_path: str, update_style: bool = False) -> str:
    writer = SvgDocumentWriter(doc)
    return writer.write(output_path, update_style=update_style)
