# JSON/CSV 统一输出工具
import sys
import os

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import pandas as pd
import json
import uuid

from config.settings import OUTPUT_CSV, OUTPUT_JSON
from core.graph_model import AbnormalItem
from core.log_config import get_logger

logger = get_logger(__name__)


def export_abnormal_csv(data_list, file_name="problem_list.csv"):
    """导出问题清单 CSV，字段固定可追溯。"""
    df = pd.DataFrame([item.model_dump() for item in data_list])
    save_path = os.path.join(OUTPUT_CSV, file_name)
    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    logger.info("Exported CSV -> %s (%d rows)", save_path, len(df))
    return save_path


def export_abnormal_json(data_list, file_name="problem_list.json"):
    """导出结构化 JSON。"""
    save_path = os.path.join(OUTPUT_JSON, file_name)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump([item.model_dump() for item in data_list], f, ensure_ascii=False, indent=2)
    logger.info("Exported JSON -> %s (%d rows)", save_path, len(data_list))
    return save_path


def gen_sample_data():
    """生成空白样例数据（用于交付样例文件）。"""
    sample = AbnormalItem(
        trace_uuid=str(uuid.uuid4()),
        equip_id="DEV_TEST_001",
        point_id="PT_001",
        line_id="10kVLINE003",
        rule_code="R001",
        rule_desc="设备拓扑度数为0，判定悬空设备",
        check_result="异常",
        review_status="待复核",
        detail="该设备无任何线路连接，判定悬空",
    )
    csv_path = export_abnormal_csv([sample], "sample_abnormal.csv")
    json_path = export_abnormal_json([sample], "sample_abnormal.json")
    return csv_path, json_path


if __name__ == "__main__":
    gen_sample_data()
