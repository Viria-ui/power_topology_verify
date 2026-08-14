import sys
sys.path.insert(0, '.')
from data_io.svg_reader import SvgDocument

doc = SvgDocument(r'数据集更新版20260729\配网 svg\LINE215_beautified.svg')
doc.parse()

texts = [t for t in doc.texts if not getattr(t, 'hidden', False)]
print(f'美化后可见文字数: {len(texts)}')
print(f'fontSize样例: {[t.font_size for t in texts[:5]]}')
print(f'fill样例: {[t.fill for t in texts[:5]]}')
print(f'fontWeight样例: {[t.font_weight for t in texts[:5]]}')

# 对比原始
doc2 = SvgDocument(r'数据集更新版20260729\配网 svg\LINE215.svg')
doc2.parse()
texts2 = [t for t in doc2.texts]
print(f'\n原始文字数: {len(texts2)}')
print(f'原始fontSize样例: {[t.font_size for t in texts2[:5]]}')
print(f'原始fill样例: {[t.fill for t in texts2[:5]]}')

# 检查设备坐标是否一致
e1 = {e.element_id: e for e in doc.elements if e.element_id}
e2 = {e.element_id: e for e in doc2.elements if e.element_id}
shared = set(e1.keys()) & set(e2.keys())
diff_count = 0
for did in shared:
    if abs(e1[did].x - e2[did].x) > 0.1 or abs(e1[did].y - e2[did].y) > 0.1:
        diff_count += 1
        if diff_count <= 3:
            print(f'\n坐标不一致: {did}')
            print(f'  原始: ({e2[did].x:.3f}, {e2[did].y:.3f})')
            print(f'  美化: ({e1[did].x:.3f}, {e1[did].y:.3f})')

print(f'\n设备坐标不一致数量: {diff_count}/{len(shared)}')

# 检查连接线坐标是否一致
c1 = {c.connection_id: c for c in doc.connections if c.connection_id}
c2 = {c.connection_id: c for c in doc2.connections if c.connection_id}
shared_c = set(c1.keys()) & set(c2.keys())
conn_diff = 0
for cid in shared_c:
    p1 = c1[cid].points[:2] if c1[cid].points else []
    p2 = c2[cid].points[:2] if c2[cid].points else []
    if len(p1) == len(p2) and len(p1) > 0:
        if abs(p1[0][0] - p2[0][0]) > 0.1 or abs(p1[0][1] - p2[0][1]) > 0.1:
            conn_diff += 1
            if conn_diff <= 3:
                print(f'\n连接线不一致: {cid}')
                print(f'  原始: {p2}')
                print(f'  美化: {p1}')

print(f'\n连接线坐标不一致数量: {conn_diff}/{len(shared_c)}')
