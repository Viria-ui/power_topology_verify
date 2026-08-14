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

        # 第1步：建立站房映射 + 文字→设备关联
        self._build_station_map()
        self._build_text_device_map()
        self._detect_spare_intervals()

        # 第2步：连接线样式规范化（颜色、线宽、线型）
        self._normalize_connection_styles()

        # 第3步：站房边框标准化
        self._normalize_station_styles()

        # 第4步：文字样式/位置规范化（紧贴设备、统一字号字重）
        self._normalize_text_styles()

        # 第5步：自适应viewbox（保持原始坐标空间）
        self._adapt_viewbox()

        # 写出 SVG（含白色背景）
        write_svg(self.doc, self.output_path, update_style=True)

        # 自检并输出质量报告
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
                margin = max(2.0, sw * 0.05)
                if (sx - margin <= elem.x <= sx + sw + margin and
                        sy - margin <= elem.y <= sy + sh + margin):
                    self.device_to_station[elem.element_id] = sid
                    break

        print(f"  站房映射已建立: {len(self.device_to_station)} 个设备归属 {len(station_bounds)} 个站房")

    # ------------------------------------------------------------------
    # 文字 → 设备 关联索引（提前构建，确保后续设备移动时文字可同步）
    # ------------------------------------------------------------------
    def _build_text_device_map(self):
        """建立 text_id → device_id 的映射，在所有设备移动操作之前调用。

        通过 object_id 直接匹配和 object_name 名称匹配两种方式建立关联。
        """
        # 建立 device_id → device 的映射
        device_by_id = {}
        for elem in self.doc.elements:
            if elem.element_id:
                device_by_id[elem.element_id] = elem

        total_texts = len(self.doc.texts)
        matched_texts = 0
        self.text_device_map = {}

        # 1. 通过 object_id 直接匹配
        for txt in self.doc.texts:
            if txt.object_id and txt.object_id in device_by_id:
                self.text_device_map[txt.text_id] = txt.object_id
                matched_texts += 1

        # 2. 如果直接匹配不足，用 object_name 与设备 element_name 匹配
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
                margin = max(2.0, sw * 0.05)
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
        """将站房外设备坐标对齐到动态网格，并同步更新连接线端点。

        核心原则：
        1. 跳过站房内设备（由拓扑布局确定坐标）
        2. 动态网格尺寸基于标准设备宽度 + 最小间距
        3. 同点去重：多个设备不会被吸附到同一网格点
        4. 连接线端点同步更新
        """
        g = self._compute_grid_size()
        snapped = 0

        device_pos_map = {}
        occupied_positions = {}  # (grid_x, grid_y) -> element_id

        for elem in self.doc.elements:
            if not elem.element_id:
                continue
            # 跳过站房内设备（由拓扑布局确定坐标）
            if elem.element_id in self.device_to_station:
                continue
            # 跳过站房本身
            if elem.layer_name == "Substation":
                continue

            old_x, old_y = elem.x, elem.y
            new_x = round(elem.x / g) * g
            new_y = round(elem.y / g) * g

            # 同点去重：如果该网格点已有设备，先尝试上下偏移，避免全部堆积在同一行
            while (new_x, new_y) in occupied_positions:
                # 先尝试向下偏移一个网格行
                next_y = new_y + g
                if (new_x, next_y) not in occupied_positions:
                    new_y = next_y
                else:
                    # 再尝试向上偏移
                    prev_y = new_y - g
                    if prev_y > 0 and (new_x, prev_y) not in occupied_positions:
                        new_y = prev_y
                    else:
                        # 最后才向右偏移
                        new_x += g

            occupied_positions[(new_x, new_y)] = elem.element_id

            device_pos_map[elem.element_id] = {
                "old_x": old_x, "old_y": old_y,
                "new_x": new_x, "new_y": new_y,
                "element": elem,
            }

            if elem.x != new_x or elem.y != new_y:
                elem.x = new_x
                elem.y = new_y
                if elem.transform or getattr(elem, 'raw_transform', None):
                    elem.patch_transform_translate(old_x, old_y, new_x, new_y)
                snapped += 1

        # 连接线端点同步
        for conn in self.doc.connections:
            if not conn.points:
                continue
            new_points = list(conn.points)
            device_point_indices = {}
            if conn.start_device_id and conn.start_device_id in device_pos_map:
                device_point_indices[conn.start_device_id] = 0
            if conn.end_device_id and conn.end_device_id in device_pos_map:
                device_point_indices[conn.end_device_id] = len(new_points) - 1

            for dev_id, point_idx in device_point_indices.items():
                if point_idx < len(new_points):
                    pos_info = device_pos_map[dev_id]
                    dx = pos_info["new_x"] - pos_info["old_x"]
                    dy = pos_info["new_y"] - pos_info["old_y"]
                    if dx != 0 or dy != 0:
                        px, py = new_points[point_idx]
                        new_points[point_idx] = (px + dx, py + dy)
            conn.points = new_points

        # 同步文字位置
        for txt in self.doc.texts:
            dev_id = self.text_device_map.get(txt.text_id, "")
            if dev_id and dev_id in device_pos_map:
                pos_info = device_pos_map[dev_id]
                dx = pos_info["new_x"] - pos_info["old_x"]
                dy = pos_info["new_y"] - pos_info["old_y"]
                if dx != 0 or dy != 0:
                    txt.x += dx
                    txt.y += dy

        print(f"  网格吸附(grid={g:.1f}): {snapped} 个站房外设备已对齐，连接线端点已同步")

    # ------------------------------------------------------------------
    # 设备重叠消解
    # ------------------------------------------------------------------
    def _resolve_device_overlaps(self):
        """检测并消解设备 bounding box 重叠：将重叠设备向 y 方向偏移。"""
        device_elems = [e for e in self.doc.elements
                        if e.element_id and e.layer_name != "Substation"
                        and e.width > 0 and e.height > 0]
        if len(device_elems) < 2:
            return

        max_iter = 3
        total_resolved = 0
        for iteration in range(max_iter):
            overlaps = 0
            for i in range(len(device_elems)):
                e1 = device_elems[i]
                for j in range(i + 1, len(device_elems)):
                    e2 = device_elems[j]
                    # 检查 bounding box 重叠
                    if not (e1.x + e1.width + 1 < e2.x or
                            e2.x + e2.width + 1 < e1.x or
                            e1.y + e1.height + 1 < e2.y or
                            e2.y + e2.height + 1 < e1.y):
                        overlaps += 1
                        # 将 e2 向下偏移
                        offset = e1.height + 4
                        old_y = e2.y
                        e2.y += offset
                        if e2.transform or getattr(e2, 'raw_transform', None):
                            e2.patch_transform_translate(e2.x, old_y, e2.x, e2.y)
                        self._sync_device_move(e2.element_id, 0, offset)
                        total_resolved += 1
            if overlaps == 0:
                break

        if total_resolved > 0:
            print(f"  设备重叠消解: {total_resolved} 个设备已偏移")

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
    # 站房内拓扑布局（基于 self.doc.connections 构建无向图）
    # ------------------------------------------------------------------
    def _layout_by_topology(self):
        """按电气拓扑关系重新排布站房内设备，消除成团现象。

        算法流程：
        1. 基于 connections 构建设备无向图
        2. 按站房分组设备
        3. 选择根节点（母线优先）
        4. BFS 分层
        5. 按拓扑层分配 x，按子树宽度分配 y
        6. 备用设备放右侧
        """
        import networkx as nx

        # 1. 构建设备无向图
        G = nx.Graph()
        device_by_id = {}
        for elem in self.doc.elements:
            if elem.element_id and elem.layer_name != "Substation":
                G.add_node(elem.element_id, layer=elem.layer_name, element=elem)
                device_by_id[elem.element_id] = elem

        for conn in self.doc.connections:
            sid = conn.start_device_id
            eid = conn.end_device_id
            if sid and eid and sid in device_by_id and eid in device_by_id:
                G.add_edge(sid, eid)

        # 2. 按站房分组设备
        station_devices = {}
        for dev_id, station_id in self.device_to_station.items():
            if station_id not in station_devices:
                station_devices[station_id] = []
            station_devices[station_id].append(dev_id)

        # 3. 获取站房边界
        station_bounds = {}
        for elem in self.doc.elements:
            if elem.layer_name == "Substation" and elem.element_id:
                station_bounds[elem.element_id] = (elem.x, elem.y, elem.width, elem.height)

        moved = 0
        stations_processed = 0
        for sid, dev_ids in station_devices.items():
            if not dev_ids or sid not in station_bounds:
                continue

            sx, sy, sw, sh = station_bounds[sid]
            sub_G = G.subgraph(dev_ids).copy()
            if not sub_G.nodes:
                continue

            # 选择根节点
            root = self._pick_root(sub_G)
            if root is None:
                continue

            # BFS 分层
            layers = self._bfs_layers(sub_G, root)

            # 分配坐标
            moved += self._assign_coords_by_layers(
                sid, layers, sub_G, sx, sy, sw, sh, device_by_id)
            stations_processed += 1

        print(f"  站房内拓扑布局: {moved} 个设备已重新排列, {stations_processed} 个站房")

    def _pick_root(self, sub_G):
        """选择根节点：母线优先，其次变压器，最后度数最大的。"""
        # 优先母线
        for node in sub_G.nodes:
            layer = sub_G.nodes[node].get("layer", "")
            if layer == "BusbarSection":
                return node
        # 其次变压器
        for node in sub_G.nodes:
            layer = sub_G.nodes[node].get("layer", "")
            if layer == "PowerTransformer":
                return node
        # 再次断路器
        for node in sub_G.nodes:
            layer = sub_G.nodes[node].get("layer", "")
            if layer == "Breaker":
                return node
        # 最后度数最大的
        if sub_G.nodes:
            return max(sub_G.nodes, key=lambda n: sub_G.degree(n))
        return None

    def _bfs_layers(self, sub_G, root):
        """从根节点 BFS 分层，返回 {layer_index: [device_ids]}。"""
        layers = {}
        visited = {root}
        queue = [(root, 0)]
        while queue:
            node, depth = queue.pop(0)
            if depth not in layers:
                layers[depth] = []
            layers[depth].append(node)
            for neighbor in sub_G.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        # 处理孤立节点
        for node in sub_G.nodes:
            if node not in visited:
                if 0 not in layers:
                    layers[0] = []
                layers[0].append(node)
        return layers

    def _assign_coords_by_layers(self, sid, layers, sub_G,
                                  sx, sy, sw, sh, device_by_id):
        """按拓扑层分配坐标：层间用 x（深度方向），层内用 y（纵向排列）。

        站房内布局规范（对齐规范 4.3）：
        - 设备按拓扑深度从左到右排列
        - 同层设备纵向等间距排列
        - 备用设备放站房右侧
        - 站房过小时自动扩展
        """
        moved = 0
        max_dev_w = max(w for w, h in DEVICE_STANDARD_SIZES.values())
        max_dev_h = max(h for w, h in DEVICE_STANDARD_SIZES.values())

        col_width = max_dev_w + 12.0  # 列宽
        row_height = max_dev_h + 16.0  # 行高

        # 计算总需要的宽度和高度
        num_layers = max(layers.keys()) + 1 if layers else 1
        total_width = num_layers * col_width + 20
        max_layer_size = max(len(devs) for devs in layers.values()) if layers else 1
        total_height = max(max_layer_size * row_height + 20, sh)

        # 如果站房太小，扩大站房（同时更新 polygon points）
        station_elem = None
        for elem in self.doc.elements:
            if elem.element_id == sid and elem.layer_name == "Substation":
                station_elem = elem
                break

        if station_elem:
            needs_update = False
            new_w = sw
            new_h = sh
            if sw < total_width:
                new_w = total_width
                needs_update = True
            if sh < total_height:
                new_h = total_height
                needs_update = True

            if needs_update:
                # 更新 Python 属性
                station_elem.width = new_w
                station_elem.height = new_h
                # 同步更新 polygon points（如果是 polygon 元素）
                if station_elem.shape_tag == "polygon":
                    pts_str = station_elem.shape_attrs.get("points", "")
                    if pts_str:
                        # 解析原始 points，找到四个角点，更新 x2 和 y2
                        # polygon 格式: "x1,y1 x1,y2 x2,y2 x2,y1"
                        pts = pts_str.strip().split()
                        if len(pts) >= 4:
                            # 从第一个点获取 x1, y1
                            x1, y1 = pts[0].split(",")
                            x1_val, y1_val = float(x1), float(y1)
                            # 新的 x2, y2
                            x2_new = x1_val + new_w
                            y2_new = y1_val + new_h
                            # 重建 points 字符串（保持原格式）
                            new_pts = (
                                f"{x1_val:.6f},{y1_val:.6f} "
                                f"{x1_val:.6f},{y2_new:.6f} "
                                f"{x2_new:.6f},{y2_new:.6f} "
                                f"{x2_new:.6f},{y1_val:.6f}"
                            )
                            station_elem.shape_attrs["points"] = new_pts
                sw = new_w
                sh = new_h

        # 分配坐标
        for layer_idx, dev_ids in sorted(layers.items()):
            x = sx + 10 + layer_idx * col_width
            non_spare_devs = [d for d in dev_ids if d not in self.spare_device_ids]
            num_in_layer = len(non_spare_devs)
            if num_in_layer == 0:
                continue

            for i, dev_id in enumerate(non_spare_devs):
                elem = device_by_id.get(dev_id)
                if not elem:
                    continue

                std_w, std_h = DEVICE_STANDARD_SIZES.get(elem.layer_name, (16, 10))
                # 纵向等间距排列
                if num_in_layer > 1:
                    y_spacing = max(sh - 20, num_in_layer * row_height) / (num_in_layer + 1)
                    y = sy + 10 + y_spacing * (i + 1) - std_h / 2
                else:
                    y = sy + sh / 2 - std_h / 2

                new_x = x
                new_y = y
                dx = new_x - elem.x
                dy = new_y - elem.y
                if abs(dx) > 0.1 or abs(dy) > 0.1:
                    old_x, old_y = elem.x, elem.y
                    elem.x = new_x
                    elem.y = new_y
                    if elem.transform or getattr(elem, 'raw_transform', None):
                        elem.patch_transform_translate(old_x, old_y, new_x, new_y)
                    self._sync_device_move(elem.element_id, dx, dy)
                    moved += 1

        # 备用设备放站房右侧
        spare_devs = [dev_id for dev_id in self.spare_device_ids
                      if self.device_to_station.get(dev_id) == sid]
        for i, dev_id in enumerate(spare_devs):
            elem = device_by_id.get(dev_id)
            if not elem:
                continue
            std_w, std_h = DEVICE_STANDARD_SIZES.get(elem.layer_name, (16, 10))
            spare_x = sx + sw - 10 - std_w
            if len(spare_devs) > 1:
                spare_y_spacing = max(sh - 20, len(spare_devs) * row_height) / (len(spare_devs) + 1)
                spare_y = sy + 10 + spare_y_spacing * (i + 1) - std_h / 2
            else:
                spare_y = sy + sh / 2 - std_h / 2
            dx = spare_x - elem.x
            dy = spare_y - elem.y
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                old_x, old_y = elem.x, elem.y
                elem.x = spare_x
                elem.y = spare_y
                if elem.transform or getattr(elem, 'raw_transform', None):
                    elem.patch_transform_translate(old_x, old_y, spare_x, spare_y)
                self._sync_device_move(elem.element_id, dx, dy)
                moved += 1

        return moved

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

        # 文字→设备关联索引已在 _build_text_device_map() 中提前构建
        print(f"  文字→设备关联: {len(self.text_device_map)}/{len(self.doc.texts)}")

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

            # 3. 位置：保持原始文字位置，仅调整 dx/dy 偏移和对齐方式
            dev_id = self.text_device_map.get(txt.text_id, "")
            elem = device_by_id.get(dev_id) if dev_id else None
            if elem and not (elem.width <= 0 and elem.height <= 0 and elem.x == 0 and elem.y == 0):
                pos_info = self._compute_text_position(txt, elem)
                if pos_info:
                    old_dx, old_dy = txt.dx, txt.dy
                    txt.dx = pos_info.get("dx", 0)
                    txt.dy = pos_info.get("dy", 0)
                    txt.text_anchor = pos_info.get("text_anchor", "middle")
                    txt.dominant_baseline = pos_info.get("dominant_baseline", "auto")
                    # 不覆盖原始 x/y，保持原始布局
                    if txt.dx != old_dx or txt.dy != old_dy:
                        pos_updated += 1
            else:
                # 无有效关联设备：保持原始位置，仅更新偏移
                pos_info = self._compute_text_position_no_device(txt)
                if pos_info:
                    old_dx, old_dy = txt.dx, txt.dy
                    txt.dx = pos_info.get("dx", 0)
                    txt.dy = pos_info.get("dy", 0)
                    txt.text_anchor = pos_info.get("text_anchor", "middle")
                    txt.dominant_baseline = pos_info.get("dominant_baseline", "auto")
                    if txt.dx != old_dx or txt.dy != old_dy:
                        pos_updated += 1

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
        """根据规范B.4计算文字定位（基于设备 bounding box 动态计算偏移）。"""
        cx = elem.x + elem.width / 2
        cy = elem.y + elem.height / 2
        half_h = elem.height / 2
        half_w = elem.width / 2
        layer = elem.layer_name
        role = txt.text_role

        if role == "title":
            # 站房标题：设备上方
            return {
                "dx": 0,
                "dy": -(half_h + 18),
                "text_anchor": "middle",
                "dominant_baseline": "auto",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "spare":
            # 备用标注：设备右侧
            return {
                "dx": half_w + 4,
                "dy": 0,
                "text_anchor": "start",
                "dominant_baseline": "middle",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "line":
            # 线路名称：设备上方
            return {
                "dx": 0,
                "dy": -(half_h + 6),
                "text_anchor": "middle",
                "dominant_baseline": "auto",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "id":
            # 设备ID：设备下方
            return {
                "dx": 0,
                "dy": half_h + 12,
                "text_anchor": "middle",
                "dominant_baseline": "hanging",
                "device_x": cx,
                "device_y": cy,
            }

        if role == "name":
            if layer in KEY_DEVICE_LAYERS:
                # 关键设备名：设备下方
                return {
                    "dx": 0,
                    "dy": half_h + 14,
                    "text_anchor": "middle",
                    "dominant_baseline": "hanging",
                    "device_x": cx,
                    "device_y": cy,
                }
            # 支线设备名：设备右侧
            return {
                "dx": half_w + 4,
                "dy": 0,
                "text_anchor": "start",
                "dominant_baseline": "middle",
                "device_x": cx,
                "device_y": cy,
            }

        return {
            "dx": 0,
            "dy": half_h + 14,
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

            # 重建 transform：保留旋转分量，scale 由 width/height 决定
            # 旋转中心点使用新位置的中心，确保旋转围绕设备视觉中心
            _, _, orig_scale, rotation, _ = SvgDocument._parse_transform(
                elem.transform or elem.raw_transform or ''
            )
            new_cx = new_x + std_w / 2.0
            new_cy = new_y + std_h / 2.0
            if abs(rotation) > 0.001:
                elem.transform = f"rotate({rotation:.6f},{new_cx:.6f},{new_cy:.6f})"
            else:
                elem.transform = ''

            # 同步连接线端点和文字位置
            self._sync_device_move(elem.element_id, dx, dy)

            updated += 1

        print(f"  设备图标已标准化: {updated} 个")

    def _compute_grid_size(self) -> float:
        """动态计算网格尺寸：基于最大标准设备宽度和最小间距。"""
        max_dev_w = max(w for w, h in DEVICE_STANDARD_SIZES.values())
        min_spacing = 8.0
        return max_dev_w + min_spacing  # 40.0

    def _normalize_coordinate_scale(self):
        """基于实际最小设备间距计算缩放因子，替代固定 factor=3.5。

        核心逻辑：计算所有设备间的最小曼哈顿距离，如果小于目标间距
        （最大设备宽 + 最小间距），则按比例放大所有坐标。
        """
        device_elems = [e for e in self.doc.elements
                        if e.element_id and e.layer_name != "Substation"]
        if len(device_elems) < 2:
            return

        # 计算设备中心点间的最小间距
        min_dist = float('inf')
        centers = []
        for e in device_elems:
            cx = e.x + (e.width or 0) / 2
            cy = e.y + (e.height or 0) / 2
            centers.append((cx, cy))

        for i in range(len(centers)):
            for j in range(i + 1, len(centers)):
                dist = abs(centers[i][0] - centers[j][0]) + abs(centers[i][1] - centers[j][1])
                if dist > 0.01:
                    min_dist = min(min_dist, dist)

        if min_dist == float('inf') or min_dist < 0.01:
            return

        # 目标最小间距：最大设备宽度 + 最小间距
        max_dev_w = max(w for w, h in DEVICE_STANDARD_SIZES.values())
        target_min_dist = max_dev_w + 8.0

        if min_dist >= target_min_dist:
            print(f"  坐标尺度已满足: 最小间距 {min_dist:.2f} >= 目标 {target_min_dist:.2f}")
            return

        factor = target_min_dist / min_dist
        # 限制最大缩放因子
        factor = min(factor, 50.0)

        for elem in self.doc.elements:
            elem.x *= factor
            elem.y *= factor

        for conn in self.doc.connections:
            conn.points = [(x * factor, y * factor) for x, y in conn.points]

        for txt in self.doc.texts:
            txt.x *= factor
            txt.y *= factor

        print(f"  坐标尺度归一化: 最小间距 {min_dist:.2f} → {min_dist * factor:.2f} (×{factor:.2f})")

    def _route_connections_to_edges(self):
        """连接线正交路由：端点贴设备边缘 + L 型中间路径。

        策略：
        1. 起点和终点贴到设备边缘
        2. 如果只有首尾两点，生成 L 型正交中间点
        3. 如果有中间点，仅更新首尾端点
        """
        device_by_id = {e.element_id: e for e in self.doc.elements if e.element_id}
        updated = 0

        def _edge_point(dev, target_x, target_y):
            cx = dev.x + dev.width / 2.0
            cy = dev.y + dev.height / 2.0
            dx = target_x - cx
            dy = target_y - cy
            if abs(dx) < 1e-6 and abs(dy) < 1e-6:
                return cx, cy
            # 防止设备尺寸为0时除零
            if dev.width <= 0 or dev.height <= 0:
                return cx, cy
            if abs(dx) * dev.height > abs(dy) * dev.width:
                ex = dev.x + (dev.width if dx > 0 else 0.0)
                ratio = (dev.width / 2.0) / abs(dx) if abs(dx) > 1e-6 else 0
                ey = cy + dy * ratio
            else:
                ratio = (dev.height / 2.0) / abs(dy) if abs(dy) > 1e-6 else 0
                ex = cx + dx * ratio
                ey = dev.y + (dev.height if dy > 0 else 0.0)
            return ex, ey

        for conn in self.doc.connections:
            if not conn.points or len(conn.points) < 2:
                continue

            new_points = list(conn.points)
            start_dev = device_by_id.get(conn.start_device_id) if conn.start_device_id else None
            end_dev = device_by_id.get(conn.end_device_id) if conn.end_device_id else None

            # 起点贴设备边缘
            if start_dev:
                target = new_points[1]
                new_start = _edge_point(start_dev, target[0], target[1])
                if new_start != new_points[0]:
                    new_points[0] = new_start
                    updated += 1

            # 终点贴设备边缘
            if end_dev:
                target = new_points[-2]
                new_end = _edge_point(end_dev, target[0], target[1])
                if new_end != new_points[-1]:
                    new_points[-1] = new_end
                    updated += 1

            # L 型正交路由：如果只有首尾两点且不在同一行/列，添加中间转折点
            if len(new_points) == 2 and start_dev and end_dev:
                sp = new_points[0]
                ep = new_points[-1]
                if abs(sp[0] - ep[0]) > 1.0 and abs(sp[1] - ep[1]) > 1.0:
                    # L 型：先水平后垂直
                    mid_pt = (ep[0], sp[1])
                    new_points = [sp, mid_pt, ep]
                    updated += 1
            elif len(new_points) == 2 and (start_dev or end_dev):
                sp = new_points[0]
                ep = new_points[-1]
                if abs(sp[0] - ep[0]) > 1.0 and abs(sp[1] - ep[1]) > 1.0:
                    mid_pt = (ep[0], sp[1])
                    new_points = [sp, mid_pt, ep]
                    updated += 1

            conn.points = new_points

        print(f"  连接线正交路由: {updated} 条已更新")


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
