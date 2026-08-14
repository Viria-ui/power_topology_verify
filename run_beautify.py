import sys
import os
sys.path.insert(0, '.')
from svg_io.svg_beautifier import SvgBeautifier

output_dir = os.path.join('output', 'svg')
os.makedirs(output_dir, exist_ok=True)

# 处理LINE215
svg_path = r'数据集更新版20260729\配网 svg\LINE215.svg'
output_path = os.path.join(output_dir, 'LINE215_beautified.svg')
beautifier = SvgBeautifier(svg_path, output_path)
result = beautifier.beautify()
print(f'LINE215 美化完成: {result}')

# 处理LINE216
svg_path2 = r'数据集更新版20260729\配网 svg\LINE216.svg'
output_path2 = os.path.join(output_dir, 'LINE216_beautified.svg')
beautifier2 = SvgBeautifier(svg_path2, output_path2)
result2 = beautifier2.beautify()
print(f'LINE216 美化完成: {result2}')