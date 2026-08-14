# SQL数据集读取基类
import sys
import os
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import pandas as pd
import glob
import re
from config.settings import TEST_SQL_ROOT

class SqlTableLoader:
    def __init__(self):
        self.sql_dir = TEST_SQL_ROOT

    def parse_sql_insert_to_df(self, sql_file_path: str) -> pd.DataFrame:
        """适配PostgreSQL带双引号、schema前缀的INSERT语句解析"""
        # 优先 GBK（项目 input/sql_gbk），失败回退 UTF-8
        sql_text = None
        for enc in ("gbk", "gb18030", "utf-8-sig", "utf-8"):
            try:
                with open(sql_file_path, "r", encoding=enc) as f:
                    sql_text = f.read()
                break
            except UnicodeDecodeError:
                continue
        if sql_text is None:
            with open(sql_file_path, "r", encoding="utf-8", errors="ignore") as f:
                sql_text = f.read()
        
        # 正则匹配：兼容 "SCHEMA"."TABLE"("COL1","COL2") VALUES (...) 双引号格式
        pattern = re.compile(r'INSERT INTO .*?\("(.*?)"\)\s*VALUES\s*\((.*?)\);', re.S)
        cols = []
        rows = []
        for match in pattern.finditer(sql_text):
            col_str = match.group(1).strip()
            val_str = match.group(2).strip()
            # 拆分带双引号的列名 "EQUIP_ID","EQUIP_NAME"
            cols = [c.strip() for c in col_str.split('","')]
            # 拆分数值，去除单引号
            vals = [v.strip().strip("'") for v in val_str.split(",")]
            rows.append(vals)
        
        # 无数据返回空表，避免报错
        if not rows:
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(rows, columns=cols)

    def load_all_topo_tables(self):
        """批量加载拓扑所需两张核心表"""
        table_map = {
            "equip": "EQUIP_JBS_PWEQUIPINFO.sql",
            "line": "EQUIP_JBS_PWFEEDERLINE.sql"
        }
        table_data = {}
        for key, fname in table_map.items():
            fpath = os.path.join(self.sql_dir, fname)
            table_data[key] = self.parse_sql_insert_to_df(fpath)
            # 统一字段类型（全部字符串）
            table_data[key] = table_data[key].astype(str)
            table_data[key] = table_data[key].apply(lambda col: col.str.strip())
        return table_data
# 单独测试读取SQL
if __name__ == "__main__":
    loader = SqlTableLoader()
    data = loader.load_all_topo_tables()
    print("设备表行数：", len(data["equip"]))
    print("线路表行数：", len(data["line"]))
    print("设备表列名：", list(data["equip"].columns))
    print("设备表示例前3行：\n", data["equip"].head(3))