import os
import json
import sys
import time

# Ensure project root is in path
PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data_io.svg_reader import SvgDocument
from data_io.svg_writer import SvgDocumentWriter
from core.topology_validator import (
    validate_svg_only, validate_svg_vs_topology, 
    validate_rendered_svg, export_defect_report
)
from core.topology_repairer import TopologyRepairer
from svg_io.svg_beautifier import SvgBeautifier
from svg_io.svg_editor import SvgInteractiveEditor
from scripts._load_sql_topology import load_sql_topology

def run_beautify_only_pipeline():
    # 1. Initialize paths
    input_dir = os.path.join(PROJECT_ROOT, "数据集更新版20260729", "配网 svg")
    output_dir = os.path.join(PROJECT_ROOT, "output", "svg")
    report_dir = os.path.join(PROJECT_ROOT, "output", "reports")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    # 注意：任务 5.1 明确要求“不读取数据库拓扑信息，仅依托 SVG 文件自身连接关系”
    print("\n[Step 0] 启动美化专项流水线 (不依赖数据库)...")
    
    target_files = ["LINE215.svg", "LINE216.svg"]
    
    for filename in target_files:
        print(f"\n" + "="*60)
        print(f"正在执行 5.1 美化任务: {filename}")
        print("="*60)
        
        input_path = os.path.join(input_dir, filename)
        if not os.path.exists(input_path):
            print(f"文件不存在: {input_path}")
            continue
            
        # ---- Step 1: 解析原始 SVG ----
        print("\n[Step 1] 解析原始 SVG (提取图元、文本、坐标、连线)...")
        doc = SvgDocument(input_path)
        if not doc.parse():
            print(f"解析失败: {filename}")
            continue
        
        # 导出原始 IR
        ir_initial_path = os.path.join(report_dir, f"{filename}_ir_initial.json")
        doc.dump_ir(ir_initial_path)
            
        # ---- Step 2: 初始质量校验 (仅针对 SVG 规范) ----
        print("\n[Step 2] 正在执行初始质量校验 (23项配网制图规范)...")
        defects_svg, summary_svg = validate_svg_only(doc, stage="initial")
        report_initial_path = os.path.join(report_dir, f"{filename}_validation_initial.json")
        export_defect_report(defects_svg, summary_svg, report_initial_path)
        print(f"  初始发现缺陷: {len(defects_svg)} 条")

        # ---- Step 3: 执行拓扑自动修复 (仅基于 SVG 几何与 glink) ----
        print("\n[Step 3] 执行拓扑缺陷整治 (修复飞线、缝合孤岛)...")
        pre_counts = {"elements": len(doc.elements), "connections": len(doc.connections)}
        
        repairer = TopologyRepairer(doc)
        doc = repairer.repair() # 该模块已重构，仅使用 doc 内部数据
        
        post_counts = {"elements": len(doc.elements), "connections": len(doc.connections)}
        # 导出修复后 IR
        ir_repaired_path = os.path.join(report_dir, f"{filename}_ir_repaired.json")
        doc.dump_ir(ir_repaired_path)
        
        q = getattr(doc, "topology_stats", {})
        print(f"  修复成果: 新增物理连接 {post_counts['connections'] - pre_counts['connections']} 条")
        print(f"  拓扑状态: 连通分量={q.get('connected_components')}, 孤立节点={q.get('isolated_nodes_count')}")

        # ---- Step 4: 执行标准化美化排版 (Task 5.1 核心) ----
        print("\n[Step 4] 执行标准化美化排版 (布局重构、站房规范、L-Shape 路由)...")
        beautified_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_beautified.svg")
        beautifier = SvgBeautifier(input_path, output_path=beautified_path)
        beautifier.doc = doc # 传入修复后的 IR
        beautifier.beautify()
        
        # 核心修复：美化后再次导出最终 IR，展示重排后的坐标、正交化路径和归一化角度
        ir_final_path = os.path.join(report_dir, f"{filename}_ir_final.json")
        doc.dump_ir(ir_final_path)
        print(f"  最终美化版 IR 已导出: {ir_final_path}")
        
        # ---- Step 5: 美化后质量终审 ----
        print("\n[Step 5] 执行美化后质量终审...")
        defects_post, summary_post = validate_rendered_svg(beautified_path)
        report_beautified_path = os.path.join(report_dir, f"{filename}_validation_beautified.json")
        export_defect_report(defects_post, summary_post, report_beautified_path)
        print(f"  最终残余缺陷: {len(defects_post)} 条 (主要为建议性标注)")

    print("\n" + "="*60)
    print("5.1 美化专项测试任务执行完毕，请查看 output 目录下的 _beautified.svg 文件。")
    print("="*60)

if __name__ == "__main__":
    print("="*60)
    print("SVG 拓扑图形美化流水线 (Task 5.1 专项版)")
    print("="*60)
    try:
        run_beautify_only_pipeline()
    except Exception as e:
        print(f"\n执行失败: {e}")
        import traceback
        traceback.print_exc()
