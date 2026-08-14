import xml.etree.ElementTree as ET
from collections import Counter

ns = {'svg': 'http://www.w3.org/2000/svg'}
path = r'C:\Users\1\Desktop\power_topology_verify\output\svg\LINE215_beautified.svg'
tree = ET.parse(path)
root = tree.getroot()

layer = root.find('.//svg:g[@id="Connection_Layer"]', ns)
if layer is None:
    layer = root

zero_count = 0
poly_count = 0
endpoint_pairs = []
for elem in layer.findall('.//svg:polyline', ns) + layer.findall('.//svg:path', ns):
    pts_str = elem.get('points', '')
    if not pts_str:
        d = elem.get('d', '')
        continue
    pts = [tuple(map(float, p.split(','))) for p in pts_str.strip().split()]
    poly_count += 1
    if len(pts) >= 2:
        p0, p1 = pts[0], pts[-1]
        if (abs(p0[0]) < 0.001 and abs(p0[1]) < 0.001) or (abs(p1[0]) < 0.001 and abs(p1[1]) < 0.001):
            zero_count += 1
            endpoint_pairs.append((p0, p1))

print(f'总 polyline: {poly_count}, 含 (0,0) 端点: {zero_count}')
print('前 10 条含 (0,0) 的线:')
for p0, p1 in endpoint_pairs[:10]:
    print(f'  {p0} -> {p1}')

# 设备坐标范围（排除 symbol 定义里的 terminal use）
xs, ys = [], []
for use in root.findall('.//svg:use', ns):
    href = use.get('{http://www.w3.org/1999/xlink}href', '')
    if href == '#terminal':
        continue
    x = float(use.get('x', 0))
    y = float(use.get('y', 0))
    xs.append(x)
    ys.append(y)
print(f'\n设备 use 坐标范围: x [{min(xs):.1f}, {max(xs):.1f}], y [{min(ys):.1f}, {max(ys):.1f}]')

center_devices = [(x, y) for x, y in zip(xs, ys) if abs(x) < 50 and abs(y) < 50]
print(f'(0,0) 附近 50px 内设备数: {len(center_devices)}')
if center_devices:
    print(f'  前 10 个: {center_devices[:10]}')

# 原始 SVG
orig_path = r'C:\Users\1\Desktop\power_topology_verify\数据集更新版20260729\配网 svg\LINE215.svg'
orig_tree = ET.parse(orig_path)
orig_root = orig_tree.getroot()
orig_zero = 0
for elem in orig_root.findall('.//svg:polyline', ns) + orig_root.findall('.//svg:path', ns):
    pts_str = elem.get('points', '')
    if pts_str:
        pts = [tuple(map(float, p.split(','))) for p in pts_str.strip().split()]
        if len(pts) >= 2:
            if (abs(pts[0][0]) < 0.001 and abs(pts[0][1]) < 0.001) or (abs(pts[-1][0]) < 0.001 and abs(pts[-1][1]) < 0.001):
                orig_zero += 1
print(f'\n原始 SVG 含 (0,0) 端点连接: {orig_zero}')
