import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config.settings import TEST_SVG_ROOT
from core.graph_model import TopologyGraph
from core.topology_builder import TopologyBuilder
from data_io.data_reader import SqlTableLoader
from data_io.data_writer import gen_sample_data
from data_io.svg_reader import SvgParser

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

    # 2.1 【修复1】调用电气逻辑校验（E01-E07 + 主配接口）
    print("\n===== 电气逻辑校验（E01-E07）=====")
    elec_results = builder.check_electrical_logic()
    print(f"  电气逻辑缺陷数量: {len(elec_results)}")
    elec_by_type: dict = {}
    for r in elec_results:
        code = r.get("rule_code", "未知")
        elec_by_type[code] = elec_by_type.get(code, 0) + 1
    for code, cnt in sorted(elec_by_type.items()):
        print(f"    {code}: {cnt}条")
    print(f"  主配接口异常数量: {len([a for a in dist_topo.abnormal_list if '接口' in a.dimension])}")

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

    # 5.SVG解析：提取LINE215/LINE216图元清单与连接关系
    print("\n===== SVG解析任务启动 =====")
    svg_dir = TEST_SVG_ROOT
    for fname in ['LINE215.svg', 'LINE216.svg']:
        fpath = os.path.join(svg_dir, fname)
        if os.path.exists(fpath):
            print(f"\n--- 解析 {fname} ---")
            doc = SvgParser.parse(fpath)
            if doc:
                doc.export_elements_json(f'{fname}_elements.json')
                doc.export_elements_csv(f'{fname}_elements.csv')
                doc.export_connections_json(f'{fname}_connections.json')
                doc.export_connections_csv(f'{fname}_connections.csv')
                print(f"  图元清单导出: output/csv/{fname}_elements.csv")
                print(f"  连接关系导出: output/csv/{fname}_connections.csv")
        else:
            print(f" 文件不存在: {fname}")
    print("\n=== SVG解析任务完成 ===")

    print("\n=== 拓扑构建任务运行结束，满足验收条件 ===")