# -*- coding: utf-8 -*-
"""检查tie_loop_list的数据结构"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder


def main():
    print("加载数据...")
    loader = SqlTableLoader()
    table_data = loader.load_all_topo_tables()
    
    print("构建拓扑...")
    builder = TopologyBuilder(table_data)
    main_topo, dist_topo = builder.build_full_topology()
    
    tie_loop_list = dist_topo.tie_loop_list
    print(f"\ntie_loop_list 总数: {len(tie_loop_list)}")
    
    if tie_loop_list:
        print("\n前5条记录的字段:")
        for i, item in enumerate(tie_loop_list[:5]):
            print(f"\n--- 第{i+1}条 ---")
            if hasattr(item, '__dict__'):
                for k, v in item.__dict__.items():
                    print(f"  {k}: {v}")
            elif isinstance(item, dict):
                for k, v in item.items():
                    print(f"  {k}: {v}")
        
        # 统计result_type的所有可能值
        result_types = {}
        for item in tie_loop_list:
            if hasattr(item, 'result_type'):
                rt = item.result_type
            elif isinstance(item, dict):
                rt = item.get('result_type', 'N/A')
            else:
                rt = 'UNKNOWN'
            result_types[rt] = result_types.get(rt, 0) + 1
        
        print("\n\nresult_type 统计:")
        for rt, count in sorted(result_types.items(), key=lambda x: -x[1]):
            print(f"  '{rt}': {count}条")


if __name__ == "__main__":
    main()
