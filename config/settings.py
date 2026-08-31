import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 输入路径（D盘项目内；GBK SQL 优先）
INPUT_SQL_DIR = os.path.join(BASE_DIR, "input", "sql_gbk")
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

# ========== 比赛数据集路径（7/29 基础 + 8/21 增量补丁）==========
DATASET_DIR_729 = os.path.join(BASE_DIR, "数据集更新版20260729")
DATASET_DIR_821 = os.path.join(BASE_DIR, "数据集更新版20260821")
DATASET_SQL_729 = os.path.join(DATASET_DIR_729, "sql形式数据集")
DATASET_SVG_729 = os.path.join(DATASET_DIR_729, "配网 svg")
DATASET_PATCH_821 = os.path.join(DATASET_DIR_821, "数据库更新脚本20260821.txt")
DATASET_STANDARD_OUTPUT_XLSX = os.path.join(DATASET_DIR_821, "拓扑校验问题标准输出.xlsx")
DATASET_UPDATE_NOTE_729 = os.path.join(DATASET_DIR_729, "数据集更新说明：.txt")

# 运行时 SQL：input/sql_gbk（由 scripts/sync_dataset.py 从 729 同步并叠加 821 补丁）
_TEST_SQL_GBK = os.path.join(BASE_DIR, "input", "sql_gbk")
_TEST_SQL_DATASET = DATASET_SQL_729
TEST_SQL_ROOT = _TEST_SQL_GBK if os.path.isdir(_TEST_SQL_GBK) else _TEST_SQL_DATASET

# SVG 配网单线图：7/29 更新版（含 objectid / GLink_Ref 修复与文件名对齐）
TEST_SVG_ROOT = DATASET_SVG_729 if os.path.isdir(DATASET_SVG_729) else os.path.join(BASE_DIR, "input", "svg")

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
