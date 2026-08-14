import sys
import os
import re
import json
import math
import pandas as pd
from xml.etree import ElementTree as ET

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config.settings import OUTPUT_JSON, OUTPUT_CSV

NS_MAP = {
    'ns0': 'http://www.w3.org/2000/svg',
    'ns1': 'http://www.w3.org/1999/xlink',
    'ns2': 'http://iec.ch/TC57/2005/SVG-schema#'
}

LAYER_TYPE_MAP = {
    'PowerTransformer_Layer': 'PowerTransformer',
    'Breaker_Layer': 'Breaker',
    'Disconnector_Layer': 'Disconnector',
    'LoadBreakSwitch_Layer': 'LoadBreakSwitch',
    'CompositeSwitch_Layer': 'CompositeSwitch',
    'Fuse_Layer': 'Fuse',
    'Junction_Layer': 'Junction',
    'PoleCode_Layer': 'PoleCode',
    'EnergyConsumer_Layer': 'EnergyConsumer',
    'PotentialTransformer_Layer': 'PotentialTransformer',
    'CurrentTransformer_Layer': 'CurrentTransformer',
    'GroundDisconnector_Layer': 'GroundDisconnector',
    'RemoteUnit_Layer': 'RemoteUnit',
    'BusbarSection_Layer': 'BusbarSection',
    'Substation_Layer': 'Substation',
    'ACLineSegment_Layer': 'ACLineSegment',
    'ConnLine_Layer': 'ConnLine',
    'Other_Layer': 'Other',
}

TYPE_NAME_MAP = {
    'Breaker': '断路器',
    'PowerTransformer': '变压器',
    'Disconnector': '隔离开关',
    'LoadBreakSwitch': '负荷开关',
    'CompositeSwitch': '组合开关',
    'Fuse': '熔断器',
    'Junction': '连接点',
    'PoleCode': '杆塔',
    'EnergyConsumer': '负荷',
    'PotentialTransformer': '电压互感器',
    'CurrentTransformer': '电流互感器',
    'GroundDisconnector': '接地刀闸',
    'RemoteUnit': '终端设备',
    'BusbarSection': '母线',
    'Substation': '站房',
    'ACLineSegment': '交流线段',
    'ConnLine': '连接线',
    'Other': '其他'
}


def parse_transform(transform_str, x, y):
    if not transform_str:
        return x, y
    
    current_x, current_y = float(x), float(y)
    
    transforms = re.findall(r'(translate|rotate|scale|matrix)\(([^)]+)\)', transform_str)
    
    for transform_type, params_str in reversed(transforms):
        params = [float(p.strip()) for p in params_str.split(',')]
        
        if transform_type == 'translate':
            current_x += params[0]
            current_y += params[1] if len(params) > 1 else 0
        elif transform_type == 'scale':
            sx = params[0]
            sy = params[1] if len(params) > 1 else params[0]
            current_x *= sx
            current_y *= sy
        elif transform_type == 'rotate':
            angle = math.radians(params[0])
            cx = params[1] if len(params) > 1 else 0
            cy = params[2] if len(params) > 2 else 0
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            dx = current_x - cx
            dy = current_y - cy
            current_x = cx + dx * cos_a - dy * sin_a
            current_y = cy + dx * sin_a + dy * cos_a
        elif transform_type == 'matrix':
            a, b, c, d, e, f = params
            new_x = a * current_x + c * current_y + e
            new_y = b * current_x + d * current_y + f
            current_x, current_y = new_x, new_y
    
    return current_x, current_y


def parse_transform_forward(transform_str, x, y):
    if not transform_str:
        return x, y, 1.0, 0.0, 0.0, 1.0
    
    tx, ty, sx, sy, angle = 0.0, 0.0, 1.0, 1.0, 0.0
    cx, cy = 0.0, 0.0
    has_center = False
    
    transforms = re.findall(r'(translate|rotate|scale)\(([^)]+)\)', transform_str)
    
    for transform_type, params_str in transforms:
        params = [float(p.strip()) for p in params_str.split(',')]
        
        if transform_type == 'translate':
            tx += params[0]
            ty += params[1] if len(params) > 1 else 0
        elif transform_type == 'scale':
            sx *= params[0]
            sy *= params[1] if len(params) > 1 else params[0]
        elif transform_type == 'rotate':
            angle += params[0]
            if len(params) > 1:
                cx = params[1]
                cy = params[2] if len(params) > 2 else 0
                has_center = True
    
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    abs_x = float(x) + tx
    abs_y = float(y) + ty
    
    if has_center:
        dx = abs_x - cx
        dy = abs_y - cy
        final_x = cx + (dx * cos_a - dy * sin_a) * sx
        final_y = cy + (dx * sin_a + dy * cos_a) * sy
    else:
        final_x = abs_x * sx
        final_y = abs_y * sy
    
    return final_x, final_y


class SvgTerminal:
    def __init__(self, index, x, y):
        self.index = int(index)
        self.x = float(x)
        self.y = float(y)
        self.point_id = None

    def to_dict(self):
        return {
            'terminal_index': self.index,
            'x': round(self.x, 4),
            'y': round(self.y, 4),
            'point_id': self.point_id
        }


class SvgText:
    def __init__(self, text_id, x, y, content='', font_size=0, color=''):
        self.text_id = text_id
        self.x = float(x)
        self.y = float(y)
        self.content = content
        self.font_size = font_size
        self.color = color
        self.object_id = None
        self.object_name = None
        self.psr_type = None
        self.related_element_id = None

    def to_dict(self):
        return {
            'text_id': self.text_id,
            'x': round(self.x, 4),
            'y': round(self.y, 4),
            'content': self.content,
            'font_size': round(self.font_size, 4),
            'color': self.color,
            'object_id': self.object_id,
            'related_element_id': self.related_element_id
        }


class SvgElement:
    def __init__(self, element_id, element_type, x, y, width=0, height=0):
        self.element_id = element_id
        self.element_type = element_type
        self.x = float(x)
        self.y = float(y)
        self.width = float(width) if width else 0
        self.height = float(height) if height else 0
        self.object_id = None
        self.object_name = None
        self.psr_type = None
        self.terminals = []
        self.layer = None
        self.layer_id = None
        self.symbol_id = None
        self.voltage_level = None
        self.css_class = None
        self.stroke_color = None
        self.fill_color = None
        self.stroke_width = None
        self.related_text_ids = []
        self.is_junction = False

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_related_text(self, text_id):
        if text_id not in self.related_text_ids:
            self.related_text_ids.append(text_id)

    def to_dict(self):
        return {
            'element_id': self.element_id,
            'element_type': self.element_type,
            'element_type_cn': TYPE_NAME_MAP.get(self.element_type, self.element_type),
            'x': round(self.x, 4),
            'y': round(self.y, 4),
            'width': round(self.width, 4),
            'height': round(self.height, 4),
            'object_id': self.object_id,
            'object_name': self.object_name,
            'psr_type': self.psr_type,
            'layer': self.layer,
            'voltage_level': self.voltage_level,
            'css_class': self.css_class,
            'stroke_color': self.stroke_color,
            'is_junction': self.is_junction,
            'related_text_ids': self.related_text_ids,
            'terminals': [t.to_dict() for t in self.terminals]
        }


LINE_TYPE_MAP = {
    '#00A854': 'main_line',
    '#FF6A00': 'tie_line',
    '#722ED1': 'inter_station_line',
    '#BFBFBF': 'spare_line',
    '#1890FF': 'trace_path',
}

LINE_TYPE_NAME_MAP = {
    'main_line': '主干线',
    'tie_line': '联络线',
    'inter_station_line': '站间连线',
    'spare_line': '备用线',
    'trace_path': '追踪路径',
    'branch_line': '支线',
    'container_border': '容器边界',
    'Trunk': '主干',
    'Branch': '分支',
    'Tie': '联络'
}


class SvgLine:
    def __init__(self, line_id, points_str, line_type=None):
        self.line_id = line_id
        self.points = self._parse_points(points_str)
        self.line_type = line_type
        self.line_type_cn = LINE_TYPE_NAME_MAP.get(line_type, line_type) if line_type and line_type not in ('Trunk', 'Branch', 'Tie') else None
        self.start_point = None
        self.end_point = None
        self.object_id = None
        self.glink_refs = []
        self.voltage_level = None
        self.color = None
        self.stroke_width = None
        self.css_class = None
        self.inferred_type = None
        self.inferred_type_cn = None

    def _parse_points(self, points_str):
        coords = []
        point_values = re.split(r'[ ,]+', points_str.strip())
        point_values = [v for v in point_values if v]
        for i in range(0, len(point_values), 2):
            if i + 1 < len(point_values):
                coords.append((float(point_values[i]), float(point_values[i+1])))
        return coords

    def infer_line_type(self):
        inferred = None
        if self.color:
            color_upper = self.color.upper()
            if color_upper in LINE_TYPE_MAP:
                inferred = LINE_TYPE_MAP[color_upper]
        if not inferred and self.stroke_width:
            try:
                width = float(self.stroke_width)
                if width >= 4.0:
                    inferred = 'tie_line'
                elif width >= 2.5:
                    inferred = 'main_line'
                elif width <= 1.2:
                    inferred = 'spare_line'
                else:
                    inferred = 'branch_line'
            except ValueError:
                pass
        self.inferred_type = inferred
        self.inferred_type_cn = LINE_TYPE_NAME_MAP.get(inferred, inferred) if inferred else None
        if not self.line_type and inferred:
            self.line_type = inferred
            self.line_type_cn = self.inferred_type_cn
        return inferred

    def to_dict(self):
        return {
            'line_id': self.line_id,
            'points': [(round(p[0], 4), round(p[1], 4)) for p in self.points],
            'line_type': self.line_type,
            'line_type_cn': self.line_type_cn,
            'inferred_type': self.inferred_type,
            'inferred_type_cn': self.inferred_type_cn,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'object_id': self.object_id,
            'glink_refs': self.glink_refs,
            'color': self.color,
            'stroke_width': self.stroke_width,
            'voltage_level': self.voltage_level
        }


class SvgConnection:
    def __init__(self, from_element_id, from_terminal, to_element_id, to_terminal, line_id=None):
        self.from_element_id = from_element_id
        self.from_terminal = from_terminal
        self.to_element_id = to_element_id
        self.to_terminal = to_terminal
        self.line_id = line_id

    def to_dict(self):
        return {
            'from_element_id': self.from_element_id,
            'from_terminal': self.from_terminal,
            'to_element_id': self.to_element_id,
            'to_terminal': self.to_terminal,
            'line_id': self.line_id
        }


class SvgDocument:
    def __init__(self):
        self.elements = {}
        self.lines = {}
        self.texts = {}
        self.connections = []
        self.symbol_defs = {}
        self.filename = ''

    def add_element(self, element):
        self.elements[element.element_id] = element

    def add_line(self, line):
        self.lines[line.line_id] = line

    def add_text(self, text):
        self.texts[text.text_id] = text

    def add_connection(self, connection):
        self.connections.append(connection)

    def load_symbol_defs(self, root):
        for symbol in root.findall('.//ns0:symbol', NS_MAP):
            symbol_id = symbol.get('id', '')
            terminals = []
            for use in symbol.findall('.//ns0:use', NS_MAP):
                term_index = use.get('terminal-index')
                x = use.get('x', '0')
                y = use.get('y', '0')
                if term_index:
                    terminals.append(SvgTerminal(term_index, x, y))
            self.symbol_defs[symbol_id] = terminals

    def parse_elements(self, root):
        for layer_id, elem_type in LAYER_TYPE_MAP.items():
            if elem_type in ('ConnLine', 'Other'):
                continue
            
            layer = root.find(f'.//ns0:g[@id="{layer_id}"]', NS_MAP)
            if layer is None:
                continue
            
            for group in layer.findall('.//ns0:g', NS_MAP):
                group_id = group.get('id', '')
                
                use_elem = group.find('.//ns0:use', NS_MAP)
                if use_elem is not None:
                    href = use_elem.get('{http://www.w3.org/1999/xlink}href', '')
                    if href.startswith('#'):
                        symbol_id = href[1:]
                    else:
                        symbol_id = href
                    
                    x = use_elem.get('x', '0')
                    y = use_elem.get('y', '0')
                    width = use_elem.get('width', '0')
                    height = use_elem.get('height', '0')
                    transform = use_elem.get('transform', '')
                    css_class = use_elem.get('class', '')
                    
                    abs_x, abs_y = parse_transform_forward(transform, x, y)
                    
                    element = SvgElement(group_id, elem_type, abs_x, abs_y, width, height)
                    element.layer = layer_id
                    element.layer_id = layer_id
                    element.symbol_id = symbol_id
                    element.voltage_level = self._class_to_voltage(css_class)
                    element.css_class = css_class
                    element.is_junction = elem_type == 'Junction'
                    
                    polyline_elem = group.find('.//ns0:polyline', NS_MAP)
                    if polyline_elem is not None:
                        element.stroke_color = polyline_elem.get('stroke', '')
                        element.stroke_width = polyline_elem.get('stroke-width', '')
                    
                    if symbol_id in self.symbol_defs:
                        for term in self.symbol_defs[symbol_id]:
                            term_x, term_y = parse_transform_forward(transform, 
                                float(x) + term.x, float(y) + term.y)
                            element.add_terminal(SvgTerminal(term.index, term_x, term_y))
                    
                    self._parse_metadata(group, element)
                    self.add_element(element)
                
                polygon_elem = group.find('.//ns0:polygon', NS_MAP)
                if polygon_elem is not None and elem_type == 'Substation':
                    points_str = polygon_elem.get('points', '')
                    points = self._parse_points_str(points_str)
                    if points:
                        min_x = min(p[0] for p in points)
                        min_y = min(p[1] for p in points)
                        max_x = max(p[0] for p in points)
                        max_y = max(p[1] for p in points)
                        element = SvgElement(
                            group_id, elem_type,
                            (min_x + max_x) / 2, (min_y + max_y) / 2,
                            max_x - min_x, max_y - min_y
                        )
                        element.layer = layer_id
                        element.layer_id = layer_id
                        element.stroke_color = polygon_elem.get('stroke', '')
                        self._parse_metadata(group, element)
                        self.add_element(element)

    def parse_texts(self, root):
        text_layer = root.find('.//ns0:g[@id="Text_Layer"]', NS_MAP)
        if text_layer is None:
            return
        
        for group in text_layer.findall('.//ns0:g', NS_MAP):
            group_id = group.get('id', '')
            
            text_elems = group.findall('.//ns0:text', NS_MAP)
            if not text_elems:
                continue
            
            for text_elem in text_elems:
                x = text_elem.get('x', '0')
                y = text_elem.get('y', '0')
                content = text_elem.text or ''
                font_size = text_elem.get('font-size', '0')
                color = text_elem.get('fill', '')
                
                if not content.strip():
                    continue
                
                text = SvgText(group_id, x, y, content.strip(), float(font_size), color)
                
                self._parse_text_metadata(group, text)
                self.add_text(text)
        
        self._associate_texts_with_elements()

    def _parse_text_metadata(self, group, text):
        metadata = group.find('.//ns0:metadata', NS_MAP)
        if metadata is not None:
            psr_ref = metadata.find('.//ns2:PSR_Ref', NS_MAP)
            if psr_ref is not None:
                text.object_id = psr_ref.get('ObjectID')
                text.object_name = psr_ref.get('ObjectName')
                text.psr_type = psr_ref.get('PSRType')

    def _associate_texts_with_elements(self):
        for text_id, text in self.texts.items():
            elem_id = None
            
            if text_id.startswith('TXT-'):
                candidate_id = text_id[4:]
                if candidate_id in self.elements:
                    elem_id = candidate_id
            
            if elem_id is None and text.object_id:
                for eid, elem in self.elements.items():
                    if elem.object_id == text.object_id:
                        elem_id = eid
                        break
            
            if elem_id is None and text.object_name:
                for eid, elem in self.elements.items():
                    if elem.object_name == text.object_name:
                        elem_id = eid
                        break
            
            if elem_id is None:
                for eid, elem in self.elements.items():
                    dist = ((text.x - elem.x) ** 2 + (text.y - elem.y) ** 2) ** 0.5
                    if dist < 30:
                        elem_id = eid
                        break
            
            if elem_id:
                text.related_element_id = elem_id
                self.elements[elem_id].add_related_text(text_id)

    def _class_to_voltage(self, css_class):
        if not css_class:
            return None
        match = re.search(r'lkv(\d+(?:\.\d+)?)', css_class)
        if match:
            return match.group(1) + 'kV'
        match = re.search(r'kv(\d+(?:\.\d+)?)', css_class)
        if match:
            return match.group(1) + 'kV'
        return None

    def _parse_points_str(self, points_str):
        coords = []
        pairs = re.findall(r'([\d.]+),([\d.]+)', points_str)
        for x, y in pairs:
            coords.append((float(x), float(y)))
        return coords

    def _parse_metadata(self, group, element):
        metadata = group.find('.//ns0:metadata', NS_MAP)
        if metadata is not None:
            psr_ref = metadata.find('.//ns2:PSR_Ref', NS_MAP)
            if psr_ref is not None:
                element.object_id = psr_ref.get('ObjectID')
                element.object_name = psr_ref.get('ObjectName')
                element.psr_type = psr_ref.get('PSRType')
            
            layer_ref = metadata.find('.//ns2:Layer_Ref', NS_MAP)
            if layer_ref is not None:
                element.layer = layer_ref.get('ObjectName')

    def parse_lines(self, root):
        for layer_id in ['ConnLine_Layer', 'ACLineSegment_Layer']:
            layer = root.find(f'.//ns0:g[@id="{layer_id}"]', NS_MAP)
            if layer is None:
                continue
            
            for group in layer.findall('.//ns0:g', NS_MAP):
                group_id = group.get('id', '')
                polyline = group.find('.//ns0:polyline', NS_MAP)
                line_elem = group.find('.//ns0:line', NS_MAP)
                
                if polyline is not None:
                    points_str = polyline.get('points', '')
                    line_class = polyline.get('class', '')
                    stroke = polyline.get('stroke', '')
                    stroke_width = polyline.get('stroke-width', '')
                    
                    line = SvgLine(group_id, points_str, line_class)
                    line.voltage_level = self._class_to_voltage(line_class)
                    line.color = stroke
                    line.stroke_width = stroke_width
                    line.css_class = line_class
                    line.infer_line_type()
                    
                    self._parse_line_metadata(group, line)
                    self.add_line(line)
                
                elif line_elem is not None:
                    x1 = line_elem.get('x1', '0')
                    y1 = line_elem.get('y1', '0')
                    x2 = line_elem.get('x2', '0')
                    y2 = line_elem.get('y2', '0')
                    points_str = f"{x1},{y1} {x2},{y2}"
                    line_class = line_elem.get('class', '')
                    stroke = line_elem.get('stroke', '')
                    stroke_width = line_elem.get('stroke-width', '')
                    
                    line = SvgLine(group_id, points_str, line_class)
                    line.voltage_level = self._class_to_voltage(line_class)
                    line.color = stroke
                    line.stroke_width = stroke_width
                    line.css_class = line_class
                    line.infer_line_type()
                    
                    self._parse_line_metadata(group, line)
                    self.add_line(line)

    def _parse_line_metadata(self, group, line):
        metadata = group.find('.//ns0:metadata', NS_MAP)
        if metadata is not None:
            psr_ref = metadata.find('.//ns2:PSR_Ref', NS_MAP)
            if psr_ref is not None:
                line.object_id = psr_ref.get('ObjectID')
                meta_line_type = psr_ref.get('LineType')
                if meta_line_type:
                    line.line_type = meta_line_type
                    line.line_type_cn = LINE_TYPE_NAME_MAP.get(meta_line_type, meta_line_type)
            
            for glink in metadata.findall('.//ns2:GLink_Ref', NS_MAP):
                line.glink_refs.append(glink.get('ObjectID'))

    def build_connections(self):
        skipped = 0
        for line_id, line in self.lines.items():
            if not line.points:
                continue
            
            start_coords = line.points[0]
            end_coords = line.points[-1]
            
            start_elem, start_term = self._find_nearest_element(start_coords, exclude_element_id=None)
            end_elem, end_term = self._find_nearest_element(end_coords, exclude_element_id=start_elem.element_id if start_elem else None)
            
            if start_elem and end_elem:
                if start_elem.element_id == end_elem.element_id and start_term == end_term:
                    skipped += 1
                    continue
                
                conn = SvgConnection(
                    start_elem.element_id, start_term,
                    end_elem.element_id, end_term,
                    line_id
                )
                self.add_connection(conn)
        
        if skipped > 0:
            print(f"  跳过自连接(同设备同端子): {skipped}条")

    def _find_nearest_element(self, coords, exclude_element_id=None):
        nearest = None
        min_dist = float('inf')
        nearest_term = 1
        x, y = coords
        
        for elem in self.elements.values():
            if exclude_element_id and elem.element_id == exclude_element_id:
                continue
            
            if elem.terminals:
                for term in elem.terminals:
                    dist = ((x - term.x) ** 2 + (y - term.y) ** 2) ** 0.5
                    if dist < min_dist and dist < 3:
                        min_dist = dist
                        nearest = elem
                        nearest_term = term.index
            else:
                dist = ((x - elem.x) ** 2 + (y - elem.y) ** 2) ** 0.5
                if dist < min_dist and dist < 8:
                    min_dist = dist
                    nearest = elem
                    nearest_term = 1
        
        if nearest is None:
            nearest, min_dist, nearest_term = self._find_best_match(coords, exclude_element_id)
        
        return nearest, nearest_term

    def _find_best_match(self, coords, exclude_element_id=None):
        nearest = None
        min_dist = float('inf')
        nearest_term = 1
        x, y = coords
        
        for elem in self.elements.values():
            if exclude_element_id and elem.element_id == exclude_element_id:
                continue
            
            if elem.terminals:
                for term in elem.terminals:
                    dist = ((x - term.x) ** 2 + (y - term.y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        nearest = elem
                        nearest_term = term.index
            else:
                dist = ((x - elem.x) ** 2 + (y - elem.y) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest = elem
                    nearest_term = 1
        
        return nearest, min_dist, nearest_term

    def export_elements_json(self, filename='svg_elements.json'):
        data = {
            'filename': self.filename,
            'element_count': len(self.elements),
            'line_count': len(self.lines),
            'text_count': len(self.texts),
            'connection_count': len(self.connections),
            'elements': [e.to_dict() for e in self.elements.values()],
            'texts': [t.to_dict() for t in self.texts.values()]
        }
        save_path = os.path.join(OUTPUT_JSON, filename)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return save_path

    def export_connections_json(self, filename='svg_connections.json'):
        data = {
            'filename': self.filename,
            'connections': [c.to_dict() for c in self.connections]
        }
        save_path = os.path.join(OUTPUT_JSON, filename)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return save_path

    def export_elements_csv(self, filename='svg_elements.csv'):
        rows = []
        for elem in self.elements.values():
            for term in elem.terminals:
                rows.append({
                    'element_id': elem.element_id,
                    'element_type': elem.element_type,
                    'element_type_cn': TYPE_NAME_MAP.get(elem.element_type, elem.element_type),
                    'x': round(elem.x, 4),
                    'y': round(elem.y, 4),
                    'object_id': elem.object_id,
                    'object_name': elem.object_name,
                    'psr_type': elem.psr_type,
                    'layer': elem.layer,
                    'voltage_level': elem.voltage_level,
                    'css_class': elem.css_class,
                    'stroke_color': elem.stroke_color,
                    'is_junction': elem.is_junction,
                    'related_text_count': len(elem.related_text_ids),
                    'terminal_index': term.index,
                    'terminal_x': round(term.x, 4),
                    'terminal_y': round(term.y, 4)
                })
            if not elem.terminals:
                rows.append({
                    'element_id': elem.element_id,
                    'element_type': elem.element_type,
                    'element_type_cn': TYPE_NAME_MAP.get(elem.element_type, elem.element_type),
                    'x': round(elem.x, 4),
                    'y': round(elem.y, 4),
                    'object_id': elem.object_id,
                    'object_name': elem.object_name,
                    'psr_type': elem.psr_type,
                    'layer': elem.layer,
                    'voltage_level': elem.voltage_level,
                    'css_class': elem.css_class,
                    'stroke_color': elem.stroke_color,
                    'is_junction': elem.is_junction,
                    'related_text_count': len(elem.related_text_ids),
                    'terminal_index': '',
                    'terminal_x': '',
                    'terminal_y': ''
                })
        
        df = pd.DataFrame(rows)
        save_path = os.path.join(OUTPUT_CSV, filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

    def export_texts_csv(self, filename='svg_texts.csv'):
        rows = []
        for text in self.texts.values():
            rows.append({
                'text_id': text.text_id,
                'x': round(text.x, 4),
                'y': round(text.y, 4),
                'content': text.content,
                'font_size': round(text.font_size, 4),
                'color': text.color,
                'object_id': text.object_id,
                'related_element_id': text.related_element_id
            })
        
        df = pd.DataFrame(rows)
        save_path = os.path.join(OUTPUT_CSV, filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path

    def export_connections_csv(self, filename='svg_connections.csv'):
        rows = []
        for conn in self.connections:
            from_elem = self.elements.get(conn.from_element_id)
            to_elem = self.elements.get(conn.to_element_id)
            line = self.lines.get(conn.line_id) if conn.line_id else None
            rows.append({
                'line_id': conn.line_id,
                'line_type': line.line_type if line else '',
                'line_type_cn': line.line_type_cn if line else '',
                'inferred_type': line.inferred_type if line else '',
                'inferred_type_cn': line.inferred_type_cn if line else '',
                'line_color': line.color if line else '',
                'line_stroke_width': line.stroke_width if line else '',
                'from_element_id': conn.from_element_id,
                'from_element_type': from_elem.element_type if from_elem else '',
                'from_element_name': from_elem.object_name if from_elem else '',
                'from_terminal': conn.from_terminal,
                'to_element_id': conn.to_element_id,
                'to_element_type': to_elem.element_type if to_elem else '',
                'to_element_name': to_elem.object_name if to_elem else '',
                'to_terminal': conn.to_terminal
            })
        
        df = pd.DataFrame(rows)
        save_path = os.path.join(OUTPUT_CSV, filename)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        return save_path


class SvgParser:
    @staticmethod
    def parse(file_path):
        doc = SvgDocument()
        doc.filename = os.path.basename(file_path)
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            doc.load_symbol_defs(root)
            doc.parse_elements(root)
            doc.parse_texts(root)
            doc.parse_lines(root)
            doc.build_connections()
            
            print(f"SVG解析完成: {doc.filename}")
            print(f"  图元数量: {len(doc.elements)}")
            print(f"  线路数量: {len(doc.lines)}")
            print(f"  文字标注: {len(doc.texts)}")
            print(f"  连接关系: {len(doc.connections)}")
            
            type_counts = {}
            for elem in doc.elements.values():
                t = elem.element_type
                type_counts[t] = type_counts.get(t, 0) + 1
            print(f"  设备类型分布: {type_counts}")
            
            return doc
        except Exception as e:
            import traceback
            print(f"SVG解析失败: {e}")
            traceback.print_exc()
            return None


if __name__ == "__main__":
    
    svg_dir = r"D:\挑战杯\挑战杯\数据集更新版\数据集更新版20260729\配网 svg"
    
    for fname in ['LINE215.svg', 'LINE216.svg']:
        fpath = os.path.join(svg_dir, fname)
        if os.path.exists(fpath):
            print(f"\n=== 解析 {fname} ===")
            doc = SvgParser.parse(fpath)
            if doc:
                doc.export_elements_json(f'{fname}_elements.json')
                doc.export_elements_csv(f'{fname}_elements.csv')
                doc.export_texts_csv(f'{fname}_texts.csv')
                doc.export_connections_json(f'{fname}_connections.json')
                doc.export_connections_csv(f'{fname}_connections.csv')
                print(f"  导出完成")
        else:
            print(f" 文件不存在: {fname}")