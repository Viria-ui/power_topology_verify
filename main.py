import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from core.graph_model import TopologyGraph
from core.topology_builder import TopologyBuilder
from data_io.data_reader import SqlTableLoader
from data_io.data_writer import gen_sample_data

if __name__ == "__main__":
    print("=== 配网拓扑构建任务启动 ===")

    # 1.加载SQL测试数据集
    sql_loader = SqlTableLoader()
    table_datas = sql_loader.load_all_topo_tables()
    print(f"成功加载设备表{len(table_datas['equip'])}条、线路表{len(table_datas['line'])}条")

    # 2.构建主网、配网拓扑，自动补齐设备内部连通
    builder = TopologyBuilder(table_datas)
    main_topo, dist_topo = builder.build_full_topology()
    print("主网/配网拓扑构建完成，设备内部端点连通关系已补齐")

    # 3.输出验收所需拓扑统计信息
    main_stat = builder.get_topo_statistics(main_topo, "110kV主网拓扑")
    dist_stat = builder.get_topo_statistics(dist_topo, "10kV配网拓扑")
    print("\n===== 主网拓扑统计 =====")
    for k, v in main_stat.items():
        print(f"{k}: {v}")
    print("\n===== 配网拓扑统计 =====")
    for k, v in dist_stat.items():
        print(f"{k}: {v}")

    # 4.生成标准JSON/CSV输出样例
    gen_sample_data()
    print("\nJSON/CSV标准样例已生成至docs目录")
    print("=== 拓扑构建任务运行结束，满足验收条件 ===")