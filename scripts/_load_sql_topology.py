"""
_load_sql_topology.py - 加载 input/sql_gbk 下 SQL 并构造 TopologyBuilder 所需 table_data。

TopologyBuilder(table_data) 入参格式：
  table_data = {"equip": DataFrame, "line": DataFrame}
  equip_df 列：EQUIP_ID, EQUIP_NAME, EQUIP_TYPE, VOLTAGE_TYPE, FEEDER_ID, DSUBSTATION_ID
  line_df  列：LINE_ID, START_ST_ID, END_ST_ID, LINE_NAME

使用方式：
  from scripts._load_sql_topology import load_sql_topology
  table_data, builder, (main_topo, dist_topo), stats = load_sql_topology()
"""
from __future__ import annotations

import os
import sys

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder


def load_sql_topology(verbose: bool = True):
    """完整链路：读SQL -> 构造table_data -> build_full_topology -> 返回统计。

    Returns:
        (table_data, builder, (main_topo, dist_topo), statistics)
    """
    loader = SqlTableLoader()
    table_data = loader.load_all_topo_tables()
    if verbose:
        print(f"[LOAD] equip表: {len(table_data['equip'])} 行")
        print(f"[LOAD] line表:  {len(table_data['line'])} 行")
        if len(table_data['equip']) > 0:
            print(f"[LOAD] equip列名: {list(table_data['equip'].columns)}")

    builder = TopologyBuilder(table_data)
    main_topo, dist_topo = builder.build_full_topology()
    stat_main = builder.get_topo_statistics(main_topo, "主网110kV")
    stat_dist = builder.get_topo_statistics(dist_topo, "配网10kV")

    if verbose:
        print(f"[BUILD] 主网: 节点={stat_main['总节点(端点)数']}, 边={stat_main['总边数(线路+内部通路)']}, "
              f"连通分量={stat_main['连通分量数量']}")
        print(f"[BUILD] 配网: 节点={stat_dist['总节点(端点)数']}, 边={stat_dist['总边数(线路+内部通路)']}, "
              f"连通分量={stat_dist['连通分量数量']}, 设备数={len(stat_dist['设备ID清单'])}")
    return table_data, builder, (main_topo, dist_topo), {"main": stat_main, "dist": stat_dist}


if __name__ == "__main__":
    load_sql_topology()
