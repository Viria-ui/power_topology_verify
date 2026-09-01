# -*- coding: utf-8 -*-
"""将图模校验与分析结果导出为比赛标准 Excel 格式（5 个工作表）。"""
from __future__ import annotations

import re
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from config.settings import DATASET_STANDARD_OUTPUT_XLSX

SHEET_DEFECTS = "拓扑校验问题清单"
SHEET_BREAKPOINTS = "拓扑连通性异常诊断与断点定位结果"
SHEET_TIE = "联络开关自动识别与可视化梳理任务结果"
SHEET_LOOP = "非计划性合环拓扑识别任务结果"
SHEET_SCORE = "模型修正质量评分任务结果"
DROPDOWN_SHEET = "问题类型下拉选项"

SHEET_CONFIGS = {
    SHEET_DEFECTS: [
        "序号", "一级分类", "二级分类", "问题设备id", "问题设备名称",
        "所属馈线", "所属厂站", "问题说明", "修正方案", "修正sql",
    ],
    SHEET_BREAKPOINTS: [
        "序号", "起点设备id", "终点设备id", "断点类型",
        "本侧疑似断点设备id", "本侧疑似断点设备名称",
        "对侧疑似断点设备id", "对侧疑似断点设备名称",
        "修正方案", "修正sql",
    ],
    SHEET_TIE: [
        "线路id", "线路名称", "上级变电站名称", "联络开关id", "联络开关名称",
        "是否有联络", "联络线路id", "联络线路名称", "联络线变电站名称",
    ],
    SHEET_LOOP: [
        "线路id", "线路名称", "上级变电站名称", "合环线路id", "合环线路名称",
        "合环线变电站名称", "疑似联络开关id", "疑似联络开关名称", "修正sql",
    ],
    SHEET_SCORE: [
        "序号", "厂站名称", "厂站id", "馈线名称", "馈线id", "修正前评分", "修正后评分",
    ],
}

DEFECT_CATEGORY_MAP = {
    "图上有模型无": ("2 图模一致性校验", "2.1 图上有、模型无校验任务"),
    "模型有图上无": ("2 图模一致性校验", "2.2 模型有、图上无校验任务"),
    "物理连接不一致": ("2 图模一致性校验", "2.3 图形物理连通、拓扑逻辑断开校验任务"),
    "逻辑连接不一致": ("3 电气逻辑校验", "3.1 开关 - 电压基础状态匹配校验任务"),
}
DEFAULT_CATEGORY = ("2 图模一致性校验", "2.1 图上有、模型无校验任务")
_NAME_IN_DESC_RE = re.compile(r"设备\[([^\]]+)\]")


def _copy_cell_style(src, dst, *, wrap_text: bool = True) -> None:
    if src.has_style:
        dst.font = copy(src.font)
        dst.fill = copy(src.fill)
        dst.border = copy(src.border)
        dst.number_format = copy(src.number_format)
        dst.protection = copy(src.protection)
    src_al = src.alignment
    dst.alignment = Alignment(
        horizontal=getattr(src_al, "horizontal", None),
        vertical=getattr(src_al, "vertical", None) or "center",
        wrap_text=(
            getattr(src_al, "wrap_text", None)
            if getattr(src_al, "wrap_text", None) is not None
            else wrap_text
        ),
    )


def _resolve_equip_name(defect: dict) -> str:
    if defect.get("equip_name"):
        return str(defect["equip_name"])
    m = _NAME_IN_DESC_RE.search(defect.get("description", ""))
    if m:
        return m.group(1)
    if "<->" in str(defect.get("equip_id", "")):
        return "物理连接"
    return ""


def _resolve_station(defect: dict, default_station: str) -> str:
    if defect.get("station_id"):
        return str(defect["station_id"])
    if defect.get("dsubstation_id"):
        return str(defect["dsubstation_id"])
    return default_station or ""


def defect_to_standard_row(
    defect: dict,
    seq: int,
    line_name: str,
    default_station: str = "",
) -> dict[str, object]:
    cat1, cat2 = DEFECT_CATEGORY_MAP.get(defect.get("defect_type", ""), DEFAULT_CATEGORY)
    return {
        "序号": seq,
        "一级分类": cat1,
        "二级分类": cat2,
        "问题设备id": defect.get("equip_id", ""),
        "问题设备名称": _resolve_equip_name(defect),
        "所属馈线": line_name,
        "所属厂站": _resolve_station(defect, default_station),
        "问题说明": defect.get("description", ""),
        "修正方案": defect.get("suggestion", ""),
        "修正sql": defect.get("sql_draft", ""),
    }


def _read_sheet_meta(template_ws, headers: list[str]) -> tuple[dict, dict, object | None]:
    header_styles = {i + 1: template_ws.cell(1, i + 1) for i in range(len(headers))}
    col_widths = {
        get_column_letter(i + 1): template_ws.column_dimensions[get_column_letter(i + 1)].width
        for i in range(len(headers))
    }
    sample_cell = template_ws.cell(2, 1) if template_ws.max_row >= 2 else None
    return header_styles, col_widths, sample_cell


def _apply_header_row(ws, headers: list[str], header_styles: dict) -> None:
    for col_idx, title in enumerate(headers, start=1):
        cell = ws.cell(1, col_idx, title)
        src = header_styles.get(col_idx)
        if src is not None:
            _copy_cell_style(src, cell, wrap_text=True)


def _apply_column_widths(ws, col_widths: dict) -> None:
    for letter, width in col_widths.items():
        if width:
            ws.column_dimensions[letter].width = width


def _fill_sheet(
    ws,
    headers: list[str],
    rows: list[dict],
    header_styles: dict,
    col_widths: dict,
    sample_cell,
) -> None:
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)

    _apply_header_row(ws, headers, header_styles)
    _apply_column_widths(ws, col_widths)

    for row_idx, row_data in enumerate(rows, start=2):
        for col_idx, key in enumerate(headers, start=1):
            value = row_data.get(key, "")
            cell = ws.cell(row_idx, col_idx, value)
            if sample_cell is not None:
                _copy_cell_style(sample_cell, cell, wrap_text=True)
            else:
                cell.alignment = Alignment(vertical="center", wrap_text=True)


def _apply_defect_dropdowns(ws, last_row: int) -> None:
    if last_row < 2:
        return
    ws.data_validations = openpyxl.worksheet.datavalidation.DataValidationList()
    dv1 = DataValidation(type="list", formula1=f"{DROPDOWN_SHEET}!$A$1:$A$11", allow_blank=True)
    dv1.add(f"B2:B{last_row}")
    ws.add_data_validation(dv1)
    dv2 = DataValidation(type="list", formula1=f"{DROPDOWN_SHEET}!$B$1:$B$12", allow_blank=True)
    dv2.add(f"C2:C{last_row}")
    ws.add_data_validation(dv2)


def _build_defect_rows(defects: list[dict], line_name: str, default_station: str) -> list[dict]:
    return [
        defect_to_standard_row(d, idx, line_name, default_station)
        for idx, d in enumerate(defects, start=1)
    ]


def _flatten_tie_rows(tie_data) -> list[dict]:
    """接收单线路/批量分析结果，兼容 list、dict 与 DataFrame。"""
    if hasattr(tie_data, "to_dict") and hasattr(tie_data, "columns"):
        # pandas.DataFrame：此前在这里被当成未知类型而丢弃。
        return [row for row in tie_data.to_dict("records") if isinstance(row, dict)]
    if isinstance(tie_data, dict):
        if any(key in tie_data for key in ("联络开关id", "联络线路id", "是否有联络")):
            return [tie_data]
        rows = []
        for value in tie_data.values():
            rows.extend(_flatten_tie_rows(value))
        return rows
    if not isinstance(tie_data, list):
        return []
    return [row for row in tie_data if isinstance(row, dict)]


_TIE_HEADER_ALIASES = {
    # 标准模板当前使用“名称”后缀；同时兼容任务说明及历史版本的短字段名。
    "上级变电站名": "上级变电站名称",
    "上级变电站名称": "上级变电站名称",
    "联络线变电站": "联络线变电站名称",
    "联络线变电站名称": "联络线变电站名称",
}


def _normalise_tie_row(row: dict) -> dict:
    """将上游不同字段拼写统一为当前标准模板的列名。"""
    normalised = dict(row)
    for source, target in _TIE_HEADER_ALIASES.items():
        if source in row and row.get(source) not in (None, ""):
            normalised[target] = row[source]
    # 同时保留无后缀别名，保证换用历史模板时也能按其真实列名写入。
    if normalised.get("上级变电站名称") not in (None, ""):
        normalised["上级变电站名"] = normalised["上级变电站名称"]
    if normalised.get("联络线变电站名称") not in (None, ""):
        normalised["联络线变电站"] = normalised["联络线变电站名称"]
    return normalised


def _merge_tie_rows(tie_data) -> list[dict]:
    """汇总所有线路关系；同一线路存在“是”时移除占位的“否”。"""
    rows = [_normalise_tie_row(row) for row in _flatten_tie_rows(tie_data)]
    lines_with_tie = {
        str(row.get("线路id") or "") for row in rows
        if row.get("是否有联络") == "是"
    }
    merged: list[dict] = []
    seen: set[tuple] = set()
    for row in rows:
        line_id = str(row.get("线路id") or "")
        if row.get("是否有联络") == "否" and line_id in lines_with_tie:
            continue
        key = (
            line_id,
            str(row.get("联络开关id") or ""),
            str(row.get("联络线路id") or ""),
            str(row.get("是否有联络") or ""),
        )
        if key not in seen:
            seen.add(key)
            merged.append(row)
    return merged


def export_defects_xlsx(
    defects: list[dict],
    output_path: str | Path,
    line_name: str,
    *,
    template_path: str | Path | None = None,
    default_station: str = "",
    analysis: dict | None = None,
) -> Path:
    """基于标准模板导出完整 Excel 报告（前 5 个工作表）。"""
    template_path = Path(template_path or DATASET_STANDARD_OUTPUT_XLSX)
    output_path = Path(output_path)
    if not template_path.is_file():
        raise FileNotFoundError(f"未找到标准 Excel 模板: {template_path}")

    analysis = analysis or {}
    defect_rows = _build_defect_rows(defects, line_name, default_station)
    breakpoint_rows = analysis.get("breakpoints", [])
    # batch_tie_switches / all_tie_switches 可由批量调用方传入；单线路
    # 调用仍使用 tie_switches。合并后确保不会被邻线缺失时的“否”覆盖。
    tie_source = analysis.get(
        "batch_tie_switches",
        analysis.get("all_tie_switches", analysis.get("tie_switches", [])),
    )
    tie_source_rows = _flatten_tie_rows(tie_source)
    tie_rows = _merge_tie_rows(tie_source)
    print(
        f"[Excel] Sheet 3 联络源数据 {len(tie_source_rows)} 行，"
        f"汇总后 {len(tie_rows)} 行：{tie_rows}"
    )
    loop_rows = analysis.get("loops", [])
    score_rows = analysis.get("scores", [])

    wb = openpyxl.load_workbook(template_path)

    sheet_payloads = [
        (SHEET_DEFECTS, defect_rows),
        (SHEET_BREAKPOINTS, breakpoint_rows),
        (SHEET_TIE, tie_rows),
        (SHEET_LOOP, loop_rows),
        (SHEET_SCORE, score_rows),
    ]

    for sheet_name, rows in sheet_payloads:
        if sheet_name not in wb.sheetnames:
            continue
        headers = SHEET_CONFIGS[sheet_name]
        ws = wb[sheet_name]
        header_styles, col_widths, sample_cell = _read_sheet_meta(ws, headers)
        _fill_sheet(ws, headers, rows, header_styles, col_widths, sample_cell)
        if sheet_name == SHEET_DEFECTS and rows:
            _apply_defect_dropdowns(ws, len(rows) + 1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    wb.close()

    # 明确回读 Sheet 3，便于批量运行日志直接确认联络数据已落盘。
    check_wb = openpyxl.load_workbook(output_path, read_only=True, data_only=True)
    try:
        if SHEET_TIE in check_wb.sheetnames:
            check_ws = check_wb[SHEET_TIE]
            written_rows = list(check_ws.iter_rows(min_row=2, values_only=True))
            print(f"[Excel] Sheet 3 联络开关实际写入 {len(written_rows)} 行：{written_rows}")
    finally:
        check_wb.close()
    return output_path
