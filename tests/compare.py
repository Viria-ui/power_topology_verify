import sys
import os
import json

# 1. 确保项目根目录在 sys.path 中
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder

# ==========================================
# 步骤 1：加载数据库拓扑模型
# ==========================================
print("正在从 SQL 读取数据并构建拓扑模型...")
loader = SqlTableLoader()
table_data = loader.load_all_topo_tables()

builder = TopologyBuilder(table_data)
main_topo, dist_topo = builder.build_full_topology()
print(f"✅ 全库配网设备构建完成，总数：{len(dist_topo.device_map)} 个\n")

# ==========================================
# 步骤 2：读取 SVG 数据 (设备表 & 连接关系表)
# ==========================================
line_name = "LINE215"
json_elem_path = f"output/json/{line_name}.svg_elements.json"
json_conn_path = f"output/json/{line_name}.svg_connections.json"

# 2.1 读取设备图元并构建 element_id -> object_id 映射关系
with open(json_elem_path, "r", encoding="utf-8") as f:
    svg_elem_data = json.load(f)  # 确认此处变量名为 svg_elem_data

raw_elements = svg_elem_data.get("elements", [])
svg_device_map = {}          # object_id -> elem 详细信息
element_to_object_map = {}    # element_id (UUID) -> object_id (业务ID)

for elem in raw_elements:
    if isinstance(elem, dict):
        elem_id = elem.get("element_id")
        obj_id = elem.get("object_id") or elem.get("equip_id")
        
        if obj_id:
            obj_id_str = str(obj_id).strip()
            svg_device_map[obj_id_str] = elem
            if elem_id:
                element_to_object_map[str(elem_id).strip()] = obj_id_str

# 2.2 读取连接关系
svg_connections = []
if os.path.exists(json_conn_path):
    with open(json_conn_path, "r", encoding="utf-8") as f:
        svg_conn_data = json.load(f)
        svg_connections = svg_conn_data.get("connections", svg_conn_data.get("data", []))

print(f"✅ 从 SVG 读取设备：{len(svg_device_map)} 个，物理连接：{len(svg_connections)} 条\n")

# ==========================================
# 步骤 3：筛选数据库对应馈线设备
# ==========================================
line215_db_devices = {}
for equip_id, dev in dist_topo.device_map.items():
    dev_str = str(vars(dev))
    if "215" in dev_str or "LINE215" in dev_str or getattr(dev, 'feeder_id', '') == 'TMP00000160':
        line215_db_devices[equip_id] = dev

svg_dev_ids = set(svg_device_map.keys())
db_dev_ids = set(line215_db_devices.keys())

# 全局缺陷结果存储列表
defects_report = []

# ==========================================
# 校验 1：图上有，模型无
# ==========================================
type1_ids = svg_dev_ids - db_dev_ids
for dev_id in type1_ids:
    elem_info = svg_device_map.get(dev_id, {})
    dev_name = elem_info.get("object_name") or elem_info.get("element_type_cn") or "未知设备"
    defects_report.append({
        "equip_id": dev_id,
        "defect_type": "图上有模型无",
        "description": f"SVG图纸存在设备[{dev_name}](ID:{dev_id})，但数据库拓扑模型中缺失",
        "suggestion": f"建议在数据库设备表中补全设备 {dev_id} 信息",
        "sql_draft": f"INSERT INTO EQUIP_JBS_PWEQUIPINFO (EQUIP_ID, EQUIP_NAME) VALUES ('{dev_id}', '{dev_name}');"
    })

# ==========================================
# 校验 2：模型有，图上无
# ==========================================
type2_ids = db_dev_ids - svg_dev_ids
for dev_id in type2_ids:
    db_dev = line215_db_devices[dev_id]
    dev_name = getattr(db_dev, 'equip_name', '未知设备')
    defects_report.append({
        "equip_id": dev_id,
        "defect_type": "模型有图上无",
        "description": f"数据库拓扑模型存在设备[{dev_name}](ID:{dev_id})，但SVG图纸未绘制该图元",
        "suggestion": f"建议重新补全SVG图纸绘图，增加设备 {dev_id} 图元",
        "sql_draft": f"-- 图纸层面补全，无需调整数据库数据"
    })

# ==========================================
# 校验 3：物理连接不一致 (已解决 UUID 到 object_id 的映射)
# ==========================================
for conn in svg_connections:
    if isinstance(conn, dict):
        from_elem_id = str(conn.get("from_element_id") or "").strip()
        to_elem_id = str(conn.get("to_element_id") or "").strip()
        
        # 将线段两端的 UUID 翻译成业务 object_id
        from_obj_id = element_to_object_map.get(from_elem_id)
        to_obj_id = element_to_object_map.get(to_elem_id)

        if from_obj_id and to_obj_id:
            has_edge = False
            if hasattr(dist_topo, 'graph'):
                has_edge = dist_topo.graph.has_edge(from_obj_id, to_obj_id) or dist_topo.graph.has_edge(to_obj_id, from_obj_id)
            
            if not has_edge:
                defects_report.append({
                    "equip_id": f"{from_obj_id} <-> {to_obj_id}",
                    "defect_type": "物理连接不一致",
                    "description": f"SVG图纸存在设备 {from_obj_id} 与 {to_obj_id} 的物理连接，但数据库拓扑网中缺失该连线",
                    "suggestion": "建议在数据库线路表 EQUIP_JBS_PWFEEDERLINE 中增补对应物理连接记录",
                    "sql_draft": f"INSERT INTO EQUIP_JBS_PWFEEDERLINE (START_EQUIP, END_EQUIP) VALUES ('{from_obj_id}', '{to_obj_id}');"
                })

# ==========================================
# 校验 4：逻辑连接/属性不一致
# ==========================================
common_ids = svg_dev_ids & db_dev_ids
for dev_id in common_ids:
    svg_elem = svg_device_map[dev_id]
    db_dev = line215_db_devices[dev_id]
    
    svg_voltage = svg_elem.get("voltage_level")
    db_voltage = getattr(db_dev, "voltage_type", None)
    
    if svg_voltage and db_voltage and (str(svg_voltage) not in str(db_voltage)):
        defects_report.append({
            "equip_id": dev_id,
            "defect_type": "逻辑连接不一致",
            "description": f"设备 {dev_id} 属性不一致：SVG电压等级为[{svg_voltage}]，而数据库模型属性为[{db_voltage}]",
            "suggestion": f"校对设备逻辑属性，统一将数据库更新为 SVG 图纸属性 [{svg_voltage}]",
            "sql_draft": f"UPDATE EQUIP_JBS_PWEQUIPINFO SET VOLTAGE_TYPE='{svg_voltage}' WHERE EQUIP_ID='{dev_id}';"
        })

# ==========================================
# 输出统计与导出 JSON 文件
# ==========================================
print("=" * 60)
print(f"📊 图模一致性校验完成！累计发现缺陷总数：{len(defects_report)} 条")
print("=" * 60)

type_counts = {}
for d in defects_report:
    t = d["defect_type"]
    type_counts[t] = type_counts.get(t, 0) + 1

for defect_type, count in type_counts.items():
    print(f"  • 【{defect_type}】: {count} 处")

output_json_path = f"output/{line_name}_缺陷清单报告.json"
os.makedirs("output", exist_ok=True)
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(defects_report, f, ensure_ascii=False, indent=4)

print(f"\n🎉 已成功将格式化缺陷清单（含设备ID、说明、修正建议、SQL草案）导出至文件：\n👉 {output_json_path}")