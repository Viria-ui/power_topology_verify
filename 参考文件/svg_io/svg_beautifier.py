"""SVG美化模块 - 按《SVG制图规范 v1》完整落地。

修复清单（对比原规范）：
  ✅ B.2 色值规范化
  ✅ B.3 线宽/线型规范
  ✅ B.4 字号分级（标题/关键设备/支线/线路/ID）
  ✅ B.4 文字位置（dx/dy/text-anchor/dominant-baseline）
  ✅ B.1 10px 网格吸附（设备与连接线端点同步）
  ✅ 白色背景 #FFFFFF
  ✅ 电源追溯路径 #1890FF
  ✅ 联络线橙色 / 跨站联络紫色
  ✅ 备用间隔灰色+虚线
  ✅ 站房边框规范化
"""
import os
import re

from data_io.svg_reader import SvgDocument, SvgElement, SvgConnection, SvgText
from data_io.svg_writer import write_svg


# ------------------------------------------------------------------
# B.2 精准色值映射表
# ------------------------------------------------------------------
STYLE = {
    "background": "#FFFFFF",
    "text": "#262626",
    "station_border": "#595959",
    "main_feeder": "#00A854",
    "tie_line": "#FF6A00",
    "cross_station_tie": "#722ED1",
    "spare_interval": "#BFBFBF",
    "trace_path": "#1890FF",
}

# ------------------------------------------------------------------
# B.3 线宽 (px) 与线型规范
# ------------------------------------------------------------------
LINE_WIDTHS = {
    "main_feeder": 3.0,
    "branch": 1.5,
    "tie_line": 4.5,
    "spare_interval": 1.0,
    "station_border": 2.0,
}

VOLTAGE_CLASS_MAP = {
    "lkv1000": "#00A854", "lkv750": "#00A854", "lkv500": "#00A854",
    "lkv330": "#00A854", "lkv220": "#00A854", "lkv110": "#00A854",
    "lkv66": "#00A854", "lkv35": "#00A854", "lkv20": "#00A854",
    "lkv15.75": "#00A854", "lkv13.8": "#00A854",
    "lkv10": "#00A854", "lkv6": "#00A854", "lkv3": "#00A854",
    "lv380": "#FF6A00", "lv220": "#FF6A00", "lv110": "#FF6A00",
    "lvdc": "#FF6A00",
}

VOLTAGE_CLASS_WIDTHS = {
    "lkv1000": 3.0, "lkv750": 3.0, "lkv500": 3.0, "lkv330": 3.0,
    "lkv220": 3.0, "lkv110": 3.0, "lkv66": 3.0, "lkv35": 3.0,
    "lkv20": 3.0, "lkv15.75": 3.0, "lkv13.8": 3.0, "lkv10": 3.0,
    "lkv6": 1.5, "lkv3": 1.5, "lv380": 1.5, "lv220": 1.5,
    "lv110": 1.5, "lvdc": 1.5,
}

# ------------------------------------------------------------------
# B.4 字体字号 (px) 与字重
# ------------------------------------------------------------------
FONTS = {
    "title": 21.3,          # 图纸标题/站房名 16pt bold
    "key_device": 14.0,     # 关键一次设备 10.5pt bold
    "branch_device": 12.0,  # 支线设备/备用 9pt normal
    "line_label": 12.0,     # 线路名称/编号 9pt normal
    "device_id": 10.0,      # 设备唯一ID 7.5pt normal
}

# 关键一次设备图层（字号14, bold）
KEY_DEVICE_LAYERS = {"PowerTransformer", "Breaker", "BusbarSection"}

# 支线设备图层（字号12, normal）
BRANCH_DEVICE_LAYERS = {
    "LoadBreakSwitch", "Fuse", "Disconnector", "GroundDisconnector",
    "CompositeSwitch", "CurrentTransformer", "PotentialTransformer",
    "Junction", "EnergyConsumer", "Other", "RemoteUnit", "PoleCode",
}

# 设备标准显示尺寸（px）：解决原始 symbol 极小导致文字/线宽尺度倒置的问题
DEVICE_STANDARD_SIZES = {
    "PowerTransformer": (28.0, 20.0),
    "Breaker": (24.0, 12.0),
    "BusbarSection": (32.0, 6.0),
    "LoadBreakSwitch": (20.0, 10.0),
    "Disconnector": (20.0, 10.0),
    "GroundDisconnector": (20.0, 10.0),
    "Fuse": (16.0, 8.0),
    "CompositeSwitch": (20.0, 10.0),
    "CurrentTransformer": (16.0, 12.0),
    "PotentialTransformer": (16.0, 12.0),
    "Junction": (8.0, 8.0),
    "EnergyConsumer": (20.0, 12.0),
    "RemoteUnit": (16.0, 10.0),
    "PoleCode": (16.0, 10.0),
    "Other": (16.0, 10.0),
}

# ------------------------------------------------------------------
# B.1 网格吸附
# ------------------------------------------------------------------
GRID_SIZE = 10.0

# SVG 坐标系统说明：
#   viewBox = 1124 × 795 (SVG 用户单位)
#   设备宽度 ≈ 8.1 单位，设备间距 ≈ 2.0 单位
#
# 规范 B.4 固定字号（px）与字重：
#   图纸标题/站房名  21.3 px  bold
#   关键一次设备名  14.0 px  bold
#   支线设备/备用名  12.0 px  normal
#   线路名称/编号   12.0 px  normal
#   设备唯一 ID    10.0 px  normal
#
# 规范 B.4 固定偏移（px）：
#   关键一次设备名：dx=0,  dy=18,  text-anchor=middle, dominant-baseline=hanging
#   支线设备/备用名：dx=14, dy=4,   text-anchor=start,  dominant-baseline=middle
#   线路名称/编号： dx=0,  dy=-6,  text-anchor=middle, dominant-baseline=auto
#   设备唯一 ID：   dx=0,  dy=30,  text-anchor=middle, dominant-baseline=hanging
#   图纸标题/站房名：dx=0,  dy=-18, text-anchor=middle, dominant-baseline=auto


class SvgBeautifier:
    """基于中间模型的 SVG 美化器（按规范 v1 完整落地）。"""

    def __init__(self, svg_path: str, output_path: str = None):
        self.svg_path = svg_path
        self.svg_filename = os.path.basename(svg_path)
        self.output_path = output_path or svg_path.replace(".svg", "_beautified.svg")
        self.doc = SvgDocument(svg_path)
        self.spare_device_ids: set[str] = set()
        self.device_to_station: dict[str, str] = {}
        self.text_device_map: dict[str, str] = {}  # text_id → device_id

    def beautify(self) -> str:
        print(f"\n{'='*60}")
        print(f"美化 {self.svg_filename}")
        print(f"{'='*60}")

        self.doc.parse()

        # 第1步：建立站房映射 + 识别备用间隔（基于原始坐标）
        self._build_station_map()
        self._detect_spare_intervals()

        # 第2步：网格吸附 + transform同步 + 连接线端点同步
        self._snap_to_grid()

        # 第3步：站房内布局重构（暂不执行）
        # self._rearrange_station_devices()

        # 第4步：连接线样式规范化
        self._normalize_connection_styles()

        # 第5步：站房边框 + 设备图标标准化
        self._normalize_station_styles()
        self._normalize_device_icons()

        # 第6步：坐标空间缩放，让密集布局舒展
        self._scale_coordinate_space(factor=3.5)

        # 第7步：连接线端点路由到设备边缘，避免线穿过设备
        self._route_connections_to_edges()

        # 第8步：文字样式/位置规范化（基于缩放后的设备坐标）
        self._normalize_text_styles()
        self._resolve_text_collisions()

        # 第9步（最后处理）：自适应viewbox包裹缩放后内容
        self._adapt_viewbox()

        # 第7步：写出 SVG（含白色背景）
        write_svg(self.doc, self.output_path, update_style=True)

        # 第8步：自检并输出质量报告
        self._check_beautify_quality()

        print(f"\n美化完成: {self.output_path}")
        return self.output_path

    # ------------------------------------------------------------------
    # B.1 画布视区（最后处理，viewBox/width/height 同步）
    # ------------------------------------------------------------------
    def _adapt_viewbox(self):
        """根据缩放后的实际内容计算 viewBox，四周留边距，width/height 同步。"""
        old_vb = self.doc.viewbox
        margin = 48.0

        # 使用文档自带的自适应计算，基于当前（已缩放）内容求包围盒
        new_vb = self.doc.compute_adaptive_viewbox(margin=margin)

        self.doc.viewbox = new_vb
        self.doc.width = new_vb[2]
        self.doc.height = new_vb[3]
        print(f"  viewBox 已适配: ({old_vb[0]:.2f},{old_vb[1]:.2f} {old_vb[2]:.2f}x{old_vb[3]:.2f}) "
              f"-> ({new_vb[0]:.2f},{new_vb[1]:.2f} {new_vb[2]:.2f}x{new_vb[3]:.2f})")

    def _check_beautify_quality(self):
        """输出美化质量自检报告：文字重叠、越界、隐藏比例等。"""
        vb = self.doc.viewbox
        vb_x, vb_y, vb_w, vb_h = vb

        # 文字
        visible_texts = [t for t in self.doc.texts if not getattr(t, "hidden", False)]
        hidden_texts = [t for t in self.doc.texts if getattr(t, "hidden", False)]
        text_overlap = 0
        text_outside = 0
        bboxes = []
        for txt in visible_texts:
            bx, by, bw, bh = self._text_bbox(txt)
            bboxes.append((bx, by, bw, bh))
            if bx + bw < vb_x or bx > vb_x + vb_w or by + bh < vb_y or by > vb_y + vb_h:
                text_outside += 1
        for i in range(len(bboxes)):
            for j in range(i + 1, len(bboxes)):
                x1, y1, w1, h1 = bboxes[i]
                x2, y2, w2, h2 = bboxes[j]
                if self._bbox_overlap(x1, y1, w1, h1, x2, y2, w2, h2, buffer=0):
                    text_overlap += 1
                    break

        # 设备
        dev_outside = 0
        for elem in self.doc.elements:
            ex, ey = elem.x, elem.y
            ew, eh = elem.width or 0, elem.height or 0
            if ex + ew < vb_x or ex > vb_x + vb_w or ey + eh < vb_y or ey > vb_y + vb_h:
                dev_outside += 1

        # 连接线端点
        conn_outside = 0
        for conn in self.doc.connections:
            if not conn.points:
                continue
            for px, py in conn.points[:1] + conn.points[-1:]:
                if px < vb_x or px > vb_x + vb_w or py < vb_y or py > vb_y + vb_h:
                    conn_outside += 1
                    break

        total = len(self.doc.texts)
        print(f"\n  === 美化质量自检 ===")
        print(f"  文字总数: {total}, 可见: {len(visible_texts)}, 隐藏: {len(hidden_texts)} "
              f"({len(hidden_texts)/total*100:.1f}%)")
        print(f"  文字重叠: {text_overlap} 对 ({text_overlap/len(visible_texts)*100:.1f}%)  "
              f"越界: {text_outside} 个")
        print(f"  设备越界: {dev_outside} 个, 连接线端点越界: {conn_outside} 条")

    # ------------------------------------------------------------------
    # 站房映射（用于跨站联络识别）
    # ------------------------------------------------------------------
    def _build_station_map(self):
        """构建 device_id -> station_id 映射。"""
        station_bounds = []
        for elem in self.doc.elements:
            if elem.layer_name == "Substation" and elem.element_id:
                station_bounds.append((
                    elem.element_id,
                    elem.x, elem.y, elem.width, elem.height,
                ))

        self.device_to_station = {}
        for elem in self.doc.elements:
            if elem.layer_name == "Substation" or not elem.element_id:
                continue
            for sid, sx, sy, sw, sh in station_bounds:
                margin = 2.0
                if (sx - margin <= elem.x <= sx + sw + margin and
                        sy - margin <= elem.y <= sy + sh + margin):
                    self.device_to_station[elem.element_id] = sid
                    break

        print(f"  站房映射已建立: {len(self.device_to_station)} 个设备归属 {len(station_bounds)} 个站房")

    # ------------------------------------------------------------------
    # 备用间隔检测（完善版）
    # ------------------------------------------------------------------
    def _detect_spare_intervals(self):
        """识别站内备用间隔设备。

        规则（需同时满足）：
        1. 设备类型为 LoadBreakSwitch 或 Breaker
        2. 设备位于站房内部
        3. 业务类型不是主干(3)或联络(5)
        4. 连接设备数 <= 1
        """
        station_bounds = {
            sid: (sx, sy, sw, sh)
            for sid, sx, sy, sw, sh in [
                (e.element_id, e.x, e.y, e.width, e.height)
                for e in self.doc.elements
                if e.layer_name == "Substation"
            ]
            if sid
        }

        self.spare_device_ids = set()
        for elem in self.doc.elements:
            if elem.layer_name not in ("LoadBreakSwitch", "Breaker"):
                continue
            if not elem.element_id:
                continue

            # 位于站房内部
            in_station = False
            for sx, sy, sw, sh in station_bounds.values():
                margin = 2.0
                if (sx - margin <= elem.x <= sx + sw + margin and
                        sy - margin <= elem.y <= sy + sh + margin):
                    in_station = True
                    break
            if not in_station:
                continue

            # 排除主干和联络
            if elem.line_type == "Trunk" or elem.business_type == "5":
                continue

            # 连接数检查
            connected = self.doc.get_connected_devices(elem.element_id)
            if len(connected) <= 1:
                self.spare_device_ids.add(elem.element_id)

        if self.spare_device_ids:
            print(f"  检测到备用间隔设备: {len(self.spare_device_ids)} 个")

        # 为备用设备添加“备用”标注
        for dev_id in self.spare_device_ids:
            elem = None
            for e in self.doc.elements:
                if e.element_id == dev_id:
                    elem = e
                    break
            if elem is None:
                continue
            spare_txt = SvgText()
            spare_txt.text_id = f"TXT_SPARE_{dev_id}"
            spare_txt.content = "备用"
            spare_txt.object_id = dev_id
            spare_txt.raw_object_id = f"TXT_SPARE_{dev_id}"
            spare_txt.font_size = 12.0
            spare_txt.font_weight = "normal"
            spare_txt.font_family = "Microsoft YaHei, SimHei, sans-serif"
            spare_txt.fill = STYLE["text"]
            spare_txt.text_role = "spare"
            spare_txt.dx = 14
            spare_txt.dy = 4
            spare_txt.text_anchor = "start"
            spare_txt.dominant_baseline = "middle"
            cx = elem.x + elem.width / 2
            cy = elem.y + elem.height / 2
            spare_txt.x = cx
            spare_txt.y = cy
            self.doc.texts.append(spare_txt)
            self.text_device_map[spare_txt.text_id] = dev_id

        if self.spare_device_ids:
            print(f"  已添加备用标注: {len(self.spare_device_ids)} 个")

    # ------------------------------------------------------------------
    # B.1 网格吸附（设备与连接线同步）
    # ------------------------------------------------------------------
    def _snap_to_grid(self):
        """将设备坐标对齐到网格，并同步更新连接线端点。

        核心原则：
        1. 使用 start_device_id/end_device_id 精确匹配连接线端点到设备
        2. 吸附后同步更新 transform 的 translate 分量
        3. 不改变 width/height（保持显示比例）
        """
        g = GRID_SIZE
        snapped = 0

        # 建立设备位置映射
        device_pos_map = {}  # device_id -> {old_x, old_y, new_x, new_y, element}
        for elem in self.doc.elements:
            if not elem.element_id:
                continue
            old_x, old_y = elem.x, elem.y
            new_x = round(elem.x / g) * g
            new_y = round(elem.y / g) * g

            device_pos_map[elem.element_id] = {
                "old_x": old_x, "old_y": old_y,
                "new_x": new_x, "new_y": new_y,
                "element": elem,
            }

            if elem.x != new_x or elem.y != new_y:
                old_x, old_y = elem.x, elem.y
                elem.x = new_x
                elem.y = new_y
                # 同步更新 transform：保留 scale/rotate，仅替换位置相关数值
                if elem.transform or getattr(elem, 'raw_transform', None):
                    elem.patch_transform_translate(old_x, old_y, new_x, new_y)
                snapped += 1

        # 连接线端点同步：使用 start_device_id/end_device_id 精确匹配
        for conn in self.doc.connections:
            if not conn.points:
                continue
            new_points = list(conn.points)

            # 设备端点映射：device_id -> index of point in conn.points
            device_point_indices = {}
            if conn.start_device_id and conn.start_device_id in device_pos_map:
                device_point_indices[conn.start_device_id] = 0
            if conn.end_device_id and conn.end_device_id in device_pos_map:
                device_point_indices[conn.end_device_id] = len(new_points) - 1

            # 根据设备位移同步更新端点
            for dev_id, point_idx in device_point_indices.items():
                if point_idx < len(new_points):
                    pos_info = device_pos_map[dev_id]
                    dx = pos_info["new_x"] - pos_info["old_x"]
                    dy = pos_info["new_y"] - pos_info["old_y"]
                    if dx != 0 or dy != 0:
                        px, py = new_points[point_idx]
                        new_points[point_idx] = (px + dx, py + dy)

            conn.points = new_points

        # 同步更新文字位置
        for txt in self.doc.texts:
            dev_id = self.text_device_map.get(txt.text_id, "")
            if dev_id and dev_id in device_pos_map:
                pos_info = device_pos_map[dev_id]
                dx = pos_info["new_x"] - pos_info["old_x"]
                dy = pos_info["new_y"] - pos_info["old_y"]
                if dx != 0 or dy != 0:
                    txt.x += dx
                    txt.y += dy

        print(f"  网格吸附({g}): {snapped} 个设备已对齐，连接线端点已同步")

    # ------------------------------------------------------------------
    # 站房内设备布局重构
    # ------------------------------------------------------------------
    def _rearrange_station_devices(self):
        """重构站房内设备布局：关键设备居中，备用设备放右侧，其他设备纵向等间距排列。"""
        station_bounds = {
            e.element_id: (e.x, e.y, e.width, e.height)
            for e in self.doc.elements
            if e.layer_name == "Substation" and e.element_id
        }
        if not station_bounds:
            return

        moved = 0
        for sid, (sx, sy, sw, sh) in station_bounds.items():
            inner = [e for e in self.doc.elements
                     if e.element_id != sid and self.device_to_station.get(e.element_id) == sid]
            if not inner:
                continue

            key_devs = [e for e in inner if e.layer_name in KEY_DEVICE_LAYERS or e.layer_name == "BusbarSection"]
            spare_devs = [e for e in inner if e.element_id in self.spare_device_ids]
            other_devs = [e for e in inner if e not in key_devs and e not in spare_devs]

            left_margin = 10.0
            right_margin = 10.0
            top_margin = 10.0
            bottom_margin = 10.0

            main_devs = key_devs + other_devs
            if main_devs:
                usable_h = max(sh - top_margin - bottom_margin, 10.0)
                spacing = usable_h / (len(main_devs) + 1)
                for i, elem in enumerate(main_devs):
                    new_x = sx + sw / 2 - elem.width / 2
                    new_y = sy + top_margin + spacing * (i + 1) - elem.height / 2
                    dx = new_x - elem.x
                    dy = new_y - elem.y
                    if dx != 0 or dy != 0:
                        old_x, old_y = elem.x, elem.y
                        elem.x = new_x
                        elem.y = new_y
                        if elem.transform or getattr(elem, 'raw_transform', None):
                            elem.patch_transform_translate(old_x, old_y, new_x, new_y)
                        moved += 1
                        self._sync_device_move(elem.element_id, dx, dy)

            if spare_devs:
                usable_h = max(sh - top_margin - bottom_margin, 10.0)
                spacing = usable_h / (len(spare_devs) + 1)
                for i, elem in enumerate(spare_devs):
                    new_x = sx + sw - right_margin - elem.width
                    new_y = sy + top_margin + spacing * (i + 1) - elem.height / 2
                    dx = new_x - elem.x
                    dy = new_y - elem.y
                    if dx != 0 or dy != 0:
                        old_x, old_y = elem.x, elem.y
                        elem.x = new_x
                        elem.y = new_y
                        if elem.transform or getattr(elem, 'raw_transform', None):
                            elem.patch_transform_translate(old_x, old_y, new_x, new_y)
                        moved += 1
                        self._sync_device_move(elem.element_id, dx, dy)

        print(f"  站房内设备已重构布局: {moved} 个设备已移动")

    def _sync_device_move(self, dev_id: str, dx: float, dy: float):
        """同步移动与设备关联的连接线端点和文字。"""
        for conn in self.doc.connections:
            if not conn.points:
                continue
            updated = False
            new_points = list(conn.points)
            if conn.start_device_id == dev_id:
                px, py = new_points[0]
                new_points[0] = (px + dx, py + dy)
                updated = True
            if conn.end_device_id == dev_id:
                px, py = new_points[-1]
                new_points[-1] = (px + dx, py + dy)
                updated = True
            if updated:
                conn.points = new_points
        for txt in self.doc.texts:
            if self.text_device_map.get(txt.text_id) == dev_id:
                txt.x += dx
                txt.y += dy

    # ------------------------------------------------------------------
    # B.2/B.3 连接线样式
    # ------------------------------------------------------------------
    def _normalize_connection_styles(self):
        """按业务类型和电压等级统一连接线颜色、线宽、线型。"""
        updated = 0
        cross_station_count = 0
        for conn in self.doc.connections:
            style = self._classify_connection(conn)
            if style["color"] == STYLE["cross_station_tie"]:
                cross_station_count += 1
            conn.stroke = style["color"]
            conn.stroke_width = str(style["width"])
            conn.stroke_dasharray = style.get("dasharray", "")
            conn.fill = "none"
            conn.stroke_linecap = "round"
            conn.stroke_linejoin = "round"
            updated += 1
        print(f"  连接线样式已规范化: {updated} 条 (跨站联络: {cross_station_count} 条)")

    def _classify_connection(self, conn: SvgConnection) -> dict:
        cls = conn.css_class or ""

        # 1. 电源追溯路径 #1890FF（businessType="1" 或 TopType="01"）
        if conn.business_type == "1" or conn.top_type == "01":
            return {
                "color": STYLE["trace_path"],
                "width": LINE_WIDTHS["main_feeder"],
            }

        # 2. 备用间隔引线
        if self.spare_device_ids:
            refs = set(conn.glink_refs)
            if refs & self.spare_device_ids:
                return {
                    "color": STYLE["spare_interval"],
                    "width": LINE_WIDTHS["spare_interval"],
                    "dasharray": "4,4",
                }

        # 3. 联络线 businessType=5
        if conn.business_type == "5":
            start_station = self.device_to_station.get(conn.start_device_id, "")
            end_station = self.device_to_station.get(conn.end_device_id, "")
            if start_station and end_station and start_station != end_station:
                return {"color": STYLE["cross_station_tie"], "width": LINE_WIDTHS["tie_line"]}
            return {"color": STYLE["tie_line"], "width": LINE_WIDTHS["tie_line"]}

        # 4. 按电压等级映射
        width = LINE_WIDTHS["branch"]
        color = STYLE["main_feeder"]
        for c, w in VOLTAGE_CLASS_WIDTHS.items():
            if c in cls:
                width = w
                color = VOLTAGE_CLASS_MAP.get(c, STYLE["main_feeder"])
                break
        return {"color": color, "width": width}

    # ------------------------------------------------------------------
    # B.4 文字样式 + 位置规范化
    # ------------------------------------------------------------------
    def _normalize_text_styles(self):
        """按规范B.4设置文字颜色、字号、字重和位置。"""
        color_updated = 0
        font_updated = 0
        pos_updated = 0
        hidden_count = 0
        matched_texts = 0
        total_texts = len(self.doc.texts)

        # 建立 device_id → device 的映射
        device_by_id = {}
        for elem in self.doc.elements:
            if elem.element_id:
                device_by_id[elem.element_id] = elem

        # 建立站房边界列表（用于判断设备是否在站房内，从而过滤站内设备名称）
        station_bounds = []
        for elem in self.doc.elements:
            if elem.layer_name == "Substation" and elem.width and elem.height:
                station_bounds.append((elem.x, elem.y, elem.width, elem.height))

        # 建立 connection_id / glink_ref → connection 的映射（用于线路文字定位）
        connection_by_id = {}
        for conn in self.doc.connections:
            if conn.connection_id:
                connection_by_id[conn.connection_id] = conn
            for gid in conn.glink_refs:
                if gid:
                    connection_by_id[gid] = conn

        # 建立文字 → 设备 关联索引（通过 object_id 名称匹配）
        # object_id 已经在 reader 中去掉 TXT_ 前缀
        self.text_device_map = {}
        for txt in self.doc.texts:
            if txt.object_id and txt.object_id in device_by_id:
                self.text_device_map[txt.text_id] = txt.object_id
                matched_texts += 1

        # 如果直接匹配不足，用 object_name 与设备 element_name 匹配
        if matched_texts < total_texts:
            name_to_device = {}
            for elem in self.doc.elements:
                if elem.element_name:
                    name_to_device[elem.element_name] = elem.element_id

            for txt in self.doc.texts:
                if txt.text_id not in self.text_device_map and txt.object_name:
                    dev_id = name_to_device.get(txt.object_name, "")
                    if dev_id:
                        self.text_device_map[txt.text_id] = dev_id
                        matched_texts += 1

        print(f"  文字→设备关联: {matched_texts}/{total_texts}")

        for txt in self.doc.texts:
            # 1. 颜色统一
            if txt.fill != STYLE["text"]:
                txt.fill = STYLE["text"]
                color_updated += 1

            # 2. 判定 text_role（保留已预设的特殊角色，如 spare）
            if not txt.text_role:
                dev_id = self.text_device_map.get(txt.text_id, "")
                elem = device_by_id.get(dev_id)
                content = txt.content.strip()
                has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
                is_code = bool(re.match(r'^[A-Z0-9_-]+$', content)) and not has_chinese
                is_station_name = bool(re.search(r'(变电站|开关站|配电室|站房|开闭所)', content))
                is_line_name = bool(re.search(r'LINE\d+|_线|馈线', content))
                if elem and elem.layer_name == "Substation":
                    txt.text_role = "title"
                elif elem and elem.layer_name == "ACLineSegment":
                    txt.text_role = "line"
                elif is_station_name:
                    txt.text_role = "title"
                elif is_line_name:
                    txt.text_role = "line"
                elif is_code or content == txt.object_id:
                    txt.text_role = "id"
                else:
                    txt.text_role = "name"

            # 2.1 文字过滤：隐藏 ID 和描述性线路标签
            if self._should_hide_text(txt):
                txt.hidden = True
                hidden_count += 1
                continue

            # 2.2 长标签截断
            txt.content = self._truncate_text(txt.content)

            # 3. 字体
            txt.font_family = "Microsoft YaHei, SimHei, sans-serif"

            # 4. 字号/字重分级
            old_size = txt.font_size
            old_weight = txt.font_weight
            size, weight = self._classify_text(txt, device_by_id)
            if size != old_size or weight != old_weight:
                txt.font_size = size
                txt.font_weight = weight
                font_updated += 1

            # 3. 位置：根据关联设备按 B.4 规范重新定位
            dev_id = self.text_device_map.get(txt.text_id, "")
            elem = device_by_id.get(dev_id) if dev_id else None
            if elem and not (elem.width <= 0 and elem.height <= 0 and elem.x == 0 and elem.y == 0):
                pos_info = self._compute_text_position(txt, elem)
                if pos_info:
                    if pos_info.get("dx") != txt.dx or pos_info.get("dy") != txt.dy:
                        pos_updated += 1
                    txt.dx = pos_info.get("dx", 0)
                    txt.dy = pos_info.get("dy", 0)
                    txt.text_anchor = pos_info.get("text_anchor", "middle")
                    txt.dominant_baseline = pos_info.get("dominant_baseline", "auto")
                    txt.x = pos_info["device_x"]
                    txt.y = pos_info["device_y"]
            else:
                # 无有效关联设备（或 ACLineSegment 无图元）
                # 线路文字优先按对应连接线中点定位，避免大量标签共享同一 y 坐标
                if txt.text_role == "line":
                    conn = connection_by_id.get(txt.object_id)
                    if conn and conn.points:
                        mid_idx = len(conn.points) // 2
                        new_x, new_y = conn.points[mid_idx]
                        if abs(new_x - txt.x) > 0.001 or abs(new_y - txt.y) > 0.001:
                            txt.x = new_x
                            txt.y = new_y
                            pos_updated += 1

                pos_info = self._compute_text_position_no_device(txt)
                if pos_info:
                    if pos_info.get("dx") != txt.dx or pos_info.get("dy") != txt.dy:
                        pos_updated += 1
                    txt.dx = pos_info.get("dx", 0)
                    txt.dy = pos_info.get("dy", 0)
                    txt.text_anchor = pos_info.get("text_anchor", "middle")
                    txt.dominant_baseline = pos_info.get("dominant_baseline", "auto")

        print(f"  文字颜色: {color_updated} 个, 字号/字重: {font_updated} 个, 位置: {pos_updated} 个, 隐藏: {hidden_count} 个")

    def _resolve_text_collisions(self):
        """全局文字碰撞避让：基于近似包围盒，按优先级贪心错开，必要时隐藏。

        策略：按 title > 关键设备名 > 普通设备名 > spare > line 优先级排序，
        对每个文字计算近似 BBox，若与已放置文字重叠，尝试在 ±30px 范围内小步
        偏移（优先纵向，其次横向），仍无法错开时隐藏优先级较低的文字，避免
        标签远离设备。
        """
        visible_texts = [t for t in self.doc.texts if not getattr(t, "hidden", False)]
        if not visible_texts:
            return

        device_by_id = {e.element_id: e for e in self.doc.elements if e.element_id}

        def _priority(t: SvgText) -> int:
            if t.text_role == "title":
                return 0
            if t.text_role == "name":
                dev_id = self.text_device_map.get(t.text_id, "")
                elem = device_by_id.get(dev_id)
                if elem and elem.layer_name in KEY_DEVICE_LAYERS:
                    return 1
                return 2
            if t.text_role == "spare":
                return 3
            if t.text_role == "line":
                return 4
            return 5

        visible_texts.sort(key=lambda t: (_priority(t), t.y, t.x))

        placed = []  # (x, y, w, h)
        adjusted = 0
        hidden = 0

        # 候选偏移：优先小幅度纵向，再横向；限制在设备附近
        candidate_offsets = [
            (0, 12), (0, -12), (0, 24), (0, -24), (0, 30), (0, -30),
            (12, 0), (-12, 0), (24, 0), (-24, 0),
        ]

        for txt in visible_texts:
            bx, by, bw, bh = self._text_bbox(txt)
            overlaps = lambda x, y: any(
                self._bbox_overlap(x, y, bw, bh, px, py, pw, ph) for px, py, pw, ph in placed
            )

            if not overlaps(bx, by):
                placed.append((bx, by, bw, bh))
                continue

            found = False
            best_x, best_y = bx, by
            for ox, oy in candidate_offsets:
                nx, ny = bx + ox, by + oy
                if not overlaps(nx, ny):
                    best_x, best_y = nx, ny
                    found = True
                    break

            if found:
                # 将偏移量累加到 dx/dy
                txt.dx += best_x - bx
                txt.dy += best_y - by
                placed.append((best_x, best_y, bw, bh))
                adjusted += 1
            else:
                txt.hidden = True
                hidden += 1

        print(f"  文字碰撞避让: 调整 {adjusted} 个, 隐藏 {hidden} 个")

    def _text_bbox(self, txt: SvgText) -> tuple:
        """计算文字近似包围盒，尽量贴近浏览器实际渲染。"""
        x = txt.x + txt.dx
        y = txt.y + txt.dy
        content = txt.content or ""
        # 中文字符近似宽度：字号 × 0.7；英文/数字更窄，这里取保守值
        w = max(txt.font_size * len(content) * 0.7, txt.font_size * 1.5)
        h = txt.font_size * 1.5
        # 根据 text-anchor 修正：middle 时 x 为文字中心
        if txt.text_anchor == "middle":
            x -= w / 2.0
        elif txt.text_anchor == "end":
            x -= w
        # 根据 dominant-baseline 修正 BBox 顶边
        if txt.dominant_baseline in ("middle", "central"):
            y -= h / 2.0
        elif txt.dominant_baseline == "hanging":
            # hanging：y 为顶线，顶边就是 y
            pass
        else:
            # auto / alphabetic：y 为基线，保守取字形顶边在 y - h 处
            y -= h
        return x, y, w, h

    def _bbox_overlap(self, x1, y1, w1, h1, x2, y2, w2, h2, buffer: float = 1.0) -> bool:
        """判断两个轴对齐包围盒是否重叠（含 1px 缓冲）。"""
        return not (
            x1 + w1 + buffer < x2
            or x2 + w2 + buffer < x1
            or y1 + h1 + buffer < y2
            or y2 + h2 + buffer < y1
        )

    def _get_device_scale(self, elem: SvgElement) -> float:
        """从 transform 中提取设备的视觉缩放因子。

        SVG 中设备使用 use + transform 来渲染：
        transform = translate(tx, ty) scale(s) translate(-tx, -ty)
        渲染尺寸 = width × s, height × s

        返回值为设备的实际缩放因子（默认 1.0）。
        """
        if not elem.transform:
            return 1.0
        match = re.search(r'scale\(([^)]+)\)', elem.transform)
        if match:
            scale_str = match.group(1)
            parts = scale_str.split(',')
            sx = float(parts[0].strip())
            return abs(sx)
        return 1.0

    def _compute_text_position(self, txt: SvgText, elem: SvgElement) -> dict:
        """根据规范B.4计算文字定位（固定偏移，不使用设备高度倍数）。"""
        cx = elem.x + elem.width / 2
        cy = elem.y + elem.height / 2
        layer = elem.layer_name
        role = txt.text_role

        if role == "title":
            return {
                "dx": 0,
                "dy": -18,
                "text_anchor": "middle",
                "dominant_baseline": "auto",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "spare":
            return {
                "dx": 14,
                "dy": 4,
                "text_anchor": "start",
                "dominant_baseline": "middle",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "line":
            return {
                "dx": 0,
                "dy": -6,
                "text_anchor": "middle",
                "dominant_baseline": "auto",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "id":
            return {
                "dx": 0,
                "dy": 30,
                "text_anchor": "middle",
                "dominant_baseline": "hanging",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "name":
            if layer in KEY_DEVICE_LAYERS:
                return {
                    "dx": 0,
                    "dy": 18,
                    "text_anchor": "middle",
                    "dominant_baseline": "hanging",
                    "device_x": cx,
                    "device_y": cy,
                }
            return {
                "dx": 14,
                "dy": 4,
                "text_anchor": "start",
                "dominant_baseline": "middle",
                "device_x": cx,
                "device_y": cy,
            }

        return {
            "dx": 0,
            "dy": 18,
            "text_anchor": "middle",
            "dominant_baseline": "hanging",
            "device_x": cx,
            "device_y": cy,
        }

    def _compute_text_position_no_device(self, txt: SvgText) -> dict:
        """无有效关联设备时，仅按 text_role 应用规范 dx/dy/anchor（保持原 x/y）。"""
        role = txt.text_role
        if role == "title":
            return {"dx": 0, "dy": -18, "text_anchor": "middle", "dominant_baseline": "auto"}
        if role == "line":
            return {"dx": 0, "dy": -6, "text_anchor": "middle", "dominant_baseline": "auto"}
        if role == "id":
            return {"dx": 0, "dy": 30, "text_anchor": "middle", "dominant_baseline": "hanging"}
        if role == "spare":
            return {"dx": 14, "dy": 4, "text_anchor": "start", "dominant_baseline": "middle"}
        # 默认按支线设备名称处理
        return {"dx": 14, "dy": 4, "text_anchor": "start", "dominant_baseline": "middle"}

    def _should_hide_text(self, txt: SvgText) -> bool:
        """过滤非关键文字，降低图纸信息密度。

        隐藏规则：
        - 设备唯一 ID
        - 线路描述性标签（含 TMP/线开关/环网箱/进线/出线/联络等内部关键词）
        """
        role = txt.text_role
        content = txt.content or ""
        lower = content.lower()

        # 1. 隐藏设备唯一 ID
        if role == "id":
            return True

        # 2. 隐藏 ACLineSegment 内部描述性长标签
        if role == "line":
            # 包含内部编码或描述性关键词
            if any(k in lower for k in ["tmp", "线开关", "环网箱", "进线", "出线", "联络", "馈线"]):
                return True
            # 超长且带下划线的内部编号
            if len(content) > 20 and "_" in content:
                return True

        return False

    def _truncate_text(self, content: str, max_chars: int = 12) -> str:
        """长标签截断，超过 max_chars 时保留前段并加省略号。"""
        if not content:
            return content
        content = content.strip()
        if len(content) <= max_chars:
            return content
        return content[:max_chars] + "…"

    def _classify_text(self, txt: SvgText, device_by_id: dict) -> tuple:
        """根据 text_role 和关联设备图层返回固定字号（px）和字重。"""
        dev_id = self.text_device_map.get(txt.text_id, "")
        elem = device_by_id.get(dev_id)
        layer = elem.layer_name if elem else ""

        role = txt.text_role
        if role == "title":
            return 21.3, "bold"
        if role == "line":
            return 12.0, "normal"
        if role == "id":
            return 10.0, "normal"
        if role == "spare":
            return 12.0, "normal"
        if role == "name":
            if layer in KEY_DEVICE_LAYERS:
                return 14.0, "bold"
            return 12.0, "normal"
        return 12.0, "normal"

    # ------------------------------------------------------------------
    # B.2 站房边框
    # ------------------------------------------------------------------
    def _normalize_station_styles(self):
        """统一站房边框样式。"""
        updated = 0
        for elem in self.doc.elements:
            if elem.layer_name == "Substation":
                elem.fill = "none"
                elem.stroke = STYLE["station_border"]
                elem.stroke_width = str(LINE_WIDTHS["station_border"])
                updated += 1
        print(f"  站房边框样式已规范化: {updated} 个")

    # ------------------------------------------------------------------
    # 设备图标
    # ------------------------------------------------------------------
    def _normalize_device_icons(self):
        """标准化设备显示尺寸：按类型设定 width/height，去除 transform 中的极小 scale，
        并按中心点不变修正 x/y，使设备与文字/线宽尺度协调。"""
        updated = 0
        for elem in self.doc.elements:
            layer = elem.layer_name
            if layer not in DEVICE_STANDARD_SIZES:
                continue

            std_w, std_h = DEVICE_STANDARD_SIZES[layer]
            old_w = elem.width or std_w
            old_h = elem.height or std_h
            cx = elem.x + old_w / 2.0
            cy = elem.y + old_h / 2.0

            new_x = cx - std_w / 2.0
            new_y = cy - std_h / 2.0
            dx = new_x - elem.x
            dy = new_y - elem.y

            elem.x = new_x
            elem.y = new_y
            elem.width = std_w
            elem.height = std_h

            # 同步更新 transform：简化为 rotate(angle,cx,cy)
            # use 的 x/y 已经定位，不需要 transform 再带 translate；scale 由 width/height 决定
            rotation = SvgDocument._parse_transform(elem.transform or getattr(elem, 'raw_transform', '') or '')[3]
            elem.transform = f"rotate({rotation:.6f},{cx:.6f},{cy:.6f})"

            updated += 1

        print(f"  设备图标已标准化: {updated} 个")

    def _scale_coordinate_space(self, factor: float = 3.5):
        """统一放大坐标空间，使原始密集布局舒展到能容纳标准尺寸设备和文字。

        只缩放位置（x/y、连接点、文字基准点），设备 width/height 保持规范 px
        尺寸，文字字号也保持不变。
        """
        for elem in self.doc.elements:
            elem.x *= factor
            elem.y *= factor
            # width/height 是规范标准 px 尺寸，不随坐标空间缩放

        for conn in self.doc.connections:
            conn.points = [(x * factor, y * factor) for x, y in conn.points]

        for txt in self.doc.texts:
            txt.x *= factor
            txt.y *= factor
            # dx/dy 是规范固定 px 偏移，不随坐标空间缩放

        # 站房边界也同步缩放
        self.station_bounds = [
            (sx * factor, sy * factor, sw * factor, sh * factor)
            for (sx, sy, sw, sh) in getattr(self, "station_bounds", [])
        ]

        print(f"  坐标空间已缩放: {factor} 倍")

    def _route_connections_to_edges(self):
        """把连接线端点从设备中心移到设备边缘，避免线穿过设备内部。"""
        device_by_id = {e.element_id: e for e in self.doc.elements if e.element_id}
        updated = 0

        def _edge_point(dev, target_x, target_y):
            cx = dev.x + dev.width / 2.0
            cy = dev.y + dev.height / 2.0
            dx = target_x - cx
            dy = target_y - cy
            if abs(dx) < 1e-6 and abs(dy) < 1e-6:
                return cx, cy
            # 判断射线先碰到水平边还是垂直边
            if abs(dx) * dev.height > abs(dy) * dev.width:
                # 碰到左右边
                ex = dev.x + (dev.width if dx > 0 else 0.0)
                ratio = (dev.width / 2.0) / abs(dx)
                ey = cy + dy * ratio
            else:
                # 碰到上下边
                ratio = (dev.height / 2.0) / abs(dy)
                ex = cx + dx * ratio
                ey = dev.y + (dev.height if dy > 0 else 0.0)
            return ex, ey

        for conn in self.doc.connections:
            if not conn.points:
                continue
            # 起点
            if conn.start_device_id:
                dev = device_by_id.get(conn.start_device_id)
                if dev and len(conn.points) >= 2:
                    new_pt = _edge_point(dev, conn.points[1][0], conn.points[1][1])
                    if new_pt != conn.points[0]:
                        conn.points[0] = new_pt
                        updated += 1
            # 终点
            if conn.end_device_id:
                dev = device_by_id.get(conn.end_device_id)
                if dev and len(conn.points) >= 2:
                    new_pt = _edge_point(dev, conn.points[-2][0], conn.points[-2][1])
                    if new_pt != conn.points[-1]:
                        conn.points[-1] = new_pt
                        updated += 1

        print(f"  连接线已路由到设备边缘: {updated} 条")


def beautify_svg_file(svg_path: str, output_path: str = None) -> str:
    beautifier = SvgBeautifier(svg_path, output_path=output_path)
    return beautifier.beautify()


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    svg_dir = os.path.join(project_root, "数据集更新版20260729", "配网 svg")
    output_dir = os.path.join(project_root, "output", "svg")
    os.makedirs(output_dir, exist_ok=True)

    for fname in ["LINE215.svg", "LINE216.svg"]:
        fpath = os.path.join(svg_dir, fname)
        if os.path.exists(fpath):
            print(f"\n处理 {fname}...")
            out_path = os.path.join(output_dir, f"{os.path.splitext(fname)[0]}_beautified.svg")
            result_path = beautify_svg_file(fpath, output_path=out_path)
            print(f"已输出: {result_path}")


if __name__ == "__main__":
    main()
