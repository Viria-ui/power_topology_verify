import sys
sys.path.insert(0, '.')
from svg_io.svg_beautifier import SvgBeautifier

# 处理LINE215
svg_path = r'数据集更新版20260729\配网 svg\LINE215.svg'
beautifier = SvgBeautifier(svg_path)
result = beautifier.beautify()
print(f'LINE215 美化完成: {result}')

# 处理LINE216
svg_path2 = r'数据集更新版20260729\配网 svg\LINE216.svg'
beautifier2 = SvgBeautifier(svg_path2)
result2 = beautifier2.beautify()
print(f'LINE216 美化完成: {result2}')