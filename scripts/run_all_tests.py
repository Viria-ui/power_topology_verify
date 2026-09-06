# -*- coding: utf-8 -*-
"""
=====================================
图模质量校验及修正 - 综合测试脚本 v2.0
=====================================
根据参考文件中的测试任务全面执行各项校验功能
修复：SVG加载路径、联络开关检测、评分逻辑
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from data_io.data_reader import SqlTableLoader
from core.topology_builder import TopologyBuilder
from core.telemetry_evaluator import TelemetryEvaluator
from svg_io.svg_beautifier import SvgBeautifier
from svg_io.svg_auto_generator import SvgAutoGenerator
from core.graph_model import TopologyGraph
from config.settings import OUTPUT_SVG, OUTPUT_JSON, OUTPUT_CSV


def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subheader(title):
    print(f"\n## {title}")


def safe_get(obj, key, default=None):
    """安全获取属性或字典值"""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def to_dict(obj):
    """转换为字典"""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, 'dict'):
        return obj.dict()
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return {}


def load_data():
    """加载SQL数据"""
    print("\n[1] 加载数据...")
    loader = SqlTableLoader()
    table_data = loader.load_all_topo_tables()
    print(f"  设备表: {len(table_data.get('equip', []))} 条")
    print(f"  线路表: {len(table_data.get('line', []))} 条")
    print(f"  端子表: {len(table_data.get('terminal', []))} 条")
    print(f"  遥信遥测: {len(table_data.get('yx_real', []))} 条")
    print(f"  主网站点: {len(table_data.get('zw_substation', []))} 条")
    return table_data


def find_svg_file(line_name):
    """从多个可能路径中查找SVG文件"""
    possible_paths = [
        # 数据集目录
        os.path.join(os.path.dirname(OUTPUT_SVG), "..", "数据集更新版20260729", "配网 svg", f"{line_name}.svg"),
        os.path.join(os.path.dirname(OUTPUT_SVG), "..", "数据集更新版20260729", "配网 svg", f"10kV{line_name}.svg"),
        os.path.join(os.path.dirname(OUTPUT_SVG), "input", "svg", f"{line_name}.svg"),
        # output目录
        os.path.join(OUTPUT_SVG, f"{line_name}.svg"),
        os.path.join(OUTPUT_SVG, f"10kV{line_name}.svg"),
    ]
    
    for path in possible_paths:
        normalized = os.path.normpath(path)
        if os.path.exists(normalized):
            print(f"    找到SVG: {normalized}")
            return normalized
    return None


def test_module1_1_hanging_devices(dist_topo):
    """模块1.1: 设备拓扑悬空检测"""
    print_header("模块1.1: 设备拓扑悬空检测")
    
    hanging_count = 0
    hanging_list = []
    
    for eid, dev in dist_topo.device_map.items():
        if safe_get(dev, 'equip_type') in {'1705', '1706', '1707', '1708', '1709', '开关', '刀闸'}:
            points = dist_topo.get_device_all_points(eid) if hasattr(dist_topo, 'get_device_all_points') else []
            if len(points) == 1:
                # 检查是否为末端设备（豁免）
                equip_name = safe_get(dev, 'equip_name', '')
                equip_type = safe_get(dev, 'equip_type', '')
                # 豁免条件：配变、电缆终端头、备用间隔
                exempt_keywords = ['配变', '变压器', '用户', '终端', '备用']
                is_exempt = any(kw in str(equip_name) for kw in exempt_keywords)
                
                if not is_exempt:
                    hanging_count += 1
                    if len(hanging_list) < 10:
                        hanging_list.append({
                            'equip_id': eid,
                            'equip_name': equip_name,
                            'equip_type': equip_type,
                            'point_count': len(points)
                        })
    
    print(f"\n  [结果] 检测到 {hanging_count} 个悬空设备（开关/刀闸单端连接）")
    for h in hanging_list[:5]:
        print(f"    - {h['equip_id']}: {h['equip_name']}")
    
    return {"hanging_count": hanging_count, "hanging_list": hanging_list}


def test_module1_2_breakpoint_finding(dist_topo):
    """模块1.2: 拓扑连通性异常诊断与断点定位"""
    print_header("模块1.2: 拓扑连通性异常诊断与断点定位")
    
    import networkx as nx
    
    # 获取断点列表
    breakpoint_list = safe_get(dist_topo, 'breakpoint_list', [])
    print(f"\n  [拓扑校验] 断点数量: {len(breakpoint_list)}")
    
    # 测试任务1: 找TMP00013138至TMP00047197中间的断点
    print("\n[测试任务1] 拓扑找TMP00013138至TMP00047197中间的断点位置:")
    equip1, equip2 = "TMP00013138", "TMP00047197"
    
    G = safe_get(dist_topo, 'graph')
    if G and G.has_node(equip1) and G.has_node(equip2):
        if nx.has_path(G, equip1, equip2):
            path = nx.shortest_path(G, equip1, equip2)
            print(f"  路径存在: {equip1} → {equip2}")
            print(f"  路径长度: {len(path)} 跳")
            # 找路径中的开关设备
            switches_in_path = []
            for node in path[1:-1]:
                dev = dist_topo.device_map.get(node)
                if dev and safe_get(dev, 'switch_status') == '0':
                    switches_in_path.append(node)
            if switches_in_path:
                print(f"  路径中分位开关: {switches_in_path}")
        else:
            # 找断点
            print(f"  两设备间不存在连通路径！")
            # 找两个设备所在连通分量
            comps = list(nx.connected_components(G))
            for comp in comps:
                if equip1 in comp:
                    print(f"  {equip1}所在分量: {len(comp)}个设备")
                if equip2 in comp:
                    print(f"  {equip2}所在分量: {len(comp)}个设备")
    else:
        print(f"  设备不存在: {equip1 if not (G and G.has_node(equip1)) else equip2}")
    
    # 测试任务2
    print("\n[测试任务2] 拓扑找TMP00007913至TMP00007907中间的断点位置:")
    equip3, equip4 = "TMP00007913", "TMP00007907"
    
    if G and G.has_node(equip3) and G.has_node(equip4):
        if nx.has_path(G, equip3, equip4):
            path = nx.shortest_path(G, equip3, equip4)
            print(f"  路径存在: {equip3} → {equip4}")
            print(f"  路径长度: {len(path)} 跳")
            # 检查路径中的断点
            switches_open = []
            for node in path[1:-1]:
                dev = dist_topo.device_map.get(node)
                if dev and safe_get(dev, 'switch_status') == '0':
                    switches_open.append({
                        'equip_id': node,
                        'equip_name': safe_get(dev, 'equip_name', 'N/A'),
                        'status': '分位'
                    })
            if switches_open:
                print(f"  可能断点（分位开关）:")
                for s in switches_open[:5]:
                    print(f"    - {s['equip_id']}: {s['equip_name']} ({s['status']})")
        else:
            print(f"  两设备间不存在连通路径！")
    
    return {"breakpoint_count": len(breakpoint_list)}


def test_module1_3_tie_switch(dist_topo, line_df):
    """模块1.3: 联络开关自动识别与可视化"""
    print_header("模块1.3: 联络开关自动识别与可视化梳理")
    
    import networkx as nx
    
    # 从line表获取所有馈线信息
    tie_switches = []
    G = safe_get(dist_topo, 'graph')
    
    if line_df is not None and not line_df.empty:
        # 构建馈线ID到设备的映射
        feeder_devices = {}
        for eid, dev in dist_topo.device_map.items():
            fid = safe_get(dev, 'feeder_id')
            if fid:
                if fid not in feeder_devices:
                    feeder_devices[fid] = []
                feeder_devices[fid].append(eid)
        
        print(f"\n  馈线数量: {len(feeder_devices)}")
        
        # 识别联络开关：连接两条不同馈线的分位开关
        for eid, dev in dist_topo.device_map.items():
            if safe_get(dev, 'switch_status') == '0':  # 分位
                points = dist_topo.get_device_all_points(eid) if hasattr(dist_topo, 'get_device_all_points') else []
                if len(points) >= 2 and G:
                    # 检查是否连接了不同的馈线
                    connected_feeders = set()
                    for p in points:
                        if G.has_node(p):
                            for neighbor in G.neighbors(p):
                                neighbor_dev = dist_topo.device_map.get(neighbor)
                                if neighbor_dev:
                                    fid = safe_get(neighbor_dev, 'feeder_id')
                                    if fid:
                                        connected_feeders.add(fid)
                    
                    # 如果连接了多条馈线，可能是联络开关
                    if len(connected_feeders) >= 2:
                        tie_switches.append({
                            'equip_id': eid,
                            'equip_name': safe_get(dev, 'equip_name', 'N/A'),
                            'status': '分位',
                            'connected_feeders': list(connected_feeders),
                            'feeder_count': len(connected_feeders)
                        })
    
    print(f"\n  [结果] 识别到 {len(tie_switches)} 个联络开关")
    
    if tie_switches:
        print("\n  联络开关列表:")
        for ts in tie_switches[:10]:
            print(f"    - {ts['equip_id']}: {ts['equip_name']}")
            print(f"      连接的馈线: {ts['connected_feeders']}")
    
    # 导出联络关系
    if tie_switches:
        tie_output = os.path.join(OUTPUT_CSV, "tie_switches.csv")
        df = pd.DataFrame(tie_switches)
        df.to_csv(tie_output, index=False, encoding='utf-8-sig')
        print(f"\n  联络开关表格已导出: {tie_output}")
    
    return {"tie_switch_count": len(tie_switches), "tie_switches": tie_switches}


def test_module1_4_suspect_tie(dist_topo):
    """模块1.4: 疑似联络开关智能识别"""
    print_header("模块1.4: 疑似联络开关智能识别与复核研判")
    
    import networkx as nx
    
    suspect_list = []
    G = safe_get(dist_topo, 'graph')
    
    # 检测分闸非检修状态开关
    for eid, dev in dist_topo.device_map.items():
        if safe_get(dev, 'switch_status') == '0':  # 分位
            points = dist_topo.get_device_all_points(eid) if hasattr(dist_topo, 'get_device_all_points') else []
            if not points:
                continue
                
            # 检查单侧连通情况
            if G:
                connected_neighbors = set()
                for p in points:
                    if G.has_node(p):
                        for neighbor in G.neighbors(p):
                            if neighbor != eid:  # 排除自身
                                connected_neighbors.add(neighbor)
                
                # 单侧连接或连接设备少
                if len(connected_neighbors) <= 2:
                    equip_name = safe_get(dev, 'equip_name', 'N/A')
                    # 检查是否为正常分位开关
                    is_normal_open = '地刀' in str(equip_name) or '刀闸' in str(equip_name)
                    
                    if not is_normal_open:
                        suspect_list.append({
                            'equip_id': eid,
                            'equip_name': equip_name,
                            'status': '分位单侧连接',
                            'connected_count': len(connected_neighbors),
                            'suggestion': '检查是否为联络开关或存在拓扑缺失',
                            'issue_type': '单侧拓扑缺失' if len(connected_neighbors) <= 1 else '线路断连'
                        })
    
    print(f"\n  [结果] 识别到 {len(suspect_list)} 个疑似联络开关")
    
    for s in suspect_list[:5]:
        print(f"    - {s['equip_id']}: {s['equip_name']}")
        print(f"      状态: {s['status']} | 连接数: {s['connected_count']}")
        print(f"      问题类型: {s['issue_type']} | 建议: {s['suggestion']}")
    
    return {"suspect_count": len(suspect_list), "suspect_list": suspect_list}


def test_module1_5_unplanned_loop(dist_topo):
    """模块1.5: 非计划性合环拓扑识别"""
    print_header("模块1.5: 非计划性合环拓扑识别")
    
    import networkx as nx
    
    loops = []
    G = safe_get(dist_topo, 'graph')
    
    if G:
        # 找所有简单环（通过找所有连通分量中的环）
        for component in nx.connected_components(G):
            subgraph = G.subgraph(component)
            # 检查是否有环（不是树）
            if not nx.is_tree(subgraph):
                # 找环中的开关
                for cycle in nx.simple_cycles(subgraph):
                    if len(cycle) >= 3:
                        # 检查环中电源数量
                        source_count = 0
                        loop_devices = []
                        for node in cycle:
                            dev = dist_topo.device_map.get(node)
                            if dev:
                                is_source = safe_get(dev, 'is_source', False)
                                if is_source:
                                    source_count += 1
                                loop_devices.append({
                                    'equip_id': node,
                                    'equip_name': safe_get(dev, 'equip_name', 'N/A'),
                                    'is_source': is_source
                                })
                        
                        # 非计划合环：环中只有1个电源（正常应该有2个）
                        is_planned = source_count >= 2
                        
                        loops.append({
                            'loop_devices': cycle,
                            'source_count': source_count,
                            'is_planned_loop': is_planned,
                            'risk_level': '高' if not is_planned and source_count == 1 else '中',
                            'devices': loop_devices
                        })
    
    print(f"\n  [结果] 检测到 {len(loops)} 个合环")
    
    for loop in loops[:3]:
        print(f"    - 环长度: {len(loop['loop_devices'])} 设备")
        print(f"      电源数: {loop['source_count']}")
        print(f"      是否计划合环: {'是' if loop['is_planned_loop'] else '否'}")
        print(f"      风险: {loop['risk_level']}")
    
    return {"loop_count": len(loops), "loops": loops}


def load_svg_from_output(line_name):
    """从output目录加载已解析的SVG数据"""
    json_path = os.path.join(OUTPUT_JSON, f"{line_name}.svg_elements.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            elements = data.get('elements', [])
            svg_devices = {}
            for elem in elements:
                obj_id = elem.get('object_id') or elem.get('id')
                if obj_id:
                    svg_devices[obj_id] = elem
            return svg_devices, elements
    return {}, []


def test_module2_1_svg_vs_db_no_model(dist_topo, svg_data):
    """模块2.1: 图上有、模型无校验"""
    print_header("模块2.1: 图上有、模型无校验")
    
    svg_devices = set(svg_data.keys()) if svg_data else set()
    db_devices = set(dist_topo.device_map.keys())
    
    missing_in_db = svg_devices - db_devices
    
    print(f"\n  SVG设备数: {len(svg_devices)}")
    print(f"  数据库设备数: {len(db_devices)}")
    print(f"  图上有模型无: {len(missing_in_db)} 个")
    
    if missing_in_db:
        print("\n  缺失设备示例（前10个）:")
        for dev_id in list(missing_in_db)[:10]:
            svg_info = svg_data.get(dev_id, {})
            name = svg_info.get('object_name', svg_info.get('element_type_cn', 'N/A'))
            print(f"    - {dev_id}: {name}")
    
    return {"missing_in_db": len(missing_in_db), "list": list(missing_in_db)[:100]}


def test_module2_2_db_vs_svg_no_svg(dist_topo, svg_data, feeder_id):
    """模块2.2: 模型有、图上无校验"""
    print_header("模块2.2: 模型有、图上无校验")
    
    svg_devices = set(svg_data.keys()) if svg_data else set()
    line_db_devices = {k: v for k, v in dist_topo.device_map.items() 
                       if safe_get(v, 'feeder_id') == feeder_id}
    db_line_devices = set(line_db_devices.keys())
    
    missing_in_svg = db_line_devices - svg_devices
    
    print(f"\n  馈线{feeder_id}数据库设备数: {len(db_line_devices)}")
    print(f"  SVG设备数: {len(svg_devices)}")
    print(f"  模型有图上无: {len(missing_in_svg)} 个")
    
    if missing_in_svg:
        print("\n  缺失设备示例（前10个）:")
        for dev_id in list(missing_in_svg)[:10]:
            dev = line_db_devices.get(dev_id)
            print(f"    - {dev_id}: {safe_get(dev, 'equip_name', 'N/A')}")
    
    return {"missing_in_svg": len(missing_in_svg), "list": list(missing_in_svg)[:100]}


def test_module2_3_physical_vs_logical(dist_topo, svg_elements):
    """模块2.3: 图形物理连通、拓扑逻辑断开"""
    print_header("模块2.3: 图形物理连通、拓扑逻辑断开校验")
    
    G = safe_get(dist_topo, 'graph')
    
    # 从SVG连接关系中检测不一致
    physical_connections = []
    for elem in svg_elements[:100]:
        connections = elem.get('connections', [])
        for conn in connections:
            from_id = conn.get('from_element_id') or conn.get('from')
            to_id = conn.get('to_element_id') or conn.get('to')
            if from_id and to_id:
                physical_connections.append((from_id, to_id))
                if G and not G.has_edge(from_id, to_id):
                    print(f"  物理连通但逻辑断开: {from_id} → {to_id}")
    
    print(f"\n  SVG物理连接（抽样）: {len(physical_connections)} 条")
    print(f"  拓扑逻辑连接: {G.number_of_edges() if G else 0} 条")
    print(f"  物理连通但逻辑断开: {len([c for c in physical_connections if G and not G.has_edge(c[0], c[1])])} 处")
    
    return {"physical_connections": len(physical_connections)}


def test_module2_4_logical_vs_physical(dist_topo):
    """模块2.4: 图形物理断开、拓扑逻辑误连通"""
    print_header("模块2.4: 图形物理断开、拓扑逻辑误连通校验")
    
    fake_connections = []
    
    for eid, dev in dist_topo.device_map.items():
        if safe_get(dev, 'switch_status') == '0':  # 分位开关
            points = dist_topo.get_device_all_points(eid) if hasattr(dist_topo, 'get_device_all_points') else []
            if points and len(points) >= 2:
                fake_connections.append({
                    'equip_id': eid,
                    'equip_name': safe_get(dev, 'equip_name', 'N/A'),
                    'status': '分位',
                    'issue': '分位开关仍存在拓扑连接，可能为虚假连通'
                })
    
    print(f"\n  [结果] 检测到 {len(fake_connections)} 个可能虚假连通")
    for fc in fake_connections[:5]:
        print(f"    - {fc['equip_id']}: {fc['equip_name']}")
        print(f"      问题: {fc['issue']}")
    
    return {"fake_count": len(fake_connections)}


def test_module3_electrical_logic(dist_topo, tele_evaluator):
    """模块3: 电气逻辑校验"""
    print_header("模块3: 电气逻辑校验 (E01-E07)")
    
    # 获取拓扑构建时检测到的电气逻辑异常
    electrical_defects = safe_get(dist_topo, 'electrical_defects', [])
    
    # 统计各规则命中数
    rule_stats = {}
    for r in electrical_defects:
        rule = safe_get(r, 'rule_code', 'UNKNOWN')
        rule_stats[rule] = rule_stats.get(rule, 0) + 1
    
    print(f"\n  [结果] E01-E07规则命中统计:")
    for rule, count in sorted(rule_stats.items()):
        print(f"    - {rule}: {count} 处")
    
    print(f"\n  总计电气逻辑异常: {len(electrical_defects)} 条")
    
    # 额外抽样验证
    sample_results = []
    sample_count = 0
    for eid, dev in list(dist_topo.device_map.items())[:100]:
        if sample_count >= 20:
            break
        tele_data = tele_evaluator.telemetry_data.get(str(eid), [])
        if tele_data:
            try:
                result = tele_evaluator.evaluate_electrical_logic(eid)
                if result:
                    sample_results.extend(result)
                sample_count += 1
            except:
                pass
    
    if sample_results:
        sample_stats = {}
        for r in sample_results:
            rule = safe_get(r, 'rule_code', 'UNKNOWN')
            sample_stats[rule] = sample_stats.get(rule, 0) + 1
        print(f"\n  [抽样验证-前20个设备] 规则命中:")
        for rule, count in sorted(sample_stats.items()):
            print(f"    - {rule}: {count} 处")
    
    return {"total": len(electrical_defects), "by_rule": rule_stats}


def test_module4_interface(table_data, dist_topo):
    """模块4: 主配网接口拓扑完整性校验"""
    print_header("模块4: 主配网接口拓扑完整性校验")
    
    zw_substations = table_data.get('zw_substation', pd.DataFrame())
    
    # 获取主配接口校验结果
    abnormal_list = safe_get(dist_topo, 'abnormal_list', [])
    
    # 分类统计
    missing_interface = 0
    wrong_interface = 0
    
    for ab in abnormal_list:
        desc = safe_get(ab, 'description', '')
        if '接口漏拼' in desc or '接口缺失' in desc:
            missing_interface += 1
        elif '接口错拼' in desc or '接口错误' in desc:
            wrong_interface += 1
    
    print(f"\n  主网站点: {len(zw_substations)} 个")
    print(f"  主配接口异常: {len(abnormal_list)} 条")
    print(f"  [接口漏拼接] {missing_interface} 处")
    print(f"  [接口错拼接] {wrong_interface} 处")
    
    # 详细列出
    if missing_interface > 0:
        print("\n  漏拼接示例:")
        count = 0
        for ab in abnormal_list:
            if '接口漏拼' in safe_get(ab, 'description', '') and count < 5:
                print(f"    - {safe_get(ab, 'equip_id')}: {safe_get(ab, 'description')}")
                count += 1
    
    return {"missing": missing_interface, "wrong": wrong_interface, "total": len(abnormal_list)}


def test_module5_score(dist_topo, defects_list, abnormal_list):
    """模块5: 模型修正质量自评分"""
    print_header("模块5: 模型修正质量自评分")
    
    from core.score_engine import ScoreAndConfidenceEngine
    from core.telemetry_evaluator import TelemetryEvaluator
    
    # 创建遥测评估器
    yx_real_df = pd.DataFrame()  # 已在拓扑构建时使用
    tele_evaluator = TelemetryEvaluator()  # 空评估器
    
    score_engine = ScoreAndConfidenceEngine(tele_evaluator)
    
    # 使用实际的缺陷列表
    actual_defects = defects_list if defects_list else []
    
    # 如果没有传入缺陷，从拓扑异常列表获取
    if not actual_defects and abnormal_list:
        actual_defects = [
            {
                'defect_type': safe_get(ab, 'rule_code', 'UNKNOWN'),
                'description': safe_get(ab, 'detail', ''),
                'dimension': safe_get(ab, 'dimension', '拓扑完整性')
            }
            for ab in abnormal_list[:100]
        ]
    
    score_summary = score_engine.evaluate_quality_score(
        defects_report=actual_defects,
        total_equip_count=len(dist_topo.device_map),
        repaired_defect_ids=[]
    )
    
    print(f"\n  [评分结果]")
    print(f"    修正前质量评分: {score_summary.get('score_before', 'N/A')}")
    print(f"    修正后质量评分: {score_summary.get('score_after', 'N/A')}")
    
    dim = score_summary.get('dimension_deduction', {})
    print(f"\n  [各维度扣分]")
    for k, v in dim.items():
        print(f"    - {k}: {v}")
    
    print(f"\n  [缺陷统计]")
    print(f"    总缺陷数: {score_summary.get('defect_count', 0)}")
    
    return score_summary


def test_svg_beautify():
    """SVG美化任务"""
    print_header("任务二5.1: SVG标准化美化排版")
    
    for line_name in ['LINE215', 'LINE216']:
        svg_path = find_svg_file(line_name)
        if svg_path:
            print(f"\n  美化 {line_name}.svg...")
            try:
                beautifier = SvgBeautifier(svg_path)
                beautifier.auto_layout()
                output_path = os.path.join(OUTPUT_SVG, f'{line_name}_beautified.svg')
                beautifier.save(output_path)
                print(f"    输出: {output_path}")
            except Exception as e:
                print(f"    美化失败: {e}")
        else:
            print(f"\n  未找到SVG文件: {line_name}.svg")
    
    return {}


def test_svg_auto_generate(table_data, dist_topo):
    """SVG自动生成任务"""
    print_header("任务二5.3: 自动生成SVG接线图")
    
    g = SvgAutoGenerator()
    results = {}
    
    # 任务1: 单线图生成
    print("\n[任务1] 生成LINE215/LINE216单线图...")
    for feeder in ['LINE215', 'LINE216']:
        path = os.path.join(OUTPUT_SVG, f'{feeder}_single_line.svg')
        try:
            p = g.generate_feeder_single_line_diagram(feeder, path)
            results[f'{feeder}_单线图'] = p
            print(f"  {feeder}: {p.get('nodes', 0)}节点, {p.get('edges', 0)}边")
        except Exception as e:
            print(f"  {feeder} 生成失败: {e}")
            results[f'{feeder}_单线图'] = {'error': str(e)}
    
    # 任务2: 联络关系图
    print("\n[任务2] 生成10kVLINE111联络关系图...")
    path = os.path.join(OUTPUT_SVG, '10kVLINE111_tie.svg')
    try:
        p = g.generate_feeder_tie_diagram('10kVLINE111', path)
        results['LINE111_联络图'] = p
        print(f"  10kVLINE111: {p.get('nodes', 0)}节点, {p.get('edges', 0)}边")
    except Exception as e:
        print(f"  10kVLINE111 生成失败: {e}")
        results['LINE111_联络图'] = {'error': str(e)}
    
    # 任务3: 全站联络总图
    print("\n[任务3] 生成SUB004变电站联络总图...")
    path = os.path.join(OUTPUT_SVG, 'SUB004_station_tie.svg')
    try:
        p = g.generate_station_tie_diagram('SUB004', path)
        results['SUB004_联络总图'] = p
        print(f"  SUB004: {p.get('nodes', 0)}节点, {p.get('edges', 0)}边")
    except Exception as e:
        print(f"  SUB004 生成失败: {e}")
        results['SUB004_联络总图'] = {'error': str(e)}
    
    # 任务4: 电源追溯图
    print("\n[任务4] 生成LINE074配变TMP00034205电源追溯图...")
    path = os.path.join(OUTPUT_SVG, 'TMP00034205_power_trace.svg')
    try:
        p = g.generate_power_trace_diagram('TMP00034205', 'LINE074', path)
        results['TMP00034205_电源追溯'] = p
        print(f"  TMP00034205: {p.get('nodes', 0)}节点, {p.get('edges', 0)}边")
    except Exception as e:
        print(f"  TMP00034205 生成失败: {e}")
        results['TMP00034205_电源追溯'] = {'error': str(e)}
    
    return results


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("   配电网图模质量校验及修正 - 综合测试 v2.0")
    print("=" * 70)
    
    # 加载数据
    table_data = load_data()
    line_df = table_data.get('line', pd.DataFrame())
    
    # 构建拓扑
    print("\n[2] 构建拓扑...")
    builder = TopologyBuilder(table_data)
    main_topo, dist_topo = builder.build_full_topology()
    print(f"  主网设备: {len(main_topo.device_map)} 个")
    print(f"  配网设备: {len(dist_topo.device_map)} 个")
    
    # 获取遥测评估器（从builder中获取）
    tele_evaluator = safe_get(builder, 'telemetry_evaluator')
    if not tele_evaluator:
        yx_real_df = table_data.get('yx_real', pd.DataFrame())
        tele_evaluator = TelemetryEvaluator.from_pwreal(yx_real_df)
    
    # 加载SVG数据（从output目录加载已解析的数据）
    print("\n[3] 加载SVG数据...")
    svg_data = {}
    svg_elements = []
    for line_name in ['LINE215', 'LINE216']:
        devices, elements = load_svg_from_output(line_name)
        if devices:
            svg_data.update(devices)
            svg_elements.extend(elements)
            print(f"  {line_name}: {len(devices)} 图元")
        else:
            print(f"  {line_name}: 未找到解析数据")
    
    # 从拓扑异常列表获取缺陷
    abnormal_list = safe_get(dist_topo, 'abnormal_list', [])
    electrical_defects = safe_get(dist_topo, 'electrical_defects', [])
    
    print(f"\n  拓扑异常列表: {len(abnormal_list)} 条")
    print(f"  电气逻辑异常: {len(electrical_defects)} 条")
    
    # ========== 任务一：模块一 ==========
    print_subheader("任务一：模块一 - 拓扑结构完整性检测")
    
    m1_1 = test_module1_1_hanging_devices(dist_topo)
    m1_2 = test_module1_2_breakpoint_finding(dist_topo)
    m1_3 = test_module1_3_tie_switch(dist_topo, line_df)
    m1_4 = test_module1_4_suspect_tie(dist_topo)
    m1_5 = test_module1_5_unplanned_loop(dist_topo)
    
    # ========== 任务一：模块二 ==========
    print_subheader("任务一：模块二 - 图模一致性校验")
    
    feeder_id = 'TMP00000188'  # LINE215对应
    m2_1 = test_module2_1_svg_vs_db_no_model(dist_topo, svg_data)
    m2_2 = test_module2_2_db_vs_svg_no_svg(dist_topo, svg_data, feeder_id)
    m2_3 = test_module2_3_physical_vs_logical(dist_topo, svg_elements)
    m2_4 = test_module2_4_logical_vs_physical(dist_topo)
    
    # ========== 任务一：模块三 ==========
    print_subheader("任务一：模块三 - 电气逻辑校验")
    
    m3 = test_module3_electrical_logic(dist_topo, tele_evaluator)
    
    # ========== 任务一：模块四 ==========
    print_subheader("任务一：模块四 - 主配网接口校验")
    
    m4 = test_module4_interface(table_data, dist_topo)
    
    # ========== 任务一：模块五 ==========
    print_subheader("任务一：模块五 - 模型修正质量评分")
    
    # 合并所有缺陷
    all_defects = []
    all_defects.extend([
        {'defect_type': '拓扑异常', 'description': safe_get(a, 'detail', ''), 'dimension': safe_get(a, 'dimension', '拓扑完整性')}
        for a in abnormal_list
    ])
    all_defects.extend([
        {'defect_type': safe_get(e, 'rule_code', '电气异常'), 'description': safe_get(e, 'detail', ''), 'dimension': '电气逻辑'}
        for e in electrical_defects
    ])
    
    m5 = test_module5_score(dist_topo, all_defects, abnormal_list)
    
    # ========== 任务二：SVG美化 ==========
    print_subheader("任务二 - SVG拓扑图形美化专项")
    
    t_svg_beautify = test_svg_beautify()
    t_svg_auto = test_svg_auto_generate(table_data, dist_topo)
    
    # ========== 汇总 ==========
    print("\n" + "=" * 70)
    print("  测试汇总")
    print("=" * 70)
    
    summary = {
        "模块1.1_悬空检测": {"count": m1_1.get('hanging_count', 0)},
        "模块1.2_断点定位": {"breakpoint_count": m1_2.get('breakpoint_count', 0)},
        "模块1.3_联络开关": {"count": m1_3.get('tie_switch_count', 0)},
        "模块1.4_疑似联络": {"count": m1_4.get('suspect_count', 0)},
        "模块1.5_合环检测": {"count": m1_5.get('loop_count', 0)},
        "模块2.1_图有模无": {"count": m2_1.get('missing_in_db', 0)},
        "模块2.2_模有图无": {"count": m2_2.get('missing_in_svg', 0)},
        "模块2.3_物通逻断": m2_3,
        "模块2.4_逻通物断": {"count": m2_4.get('fake_count', 0)},
        "模块3_电气逻辑": {"total": m3.get('total', 0)},
        "模块4_主配接口": {"missing": m4.get('missing', 0), "wrong": m4.get('wrong', 0)},
        "模块5_质量评分": {
            "score_before": m5.get('score_before'),
            "score_after": m5.get('score_after'),
        }
    }
    
    output_path = os.path.join(OUTPUT_JSON, "test_summary_v2.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n  测试汇总已保存: {output_path}")
    print("\n✅ 全部测试任务完成!")
    
    return summary


if __name__ == "__main__":
    main()
