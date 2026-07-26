# -*- coding: utf-8 -*-
"""将 SQL 转 GBK，并生成《图模字段映射表 v1》Excel；导出 LINE215 映射样例。"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_SRC = Path(
    r"d:\挑战杯\挑战杯\CP-202606-面向新型电力系统的配电网图模拓扑智能识别与修正研究比赛资料"
    r"\sql形式数据集"
)
SVG_SRC = Path(
    r"d:\挑战杯\挑战杯\CP-202606-面向新型电力系统的配电网图模拓扑智能识别与修正研究比赛资料"
    r"\svg\配网 svg\LINE215.svg"
)
SQL_GBK_DIR = PROJECT_ROOT / "input" / "sql_gbk"
DOCS_DIR = PROJECT_ROOT / "docs"
OUT_CSV = PROJECT_ROOT / "output" / "csv"
OUT_JSON = PROJECT_ROOT / "output" / "json"
EXCEL_PATH = DOCS_DIR / "图模字段映射表_v1.xlsx"
SAMPLE_DIR = DOCS_DIR / "svg_parse_sample_LINE215"


def detect_and_decode(raw: bytes) -> tuple[str, str]:
    for enc in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def convert_sql_to_gbk() -> list[dict]:
    SQL_GBK_DIR.mkdir(parents=True, exist_ok=True)
    reports = []
    gbk = "gbk"
    for src in sorted(SQL_SRC.glob("*.sql")):
        raw = src.read_bytes()
        text, src_enc = detect_and_decode(raw)
        dst = SQL_GBK_DIR / src.name
        dst.write_bytes(text.encode(gbk, errors="replace"))
        reports.append(
            {
                "文件名": src.name,
                "源编码识别": src_enc,
                "目标编码": gbk,
                "源字节数": len(raw),
                "目标字节数": dst.stat().st_size,
                "输出路径": str(dst),
            }
        )
        print(f"[GBK] {src.name}: {src_enc} -> {gbk}")
    return reports


def extract_insert_columns(sql_text: str) -> list[str]:
    m = re.search(r'INSERT INTO .*?\("(.*?)"\)\s*VALUES', sql_text, re.S)
    if not m:
        return []
    return [c.strip() for c in m.group(1).split('","')]


def build_sql_dict_sheets() -> tuple[pd.DataFrame, pd.DataFrame]:
    table_meta = [
        ("EQUIP_JBS_PWEQUIPINFO.sql", "JBS_PWEQUIPINFO", "配网设备主表"),
        ("EQUIP_JBS_PWFEEDERLINE.sql", "JBS_PWFEEDERLINE", "配网馈线/线路表"),
        ("EQUIP_JBS_PWTERMINAL.sql", "JBS_PWTERMINAL", "配网设备端子表"),
        ("EQUIP_JBS_PWROOM.sql", "JBS_PWROOM", "配网站房表"),
        ("EQUIP_JBS_VOLTAGETYPE.sql", "JBS_VOLTAGETYPE", "电压等级字典"),
        ("EQUIP_JBS_ZD_OBJECT.sql", "JBS_ZD_OBJECT", "设备类型字典"),
        ("EQUIP_JBS_ZWEQUIPINFO.sql", "JBS_ZWEQUIPINFO", "主网设备主表"),
        ("EQUIP_JBS_ZWTERMINAL.sql", "JBS_ZWTERMINAL", "主网设备端子表"),
        ("EQUIP_JBS_ZWLINEEND.sql", "JBS_ZWLINEEND", "主网线路端点表"),
        ("EQUIP_JBS_ZWSUBSTATION.sql", "JBS_ZWSUBSTATION", "主网变电站表"),
        ("EQUIP_JBS_PWREAL.sql", "JBS_PWREAL", "配网量测实值"),
        ("EQUIP_JBS_ZWMEA.sql", "JBS_ZWMEA", "主网量测"),
        ("EQUIP_JBS_ZWSIGNAL.sql", "JBS_ZWSIGNAL", "主网信号"),
        ("EQUIP_JBS_ZD_MEASTYPE.sql", "JBS_ZD_MEASTYPE", "量测类型字典"),
        ("date.sql", "date", "日期辅助数据"),
    ]
    field_desc = {
        ("JBS_PWEQUIPINFO", "EQUIP_ID"): ("PK", "设备主键", "对 SVG ObjectID"),
        ("JBS_PWEQUIPINFO", "EQUIP_NAME"): ("", "设备名称", "辅配 ObjectName"),
        ("JBS_PWEQUIPINFO", "EQUIP_TYPE"): ("FK→ZD_OBJECT.OBJ_CODE", "设备类型编码", "对 element_type"),
        ("JBS_PWEQUIPINFO", "VOLTAGE_TYPE"): ("FK→VOLTAGETYPE", "电压等级编码", "主/配网拆分"),
        ("JBS_PWEQUIPINFO", "FEEDER_ID"): ("FK→PWFEEDERLINE.LINE_ID", "所属馈线", "对 SVG 文件名"),
        ("JBS_PWEQUIPINFO", "DSUBSTATION_ID"): ("FK→PWROOM.ROOM_ID", "所属站房", "站房归属"),
        ("JBS_PWEQUIPINFO", "COMPOSITESWITCH"): ("", "组合开关ID", "组合开关成员"),
        ("JBS_PWFEEDERLINE", "LINE_ID"): ("PK", "馈线/线路主键", "FEEDER_ID 外键目标"),
        ("JBS_PWFEEDERLINE", "LINE_NAME"): ("", "线路名称如LINE215", "对 SVG 文件名"),
        ("JBS_PWFEEDERLINE", "START_ST_ID"): ("FK", "起始站/电源侧ID", "拓扑电源锚点"),
        ("JBS_PWFEEDERLINE", "VOLTAGE_TYPE"): ("FK", "电压等级", "电压过滤"),
        ("JBS_PWTERMINAL", "ID"): ("PK", "端子主键", "SQL端点ID"),
        ("JBS_PWTERMINAL", "EQUIP_ID"): ("FK→PWEQUIPINFO", "所属设备", "端子归属"),
        ("JBS_PWTERMINAL", "CONNECTIVITYNODE_ID"): ("", "连接节点", "同节点即电气连通"),
        ("JBS_PWROOM", "ROOM_ID"): ("PK", "站房ID", "对 Substation"),
        ("JBS_PWROOM", "ROOM_NAME"): ("", "站房名称", "名称辅配"),
        ("JBS_PWROOM", "TOP_VOLTAGE_TYPE"): ("", "最高电压", ""),
        ("JBS_PWROOM", "FEEDER_ID"): ("FK", "所属馈线", ""),
        ("JBS_VOLTAGETYPE", "VOLTAGE_ID"): ("PK", "电压编码", ""),
        ("JBS_VOLTAGETYPE", "VOLTAGE_NAME"): ("", "电压名称", "如10kV"),
        ("JBS_ZD_OBJECT", "OBJ_ID"): ("PK", "对象字典ID", ""),
        ("JBS_ZD_OBJECT", "OBJ_CODE"): ("UK", "类型编码", "EQUIP_TYPE"),
        ("JBS_ZD_OBJECT", "OBJ_CNNAME"): ("", "中文类型名", "类型对照"),
        ("JBS_ZD_OBJECT", "OBJ_ENNAME"): ("", "英文类型名", "对 SVG layer"),
        ("JBS_ZWEQUIPINFO", "EQUIP_ID"): ("PK", "主网设备主键", "对 SVG ObjectID"),
        ("JBS_ZWEQUIPINFO", "EQUIP_NAME"): ("", "设备名称", ""),
        ("JBS_ZWEQUIPINFO", "EQUIP_TYPE"): ("FK", "类型编码", ""),
        ("JBS_ZWEQUIPINFO", "ST_ID"): ("FK", "所属变电站", ""),
        ("JBS_ZWEQUIPINFO", "VOLTAGE_TYPE"): ("FK", "电压等级", ""),
        ("JBS_ZWTERMINAL", "ID"): ("PK", "主网端子ID", "端点"),
        ("JBS_ZWTERMINAL", "EQUIP_ID"): ("FK", "所属设备", ""),
        ("JBS_ZWTERMINAL", "CONNECTIVITYNODE_ID"): ("", "连接节点", "电气连通"),
        ("JBS_ZWLINEEND", "LINEEND_ID"): ("PK", "线路端点ID", ""),
        ("JBS_ZWLINEEND", "LINEEND_NAME"): ("", "端点名称", ""),
        ("JBS_ZWLINEEND", "VOLTAGE_TYPE"): ("", "电压", ""),
        ("JBS_ZWLINEEND", "ST_ID"): ("FK", "所属站", ""),
    }

    rows = []
    rel_rows = []
    for fname, tname, tcn in table_meta:
        fpath = SQL_SRC / fname
        if not fpath.exists():
            continue
        text, _ = detect_and_decode(fpath.read_bytes())
        cols = extract_insert_columns(text)
        for col in cols:
            key = (tname, col)
            pkfk, meaning, usage = field_desc.get(key, ("", "", "图模关联待扩展"))
            rows.append(
                {
                    "SQL文件": fname,
                    "表名": tname,
                    "表说明": tcn,
                    "字段名": col,
                    "主键/外键": pkfk,
                    "中文含义": meaning or col,
                    "图模用途": usage,
                }
            )

    rel_rows = [
        {"关联编号": "R-SQL-01", "左表.字段": "JBS_PWEQUIPINFO.FEEDER_ID", "右表.字段": "JBS_PWFEEDERLINE.LINE_ID", "关系": "N:1", "说明": "设备归属馈线"},
        {"关联编号": "R-SQL-02", "左表.字段": "JBS_PWEQUIPINFO.EQUIP_TYPE", "右表.字段": "JBS_ZD_OBJECT.OBJ_CODE", "关系": "N:1", "说明": "设备类型字典"},
        {"关联编号": "R-SQL-03", "左表.字段": "JBS_PWEQUIPINFO.VOLTAGE_TYPE", "右表.字段": "JBS_VOLTAGETYPE.VOLTAGE_ID", "关系": "N:1", "说明": "电压等级"},
        {"关联编号": "R-SQL-04", "左表.字段": "JBS_PWEQUIPINFO.DSUBSTATION_ID", "右表.字段": "JBS_PWROOM.ROOM_ID", "关系": "N:1", "说明": "设备所属站房"},
        {"关联编号": "R-SQL-05", "左表.字段": "JBS_PWTERMINAL.EQUIP_ID", "右表.字段": "JBS_PWEQUIPINFO.EQUIP_ID", "关系": "N:1", "说明": "端子归属设备"},
        {"关联编号": "R-SQL-06", "左表.字段": "JBS_PWTERMINAL.CONNECTIVITYNODE_ID", "右表.字段": "同表同字段聚合", "关系": "N:N", "说明": "同连接节点=电气连通"},
        {"关联编号": "R-SQL-07", "左表.字段": "JBS_PWFEEDERLINE.LINE_NAME", "右表.字段": "SVG文件名(LINE215.svg)", "关系": "1:1", "说明": "馈线对单线图"},
        {"关联编号": "R-SQL-08", "左表.字段": "JBS_PWROOM.FEEDER_ID", "右表.字段": "JBS_PWFEEDERLINE.LINE_ID", "关系": "N:1", "说明": "站房归属馈线"},
        {"关联编号": "R-SQL-09", "左表.字段": "JBS_ZWTERMINAL.EQUIP_ID", "右表.字段": "JBS_ZWEQUIPINFO.EQUIP_ID", "关系": "N:1", "说明": "主网端子归属"},
        {"关联编号": "R-SQL-10", "左表.字段": "JBS_ZWEQUIPINFO.ST_ID", "右表.字段": "主网变电站/站ID", "关系": "N:1", "说明": "主网设备所属站"},
    ]
    return pd.DataFrame(rows), pd.DataFrame(rel_rows)


def build_svg_sheet() -> pd.DataFrame:
    rows = [
        {"解析字段": "element_id", "SVG来源": "g@id", "示例": "TMP_350d4db8-...", "对应SQL": "无直接字段(图元主键)", "说明": "图形元素唯一ID"},
        {"解析字段": "object_id", "SVG来源": "metadata/PSR_Ref@ObjectID", "示例": "TMP00046409", "对应SQL": "JBS_PWEQUIPINFO.EQUIP_ID", "说明": "图模主键对齐"},
        {"解析字段": "object_name", "SVG来源": "PSR_Ref@ObjectName", "示例": "配变2186", "对应SQL": "EQUIP_NAME", "说明": "名称辅配"},
        {"解析字段": "psr_type", "SVG来源": "PSR_Ref@PSRType", "示例": "0110", "对应SQL": "EQUIP_TYPE(辅证)", "说明": "CIM/PSR类型码"},
        {"解析字段": "element_type", "SVG来源": "Layer_id映射", "示例": "PowerTransformer", "对应SQL": "ZD_OBJECT.OBJ_ENNAME/中文名", "说明": "图层类型"},
        {"解析字段": "layer", "SVG来源": "Layer_Ref/图层g@id", "示例": "PowerTransformer_Layer", "对应SQL": "", "说明": "图层"},
        {"解析字段": "voltage_level", "SVG来源": "class如lkv10", "示例": "10kV", "对应SQL": "VOLTAGETYPE.VOLTAGE_NAME", "说明": "电压"},
        {"解析字段": "terminal_index", "SVG来源": "symbol use@terminal-index", "示例": "1/2", "对应SQL": "端子序/PWTERMINAL", "说明": "端点序号"},
        {"解析字段": "terminal_x/y", "SVG来源": "symbol+transform", "示例": "344.02,493.60", "对应SQL": "几何连通用", "说明": "端子坐标"},
        {"解析字段": "line_id", "SVG来源": "ConnLine/ACLineSegment g@id", "示例": "TMP_30b99c0b-...", "对应SQL": "无强制等值", "说明": "连接线图元ID"},
        {"解析字段": "line.object_id", "SVG来源": "线PSR_Ref@ObjectID", "示例": "", "对应SQL": "可对LINE_ID", "说明": "有则优先"},
        {"解析字段": "glink_refs", "SVG来源": "GLink_Ref@ObjectID", "示例": "", "对应SQL": "EQUIP_ID列表", "说明": "线关联设备"},
        {"解析字段": "from/to_element_id", "SVG来源": "几何最近端子推断", "示例": "TMP_111aff70-...", "对应SQL": "经object_id→EQUIP_ID", "说明": "连接两端图元"},
        {"解析字段": "from/to_terminal", "SVG来源": "最近端子序号", "示例": "1", "对应SQL": "PWTERMINAL序/PT_规则", "说明": "连接端点"},
        {"解析字段": "related_text", "SVG来源": "Text_Layer + TXT-前缀", "示例": "TXT-TMP_...", "对应SQL": "EQUIP_NAME展示", "说明": "标注关联"},
    ]
    return pd.DataFrame(rows)


def build_id_rules() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"规则编号": "M01", "源": "SVG.object_id", "目标": "SQL.EQUIP_ID", "匹配方式": "精确等值", "失败处理": "R003 图存模无", "优先级": "P0"},
            {"规则编号": "M02", "源": "SQL.EQUIP_ID", "目标": "SVG.object_id", "匹配方式": "精确等值", "失败处理": "R004 模存图无", "优先级": "P0"},
            {"规则编号": "M03", "源": "PWFEEDERLINE.LINE_NAME", "目标": "SVG文件名", "匹配方式": "LINE215 ↔ LINE215.svg；或10kVLINE215", "失败处理": "R006 馈线不匹配", "优先级": "P0"},
            {"规则编号": "M04", "源": "PWEQUIPINFO.FEEDER_ID", "目标": "PWFEEDERLINE.LINE_ID", "匹配方式": "外键等值后取LINE_NAME对文件", "失败处理": "设备无馈线", "优先级": "P0"},
            {"规则编号": "M05", "源": "SVG.element_id", "目标": "（仅图形）", "匹配方式": "不映射库主键；通过object_id挂设备", "失败处理": "—", "优先级": "P0"},
            {"规则编号": "M06", "源": "SVG.terminal_index", "目标": "point_id", "匹配方式": "优先PWTERMINAL.ID；否则PT_{EQUIP_ID}_{N}", "失败处理": "补模拟端点", "优先级": "P0"},
            {"规则编号": "M07", "源": "PWTERMINAL.CONNECTIVITYNODE_ID", "目标": "电气连通边", "匹配方式": "同节点端子互通", "失败处理": "断点检测", "优先级": "P0"},
            {"规则编号": "M08", "源": "SVG连接两端object_id", "目标": "模侧连通", "匹配方式": "几何最近端子(阈值<3px)→端子所属设备", "失败处理": "悬空/断点", "优先级": "P0"},
            {"规则编号": "M09", "源": "EQUIP_NAME / ObjectName", "目标": "辅配", "匹配方式": "object_id失败时同馈线内名称匹配", "失败处理": "人工复核", "优先级": "P1"},
            {"规则编号": "M10", "源": "EQUIP_TYPE / element_type", "目标": "类型一致校验", "匹配方式": "经ZD_OBJECT中英文对照", "失败处理": "类型不一致告警", "优先级": "P1"},
            {"规则编号": "M11", "源": "DSUBSTATION_ID / ROOM_ID", "目标": "SVG Substation.object_id", "匹配方式": "等值", "失败处理": "站房缺失", "优先级": "P1"},
            {"规则编号": "M12", "源": "端点命名规范", "目标": "统一ID", "匹配方式": "库端子用TERMINAL.ID；图端子无库ID时PT_{object_id}_{terminal_index}", "失败处理": "—", "优先级": "P0"},
        ]
    )


def build_type_map() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"OBJ_CODE": "1703", "OBJ_CNNAME": "配网变压器", "SVG_element_type": "PowerTransformer", "SVG中文": "变压器", "端子数建议": 2},
            {"OBJ_CODE": "1705", "OBJ_CNNAME": "配网断路器", "SVG_element_type": "Breaker", "SVG中文": "断路器", "端子数建议": 2},
            {"OBJ_CODE": "1706", "OBJ_CNNAME": "配网负荷开关", "SVG_element_type": "LoadBreakSwitch", "SVG中文": "负荷开关", "端子数建议": 2},
            {"OBJ_CODE": "1707", "OBJ_CNNAME": "配网熔断器", "SVG_element_type": "Fuse", "SVG中文": "熔断器", "端子数建议": 2},
            {"OBJ_CODE": "1708", "OBJ_CNNAME": "配网刀闸", "SVG_element_type": "Disconnector", "SVG中文": "隔离开关", "端子数建议": 2},
            {"OBJ_CODE": "1709", "OBJ_CNNAME": "配网接地刀闸", "SVG_element_type": "GroundDisconnector", "SVG中文": "接地刀闸", "端子数建议": 1},
            {"OBJ_CODE": "1710", "OBJ_CNNAME": "配网母线段", "SVG_element_type": "BusbarSection", "SVG中文": "母线", "端子数建议": "N"},
            {"OBJ_CODE": "1713", "OBJ_CNNAME": "配网电压互感器", "SVG_element_type": "PotentialTransformer", "SVG中文": "电压互感器", "端子数建议": 1},
            {"OBJ_CODE": "1714", "OBJ_CNNAME": "配网杆塔", "SVG_element_type": "PoleCode", "SVG中文": "杆塔", "端子数建议": "1+"},
            {"OBJ_CODE": "1719", "OBJ_CNNAME": "配网电力用户", "SVG_element_type": "EnergyConsumer", "SVG中文": "负荷", "端子数建议": 1},
            {"OBJ_CODE": "1720", "OBJ_CNNAME": "组合开关", "SVG_element_type": "CompositeSwitch", "SVG中文": "组合开关", "端子数建议": "N"},
            {"OBJ_CODE": "1702", "OBJ_CNNAME": "馈线段", "SVG_element_type": "ACLineSegment/ConnLine", "SVG中文": "交流线/连接线", "端子数建议": "边"},
            {"OBJ_CODE": "1301", "OBJ_CNNAME": "母线", "SVG_element_type": "BusbarSection", "SVG中文": "母线", "端子数建议": "N"},
            {"OBJ_CODE": "1311", "OBJ_CNNAME": "变压器", "SVG_element_type": "PowerTransformer", "SVG中文": "变压器", "端子数建议": 2},
            {"OBJ_CODE": "1321", "OBJ_CNNAME": "断路器", "SVG_element_type": "Breaker", "SVG中文": "断路器", "端子数建议": 2},
            {"OBJ_CODE": "1322", "OBJ_CNNAME": "隔离开关", "SVG_element_type": "Disconnector", "SVG中文": "隔离开关", "端子数建议": 2},
            {"OBJ_CODE": "1323", "OBJ_CNNAME": "接地刀闸", "SVG_element_type": "GroundDisconnector", "SVG中文": "接地刀闸", "端子数建议": 1},
            {"OBJ_CODE": "—", "OBJ_CNNAME": "连接点(图元)", "SVG_element_type": "Junction", "SVG中文": "连接点", "端子数建议": "1+"},
            {"OBJ_CODE": "—", "OBJ_CNNAME": "站房", "SVG_element_type": "Substation", "SVG中文": "站房", "端子数建议": "容器"},
            {"OBJ_CODE": "—", "OBJ_CNNAME": "终端设备", "SVG_element_type": "RemoteUnit", "SVG中文": "终端设备", "端子数建议": 1},
        ]
    )


def load_line215_samples() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    elem_csv = OUT_CSV / "LINE215.svg_elements.csv"
    conn_csv = OUT_CSV / "LINE215.svg_connections.csv"
    if not elem_csv.exists():
        raise FileNotFoundError(f"缺少解析结果: {elem_csv}")

    # 设备级去重样例
    seen = set()
    equip_rows = []
    with elem_csv.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            eid = row["element_id"]
            if eid in seen:
                continue
            seen.add(eid)
            oid = row.get("object_id") or ""
            equip_rows.append(
                {
                    "svg_file": "LINE215.svg",
                    "feeder_line_name": "LINE215",
                    "feeder_line_id": "TMP00000188",
                    "element_id": eid,
                    "object_id(=EQUIP_ID)": oid,
                    "object_name": row.get("object_name"),
                    "element_type": row.get("element_type"),
                    "element_type_cn": row.get("element_type_cn"),
                    "psr_type": row.get("psr_type"),
                    "voltage_level": row.get("voltage_level"),
                    "建议point_id_端子1": f"PT_{oid}_1" if oid else "",
                    "建议point_id_端子2": f"PT_{oid}_2" if oid else "",
                }
            )
            if len(equip_rows) >= 80:
                break

    term_rows = []
    with elem_csv.open(encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.DictReader(f)):
            oid = row.get("object_id") or ""
            term_rows.append(
                {
                    "element_id": row["element_id"],
                    "object_id": oid,
                    "object_name": row.get("object_name"),
                    "element_type_cn": row.get("element_type_cn"),
                    "terminal_index": row.get("terminal_index"),
                    "terminal_x": row.get("terminal_x"),
                    "terminal_y": row.get("terminal_y"),
                    "point_id规则": f"PT_{oid}_{row.get('terminal_index')}" if oid else "",
                }
            )
            if i >= 119:
                break

    conn_rows = []
    if conn_csv.exists():
        with conn_csv.open(encoding="utf-8-sig", newline="") as f:
            for i, row in enumerate(csv.DictReader(f)):
                conn_rows.append(
                    {
                        "line_id": row.get("line_id"),
                        "line_type": row.get("line_type"),
                        "from_element_id": row.get("from_element_id"),
                        "from_element_type": row.get("from_element_type"),
                        "from_element_name": row.get("from_element_name"),
                        "from_terminal": row.get("from_terminal"),
                        "to_element_id": row.get("to_element_id"),
                        "to_element_type": row.get("to_element_type"),
                        "to_element_name": row.get("to_element_name"),
                        "to_terminal": row.get("to_terminal"),
                    }
                )
                if i >= 79:
                    break

    return pd.DataFrame(equip_rows), pd.DataFrame(term_rows), pd.DataFrame(conn_rows)


def build_version_sheet(gbk_reports: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"项": "版本", "内容": "图模字段映射表 v1"},
            {"项": "SQL源路径(D盘)", "内容": str(SQL_SRC)},
            {"项": "SQL_GBK输出", "内容": str(SQL_GBK_DIR)},
            {"项": "SVG样例", "内容": str(SVG_SRC)},
            {"项": "LINE215馈线", "内容": "LINE_ID=TMP00000188, LINE_NAME=LINE215"},
            {"项": "主键对齐", "内容": "SVG.object_id == SQL.EQUIP_ID"},
            {"项": "图元ID", "内容": "SVG.element_id 仅图形主键，不直接作库主键"},
            {"项": "端点规则", "内容": "优先PWTERMINAL.ID；否则 PT_{EQUIP_ID}_{terminal_index}"},
            {"项": "连接规则", "内容": "同CONNECTIVITYNODE互通；SVG侧几何最近端子连通"},
            {"项": "GBK文件数", "内容": str(len(gbk_reports))},
            {"项": "解析样例目录", "内容": str(SAMPLE_DIR)},
        ]
    )


def copy_svg_sample() -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    mapping = {
        "LINE215.svg_elements.csv": OUT_CSV / "LINE215.svg_elements.csv",
        "LINE215.svg_connections.csv": OUT_CSV / "LINE215.svg_connections.csv",
        "LINE215.svg_texts.csv": OUT_CSV / "LINE215.svg_texts.csv",
        "LINE215.svg_elements.json": OUT_JSON / "LINE215.svg_elements.json",
        "LINE215.svg_connections.json": OUT_JSON / "LINE215.svg_connections.json",
    }
    for name, src in mapping.items():
        if src.exists():
            dst = SAMPLE_DIR / name
            dst.write_bytes(src.read_bytes())
            print(f"[SAMPLE] {dst}")

    # 迷你摘要 JSON
    summary = {
        "svg_file": "LINE215.svg",
        "sql_feeder": {"LINE_ID": "TMP00000188", "LINE_NAME": "LINE215"},
        "id_mapping_rule": {
            "equip": "SVG.object_id == EQUIP.EQUIP_ID",
            "element": "SVG.element_id 为图元ID",
            "point": "PT_{object_id}_{terminal_index} 或 PWTERMINAL.ID",
        },
        "sample_element": {
            "element_id": "TMP_350d4db8-81f5-428e-8058-388cebbce60d",
            "object_id": "TMP00046409",
            "object_name": "配变2186",
            "element_type": "PowerTransformer",
            "terminals": [
                {"terminal_index": 1, "point_id": "PT_TMP00046409_1"},
                {"terminal_index": 2, "point_id": "PT_TMP00046409_2"},
            ],
        },
        "artifacts": list(mapping.keys()),
    }
    (SAMPLE_DIR / "mapping_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    if not SQL_SRC.exists():
        raise FileNotFoundError(f"SQL源目录不存在: {SQL_SRC}")

    gbk_reports = convert_sql_to_gbk()
    df_gbk = pd.DataFrame(gbk_reports)
    df_sql, df_rel = build_sql_dict_sheets()
    df_svg = build_svg_sheet()
    df_rules = build_id_rules()
    df_types = build_type_map()
    df_equip, df_terms, df_conns = load_line215_samples()
    df_ver = build_version_sheet(gbk_reports)

    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:
        df_ver.to_excel(writer, sheet_name="版本说明", index=False)
        df_sql.to_excel(writer, sheet_name="SQL字段字典", index=False)
        df_rel.to_excel(writer, sheet_name="SQL表关联", index=False)
        df_svg.to_excel(writer, sheet_name="SVG字段字典", index=False)
        df_rules.to_excel(writer, sheet_name="ID映射规则", index=False)
        df_types.to_excel(writer, sheet_name="设备类型对照", index=False)
        df_equip.to_excel(writer, sheet_name="LINE215设备映射样例", index=False)
        df_terms.to_excel(writer, sheet_name="端点映射样例", index=False)
        df_conns.to_excel(writer, sheet_name="连接映射样例", index=False)
        df_gbk.to_excel(writer, sheet_name="SQL_GBK转换清单", index=False)

    copy_svg_sample()
    print(f"[OK] Excel -> {EXCEL_PATH}")
    print(f"[OK] GBK  -> {SQL_GBK_DIR}")
    print(f"[OK] Sample -> {SAMPLE_DIR}")


if __name__ == "__main__":
    main()
