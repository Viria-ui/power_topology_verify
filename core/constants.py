"""核心规范参数常量。"""

# B.2 精准色值映射表
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

# B.3 线宽 (px) 与线型规范
LINE_WIDTHS = {
    "main_feeder": 3.0,
    "branch": 1.5,
    "tie_line": 4.5,
    "spare_interval": 1.0,
    "station_border": 2.0,
}

VOLTAGE_CLASS_MAP = {
    "lkv1000": "#66CCFF", "lkv750": "#FF00FF", "lkv500": "#B400B4",
    "lkv330": "#008000", "lkv220": "#800080", "lkv110": "#F04155",
    "lkv66": "#FFCC00",  "lkv35": "#00C8FF",  "lkv20": "#00A854",
    "lkv15.75": "#00A854", "lkv13.8": "#00A854",
    "lkv10": "#FF0000",  "lkv6": "#00A854",   "lkv3": "#00A854",
    "lv380": "#FF6A00",  "lv220": "#FF6A00",  "lv110": "#FF6A00",
    "lvdc": "#FF6A00",
}

VOLTAGE_CLASS_WIDTHS = {
    "lkv1000": 3.0, "lkv750": 3.0, "lkv500": 3.0, "lkv330": 3.0,
    "lkv220": 3.0, "lkv110": 3.0, "lkv66": 3.0, "lkv35": 3.0,
    "lkv20": 3.0, "lkv15.75": 3.0, "lkv13.8": 3.0, "lkv10": 3.0,
    "lkv6": 1.5, "lkv3": 1.5, "lv380": 1.5, "lv220": 1.5,
    "lv110": 1.5, "lvdc": 1.5,
}

# 设备标准尺寸 (Task 5.1.3 规范)
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

# B.4 字体字号 (px) 与字重
FONTS = {
    "title": 21.3,          # 图纸标题/站房名 16pt bold
    "key_device": 14.0,     # 关键一次设备 10.5pt bold
    "branch_device": 12.0,  # 支线设备/线路名称 9pt normal
    "line_label": 12.0,     # 线路名称/编号 9pt normal
    "device_id": 10.0,      # 设备唯一 ID 7.5pt normal
}

# 布局参数 (v2 规范)
LAYOUT = {
    "grid": 10,
    "margin": 40,
    "title_h": 52,
    "node_w": 56,
    "unit_v": 14,
    "h_gap": 36,
    "v_gap": 4,
    "cont_pad": 24,
    "cont_gap": 16,
    "sym_scale": 3.5,
}

# 业务分类标记
WIRE_MARKERS = ('TMP', 'dxd')
BUSBAR_TYPES = {'0311', 'BusbarSection'}
CONTAINER_TYPES = {'zf01', 'zf06', 'zf07', 'zf08', 'Substation'}
SWITCH_TYPES = {'0307', '0201', '0202', '0203', '0302', '0305', '0306', '0309', 'Breaker', 'LoadBreakSwitch', 'Disconnector', 'GroundDisconnector'}
TRANSFORMER_TYPES = {'0110', '0111', 'PowerTransformer'}
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

# 关键一次设备图层（字号14, bold）
KEY_DEVICE_LAYERS = {"PowerTransformer", "Breaker", "BusbarSection"}

# B.1 网格吸附
GRID_SIZE = 10.0
