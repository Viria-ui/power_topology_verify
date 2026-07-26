import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 输入路径（对应你本地存放的SQL、SVG）
INPUT_SQL_DIR = os.path.join(BASE_DIR, "input", "sql")
INPUT_SVG_DIR = os.path.join(BASE_DIR, "input", "svg")
RULE_JSON_PATH = os.path.join(BASE_DIR, "config", "rule_config.json")

# 输出路径
OUTPUT_CSV = os.path.join(BASE_DIR, "output", "csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "output", "json")
OUTPUT_SQL = os.path.join(BASE_DIR, "output", "sql")
OUTPUT_SVG = os.path.join(BASE_DIR, "output", "svg")
OUTPUT_LOG = os.path.join(BASE_DIR, "output", "log")

# 自动创建输出文件夹
for path in [OUTPUT_CSV, OUTPUT_JSON, OUTPUT_SQL, OUTPUT_SVG, OUTPUT_LOG]:
    os.makedirs(path, exist_ok=True)

# 核心主键映射（SQL字段固定）
PRIMARY_KEY = {
    "equip_id": "EQUIP_ID",       # 设备主键
    "line_id": "LINE_ID",         # 线路主键
    "feeder_id": "FEEDER_ID"      # 馈线编号，匹配svg文件名10kVLINExxx
}

# ========== 新增：比赛测试SQL路径、电压等级、设备内部连通规则 ==========
# 外部比赛测试数据集绝对路径
TEST_SQL_ROOT = r"C:\Users\Xu's\Desktop\CP-202606-面向新型电力系统的配电网图模拓扑智能识别与修正研究比赛资料\sql形式数据集"

# 电压等级常量（区分主网/配网）
MAIN_VOLTAGE = "110"    # 主网电压标识
DIST_VOLTAGE = "10"     # 配网电压标识

# 设备内部连通规则配置
DEVICE_INTERNAL_RULE = {
    "变压器": "高低压两端连通",
    "断路器": "进出线端子连通",
    "隔离开关": "进出线端子连通",
    "母线": "所有端子互相连通",
    "负荷": "单端子无内部连接"
}