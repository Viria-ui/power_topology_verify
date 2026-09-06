"""
配电网图模拓扑智能识别与校验系统 - 统一入口
=============================================

整合功能：
  1. 拓扑校验：主网/配网拓扑构建、电气逻辑校验（E01-E07）、主配接口校验
  2. 图模比对：SVG与数据库一致性校验、缺陷发现、修复建议、SQL草案生成
  3. SVG编辑与自动出图：交互式SVG编辑、自动生成4类5张SVG图
  4. 质量评分：图模质量评分、置信度计算、美化前后对比报告

Usage:
  python main.py --all              # 运行全部功能
  python main.py --topo            # 仅拓扑校验
  python main.py --compare LINE215  # 仅图模比对
  python main.py --svg             # 仅SVG编辑与自动出图
  python main.py --line LINE215 LINE216  # 指定线路进行图模比对
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from typing import Any, Optional

# ============================================================================
# 项目路径初始化
# ============================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config.settings import (
    TEST_SVG_ROOT, OUTPUT_SVG, OUTPUT_JSON, OUTPUT_SQL,
    DATASET_STANDARD_OUTPUT_XLSX
)
from core.graph_model import TopologyGraph
from core.topology_builder import TopologyBuilder
from core.telemetry_evaluator import TelemetryEvaluator
from core.score_engine import ScoreAndConfidenceEngine
from core.repair_generator import TopologyRepairGenerator
from core.defect_excel_exporter import export_defects_xlsx
from core.feeder_topology_analysis import build_feeder_analysis
from data_io.data_reader import SqlTableLoader
from data_io.data_writer import gen_sample_data
from data_io.svg_reader import SvgParser

# SVG 编辑与出图模块（可选导入，失败不中断）
try:
    from svg_io.svg_beautifier import SvgBeautifier
    from svg_io.svg_editor import SvgInteractiveEditorV2
    from svg_io.svg_auto_generator import SvgAutoGenerator
    from svg_io.quality_checker import check_svg_quality
    SVG_MODULES_OK = True
except ImportError as e:
    SVG_MODULES_OK = False
    print(f"[警告] SVG模块导入失败: {e}")


# ============================================================================
# 辅助函数
# ============================================================================

def _sql_quote(v: Any) -> str:
    """SQL字符串转义"""
    if v is None:
        return "NULL"
    return "'" + str(v).replace("'", "''") + "'"


def discover_available_lines() -> list[str]:
    """扫描output/json目录，自动发现已有SVG解析结果的线路名称"""
    json_dir = os.path.join(PROJECT_ROOT, "output", "json")
    if not os.path.isdir(json_dir):
        return []
    lines = set()
    for path in glob.glob(os.path.join(json_dir, "*.svg_elements.json")):
        base = os.path.basename(path).replace(".svg_elements.json", "")
        if base:
            lines.add(base)
    return sorted(lines)


def load_svg_data(line_name: str) -> tuple[dict, dict, list]:
    """读取指定线路的SVG设备与连接JSON"""
    json_elem_path = os.path.join(PROJECT_ROOT, "output", "json", f"{line_name}.svg_elements.json")
    json_conn_path = os.path.join(PROJECT_ROOT, "output", "json", f"{line_name}.svg_connections.json")

    if not os.path.isfile(json_elem_path):
        raise FileNotFoundError(f"未找到SVG设备JSON: {json_elem_path}")

    with open(json_elem_path, "r", encoding="utf-8") as f:
        svg_elem_data = json.load(f)

    raw_elements = svg_elem_data.get("elements", [])
    svg_device_map = {}
    element_to_object_map = {}

    for elem in raw_elements:
        if isinstance(elem, dict):
            elem_id = elem.get("element_id")
            obj_id = elem.get("object_id") or elem.get("equip_id")
            if obj_id:
                svg_device_map[str(obj_id).strip()] = elem
                if elem_id:
                    element_to_object_map[str(elem_id).strip()] = str(obj_id).strip()

    svg_connections = []
    if os.path.exists(json_conn_path):
        with open(json_conn_path, "r", encoding="utf-8") as f:
            svg_conn_data = json.load(f)
            svg_connections = svg_conn_data.get("connections", svg_conn_data.get("data", []))

    return svg_device_map, element_to_object_map, svg_connections


def resolve_feeder_id(line_name: str, line_df) -> str:
    """将线路名称解析为数据库FEEDER_ID"""
    if line_df is None or len(line_df) == 0:
        return line_name
    kw = line_name.strip()
    kw_low = kw.lower()
    matches = line_df[line_df["LINE_NAME"].astype(str).str.lower() == kw_low]
    if len(matches) > 0:
        return str(matches.iloc[0]["LINE_ID"])
    # 前缀剥离
    for prefix in ("10kvline", "35kvline", "110kvline", "kvline", "line"):
        if kw_low.startswith(prefix):
            suffix = kw_low[len(prefix):]
            if suffix and len(suffix) >= 2:
                mask = line_df["LINE_NAME"].astype(str).str.extract(r"(\d{2,4})", expand=False).fillna("")
                end_chars = suffix[-3:] if len(suffix) >= 3 else suffix[-2:]
                if mask.str.endswith(end_chars).any():
                    return str(line_df[mask.str.endswith(end_chars)].iloc[0]["LINE_ID"])
    return kw


def resolve_start_st_id(feeder_id: str, line_df) -> str:
    """从馈线表获取主配网挂接站房ID"""
    if line_df is None or len(line_df) == 0:
        return ""
    matches = line_df[line_df["LINE_ID"].astype(str) == str(feeder_id)]
    if len(matches) > 0:
        return str(matches.iloc[0].get("START_ST_ID", "") or "")
    return ""


def filter_feeder_devices(dist_topo, feeder_id: str) -> dict:
    """按FEEDER_ID筛选当前馈线的数据库设备"""
    feeder_id_str = str(feeder_id)
    return {
        equip_id: dev
        for equip_id, dev in dist_topo.device_map.items()
        if str(getattr(dev, "feeder_id", "") or "") == feeder_id_str
    }


# ============================================================================
# 功能模块
# ============================================================================

def run_topo_validation(table_datas: dict) -> tuple:
    """功能1：拓扑校验（主网/配网构建 + 电气逻辑校验）"""
    print("\n" + "=" * 70)
    print("【功能1】拓扑校验：主网/配网拓扑构建 + 电气逻辑校验")
    print("=" * 70)

    builder = TopologyBuilder(table_datas)
    main_topo, dist_topo = builder.build_full_topology()
    print("✅ 主网/配网拓扑构建完成，设备内部端点连通关系已补齐")

    # 1.1 电气逻辑校验（E01-E07 + 主配接口）
    print("\n--- 电气逻辑校验（E01-E07）---")
    elec_results = builder.check_electrical_logic()
    print(f"  电气逻辑缺陷数量: {len(elec_results)}")
    elec_by_type: dict = {}
    for r in elec_results:
        code = r.get("rule_code", "未知")
        elec_by_type[code] = elec_by_type.get(code, 0) + 1
    for code, cnt in sorted(elec_by_type.items()):
        print(f"    {code}: {cnt}条")
    
    # 主配接口异常
    interface_defects = [a for a in dist_topo.abnormal_list if '接口' in getattr(a, 'dimension', '')]
    print(f"  主配接口异常数量: {len(interface_defects)}")

    # 1.2 拓扑统计（不输出设备ID完整列表，避免刷屏）
    main_stat = builder.get_topo_statistics(main_topo, "110kV主网拓扑")
    dist_stat = builder.get_topo_statistics(dist_topo, "10kV配网拓扑")
    print("\n--- 主网拓扑统计 ---")
    for k, v in main_stat.items():
        # 跳过设备ID清单，只打印统计指标
        if k in ("设备ID清单", "设备ID列表", "设备ID"):
            print(f"  {k}: {len(v)} 个设备")
        else:
            print(f"  {k}: {v}")
    print("\n--- 配网拓扑统计 ---")
    for k, v in dist_stat.items():
        if k in ("设备ID清单", "设备ID列表", "设备ID"):
            print(f"  {k}: {len(v)} 个设备")
        else:
            print(f"  {k}: {v}")

    # 1.3 拓扑异常检测
    print("\n--- 拓扑异常检测 ---")
    abnormal_list, breakpoint_list = builder.check_topo_abnormal(dist_topo)
    # 联络合环结果已回写到 dist_topo.tie_loop_list
    tie_loop_list = getattr(dist_topo, 'tie_loop_list', []) or []
    print(f"  异常项: {len(abnormal_list)} 条")
    print(f"  断点: {len(breakpoint_list)} 条")
    print(f"  联络合环: {len(tie_loop_list)} 条")

    return builder, main_topo, dist_topo, elec_results


def run_svg_parsing(table_datas: dict) -> dict:
    """功能2：SVG解析（提取图元清单与连接关系）"""
    print("\n" + "=" * 70)
    print("【功能2】SVG解析：提取图元清单与连接关系")
    print("=" * 70)

    svg_dir = TEST_SVG_ROOT
    results = {}
    for fname in ['LINE215.svg', 'LINE216.svg']:
        fpath = os.path.join(svg_dir, fname)
        if os.path.exists(fpath):
            print(f"\n--- 解析 {fname} ---")
            doc = SvgParser.parse(fpath)
            if doc:
                # 输出到output/csv/
                doc.export_elements_json(f'{fname}_elements.json')
                doc.export_elements_csv(f'{fname}_elements.csv')
                doc.export_connections_json(f'{fname}_connections.json')
                doc.export_connections_csv(f'{fname}_connections.csv')
                print(f"  图元清单: output/csv/{fname}_elements.csv")
                print(f"  连接关系: output/csv/{fname}_connections.csv")
                results[fname] = doc
            else:
                print(f"  ⚠️ 解析失败: {fname}")
        else:
            print(f"  ⚠️ 文件不存在: {fname}")
    
    return results


def run_compare_for_line(line_name: str, dist_topo, line_df, table_data: dict) -> dict:
    """功能3：图模比对（SVG与数据库一致性校验）"""
    feeder_id = resolve_feeder_id(line_name, line_df)
    start_st_id = resolve_start_st_id(feeder_id, line_df)

    print(f"\n{'=' * 60}")
    print(f"🔍 图模比对: {line_name} (FEEDER_ID={feeder_id})")
    print(f"{'=' * 60}")

    # 加载SVG数据
    svg_device_map, element_to_object_map, svg_connections = load_svg_data(line_name)
    print(f"✅ SVG设备: {len(svg_device_map)}个, 连接: {len(svg_connections)}条")

    # 筛选馈线设备
    line_db_devices = filter_feeder_devices(dist_topo, feeder_id)
    print(f"✅ 数据库馈线设备: {len(line_db_devices)}个")

    svg_dev_ids = set(svg_device_map.keys())
    db_dev_ids = set(line_db_devices.keys())
    all_db_dev_ids = set(dist_topo.device_map.keys())
    defects_report = []

    # 校验1：图上有，模型无
    for dev_id in svg_dev_ids - all_db_dev_ids:
        elem_info = svg_device_map.get(dev_id, {})
        dev_name = elem_info.get("object_name") or elem_info.get("element_type_cn") or "未知设备"
        defects_report.append({
            "equip_id": dev_id,
            "defect_type": "图上有模型无",
            "description": f"SVG图纸存在设备[{dev_name}](ID:{dev_id})，但数据库拓扑模型中缺失",
            "suggestion": f"建议在数据库设备表中补全设备 {dev_id} 信息",
            "sql_draft": f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME) VALUES ('{dev_id}', '{dev_name}');",
            "equip_name": dev_name,
            "station_id": start_st_id,
        })

    # 校验2：模型有，图上无
    for dev_id in db_dev_ids - svg_dev_ids:
        db_dev = line_db_devices[dev_id]
        dev_name = getattr(db_dev, "equip_name", "未知设备") or "未知设备"
        station = getattr(db_dev, "dsubstation_id", "") or start_st_id
        defects_report.append({
            "equip_id": dev_id,
            "defect_type": "模型有图上无",
            "description": f"数据库拓扑模型存在设备[{dev_name}](ID:{dev_id})，但SVG图纸未绘制该图元",
            "suggestion": f"建议重新补全SVG图纸绘图，增加设备 {dev_id} 图元",
            "sql_draft": "-- 图纸层面补全，无需调整数据库数据",
            "equip_name": dev_name,
            "station_id": station,
        })

    # 校验3：物理连接不一致
    for conn in svg_connections:
        if isinstance(conn, dict):
            from_elem_id = str(conn.get("from_element_id") or "").strip()
            to_elem_id = str(conn.get("to_element_id") or "").strip()
            from_obj_id = element_to_object_map.get(from_elem_id)
            to_obj_id = element_to_object_map.get(to_elem_id)

            if from_obj_id and to_obj_id and (from_obj_id != to_obj_id):
                has_logic_conn = False
                if hasattr(dist_topo, "graph"):
                    import networkx as nx_
                    G = dist_topo.graph
                    pts_from = dist_topo.get_device_all_points(from_obj_id) if hasattr(dist_topo, 'get_device_all_points') else []
                    pts_to = dist_topo.get_device_all_points(to_obj_id) if hasattr(dist_topo, 'get_device_all_points') else []
                    if pts_from and pts_to:
                        for pa in pts_from:
                            if not G.has_node(pa):
                                continue
                            for pb in pts_to:
                                if not G.has_node(pb):
                                    continue
                                try:
                                    if nx_.has_path(G, pa, pb):
                                        has_logic_conn = True
                                        break
                                except (nx_.NetworkXNoPath, nx_.NodeNotFound):
                                    continue
                            if has_logic_conn:
                                break
                if not has_logic_conn:
                    defects_report.append({
                        "equip_id": f"{from_obj_id} <-> {to_obj_id}",
                        "defect_type": "物理连接不一致",
                        "description": f"SVG图纸存在设备 {from_obj_id} 与 {to_obj_id} 的物理连接，但数据库拓扑网中缺失该连线",
                        "suggestion": "建议在数据库线路表中增补对应物理连接记录",
                        "sql_draft": f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (START_EQUIP, END_EQUIP) VALUES ('{from_obj_id}', '{to_obj_id}');",
                        "equip_name": "物理连接",
                        "station_id": start_st_id,
                    })

    # 校验4：逻辑属性不一致
    for dev_id in svg_dev_ids & db_dev_ids:
        svg_elem = svg_device_map[dev_id]
        db_dev = line_db_devices[dev_id]
        svg_voltage = svg_elem.get("voltage_level")
        db_voltage = getattr(db_dev, "voltage_type", None)
        dev_name = svg_elem.get("object_name") or getattr(db_dev, "equip_name", "") or "未知设备"
        station = getattr(db_dev, "dsubstation_id", "") or start_st_id
        if svg_voltage and db_voltage and (str(svg_voltage) not in str(db_voltage)):
            defects_report.append({
                "equip_id": dev_id,
                "defect_type": "逻辑连接不一致",
                "description": f"设备 {dev_id} 属性不一致：SVG电压=[{svg_voltage}]，数据库=[{db_voltage}]",
                "suggestion": f"校对设备逻辑属性，统一将数据库更新为SVG图纸属性 [{svg_voltage}]",
                "sql_draft": f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='{svg_voltage}' WHERE EQUIP_ID='{dev_id}';",
                "equip_name": dev_name,
                "station_id": station,
            })

    # 输出统计
    print(f"\n📊 图模一致性校验完成！累计发现缺陷: {len(defects_report)} 条")
    type_counts = {}
    for d in defects_report:
        t = d["defect_type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    for defect_type, count in sorted(type_counts.items()):
        print(f"  • 【{defect_type}】: {count} 处")

    # 导出缺陷清单
    output_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_json_path = os.path.join(output_dir, f"{line_name}_缺陷清单报告.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(defects_report, f, ensure_ascii=False, indent=4)
    print(f"👉 缺陷清单JSON: {output_json_path}")

    # 生成修复候选与SQL
    print("\n🔧 生成最小修改候选方案与SQL草案...")
    repair_gen = TopologyRepairGenerator(defects_report)
    repair_candidates = repair_gen.generate_repair_candidates()
    topo_delta = TopologyRepairGenerator.calculate_topology_delta(line_db_devices, repair_candidates)

    repair_output_path = os.path.join(output_dir, f"{line_name}_最小修改候选与SQL草案.json")
    sql_script_path = os.path.join(output_dir, f"{line_name}_正向修复与回滚脚本.sql")

    with open(repair_output_path, "w", encoding="utf-8") as f:
        json.dump({"topology_delta": topo_delta, "candidates": repair_candidates}, f, ensure_ascii=False, indent=4)

    with open(sql_script_path, "w", encoding="utf-8") as f:
        f.write("-- ==========================================\n")
        f.write(f"-- {line_name} 自动化拓扑修复SQL脚本\n")
        f.write("-- ==========================================\n\n")
        f.write("-- 1. 正向修复SQL脚本\n")
        for c in repair_candidates:
            f.write(f"{c['sql_forward']} -- {c['impact_summary']}\n")
        f.write("\n\n-- 2. 逆向回滚SQL脚本\n")
        for c in reversed(repair_candidates):
            f.write(f"{c['sql_rollback']}\n")

    print(f"👉 修复候选JSON: {repair_output_path}")
    print(f"👉 SQL脚本: {sql_script_path}")

    # 质量评分
    print("\n📈 质量评分与置信度计算...")
    tele_evaluator = TelemetryEvaluator()
    score_engine = ScoreAndConfidenceEngine(tele_evaluator)
    repaired_defect_ids = list(range(len(defects_report)))
    score_summary = score_engine.evaluate_quality_score(
        defects_report, len(dist_topo.device_map),
        repaired_defect_ids=repaired_defect_ids
    )
    print(f"  • 修正前评分: {score_summary['score_before']} 分")
    print(f"  • 预计修正后评分: {score_summary['score_after']} 分")
    print(f"  • 缺陷总数: {score_summary['defect_count']} 处")

    score_output_path = os.path.join(output_dir, f"{line_name}_质量评分与可解释置信度报告.json")
    with open(score_output_path, "w", encoding="utf-8") as f:
        json.dump({
            "line_name": line_name,
            "feeder_id": feeder_id,
            "start_st_id": start_st_id,
            "score_summary": {
                "score_before": score_summary["score_before"],
                "score_after": score_summary["score_after"],
                "total_deduction": score_summary["total_deduction"],
                "defect_count": score_summary["defect_count"],
            },
            "defects_with_confidence": score_summary["processed_defects"],
        }, f, ensure_ascii=False, indent=4)
    print(f"👉 质量评分报告: {score_output_path}")

    # 馈线分析
    analysis = build_feeder_analysis(
        line_name=line_name, feeder_id=feeder_id, start_st_id=start_st_id,
        dist_topo=dist_topo, table_data=table_data,
        svg_connections=svg_connections,
        element_to_object_map=element_to_object_map,
        line_db_devices=line_db_devices,
        defects_report=defects_report,
        score_summary=score_summary,
    )

    # Excel报告
    xlsx_output_path = os.path.join(output_dir, f"{line_name}_拓扑校验缺陷报告.xlsx")
    export_defects_xlsx(
        defects_report, xlsx_output_path, line_name,
        template_path=DATASET_STANDARD_OUTPUT_XLSX,
        default_station=start_st_id,
        analysis=analysis,
    )
    print(f"👉 标准Excel报告: {xlsx_output_path}")

    return {
        "line_name": line_name,
        "feeder_id": feeder_id,
        "defect_count": len(defects_report),
        "type_counts": type_counts,
        "score_before": score_summary["score_before"],
        "score_after": score_summary["score_after"],
    }


def run_svg_edit_and_generate() -> dict:
    """功能4：SVG编辑与自动出图"""
    if not SVG_MODULES_OK:
        print("\n⚠️ SVG模块不可用，跳过SVG编辑与出图功能")
        return {}

    print("\n" + "=" * 70)
    print("【功能4】SVG编辑与自动出图")
    print("=" * 70)

    os.makedirs(OUTPUT_SVG, exist_ok=True)
    os.makedirs(OUTPUT_SQL, exist_ok=True)
    os.makedirs(OUTPUT_JSON, exist_ok=True)

    results = {}

    # ----- Task A: 交互式编辑 -----
    print("\n--- Task A: 交互式SVG编辑 ---")

    # A1. LINE215 插入站房000300
    line215_src = os.path.join(TEST_SVG_ROOT, "LINE215.svg")
    line215_out = os.path.join(OUTPUT_SVG, "LINE215_add_station_000300.svg")

    b1 = SvgBeautifier(line215_src, output_path=line215_out)
    b1._prepare_internal_data()
    b1.repair()
    b1.layout()

    def _count_internal(b):
        real_devs = [p for p, d in b.devices.items() if b.is_real_device(d['type'])]
        conns = sum(len(v) for v in b.adj.values()) // 2
        return {"devices": len(real_devs), "stations": len(b.containers), "connections": conns}

    pre_stat = _count_internal(b1)
    editor = SvgInteractiveEditorV2(b1)
    editor.add_station(
        station_id="000300",
        station_name="站房000300",
        upstream_query="TMP00044018",
        downstream_query="TMP00044016",
        internal_switch_ids=["00301", "00302", "00303"],
    )
    editor.save(line215_out)
    post_stat = _count_internal(b1)

    ok_a1, rep_a1 = check_svg_quality(
        line215_out, os.path.join(OUTPUT_JSON, "LINE215_with_000300_质量报告.json"))

    add_sql = f"""-- Phase 2 Test Task 1：新增站房000300 + 3台负荷开关
BEGIN TRANSACTION;
INSERT INTO EQUIP_JBS_PWROOM (ROOM_ID, ROOM_NAME, ROOM_TYPE, VOLTAGE_TYPE)
VALUES ({_sql_quote('TMPROOM000300')}, {_sql_quote('站房000300')}, '开闭所', 'lkv10');
INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME, EQUIP_TYPE, FEEDER_ID) VALUES
  ({_sql_quote('TMP00301')}, {_sql_quote('开关00301')}, '负荷开关', {_sql_quote('LINE215')}),
  ({_sql_quote('TMP00302')}, {_sql_quote('开关00302')}, '负荷开关', {_sql_quote('LINE215')}),
  ({_sql_quote('TMP00303')}, {_sql_quote('开关00303')}, '负荷开关', {_sql_quote('LINE215')});
COMMIT;
"""
    with open(os.path.join(OUTPUT_SQL, "edit_add_station_000300.sql"), "w", encoding="utf-8") as f:
        f.write(add_sql)
    print(f"  A1 LINE215插入站房000300: {'✅ PASS' if ok_a1 else '❌ FAIL'} | Δ={ {k: post_stat[k]-pre_stat[k] for k in pre_stat} }")

    # A2. LINE216 删除开关00024
    line216_src = os.path.join(TEST_SVG_ROOT, "LINE216.svg")
    line216_out = os.path.join(OUTPUT_SVG, "LINE216_del_switch_00024.svg")

    b2 = SvgBeautifier(line216_src, output_path=line216_out)
    b2._prepare_internal_data()
    b2.repair()
    b2.layout()

    pre_stat2 = _count_internal(b2)
    editor2 = SvgInteractiveEditorV2(b2)
    editor2.delete_device("TMP00043912")
    editor2.save(line216_out)
    post_stat2 = _count_internal(b2)

    ok_a2, rep_a2 = check_svg_quality(
        line216_out, os.path.join(OUTPUT_JSON, "LINE216_del_00024_质量报告.json"))
    print(f"  A2 LINE216删除开关00024: {'✅ PASS' if ok_a2 else '❌ FAIL'} | Δ={ {k: post_stat2[k]-pre_stat2[k] for k in pre_stat2} }")

    results["TaskA"] = {
        "LINE215_add_station": {"quality_pass": ok_a1, "delta": {k: post_stat[k]-pre_stat[k] for k in pre_stat}},
        "LINE216_del_switch": {"quality_pass": ok_a2, "delta": {k: post_stat2[k]-pre_stat2[k] for k in pre_stat2}},
    }

    # ----- Task B: 自动出图 -----
    print("\n--- Task B: 自动SVG生成 ---")
    g = SvgAutoGenerator()

    # B1-B2. 单线图
    for feeder in ["LINE215", "LINE216"]:
        p = g.generate_feeder_single_line_diagram(
            feeder_name=feeder,
            out_path=os.path.join(OUTPUT_SVG, f"{feeder}_single_line.svg"))
        print(f"  B {feeder}单线图: nodes={p.get('nodes')} edges={p.get('edges')} SVG={p.get('svg')}")
        results[f"B_{feeder}_单线图"] = p

    # B3. 联络关系图
    p = g.generate_feeder_tie_diagram(
        feeder_name="10kVLINE111",
        out_path=os.path.join(OUTPUT_SVG, "10kVLINE111_tie.svg"))
    print(f"  B 10kVLINE111联络图: nodes={p.get('nodes')} edges={p.get('edges')} SVG={p.get('svg')}")
    results["B_10kVLINE111_联络图"] = p

    # B4. 全站联络总图
    p = g.generate_station_tie_diagram(
        substation_id="SUB004",
        out_path=os.path.join(OUTPUT_SVG, "SUB004_station_tie.svg"))
    print(f"  B SUB004全站联络图: nodes={p.get('nodes')} edges={p.get('edges')} SVG={p.get('svg')}")
    results["B_SUB004_全站联络图"] = p

    # B5. 电源追溯图
    p = g.generate_power_trace_diagram(
        target_equip_id="TMP00034205",
        feeder_name="LINE074",
        out_path=os.path.join(OUTPUT_SVG, "TMP00034205_power_trace.svg"))
    print(f"  B LINE074电源追溯: nodes={p.get('nodes')} edges={p.get('edges')} SVG={p.get('svg')}")
    results["B_LINE074_电源追溯"] = p

    with open(os.path.join(OUTPUT_JSON, "auto_generate_summary.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results


# ============================================================================
# 主入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="配电网图模拓扑智能识别与校验系统 - 统一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --all                    # 运行全部功能
  python main.py --topo                  # 仅拓扑校验
  python main.py --svg                   # 仅SVG编辑与自动出图
  python main.py --compare LINE215        # 图模比对（指定线路）
  python main.py --compare LINE215 LINE216  # 图模比对（多线路）
  python main.py --all --no-svg           # 全部功能但跳过SVG编辑
        """
    )
    parser.add_argument("--all", action="store_true", help="运行全部功能")
    parser.add_argument("--topo", action="store_true", help="仅运行拓扑校验")
    parser.add_argument("--compare", nargs="+", metavar="LINE", help="图模比对（可指定线路名）")
    parser.add_argument("--svg", action="store_true", help="仅SVG编辑与自动出图")
    parser.add_argument("--no-svg", action="store_true", help="跳过SVG相关功能")
    parser.add_argument("--parse-svg", action="store_true", help="仅SVG解析")
    args = parser.parse_args()

    # 默认行为：运行全部功能
    run_all = args.all or (not args.topo and not args.compare and not args.svg and not args.parse_svg)

    print("=" * 70)
    print("配电网图模拓扑智能识别与校验系统")
    print("=" * 70)

    # 加载数据
    print("\n📂 加载SQL数据...")
    sql_loader = SqlTableLoader()
    table_datas = sql_loader.load_all_topo_tables()
    print(f"  设备表: {len(table_datas.get('equip', []))} 条")
    print(f"  线路表: {len(table_datas.get('line', []))} 条")
    print(f"  主网站点: {len(table_datas.get('zw_substation', []))} 条")
    print(f"  遥信遥测: {len(table_datas.get('yx_real', []))} 条")

    results = {}

    # 功能1: 拓扑校验
    if run_all or args.topo:
        builder, main_topo, dist_topo, elec_results = run_topo_validation(table_datas)
        results["topo"] = {
            "elec_defects": len(elec_results),
            "main_devices": len(main_topo.device_map),
            "dist_devices": len(dist_topo.device_map),
        }

    # 功能2: SVG解析
    if run_all or args.parse_svg:
        svg_results = run_svg_parsing(table_datas)
        results["svg_parse"] = list(svg_results.keys())

    # 功能3: 图模比对
    if run_all or args.compare is not None:
        if args.compare:
            line_names = args.compare
        else:
            line_names = discover_available_lines()
            if not line_names:
                print("\n⚠️ 未发现SVG解析结果，请先运行 --parse-svg")
                line_names = []

        if line_names:
            print(f"\n📋 待比对线路 ({len(line_names)}条): {', '.join(line_names)}")
            compare_results = []
            for line_name in line_names:
                try:
                    r = run_compare_for_line(line_name, dist_topo, table_datas["line"], table_datas)
                    compare_results.append(r)
                except FileNotFoundError as e:
                    print(f"⚠️ 跳过 {line_name}: {e}")
                except Exception as e:
                    print(f"❌ 处理 {line_name} 出错: {e}")

            results["compare"] = compare_results

            # 汇总
            if len(compare_results) > 1:
                print(f"\n{'=' * 60}")
                print("📋 批量校验汇总")
                for r in compare_results:
                    print(f"  • {r['line_name']}: 缺陷{r['defect_count']}处, 评分{r['score_before']}→{r['score_after']}")

    # 功能4: SVG编辑与自动出图
    if (run_all or args.svg) and not args.no_svg:
        svg_results = run_svg_edit_and_generate()
        results["svg"] = svg_results

    # 生成标准样例
    if run_all:
        print("\n📄 生成标准JSON/CSV样例...")
        gen_sample_data()

    print("\n" + "=" * 70)
    print("✅ 全部任务完成!")
    print("=" * 70)
    print(f"输出目录: {os.path.join(PROJECT_ROOT, 'output')}")

    return results


if __name__ == "__main__":
    main()
