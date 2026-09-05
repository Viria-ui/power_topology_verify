# JSON/CSV统一输出工具
import sys
import os
# 把项目根目录加入Python检索路径，解决模块找不到问题
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# JSON/CSV统一输出工具
import pandas as pd
import json
import uuid
from config.settings import OUTPUT_CSV, OUTPUT_JSON
from core.graph_model import AbnormalItem

def export_abnormal_csv(data_list: list[AbnormalItem], file_name="problem_list.csv"):
    """导出问题清单CSV,字段固定可追溯"""
    df = pd.DataFrame([item.model_dump() for item in data_list])
    save_path = os.path.join(OUTPUT_CSV, file_name)
    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    return save_path

def export_abnormal_json(data_list: list[AbnormalItem], file_name="problem_list.json"):
    """导出结构化JSON"""
    save_path = os.path.join(OUTPUT_JSON, file_name)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump([item.model_dump() for item in data_list], f, ensure_ascii=False, indent=2)
    return save_path

# 生成空白样例数据（用于交付样例文件）
def gen_sample_data():
    sample = AbnormalItem(
        trace_uuid=str(uuid.uuid4()),
        equip_id="DEV_TEST_001",
        point_id="PT_001",
        line_id="10kVLINE003",
        rule_code="R001",
        rule_desc="设备拓扑度数为0，判定悬空设备",
        check_result="异常",
        review_status="待复核",
        detail="该设备无任何线路连接，判定悬空"
    )
    # 样例文件输出到项目根目录docs，不要复用export_abnormal_csv（它会强制拼接OUTPUT_CSV）
    docs_dir = os.path.join(PROJECT_ROOT, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    csv_path = os.path.join(docs_dir, "sample_abnormal.csv")
    df = pd.DataFrame([sample.model_dump()])
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    json_path = os.path.join(docs_dir, "sample_abnormal.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([sample.model_dump()], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    gen_sample_data()