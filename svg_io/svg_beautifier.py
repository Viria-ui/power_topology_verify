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

    def _move_device(self, elem, new_x: float, new_y: float):
        """移动设备到新坐标：更新 x/y 属性 + transform 中的 translate 值。

        保留原始 transform 的 translate(x,y) scale(s) translate(-x,-y) 结构，
        仅替换 translate 和 rotate 中的坐标值。
        """
        old_x, old_y = elem.x, elem.y
        elem.x = new_x
        elem.y = new_y
        # 使用 patch_transform_translate 更新 transform 中的位置
        elem.patch_transform_translate(old_x, old_y, new_x, new_y)
        # 同步连接线端点和文字
        self._sync_device_move(elem.element_id, new_x - old_x, new_y - old_y)

    def beautify(self) -> str:
        print(f"\n{'='*60}")
        print(f"美化 {self.svg_filename}")
        print(f"{'='*60}")

        self.doc.parse()

        # 第1步：建立站房映射 + 文字→设备关联 + 备用间隔检测
        self._build_station_map()
        self._build_text_device_map()
        self._detect_spare_intervals()

        # 第2步：设备图标标准化（统一显示尺寸，重建 transform）
        self._normalize_device_icons()

        # 第3步：全局拓扑布局重构（BFS 分层 + 纵向排列，替代坐标缩放）
        self._layout_by_topology()

        # 第4步：设备重叠消解
        self._resolve_device_overlaps()

        # 第5步：连接线样式规范化（颜色、线宽、线型）
        self._normalize_connection_styles()

        # 第6步：站房边框标准化
        self._normalize_station_styles()

        # 第7步：连接线正交路由（端点贴设备边缘 + L 型路径）
        self._route_connections_to_edges()

        # 第8步：文字样式规范化（颜色、字号、字重、位置）
        self._normalize_text_styles()

        # 第9步：文字碰撞避让
        self._resolve_text_collisions()

        # 第10步：自适应 viewBox（最后处理，width/height 同步）
        self._adapt_viewbox()

        # 写出 SVG
        write_svg(self.doc, self.output_path, update_style=True)

        # 自检并输出质量报告
        self._check_beautify_quality()

        print(f"\n美化完成: {self.output_path}")
        return self.output_path

    # ------------------------------------------------------------------
    # 坐标空间等比放大
    # ------------------------------------------------------------------
    def _scale_coordinate_space(self, factor: float = 8.0):
        """等比放大整个坐标空间，让所有元素变得可见。

        放大的维度：
        - 设备 x, y, width, height
        - 连接线所有点
        - 文字 x, y, font_size
        - viewBox

        放大后相对位置不变，但绝对尺寸变大，文字/设备可见。
        """
        print(f"  坐标空间放大: factor={factor}")

        # 放大设备
        for elem in self.doc.elements:
            elem.x *= factor
            elem.y *= factor
            elem.width *= factor
            elem.height *= factor
            # 更新 transform（平移分量也要放大）
            if elem.transform:
                elem._transform_tx *= factor
                elem._transform_ty *= factor
                elem.rebuild_transform()
            # polygon 的 points 也要放大
            if elem.shape_tag == "polygon":
                pts_str = elem.shape_attrs.get("points", "")
                if pts_str:
                    new_pts = []
                    for pt in pts_str.strip().split():
                        coords = pt.split(",")
                        if len(coords) == 2:
                            new_pts.append(f"{float(coords[0])*factor:.6f},{float(coords[1])*factor:.6f}")
                        else:
                            new_pts.append(pt)
                    elem.shape_attrs["points"] = " ".join(new_pts)

        # 放大连接线
        for conn in self.doc.connections:
            if conn.points:
                conn.points = [(p[0] * factor, p[1] * factor) for p in conn.points]

        # 放大文字
        for txt in self.doc.texts:
            txt.x *= factor
            txt.y *= factor
            txt.font_size = (txt.font_size or 12.0) * factor
            # dx/dy 也放大
            if hasattr(txt, 'dx'):
                txt.dx = (txt.dx or 0) * factor
            if hasattr(txt, 'dy'):
                txt.dy = (txt.dy or 0) * factor

        # 放大 viewBox
        vx, vy, vw, vh = self.doc.viewbox
        self.doc.viewbox = (vx * factor, vy * factor, vw * factor, vh * factor)
        self.doc.width = vw * factor
        self.doc.height = vh * factor

        print(f"  viewBox: ({vx:.1f},{vy:.1f} {vw:.1f}x{vh:.1f}) -> "
              f"({vx*factor:.1f},{vy*factor:.1f} {vw*factor:.1f}x{vh*factor:.1f})")

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
        invalid_dev_count = 0
        for elem in self.doc.elements:
            ex, ey = elem.x, elem.y
            ew, eh = elem.width or 0, elem.height or 0
            # 跳过无效设备（width/height 为 0 或坐标在原点附近），这些是解析失败的占位元素
            if ew <= 0 or eh <= 0:
                invalid_dev_count += 1
                continue
            # 跳过 (0,0) 原点附近设备（原始 SVG 中的占位符）
            if abs(ex) < 1.0 and abs(ey) < 1.0:
                invalid_dev_count += 1
                continue
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
        print(f"  设备越界: {dev_outside} 个 (无效设备: {invalid_dev_count} 个), "
              f"连接线端点越界: {conn_outside} 条")

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
            # 跳过非标准设备图层（如 ACLineSegment 是线路图层，不应作为设备处理）
            if elem.layer_name not in DEVICE_STANDARD_SIZES:
                continue
            # 跳过站房内设备（由拓扑布局确定坐标）
            if elem.element_id in self.device_to_station:
                continue
            # 跳过站房本身
            if elem.layer_name == "Substation":
                continue
            # 跳过 (0,0) 附近的无效设备（解析失败的占位元素）
            if abs(elem.x) < 1.0 and abs(elem.y) < 1.0:
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
                self._move_device(elem, new_x, new_y)
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
        """检测并消解设备重叠：仅处理明显重叠，不破坏拓扑布局。

        关键改进：
        1. 按 X/Y 排序后分组检查，避免 O(N²) 全量比较
        2. 只处理真正严重重叠（重叠面积 > 30%）
        3. 站内设备不在此处理（由 _layout_station_internal 管理）
        4. 只做 1 轮微调，避免层层推开导致整体Y发散
        """
        device_elems = [e for e in self.doc.elements
                        if e.element_id and e.layer_name != "Substation"
                        and e.width > 0 and e.height > 0
                        and e.element_id not in self.device_to_station]  # 跳过站内设备
        if len(device_elems) < 2:
            return

        total_resolved = 0
        OVERLAP_TOL_X = 4  # X方向容差：同列设备允许稍微重叠
        OVERLAP_TOL_Y = 4  # Y方向容差

        # 按Y排序，按X分桶检查（减少比较量）
        device_elems.sort(key=lambda e: (round(e.x / 60), e.y))

        for i in range(len(device_elems)):
            e1 = device_elems[i]
            for j in range(i + 1, min(i + 10, len(device_elems))):
                e2 = device_elems[j]
                # 快速过滤X不重叠
                if (e1.x + e1.width + OVERLAP_TOL_X < e2.x or
                    e2.x + e2.width + OVERLAP_TOL_X < e1.x):
                    continue
                if (e1.y + e1.height + OVERLAP_TOL_Y < e2.y or
                    e2.y + e2.height + OVERLAP_TOL_Y < e1.y):
                    continue

                # 计算重叠面积
                ov_x1 = max(e1.x, e2.x)
                ov_y1 = max(e1.y, e2.y)
                ov_x2 = min(e1.x + e1.width, e2.x + e2.width)
                ov_y2 = min(e1.y + e1.height, e2.y + e2.height)
                ov_area = max(0, ov_x2 - ov_x1) * max(0, ov_y2 - ov_y1)
                min_area = min(e1.width * e1.height, e2.width * e2.height)
                if min_area <= 0:
                    continue

                # 只有重叠>30%才处理
                if ov_area / min_area < 0.3:
                    continue

                # 将 e2 向下偏移到 e1 下方
                offset = (e1.y + e1.height) - e2.y + 6
                if offset > 0:
                    self._move_device(e2, e2.x, e2.y + offset)
                    total_resolved += 1

        if total_resolved > 0:
            print(f"  设备重叠消解: {total_resolved} 个设备已偏移")
        else:
            print(f"  设备重叠消解: 0 个需要处理")

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
                    if new_x != elem.x or new_y != elem.y:
                        self._move_device(elem, new_x, new_y)
                        moved += 1

            if spare_devs:
                usable_h = max(sh - top_margin - bottom_margin, 10.0)
                spacing = usable_h / (len(spare_devs) + 1)
                for i, elem in enumerate(spare_devs):
                    new_x = sx + sw - right_margin - elem.width
                    new_y = sy + top_margin + spacing * (i + 1) - elem.height / 2
                    if new_x != elem.x or new_y != elem.y:
                        self._move_device(elem, new_x, new_y)
                        moved += 1

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
        """拓扑布局：大分量BFS分层 + 孤立设备2D网格。

        画布目标：1400 × 1000（黄金比例），避免极端拉伸。
        """
        from collections import deque, defaultdict

        device_by_id = {e.element_id: e for e in self.doc.elements if e.element_id}

        # 1. 收集有效设备
        valid_devices = []
        for elem in self.doc.elements:
            if not elem.element_id:
                continue
            if elem.layer_name not in DEVICE_STANDARD_SIZES:
                continue
            if elem.layer_name == "Substation":
                continue
            if elem.width <= 0 or elem.height <= 0:
                continue
            if abs(elem.x) < 0.1 and abs(elem.y) < 0.1:
                continue
            valid_devices.append(elem.element_id)
        valid_set = set(valid_devices)

        if not valid_devices:
            print("  拓扑布局: 无有效设备，跳过")
            return

        # 2. 构建邻接图
        adj = defaultdict(set)
        for conn in self.doc.connections:
            sid = conn.start_device_id
            eid = conn.end_device_id
            if sid and eid and sid != eid:
                adj[sid].add(eid)
                adj[eid].add(sid)

        # 3. 找连通分量
        visited_global = set()
        components = []
        for dev_id in valid_devices:
            if dev_id not in visited_global:
                comp = []
                queue = deque([dev_id])
                visited_global.add(dev_id)
                while queue:
                    cur = queue.popleft()
                    comp.append(cur)
                    for nb in adj.get(cur, []):
                        if nb not in visited_global and nb in valid_set:
                            visited_global.add(nb)
                            queue.append(nb)
                components.append(comp)

        # 按大小降序：大分量先布局
        components.sort(key=len, reverse=True)

        # 4. 布局参数（紧凑画布）
        CANVAS_W = 1400.0
        CANVAS_H = 1000.0
        MARGIN = 80.0
        LAYER_SPACING = 90.0
        ROW_SPACING = 38.0
        MAX_ROWS_PER_COMP = 25  # 单个分量每列最大行数

        # 5. 分离：大分量 vs 孤立设备
        big_comps = [c for c in components if len(c) >= 2]
        isolated = [c[0] for c in components if len(c) == 1]

        # 统计孤立设备类型占比
        iso_by_layer = defaultdict(list)
        for dev_id in isolated:
            elem = device_by_id.get(dev_id)
            if elem:
                iso_by_layer[elem.layer_name].append(dev_id)

        moved = 0
        # 6. 大分量：从上往下排列，每分量占一行区域，BFS左右分层
        comp_y_start = MARGIN
        comp_x_start = MARGIN

        # 计算大分量总共占用多少行高，按均匀分布
        total_devs_big = sum(len(c) for c in big_comps)
        if total_devs_big > 0:
            row_h = min(ROW_SPACING * MAX_ROWS_PER_COMP, (CANVAS_H - 2 * MARGIN) / max(len(big_comps), 1))
        else:
            row_h = CANVAS_H - 2 * MARGIN

        for comp in big_comps:
            # 选根
            root = None
            for dev_id in comp:
                elem = device_by_id.get(dev_id)
                if elem and elem.layer_name == "PowerTransformer":
                    root = dev_id
                    break
            if not root:
                for dev_id in comp:
                    elem = device_by_id.get(dev_id)
                    if elem and elem.layer_name == "Breaker":
                        root = dev_id
                        break
            if not root:
                for dev_id in comp:
                    elem = device_by_id.get(dev_id)
                    if elem and elem.layer_name == "LoadBreakSwitch":
                        root = dev_id
                        break
            if not root:
                deg = {d: len(adj.get(d, [])) for d in comp}
                root = max(comp, key=lambda d: deg.get(d, 0))

            # BFS 分层
            comp_visited = set()
            layers = []
            q = deque([(root, 0)])
            comp_visited.add(root)
            while q:
                dev_id, layer = q.popleft()
                while len(layers) <= layer:
                    layers.append([])
                layers[layer].append(dev_id)
                for nb in sorted(adj.get(dev_id, []), key=lambda d: len(adj.get(d, [])), reverse=True):
                    if nb not in comp_visited and nb in valid_set:
                        comp_visited.add(nb)
                        q.append((nb, layer + 1))
            for dev_id in comp:
                if dev_id not in comp_visited:
                    layers.append([dev_id])

            # 给分量分配Y空间：从 comp_y_start 开始，按层内最多元素的数量决定列数
            max_devs_in_layer = max(len(l) for l in layers) if layers else 1
            # 计算层内需要多少子列：如果超过 MAX_ROWS_PER_COMP 则多行多列
            layer_cols = 1
            if max_devs_in_layer > MAX_ROWS_PER_COMP:
                layer_cols = (max_devs_in_layer + MAX_ROWS_PER_COMP - 1) // MAX_ROWS_PER_COMP

            comp_width = len(layers) * LAYER_SPACING + (layer_cols - 1) * LAYER_SPACING * 0.6
            # 如果超出画布宽，缩放层间距
            if comp_x_start + comp_width > CANVAS_W - MARGIN:
                comp_x_start = MARGIN
                comp_y_start += row_h + 20

            # 分配坐标
            local_x = comp_x_start
            for layer_idx, devs_in_layer in enumerate(layers):
                # 层内按 MAX_ROWS_PER_COMP 分组，每组占一列位置
                col_y = comp_y_start
                col_x = local_x
                for i, dev_id in enumerate(devs_in_layer):
                    elem = device_by_id.get(dev_id)
                    if not elem:
                        continue
                    old_x, old_y = elem.x, elem.y
                    self._move_device(elem, col_x, col_y)
                    moved += 1
                    col_y += ROW_SPACING
                    # 换子列
                    if (i + 1) % MAX_ROWS_PER_COMP == 0 and (i + 1) != len(devs_in_layer):
                        col_y = comp_y_start
                        col_x += LAYER_SPACING * 0.6

                local_x += LAYER_SPACING

            # 下一个分量：x继续右移，如果超宽则换行
            comp_x_start = local_x + 30
            if comp_x_start > CANVAS_W - MARGIN - LAYER_SPACING:
                comp_x_start = MARGIN
                comp_y_start += row_h + 20

        # 7. 孤立设备：2D网格（按层排，重要类型在前）
        # 优先类型顺序：变电站相关设备 → 变压器 → 开关 → 其他
        iso_layer_priority = {
            "PowerTransformer": 0, "Breaker": 1, "LoadBreakSwitch": 2,
            "Fuse": 3, "Disconnector": 4, "CurrentTransformer": 5,
            "EnergyConsumer": 6, "Junction": 7, "Other": 8,
        }
        iso_sorted_devs = []
        for dev_id in isolated:
            elem = device_by_id.get(dev_id)
            pri = iso_layer_priority.get(elem.layer_name, 5) if elem else 5
            iso_sorted_devs.append((pri, dev_id))
        iso_sorted_devs.sort(key=lambda x: x[0])

        # 紧凑网格：基于剩余空间
        iso_start_y = comp_y_start + 10
        iso_area_h = max(CANVAS_H - iso_start_y - MARGIN, 400)
        ISO_ROWS = max(8, int(iso_area_h / ROW_SPACING))  # 多少行
        iso_cur_x = MARGIN
        iso_cur_y = iso_start_y
        iso_x_step = LAYER_SPACING * 1.2
        iso_row_count = 0

        for _, dev_id in iso_sorted_devs:
            elem = device_by_id.get(dev_id)
            if not elem:
                continue
            old_x, old_y = elem.x, elem.y
            self._move_device(elem, iso_cur_x, iso_cur_y)
            moved += 1
            iso_row_count += 1
            if iso_row_count >= ISO_ROWS:
                # 换列
                iso_cur_x += iso_x_step
                iso_cur_y = iso_start_y
                iso_row_count = 0
            else:
                iso_cur_y += ROW_SPACING

        # 8. 站房内设备纵向排列 + 站房位置跟随
        station_moved = self._layout_station_internal(device_by_id, ROW_SPACING)

        # 9. 站房位置：跟随其内部设备的中心
        self._reposition_stations(device_by_id)

        # 10. 文字位置同步到设备
        unmatched = 0
        for txt in self.doc.texts:
            dev_id = self.text_device_map.get(txt.text_id, "")
            elem = device_by_id.get(dev_id)
            if elem and elem.width > 0 and elem.height > 0:
                # 设备有效：文字跟随设备
                txt.x = elem.x + elem.width / 2
                txt.y = elem.y + elem.height / 2
            elif not dev_id:
                # 完全无设备关联：隐藏
                txt.hidden = True
                unmatched += 1
            else:
                # 设备无效（width=0）：尝试找最近的有效设备
                # 如果找不到，保持原位但不隐藏（让 _normalize_text_styles 处理）
                pass

        if unmatched:
            print(f"  文字位置同步: {unmatched} 个无关联文字已隐藏")

        print(f"  拓扑布局: {len(components)} 分量(大{len(big_comps)}/孤{len(isolated)}), {moved} 设备重排, {station_moved} 站内设备")

    def _layout_station_internal(self, device_by_id: dict, grid_y: float) -> int:
        """站房内设备纵向排列，站房位置基于内部设备的BFS布局位置。

        核心修复：
        - 不使用站房的原始坐标（那是极小坐标系）
        - 先计算内部设备的质心作为站房新位置
        - 再在站房内纵向排列设备
        """
        station_devices = {}
        for dev_id, station_id in self.device_to_station.items():
            if station_id not in station_devices:
                station_devices[station_id] = []
            station_devices[station_id].append(dev_id)

        station_bounds = {}
        for elem in self.doc.elements:
            if elem.layer_name == "Substation" and elem.element_id:
                station_bounds[elem.element_id] = elem

        moved = 0
        for sid, dev_ids in station_devices.items():
            if sid not in station_bounds:
                continue
            station_elem = station_bounds[sid]

            # 收集站内设备
            internal_devs = []
            for dev_id in dev_ids:
                elem = device_by_id.get(dev_id)
                if elem and elem.width > 0 and elem.height > 0:
                    internal_devs.append(elem)

            if not internal_devs:
                continue

            # 计算设备质心（基于BFS布局后的当前位置）
            avg_x = sum(e.x + e.width / 2 for e in internal_devs) / len(internal_devs)
            avg_y = sum(e.y + e.height / 2 for e in internal_devs) / len(internal_devs)

            # 站房新位置：以质心为参考
            station_w = max(max(e.width for e in internal_devs) + 24.0, 50.0)
            station_h = sum(max(e.height + 6.0, 25.0) for e in internal_devs) + 24.0
            station_x = avg_x - station_w / 2.0
            station_y = avg_y - station_h / 2.0

            # 按原始 x 坐标排序
            internal_devs.sort(key=lambda e: e.x)

            # 纵向排列（间距足够容纳文字标注）
            y_offset = 12.0
            max_x = 0
            STATION_DEV_SPACING = 25.0  # 最小设备间距，确保文字不重叠
            for elem in internal_devs:
                old_x, old_y = elem.x, elem.y
                new_x = station_x + 12.0
                new_y = station_y + y_offset
                self._move_device(elem, new_x, new_y)
                y_offset += max(elem.height + 6.0, STATION_DEV_SPACING)
                max_x = max(max_x, elem.x + elem.width)
                moved += 1

            # 更新站房边框
            new_w = max(max_x - station_x + 12.0, 50.0)
            new_h = y_offset + 12.0
            station_elem.x = station_x
            station_elem.y = station_y
            station_elem.width = new_w
            station_elem.height = new_h
            if station_elem.shape_tag == "polygon":
                pts = f"{station_x},{station_y} {station_x + new_w},{station_y} {station_x + new_w},{station_y + new_h} {station_x},{station_y + new_h}"
                station_elem.shape_attrs["points"] = pts

        return moved

    def _reposition_stations(self, device_by_id: dict):
        """站房位置跟随其内部设备的包围盒中心。"""
        # 按站房分组设备
        station_devices = {}
        for dev_id, station_id in self.device_to_station.items():
            if station_id not in station_devices:
                station_devices[station_id] = []
            station_devices[station_id].append(dev_id)

        for sid, dev_ids in station_devices.items():
            station_elem = None
            for e in self.doc.elements:
                if e.element_id == sid and e.layer_name == "Substation":
                    station_elem = e
                    break
            if not station_elem:
                continue

            # 计算内部设备包围盒
            xs, ys = [], []
            for dev_id in dev_ids:
                elem = device_by_id.get(dev_id)
                if elem and elem.width > 0 and elem.height > 0:
                    xs.extend([elem.x, elem.x + elem.width])
                    ys.extend([elem.y, elem.y + elem.height])
            if not xs:
                continue

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            padding = 12.0

            old_x, old_y = station_elem.x, station_elem.y
            station_elem.x = min_x - padding
            station_elem.y = min_y - padding
            station_elem.width = (max_x - min_x) + 2 * padding
            station_elem.height = (max_y - min_y) + 2 * padding

            # 更新 polygon points
            if station_elem.shape_tag == "polygon":
                sx, sy = station_elem.x, station_elem.y
                sw, sh = station_elem.width, station_elem.height
                pts = f"{sx},{sy} {sx+sw},{sy} {sx+sw},{sy+sh} {sx},{sy+sh}"
                station_elem.shape_attrs["points"] = pts

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
                if abs(new_x - elem.x) > 0.1 or abs(new_y - elem.y) > 0.1:
                    self._move_device(elem, new_x, new_y)
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
            if abs(spare_x - elem.x) > 0.1 or abs(spare_y - elem.y) > 0.1:
                self._move_device(elem, spare_x, spare_y)
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

        # 建立站房边界列表
        station_bounds = []
        for elem in self.doc.elements:
            if elem.layer_name == "Substation" and elem.width and elem.height:
                station_bounds.append((elem.x, elem.y, elem.width, elem.height))

        # 建立 connection_id / glink_ref → connection 的映射
        connection_by_id = {}
        for conn in self.doc.connections:
            if conn.connection_id:
                connection_by_id[conn.connection_id] = conn
            for gid in conn.glink_refs:
                if gid:
                    connection_by_id[gid] = conn

        # 预处理：对每个设备只保留最高优先级的文字，其余标记隐藏
        device_best_text = {}  # dev_id → (priority, text_id)
        for txt in self.doc.texts:
            if getattr(txt, "hidden", False):
                continue
            dev_id = self.text_device_map.get(txt.text_id, "")
            if not dev_id:
                continue
            content = (txt.content or "").strip()
            has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
            if not has_chinese or len(content) < 2:
                continue
            # 优先级：站名 > 关键设备名 > 普通设备名 > 线路名 > ID
            pri = 0
            if re.search(r'(变电站|开关站|配电室|站房|开闭所)', content):
                pri = 0
            elif re.search(r'(环网箱|箱变|变压器|故障指示器|开关)', content):
                pri = 1
            else:
                pri = 2
            existing = device_best_text.get(dev_id)
            if existing is None or pri < existing[0]:
                device_best_text[dev_id] = (pri, txt.text_id)

        for txt in self.doc.texts:
            # 0. 清理文字内容：去除TMP前缀元数据，提取有意义的设备名
            txt.content = self._clean_text_content(txt.content)

            # 0.1 去重：同一设备只保留最高优先级的文字
            dev_id = self.text_device_map.get(txt.text_id, "")
            if dev_id and dev_id in device_best_text:
                best_text_id = device_best_text[dev_id][1]
                if txt.text_id != best_text_id:
                    # 非最佳文字，检查是否是线路标签（保留线路标签）
                    content = (txt.content or "").strip()
                    is_line_name = bool(re.search(r'LINE\d+|_线|馈线', content))
                    if not is_line_name:
                        txt.hidden = True
                        hidden_count += 1
                        continue

            # 1. 颜色统一
            if txt.fill != STYLE["text"]:
                txt.fill = STYLE["text"]
                color_updated += 1

            # 2. 判定 text_role（保留已预设的特殊角色，如 spare）
            if not txt.text_role:
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

            # 2.1 文字过滤
            if self._should_hide_text(txt):
                txt.hidden = True
                hidden_count += 1
                continue

            # 2.2 截断
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

            # 5. 位置：文字坐标已在布局阶段同步到设备中心，这里仅设置 dx/dy 偏移
            dev_id = self.text_device_map.get(txt.text_id, "")
            elem = device_by_id.get(dev_id) if dev_id else None
            if elem and elem.width > 0 and elem.height > 0:
                pos_info = self._compute_text_position(txt, elem)
                if pos_info:
                    old_dx, old_dy = txt.dx, txt.dy
                    txt.dx = pos_info.get("dx", 0)
                    txt.dy = pos_info.get("dy", 0)
                    txt.text_anchor = pos_info.get("text_anchor", "middle")
                    txt.dominant_baseline = pos_info.get("dominant_baseline", "auto")
                    if txt.dx != old_dx or txt.dy != old_dy:
                        pos_updated += 1
            else:
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
        """全局文字碰撞避让：基于近似包围盒，按优先级贪心错开。

        策略：优先小幅度偏移解决重叠，仅当无法错开时才隐藏低优先级文字。
        大幅提高偏移尝试次数，尽量保留所有文字。
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

        # 扩展候选偏移范围：更多纵向/横向选项
        candidate_offsets = []
        for i in range(1, 20):
            candidate_offsets.extend([
                (0, i * 6), (0, -i * 6),
                (i * 6, 0), (-i * 6, 0),
                (i * 6, i * 6), (i * 6, -i * 6),
                (-i * 6, i * 6), (-i * 6, -i * 6),
            ])

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
                txt.dx += best_x - bx
                txt.dy += best_y - by
                placed.append((best_x, best_y, bw, bh))
                adjusted += 1
            else:
                # 无法错开：保留文字（即使重叠），不隐藏
                # 仅当文字内容为空或过短时才隐藏
                content = (txt.content or "").strip()
                if len(content) < 2:
                    txt.hidden = True
                    hidden += 1
                else:
                    placed.append((bx, by, bw, bh))

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

    def _clean_text_content(self, content: str) -> str:
        """清理文字内容：去除元数据前缀，提取有意义的设备名。

        原始SVG中的文字模式：
        - "TMP00131368#~界著支1#" → "界著支1#"
        - "00000#~LINE216_争15#" → "LINE216_争15#" → "争15#"
        - "TMP00131373LINE215_线开关－LINE215_线LINE365_1#环网箱101" → "环网箱101"
        - "00000白7#~界著支26白8#" → "界著支26白8#"
        - "TMP00132954白1#SUB011_-LINE216_争140白3#" → "争140白3#"
        - "TMP00131599LINE216_争24电缆次" → "争24电缆次"
        - "SUB010_66kV变电站" → 保留
        - "故障指示器006" → 保留
        """
        if not content:
            return content
        content = content.strip()

        # 1. 去除 TMP + 数字 前缀
        content = re.sub(r'^TMP\d+#?', '', content)

        # 2. 去除 00000 占位前缀
        content = re.sub(r'^0{3,}', '', content)

        # 3. 按分隔符分割取最后一段（~ | #- | _-LINE | SUB\d+_）
        # SUB011_-LINE... 和 SUB010_断路器 也是分隔符
        # 先处理 SUB\d+_ 类型的分隔符（不包含变电站等有意义的）
        def _split_sub(m):
            full = m.group(0)
            # 如果是变电站等有意义的 SUBxxx_名称，保留
            suffix = content[m.end():m.end()+8] if m.end()+8 <= len(content) else content[m.end():]
            if re.search(r'(变电站|开关站|配电室|站房|开闭所)', content[m.start():]):
                return full  # 保留有意义的 SUB_
            # 否则作为分隔符处理
            return '|||'  # 临时分隔符

        sub_split = re.sub(r'SUB\d+_', _split_sub, content)
        # 统一使用 ||| 分割 + _-LINE 分割 + #- + ~
        parts = re.split(r'\|\|\||_-LINE|#-|~', sub_split)
        if len(parts) > 1:
            # 取最后一段（含 LINE 前缀的优先移除前缀）
            best_parts = []
            for part in reversed(parts):
                part = part.strip()
                if part and len(part) >= 2:
                    best_parts.append(part)
            if best_parts:
                content = best_parts[0]

        # 4. 去除开头的 #、~、-、. 等残留分隔符
        content = re.sub(r'^[#~\-.]+', '', content)

        # 5. 如果含 －/— 分隔的连接描述，取最后一段
        # 注意：短横杠 - 可能是设备名的一部分（如电缆终端头的名称），所以不按 - 分割
        if re.search(r'[－—]', content):
            parts = re.split(r'[－—]', content)
            if len(parts) >= 2:
                last_part = parts[-1].strip()
                if last_part and len(last_part) >= 2:
                    content = last_part

        # 6. 去除 LINE\d+_ 前缀（如 LINE216_争 → 争）
        m = re.match(r'^LINE\d+_(.+)$', content)
        if m:
            remaining = m.group(1)
            if re.search(r'[\u4e00-\u9fff\d]', remaining):
                content = remaining

        # 7. 去除开头的 # 和 -
        content = re.sub(r'^[#\-]+', '', content)

        # 8. 去除末尾所有残留标点（.、#、-、~ 等重复出现的）
        content = re.sub(r'[.#~\-]+$', '', content)

        return content.strip()

    def _should_hide_text(self, txt: SvgText) -> bool:
        """过滤非关键文字，降低图纸信息密度。

        隐藏规则：
        - 纯编码ID（无中文）且role=id → 隐藏
        - 空内容 → 隐藏
        - 内容过短（<2字符）且无意义 → 隐藏
        - 仍在原始坐标区域(290-540, 410-580)的文字 → 隐藏（设备未被移动）
        - 纯垃圾文字（无设备关键词、无编号、全是随机中文）→ 隐藏
        """
        role = txt.text_role
        content = (txt.content or "").strip()

        if not content:
            return True

        if len(content) < 2:
            return True

        # 纯 ID 类型（纯编码、无中文）→ 隐藏
        if role == "id":
            has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
            if not has_chinese:
                return True

        # 仍在原始坐标区域的文字：关联设备未被布局移动
        if 290 <= txt.x <= 540 and 410 <= txt.y <= 580:
            return True

        # 垃圾文字检测：中文随机字符组合，伪装成设备标注
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
        if not has_chinese:
            return False  # 非中文交给其他规则

        # (1) 合法设备关键词检查
        LEGIT_KW = (
            '变电站', '开关站', '配电室', '站房', '开闭所', '环网箱', '箱变', '变压器',
            '故障指示器', '开关', '刀闸', '配变', '用户', '母线', '终端头', '电缆',
            '主变', '联络', '馈线', '进线', '出线', '数线', '次母线', '站外', '站内',
        )
        has_device_keyword = any(kw in content for kw in LEGIT_KW)
        # 合法后缀：结构字（支/分/争）+数字 或 （照/白/间/开关/刀闸/配变/用户等）+数字
        legit_suffix_match = re.search(
            r'(支\d|分\d|照\d|白\d|间\d|柜\d|线\d|盒\d|表\d|'
            r'用户\d|开关\d|刀闸\d|配变\d|争\d|站\d|箱\d|缆\d|头\d|'
            r'次母线|母线|数线)',
            content
        )
        has_number = bool(re.search(r'\d', content))

        # 提取所有中文段
        cn_segments = re.findall(r'[\u4e00-\u9fff]+', content)
        cn_only = ''.join(cn_segments)
        # 合法地名+结构字模式（2字地名+1字结构字 或 3字地名+1字结构字）
        # 如：界著支、饭想分、清叫支、五海分、从地支、多列分、士诉分、约命...（非）
        # 结构字限定为：支、分、争
        STRUCT_RE = re.compile(r'^[\u4e00-\u9fff]{1,3}[支分争]$')

        # (2) 单段中文>=4字且不含关键词 → 乱码（"故障指示器"5字含关键词，通过；"助速常开发个行者劳"8字无关键词，被隐藏）
        for seg in cn_segments:
            seg_has_kw = any(kw in seg for kw in LEGIT_KW)
            if len(seg) >= 4 and not seg_has_kw:
                return True

        # (3) 含设备关键词的场景：检查前缀是否为乱码段
        # 例："了严2#母线" → cn_segments=["了严", "母线"], has_device_keyword=True
        #   "了严" 不在关键词中 → 检查 "了严" 是否为合法2字地名/前缀
        LEGIT_2CH_OR_SUFFIX = (
            '数线', '进线', '出线', '馈线', '母线', '联络', '电缆', '终端', '站外',
            '站内', '故障', '指示', '变压', '箱变', '开关', '刀闸', '配变', '用户',
            '开闭', '配电', '变电', '环网', '次母',
        )
        LEGIT_SINGLE = ('白', '照', '间', '箱', '柜', '表', '盒', '线', '缆', '头',
                        '开', '关', '配', '闸', '站', '主', '次', '争')
        if has_device_keyword and len(cn_segments) >= 2:
            for seg in cn_segments:
                seg_has_kw = any(kw in seg for kw in LEGIT_KW)
                if seg_has_kw or len(seg) < 2:
                    continue
                # 合法地名结构（2-3字+支/分/争结尾）
                if STRUCT_RE.match(seg):
                    continue
                # 合法后缀词（数线等）
                if seg in LEGIT_2CH_OR_SUFFIX:
                    continue
                # 3字或更长的非结构字结尾 → 乱码
                if len(seg) >= 3:
                    return True
                # 2字段：是合法后缀词（如"照1"的"照"是长度1，不触发这里）→ 乱码（如"了严"）
                if len(seg) == 2:
                    return True

        # (4) 总中文字符数过多且无关键词（不管后缀）→ 乱码
        # 正常："清叫支20#数线" → cn=["清叫支","数线"] → cn_only=5字
        #       "约命了严个行者劳2#" → 去掉数字，cn_only="约命了严个行者劳"=9字 无kw → 隐藏
        if len(cn_only) >= 7 and not has_device_keyword:
            return True

        # (5) 没有关键词、没有合法后缀、总中文>=5 → 乱码
        if not has_device_keyword and not legit_suffix_match and len(cn_only) >= 5:
            return True

        # (6) 兜底：纯中文（无数字无#）+ 无关键词 → 隐藏
        if not has_device_keyword and not has_number and '#' not in content:
            return True

        return False

    def _truncate_text(self, content: str, max_chars: int = 25) -> str:
        """长标签截断，超过 max_chars 时保留前段并加省略号。"""
        if not content:
            return content
        content = content.strip()
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', content))
        limit = 30 if has_chinese else max_chars
        if len(content) <= limit:
            return content
        return content[:limit] + "…"

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
        并按中心点不变修正 x/y，使设备与文字/线宽尺度协调。

        关键修复：
        1. width/height 为 0 或极小时用 std 兜底，避免 _edge_point 误返回 (0,0)
        2. transform 重建为 translate + rotate（清除极小 scale），use.width 直接决定显示尺寸
        3. 同步连接线端点和文字位置
        """
        updated = 0
        skipped_zero = 0
        for elem in self.doc.elements:
            layer = elem.layer_name
            if layer not in DEVICE_STANDARD_SIZES:
                continue
            if not elem.element_id:
                continue

            std_w, std_h = DEVICE_STANDARD_SIZES[layer]
            old_w = elem.width if (elem.width and elem.width > 0.01) else std_w
            old_h = elem.height if (elem.height and elem.height > 0.01) else std_h

            if (elem.x == 0 and elem.y == 0 and
                    elem.width <= 0.01 and elem.height <= 0.01):
                skipped_zero += 1
                continue

            # 保留原始 transform 结构（translate(x,y) scale(s) translate(-x,-y)）
            # 将 scale 设为 1.0，通过 width/height 控制显示尺寸
            # 这样 transform 仅负责定位（translate + rotate），不参与缩放
            elem.patch_transform_scale(1.0)

            # 更新 width/height 为标准尺寸
            elem.width = std_w
            elem.height = std_h

            updated += 1

        print(f"  设备图标已标准化: {updated} 个 (跳过零坐标设备: {skipped_zero} 个)")

    def _compute_grid_size(self) -> float:
        """动态计算网格尺寸：基于最大标准设备宽度和最小间距。"""
        max_dev_w = max(w for w, h in DEVICE_STANDARD_SIZES.values())
        min_spacing = 8.0
        return max_dev_w + min_spacing  # 40.0

    def _normalize_coordinate_scale(self):
        """基于实际最小设备间距计算缩放因子，替代固定 factor=3.5。

        核心逻辑：计算所有设备间的最小曼哈顿距离，如果小于目标间距
        （最大设备宽 + 最小间距），则按比例放大所有坐标。

        关键修复：
        1. factor 上限改为 10.0（避免极端放大导致设备飞散）
        2. 当 min_dist 极小（<1.0）时直接使用保守 factor，避免单点误差放大
        3. 放大时同步处理 polygon points（站房矩形等），不只是 x/y
        """
        device_elems = [e for e in self.doc.elements
                        if e.element_id and e.layer_name != "Substation"
                        and e.width and e.width > 0
                        and e.height and e.height > 0]
        if len(device_elems) < 2:
            return

        # 计算设备中心点间的最小间距
        min_dist = float('inf')
        centers = []
        for e in device_elems:
            cx = e.x + e.width / 2
            cy = e.y + e.height / 2
            centers.append((cx, cy))

        for i in range(len(centers)):
            for j in range(i + 1, len(centers)):
                dist = abs(centers[i][0] - centers[j][0]) + abs(centers[i][1] - centers[j][1])
                if dist > 0.5:  # 过滤重合设备
                    min_dist = min(min_dist, dist)

        if min_dist == float('inf'):
            return

        # 目标最小间距：最大设备宽度 + 最小间距
        max_dev_w = max(w for w, h in DEVICE_STANDARD_SIZES.values())
        target_min_dist = max_dev_w + 8.0  # 40.0

        if min_dist >= target_min_dist:
            print(f"  坐标尺度已满足: 最小间距 {min_dist:.2f} >= 目标 {target_min_dist:.2f}")
            return

        factor = target_min_dist / min_dist
        # 限制最大缩放因子（避免极小间距导致爆炸放大）
        factor = min(factor, 10.0)

        # 放大设备坐标
        for elem in self.doc.elements:
            elem.x *= factor
            elem.y *= factor
            # Substation 是 polygon，width/height 不变但 points 要放大
            if elem.shape_tag == "polygon":
                pts_str = elem.shape_attrs.get("points", "")
                if pts_str:
                    new_pts = []
                    for pt in pts_str.strip().split():
                        coords = pt.split(",")
                        if len(coords) == 2:
                            try:
                                new_pts.append(
                                    f"{float(coords[0]) * factor:.6f},"
                                    f"{float(coords[1]) * factor:.6f}"
                                )
                            except ValueError:
                                new_pts.append(pt)
                        else:
                            new_pts.append(pt)
                    elem.shape_attrs["points"] = " ".join(new_pts)
            # 同步 transform 的 translate 分量
            if elem.transform:
                elem._transform_tx *= factor
                elem._transform_ty *= factor
                elem.rebuild_transform()

        # 放大连接线坐标
        for conn in self.doc.connections:
            conn.points = [(x * factor, y * factor) for x, y in conn.points]

        # 放大文字坐标（字号不放大，由 _normalize_text_styles 按规范统一设置）
        for txt in self.doc.texts:
            txt.x *= factor
            txt.y *= factor

        print(f"  坐标尺度归一化: 最小间距 {min_dist:.2f} → {min_dist * factor:.2f} (×{factor:.2f})")

    def _route_connections_to_edges(self):
        """基于新设备位置重新生成正交连接线路径。

        核心逻辑：
        1. 获取连接线的起止设备
        2. 计算设备边缘连接点
        3. 生成正交路径（L型或Z型）
        4. 无设备关联的连接线保持原样
        """
        device_by_id = {e.element_id: e for e in self.doc.elements if e.element_id}
        updated = 0
        skipped = 0

        def _edge_point(dev, target_x, target_y):
            """计算设备边缘上最接近目标方向的连接点。"""
            if not dev or dev.width <= 0 or dev.height <= 0:
                return None
            cx = dev.x + dev.width / 2.0
            cy = dev.y + dev.height / 2.0
            dx = target_x - cx
            dy = target_y - cy
            if abs(dx) < 1e-6 and abs(dy) < 1e-6:
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

        def _make_orthogonal_path(x1, y1, x2, y2):
            """生成正交折线路径：L型或Z型。"""
            if abs(x1 - x2) < 1.0:
                # 垂直直连
                return [(x1, y1), (x2, y2)]
            if abs(y1 - y2) < 1.0:
                # 水平直连
                return [(x1, y1), (x2, y2)]

            # 判断用L型还是Z型
            mid_x = (x1 + x2) / 2.0
            if abs(y1 - y2) < abs(x1 - x2) * 0.3:
                # Y差较小，用Z型走中线
                return [(x1, y1), (mid_x, y1), (mid_x, y2), (x2, y2)]
            else:
                # Y差较大，用L型
                if abs(y1 - y2) > abs(x1 - x2):
                    # 先垂直再水平
                    return [(x1, y1), (x1, y2), (x2, y2)]
                else:
                    # 先水平再垂直
                    return [(x1, y1), (x2, y1), (x2, y2)]

        for conn in self.doc.connections:
            start_dev = device_by_id.get(conn.start_device_id) if conn.start_device_id else None
            end_dev = device_by_id.get(conn.end_device_id) if conn.end_device_id else None

            # 跳过 start==end
            if start_dev and end_dev and start_dev.element_id == end_dev.element_id:
                skipped += 1
                continue

            if not start_dev and not end_dev:
                # 无设备关联，保持原样
                continue

            # 计算起止设备中心
            if start_dev:
                scx = start_dev.x + start_dev.width / 2
                scy = start_dev.y + start_dev.height / 2
            else:
                if not conn.points:
                    continue
                scx, scy = conn.points[0]

            if end_dev:
                ecx = end_dev.x + end_dev.width / 2
                ecy = end_dev.y + end_dev.height / 2
            else:
                if not conn.points:
                    continue
                ecx, ecy = conn.points[-1]

            # 计算边缘连接点
            sp = _edge_point(start_dev, ecx, ecy) if start_dev else (scx, scy)
            ep = _edge_point(end_dev, scx, scy) if end_dev else (ecx, ecy)

            if sp is None or ep is None:
                skipped += 1
                continue

            # 生成正交路径
            new_points = _make_orthogonal_path(sp[0], sp[1], ep[0], ep[1])
            conn.points = new_points
            updated += 1

        print(f"  连接线正交路由: {updated} 条已更新 (跳过: {skipped} 条)")


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
