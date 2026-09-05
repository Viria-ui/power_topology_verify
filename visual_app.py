from __future__ import annotations

import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


PROJECT_ROOT = Path(__file__).resolve().parent
SVG_DIR = PROJECT_ROOT / "output" / "svg"
REPORT_DIR = PROJECT_ROOT / "output" / "reports"


st.set_page_config(
    page_title="配电网拓扑图美化结果查看器",
    page_icon="⚡",
    layout="wide",
)


def list_files(directory: Path, suffixes: tuple[str, ...]) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in suffixes
    )


def render_svg(svg_path: Path) -> None:
    svg_text = svg_path.read_text(encoding="utf-8", errors="ignore")
    components.html(
        f"""
        <div style="width:100%; height:760px; overflow:auto; border:1px solid #d0d5dd; background:#fff;">
            {svg_text}
        </div>
        """,
        height=780,
        scrolling=True,
    )


def render_source(svg_path: Path) -> None:
    with st.expander("查看 SVG 源文件片段"):
        svg_text = svg_path.read_text(encoding="utf-8", errors="ignore")
        st.code(svg_text[:6000], language="xml")


def render_report_preview() -> None:
    report_files = list_files(REPORT_DIR, (".json",))
    if not report_files:
        st.info("暂未发现 output/reports 下的 JSON 报告。")
        return

    selected = st.selectbox(
        "选择校验报告",
        report_files,
        format_func=lambda path: path.name,
    )
    st.json(selected.read_text(encoding="utf-8", errors="ignore"))


def main() -> None:
    st.title("配电网拓扑图美化结果查看器")
    st.caption("运行后先进入这个窗口，用户可以选择具体美化后的拓扑图进行查看。")

    tab_svg, tab_upload, tab_report = st.tabs(["选择美化图", "上传图片/SVG", "查看报告"])

    with tab_svg:
        svg_files = list_files(SVG_DIR, (".svg",))
        if not svg_files:
            st.warning("没有找到 output/svg/*.svg，请先运行 SVG 生成或美化流程。")
            st.code("python run_svg_pipeline.py", language="bash")
            return

        left, right = st.columns([0.25, 0.75], gap="large")

        with left:
            selected = st.selectbox(
                "选择要查看的拓扑图",
                svg_files,
                index=0,
                format_func=lambda path: path.name,
            )
            st.write("文件路径")
            st.code(str(selected.relative_to(PROJECT_ROOT)))
            st.write("文件大小")
            st.code(f"{selected.stat().st_size / 1024:.1f} KB")

            auto_index = SVG_DIR / "auto_index.html"
            if auto_index.exists():
                st.link_button("打开自动索引页面", auto_index.as_uri(), use_container_width=True)

        with right:
            st.subheader(html.escape(selected.name))
            render_svg(selected)
            render_source(selected)

    with tab_upload:
        uploaded = st.file_uploader("上传本地 PNG/JPG/SVG 预览", type=["png", "jpg", "jpeg", "svg"])
        if uploaded is None:
            st.info("可以把队友生成的图拖到这里临时预览。")
        elif uploaded.name.lower().endswith(".svg"):
            svg_text = uploaded.getvalue().decode("utf-8", errors="ignore")
            components.html(
                f"""
                <div style="width:100%; height:760px; overflow:auto; border:1px solid #d0d5dd; background:#fff;">
                    {svg_text}
                </div>
                """,
                height=780,
                scrolling=True,
            )
        else:
            st.image(uploaded, use_container_width=True)

    with tab_report:
        render_report_preview()


if __name__ == "__main__":
    main()
