import sys, os
sys.path.insert(0, os.getcwd())
from data_io.data_reader import SqlTableLoader
loader = SqlTableLoader()
td = loader.load_all_topo_tables()
equip_df = td['equip']
line_df = td['line']

with open('verify_mapping.log', 'w', encoding='utf-8') as f:
    # 验证 LINE_ID == FEEDER_ID
    f.write("=== 验证 LINE_ID == FEEDER_ID 假设 ===\n\n")

    # 查 line 表中 LINE215/LINE216/10kVLINE111/10kVLINE074 的 LINE_ID
    for kw in ['LINE215', 'LINE216', '10kVLINE111', '10kVLINE074', '10kVLINE098']:
        row = line_df[line_df['LINE_NAME'].astype(str) == kw]
        if len(row) > 0:
            lid = row.iloc[0]['LINE_ID']
            cnt = (equip_df['FEEDER_ID'].astype(str) == str(lid)).sum()
            f.write(f"{kw}: LINE_ID={lid}, FEEDER_ID={lid} 下设备数 = {cnt}\n")

    # 看 FEEDER_ID 中前 10 大的是否有对应的 LINE_NAME
    f.write("\n=== Top 10 FEEDER_ID 及其对应 LINE_NAME ===\n")
    top_feeders = equip_df['FEEDER_ID'].astype(str).value_counts().head(10)
    for fid, cnt in top_feeders.items():
        r = line_df[line_df['LINE_ID'].astype(str) == fid]
        lnm = r.iloc[0]['LINE_NAME'] if len(r) > 0 else '(no match)'
        f.write(f"  FEEDER_ID={fid}: {cnt} devices, LINE_NAME={lnm}\n")

    # 10kVLINE111 的 FEEDER_ID = TMP00000033 有多少设备？
    f.write("\n=== 10kVLINE111 检查 ===\n")
    fid_111 = 'TMP00000033'
    cnt_111 = (equip_df['FEEDER_ID'].astype(str) == fid_111).sum()
    f.write(f"FEEDER_ID={fid_111}: {cnt_111} devices\n")

    # FEEDER_ID 最后 3 位含 111 的是哪个？
    f.write("\n=== 查找 FEEDER_ID 含 '111' 的 ===\n")
    mask = equip_df['FEEDER_ID'].astype(str).str.contains('111', na=False)
    if mask.any():
        uniq = equip_df[mask]['FEEDER_ID'].astype(str).unique()
        for u in uniq:
            cnt = (equip_df['FEEDER_ID'].astype(str) == u).sum()
            f.write(f"  {u}: {cnt} devices\n")

print("done -> verify_mapping.log")
