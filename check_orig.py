import sys
sys.path.insert(0, '.')
from data_io.svg_reader import SvgDocument

doc = SvgDocument(r'数据集更新版20260729\配网 svg\LINE215.svg')
doc.parse()

texts = [t for t in doc.texts]
print(f'原始文字数: {len(texts)}')
xs = [t.x for t in texts]
ys = [t.y for t in texts]
print(f'文字X: [{min(xs):.1f}, {max(xs):.1f}]')
print(f'文字Y: [{min(ys):.1f}, {max(ys):.1f}]')

# 近似重叠检测
overlaps = 0
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        if abs(texts[i].x - texts[j].x) < 5 and abs(texts[i].y - texts[j].y) < 5:
            overlaps += 1
            break

print(f'原始文字近似重叠: {overlaps} 个文字有重叠 ({overlaps*100//len(texts)}%)')
print(f'原始fontSize样例: {[t.font_size for t in texts[:5]]}')
print(f'原始fill样例: {[t.fill for t in texts[:5]]}')
