"""SVG编辑模块 - 基于 SvgDocument 中间模型进行设备新增和删除。

闭环流程：
    原始 SVG -> SvgDocument.parse() -> 中间模型
    中间模型 -> 修改（新增/删除） -> SvgDocumentWriter.write() -> 新 SVG
    新 SVG -> SvgDocument.parse() -> 验证中间模型

测试任务:
1. LINE215: 在开关00104和00102之间插入站房000300，含3个负荷开关
2. LINE216: 删除开关00024，两侧设备直接连接
"""
import os

from data_io.svg_reader import SvgDocument, SvgElement, SvgConnection, SvgText
from data_io.svg_writer import write_svg


class SvgEditor:
    """基于中间模型的 SVG 编辑器。"""

    def __init__(self, svg_path: str):
        self.svg_path = svg_path
        self.svg_filename = os.path.basename(svg_path)
        self.doc = SvgDocument(svg_path)

    # ------------------------------------------------------------------
    # 加载
    # ------------------------------------------------------------------
    def load(self):
        ok = self.doc.parse()
        if not ok:
            raise RuntimeError(f"SVG 解析失败: {self.svg_path}")
        return self

    # ------------------------------------------------------------------
    # 新增站房 + 开关
    # ------------------------------------------------------------------
    def add_station_with_switches(self, upstream_switch_id: str, downstream_switch_id: str,
                                   station_id: str, switch_ids: list[str],
                                   output_path: str = None) -> str:
        """在两个开关之间插入新站房和负荷开关。"""
        print(f"\n插入站房 {station_id}，包含 {len(switch_ids)} 个开关")
        print(f"  上游开关: {upstream_switch_id}")
        print(f"  下游开关: {downstream_switch_id}")

        up = self.doc.get_device_by_id(upstream_switch_id)
        down = self.doc.get_device_by_id(downstream_switch_id)
        if up is None or down is None:
            print("  找不到指定的开关设备")
            return self.svg_path

        up_x, up_y = up.x, up.y
        down_x, down_y = down.x, down.y
        mid_x = (up_x + down_x) / 2
        mid_y = (up_y + down_y) / 2
        gap = abs(down_x - up_x)

        # 站房尺寸（基于模型坐标空间）
        station_w = min(7.0, max(gap - 1.5, 4.0))
        station_h = 4.0
        station_x = mid_x - station_w / 2
        station_y = mid_y - station_h / 2

        # 创建站房
        station = self._make_station(station_id, station_x, station_y, station_w, station_h)
        self.doc.add_element(station)

        # 创建开关（垂直排布）
        spacing = station_w / (len(switch_ids) + 1)
        switches = []
        for i, sw_id in enumerate(switch_ids):
            sw_x = station_x + spacing * (i + 1)
            if i == 0 or i == len(switch_ids) - 1:
                sw_y = mid_y
            else:
                sw_y = mid_y + 1.5
            sw = self._make_switch(sw_id, sw_x, sw_y)
            switches.append(sw)
            self.doc.add_element(sw)
            # 文字标注
            txt = self._make_text(f"TXT-TMP{sw_id}", sw_id, sw_x, sw_y + 1.0)
            self.doc.add_text(txt)

        # 创建连接：上游 -> 首开关 -> 末开关 -> 下游
        # 中间开关作为备用间隔，从首开关引出死端分支
        first, last = switches[0], switches[-1]
        conns = [
            (upstream_switch_id, first.element_id),
            (first.element_id, last.element_id),
            (last.element_id, downstream_switch_id),
        ]
        for mid in switches[1:-1]:
            conns.append((first.element_id, mid.element_id))

        for a_id, b_id in conns:
            dev_a = self.doc.get_device_by_id(a_id)
            dev_b = self.doc.get_device_by_id(b_id)
            if dev_a and dev_b:
                conn = self._make_connection(a_id, b_id)
                self.doc.add_connection(conn)

        output_path = output_path or self.svg_path.replace(".svg", f"_with_{station_id}.svg")
        write_svg(self.doc, output_path)
        print(f"  站房插入完成: {output_path}")
        return output_path

    # ------------------------------------------------------------------
    # 删除开关
    # ------------------------------------------------------------------
    def delete_switch(self, switch_id: str, output_path: str = None) -> str:
        """删除指定开关，并将两侧设备直接连接，同时清理拓扑残留。"""
        print(f"\n删除开关 {switch_id}")
        sw = self.doc.get_device_by_id(switch_id)
        if sw is None:
            print("  找不到指定的开关设备")
            return self.svg_path

        # 所有与该开关相连的 GLink_Ref
        related_conns = self.doc.get_connections_for_device(switch_id)
        connected_ids = set()
        for conn in related_conns:
            for ref in conn.glink_refs:
                if ref and ref != switch_id and self.doc.get_device_by_id(ref):
                    connected_ids.add(ref)

        # 两侧设备直接连接：优先选择距离开关最近的两个设备
        if len(connected_ids) >= 2:
            def dist_to_switch(other_id: str) -> float:
                other = self.doc.get_device_by_id(other_id)
                if other is None:
                    return float("inf")
                return ((other.x - sw.x) ** 2 + (other.y - sw.y) ** 2) ** 0.5

            sorted_ids = sorted(connected_ids, key=dist_to_switch)
            # 优先选择同图层开关类设备
            preferred = [oid for oid in sorted_ids
                         if (dev := self.doc.get_device_by_id(oid))
                         and dev.layer_name in ("Breaker", "LoadBreakSwitch")]
            if len(preferred) >= 2:
                dev_list = preferred[:2]
            else:
                dev_list = sorted_ids[:2]
            conn = self._make_connection(dev_list[0], dev_list[1])
            self.doc.add_connection(conn)
            print(f"  已创建新连接: {dev_list[0]} <-> {dev_list[1]}")

        # 删除与该开关相关的所有连接
        for conn in related_conns:
            self.doc.remove_connection(conn)
            print(f"  已删除连接: {conn.connection_id}")

        # 删除开关设备
        self.doc.remove_element(switch_id)
        print(f"  已删除开关: {switch_id}")

        # 删除相关文字标注
        to_remove = []
        for txt in self.doc.texts:
            if txt.object_id == switch_id or txt.object_id == f"TXT_{switch_id}" or txt.object_id == f"TXT-TMP{switch_id}":
                to_remove.append(txt)
            elif txt.content and switch_id.replace("TMP", "") in txt.content:
                to_remove.append(txt)
        for txt in to_remove:
            self.doc.remove_text(txt)
            print(f"  已删除文字: {txt.text_id}")

        # 清理其他元素/连接元数据中指向已删设备的悬空 GLink_Ref
        removed = 0
        for elem in self.doc.elements:
            if switch_id in elem.glink_refs:
                elem.glink_refs.remove(switch_id)
                removed += 1
        for conn in self.doc.connections:
            if switch_id in conn.glink_refs:
                conn.glink_refs.remove(switch_id)
                removed += 1
        if removed:
            print(f"  已清理残留 GLink_Ref 引用: {removed} 处")

        output_path = output_path or self.svg_path.replace(".svg", f"_del_{switch_id}.svg")
        write_svg(self.doc, output_path)
        print(f"  开关删除完成: {output_path}")
        return output_path

    # ------------------------------------------------------------------
    # 模型构造辅助
    # ------------------------------------------------------------------
    def _make_station(self, station_id: str, x: float, y: float, w: float, h: float) -> SvgElement:
        elem = SvgElement()
        elem.layer_name = "Substation"
        elem.element_type = "站房"
        elem.element_id = f"TMP{station_id}"
        elem.element_name = f"站房{station_id}"
        elem.psr_type = "zf08"
        elem.line_type = "Trunk"
        elem.top_type = "02"
        elem.business_type = "3"
        elem.x, elem.y, elem.width, elem.height = x, y, w, h
        elem.shape_tag = "rect"
        elem.fill = "none"
        elem.stroke = "#595959"
        elem.stroke_width = "1.5"
        elem.layer_ref = f"TMP_STATION_{station_id}"
        elem.raw_metadata = {
            "PSR_Ref": {
                "ObjectID": elem.element_id,
                "ObjectName": elem.element_name,
                "PSRType": elem.psr_type,
                "LineType": elem.line_type,
                "TopType": elem.top_type,
                "businessType": elem.business_type,
            },
            "Layer_Ref": {"ObjectName": elem.layer_ref},
        }
        return elem

    def _make_switch(self, switch_id: str, x: float, y: float) -> SvgElement:
        elem = SvgElement()
        elem.layer_name = "LoadBreakSwitch"
        elem.element_type = "负荷开关"
        elem.element_id = f"TMP{switch_id}"
        elem.element_name = f"开关{switch_id}"
        elem.psr_type = "0307"
        elem.line_type = "Trunk"
        elem.top_type = "02"
        elem.business_type = "3"
        elem.x, elem.y = x, y
        elem.width = 8.1
        elem.height = 1.444
        elem.shape_tag = "use"
        elem.symbol_href = self._get_default_symbol_href("LoadBreakSwitch")
        elem.css_class = "lkv10"
        elem.voltage_level = "10kV"
        # 垂直放置（270度旋转）
        elem.rotation = 270.0
        elem.transform = f"rotate(270.0,{x:.4f},{y:.4f}) translate({x:.4f},{y:.4f}) scale(1.0,1.0) translate(-{x:.4f},-{y:.4f})"
        elem.layer_ref = f"TMP_SWITCH_{switch_id}"
        elem.raw_metadata = {
            "PSR_Ref": {
                "ObjectID": elem.element_id,
                "ObjectName": elem.element_name,
                "PSRType": elem.psr_type,
                "LineType": elem.line_type,
                "TopType": elem.top_type,
                "businessType": elem.business_type,
            },
            "Layer_Ref": {"ObjectName": elem.layer_ref},
        }
        return elem

    def _make_text(self, text_id: str, content: str, x: float, y: float) -> SvgText:
        txt = SvgText()
        txt.text_id = text_id
        txt.object_id = f"TXT{content}"
        txt.object_name = content
        txt.content = content
        txt.x, txt.y = x, y
        txt.font_size = 11.0
        txt.fill = "#262626"
        txt.font_family = "Microsoft YaHei, SimHei, sans-serif"
        txt.style = "text-anchor:middle"
        txt.font_weight = "normal"
        txt.layer_ref = f"TMP_TEXT_{text_id}"
        txt.raw_metadata = {
            "PSR_Ref": {
                "ObjectID": txt.object_id,
                "ObjectName": content,
                "PSRType": "-1",
                "LineType": "Trunk",
                "TopType": "02",
                "businessType": "3",
            },
            "Layer_Ref": {"ObjectName": txt.layer_ref},
        }
        return txt

    def _make_connection(self, a_id: str, b_id: str) -> SvgConnection:
        dev_a = self.doc.get_device_by_id(a_id)
        dev_b = self.doc.get_device_by_id(b_id)
        conn = SvgConnection()
        conn.connection_id = f"TMP_CONN_{a_id}_{b_id}"
        conn.points = [(dev_a.x, dev_a.y), (dev_b.x, dev_b.y)]
        conn.glink_refs = [a_id, b_id]
        conn.line_type = "Trunk"
        conn.psr_type = "13TMP00132954"
        conn.top_type = "02"
        conn.business_type = "3"
        conn.css_class = "lkv10"
        conn.stroke = "#00A854"
        conn.stroke_width = "3.0"
        conn.voltage_level = "10kV"
        conn.layer_ref = f"TMP_CONN_{a_id}_{b_id}"
        conn.raw_metadata = {
            "PSR_Ref": {
                "ObjectID": conn.connection_id,
                "LineType": conn.line_type,
                "PSRType": conn.psr_type,
                "TopType": conn.top_type,
                "businessType": conn.business_type,
            },
            "Layer_Ref": {"ObjectName": conn.layer_ref},
        }
        return conn

    def _get_default_symbol_href(self, layer_name: str) -> str:
        for elem in self.doc.elements:
            if elem.layer_name == layer_name and elem.symbol_href:
                return elem.symbol_href
        return ""


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    svg_dir = os.path.join(project_root, "output", "svg")
    src_dir = os.path.join(project_root, "数据集更新版20260729", "配网 svg")
    os.makedirs(svg_dir, exist_ok=True)

    # LINE215：新增站房
    line215_path = os.path.join(svg_dir, "LINE215_beautified.svg")
    if not os.path.exists(line215_path):
        line215_path = os.path.join(src_dir, "LINE215.svg")
    editor = SvgEditor(line215_path)
    editor.load()
    editor.add_station_with_switches(
        upstream_switch_id="TMP00044018",
        downstream_switch_id="TMP00044016",
        station_id="000300",
        switch_ids=["00301", "00302", "00303"],
    )

    # LINE216：删除开关
    line216_path = os.path.join(svg_dir, "LINE216_beautified.svg")
    if not os.path.exists(line216_path):
        line216_path = os.path.join(src_dir, "LINE216.svg")
    editor2 = SvgEditor(line216_path)
    editor2.load()
    editor2.delete_switch("TMP00043912")


if __name__ == "__main__":
    main()
