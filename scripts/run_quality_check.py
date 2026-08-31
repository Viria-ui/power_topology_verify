"""图模一致性校验（任务一模块二）

对指定馈线执行四类校验并导出缺陷清单报告：
1. 图上有模型无
2. 模型有图无
3. 物理连接不一致
4. 逻辑连接不一致（电压等级）

用法: python scripts/run_quality_check.py [LINE215] [LINE216]
"""
import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.defect_excel_exporter import export_defects_xlsx
from config.settings import DATASET_STANDARD_OUTPUT_XLSX, TEST_SVG_ROOT
from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder
from data_io.svg_reader import SvgParser

FEEDER_MAP = {
    "LINE215": "TMP00000188",
    "LINE216": "TMP00000189",
}
SVG_DIR = TEST_SVG_ROOT
JSON_DIR = os.path.join(PROJECT_ROOT, "output", "json")
REPORT_DIR = os.path.join(PROJECT_ROOT, "output", "reports")


def ensure_json(line_name: str):
    """确保SVG解析JSON存在，不存在则导出。"""
    elem_path = os.path.join(JSON_DIR, f"{line_name}.svg_elements.json")
    conn_path = os.path.join(JSON_DIR, f"{line_name}.svg_connections.json")
    if not os.path.exists(elem_path) or not os.path.exists(conn_path):
        svg_path = os.path.join(SVG_DIR, f"{line_name}.svg")
        doc = SvgParser.parse(svg_path)
        os.makedirs(JSON_DIR, exist_ok=True)
        doc.export_elements_json(os.path.join(JSON_DIR, f"{line_name}.svg_elements.json"))
        doc.export_connections_json(os.path.join(JSON_DIR, f"{line_name}.svg_connections.json"))
    return elem_path, conn_path


def load_svg_data(line_name: str):
    elem_path, conn_path = ensure_json(line_name)
    with open(elem_path, "r", encoding="utf-8") as f:
        elem_data = json.load(f)
    with open(conn_path, "r", encoding="utf-8") as f:
        conn_data = json.load(f)

    svg_device_map = {}
    for elem in elem_data.get("elements", []):
        obj_id = elem.get("object_id") or elem.get("element_id")
        if obj_id and obj_id.startswith("TMP"):
            svg_device_map[obj_id] = elem

    svg_connections = conn_data.get("connections", [])
    return svg_device_map, svg_connections


def run_check(line_name: str, dist_topo):
    feeder_id = FEEDER_MAP[line_name]
    print(f"\n{'='*60}")
    print(f"校验 {line_name} (feeder_id={feeder_id})")
    print(f"{'='*60}")

    svg_device_map, svg_connections = load_svg_data(line_name)
    print(f"  SVG设备: {len(svg_device_map)} 个, 物理连接: {len(svg_connections)} 条")

    db_devices = {
        did: dev for did, dev in dist_topo.device_map.items()
        if getattr(dev, "feeder_id", None) == feeder_id
    }
    print(f"  数据库设备: {len(db_devices)} 个")

    svg_ids = set(svg_device_map.keys())
    db_ids = set(db_devices.keys())
    defects = []

    # 1. 图上有模型无
    for dev_id in svg_ids - db_ids:
        elem = svg_device_map[dev_id]
        dev_name = elem.get("object_name") or elem.get("element_type_cn") or "未知设备"
        defects.append({
            "equip_id": dev_id,
            "defect_type": "图上有模型无",
            "description": f"SVG图纸存在设备[{dev_name}](ID:{dev_id})，但数据库拓扑模型中缺失",
            "suggestion": f"建议在数据库设备表中补全设备 {dev_id} 信息",
            "sql_draft": f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME) VALUES ('{dev_id}', '{dev_name}');",
        })

    # 2. 模型有图无
    for dev_id in db_ids - svg_ids:
        dev = db_devices[dev_id]
        dev_name = getattr(dev, "equip_name", "未知设备")
        defects.append({
            "equip_id": dev_id,
            "defect_type": "模型有图无",
            "description": f"数据库拓扑模型存在设备[{dev_name}](ID:{dev_id})，但SVG图纸未绘制该图元",
            "suggestion": f"建议重新补全SVG图纸绘图，增加设备 {dev_id} 图元",
            "sql_draft": "-- 图纸层面补全，无需调整数据库数据",
        })

    # 3. 物理连接不一致
    for conn in svg_connections:
        from_id = conn.get("from_element_id")
        to_id = conn.get("to_element_id")
        if from_id and to_id and from_id != to_id:
            has_edge = dist_topo.graph.has_edge(from_id, to_id) or dist_topo.graph.has_edge(to_id, from_id)
            if not has_edge:
                defects.append({
                    "equip_id": f"{from_id} <-> {to_id}",
                    "defect_type": "物理连接不一致",
                    "description": f"SVG图纸存在设备 {from_id} 与 {to_id} 的物理连接，但数据库拓扑中缺失该连线",
                    "suggestion": "建议在数据库线路表 EQUIP_JBS_PWFEEDERLINE 中增补对应物理连接记录",
                    "sql_draft": f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (START_EQUIP, END_EQUIP, FEEDER_ID) VALUES ('{from_id}', '{to_id}', '{feeder_id}');",
                })

    # 4. 逻辑连接/属性不一致（电压等级）
    for dev_id in svg_ids & db_ids:
        svg_elem = svg_device_map[dev_id]
        db_dev = db_devices[dev_id]
        svg_vol = svg_elem.get("voltage_level")
        db_vol = getattr(db_dev, "voltage_type", None)
        if svg_vol and db_vol and str(svg_vol) != str(db_vol):
            defects.append({
                "equip_id": dev_id,
                "defect_type": "逻辑连接不一致",
                "description": f"设备 {dev_id} 电压等级不一致：SVG为[{svg_vol}]，数据库为[{db_vol}]",
                "suggestion": "校对设备逻辑属性，建议以 SVG 图纸为准更新数据库",
                "sql_draft": f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='{svg_vol}' WHERE EQUIP_ID='{dev_id}';",
            })

    # 统计
    type_counts = {}
    for d in defects:
        t = d["defect_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"\n  缺陷总数: {len(defects)} 条")
    for t, c in type_counts.items():
        print(f"    {t}: {c}")

    # 导出
    os.makedirs(REPORT_DIR, exist_ok=True)
    out_path = os.path.join(REPORT_DIR, f"{line_name}_缺陷清单报告.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(defects, f, ensure_ascii=False, indent=2)
    print(f"  报告已导出: {out_path}")

    xlsx_path = os.path.join(REPORT_DIR, f"{line_name}_拓扑校验缺陷报告.xlsx")
    export_defects_xlsx(
        defects,
        xlsx_path,
        line_name,
        template_path=DATASET_STANDARD_OUTPUT_XLSX,
        default_station="",
    )
    print(f"  Excel 报告已导出: {xlsx_path}")
    return defects


if __name__ == "__main__":
    lines = sys.argv[1:] if len(sys.argv) > 1 else ["LINE215", "LINE216"]

    print("加载数据库并构建拓扑...")
    loader = SqlTableLoader()
    table_data = loader.load_all_topo_tables()
    builder = TopologyBuilder(table_data)
    main_topo, dist_topo = builder.build_full_topology()
    print(f"配网设备: {len(dist_topo.device_map)} 个")

    for line in lines:
        if line in FEEDER_MAP:
            run_check(line, dist_topo)
        else:
            print(f"[跳过] 未知馈线: {line}")
    print("\n全部校验完成！")
