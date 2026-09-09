"""桌面 GUI：主配网拓扑校验与图形成果展示系统（tkinter + ttk）。

零额外依赖：仅依赖 Python 标准库 tkinter 与项目自带的 Pillow。

启动方式：
    双击  双击打开GUI.bat
    或命令行：  python scripts/visualization/gui_app.py
"""
from __future__ import annotations

import json
import re
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except Exception:
    HAS_PIL = False


# ----------------------------------------------------------------------
# 路径与常量
# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
SVG_DIR = OUTPUT / "svg"
SVG_PNG_DIR = OUTPUT / "svg_png"      # SVG → PNG 预渲染图
REPORT_DIR = OUTPUT / "reports"

# ----------------------------------------------------------------------
# 自动扫描数据集中所有线路（数据集更新版20260729/配网 svg）
# ----------------------------------------------------------------------
DATASET_SVG_ROOT_CANDIDATES = [
    ROOT / "数据集更新版20260729" / "配网 svg",
    ROOT / "input" / "svg",
    ROOT / "svg_input",
]


def _strip_voltage_prefix(name: str) -> str:
    """剥离 10kV / 35kV / 110kV 等电压前缀，用于线路匹配。"""
    import re as _re
    return _re.sub(r"^\d+(?:\.\d+)?\s*k?v", "", name.strip(), flags=_re.IGNORECASE)


def _is_valid_line_name(stem: str) -> bool:
    """判断一个 SVG 文件名是否对应一条馈线线路。

    过滤掉：美化图 ( *_beautified )、
    增删验证图（_add_ / _del_）、单线图（_single_line）、
    馈线联络图（_tie）、电源追溯图（_power_trace）、全站图（_station_tie）。
    """
    import re as _re
    s = stem.lower()
    # 排除带后缀的二次产品
    if any(s.endswith(suf) for suf in (
        "_beautified", "_single_line", "_tie", "_power_trace", "_station_tie",
    )):
        return False
    if "_add_" in s or "_del_" in s:
        return False
    # 只接受以 LINE 或 数字kVLINE 开头的
    if _re.match(r"^\d+(?:\.\d+)?\s*k?v?line", s, flags=_re.IGNORECASE):
        return True
    if s.startswith("line"):
        return True
    return False


def _discover_all_lines() -> list[str]:
    """扫描数据集目录，得到所有可识别的馈线名称（按字典序、去重）。

    优先级：数据集目录 → output/json 目录（已解析线路）。
    """
    seen: dict[str, str] = {}

    # 1) 数据集原始 SVG（这是最权威的列表）
    for cand in DATASET_SVG_ROOT_CANDIDATES:
        if cand.is_dir():
            for f in sorted(cand.glob("*.svg")):
                stem = f.stem
                if not _is_valid_line_name(stem):
                    continue
                key = stem.lower()
                if key not in seen:
                    seen[key] = stem
            if seen:
                # 数据集已扫描到足够多线路，不再继续
                break

    # 2) 已解析的 JSON（output/json）作为补充
    json_dir = OUTPUT / "json"
    if json_dir.is_dir():
        for fp in sorted(json_dir.glob("*.svg_elements.json")):
            stem = fp.name.replace(".svg_elements.json", "")
            if not _is_valid_line_name(stem):
                continue
            key = stem.lower()
            if key not in seen:
                seen[key] = stem

    # 按数字部分升序排序：10kVLINE003 < LINE215 < LINE216 < 10kVLINE230
    def _sort_key(name: str):
        import re as _re
        m = _re.search(r"(\d+)", name)
        n = int(m.group(1)) if m else 1_000_000
        return (n, name.lower())

    return sorted(seen.values(), key=_sort_key)


LINES: list[str] = _discover_all_lines()
if not LINES:
    LINES = ["LINE215", "LINE216", "LINE111"]

SVG_INFO: dict[str, tuple[str, str, str]] = {
    "LINE215_single_line.svg":        ("LINE215 单馈线单线图", "根据线路拓扑自动生成，展示线路设备及连接关系", "5.3"),
    "LINE216_single_line.svg":        ("LINE216 单馈线单线图", "根据线路拓扑自动生成，展示线路设备及连接关系", "5.3"),
    "LINE111_single_line.svg":        ("LINE111 单馈线单线图", "新增的 LINE111 馈线单线图", "5.3"),
    "10kVLINE111_tie.svg":            ("10kVLINE111 馈线联络图", "识别馈线间联络关系并突出联络开关", "5.3"),
    "SUB004_station_tie.svg":         ("SUB004 全站联络总图", "以 SUB004 为中心展示站内馈线及跨线联络关系", "5.3"),
    "TMP00034205_power_trace.svg":    ("TMP00034205 电源追溯图", "从目标设备反向追踪主供电路径与备用路径", "5.3"),
    "LINE215_beautified.svg":         ("LINE215 标准化美化图", "保留设备元数据，对图形布局和标注进行规范化", "5.1"),
    "LINE216_beautified.svg":         ("LINE216 标准化美化图", "保留设备元数据，对图形布局和标注进行规范化", "5.1"),
    "LINE215_add_station_000300.svg": ("LINE215 增加站房验证图", "用于展示增补设备后的拓扑变化", "5.2"),
    "LINE216_del_switch_00024.svg":   ("LINE216 删除开关验证图", "用于展示设备调整后的拓扑变化", "5.2"),
}

KEY_LABELS: dict[str, str] = {
    "score_before": "修复前评分", "score_after": "修复后评分", "total_deduction": "扣分合计",
    "defect_count": "缺陷数量", "deterministic_repair_ratio": "确定性修复比例",
    "defect_type": "缺陷类型", "device_id": "设备编号", "equip_id": "设备编号",
    "target_equip": "目标设备", "device_name": "设备名称", "risk_level": "风险等级",
    "confidence": "置信度", "suggestion": "修复建议", "action": "修复动作",
    "impact_summary": "影响说明", "repair_id": "方案编号", "description": "问题说明",
    "detail": "详细信息", "rule_code": "规则编号",
}

# 视觉色板 —— 现代扁平风
COLOR_BG        = "#f4f7fb"
COLOR_PANEL     = "#ffffff"
COLOR_BORDER    = "#e1e8f0"
COLOR_TEXT      = "#17243a"
COLOR_MUTED     = "#66788e"
COLOR_PRIMARY   = "#1890ff"
COLOR_SUCCESS   = "#00a854"
COLOR_WARN      = "#e99b37"
COLOR_DANGER    = "#e74747"
COLOR_SIDEBAR   = "#0e1a2b"
COLOR_SB_ACTIVE = "#1890ff"
COLOR_SB_TEXT   = "#cdd7e6"
COLOR_SB_HOVER  = "#1e2c44"

FONT_FAMILY = ("Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", "Segoe UI", "Arial")


# ----------------------------------------------------------------------
# 通用工具
# ----------------------------------------------------------------------
def decode(raw: bytes) -> str:
    for enc in ("utf-8-sig", "gb18030", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def prepare_inline_svg(raw: bytes) -> str:
    """去除 XML 命名空间前缀，便于嵌入 Tkinter。"""
    text = decode(raw)
    text = re.sub(r"<\?xml[^>]*\?>", "", text, count=1, flags=re.IGNORECASE)
    text = re.sub(r"xmlns:ns\d+=", "xmlns=", text)
    return re.sub(r"(<\/?)(?:ns\d+):", r"\1", text)


# ----------------------------------------------------------------------
# SVG → PNG 渲染（4 级回退：Edge/Chrome headless → cairosvg → svglib → Pillow）
# ----------------------------------------------------------------------
_PIL_RENDER_LOCK = None  # 占位，假装有锁（多线程时 Pillow 足够稳定）


def _find_browser() -> str | None:
    """查找系统中可用的 Edge 或 Chrome。"""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return None


def _render_svg_edge(svg_path: Path, width: int = 1400) -> bytes | None:
    """用 Edge/Chrome headless 渲染 SVG → PNG bytes。"""
    browser = _find_browser()
    if not browser:
        return None
    try:
        import tempfile, subprocess
        # 写一个 html wrapper（用 file URL 直接打开 SVG，绕开中文路径转义）
        svg_text = svg_path.read_text(encoding="utf-8", errors="replace")
        # 抽取 SVG 尺寸
        html = (
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<style>html,body{margin:0;padding:0;background:#fafafa;}"
            f"svg{{display:block;width:{width}px;height:auto;}}</style></head>"
            f"<body>{svg_text}</body></html>"
        )
        wrapper = Path(tempfile.gettempdir()) / f"svgwrap_{svg_path.name}_{abs(hash(svg_text))%100000}.html"
        wrapper.write_text(html, encoding="utf-8")
        png_out = wrapper.with_suffix(".png")
        if png_out.exists():
            png_out.unlink(missing_ok=True)
        # Edge headless
        cmd = [
            browser, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", f"--window-size={width},1100",
            f"--screenshot={png_out.as_posix()}",
            wrapper.as_uri(),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=45, encoding="utf-8", errors="replace")
        if png_out.exists():
            data = png_out.read_bytes()
            png_out.unlink(missing_ok=True)
            wrapper.unlink(missing_ok=True)
            # 验证 PNG 文件头
            if data.startswith(b"\x89PNG") and len(data) > 1000:
                return data
        return None
    except Exception:
        return None


def _render_svg_cairo(svg_path: Path, width: int = 1400) -> bytes | None:
    """用 cairosvg 渲染 SVG → PNG bytes。"""
    try:
        import cairosvg  # type: ignore
        return cairosvg.svg2png(url=str(svg_path), output_width=width)
    except Exception:
        return None


def _render_svg_svglib(svg_path: Path, width: int = 1400) -> bytes | None:
    """用 svglib + reportlab 渲染 SVG → PNG bytes。"""
    try:
        from svglib.svglib import svg2rlg  # type: ignore
        from reportlab.graphics import renderPM
        drawing = svg2rlg(str(svg_path))
        if drawing is None:
            return None
        # 缩放到目标宽度
        scale = width / max(1, drawing.width)
        drawing.width = width
        drawing.height = int(drawing.height * scale)
        return renderPM.drawToString(drawing, fmt="PNG", dpi=int(96 * scale))
    except Exception:
        return None


def render_svg_png(svg_path: Path, width: int = 1400) -> bytes | None:
    """统一 SVG → PNG 入口，按顺序尝试 Edge headless → cairosvg → svglib。

    返回 PNG bytes；任何方法都失败则返回 None（调用方走"文本回退"）。
    """
    if not svg_path.exists():
        return None
    for fn in (_render_svg_edge, _render_svg_cairo, _render_svg_svglib):
        try:
            data = fn(svg_path, width)
            if data:
                return data
        except Exception:
            continue
    return None


def make_tk_image(png_bytes: bytes, max_size=(900, 600)):
    """将 PNG bytes 转成 tkinter PhotoImage，自动缩放。"""
    from io import BytesIO
    img = Image.open(BytesIO(png_bytes))
    img.thumbnail(max_size)
    return ImageTk.PhotoImage(img)


def _png_for_svg(svg_path: Path) -> Path | None:
    """返回 SVG 对应的预渲染 PNG 路径（若存在则优先用）。"""
    if svg_path.suffix.lower() == ".svg":
        png = SVG_PNG_DIR / svg_path.name.replace(".svg", ".png")
        if png.exists():
            return png
    return None


# ----------------------------------------------------------------------
# 渲染 SVG 到 Tkinter widget 的通用工具
# ----------------------------------------------------------------------
def mount_svg_preview(parent: tk.Widget, svg_path: Path, max_size=(900, 600)) -> bool:
    """在 parent 上渲染 SVG；返回 True 表示成功显示图片，False 表示只显示了文本。"""
    png = render_svg_png(svg_path)
    if png:
        try:
            photo = make_tk_image(png, max_size)
            parent._keep_ref = getattr(parent, "_keep_ref", [])
            parent._keep_ref.append(photo)
            tk.Label(parent, image=photo, bg="#fafafa").pack(padx=4, pady=4)
            return True
        except Exception:
            pass
    # Pillow 直开兜底（如果 SVG 被识别为 raster）
    try:
        img = Image.open(svg_path)
        img.thumbnail(max_size)
        photo = ImageTk.PhotoImage(img)
        parent._keep_ref = getattr(parent, "_keep_ref", [])
        parent._keep_ref.append(photo)
        tk.Label(parent, image=photo, bg="#fafafa").pack(padx=4, pady=4)
        return True
    except Exception:
        pass
    # 文本兜底
    try:
        text = prepare_inline_svg(svg_path.read_bytes())
        tk.Label(parent, text=text[:3000] + ("\n……" if len(text) > 3000 else ""),
                 font=("Consolas", 9), bg="#fafafa", fg=COLOR_TEXT,
                 justify="left", anchor="nw").pack(fill="both", expand=True)
    except Exception:
        tk.Label(parent, text=f"无法渲染 {svg_path.name}",
                 bg="#fafafa", fg=COLOR_MUTED).pack(padx=10, pady=30)
    return False


def clean_text(value: Any) -> str:
    text = "" if value is None else str(value)
    if "\ufffd" in text or "锟斤拷" in text:
        return "原始文件未提供有效中文说明"
    return text.replace("?", "—").replace("\ufeff", "").strip()


def clean_data(value: Any) -> Any:
    if isinstance(value, dict):
        return {KEY_LABELS.get(str(k), clean_text(k)): clean_data(v) for k, v in value.items() if k != "note"}
    if isinstance(value, list):
        return [clean_data(v) for v in value]
    if isinstance(value, str):
        return clean_text(value)
    return value


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return clean_data(json.loads(decode(path.read_bytes())))
    except Exception:
        return default


def load_raw_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(decode(path.read_bytes()))
    except Exception:
        return default


def line_bundle(line: str) -> dict[str, Any]:
    """加载一条线路的所有报告数据。"""
    score_raw = load_raw_json(OUTPUT / f"{line}_质量评分与可解释置信度报告.json", {}) or {}
    score = clean_data(score_raw)
    defects = load_json(OUTPUT / f"{line}_缺陷清单报告.json", []) or []
    repair = load_json(OUTPUT / f"{line}_最小修改候选与SQL草案.json", {}) or {}
    breakpoint = load_json(OUTPUT / f"{line}_赛题1.2专项断点报告.json", {}) or {}
    sql_path = OUTPUT / f"{line}_正向修复与回滚脚本.sql"
    sql = clean_text(decode(sql_path.read_bytes())) if sql_path.exists() else ""
    return {
        "score_raw": score_raw, "score": score, "defects": defects,
        "repair": repair, "breakpoint": breakpoint, "sql": sql,
        "excel": OUTPUT / f"{line}_拓扑校验缺陷报告.xlsx",
    }


# ----------------------------------------------------------------------
# 窗口组件
# ----------------------------------------------------------------------
class ZoomableThumb:
    """可独立放置的 PNG 缩略图组件，支持滚轮缩放、拖动平移、放大缩小工具栏。
    自管理状态，不依赖外部实例属性。可放在 SubmitPage 缩略图网格中。
    """
    def __init__(self, parent, png_path: Path, initial_zoom: float = 0.4):
        self._orig_pil_image = Image.open(str(png_path)).copy()
        self._zoom = initial_zoom
        self._png_path = png_path
        self._keep_ref: list[Any] = []
        self._pan_state: tuple | None = None
        self._build(parent)

    def _build(self, parent):
        toolbar = tk.Frame(parent, bg="#fafafa")
        toolbar.pack(fill="x", padx=2, pady=(2, 0))
        self._zoom_label = tk.Label(toolbar, text=f"{int(self._zoom * 100)}%",
                                    font=(FONT_FAMILY[0], 8), fg=COLOR_MUTED, bg="#fafafa", width=5)
        self._zoom_label.pack(side="right", padx=2)
        ttk.Button(toolbar, text="➕", width=3,
                    command=lambda: self._set_zoom(self._zoom * 1.25)).pack(side="right", padx=1)
        ttk.Button(toolbar, text="➖", width=3,
                    command=lambda: self._set_zoom(self._zoom / 1.25)).pack(side="right", padx=1)
        ttk.Button(toolbar, text="↺", width=3,
                    command=lambda: self._set_zoom(0.4)).pack(side="right", padx=1)
        tk.Label(toolbar, text="💡 滚轮缩放/拖动",
                 font=(FONT_FAMILY[0], 8), fg=COLOR_MUTED, bg="#fafafa").pack(side="left", padx=2)

        canvas_frame = tk.Frame(parent, bg="#fafafa")
        canvas_frame.pack(fill="both", expand=True, padx=2, pady=(0, 2))
        self._canvas = tk.Canvas(canvas_frame, bg="#ffffff",
                                  highlightthickness=1, highlightbackground=COLOR_BORDER)
        y_sb = ttk.Scrollbar(canvas_frame, orient="vertical", command=self._canvas.yview)
        x_sb = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self._canvas.xview)
        self._canvas.configure(xscrollcommand=x_sb.set, yscrollcommand=y_sb.set)
        y_sb.pack(side="right", fill="y")
        x_sb.pack(side="bottom", fill="x")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self._canvas.bind("<Button-4>", lambda e: self._set_zoom(self._zoom * 1.1))
        self._canvas.bind("<Button-5>", lambda e: self._set_zoom(self._zoom / 1.1))
        self._canvas.bind("<ButtonPress-1>", self._pan_start)
        self._canvas.bind("<B1-Motion>", self._pan_move)
        self._render()

    def _render(self):
        w0, h0 = self._orig_pil_image.size
        zw = max(1, int(w0 * self._zoom))
        zh = max(1, int(h0 * self._zoom))
        resized = self._orig_pil_image.resize((zw, zh), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)
        self._keep_ref.append(photo)
        self._canvas.delete("all")
        self._canvas.configure(scrollregion=(0, 0, zw, zh))
        self._canvas.create_image(0, 0, anchor="nw", image=photo)
        if hasattr(self, "_zoom_label"):
            self._zoom_label.configure(text=f"{int(self._zoom * 100)}%")

    def _set_zoom(self, new_zoom: float):
        new_zoom = max(0.1, min(8.0, new_zoom))
        if abs(new_zoom - self._zoom) < 1e-4:
            return
        self._zoom = new_zoom
        self._render()

    def _on_mouse_wheel(self, event):
        if event.delta > 0:
            self._set_zoom(self._zoom * 1.1)
        else:
            self._set_zoom(self._zoom / 1.1)

    def _pan_start(self, event):
        self._canvas.scan_mark(event.x, event.y)
        self._pan_state = (event.x, event.y)

    def _pan_move(self, event):
        if self._pan_state:
            self._canvas.scan_dragto(event.x, event.y, gain=1)


class ScrollFrame(tk.Frame):
    """通用可滚动容器。"""
    def __init__(self, master, bg=COLOR_PANEL):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)

        self.win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel(self.canvas)

    def _on_inner_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.win_id, width=event.width)

    def _bind_mousewheel(self, widget):
        # 仅当鼠标在 widget 范围内才滚动
        def _on_wheel(event):
            if event.delta:
                delta = -1 if event.delta > 0 else 1
                self.canvas.yview_scroll(delta, "units")
            elif event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        widget.bind("<Enter>", lambda _: widget.bind_all("<MouseWheel>", _on_wheel))
        widget.bind("<Leave>", lambda _: widget.unbind_all("<MouseWheel>"))
        widget.bind("<Button-4>", _on_wheel)
        widget.bind("<Button-5>", _on_wheel)

    def clear(self):
        for w in self.inner.winfo_children():
            w.destroy()


class Card(tk.Frame):
    """卡片组件（白色背景、圆角风格的扁平设计）。"""
    def __init__(self, master, title: str, body: str = "", accent: str = COLOR_PRIMARY,
                 padx: int = 18, pady: int = 14, min_height: int = 96):
        super().__init__(master, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER)
        self.accent = accent
        self.title_label = tk.Label(self, text=title, font=(FONT_FAMILY[0], 14, "bold"),
                                     fg=COLOR_TEXT, bg=COLOR_PANEL, anchor="w")
        self.title_label.pack(fill="x", padx=padx, pady=(pady, 4))
        bar = tk.Frame(self, bg=accent, height=2)
        bar.pack(fill="x", padx=padx)
        self.body_label = tk.Label(self, text=body, font=(FONT_FAMILY[0], 11),
                                    fg=COLOR_MUTED, bg=COLOR_PANEL, anchor="nw",
                                    justify="left", wraplength=520)
        self.body_label.pack(fill="both", expand=True, padx=padx, pady=(8, pady))
        if min_height:
            self.body_label.configure(height=4)

    def set_body(self, body: str):
        self.body_label.configure(text=body)


class MetricCard(tk.Frame):
    """指标卡片（带色彩下划线）。"""
    def __init__(self, master, label: str, value: str, hint: str = "",
                 color: str = COLOR_PRIMARY):
        super().__init__(master, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER)
        tk.Label(self, text=label, font=(FONT_FAMILY[0], 10), fg=COLOR_MUTED,
                 bg=COLOR_PANEL, anchor="w").pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(self, text=value, font=(FONT_FAMILY[0], 22, "bold"), fg=COLOR_TEXT,
                 bg=COLOR_PANEL, anchor="w").pack(fill="x", padx=14)
        if hint:
            tk.Label(self, text=hint, font=(FONT_FAMILY[0], 9), fg="#9aa6b8",
                     bg=COLOR_PANEL, anchor="w").pack(fill="x", padx=14, pady=(0, 6))
        bar = tk.Frame(self, bg=color, height=3)
        bar.pack(fill="x", side="bottom")


class TreeTable(tk.Frame):
    """使用 ttk.Treeview 展示表格，支持搜索过滤。"""
    def __init__(self, master, columns: list[str], col_widths: dict[str, int] | None = None):
        super().__init__(master, bg=COLOR_PANEL)
        self.all_rows: list[tuple] = []
        self.all_columns = columns

        toolbar = tk.Frame(self, bg=COLOR_PANEL)
        toolbar.pack(fill="x", pady=(0, 6))
        tk.Label(toolbar, text="搜索：", font=(FONT_FAMILY[0], 10),
                 fg=COLOR_MUTED, bg=COLOR_PANEL).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh())
        entry = ttk.Entry(toolbar, textvariable=self.search_var, width=30)
        entry.pack(side="left", padx=(4, 8))
        self.count_label = tk.Label(toolbar, text="", font=(FONT_FAMILY[0], 9),
                                     fg=COLOR_MUTED, bg=COLOR_PANEL)
        self.count_label.pack(side="right")

        tree_wrap = tk.Frame(self, bg=COLOR_PANEL, highlightthickness=1,
                              highlightbackground=COLOR_BORDER)
        tree_wrap.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(tree_wrap, columns=columns, show="headings", height=18)
        widths = col_widths or {}
        for col in columns:
            self.tree.heading(col, text=KEY_LABELS.get(col, col), command=lambda c=col: self._sort(c))
            self.tree.column(col, width=widths.get(col, 110), anchor="w")
        vbar = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vbar.pack(side="right", fill="y")
        self._sort_state: dict[str, bool] = {c: False for c in columns}

    def set_rows(self, rows: list[tuple]):
        self.all_rows = rows
        self._refresh()

    def _refresh(self):
        kw = self.search_var.get().strip().lower()
        if kw:
            rows = [r for r in self.all_rows if any(kw in str(v).lower() for v in r)]
        else:
            rows = self.all_rows
        self.tree.delete(*self.tree.get_children())
        for r in rows[:500]:
            display = ["" if v is None else clean_text(v) for v in r]
            self.tree.insert("", "end", values=display)
        self.count_label.configure(text=f"显示 {min(len(rows), 500)} / 共 {len(self.all_rows)} 条")

    def _sort(self, col):
        idx = self.all_columns.index(col)
        reverse = self._sort_state[col]
        self._sort_state[col] = not reverse
        self.all_rows.sort(key=lambda r: str(r[idx]), reverse=reverse)
        self._refresh()


# ----------------------------------------------------------------------
# 各页面
# ----------------------------------------------------------------------
class OverviewPage(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master, bg=COLOR_BG)
        self.switch = switch
        self.scroll = ScrollFrame(self, bg=COLOR_BG)
        self.scroll.pack(fill="both", expand=True)
        self._build()

    def _card_grid(self, items: list[tuple[str, str]]):
        grid = tk.Frame(self.scroll.inner, bg=COLOR_BG)
        grid.pack(fill="x", padx=8, pady=(0, 14))
        for i in range(0, len(items), 2):
            row = tk.Frame(grid, bg=COLOR_BG)
            row.pack(fill="x", pady=6)
            for title, body in items[i:i + 2]:
                card = Card(row, title, body, padx=16, pady=12)
                card.pack(side="left", fill="both", expand=True, padx=6)

    def _flow(self, text: str):
        box = tk.Frame(self.scroll.inner, bg="#eef4fa", highlightthickness=1,
                        highlightbackground="#d6e2ee")
        box.pack(fill="x", padx=8, pady=(0, 14))
        tk.Label(box, text=text, font=(FONT_FAMILY[0], 11), fg="#314964",
                 bg="#eef4fa", justify="left", anchor="w").pack(padx=18, pady=12, fill="x")

    def _section(self, title: str):
        bar = tk.Frame(self.scroll.inner, bg=COLOR_BG)
        bar.pack(fill="x", padx=8, pady=(18, 10))
        tk.Frame(bar, bg=COLOR_WARN, width=4).pack(side="left", fill="y", padx=(0, 8))
        tk.Label(bar, text=title, font=(FONT_FAMILY[0], 14, "bold"),
                 fg="#183b64", bg=COLOR_BG).pack(side="left")

    def _metric_row(self, items: list[tuple[str, str, str]]):
        row = tk.Frame(self.scroll.inner, bg=COLOR_BG)
        row.pack(fill="x", padx=8, pady=(0, 14))
        for label, value, hint in items:
            MetricCard(row, label, value, hint).pack(side="left", fill="both", expand=True, padx=4)

    def _build(self):
        # 项目内容
        self._section("项目内容")
        self._card_grid([
            ("拓扑结构校验", "检测设备悬空、线路断点、联络开关及合环问题，定位到设备和线路。"),
            ("图模一致性比对", "比较 SVG 图形与数据库模型，识别图有模无、模有图无及连接不一致。"),
            ("修复方案生成", "结合风险、置信度和影响范围给出最小修改候选，并生成正向与回滚 SQL。"),
            ("SVG 图形成果", "形成馈线单线图、联络关系图、全站联络图、电源追溯图及美化图。"),
        ])

        # 输入与输出
        self._section("输入与输出")
        self._flow("输入：SQL 设备模型、端点关系、线路信息、遥信遥测数据、配网 SVG 图纸\n"
                    "　　→　分析：拓扑建图、连通性检测、图模比对、电气逻辑校验、置信度评估\n"
                    "　　→　输出：缺陷清单、评分报告、修复候选、SQL 脚本、Excel 报告、SVG 图形")

        # 现有成果
        self._section("现有成果")
        svg_n = len(list(SVG_DIR.glob("*.svg")))
        xlsx_n = len(list(OUTPUT.glob("*.xlsx")))
        json_n = len(list(OUTPUT.glob("*.json")))
        sql_n = len(list(OUTPUT.glob("*.sql")))
        defects_total = 0
        for line in LINES:
            d = load_json(OUTPUT / f"{line}_缺陷清单报告.json", [])
            if isinstance(d, list):
                defects_total += len(d)
        self._metric_row([
            ("重点线路", f"{len(LINES)} 条", "LINE215 / LINE216 / LINE111"),
            ("SVG 图形成果", f"{svg_n}", "output/svg"),
            ("缺陷记录", f"{defects_total:,}", "LINE215 / LINE216 / LINE111"),
            ("Excel 报告", f"{xlsx_n}", "output/*.xlsx"),
            ("分析报告", f"{json_n}", "output/*.json"),
        ])

        # 快捷入口
        self._section("快捷入口")
        actions = tk.Frame(self.scroll.inner, bg=COLOR_BG)
        actions.pack(fill="x", padx=8, pady=(0, 24))
        btn_specs = [
            ("⚡ 一键运行", "run"),
            ("查看线路成果", "line"),
            ("浏览 SVG 图纸", "svg"),
            ("查看增删对比", "image"),
            ("提交资料下载", "submit"),
        ]
        for label, key in btn_specs:
            ttk.Button(actions, text=label, command=lambda k=key: self.switch(k)).pack(side="left", padx=6)

        # 赛题任务
        self._section("对应赛题任务")
        tasks = [
            ("任务一", "拓扑结构完整性", "悬空检测、断点定位、联络开关识别、合环检测", "缺陷报告、专项断点报告"),
            ("任务二", "图模一致性", "图有模无、模有图无、连接关系不一致", "缺陷清单、质量评分"),
            ("任务三", "修正与复核", "最小修改候选、影响分析、修复后复核", "候选报告、SQL 脚本、Excel"),
            ("任务四", "SVG 图形专项", "标准化美化、单线图、联络图、电源追溯图", "修正 SVG 与专题图集"),
        ]
        for tno, name, method, output in tasks:
            row = tk.Frame(self.scroll.inner, bg=COLOR_PANEL, highlightthickness=1,
                           highlightbackground=COLOR_BORDER)
            row.pack(fill="x", padx=8, pady=4)
            tk.Label(row, text=tno, font=(FONT_FAMILY[0], 11, "bold"),
                     fg="#fff", bg=COLOR_PRIMARY, width=8).pack(side="left", fill="y", padx=(0, 12), pady=1)
            tk.Label(row, text=name, font=(FONT_FAMILY[0], 11, "bold"),
                     fg=COLOR_TEXT, bg=COLOR_PANEL, width=14, anchor="w").pack(side="left", pady=8)
            tk.Label(row, text=method, font=(FONT_FAMILY[0], 10),
                     fg=COLOR_MUTED, bg=COLOR_PANEL, anchor="w").pack(side="left", fill="x", expand=True, padx=8)
            tk.Label(row, text=output, font=(FONT_FAMILY[0], 10),
                     fg=COLOR_SUCCESS, bg=COLOR_PANEL, anchor="w").pack(side="right", padx=12)


class LinePage(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master, bg=COLOR_BG)
        self.switch = switch
        self.current_line = tk.StringVar(value=LINES[0])
        self._build()

    def _header(self):
        bar = tk.Frame(self, bg=COLOR_PANEL, highlightthickness=1,
                        highlightbackground=COLOR_BORDER)
        bar.pack(fill="x", padx=8, pady=(8, 6))
        tk.Label(bar, text="线路校验成果", font=(FONT_FAMILY[0], 14, "bold"),
                 fg="#183b64", bg=COLOR_PANEL).pack(side="left", padx=18, pady=10)
        tk.Label(bar, text="选择线路：", font=(FONT_FAMILY[0], 11),
                 fg=COLOR_MUTED, bg=COLOR_PANEL).pack(side="left", padx=(20, 6), pady=10)
        combo = ttk.Combobox(bar, textvariable=self.current_line, values=LINES,
                              state="readonly", width=18)
        combo.pack(side="left", pady=10)
        combo.bind("<<ComboboxSelected>>", lambda _: self._reload())

    def _build(self):
        self._header()
        self.scroll = ScrollFrame(self, bg=COLOR_BG)
        self.scroll.pack(fill="both", expand=True)
        self._reload()

    def _reload(self):
        self.scroll.clear()
        line = self.current_line.get()
        bundle = line_bundle(line)
        summary = bundle["score_raw"].get("score_summary", {}) if isinstance(bundle["score_raw"], dict) else {}
        defects = bundle["defects"] if isinstance(bundle["defects"], list) else []
        repair = bundle["repair"] if isinstance(bundle["repair"], dict) else {}
        candidates = repair.get("candidates", []) if isinstance(repair, dict) else []

        # 指标行
        mrow = tk.Frame(self.scroll.inner, bg=COLOR_BG)
        mrow.pack(fill="x", padx=8, pady=(0, 12))
        for label, value, hint, color in [
            ("线路", line, "当前选中", COLOR_PRIMARY),
            ("缺陷数量", f"{len(defects):,}", "缺陷清单报告", COLOR_DANGER),
            ("修复候选", f"{len(candidates):,}", "SQL 草案", COLOR_SUCCESS),
            ("确定性修复", f"{float(summary.get('deterministic_repair_ratio', 0)) * 100:.0f}%",
             "AI 确定性比例", COLOR_WARN),
            ("复核评分", str(summary.get("score_after", "-")), "质量评分", COLOR_PRIMARY),
        ]:
            MetricCard(mrow, label, value, hint, color).pack(side="left", fill="both", expand=True, padx=4)

        # Tabs
        nb = ttk.Notebook(self.scroll.inner)
        nb.pack(fill="both", expand=True, padx=8, pady=4)

        tab_defects = tk.Frame(nb, bg=COLOR_BG)
        tab_candidates = tk.Frame(nb, bg=COLOR_BG)
        tab_score = tk.Frame(nb, bg=COLOR_BG)
        tab_break = tk.Frame(nb, bg=COLOR_BG)
        tab_sql = tk.Frame(nb, bg=COLOR_BG)
        tab_excel = tk.Frame(nb, bg=COLOR_BG)
        nb.add(tab_defects, text="缺陷清单")
        nb.add(tab_candidates, text="修复候选")
        nb.add(tab_score, text="评分结果")
        nb.add(tab_break, text="专项断点")
        nb.add(tab_sql, text="SQL 脚本")
        nb.add(tab_excel, text="Excel 报告")

        # 缺陷清单
        self._render_tree(tab_defects, defects)

        # 修复候选
        self._render_tree(tab_candidates, candidates)

        # 评分结果
        self._render_kv(tab_score, bundle["score"])

        # 专项断点
        self._render_kv(tab_break, bundle["breakpoint"])

        # SQL
        self._render_sql(tab_sql, bundle["sql"], line)

        # Excel
        self._render_excel(tab_excel, bundle["excel"], line)

    def _render_tree(self, parent, rows: list[dict]):
        wrap = tk.Frame(parent, bg=COLOR_BG)
        wrap.pack(fill="both", expand=True, padx=4, pady=4)
        if not isinstance(rows, list) or not rows:
            tk.Label(wrap, text="暂无数据", font=(FONT_FAMILY[0], 11),
                     fg=COLOR_MUTED, bg=COLOR_BG).pack(pady=30)
            return
        # 稳定列
        seen = []
        for r in rows:
            if isinstance(r, dict):
                for k in r.keys():
                    if k not in seen:
                        seen.append(k)
        cols = seen[:8]
        widths = {c: 120 for c in cols}
        table = TreeTable(wrap, cols, widths)
        table.pack(fill="both", expand=True)
        data = [tuple(r.get(c, "") if isinstance(r, dict) else "" for c in cols) for r in rows]
        table.set_rows(data)

    def _render_kv(self, parent, data: Any):
        wrap = tk.Frame(parent, bg=COLOR_BG)
        wrap.pack(fill="both", expand=True, padx=4, pady=4)
        text = json.dumps(data, ensure_ascii=False, indent=2) if data else "暂无数据"
        txt = tk.Text(wrap, font=("Consolas", 10), bg="#0e1a2b", fg="#cdd7e6",
                      insertbackground="#fff", relief="flat", wrap="none")
        txt.pack(fill="both", expand=True, side="left")
        sb = ttk.Scrollbar(wrap, orient="vertical", command=txt.yview)
        sb.pack(fill="y", side="right")
        txt.configure(yscrollcommand=sb.set)
        if text:
            txt.insert("1.0", text)

    def _render_sql(self, parent, sql: str, line: str):
        wrap = tk.Frame(parent, bg=COLOR_BG)
        wrap.pack(fill="both", expand=True, padx=4, pady=4)
        toolbar = tk.Frame(wrap, bg=COLOR_PANEL, height=36)
        toolbar.pack(fill="x", pady=(0, 6))
        tk.Label(toolbar, text=f" {line} 的正向修复与回滚脚本", font=(FONT_FAMILY[0], 10),
                 fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", padx=10, pady=6)
        ttk.Button(toolbar, text="复制全文", command=lambda: self._copy(sql)).pack(side="right", padx=6, pady=4)
        txt = tk.Text(wrap, font=("Consolas", 10), bg="#0e1a2b", fg="#cdd7e6",
                      insertbackground="#fff", relief="flat", wrap="none")
        txt.pack(fill="both", expand=True, side="left")
        sb = ttk.Scrollbar(wrap, orient="vertical", command=txt.yview)
        sb.pack(fill="y", side="right")
        txt.configure(yscrollcommand=sb.set)
        if sql:
            txt.insert("1.0", sql)
        else:
            txt.insert("1.0", "未找到对应的 SQL 文件")

    def _render_excel(self, parent, excel_path: Path, line: str):
        wrap = tk.Frame(parent, bg=COLOR_BG)
        wrap.pack(fill="both", expand=True, padx=4, pady=4)
        if not excel_path.exists():
            tk.Label(wrap, text="运行主程序后，线路 Excel 报告会显示在这里。",
                     font=(FONT_FAMILY[0], 11), fg=COLOR_MUTED, bg=COLOR_BG).pack(pady=40)
            return
        info = tk.Frame(wrap, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        info.pack(fill="x", padx=4, pady=4)
        tk.Label(info, text=f"📄  {excel_path.name}", font=(FONT_FAMILY[0], 12, "bold"),
                 fg=COLOR_TEXT, bg=COLOR_PANEL).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(info, text=f"路径：{excel_path}　|　大小：{excel_path.stat().st_size / 1024:.1f} KB",
                 font=(FONT_FAMILY[0], 9), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(anchor="w", padx=14, pady=(0, 10))
        ttk.Button(info, text="打开所在文件夹", command=lambda: self._open_folder(excel_path)).pack(anchor="e", padx=12, pady=(0, 10))

    def _copy(self, text: str):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("已复制", "SQL 内容已复制到剪贴板")

    def _open_folder(self, path: Path):
        try:
            if sys.platform.startswith("win"):
                import subprocess
                subprocess.Popen(["explorer", "/select,", str(path)])
            else:
                webbrowser.open(path.parent.as_uri())
        except Exception as e:
            messagebox.showerror("打开失败", str(e))


class SvgPage(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master, bg=COLOR_BG)
        self.switch = switch
        self.current = tk.StringVar()
        self._build()

    def _build(self):
        # 顶部
        head = tk.Frame(self, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        head.pack(fill="x", padx=8, pady=(8, 6))
        tk.Label(head, text="SVG 图形成果", font=(FONT_FAMILY[0], 14, "bold"),
                 fg="#183b64", bg=COLOR_PANEL).pack(side="left", padx=18, pady=10)
        ttk.Button(head, text="打开输出目录", command=lambda: self._open(SVG_DIR)).pack(side="right", padx=12, pady=8)

        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        left = tk.Frame(body, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER, width=280)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        tk.Label(left, text="图纸列表", font=(FONT_FAMILY[0], 11, "bold"),
                 fg=COLOR_TEXT, bg=COLOR_PANEL, anchor="w").pack(fill="x", padx=12, pady=(10, 4))

        self.files = sorted(SVG_DIR.glob("*.svg"), key=lambda p: p.name.lower())
        if not self.files:
            tk.Label(left, text="暂无 SVG 文件", font=(FONT_FAMILY[0], 10),
                     fg=COLOR_MUTED, bg=COLOR_PANEL).pack(padx=12, pady=20)
        list_frame = tk.Frame(left, bg=COLOR_PANEL)
        list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.listbox = tk.Listbox(list_frame, font=(FONT_FAMILY[0], 10), bg=COLOR_PANEL,
                                   fg=COLOR_TEXT, selectbackground=COLOR_PRIMARY,
                                   selectforeground="#fff", borderwidth=0, highlightthickness=0,
                                   activestyle="none")
        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for f in self.files:
            label = SVG_INFO.get(f.name, (f.stem, "", ""))[0]
            self.listbox.insert("end", f"  {label}  ·  {f.name}")
        if self.files:
            self.listbox.selection_set(0)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # 右侧预览 + 信息
        self.right = tk.Frame(body, bg=COLOR_PANEL, highlightthickness=1,
                                highlightbackground=COLOR_BORDER)
        self.right.pack(side="left", fill="both", expand=True)
        if self.files:
            self._show(self.files[0])

    def _on_select(self, _event=None):
        sel = self.listbox.curselection()
        if sel:
            self._show(self.files[sel[0]])

    def _show(self, path: Path):
        for w in self.right.winfo_children():
            w.destroy()
        info = SVG_INFO.get(path.name, (path.stem, "项目生成的 SVG 图形成果", "5.x"))
        title, desc, sub = info

        head = tk.Frame(self.right, bg=COLOR_PANEL)
        head.pack(fill="x", padx=16, pady=(12, 6))
        tk.Label(head, text=title, font=(FONT_FAMILY[0], 14, "bold"),
                 fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left")
        tag = tk.Label(head, text=f"赛题 {sub}", font=(FONT_FAMILY[0], 9),
                        fg="#fff", bg=COLOR_SUCCESS, padx=8, pady=2)
        tag.pack(side="right")
        tk.Label(self.right, text=desc, font=(FONT_FAMILY[0], 10),
                 fg=COLOR_MUTED, bg=COLOR_PANEL, anchor="w",
                 wraplength=900).pack(fill="x", padx=16, pady=(0, 6))

        bar = tk.Frame(self.right, bg=COLOR_PANEL)
        bar.pack(fill="x", padx=16, pady=(0, 6))
        tk.Label(bar, text=f"文件：{path.name}　|　大小：{path.stat().st_size / 1024:.1f} KB",
                 font=(FONT_FAMILY[0], 9), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(side="left")
        ttk.Button(bar, text="💾 保存 SVG…", command=lambda: self._save(path)).pack(side="right", padx=4)

        body_wrap = tk.Frame(self.right, bg="#fafafa", highlightthickness=1,
                              highlightbackground=COLOR_BORDER)
        body_wrap.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        # 优先用预渲染 PNG（用户可直接查看，无需渲染器）
        png_path = _png_for_svg(path)
        if png_path:
            self._show_png(body_wrap, png_path)
        else:
            # PNG 不存在：实时渲染，渲染成功顺手写一份进 svg_png/ 缓存
            png_bytes = render_svg_png(path, width=1400)
            if png_bytes:
                try:
                    SVG_PNG_DIR.mkdir(parents=True, exist_ok=True)
                    cache_png = SVG_PNG_DIR / (path.stem + ".png")
                    cache_png.write_bytes(png_bytes)
                    # 写成功后用 ZoomableThumb 显示（带放大缩小）
                    ZoomableThumb(body_wrap, cache_png, initial_zoom=1.0)
                except Exception:
                    # 写文件失败（权限等），仍然显示内存中的渲染结果
                    from io import BytesIO
                    img = Image.open(BytesIO(png_bytes))
                    img.thumbnail((1100, 800))
                    photo = ImageTk.PhotoImage(img)
                    body_wrap._keep_ref = getattr(body_wrap, "_keep_ref", [])
                    body_wrap._keep_ref.append(photo)
                    tk.Label(body_wrap, image=photo, bg="#fafafa").pack(padx=4, pady=4)
            else:
                # 渲染全失败，显示 SVG 源码文本
                mount_svg_preview(body_wrap, path, max_size=(1100, 800))

    def _show_png(self, parent, png_path: Path):
        """加载 PNG 显示，支持缩放、滚轮缩放、滚动条、保存。"""
        try:
            # 读取原图（不缩放，缩放交给 zoom 处理，避免重复插值）
            orig = Image.open(str(png_path))
            self._orig_pil_image = orig.copy()
            self._zoom = 1.0
            self._png_path = png_path

            # 工具条（缩放 + 保存 + 重置）
            toolbar = tk.Frame(parent, bg="#fafafa")
            toolbar.pack(fill="x", padx=16, pady=(0, 4))
            tk.Label(toolbar, text=f"📷 {png_path.name}　{png_path.stat().st_size / 1024:.1f} KB",
                     font=(FONT_FAMILY[0], 9), fg=COLOR_SUCCESS, bg="#fafafa").pack(side="left")
            ttk.Button(toolbar, text="💾 保存 PNG", command=lambda: self._save_png(png_path)).pack(side="right", padx=2)
            ttk.Button(toolbar, text="放大 ➕", command=lambda: self._set_zoom(self._zoom * 1.25)).pack(side="right", padx=2)
            ttk.Button(toolbar, text="缩小 ➖", command=lambda: self._set_zoom(self._zoom / 1.25)).pack(side="right", padx=2)
            ttk.Button(toolbar, text="🔄 重置", command=lambda: self._set_zoom(1.0)).pack(side="right", padx=2)
            self._zoom_label = tk.Label(toolbar, text="100%", font=(FONT_FAMILY[0], 9),
                                        fg=COLOR_MUTED, bg="#fafafa", width=6)
            self._zoom_label.pack(side="right", padx=6)
            tk.Label(toolbar, text="💡 鼠标滚轮可缩放，按住拖动可平移",
                     font=(FONT_FAMILY[0], 9), fg=COLOR_MUTED, bg="#fafafa").pack(side="left", padx=12)

            # Canvas + 滚动条（缩放画布）
            canvas_frame = tk.Frame(parent, bg="#fafafa")
            canvas_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))
            self._canvas = tk.Canvas(canvas_frame, bg="#ffffff",
                                      highlightthickness=1, highlightbackground=COLOR_BORDER)
            x_sb = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self._canvas.xview)
            y_sb = ttk.Scrollbar(canvas_frame, orient="vertical", command=self._canvas.yview)
            self._canvas.configure(xscrollcommand=x_sb.set, yscrollcommand=y_sb.set)
            y_sb.pack(side="right", fill="y")
            x_sb.pack(side="bottom", fill="x")
            self._canvas.pack(side="left", fill="both", expand=True)

            # 鼠标滚轮缩放（Windows/macOS）
            self._canvas.bind("<MouseWheel>", self._on_mouse_wheel)
            # Linux 滚轮
            self._canvas.bind("<Button-4>", lambda e: self._set_zoom(self._zoom * 1.1))
            self._canvas.bind("<Button-5>", lambda e: self._set_zoom(self._zoom / 1.1))
            # 拖动平移
            self._canvas.bind("<ButtonPress-1>", self._pan_start)
            self._canvas.bind("<B1-Motion>", self._pan_move)
            self._pan_state = None

            self._render_canvas_image()
        except Exception as e:
            tk.Label(parent, text=f"PNG 加载失败：{e}",
                     font=(FONT_FAMILY[0], 10), fg=COLOR_MUTED, bg="#fafafa").pack(padx=4, pady=20)

    def _render_canvas_image(self):
        """按当前 _zoom 把原图绘制到 Canvas。"""
        if not hasattr(self, "_orig_pil_image") or self._orig_pil_image is None:
            return
        w0, h0 = self._orig_pil_image.size
        zw = max(1, int(w0 * self._zoom))
        zh = max(1, int(h0 * self._zoom))
        resized = self._orig_pil_image.resize((zw, zh), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)
        # 保留引用，否则被 GC
        self._keep_ref = getattr(self, "_keep_ref", [])
        self._keep_ref.append(photo)
        self._canvas.delete("all")
        self._canvas.create_image(0, 0, anchor="nw", image=photo)
        self._canvas.configure(scrollregion=(0, 0, zw, zh))
        if hasattr(self, "_zoom_label"):
            self._zoom_label.configure(text=f"{int(self._zoom * 100)}%")

    def _set_zoom(self, new_zoom: float):
        new_zoom = max(0.1, min(8.0, new_zoom))
        if abs(new_zoom - self._zoom) < 1e-4:
            return
        self._zoom = new_zoom
        self._render_canvas_image()

    def _on_mouse_wheel(self, event):
        # Windows: event.delta 是 120 的倍数
        if event.delta > 0:
            self._set_zoom(self._zoom * 1.1)
        elif event.delta < 0:
            self._set_zoom(self._zoom / 1.1)
        return "break"

    def _pan_start(self, event):
        self._canvas.scan_mark(event.x, event.y)
        self._pan_state = (event.x, event.y)

    def _pan_move(self, event):
        self._canvas.scan_dragto(event.x, event.y, gain=1)

    def _save_png(self, png_path: Path):
        dst = filedialog.asksaveasfilename(defaultextension=".png",
                                            initialfile=png_path.name,
                                            filetypes=[("PNG 文件", "*.png"), ("全部", "*.*")])
        if dst:
            try:
                Path(dst).write_bytes(png_path.read_bytes())
                messagebox.showinfo("已保存", f"PNG 已保存到\n{dst}")
            except Exception as e:
                messagebox.showerror("保存失败", str(e))

    def _save(self, path: Path):
        dst = filedialog.asksaveasfilename(defaultextension=".svg",
                                            initialfile=path.name,
                                            filetypes=[("SVG 文件", "*.svg"), ("全部", "*.*")])
        if dst:
            try:
                Path(dst).write_bytes(path.read_bytes())
                messagebox.showinfo("已保存", f"已保存到 {dst}")
            except Exception as e:
                messagebox.showerror("保存失败", str(e))


class ImagePage(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master, bg=COLOR_BG)
        self.switch = switch
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        head.pack(fill="x", padx=8, pady=(8, 6))
        tk.Label(head, text="增删设备对比图片", font=(FONT_FAMILY[0], 14, "bold"),
                 fg="#183b64", bg=COLOR_PANEL).pack(side="left", padx=18, pady=10)
        tk.Label(head, text="增删前 = 美化图（标准化排版）；增删后 = add/del 验证图",
                 font=(FONT_FAMILY[0], 10), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(side="left", padx=18, pady=10)

        scroll = ScrollFrame(self, bg=COLOR_BG)
        scroll.pack(fill="both", expand=True)

        # 增删对比组：(标题, 美化前SVG, 增删后SVG, 美化前标签, 增删后标签)
        groups = [
            ("LINE215 增加站房前后对比",
             SVG_DIR / "LINE215_beautified.svg",
             SVG_DIR / "LINE215_add_station_000300.svg",
             "调整前（美化图）", "增加站房后"),
            ("LINE216 删除开关前后对比",
             SVG_DIR / "LINE216_beautified.svg",
             SVG_DIR / "LINE216_del_switch_00024.svg",
             "调整前（美化图）", "删除开关后"),
        ]
        for title, before_svg, after_svg, bl, al in groups:
            card = tk.Frame(scroll.inner, bg=COLOR_PANEL, highlightthickness=1,
                             highlightbackground=COLOR_BORDER)
            card.pack(fill="x", padx=8, pady=8)
            tk.Label(card, text=title, font=(FONT_FAMILY[0], 13, "bold"),
                     fg=COLOR_TEXT, bg=COLOR_PANEL).pack(anchor="w", padx=16, pady=(12, 8))
            row = tk.Frame(card, bg=COLOR_PANEL)
            row.pack(fill="x", padx=16, pady=(0, 12))
            for svg_path, label, color in [(before_svg, bl, COLOR_WARN), (after_svg, al, COLOR_SUCCESS)]:
                col = tk.Frame(row, bg=COLOR_PANEL, highlightthickness=1,
                                highlightbackground=COLOR_BORDER)
                col.pack(side="left", fill="both", expand=True, padx=6)
                tk.Label(col, text=label, font=(FONT_FAMILY[0], 11, "bold"),
                         fg="#fff", bg=color).pack(fill="x", pady=4)
                body = tk.Frame(col, bg="#fafafa")
                body.pack(fill="both", expand=True, padx=8, pady=8)
                self._render_svg(body, svg_path)

    def _render_svg(self, parent, svg_path: Path):
        """优先用预渲染 PNG 回退，SVG 失败则文本提示。"""
        png_path = _png_for_svg(svg_path)
        if png_path:
            # 用预渲染 PNG：直接 Pillow → PhotoImage
            try:
                img = Image.open(str(png_path))
                img.thumbnail((800, 550))
                photo = ImageTk.PhotoImage(img)
                parent._keep_ref = getattr(parent, "_keep_ref", [])
                parent._keep_ref.append(photo)
                tk.Label(parent, image=photo, bg="#fafafa").pack(padx=4, pady=4)
                # 加保存 PNG 按钮
                btn = tk.Frame(parent, bg="#fafafa")
                btn.pack(fill="x", pady=(2, 4))
                ttk.Button(btn, text="💾 保存 PNG 到本地",
                           command=lambda: self._save_png(png_path)).pack(pady=2)
                return
            except Exception:
                pass
        if not svg_path.exists():
            tk.Label(parent, text=f"文件不存在：\n{svg_path.name}",
                     font=(FONT_FAMILY[0], 10), fg=COLOR_MUTED, bg="#fafafa",
                     justify="left").pack(padx=4, pady=20)
            return
        mount_svg_preview(parent, svg_path, max_size=(800, 550))

    def _save_png(self, png_path: Path):
        dst = filedialog.asksaveasfilename(defaultextension=".png",
                                            initialfile=png_path.name,
                                            filetypes=[("PNG 文件", "*.png"), ("全部", "*.*")])
        if dst:
            try:
                Path(dst).write_bytes(png_path.read_bytes())
                messagebox.showinfo("已保存", f"PNG 已保存到\n{dst}")
            except Exception as e:
                messagebox.showerror("保存失败", str(e))


# ----------------------------------------------------------------------
# 一键运行页面
# ----------------------------------------------------------------------
class RunPage(tk.Frame):
    """交互式运行界面：用户选择模式和线路，直接触发 main.py 子进程。"""
    def __init__(self, master, switch):
        super().__init__(master, bg=COLOR_BG)
        self.switch = switch
        self._proc = None
        self._running = False
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        head.pack(fill="x", padx=8, pady=(8, 6))
        tk.Label(head, text="⚡ 一键运行", font=(FONT_FAMILY[0], 14, "bold"),
                 fg="#183b64", bg=COLOR_PANEL).pack(side="left", padx=18, pady=10)

        scroll = ScrollFrame(self, bg=COLOR_BG)
        scroll.pack(fill="both", expand=True)

        # 模式选择
        self._section(scroll.inner, "选择运行模式")
        modes = [
            ("--all", "全功能模式（建议配合线路）", "⚙️",
             "python main.py --all --line LINE215\n运行全部功能（拓扑校验+图模比对+SVG+美化）"),
            ("--topo", "仅拓扑校验", "🔌",
             "python main.py --topo\n仅执行拓扑结构完整性校验（E01-E07）"),
            ("--svg", "仅 SVG 编辑与自动出图", "🖼",
             "python main.py --svg\n仅运行 SVG 交互编辑与自动出图"),
            ("--line", "图模比对（指定单线路）", "📊",
             "python main.py --line LINE215\n对指定线路进行图模一致性校验与评分"),
            ("--line --hybrid", "图模比对 + 混合智能校验", "🧠",
             "python main.py --line LINE215 --hybrid\n混合智能校验（子图+全网双报告），输出增强报告"),
            ("--line --hybrid --repair", "混合智能校验 + 修复评分", "🔧",
             "python main.py --line LINE215 --hybrid --repair\n含混合智能+修复后评分（不写库）"),
            ("--line --hybrid --repair --no-beautify", "混合智能 + 修复评分（跳过美化）", "⚡",
             "python main.py --line LINE215 --hybrid --repair --no-beautify\n跳过 SVG 美化步骤，加速运行"),
            ("--parse-only", "仅解析 SVG（不跑校验）", "📝",
             "python main.py --parse-only LINE215\n仅解析 SVG 并生成 JSON，不执行拓扑校验"),
        ]
        mode_frame = tk.Frame(scroll.inner, bg=COLOR_BG)
        mode_frame.pack(fill="x", padx=8, pady=(0, 8))

        self._selected_mode = tk.StringVar(value="--line --hybrid --repair")
        for val, label, icon, _ in modes:
            rb = tk.Radiobutton(
                mode_frame, text=f"  {icon}  {label}", variable=self._selected_mode,
                value=val, font=(FONT_FAMILY[0], 10), fg=COLOR_TEXT, bg=COLOR_BG,
                anchor="w", selectcolor=COLOR_PANEL, activebackground=COLOR_BG,
                command=self._update_cmd
            )
            rb.pack(fill="x", padx=16, pady=2)

        # 线路选择
        self._section(scroll.inner, f"选择线路（数据集共 {len(LINES)} 条）")
        line_frame = tk.Frame(scroll.inner, bg=COLOR_BG)
        line_frame.pack(fill="x", padx=8, pady=(0, 8))
        self._selected_line = tk.StringVar(value=LINES[0] if LINES else "LINE215")
        # 使用 Combobox 支持 143 条线路的下拉选择
        combo_box = ttk.Combobox(
            line_frame, textvariable=self._selected_line,
            values=LINES, state="readonly", width=24
        )
        combo_box.pack(side="left", padx=16, pady=4)
        combo_box.bind("<<ComboboxSelected>>", lambda _: self._update_cmd())
        # 搜索小输入
        tk.Label(line_frame, text="筛选：", font=(FONT_FAMILY[0], 10),
                 fg=COLOR_MUTED, bg=COLOR_BG).pack(side="left", padx=(20, 4))
        self._line_filter = tk.StringVar()
        filter_entry = ttk.Entry(line_frame, textvariable=self._line_filter, width=18)
        filter_entry.pack(side="left", padx=(0, 4), pady=4)
        filter_entry.bind("<KeyRelease>", lambda _: self._filter_lines(combo_box))
        # 快捷按钮：填入全部、按数字排序
        ttk.Button(line_frame, text="刷新线路列表",
                   command=lambda: self._refresh_lines(combo_box)).pack(side="left", padx=8)

        # 预览命令
        self._section(scroll.inner, "生成的命令")
        cmd_card = tk.Frame(scroll.inner, bg="#0e1a2b", highlightthickness=1,
                             highlightbackground=COLOR_BORDER)
        cmd_card.pack(fill="x", padx=8, pady=(0, 8))
        self._cmd_label = tk.Label(
            cmd_card, text="python main.py --line --hybrid --repair LINE215",
            font=("Consolas", 11), fg="#4ade80", bg="#0e1a2b",
            anchor="w", padx=20, pady=14, justify="left"
        )
        self._cmd_label.pack(fill="x")

        # 运行按钮
        btn_frame = tk.Frame(scroll.inner, bg=COLOR_BG)
        btn_frame.pack(fill="x", padx=8, pady=(4, 12))
        self._run_btn = ttk.Button(
            btn_frame, text="🚀 开始运行", command=self._do_run
        )
        self._run_btn.pack(side="left", padx=6)
        ttk.Button(btn_frame, text="🔄 停止运行", command=self._do_stop).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="📋 复制命令", command=self._copy_cmd).pack(side="left", padx=6)

        # 输出日志
        self._section(scroll.inner, "运行日志")
        log_card = tk.Frame(scroll.inner, bg="#0e1a2b", highlightthickness=1,
                             highlightbackground=COLOR_BORDER)
        log_card.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self._log_txt = tk.Text(
            log_card, font=("Consolas", 10), bg="#0e1a2b", fg="#cdd7e6",
            insertbackground="#fff", relief="flat", wrap="word",
            state="disabled", height=18
        )
        self._log_txt.pack(fill="both", expand=True, side="left", padx=4, pady=4)
        vbar = ttk.Scrollbar(log_card, orient="vertical", command=self._log_txt.yview)
        vbar.pack(fill="y", side="right", padx=(0, 4))
        self._log_txt.configure(yscrollcommand=vbar.set)

        # 加载历史日志
        log_file = OUTPUT / "log" / "topology_verify.log"
        if log_file.exists():
            try:
                text = decode(log_file.read_bytes())
                self._append_log("=== 历史日志（最近 200 行）===\n" + "\n".join(text.splitlines()[-200:]))
            except Exception:
                pass

    def _section(self, parent, title: str):
        bar = tk.Frame(parent, bg=COLOR_BG)
        bar.pack(fill="x", padx=8, pady=(14, 6))
        tk.Frame(bar, bg=COLOR_PRIMARY, width=4).pack(side="left", fill="y", padx=(0, 8))
        tk.Label(bar, text=title, font=(FONT_FAMILY[0], 12, "bold"),
                 fg="#183b64", bg=COLOR_BG).pack(side="left")

    def _update_cmd(self):
        mode = self._selected_mode.get()
        line = self._selected_line.get()
        parts = mode.split()
        cmd = f"python main.py {' '.join(parts)} {line}"
        self._cmd_label.configure(text=cmd)

    def _filter_lines(self, combo_box):
        """按输入框筛选线路下拉选项。"""
        kw = self._line_filter.get().strip().lower()
        if not kw:
            values = list(LINES)
        else:
            values = [ln for ln in LINES if kw in ln.lower()]
        combo_box["values"] = values
        if values and self._selected_line.get() not in values:
            self._selected_line.set(values[0])
        self._update_cmd()

    def _refresh_lines(self, combo_box):
        """重新扫描数据集目录，刷新线路列表。"""
        global LINES
        LINES = _discover_all_lines()
        if not LINES:
            LINES = ["LINE215", "LINE216", "LINE111"]
        combo_box["values"] = LINES
        if self._selected_line.get() not in LINES and LINES:
            self._selected_line.set(LINES[0])
        self._update_cmd()
        messagebox.showinfo("刷新完成", f"已扫描到 {len(LINES)} 条线路")

    def _build_cmd_parts(self) -> tuple[str, list[str]]:
        mode = self._selected_mode.get()
        line = self._selected_line.get()
        parts = mode.split()
        # 若 parts 里已经有 line 或 parse-only，把 line 放最后
        return "python main.py", parts + [line]

    def _do_run(self):
        if self._running and self._proc and self._proc.poll() is None:
            messagebox.showwarning("运行中", "程序已在运行中，请等待或先停止。")
            return
        prog, args = self._build_cmd_parts()
        full_cmd = f"{prog} {' '.join(args)}"
        self._append_log(f"\n{'='*60}\n▶ {full_cmd}\n{'='*60}\n")
        self._running = True
        self._run_btn.configure(state="disabled")
        import threading, subprocess
        ROOT_PY = ROOT / "main.py"

        def _run():
            try:
                proc = subprocess.Popen(
                    [sys.executable, str(ROOT_PY)] + args,
                    cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace", bufsize=1
                )
                self._proc = proc
                for line in iter(proc.stdout.readline, ""):
                    if line:
                        self.after(0, self._append_log, line)
                proc.wait()
                self.after(0, self._on_done, proc.returncode)
            except Exception as ex:
                self.after(0, self._append_log, f"\n❌ 启动失败: {ex}\n")
                self.after(0, self._on_done, -1)

        threading.Thread(target=_run, daemon=True).start()

    def _do_stop(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            self._append_log("\n⏹ 已发送终止信号\n")
            self._running = False
            self._run_btn.configure(state="normal")
        else:
            messagebox.showinfo("提示", "没有正在运行的程序。")

    def _on_done(self, code: int):
        self._running = False
        self._run_btn.configure(state="normal")
        status = "✅ 成功完成" if code == 0 else f"⚠️ 已退出（代码 {code}）"
        self._append_log(f"\n{'='*60}\n{status}\n{'='*60}\n")

        # 一键运行成功后：自动把 output/svg/ 下所有新生成的 SVG 转成 PNG，
        # 这样用户切到「SVG 图纸」页时直接看到 PNG 图，无需再点渲染按钮。
        if code == 0:
            self.after(200, self._auto_generate_pngs)

        self.after(500, lambda: self.switch("line"))

    def _auto_generate_pngs(self):
        """遍历 output/svg/ 下所有 SVG，逐个调用 render_svg_png 写到 output/svg_png/。"""
        import threading
        self._append_log("\n🖼  开始自动渲染 SVG → PNG（供「SVG 图纸」页直接展示）...\n")

        def _worker():
            try:
                # 局部导入避免 GUI 启动阶段缺失依赖导致崩溃
                from scripts.visualization.gui_app import render_svg_png
            except Exception:
                # 同目录下直接 import 也兜底一次
                try:
                    import importlib
                    render_svg_png = importlib.import_module("scripts.visualization.gui_app").render_svg_png
                except Exception as ex:
                    self.after(0, self._append_log, f"  ⚠️ 跳过（导入渲染器失败）：{ex}\n")
                    return

            if not SVG_DIR.exists():
                self.after(0, self._append_log, "  ⚠️ 未发现 output/svg/ 目录，跳过 PNG 生成。\n")
                return
            SVG_PNG_DIR.mkdir(parents=True, exist_ok=True)

            svgs = sorted(p for p in SVG_DIR.glob("*.svg") if p.is_file())
            if not svgs:
                self.after(0, self._append_log, "  ℹ output/svg/ 下没有 SVG 文件可渲染。\n")
                return

            for i, svg in enumerate(svgs, 1):
                png_path = SVG_PNG_DIR / (svg.stem + ".png")
                self.after(0, self._append_log, f"  [{i}/{len(svgs)}] {svg.name}  →  {png_path.name}\n")
                # 若 PNG 已存在且 mtime 早于 SVG，跳过（节省时间）
                if png_path.exists() and png_path.stat().st_mtime >= svg.stat().st_mtime:
                    self.after(0, self._append_log, f"      已存在且为最新，跳过。\n")
                    continue
                try:
                    png_bytes = render_svg_png(svg, width=1400)
                    if png_bytes:
                        png_path.write_bytes(png_bytes)
                        self.after(0, self._append_log,
                                   f"      ✅ 写入 {png_path.stat().st_size / 1024:.1f} KB\n")
                    else:
                        self.after(0, self._append_log, "      ⚠️ 渲染失败（请检查 Edge/cairosvg/svglib）\n")
                except Exception as ex:
                    self.after(0, self._append_log, f"      ❌ 异常：{ex}\n")

            self.after(0, self._append_log, "🎉 PNG 批量生成完成，可在「SVG 图纸」页查看。\n")

        threading.Thread(target=_worker, daemon=True).start()

    def _copy_cmd(self):
        prog, args = self._build_cmd_parts()
        cmd = f"{prog} {' '.join(args)}"
        self.clipboard_clear()
        self.clipboard_append(cmd)
        messagebox.showinfo("已复制", cmd)

    def _append_log(self, text: str):
        self._log_txt.configure(state="normal")
        self._log_txt.insert("end", text)
        self._log_txt.see("end")
        self._log_txt.configure(state="disabled")


# ----------------------------------------------------------------------
# 提交资料页面
# ----------------------------------------------------------------------
class SubmitPage(tk.Frame):
    def __init__(self, master, switch):
        super().__init__(master, bg=COLOR_BG)
        self.switch = switch
        self._build()

    def _build(self):
        head = tk.Frame(self, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        head.pack(fill="x", padx=8, pady=(8, 6))
        tk.Label(head, text="竞赛提交内容", font=(FONT_FAMILY[0], 14, "bold"),
                 fg="#183b64", bg=COLOR_PANEL).pack(side="left", padx=18, pady=10)

        scroll = ScrollFrame(self, bg=COLOR_BG)
        scroll.pack(fill="both", expand=True)

        # 三大类成果
        self._section(scroll.inner, "📦 提交材料压缩包")
        items = [
            ("5.1 现有 SVG 图形标准化美化排版",
             ["LINE215_beautified.svg", "LINE216_beautified.svg"],
             "LINE215、LINE216 标准化美化图及修正图",
             [SVG_DIR]),
            ("5.2 SVG 图形交互式增删设备",
             ["LINE215_add_station_000300.svg", "LINE216_del_switch_00024.svg"],
             "增加站房、删除开关的 SVG 验证图（左图=调整前美化图，右图=增删后）",
             [SVG_DIR]),
            ("5.3 自动生成 SVG 接线图",
             ["LINE215_single_line.svg", "LINE216_single_line.svg",
              "10kVLINE111_tie.svg", "SUB004_station_tie.svg",
              "TMP00034205_power_trace.svg"],
             "单线图、联络图、全站图、电源追溯图",
             [SVG_DIR]),
        ]
        for title, names, desc, dirs in items:
            self._item_card(scroll.inner, title, desc, names, dirs)

        # Excel
        self._section(scroll.inner, "📊 拓扑校验 Excel 报告")
        excel_card = tk.Frame(scroll.inner, bg=COLOR_PANEL, highlightthickness=1,
                                highlightbackground=COLOR_BORDER)
        excel_card.pack(fill="x", padx=8, pady=6)
        excel_files = sorted(OUTPUT.glob("*.xlsx"))
        if not excel_files:
            tk.Label(excel_card, text="运行主程序后，Excel 报告会显示在这里。",
                     font=(FONT_FAMILY[0], 10), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(padx=16, pady=20)
        for path in excel_files:
            row = tk.Frame(excel_card, bg=COLOR_PANEL)
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=f"📄  {path.name}", font=(FONT_FAMILY[0], 11),
                     fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left", pady=6)
            tk.Label(row, text=f"  {path.stat().st_size / 1024:.1f} KB",
                     font=(FONT_FAMILY[0], 9), fg=COLOR_MUTED, bg=COLOR_PANEL).pack(side="left")
            ttk.Button(row, text="打开所在文件夹", command=lambda p=path: self._open_in_explorer(p)).pack(side="right", padx=4)
            ttk.Button(row, text="复制路径", command=lambda p=path: self._copy(str(p))).pack(side="right", padx=4)

        # 全部文件清单
        self._section(scroll.inner, "🗂 成果文件一览")
        for name, paths in [
            ("分析报告", sorted(OUTPUT.glob("*.json"))),
            ("修复脚本", sorted(OUTPUT.glob("*.sql"))),
            ("SVG 图形", sorted(SVG_DIR.glob("*.svg"))),
            ("校验摘要", sorted(REPORT_DIR.glob("*.json"))),
        ]:
            exp = ttk.LabelFrame(scroll.inner, text=f"  {name}  ·  {len(list(paths))} 项  ", padding=8)
            exp.pack(fill="x", padx=8, pady=4)
            if not paths:
                tk.Label(exp, text="  （暂无）", fg=COLOR_MUTED,
                         bg=COLOR_PANEL, font=(FONT_FAMILY[0], 9)).pack(anchor="w")
                continue
            for p in paths:
                r = tk.Frame(exp, bg=COLOR_PANEL)
                r.pack(fill="x", pady=1)
                tk.Label(r, text=f"  {p.name}", font=(FONT_FAMILY[0], 10),
                         fg=COLOR_TEXT, bg=COLOR_PANEL, anchor="w").pack(side="left", fill="x", expand=True)
                ttk.Button(r, text="打开所在文件夹", command=lambda pp=p: self._open_in_explorer(pp)).pack(side="right", padx=2)

    def _section(self, parent, title: str):
        bar = tk.Frame(parent, bg=COLOR_BG)
        bar.pack(fill="x", padx=8, pady=(18, 8))
        tk.Frame(bar, bg=COLOR_WARN, width=4).pack(side="left", fill="y", padx=(0, 8))
        tk.Label(bar, text=title, font=(FONT_FAMILY[0], 13, "bold"),
                 fg="#183b64", bg=COLOR_BG).pack(side="left")

    def _item_card(self, parent, title: str, desc: str, names: list[str], dirs: list[Path]):
        card = tk.Frame(parent, bg=COLOR_PANEL, highlightthickness=1,
                         highlightbackground=COLOR_BORDER)
        card.pack(fill="x", padx=8, pady=6)
        head = tk.Frame(card, bg=COLOR_PANEL)
        head.pack(fill="x", padx=16, pady=(10, 6))
        tk.Label(head, text=title, font=(FONT_FAMILY[0], 12, "bold"),
                 fg=COLOR_TEXT, bg=COLOR_PANEL).pack(side="left")
        # 找第一个存在的目录
        existing_files = []
        for d in dirs:
            for n in names:
                p = d / n
                if p.exists():
                    existing_files.append(p)
        # 把同名分散目录的都加上
        for d in dirs:
            for n in names:
                p = d / n
                if p.exists() and p not in existing_files:
                    existing_files.append(p)
        if existing_files:
            ttk.Button(head, text="📦  打包下载",
                        command=lambda f=existing_files: self._zip(f, title.replace(' ', ''))).pack(side="right")
        # 缩略图网格容器（每张 SVG 一张缩略图，统一展示）
        thumbs_frame = tk.Frame(card, bg=COLOR_PANEL)
        thumbs_frame.pack(fill="x", padx=16, pady=(4, 4))
        # 用 grid 平铺，3 列
        for col in range(3):
            thumbs_frame.grid_columnconfigure(col, weight=1, uniform="thumbs")

        existing_paths: list[Path] = []
        idx = 0
        for n in names:
            found = next(((d / n) for d in dirs if (d / n).exists()), None)
            if not found:
                continue
            existing_paths.append(found)
            r, c = divmod(idx, 3)
            idx += 1
            # 缩略图卡片
            thumb = tk.Frame(thumbs_frame, bg="#fafafa", highlightthickness=1,
                              highlightbackground=COLOR_BORDER)
            thumb.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            # 标题栏：文件名 + 操作按钮
            head_r = tk.Frame(thumb, bg="#fafafa")
            head_r.pack(fill="x", padx=4, pady=(4, 2))
            tk.Label(head_r, text=f"  ✓  {n}", font=(FONT_FAMILY[0], 9),
                     fg=COLOR_SUCCESS, bg="#fafafa", anchor="w").pack(side="left", fill="x", expand=True)
            ttk.Button(head_r, text="打开", width=5,
                        command=lambda p=found: self._open_one(p)).pack(side="right", padx=1)
            ttk.Button(head_r, text="复制路径", width=8,
                        command=lambda p=found: self._copy(str(p))).pack(side="right", padx=1)
            # 缩略图画布（PNG → 实时渲染 SVG）
            body = tk.Frame(thumb, bg="#fafafa", height=160)
            body.pack(fill="both", expand=True, padx=4, pady=(0, 4))
            body.pack_propagate(False)
            png_path = _png_for_svg(found)
            if png_path:
                # 用 SvgPage 同款带放大缩小的预览（缩略图尺寸）
                self._render_thumb_with_zoom(body, found, png_path)
            else:
                # 没 PNG：实时渲染（多级回退，渲染完顺手写一份 png）
                self._render_thumb_fallback(body, found)

        # 若整个分类一个文件都没找到，保留旧的"✗ 文件名（运行相应模块后显示）"提示
        if not existing_paths:
            for n in names:
                row = tk.Frame(card, bg=COLOR_PANEL)
                row.pack(fill="x", padx=16, pady=2)
                tk.Label(row, text=f"  ✗  {n}（运行相应模块后显示）",
                         font=(FONT_FAMILY[0], 10), fg="#9aa6b8", bg=COLOR_PANEL).pack(side="left")
        tk.Frame(card, bg=COLOR_PANEL, height=8).pack()

    def _render_thumb_with_zoom(self, parent, svg_path: Path, png_path: Path):
        """缩略图：PNG + 鼠标滚轮缩放/拖动（与「SVG 图纸」页一致）。
        使用局部类 ZoomableThumb 自管理状态，避免污染 SubmitPage 自身。
        """
        try:
            ZoomableThumb(parent, png_path)
        except Exception as e:
            tk.Label(parent, text=f"PNG 加载失败：{e}",
                     font=(FONT_FAMILY[0], 8), fg=COLOR_MUTED, bg="#fafafa").pack(padx=4, pady=10)

    def _render_thumb_fallback(self, parent, svg_path: Path):
        """缩略图：PNG 不存在 → 实时渲染 SVG → 渲染成功顺手写一份 png 进 svg_png/。
        这样下次进入页面就能直接用 PNG 通道，速度更快。
        """
        # 尝试实时渲染
        try:
            png_bytes = render_svg_png(svg_path, width=1200)
            if png_bytes:
                # 写一份 PNG 缓存（供下次及「SVG 图纸」页用），渲染与缓存一起做
                cache_png = None
                try:
                    SVG_PNG_DIR.mkdir(parents=True, exist_ok=True)
                    cache_png = SVG_PNG_DIR / (svg_path.stem + ".png")
                    cache_png.write_bytes(png_bytes)
                    # 写成功 → 用 ZoomableThumb 显示（带放大缩小）
                    try:
                        tk.Label(parent, text="💡 已渲染并缓存",
                                 font=(FONT_FAMILY[0], 8), fg=COLOR_MUTED, bg="#fafafa").pack(pady=(0, 2))
                        ZoomableThumb(parent, cache_png, initial_zoom=0.4)
                    except Exception:
                        pass
                    return
                except Exception:
                    # 写文件失败（权限等），但渲染本身成功 → 用内存中的 png_bytes 直接显示
                    pass
                # 写文件失败时走这里：用 BytesIO 方式显示（不带 ZoomableThumb）
                from io import BytesIO
                img = Image.open(BytesIO(png_bytes))
                img.thumbnail((400, 280))
                photo = ImageTk.PhotoImage(img)
                parent._keep_ref = getattr(parent, "_keep_ref", [])
                parent._keep_ref.append(photo)
                tk.Label(parent, image=photo, bg="#fafafa").pack(padx=2, pady=2)
                tk.Label(parent, text="⚠️ 缓存失败，但已渲染",
                         font=(FONT_FAMILY[0], 8), fg=COLOR_MUTED, bg="#fafafa").pack(pady=(0, 2))
                return
        except Exception:
            pass
        # Pillow 直开兜底
        try:
            img = Image.open(str(svg_path))
            img.thumbnail((400, 280))
            photo = ImageTk.PhotoImage(img)
            parent._keep_ref = getattr(parent, "_keep_ref", [])
            parent._keep_ref.append(photo)
            tk.Label(parent, image=photo, bg="#fafafa").pack(padx=2, pady=2)
            return
        except Exception:
            pass
        # 文本兜底
        try:
            text = prepare_inline_svg(svg_path.read_bytes())
            tk.Label(parent, text=text[:600] + ("\n……" if len(text) > 600 else ""),
                     font=("Consolas", 8), bg="#fafafa", fg=COLOR_TEXT,
                     justify="left", anchor="nw").pack(fill="both", expand=True)
        except Exception:
            tk.Label(parent, text=f"无法渲染 {svg_path.name}",
                     bg="#fafafa", fg=COLOR_MUTED).pack(padx=10, pady=20)

    def _zip(self, files: list[Path], default_name: str):
        import zipfile, io
        dst = filedialog.asksaveasfilename(defaultextension=".zip",
                                            initialfile=f"{default_name}.zip",
                                            filetypes=[("ZIP 压缩包", "*.zip"), ("全部", "*.*")])
        if not dst:
            return
        try:
            with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
                for p in files:
                    zf.write(p, p.name)
            messagebox.showinfo("打包完成", f"已保存到 {dst}")
        except Exception as e:
            messagebox.showerror("打包失败", str(e))

    def _open_one(self, p: Path):
        try:
            if sys.platform.startswith("win"):
                import os
                os.startfile(str(p))  # type: ignore[attr-defined]
            else:
                webbrowser.open(p.as_uri())
        except Exception:
            messagebox.showerror("打开失败", str(p))

    def _open_in_explorer(self, p: Path):
        try:
            if sys.platform.startswith("win"):
                import subprocess
                subprocess.Popen(["explorer", "/select,", str(p)])
            else:
                webbrowser.open(p.parent.as_uri())
        except Exception as e:
            messagebox.showerror("打开失败", str(e))

    def _copy(self, text: str):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("已复制", text)


# ----------------------------------------------------------------------
# 主窗口
# ----------------------------------------------------------------------
class App(tk.Tk):
    PAGES = [
        ("项目概览", "overview", "📊"),
        ("⚡ 一键运行", "run", "🚀"),
        ("线路成果", "line", "⚡"),
        ("SVG 图纸", "svg", "🖼"),
        ("增删对比", "image", "🔍"),
        ("提交资料", "submit", "📦"),
    ]

    def __init__(self):
        super().__init__()
        self.title("主配网拓扑校验与图形成果展示  ·  桌面版")
        self.geometry("1400x860")
        self.minsize(1100, 680)
        self.configure(bg=COLOR_BG)

        # 设置 ttk 样式
        self._setup_style()

        # 顶部 Header
        self._build_header()

        # 主体 = 侧栏 + 内容
        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content(body)

    def _setup_style(self):
        style = ttk.Style(self)
        # 使用 'clam' 以支持更多颜色定制
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Notebook
        style.configure("TNotebook", background=COLOR_PANEL, borderwidth=0)
        style.configure("TNotebook.Tab",
                         background="#eef4fa", foreground=COLOR_TEXT,
                         padding=(18, 8), font=(FONT_FAMILY[0], 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", COLOR_PRIMARY)],
                  foreground=[("selected", "#ffffff")])

        # Buttons
        style.configure("TButton",
                         background="#ffffff", foreground=COLOR_TEXT,
                         padding=(10, 6), font=(FONT_FAMILY[0], 10))
        style.map("TButton",
                  background=[("active", "#eef4fa")],
                  foreground=[("disabled", "#9aa6b8")])

        style.configure("Nav.TButton",
                         background=COLOR_SIDEBAR, foreground=COLOR_SB_TEXT,
                         padding=(14, 12), font=(FONT_FAMILY[0], 11), anchor="w")
        style.map("Nav.TButton",
                  background=[("active", COLOR_SB_HOVER),
                               ("selected", COLOR_SB_ACTIVE)],
                  foreground=[("selected", "#ffffff")])

        style.configure("Treeview",
                         background="#ffffff", foreground=COLOR_TEXT,
                         fieldbackground="#ffffff", rowheight=26,
                         font=(FONT_FAMILY[0], 10))
        style.configure("Treeview.Heading",
                         background="#eef4fa", foreground="#183b64",
                         font=(FONT_FAMILY[0], 10, "bold"), relief="flat")
        style.map("Treeview",
                  background=[("selected", COLOR_PRIMARY)],
                  foreground=[("selected", "#ffffff")])

        style.configure("TCombobox", padding=4)

    def _build_header(self):
        header = tk.Frame(self, bg=COLOR_PRIMARY, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # 用 Canvas 实现渐变（tkinter 不支持 frame 渐变）
        canvas = tk.Canvas(header, height=64, highlightthickness=0)
        canvas.pack(fill="x")

        def _paint():
            canvas.delete("all")
            w = canvas.winfo_width()
            for i in range(w):
                r = int(24 + (0 - 24) * (i / max(1, w)))
                g = int(144 + (168 - 144) * (i / max(1, w)))
                b = int(255 + (84 - 255) * (i / max(1, w)))
                color = f"#{r:02x}{g:02x}{b:02x}"
                canvas.create_line(i, 0, i, 64, fill=color)
            canvas.create_text(20, 22, anchor="nw",
                               text="⚡  主配网拓扑校验与图形成果展示",
                               font=(FONT_FAMILY[0], 16, "bold"), fill="#ffffff")
            canvas.create_text(20, 46, anchor="nw",
                               text="电力拓扑与图模校验技术竞赛 · 拓扑校验、缺陷定位、修复建议与 SVG 成果",
                               font=(FONT_FAMILY[0], 9), fill="#e6f7ff")

        canvas.bind("<Configure>", lambda _: _paint())
        # 在右侧显示时间和操作
        right = tk.Frame(header, bg=COLOR_PRIMARY)
        right.place(relx=1.0, rely=0.5, anchor="e", x=-20, y=0)
        ttk.Button(right, text="📂  打开输出目录",
                     command=lambda: self._open_path(OUTPUT)).pack(side="right", padx=4)
        ttk.Button(right, text="🔄  刷新",
                     command=self._refresh_current).pack(side="right", padx=4)

    def _build_sidebar(self, master):
        self.sidebar = tk.Frame(master, bg=COLOR_SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="  ·  导航  ·", font=(FONT_FAMILY[0], 10),
                 fg="#5d7793", bg=COLOR_SIDEBAR).pack(fill="x", pady=(20, 8), padx=18, anchor="w")
        tk.Frame(self.sidebar, bg="#1e2c44", height=1).pack(fill="x", padx=18)

        self.nav_buttons: dict[str, ttk.Button] = {}
        for label, key, icon in self.PAGES:
            btn = ttk.Button(self.sidebar, text=f"  {icon}    {label}",
                              style="Nav.TButton",
                              command=lambda k=key: self.switch(k))
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

        # 信息块
        tk.Frame(self.sidebar, bg="#1e2c44", height=1).pack(fill="x", padx=18, pady=(20, 0))
        info = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR)
        info.pack(side="bottom", fill="x", padx=18, pady=18)
        tk.Label(info, text="电力拓扑与图模校验技术竞赛", font=(FONT_FAMILY[0], 9),
                 fg="#5d7793", bg=COLOR_SIDEBAR).pack(anchor="w")
        tk.Label(info, text="tkinter 桌面版 v1.0", font=(FONT_FAMILY[0], 9),
                 fg="#5d7793", bg=COLOR_SIDEBAR).pack(anchor="w")
        tk.Label(info, text=f"成果目录：\n{OUTPUT}", font=(FONT_FAMILY[0], 8),
                 fg="#5d7793", bg=COLOR_SIDEBAR, justify="left").pack(anchor="w", pady=(6, 0))

    def _build_content(self, master):
        self.container = tk.Frame(master, bg=COLOR_BG)
        self.container.pack(side="left", fill="both", expand=True)

        self.pages: dict[str, tk.Frame] = {}
        for label, key, icon in self.PAGES:
            page_cls = {
                "overview": OverviewPage,
                "run": RunPage,
                "line": LinePage,
                "svg": SvgPage,
                "image": ImagePage,
                "submit": SubmitPage,
            }[key]
            page = page_cls(self.container, self.switch)
            self.pages[key] = page

        self.switch("overview")

    def switch(self, key: str):
        for k, page in self.pages.items():
            page.pack_forget()
        self.pages[key].pack(fill="both", expand=True)

    def _refresh_current(self):
        """销毁当前页并重建。"""
        key = self._current_key()
        cls = {
            "overview": OverviewPage, "run": RunPage,
            "line": LinePage, "svg": SvgPage,
            "image": ImagePage, "submit": SubmitPage,
        }[key]
        self.pages[key].destroy()
        self.pages[key] = cls(self.container, self.switch)
        self.switch(key)

    def _current_key(self) -> str:
        for k, p in self.pages.items():
            if p.winfo_ismapped():
                return k
        return "overview"

    def _open_path(self, p: Path):
        try:
            if sys.platform.startswith("win"):
                import subprocess
                subprocess.Popen(["explorer", str(p)])
            else:
                webbrowser.open(p.as_uri())
        except Exception as e:
            messagebox.showerror("打开失败", str(e))


def main():
    try:
        app = App()
        app.mainloop()
    except Exception as exc:  # 捕获 GUI 启动错误，便于排查
        import traceback
        tb = traceback.format_exc()
        # 写一份错误日志
        try:
            log_path = OUTPUT / "log" / "gui_error.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text(tb, encoding="utf-8")
        except Exception:
            pass
        # 在一个新 tk 窗口里展示错误
        try:
            import tkinter as _tk
            from tkinter import scrolledtext
            win = _tk.Tk()
            win.title("GUI 启动失败")
            win.geometry("900x500")
            _tk.Label(win, text="桌面 GUI 启动失败，错误详情如下：",
                       fg="#e74747", font=(FONT_FAMILY[0], 12, "bold")).pack(pady=8)
            st = scrolledtext.ScrolledText(win, font=("Consolas", 10), wrap="word")
            st.pack(fill="both", expand=True, padx=12, pady=(0, 8))
            st.insert("1.0", tb)
            _tk.Button(win, text="关闭", command=win.destroy).pack(pady=(0, 12))
            win.mainloop()
        except Exception:
            # 兜底：用 cmd 提示
            print(tb)


if __name__ == "__main__":
    main()
