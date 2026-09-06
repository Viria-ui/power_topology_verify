# -*- coding: utf-8 -*-
"""
=====================================
快速测试脚本 - 验证修复结果
=====================================
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder
from core.telemetry_evaluator import TelemetryEvaluator
from config.settings import OUTPUT_JSON


def safe_get(obj, key, default=None):
    """安全获取属性或字典值"""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def main():
    print("\n" + "=" * 70)
    print("   快速测试 - 验证修复结果")
    print("=" * 70)
    
    # 1. 加载数据
    print("\n[1] 加载SQL数据...")
    loader = SqlTableLoader()
    table_data = loader.load_all_topo_tables()
    print(f"  设备表: {len(table_data.get('equip', []))} 条")
    print(f"  线路表: {len(table_data.get('line', []))} 条")
    
    # 2. 构建拓扑
    print("\n[2] 构建拓扑...")
    builder = TopologyBuilder(table_data)
    main_topo, dist_topo = builder.build_full_topology()
    print(f"  主网设备: {len(main_topo.device_map)} 个")
    print(f"  配网设备: {len(dist_topo.device_map)} 个")
    
    # 3. 检查联络开关检测
    print("\n[3] 检查联络开关数据...")
    
    # 检查tie_loop_list
    tie_loop_list = safe_get(dist_topo, 'tie_loop_list', [])
    abnormal_list = safe_get(dist_topo, 'abnormal_list', [])
    electrical_defects = safe_get(dist_topo, 'electrical_defects', [])
    breakpoint_list = safe_get(dist_topo, 'breakpoint_list', [])
    
    print(f"  tie_loop_list: {len(tie_loop_list)} 条")
    print(f"  abnormal_list: {len(abnormal_list)} 条")
    print(f"  electrical_defects: {len(electrical_defects)} 条")
    print(f"  breakpoint_list: {len(breakpoint_list)} 条")
    
    # 4. 分析联络开关
    print("\n[4] 分析联络开关...")
    tie_switches = []
    loops = []
    for item in tie_loop_list:
        rt = safe_get(item, 'result_type', '')
        d = item.dict() if hasattr(item, 'dict') else (item if isinstance(item, dict) else {})
        if '联络' in str(rt):
            tie_switches.append(d)
        elif '合环' in str(rt):
            loops.append(d)
    
    print(f"  联络开关: {len(tie_switches)} 个")
    print(f"  合环: {len(loops)} 个")
    
    # 5. 分析电气逻辑异常
    print("\n[5] 分析电气逻辑异常...")
    rule_stats = {}
    for r in electrical_defects:
        if isinstance(r, dict):
            rule = r.get('rule_code', 'UNKNOWN')
        else:
            rule = getattr(r, 'rule_code', 'UNKNOWN')
        rule_stats[rule] = rule_stats.get(rule, 0) + 1
    
    print("  E01-E07规则命中:")
    for rule, count in sorted(rule_stats.items()):
        print(f"    - {rule}: {count} 处")
    print(f"  总计: {len(electrical_defects)} 条")
    
    # 6. 分析拓扑异常
    print("\n[6] 分析拓扑异常...")
    abnormal_stats = {'悬空': 0, '孤岛': 0, '断点': 0, '其他': 0}
    for a in abnormal_list:
        desc = safe_get(a, 'rule_desc', safe_get(a, 'rule_code', ''))
        if '悬空' in str(desc):
            abnormal_stats['悬空'] += 1
        elif '孤岛' in str(desc):
            abnormal_stats['孤岛'] += 1
        elif '断点' in str(desc):
            abnormal_stats['断点'] += 1
        else:
            abnormal_stats['其他'] += 1
    
    print("  拓扑异常分类:")
    for k, v in abnormal_stats.items():
        if v > 0:
            print(f"    - {k}: {v} 处")
    
    # 7. 质量评分
    print("\n[7] 质量评分...")
    from core.score_engine import ScoreAndConfidenceEngine
    from core.telemetry_evaluator import TelemetryEvaluator
    
    tele_evaluator = safe_get(builder, 'telemetry_evaluator')
    if not tele_evaluator:
        yx_real_df = table_data.get('yx_real', pd.DataFrame())
        tele_evaluator = TelemetryEvaluator.from_pwreal(yx_real_df)
    
    score_engine = ScoreAndConfidenceEngine(tele_evaluator)
    
    # 构建缺陷列表
    defects_report = []
    for a in abnormal_list:
        defects_report.append({
            'defect_type': safe_get(a, 'rule_code', 'UNKNOWN'),
            'description': safe_get(a, 'detail', ''),
            'dimension': safe_get(a, 'dimension', '拓扑完整性')
        })
    
    score_summary = score_engine.evaluate_quality_score(
        defects_report=defects_report,
        total_equip_count=len(dist_topo.device_map),
        repaired_defect_ids=[]
    )
    
    print(f"  修正前评分: {score_summary.get('score_before', 'N/A')}")
    print(f"  修正后评分: {score_summary.get('score_after', 'N/A')}")
    print(f"  缺陷数: {score_summary.get('defect_count', 0)}")
    
    dim = score_summary.get('dimension_deduction', {})
    if dim:
        print("  维度扣分:")
        for k, v in dim.items():
            print(f"    - {k}: {v}")
    
    # 8. 保存汇总
    print("\n[8] 保存汇总...")
    summary = {
        "tie_switches": len(tie_switches),
        "loops": len(loops),
        "abnormal_list": len(abnormal_list),
        "electrical_defects": len(electrical_defects),
        "breakpoint_list": len(breakpoint_list),
        "rule_stats": rule_stats,
        "abnormal_stats": abnormal_stats,
        "score_before": score_summary.get('score_before'),
        "score_after": score_summary.get('score_after'),
        "defect_count": score_summary.get('defect_count', 0),
    }
    
    output_path = os.path.join(OUTPUT_JSON, "quick_test_summary.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"  已保存: {output_path}")
    
    print("\n" + "=" * 70)
    print("= 测试完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()
