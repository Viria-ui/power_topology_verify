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

    @staticmethod
    def _extract_balanced(text: str, start: int) -> tuple[str, int]:
        """从start位置（必须指向开括号'('）提取平衡括号内容，返回(内容, 结束位置)。

        引号感知：单引号内的逗号/括号/分号不参与括号深度计数，
        单引号转义('')正确处理。用于可靠切分含逗号的值。
        """
        depth = 0
        i = start
        in_quote = False
        while i < len(text):
            c = text[i]
            if in_quote:
                if c == "'":
                    if i + 1 < len(text) and text[i + 1] == "'":
                        i += 2  # SQL单引号转义
                        continue
                    in_quote = False
            else:
                if c == "'":
                    in_quote = True
                elif c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        # start指向开括号'('，返回括号【内】内容
                        return text[start + 1:i], i + 1
            i += 1
        return text[start:], len(text)

    @staticmethod
    def _split_values_tuple(tuple_str: str) -> list[str]:
        """切分一个VALUES元组内的各值（引号感知，值内逗号不切分）。"""
        vals = []
        cur = []
        i = 0
        n = len(tuple_str)
        in_quote = False
        while i < n:
            c = tuple_str[i]
            if in_quote:
                if c == "'":
                    if i + 1 < n and tuple_str[i + 1] == "'":
                        cur.append("''")
                        i += 2
                        continue
                    in_quote = False
                    cur.append(c)
                else:
                    cur.append(c)
            else:
                if c == "'":
                    in_quote = True
                    cur.append(c)
                elif c == ',':
                    vals.append(''.join(cur).strip().strip("'"))
                    cur = []
                else:
                    cur.append(c)
            i += 1
        if cur or vals:
            vals.append(''.join(cur).strip().strip("'"))
        return vals

    def parse_sql_insert_to_df(self, sql_file_path: str) -> pd.DataFrame:
        """【M9修复】括号深度感知SQL INSERT解析器。

        替代原脆弱正则（值内逗号截断/多行VALUES不匹配/引号转义无保护）。
        支持：
          - "SCHEMA"."TABLE"("COL1","COL2") VALUES (...) 双引号格式
          - 单条INSERT多值元组 VALUES (...),(...),...;
          - 值内逗号、单引号转义('')
        """
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

        cols: list[str] = []
        rows: list[list[str]] = []
        # 定位每条 INSERT INTO ... ( 语句
        insert_re = re.compile(
            r'INSERT\s+INTO\s+(?:"?[\w.$]+"?\s*\.\s*)?"?[\w$]+"?\s*\(', re.I)
        pos = 0
        while True:
            m = insert_re.search(sql_text, pos)
            if not m:
                break
            # 提取列名段（第一个平衡括号）
            col_str, after_col = self._extract_balanced(sql_text, m.end() - 1)
            # 列名拆分：兼容 "COL1","COL2" 与 COL1,COL2
            col_items = [c.strip().strip('"').strip("'") for c in col_str.split(",")]
            if not cols:
                cols = col_items
            # 定位 VALUES
            vals_pos = sql_text.find('VALUES', after_col)
            if vals_pos == -1:
                pos = after_col
                continue
            # 提取 VALUES 后的全部元组 (..),(..),... 直到分号
            scan = vals_pos + len('VALUES')
            while True:
                # 跳过空白与逗号
                while scan < len(sql_text) and sql_text[scan] in ' \t\r\n,':
                    scan += 1
                if scan >= len(sql_text):
                    break
                if sql_text[scan] == '(':
                    tuple_str, scan = self._extract_balanced(sql_text, scan)
                    vals = self._split_values_tuple(tuple_str)
                    rows.append(vals)
                elif sql_text[scan] == ';':
                    scan += 1
                    break
                else:
                    # 非元组内容（注释等），移动到下一个分号
                    semi = sql_text.find(';', scan)
                    scan = semi + 1 if semi != -1 else len(sql_text)
                    break
            pos = scan

        # 无数据返回空表，避免报错
        if not rows:
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(rows, columns=cols)

    def load_all_topo_tables(self):
        table_map = {
            "equip": "EQUIP_JBS_PWEQUIPINFO.sql",
            "line": "EQUIP_JBS_PWFEEDERLINE.sql",
            "pw_terminal": "EQUIP_JBS_PWTERMINAL.sql",
            "terminal": "EQUIP_JBS_PWTERMINAL.sql",
            # 主网端子表是可选数据：纯配网数据集可能不提供该文件。
            "zw_terminal": "EQUIP_JBS_ZWTERMINAL.sql",
            "yx_real": "EQUIP_JBS_PWREAL.sql",
            "zw_equip": "EQUIP_JBS_ZWEQUIPINFO.sql",
            "zw_line_end": "EQUIP_JBS_ZWLINEEND.sql",
            "zw_substation": "EQUIP_JBS_ZWSUBSTATION.sql",
            "zw_mea": "EQUIP_JBS_ZWMEA.sql",
            "zw_signal": "EQUIP_JBS_ZWSIGNAL.sql",
        }
        table_data = {}
        for key, fname in table_map.items():
            fpath = os.path.join(self.sql_dir, fname)
            if not os.path.isfile(fpath):
                # 不要用 None 表示缺表。下游可统一按 DataFrame 处理，纯配网
                # 模式也不会因主网增量文件缺失而中断。
                print(f"[警告] 未找到 SQL 表文件：{fname}，按空表处理")
                table_data[key] = pd.DataFrame()
            else:
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
