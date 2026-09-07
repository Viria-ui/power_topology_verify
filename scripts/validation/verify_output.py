"""验证美化输出 SVG 是否符合规范（精确版）

只统计 ConnLine_Layer 中的连接线和实际图层中的文字/设备，
避免被 <defs> 中的 symbol 内部图形干扰。
"""
import re
import os
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"


def local_tag(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def analyze_svg(fname):
    path = os.path.join('output', 'svg', fname)
    if not os.path.exists(path):
        print(f'文件不存在: {path}')
        return

    tree = ET.parse(path)
    root = tree.getroot()

    print(f'\n========== {fname} ==========')

    # 1. 根属性
    vb = root.get('viewBox', '')
    width = root.get('width', '')
    height = root.get('height', '')
    coord_extent = root.get('coordinateExtent', '')
    print(f'viewBox: {vb}')
    print(f'width/height: {width} / {height}')
    print(f'coordinateExtent: {coord_extent}')
    if vb:
        parts = [float(x) for x in vb.split()]
        if len(parts) == 4 and parts[3]:
            print(f'  跨度: {parts[2]:.1f} x {parts[3]:.1f} (宽高比 {parts[2]/parts[3]:.2f}:1)')

    # 2. 找各图层
    conn_layer = None
    text_layer = None
    for g in root.iter(f'{{{SVG_NS}}}g'):
        if g.get('id') == 'ConnLine_Layer':
            conn_layer = g
        elif g.get('id') == 'Text_Layer':
            text_layer = g

    # 3. 连接线分析（仅 ConnLine_Layer）
    if conn_layer is not None:
        polylines = []
        for poly in conn_layer.iter(f'{{{SVG_NS}}}polyline'):
            polylines.append(poly)

        # stroke-width 统计
        widths = {}
        strokes = {}
        zero_start = 0
        for poly in polylines:
            sw = poly.get('stroke-width', '')
            widths[sw] = widths.get(sw, 0) + 1
            stroke = poly.get('stroke', '')
            strokes[stroke] = strokes.get(stroke, 0) + 1
            pts = poly.get('points', '')
            if pts.startswith('0.0000,0.0000') or pts.startswith('0,0 '):
                zero_start += 1

        print(f'\n--- 连接线（ConnLine_Layer）---')
        print(f'连接线总数: {len(polylines)}')
        print(f'(0,0) 起点连接线: {zero_start}')
        print(f'stroke 集合: {strokes}')
        print(f'stroke-width 集合: {dict(sorted(widths.items(), key=lambda x: -x[1]))}')

    # 4. 文字分析（仅 Text_Layer）
    if text_layer is not None:
        texts = list(text_layer.iter(f'{{{SVG_NS}}}text'))
        sizes = {}
        missing_anchor = 0
        missing_baseline = 0
        for t in texts:
            fs = t.get('font-size', '')
            sizes[fs] = sizes.get(fs, 0) + 1
            if not t.get('text-anchor'):
                missing_anchor += 1
            if not t.get('dominant-baseline'):
                missing_baseline += 1

        print(f'\n--- 文字（Text_Layer）---')
        print(f'文字总数: {len(texts)}')
        print(f'字号集合: {sizes}')
        print(f'缺 text-anchor: {missing_anchor}, 缺 dominant-baseline: {missing_baseline}')

    # 5. 背景检查
    bg_layer = None
    for g in root.iter(f'{{{SVG_NS}}}g'):
        if g.get('id') == 'BackGround_Layer':
            bg_layer = g
            break
    if bg_layer is not None:
        for child in bg_layer:
            tag = local_tag(child.tag)
            if tag in ('rect', 'polygon'):
                fill = child.get('fill', '')
                print(f'\n--- 背景 ---')
                print(f'背景元素: <{tag}> fill={fill}')


if __name__ == '__main__':
    for fname in ['LINE215_beautified.svg', 'LINE216_beautified.svg']:
        analyze_svg(fname)
