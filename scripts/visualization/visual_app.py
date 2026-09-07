from __future__ import annotations

import html as html_lib
import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"
SVG_DIR = OUTPUT_DIR / "svg"
REPORT_DIR = OUTPUT_DIR / "reports"

SVG_MANIFEST: list[dict[str, str]] = [
    {
        "name": "LINE215 单线图",
        "file": "LINE215_single_line.svg",
        "title": "5.3.1 单馈线单线图 - LINE215",
        "desc": "基于 SQL 馈线 LINE215 的设备结果展示，采用分层布局。",
        "logic": "_feeder_subgraph('LINE215') -> _project_to_device_graph -> _sugiyama_layout",
        "report": "LINE215_single_line_validate_summary.json",
    },
    {
        "name": "LINE216 单线图",
        "file": "LINE216_single_line.svg",
        "title": "5.3.1 单馈线单线图 - LINE216",
        "desc": "基于 SQL 馈线 LINE216 的设备结果展示，采用分层布局。",
        "logic": "_feeder_subgraph('LINE216') -> _project_to_device_graph -> _sugiyama_layout",
        "report": "LINE216_single_line_validate_summary.json",
    },
    {
        "name": "10kVLINE111 联络图",
        "file": "10kVLINE111_tie.svg",
        "title": "5.3.2 馈线联络关系图 - 10kVLINE111",
        "desc": "在馈线子图中识别联络开关，高亮联络边。",
        "logic": "_find_tie_neighbors('10kVLINE111') -> radial layout",
        "report": "10kVLINE111_tie_validate_summary.json",
    },
    {
        "name": "SUB004 全站联络总图",
        "file": "SUB004_station_tie.svg",
        "title": "5.3.3 全站馈线联络总图 - SUB004",
        "desc": "全站馈线横向排列，跨列联络以虚线跨列显示。",
        "logic": "_station_feeders_and_ties('SUB004') -> 5-column layout",
        "report": "SUB004_station_tie_validate_summary.json",
    },
    {
        "name": "TMP00034205 电源追踪",
        "file": "TMP00034205_power_trace.svg",
        "title": "5.3.4 电源追踪路径图 - 目标 TMP00034205",
        "desc": "从目标配变反向 BFS 追踪到电源，主路径蓝色、备路径橙色。",
        "logic": "_power_trace_paths('TMP00034205') -> Sugiyama layout",
        "report": "TMP00034205_power_trace_validate_summary.json",
    },
]

COMPARE_SUFFIX = "_质量评分与可解释置信度报告.json"
DEFECT_SUFFIX = "_缺陷清单报告.json"
REPAIR_SUFFIX = "_最小修改候选与SQL草案.json"
SQL_SUFFIX = "_正向修复与回滚脚本.sql"


def list_files(directory: Path, suffixes: tuple[str, ...]) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        path for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in suffixes
    )


def load_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text if limit is None else text[:limit]


def inject_style() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #f5f7fa; }
        .hero {
            background: linear-gradient(135deg, #1890FF, #00A854);
            color: white;
            padding: 18px 28px;
            border-radius: 12px;
            margin-bottom: 18px;
        }
        .hero h1 { margin: 0; font-size: 26px; line-height: 1.2; }
        .hero p { margin: 8px 0 0; opacity: 0.92; font-size: 13px; }
        .section-title { margin: 0 0 8px; color: #262626; font-size: 18px; font-weight: 700; }
        .desc { color: #595959; font-size: 13px; margin: 0 0 12px; }
        .info-box {
            margin-top: 12px;
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 8px;
            padding: 14px 18px;
            line-height: 1.8;
            font-size: 13px;
        }
        .info-box > div { margin: 2px 0; }
        .metric-cell {
            border: 1px solid #d8dee9;
            border-radius: 8px;
            padding: 12px 14px;
            background: #ffffff;
        }
        .metric-cell span { color: #667085; font-size: 13px; }
        .metric-cell strong { display: block; font-size: 24px; margin-top: 4px; }
        .panel {
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 10px;
            padding: 16px 18px;
        }
        .small-muted { color: #8c8c8c; font-size: 12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>配电网拓扑校验与修复展示系统</h1>
          <p>集中展示拓扑图纸、缺陷识别、质量评分、修复候选和 SQL 草案。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label: str, value: str, hint: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-cell">
          <span>{html_lib.escape(label)}</span>
          <strong>{html_lib.escape(value)}</strong>
          <div class="small-muted">{html_lib.escape(hint)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(items: list[tuple[str, str, str]]) -> None:
    cols = st.columns(len(items))
    for col, item in zip(cols, items, strict=False):
        with col:
            render_metric(*item)


def render_svg(svg_path: Path) -> None:
    raw_svg = read_text(svg_path)
    if not raw_svg:
        st.warning(f"未找到 SVG: {svg_path.name}")
        return
    components.html(
        f"""
        <div style="width:100%; height:760px; overflow:auto; border:1px solid #d0d5dd; background:#fff; border-radius:8px; padding:10px;">
            {raw_svg}
        </div>
        """,
        height=780,
        scrolling=True,
    )


def render_svg_frame(svg_path: Path) -> None:
    components.html(
        f"""
        <object data="{svg_path.as_uri()}" width="100%" height="760px" type="image/svg+xml"
                style="border:1px solid #d0d5dd; border-radius:8px; background:#fff;"></object>
        """,
        height=780,
        scrolling=False,
    )


def get_svg_meta(svg_path: Path) -> tuple[int, int]:
    summary_name = svg_path.stem + "_validate_summary.json"
    summary = load_json(REPORT_DIR / summary_name)
    if not isinstance(summary, dict):
        return 0, 0
    return int(summary.get("svg_device_count", 0) or 0), int(summary.get("total_defects", 0) or 0)


def load_diagram_manifest() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for item in SVG_MANIFEST:
        svg_path = SVG_DIR / item["file"]
        if svg_path.exists():
            new_item = dict(item)
            new_item["svg_path"] = svg_path
            new_item["size_kb"] = round(svg_path.stat().st_size / 1024, 1)
            new_item["device_count"], new_item["reported_defects"] = get_svg_meta(svg_path)
            items.append(new_item)
    return items


def load_compare_lines() -> list[str]:
    lines = set()
    for path in list_files(OUTPUT_DIR, (".json",)):
        name = path.name
        for suffix in (COMPARE_SUFFIX, DEFECT_SUFFIX, REPAIR_SUFFIX):
            if name.endswith(suffix):
                lines.add(name.removesuffix(suffix))
    for path in list_files(OUTPUT_DIR, (".sql",)):
        name = path.name
        if name.endswith(SQL_SUFFIX):
            lines.add(name.removesuffix(SQL_SUFFIX))
    return sorted(lines)


def collect_compare_bundle(line_name: str) -> dict[str, Any]:
    return {
        "score": load_json(OUTPUT_DIR / f"{line_name}{COMPARE_SUFFIX}"),
        "defects": load_json(OUTPUT_DIR / f"{line_name}{DEFECT_SUFFIX}"),
        "repair": load_json(OUTPUT_DIR / f"{line_name}{REPAIR_SUFFIX}"),
        "sql": read_text(OUTPUT_DIR / f"{line_name}{SQL_SUFFIX}", 20000),
        "single_line_summary": load_json(REPORT_DIR / f"{line_name}_single_line_validate_summary.json"),
        "svg_initial_summary": load_json(REPORT_DIR / f"{line_name}.svg_validation_initial_summary.json"),
        "svg_beautified_summary": load_json(REPORT_DIR / f"{line_name}.svg_validation_beautified_summary.json"),
        "ir_initial": load_json(REPORT_DIR / f"{line_name}.svg_ir_initial.json"),
        "ir_repaired": load_json(REPORT_DIR / f"{line_name}.svg_ir_repaired.json"),
        "ir_final": load_json(REPORT_DIR / f"{line_name}.svg_ir_final.json"),
        "beautify_compare": load_json(REPORT_DIR / f"{line_name}_美化质量对比报告.json"),
    }


def base_interaction_tab() -> None:
    st.subheader("图纸浏览")
    st.caption("支持 SVG 图纸查看、本地图纸预览和校验报告浏览。")

    svg_files = list_files(SVG_DIR, (".svg",))
    if not svg_files:
        st.warning("未发现可展示的 SVG 图纸文件。")
        return

    left, right = st.columns([0.30, 0.70], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        selected = st.selectbox(
            "选择要查看的拓扑图",
            svg_files,
            index=0,
            format_func=lambda path: path.name,
        )
        st.markdown(f"**文件路径：** `output/svg/{selected.name}`")
        st.markdown(f"**文件大小：** `{round(selected.stat().st_size / 1024, 1)} KB`")
        auto_index = SVG_DIR / "auto_index.html"
        if auto_index.exists():
            st.markdown("**图集页面：** `output/svg/auto_index.html`")
        st.markdown("</div>", unsafe_allow_html=True)

        uploaded = st.file_uploader("上传本地 PNG/JPG/SVG", type=["png", "jpg", "jpeg", "svg"], key="base_upload")
        if uploaded is not None:
            st.markdown("**上传预览**")
            if uploaded.name.lower().endswith(".svg"):
                svg_text = uploaded.getvalue().decode("utf-8", errors="ignore")
                components.html(
                    f'<div style="width:100%; height:360px; overflow:auto; border:1px solid #d0d5dd; background:#fff;">{svg_text}</div>',
                    height=380,
                )
            else:
                st.image(uploaded, use_container_width=True)

    with right:
        st.markdown(f'<div class="section-title">{html_lib.escape(selected.name)}</div>', unsafe_allow_html=True)
        st.markdown('<p class="desc">当前视图用于查看 SVG 拓扑图纸。</p>', unsafe_allow_html=True)
        render_svg(selected)
        st.markdown(
            """
            <div class="info-box">
              <div><b>说明：</b>左侧可切换图纸或上传本地图纸，右侧显示当前图纸内容。</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    report_files = list_files(REPORT_DIR, (".json",))
    if report_files:
        st.markdown("### 报告预览")
        report_cols = st.columns([0.32, 0.68], gap="large")
        with report_cols[0]:
            report_selected = st.selectbox(
                "选择报告 JSON",
                report_files,
                format_func=lambda path: path.name,
                index=0,
                key="base_report",
            )
        with report_cols[1]:
            report_data = load_json(report_selected)
            if isinstance(report_data, dict):
                st.json(report_data)
            elif isinstance(report_data, list):
                st.dataframe(pd.DataFrame(report_data).head(50), use_container_width=True, hide_index=True)
            else:
                st.code(read_text(report_selected, 12000))


def showcase_tab() -> None:
    st.subheader("成果看板")
    st.caption("展示拓扑成图、校验摘要、缺陷清单、修复候选和 SQL 草案。")

    diagrams = load_diagram_manifest()
    if not diagrams:
        st.warning("暂未发现可预览的 SVG 图纸文件。")
        return

    names = [item["name"] for item in diagrams]
    index = st.selectbox(
        "选择要展示的拓扑图",
        list(range(len(diagrams))),
        format_func=lambda i: names[i],
        index=0,
        key="showcase_svg",
    )
    item = diagrams[index]
    svg_path = item["svg_path"]
    report_data = load_json(REPORT_DIR / item["report"])

    render_metrics([
        ("设备统计", str(item["device_count"]), "来自校验摘要"),
        ("文件大小", f"{item['size_kb']} KB", "output/svg"),
        ("关联缺陷", str(item["reported_defects"]), "来自校验摘要"),
        ("图集页面", "auto_index", "output/svg"),
    ])

    left, right = st.columns([0.28, 0.72], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"**文件：** `{svg_path.name}`")
        st.markdown(f"**标题：** {item['title']}")
        st.markdown(f"**路径：** `output/svg/{svg_path.name}`")
        st.markdown(f"**处理流程：** {item['logic']}")
        st.markdown("</div>", unsafe_allow_html=True)

        auto_index = SVG_DIR / "auto_index.html"
        if auto_index.exists():
            st.link_button("打开图集页面", auto_index.as_uri(), use_container_width=True)

    with right:
        st.markdown(f'<div class="section-title">{html_lib.escape(item["title"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="desc">{html_lib.escape(item["desc"])}</p>', unsafe_allow_html=True)
        render_svg_frame(svg_path)
        if isinstance(report_data, dict):
            st.markdown(
                f"""
                <div class="info-box">
                  <div><b>图名：</b>{html_lib.escape(item["name"])}</div>
                  <div><b>通过率：</b>{html_lib.escape(str(report_data.get("pass_rate", "n/a")))}</div>
                  <div><b>说明：</b>该区域用于查看拓扑图纸的成图效果和校验摘要。</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 验证修复结果")
    line_names = load_compare_lines()
    if not line_names:
        st.info("暂未发现验证修复结果文件。")
        return

    selected_line = st.selectbox("选择要展示的修复结果", line_names, index=0, key="repair_line")
    bundle = collect_compare_bundle(selected_line)

    score_data = bundle.get("score") or {}
    score_summary = score_data.get("score_summary", {}) if isinstance(score_data, dict) else {}
    main_interface = score_data.get("main_interface", {}) if isinstance(score_data, dict) else {}
    defects = bundle.get("defects") or []
    repair = bundle.get("repair") or {}
    topology_delta = repair.get("topology_delta", {}) if isinstance(repair, dict) else {}
    candidates = repair.get("candidates", []) if isinstance(repair, dict) else []

    render_metrics([
        ("修复前评分", str(score_summary.get("score_before", "-")), "质量评分"),
        ("修复后评分", str(score_summary.get("score_after", "-")), "质量评分"),
        ("缺陷总数", str(score_summary.get("defect_count", len(defects) if isinstance(defects, list) else 0)), "缺陷清单"),
        ("修复候选", str(len(candidates)), "SQL 草案"),
    ])

    tabs = st.tabs(["评分摘要", "缺陷清单", "修复候选", "SQL 草案"])
    with tabs[0]:
        col1, col2 = st.columns([0.55, 0.45], gap="large")
        with col1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("**验证修复摘要**")
            st.json(score_data)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("**拓扑差异**")
            st.json(topology_delta)
            if main_interface:
                st.markdown("**主配接口复核**")
                st.json(main_interface)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("查看更多校验数据"):
            for title, data in {
                "单线校验摘要": bundle.get("single_line_summary"),
                "初始 SVG 校验摘要": bundle.get("svg_initial_summary"),
                "美化 SVG 校验摘要": bundle.get("svg_beautified_summary"),
                "美化前 IR": bundle.get("ir_initial"),
                "美化后 IR": bundle.get("ir_repaired"),
                "最终 IR": bundle.get("ir_final"),
                "美化质量对比": bundle.get("beautify_compare"),
            }.items():
                if data is not None:
                    st.markdown(f"**{title}**")
                    st.json(data)

    with tabs[1]:
        if isinstance(defects, list) and defects:
            defect_df = pd.DataFrame(defects)
            defect_type = st.selectbox(
                "按缺陷类型过滤",
                ["全部"] + sorted(defect_df["defect_type"].dropna().astype(str).unique().tolist()),
                key="defect_type_filter",
            )
            if defect_type != "全部":
                defect_df = defect_df[defect_df["defect_type"].astype(str) == defect_type]
            st.dataframe(defect_df.head(80), use_container_width=True, hide_index=True)
        else:
            st.info("当前没有可展示的缺陷清单。")

    with tabs[2]:
        if isinstance(candidates, list) and candidates:
            cand_df = pd.DataFrame(candidates)
            cols = [c for c in ["repair_id", "defect_type", "target_equip", "action", "impact_summary"] if c in cand_df.columns]
            action_filter = st.selectbox(
                "按修复动作过滤",
                ["全部"] + sorted(cand_df["action"].dropna().astype(str).unique().tolist()),
                key="action_filter",
            )
            if action_filter != "全部":
                cand_df = cand_df[cand_df["action"].astype(str) == action_filter]
            st.dataframe(cand_df[cols].head(120), use_container_width=True, hide_index=True)
        else:
            st.info("当前没有可展示的修复候选。")

        with st.expander("查看拓扑差异和候选明细"):
            st.json(topology_delta)
            st.json(candidates[:10] if isinstance(candidates, list) else candidates)

    with tabs[3]:
        sql_text = bundle.get("sql") or ""
        if sql_text:
            st.code(sql_text, language="sql")
        else:
            st.info("没有找到 SQL 草案文件。")


def report_tab() -> None:
    st.subheader("报告总览")
    report_files = list_files(REPORT_DIR, (".json",))
    if not report_files:
        st.info("暂未发现 output/reports 下的 JSON 报告。")
        return

    selected = st.selectbox(
        "选择报告 JSON",
        report_files,
        format_func=lambda path: path.name,
        index=0,
        key="report_json",
    )
    data = load_json(selected)
    col1, col2 = st.columns([0.35, 0.65], gap="large")
    with col1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"**文件：** `{selected.name}`")
        st.markdown(f"**路径：** `output/reports/{selected.name}`")
        st.markdown(f"**大小：** `{round(selected.stat().st_size / 1024, 1)} KB`")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if isinstance(data, dict):
            st.json(data)
        elif isinstance(data, list):
            st.dataframe(pd.DataFrame(data).head(100), use_container_width=True, hide_index=True)
        else:
            st.code(read_text(selected, 12000))


def main() -> None:
    st.set_page_config(
        page_title="配电网拓扑校验与修复展示系统",
        page_icon="⚡",
        layout="wide",
    )
    inject_style()
    render_hero()
    st.caption("图纸浏览、成果看板和报告总览集中在一个交互窗口中。")

    tab1, tab2, tab3 = st.tabs(["图纸浏览", "成果看板", "报告总览"])
    with tab1:
        base_interaction_tab()
    with tab2:
        showcase_tab()
    with tab3:
        report_tab()


if __name__ == "__main__":
    main()
