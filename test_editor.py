import os
import sys

# Ensure project root is in path
PROJECT_ROOT = os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from svg_io.svg_editor import SvgInteractiveEditorV2
from svg_io.svg_beautifier import SvgBeautifier
import os

PROJECT_ROOT = os.getcwd()

def test_editor():
    print("="*60)
    print("任务 5.2: 交互式增删设备 (v2 引擎集成版)")
    print("="*60)
    
    input_dir = os.path.join(PROJECT_ROOT, "数据集更新版20260729", "配网 svg")
    output_dir = os.path.join(PROJECT_ROOT, "output", "svg")
    os.makedirs(output_dir, exist_ok=True)
    
    # ---------------------------------------------------------
    # 测试任务 1: LINE215 新增站房
    # ---------------------------------------------------------
    print("\n>>> 执行任务 5.2.1: LINE215 新增站房 000300")
    l215_path = os.path.join(input_dir, "LINE215.svg")
    l215_out = os.path.join(output_dir, "LINE215_add_station_000300.svg")
    
    b215 = SvgBeautifier(l215_path, output_path=l215_out)
    b215._prepare_internal_data() # 加载数据
    b215.repair()                 # 先执行修复
    
    # 初始化交互式编辑器并执行插入
    editor215 = SvgInteractiveEditorV2(b215)
    editor215.add_station(
        station_id="000300", 
        station_name="站房000300",
        upstream_query="开关00104", 
        downstream_query="开关00102", 
        internal_switch_ids=["00301", "00302", "00303"]
    )
    
    # 重新布局并渲染保存
    b215.layout()
    b215.render(l215_out)


    # ---------------------------------------------------------
    # 测试任务 2: LINE216 删除开关 00024
    # ---------------------------------------------------------
    print("\n>>> 执行任务 5.2.2: LINE216 删除开关 00024")
    l216_path = os.path.join(input_dir, "LINE216.svg")
    l216_out = os.path.join(output_dir, "LINE216_del_switch_00024.svg")
    
    b216 = SvgBeautifier(l216_path, output_path=l216_out)
    b216._prepare_internal_data()
    b216.repair()
    
    editor216 = SvgInteractiveEditorV2(b216)
    editor216.delete_device("开关00024")
    
    b216.layout()
    b216.render(l216_out)
    
    print("\n" + "="*60)
    print("交互编辑任务执行完毕。成果已保存至 output/svg 目录。")
    print("="*60)

if __name__ == "__main__":
    test_editor()