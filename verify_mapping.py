"""验证 LINE_ID == FEEDER_ID 映射关系，日志写入 OUTPUT_LOG 目录。"""
import sys
import os

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_FILE)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.settings import OUTPUT_LOG
from data_io.data_reader import SqlTableLoader
from core.log_config import get_logger

logger = get_logger(__name__)


def main():
    loader = SqlTableLoader()
    td = loader.load_all_topo_tables()
    equip_df = td['equip']
    line_df = td['line']

    os.makedirs(OUTPUT_LOG, exist_ok=True)
    log_path = os.path.join(OUTPUT_LOG, "verify_mapping.log")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=== 验证 LINE_ID == FEEDER_ID 假设 ===\n\n")
        for kw in ['LINE215', 'LINE216', '10kVLINE111', '10kVLINE074', '10kVLINE098']:
            row = line_df[line_df['LINE_NAME'].astype(str) == kw]
            if len(row) > 0:
                lid = row.iloc[0]['LINE_ID']
                cnt = (equip_df['FEEDER_ID'].astype(str) == str(lid)).sum()
                f.write(f"{kw}: LINE_ID={lid}, FEEDER_ID={lid} 下设备数 = {cnt}\n")

        f.write("\n=== Top 10 FEEDER_ID 及其对应 LINE_NAME ===\n")
        top_feeders = equip_df['FEEDER_ID'].astype(str).value_counts().head(10)
        for fid, cnt in top_feeders.items():
            r = line_df[line_df['LINE_ID'].astype(str) == fid]
            lnm = r.iloc[0]['LINE_NAME'] if len(r) > 0 else '(no match)'
            f.write(f"  FEEDER_ID={fid}: {cnt} devices, LINE_NAME={lnm}\n")

        f.write("\n=== 10kVLINE111 检查 ===\n")
        fid_111 = 'TMP00000033'
        cnt_111 = (equip_df['FEEDER_ID'].astype(str) == fid_111).sum()
        f.write(f"FEEDER_ID={fid_111}: {cnt_111} devices\n")

        f.write("\n=== 查找 FEEDER_ID 含 '111' 的 ===\n")
        mask = equip_df['FEEDER_ID'].astype(str).str.contains('111', na=False)
        if mask.any():
            uniq = equip_df[mask]['FEEDER_ID'].astype(str).unique()
            for u in uniq:
                cnt = (equip_df['FEEDER_ID'].astype(str) == u).sum()
                f.write(f"  {u}: {cnt} devices\n")

    logger.info("Mapping verification complete -> %s", log_path)


if __name__ == "__main__":
    main()
