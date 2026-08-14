#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集修正脚本
根据答疑文档要求：
1. 配网遥测/信重复记录按 TRAN_ID + DATA_DATE 去重
2. 设备类型码1312 应为 1321
"""

import os
import re
from collections import defaultdict

DATA_DIR = r"c:\Users\1\Desktop\power_topology_verify\数据集更新版20260729\sql形式数据集"

def fix_pwreal_duplicates():
    """修正JBS_PWREAL表中的重复记录"""
    print("=" * 60)
    print("任务1: 检查并修正JBS_PWREAL表重复记录")
    print("=" * 60)
    
    filepath = os.path.join(DATA_DIR, "EQUIP_JBS_PWREAL.sql")
    
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return
    
    # 读取文件
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    print(f"总记录数: {len(lines)}")
    
    # 解析记录，按TRAN_ID + DATA_DATE去重
    records = {}  # key: (TRAN_ID, DATA_DATE), value: line
    duplicates = []
    
    pattern = re.compile(r"VALUES\('(\d+)','([^']+)','([^']+)'")
    
    for line in lines:
        line = line.strip()
        if not line or not line.startswith('INSERT'):
            continue
        
        match = pattern.search(line)
        if match:
            num = match.group(1)
            tran_id = match.group(2)
            data_date = match.group(3)
            
            key = (tran_id, data_date)
            
            if key in records:
                duplicates.append({
                    'num': num,
                    'tran_id': tran_id,
                    'data_date': data_date,
                    'line': line
                })
            else:
                records[key] = line
    
    print(f"去重后记录数: {len(records)}")
    print(f"重复记录数: {len(duplicates)}")
    
    if duplicates:
        print("\n重复记录示例（前5条）:")
        for dup in duplicates[:5]:
            print(f"  NUM={dup['num']}, TRAN_ID={dup['tran_id']}, DATA_DATE={dup['data_date']}")
        
        # 写入去重后的文件
        output_lines = [records[key] + '\n' for key in sorted(records.keys())]
        
        # 备份原文件
        backup_path = filepath + '.bak'
        if not os.path.exists(backup_path):
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"\n已备份原文件到: {backup_path}")
        
        # 写入去重后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        
        print(f"已写入去重后的文件: {filepath}")
        print(f"修正了 {len(duplicates)} 条重复记录")
    else:
        print("\n未发现重复记录，无需修正")

def check_and_fix_device_type_code():
    """检查并修正设备类型码1312→1321"""
    print("\n" + "=" * 60)
    print("任务2: 检查设备类型码1312")
    print("=" * 60)
    
    # 先检查设备字典表
    dict_file = os.path.join(DATA_DIR, "EQUIP_JBS_ZD_OBJECT.sql")
    
    if os.path.exists(dict_file):
        with open(dict_file, 'r', encoding='utf-8', errors='ignore') as f:
            dict_content = f.read()
        
        has_1312 = '1312' in dict_content
        has_1321 = '1321' in dict_content
        
        print(f"设备字典表中是否存在1312: {has_1312}")
        print(f"设备字典表中是否存在1321: {has_1321}")
        
        if has_1312:
            print("\n在设备字典表中找到1312，需要修正为1321")
            # 修正字典表
            with open(dict_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 备份
            backup_path = dict_file + '.bak'
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已备份原文件到: {backup_path}")
            
            # 修正
            content_fixed = content.replace("'1312'", "'1321'")
            content_fixed = content_fixed.replace("DEV_1312", "DEV_1321")
            
            with open(dict_file, 'w', encoding='utf-8') as f:
                f.write(content_fixed)
            
            print(f"已修正设备字典表: {dict_file}")
    
    # 检查设备表中是否有使用1312的设备
    print("\n检查各设备表是否使用了1312类型码...")
    
    device_tables = [
        "EQUIP_JBS_PWEQUIPINFO.sql",
        "EQUIP_JBS_ZWEQUIPINFO.sql"
    ]
    
    found_1312 = False
    
    for table_file in device_tables:
        filepath = os.path.join(DATA_DIR, table_file)
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if '1312' in content:
            found_1312 = True
            print(f"在 {table_file} 中发现使用1312类型码的设备")
            
            # 显示包含1312的行
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '1312' in line:
                    print(f"  行 {i+1}: {line[:100]}...")
            
            # 修正
            backup_path = filepath + '.bak'
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  已备份原文件到: {backup_path}")
            
            content_fixed = content.replace("'1312'", "'1321'")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content_fixed)
            
            print(f"  已修正文件: {filepath}")
    
    if not found_1312:
        print("\n未在任何设备表中找到使用1312类型码的设备")

def main():
    print("数据集修正脚本")
    print("=" * 60)
    print(f"数据目录: {DATA_DIR}")
    print()
    
    # 执行修正任务
    fix_pwreal_duplicates()
    check_and_fix_device_type_code()
    
    print("\n" + "=" * 60)
    print("修正完成")
    print("=" * 60)

if __name__ == '__main__':
    main()