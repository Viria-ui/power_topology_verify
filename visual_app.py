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
        "desc": "基于 SQL 馈线 LINE215 的所有设备，BFS Sugiyama 分层布局，主干绿色 #00A854。",
        "logic": "_feeder_subgraph('LINE215') → _project_to_device_graph → _sugiyama_layout 分层渲染",
        "summary": "LINE215_single_line_validate_summary.json",
    },
    {
        "name": "LINE216 单线图",
        "file": "LINE216_single_line.svg",
        "title": "5.3.1 单馈线单线图 - LINE216",
        "desc": "基于 SQL 馈线 LINE216 的所有设备，BFS Sugiyama 分层布局，主干绿色 #00A854。",
        "logic": "_feeder_subgraph('LINE216') → _project_to_device_graph → _sugiyama_layout 分层渲染",
        "summary": "LINE216_single_line_validate_summary.json",
    },
    {
        "name": "10kVLINE111 联络图",
        "file": "10kVLINE111_tie.svg",
        "title": "5.3.2 馈线联络关系图 - 10kVLINE111",
        "desc": "在馈线子集 + 邻接馈线中查找联络开关，联络线高亮橙色。",
        "logic": "_find_tie_neighbors('10kVLINE111') 抽取联络关系 → 中心放射布局",
        "summary": "10kVLINE111_tie_validate_summary.json",
    },
    {
        "name": "SUB004 全站联络总图",
        "file": "SUB004_station_tie.svg",
        "title": "5.3.3 全站馈线联络总图 - SUB004",
        "desc": "SUB004 站房下所有馈线横向排列，馈线间联络开关以橙色虚线跨列连接。",
        "logic": "_station_feeders_and_ties('SUB004') 收集馈线 + 联络 → 5 列栅格布局绘制",
        "summary": "SUB004_station_tie_validate_summary.json",
    },
    {
        "name": "TMP00034205 电源追溯",
        "file": "TMP00034205_power_trace.svg",
        "title": "5.3.4 电源追溯路径图 - 目标 TMP00034205",
        "desc": "从目标配变反向 BFS 追溯到电源；主供路径实线蓝，备供路径虚线橙。",
        "logic": "_power_trace_paths('TMP00034205') 主/备供路径 → Sugiyama 布局渲染",
        "summary": "TMP00034205_power_trace_validate_summary.json",
    },
]


def list_files(directory: Path, suffixes: tuple[str, ...]) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        path
        for path in directory.iterdir()
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
        .stApp {
            background: #f5f7fa;
        }
        .hero {
            background: linear-gradient(135deg, #1890FF, #00A854);
            color: white;
            padding: 18px 28px;
            border-radius: 12px;
            margin-bottom: 18px;
        }
        .hero h1 {
            margin: 0;
            font-size: 26px;
            line-height: 1.2;
        }
        .hero p {
            margin: 8px 0 0;
            opacity: 0.92;
            font-size: 13px;
        }
        .section-title {
            margin: 0 0 8px;
            color: #262626;
            font-size: 18px;
            font-weight: 700;
        }
        .desc {
            color: #595959;
            font-size: 13px;
            margin: 0 0 12px;
        }
        .info-box {
            margin-top: 12px;
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 8px;
            padding: 14px 18px;
            line-height: 1.8;
            font-size: 13px;
        }
        .info-box > div {
            margin: 2px 0;
        }
        .metric-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(150px, 1fr));
            gap: 12px;
            margin: 0 0 14px;
        }
        .metric-cell {
            border: 1px solid #d8dee9;
            border-radius: 8px;
            padding: 12px 14px;
            background: #ffffff;
        }
        .metric-cell span {
            color: #667085;
            font-size: 13px;
        }
        .metric-cell strong {
            display: block;
            font-size: 24px;
            margin-top: 4px;
        }
        .panel {
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 10px;
            padding: 16px 18px;
        }
        .chip {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            margin-right: 6px;
        }
        .chip-pass { background: #f6ffed; color: #389e0d; }
        .chip-warn { background: #fff7e6; color: #d48806; }
        .chip-fail { background: #fff1f0; color: #cf1322; }
        .code-box {
            background: #0f172a;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 12px 14px;
            overflow: auto;
            font-size: 12px;
            line-height: 1.55;
        }
        .small-muted {
            color: #8c8c8c;
            font-size: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>配电网拓扑图美化结果查看器</h1>
          <p>页面风格对齐 output/svg/auto_index.html，同时整合验证修复模块成果、缺陷清单、评分与 SQL 草案。</p>
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
    st.markdown('<div class="metric-strip">', unsafe_allow_html=True)
    cols = st.columns(len(items))
    for col, item in zip(cols, items, strict=False):
        with col:
            render_metric(*item)
    st.markdown('</div>', unsafe_allow_html=True)


def render_svg(svg_path: Path) -> None:
    raw_svg = read_text(svg_path)
    if not raw_svg:
        st.warning(f"未找到 SVG：{svg_path.name}")
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
    lines = []
    for path in list_files(OUTPUT_DIR, (".json",)):
        name = path.name
        if name.endswith("_质量评分与可解释置信度报告.json"):
            lines.append(name.replace("_质量评分与可解释置信度报告.json", ""))
    return sorted(set(lines))


def collect_compare_bundle(line_name: str) -> dict[str, Any]:
    bundle: dict[str, Any] = {
        "score": load_json(OUTPUT_DIR / f"{line_name}_质量评分与可解释置信度报告.json"),
        "defects": load_json(OUTPUT_DIR / f"{line_name}_缺陷清单报告.json"),
        "repair": load_json(OUTPUT_DIR / f"{line_name}_最小修改候选与SQL草案.json"),
        "sql": read_text(OUTPUT_DIR / f"{line_name}_正向修复与回滚脚本.sql", 12000),
        "single_line_summary": load_json(REPORT_DIR / f"{line_name}_single_line_validate_summary.json"),
        "svg_initial_summary": load_json(REPORT_DIR / f"{line_name}.svg_validation_initial_summary.json"),
        "svg_beautified_summary": load_json(REPORT_DIR / f"{line_name}.svg_validation_beautified_summary.json"),
        "ir_initial": load_json(REPORT_DIR / f"{line_name}.svg_ir_initial.json"),
        "ir_repaired": load_json(REPORT_DIR / f"{line_name}.svg_ir_repaired.json"),
        "ir_final": load_json(REPORT_DIR / f"{line_name}.svg_ir_final.json"),
        "beautify_compare": load_json(OUTPUT_DIR / f"{line_name}_美化质量对比报告.json"),
    }
    return bundle


def render_manifest_tab() -> None:
    diagrams = load_diagram_manifest()
    if not diagrams:
        st.warning("暂未发现可预览的 SVG 图，请先生成 output/svg 下的文件。")
        return

    names = [item["name"] for item in diagrams]
    index = st.selectbox("选择要查看的拓扑图", list(range(len(diagrams))), format_func=lambda i: names[i], index=0)
    item = diagrams[index]
    svg_path = item["svg_path"]

    left, right = st.columns([0.28, 0.72], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"**文件：** `{svg_path.name}`")
        st.markdown(f"**路径：** `output/svg/{svg_path.name}`")
        st.markdown(f"**文件大小：** `{item['size_kb']} KB`")
        st.markdown(f"**节点统计：** `{item['device_count']}`")
        st.markdown(f"**验证缺陷：** `{item['reported_defects']}`")
        auto_index = SVG_DIR / "auto_index.html"
        if auto_index.exists():
            st.markdown("**参考页面：** `output/svg/auto_index.html`")
            st.caption("如果你本地要直接看静态页面，可双击这个文件。")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(f'<div class="section-title">{html_lib.escape(item["title"])}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="desc">{html_lib.escape(item["desc"])}</p>', unsafe_allow_html=True)
        render_svg(svg_path)
        st.markdown(
            f"""
            <div class="info-box">
              <div><b>图名：</b>{html_lib.escape(item["name"])}</div>
              <div><b>生成逻辑：</b>{html_lib.escape(item["logic"])}</div>
              <div><b>节点/缺陷：</b>设备={item["device_count"]} ｜ 相关缺陷={item["reported_defects"]}</div>
              <div><b>校验入口：</b>与 `output/svg/auto_index.html` 的内容风格保持一致</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_repair_tab() -> None:
    line_names = load_compare_lines()
    if not line_names:
        st.warning("未发现 compare 输出，请先运行 `python tests/compare.py --line LINE215 LINE216`。")
        return

    selected = st.selectbox("选择要展示的修复结果", line_names, index=0)
    bundle = collect_compare_bundle(selected)

    score_data = bundle.get("score") or {}
    score_summary = score_data.get("score_summary", {}) if isinstance(score_data, dict) else {}
    main_interface = score_data.get("main_interface", {}) if isinstance(score_data, dict) else {}
    defects = bundle.get("defects") or []
    repair = bundle.get("repair") or {}
    topology_delta = repair.get("topology_delta", {}) if isinstance(repair, dict) else {}
    candidates = repair.get("candidates", []) if isinstance(repair, dict) else []

    render_metrics([
        ("修复前评分", str(score_summary.get("score_before", "-")), "compare.py 产出"),
        ("修复后评分", str(score_summary.get("score_after", "-")), "compare.py 产出"),
        ("缺陷总数", str(score_summary.get("defect_count", len(defects) if isinstance(defects, list) else 0)), "缺陷清单"),
        ("修复候选", str(len(candidates)), "最小修改候选"),
    ])

    tabs = st.tabs(["验证摘要", "缺陷清单", "修复候选", "SQL 草案"])

    with tabs[0]:
        col1, col2 = st.columns([0.55, 0.45], gap="large")
        with col1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("**验证修复模块摘要**")
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

        summary_items = {
            "单线校验摘要": bundle.get("single_line_summary"),
            "初始 SVG 校验摘要": bundle.get("svg_initial_summary"),
            "美化 SVG 校验摘要": bundle.get("svg_beautified_summary"),
            "美化前 IR": bundle.get("ir_initial"),
            "美化后 IR": bundle.get("ir_repaired"),
            "最终 IR": bundle.get("ir_final"),
            "美化质量对比": bundle.get("beautify_compare"),
        }
        with st.expander("展开更多校验产物"):
            for title, data in summary_items.items():
                if data is not None:
                    st.markdown(f"**{title}**")
                    st.json(data)

    with tabs[1]:
        if isinstance(defects, list) and defects:
            defect_df = pd.DataFrame(defects)
            defect_type = st.selectbox("按缺陷类型过滤", ["全部"] + sorted(defect_df["defect_type"].dropna().astype(str).unique().tolist()))
            if defect_type != "全部":
                defect_df = defect_df[defect_df["defect_type"].astype(str) == defect_type]
            st.dataframe(defect_df.head(50), use_container_width=True, hide_index=True)
            st.caption(f"共 {len(defects)} 条，当前显示前 {min(50, len(defect_df))} 条")
        else:
            st.info("当前线路没有可展示的缺陷清单。")

    with tabs[2]:
        if isinstance(candidates, list) and candidates:
            cand_df = pd.DataFrame(candidates)
            action_filter = st.selectbox("按修复动作过滤", ["全部"] + sorted(cand_df["action"].dropna().astype(str).unique().tolist()))
            if action_filter != "全部":
                cand_df = cand_df[cand_df["action"].astype(str) == action_filter]
            st.dataframe(cand_df[["repair_id", "defect_type", "target_equip", "action", "impact_summary"]].head(80), use_container_width=True, hide_index=True)
        else:
            st.info("当前线路没有修复候选数据。")

        with st.expander("查看 topology_delta 与候选原文"):
            st.json(topology_delta)
            st.json(candidates[:10] if isinstance(candidates, list) else candidates)

    with tabs[3]:
        sql_text = bundle.get("sql") or ""
        if sql_text:
            st.code(sql_text, language="sql")
        else:
            st.info("没有找到 SQL 草案文件。")


def render_report_tab() -> None:
    report_files = list_files(REPORT_DIR, (".json",))
    if not report_files:
        st.info("暂未发现 output/reports 下的 JSON 报告。")
        return

    selected = st.selectbox("选择报告 JSON", report_files, format_func=lambda path: path.name, index=0)
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
        else:
            st.code(read_text(selected, 12000))


def main() -> None:
    st.set_page_config(
        page_title="配电网拓扑图美化结果查看器",
        page_icon="⚡",
        layout="wide",
    )
    inject_style()
    render_hero()

    st.caption("运行后先进入这个窗口，用户可以选择具体美化后的拓扑图、查看 compare.py 的修复结果，并打开 auto_index.html 对照。")
    tab1, tab2, tab3 = st.tabs(["图集预览", "验证修复", "报告总览"])

    with tab1:
        render_manifest_tab()

    with tab2:
        render_repair_tab()

    with tab3:
        render_report_tab()


if __name__ == "__main__":
    main()
