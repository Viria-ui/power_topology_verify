import sys
import os
import json
import argparse
import glob

# 1. 确保项目根目录在 sys.path 中
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder
from core.repair_generator import TopologyRepairGenerator
from core.telemetry_evaluator import TelemetryEvaluator
from core.score_engine import ScoreAndConfidenceEngine
from core.defect_excel_exporter import export_defects_xlsx
from core.feeder_topology_analysis import build_feeder_analysis
from config.settings import DATASET_STANDARD_OUTPUT_XLSX


def resolve_feeder_id(line_name: str, line_df) -> str:
    """将 LINE215 / 10kVLINE215 / LINE074 等名称解析为数据库 FEEDER_ID (LINE_ID)。"""
    if line_df is None or len(line_df) == 0:
        return line_name
    kw = line_name.strip()
    kw_low = kw.lower()
    matches = line_df[line_df["LINE_NAME"].astype(str).str.lower() == kw_low]
    if len(matches) > 0:
        return str(matches.iloc[0]["LINE_ID"])
    digit_suffix = kw_low
    for prefix in ("10kvline", "35kvline", "110kvline", "kvline", "line"):
        if digit_suffix.startswith(prefix):
            digit_suffix = digit_suffix[len(prefix):]
    if digit_suffix and len(digit_suffix) >= 2:
        mask = (
            line_df["LINE_NAME"]
            .astype(str)
            .str.extract(r"(\d{2,4})", expand=False)
            .fillna("")
            .str.endswith(digit_suffix[-3:] if len(digit_suffix) >= 3 else digit_suffix[-2:])
        )
        if mask.any():
            return str(line_df[mask].iloc[0]["LINE_ID"])
    return kw


def resolve_start_st_id(feeder_id: str, line_df) -> str:
    """从馈线表获取主配网挂接站房 ID (START_ST_ID)。"""
    if line_df is None or len(line_df) == 0:
        return ""
    matches = line_df[line_df["LINE_ID"].astype(str) == str(feeder_id)]
    if len(matches) > 0:
        return str(matches.iloc[0].get("START_ST_ID", "") or "")
    return ""


def discover_available_lines(json_dir: str | None = None) -> list[str]:
    """扫描 output/json 目录，自动发现已有 SVG 解析结果的线路名称。"""
    json_dir = json_dir or os.path.join(PROJECT_ROOT, "output", "json")
    if not os.path.isdir(json_dir):
        return []
    lines = set()
    for path in glob.glob(os.path.join(json_dir, "*.svg_elements.json")):
        base = os.path.basename(path).replace(".svg_elements.json", "")
        if base:
            lines.add(base)
    return sorted(lines)


def load_svg_data(line_name: str) -> tuple[dict, dict, list]:
    """读取指定线路的 SVG 设备与连接 JSON，返回 (svg_device_map, element_to_object_map, svg_connections)。"""
    json_elem_path = os.path.join(PROJECT_ROOT, "output", "json", f"{line_name}.svg_elements.json")
    json_conn_path = os.path.join(PROJECT_ROOT, "output", "json", f"{line_name}.svg_connections.json")

    if not os.path.isfile(json_elem_path):
        raise FileNotFoundError(f"未找到 SVG 设备 JSON: {json_elem_path}")

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
                obj_id_str = str(obj_id).strip()
                svg_device_map[obj_id_str] = elem
                if elem_id:
                    element_to_object_map[str(elem_id).strip()] = obj_id_str

    svg_connections = []
    if os.path.exists(json_conn_path):
        with open(json_conn_path, "r", encoding="utf-8") as f:
            svg_conn_data = json.load(f)
            svg_connections = svg_conn_data.get("connections", svg_conn_data.get("data", []))

    return svg_device_map, element_to_object_map, svg_connections


def filter_feeder_devices(dist_topo, feeder_id: str) -> dict:
    """按 FEEDER_ID 筛选当前馈线的数据库设备。"""
    feeder_id_str = str(feeder_id)
    return {
        equip_id: dev
        for equip_id, dev in dist_topo.device_map.items()
        if str(getattr(dev, "feeder_id", "") or "") == feeder_id_str
    }


def _make_defect(
    equip_id: str,
    defect_type: str,
    description: str,
    suggestion: str,
    sql_draft: str,
    *,
    equip_name: str = "",
    station_id: str = "",
) -> dict:
    return {
        "equip_id": equip_id,
        "defect_type": defect_type,
        "description": description,
        "suggestion": suggestion,
        "sql_draft": sql_draft,
        "equip_name": equip_name,
        "station_id": station_id,
    }


def run_compare_for_line(line_name: str, dist_topo, line_df, table_data: dict) -> dict:
    """对单条线路执行图模一致性校验、修复候选生成与质量评分，并导出报告。"""
    feeder_id = resolve_feeder_id(line_name, line_df)
    start_st_id = resolve_start_st_id(feeder_id, line_df)

    print(f"\n{'=' * 60}")
    print(f"🔍 开始校验线路: {line_name}  (FEEDER_ID={feeder_id})")
    print(f"{'=' * 60}")

    svg_device_map, element_to_object_map, svg_connections = load_svg_data(line_name)
    print(f"✅ 从 SVG 读取设备：{len(svg_device_map)} 个，物理连接：{len(svg_connections)} 条")

    line_db_devices = filter_feeder_devices(dist_topo, feeder_id)
    print(f"✅ 数据库馈线设备：{len(line_db_devices)} 个")

    svg_dev_ids = set(svg_device_map.keys())
    db_dev_ids = set(line_db_devices.keys())
    all_db_dev_ids = set(dist_topo.device_map.keys())
    defects_report = []

    # 校验 1：图上有，模型无（对照全库设备）
    for dev_id in svg_dev_ids - all_db_dev_ids:
        elem_info = svg_device_map.get(dev_id, {})
        dev_name = elem_info.get("object_name") or elem_info.get("element_type_cn") or "未知设备"
        defects_report.append(_make_defect(
            equip_id=dev_id,
            defect_type="图上有模型无",
            description=f"SVG图纸存在设备[{dev_name}](ID:{dev_id})，但数据库拓扑模型中缺失",
            suggestion=f"建议在数据库设备表中补全设备 {dev_id} 信息",
            sql_draft=f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME) VALUES ('{dev_id}', '{dev_name}');",
            equip_name=dev_name,
            station_id=start_st_id,
        ))

    # 校验 2：模型有，图上无（仅当前馈线）
    for dev_id in db_dev_ids - svg_dev_ids:
        db_dev = line_db_devices[dev_id]
        dev_name = getattr(db_dev, "equip_name", "未知设备") or "未知设备"
        station = getattr(db_dev, "dsubstation_id", "") or start_st_id
        defects_report.append(_make_defect(
            equip_id=dev_id,
            defect_type="模型有图上无",
            description=f"数据库拓扑模型存在设备[{dev_name}](ID:{dev_id})，但SVG图纸未绘制该图元",
            suggestion=f"建议重新补全SVG图纸绘图，增加设备 {dev_id} 图元",
            sql_draft="-- 图纸层面补全，无需调整数据库数据",
            equip_name=dev_name,
            station_id=station,
        ))

    # 校验 3：物理连接不一致
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
                    # 拓扑图是 设备-端子/端子-端子 混合图，不能直接 has_edge(device, device)。
                    # 正确方式：取两端设备各自的端子，检查是否存在连通路径。
                    pts_from = dist_topo.get_device_all_points(from_obj_id)
                    pts_to = dist_topo.get_device_all_points(to_obj_id)
                    if pts_from and pts_to:
                        for pa in pts_from:
                            if not G.has_node(pa):
                                continue
                            for pb in pts_to:
                                if not G.has_node(pb):
                                    continue
                                try:
                                    if nx_.has_path(G, pa, pb):
                                        plen = len(nx_.shortest_path(G, pa, pb))
                                        if plen <= 10:
                                            has_logic_conn = True
                                            break
                                except (nx_.NetworkXNoPath, nx_.NodeNotFound):
                                    continue
                            if has_logic_conn:
                                break
                    # 退化：无端子时直接检查节点是否存在路径
                    if not has_logic_conn and G.has_node(from_obj_id) and G.has_node(to_obj_id):
                        try:
                            has_logic_conn = nx_.has_path(G, from_obj_id, to_obj_id)
                        except (nx_.NetworkXNoPath, nx_.NodeNotFound):
                            pass
                if not has_logic_conn:
                    defects_report.append(_make_defect(
                        equip_id=f"{from_obj_id} <-> {to_obj_id}",
                        defect_type="物理连接不一致",
                        description=(
                            f"SVG图纸存在设备 {from_obj_id} 与 {to_obj_id} 的物理连接，"
                            f"但数据库拓扑网中缺失该连线(端子图不连通)"
                        ),
                        suggestion="建议在数据库线路表 EQUIP_JBS_PWFEEDERLINE 中增补对应物理连接记录",
                        sql_draft=(
                            f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (START_EQUIP, END_EQUIP) "
                            f"VALUES ('{from_obj_id}', '{to_obj_id}');"
                        ),
                        equip_name="物理连接",
                        station_id=start_st_id,
                    ))

    # 校验 4：逻辑连接/属性不一致
    for dev_id in svg_dev_ids & db_dev_ids:
        svg_elem = svg_device_map[dev_id]
        db_dev = line_db_devices[dev_id]
        svg_voltage = svg_elem.get("voltage_level")
        db_voltage = getattr(db_dev, "voltage_type", None)
        dev_name = (
            svg_elem.get("object_name")
            or svg_elem.get("element_type_cn")
            or getattr(db_dev, "equip_name", "")
            or "未知设备"
        )
        station = getattr(db_dev, "dsubstation_id", "") or start_st_id
        if svg_voltage and db_voltage and (str(svg_voltage) not in str(db_voltage)):
            defects_report.append(_make_defect(
                equip_id=dev_id,
                defect_type="逻辑连接不一致",
                description=(
                    f"设备 {dev_id} 属性不一致：SVG电压等级为[{svg_voltage}]，"
                    f"而数据库模型属性为[{db_voltage}]"
                ),
                suggestion=f"校对设备逻辑属性，统一将数据库更新为 SVG 图纸属性 [{svg_voltage}]",
                sql_draft=(
                    f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='{svg_voltage}' "
                    f"WHERE EQUIP_ID='{dev_id}';"
                ),
                equip_name=dev_name,
                station_id=station,
            ))

    # 输出统计与导出缺陷清单
    print(f"📊 图模一致性校验完成！累计发现缺陷总数：{len(defects_report)} 条")
    type_counts = {}
    for d in defects_report:
        t = d["defect_type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    for defect_type, count in type_counts.items():
        print(f"  • 【{defect_type}】: {count} 处")

    output_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_json_path = os.path.join(output_dir, f"{line_name}_缺陷清单报告.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(defects_report, f, ensure_ascii=False, indent=4)
    print(f"👉 缺陷清单 JSON: {output_json_path}")

    # 生成修补候选与 SQL
    print("\n🔧 开始生成最小修改候选方案与可回滚 SQL...")
    repair_gen = TopologyRepairGenerator(defects_report)
    repair_candidates = repair_gen.generate_repair_candidates()
    topo_delta = TopologyRepairGenerator.calculate_topology_delta(line_db_devices, repair_candidates)

    repair_output_path = os.path.join(output_dir, f"{line_name}_最小修改候选与SQL草案.json")
    sql_script_path = os.path.join(output_dir, f"{line_name}_正向修复与回滚脚本.sql")

    with open(repair_output_path, "w", encoding="utf-8") as f:
        json.dump({"topology_delta": topo_delta, "candidates": repair_candidates}, f, ensure_ascii=False, indent=4)

    with open(sql_script_path, "w", encoding="utf-8") as f:
        f.write("-- ==========================================\n")
        f.write(f"-- {line_name} 自动化拓扑修复 SQL 脚本\n")
        f.write("-- ==========================================\n\n")
        f.write("-- 1. 正向修复 SQL 脚本 (Forward Repair)\n")
        for c in repair_candidates:
            f.write(f"{c['sql_forward']} -- {c['impact_summary']}\n")
        f.write("\n\n-- ==========================================\n")
        f.write("-- 2. 逆向回滚 SQL 脚本 (Rollback)\n")
        f.write("-- ==========================================\n")
        for c in reversed(repair_candidates):
            f.write(f"{c['sql_rollback']}\n")

    print(f"👉 修复候选 JSON: {repair_output_path}")
    print(f"👉 SQL 脚本: {sql_script_path}")

    # 遥测评估与质量评分
    print("\n📈 开始进行遥信遥测校验、主配接口复核与质量评分...")
    tele_evaluator = TelemetryEvaluator()
    score_engine = ScoreAndConfidenceEngine(tele_evaluator)

    main_interface_ok, interface_conf, interface_msg = tele_evaluator.verify_main_substation_interface(
        feeder_id, start_st_id
    )
    print(f"🔌 主配网接口校验结果: [{interface_msg}] (置信度: {interface_conf})")

    # 计算已修复的缺陷ID（所有 repair_candidates 对应的缺陷索引）
    # 注意：processed_defects 中的 _idx 是整数索引 (0, 1, 2, ...)
    repaired_defect_ids = list(range(len(defects_report)))

    # 评估修复前后的评分
    score_summary = score_engine.evaluate_quality_score(
        defects_report, len(dist_topo.device_map),
        repaired_defect_ids=repaired_defect_ids
    )
    print(f"  • 修正前图模质量评分: {score_summary['score_before']} 分")
    print(f"  • 预计修正后质量评分: {score_summary['score_after']} 分")
    print(f"  • 缺陷总数: {score_summary['defect_count']} 处")
    print(f"  • 将修复缺陷数: {len(repaired_defect_ids)} 处")

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
            "main_interface": {
                "ok": main_interface_ok,
                "confidence": interface_conf,
                "message": interface_msg,
            },
            "defects_with_confidence": score_summary["processed_defects"],
        }, f, ensure_ascii=False, indent=4)

    print(f"👉 质量评分报告: {score_output_path}")

    analysis = build_feeder_analysis(
        line_name=line_name,
        feeder_id=feeder_id,
        start_st_id=start_st_id,
        dist_topo=dist_topo,
        table_data=table_data,
        svg_connections=svg_connections,
        element_to_object_map=element_to_object_map,
        line_db_devices=line_db_devices,
        defects_report=defects_report,
        score_summary=score_summary,
    )

    xlsx_output_path = os.path.join(output_dir, f"{line_name}_拓扑校验缺陷报告.xlsx")
    export_defects_xlsx(
        defects_report,
        xlsx_output_path,
        line_name,
        template_path=DATASET_STANDARD_OUTPUT_XLSX,
        default_station=start_st_id,
        analysis=analysis,
    )
    print(f"👉 标准 Excel 报告(5表): {xlsx_output_path}")
    print(
        f"   └─ 断点 {len(analysis['breakpoints'])} 条 / "
        f"联络 {len(analysis['tie_switches'])} 条 / "
        f"合环 {len(analysis['loops'])} 条 / "
        f"评分 {len(analysis['scores'])} 条"
    )

    return {
        "line_name": line_name,
        "feeder_id": feeder_id,
        "defect_count": len(defects_report),
        "type_counts": type_counts,
        "score_before": score_summary["score_before"],
        "score_after": score_summary["score_after"],
    }


def parse_args():
    parser = argparse.ArgumentParser(description="图模一致性校验：支持单条或多条馈线批量比对")
    parser.add_argument(
        "--line", "-l",
        nargs="+",
        help="指定线路名称，如 LINE215 LINE216；不指定则自动处理 output/json 下所有可用线路",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="处理 output/json 目录下所有已解析的线路（与默认行为相同）",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.line:
        line_names = args.line
    else:
        line_names = discover_available_lines()
        if not line_names:
            print("❌ 未在 output/json 中发现任何 *.svg_elements.json 文件。")
            print("   请先运行 SVG 解析流程，或使用 --line LINE215 指定线路。")
            sys.exit(1)

    print("正在从 SQL 读取数据并构建拓扑模型...")
    loader = SqlTableLoader()
    table_data = loader.load_all_topo_tables()
    builder = TopologyBuilder(table_data)
    _, dist_topo = builder.build_full_topology()
    print(f"✅ 全库配网设备构建完成，总数：{len(dist_topo.device_map)} 个")
    print(f"📋 待校验线路 ({len(line_names)} 条): {', '.join(line_names)}")

    results = []
    failed = []
    for line_name in line_names:
        try:
            result = run_compare_for_line(line_name, dist_topo, table_data["line"], table_data)
            results.append(result)
        except FileNotFoundError as e:
            print(f"⚠️  跳过 {line_name}: {e}")
            failed.append(line_name)
        except Exception as e:
            print(f"❌ 处理 {line_name} 时出错: {e}")
            failed.append(line_name)

    if len(line_names) > 1:
        print(f"\n{'=' * 60}")
        print("📋 批量校验汇总")
        print(f"{'=' * 60}")
        for r in results:
            print(
                f"  • {r['line_name']}: 缺陷 {r['defect_count']} 处, "
                f"评分 {r['score_before']} → {r['score_after']}"
            )
        if failed:
            print(f"  ⚠️  失败/跳过: {', '.join(failed)}")

    if not results and failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
