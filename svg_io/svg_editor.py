import os
import sys
import uuid
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from svg_io.svg_beautifier import SvgBeautifier

SVG_NS = 'http://www.w3.org/2000/svg'

CONDUCTIVE_TYPES = {
    '0307', '0201', '0202', '0203', '0302', '0309',
    '0110', '0111', '0311', '370000', '0313', '0314', '0115',
}

DEVICE_TYPE_MAP = {
    '开关': '0307', '断路器': '0307', 'breaker': '0307',
    '刀闸': '0202', '隔离开关': '0202', 'disconnector': '0202',
    '接地刀闸': '0203', '地刀': '0203',
    '负荷开关': '0201', 'loadswitch': '0201',
    '熔断器': '0302', 'fuse': '0302',
    '配变': '0111', '变压器': '0111', '配电变压器': '0111', 'transformer': '0111',
    '母线': '0311', 'busbar': '0311',
    '用户': '370000', 'energyconsumer': '370000',
    '避雷器': '0116', 'surgearrester': '0116',
    'pt': '0305', '电压互感器': '0305',
    'ct': '0306', '电流互感器': '0306',
    '故障指示器': '0309',
}

TYPE_SYMBOL_KW = {
    '0307': 'Breaker', '0201': 'LoadBreakSwitch',
    '0202': 'Disconnector', '0203': 'GroundDisconnector',
    '0302': 'Fuse', '0111': 'PowerTransformer',
    '0311': 'Busbar', '370000': 'EnergyConsumer',
    '0116': 'SurgeArrester', '0305': 'PotentialTransformer',
    '0306': 'CurrentTransformer', '0309': 'FaultIndicator',
}

TYPE_LAYER = {
    '0307': 'Breaker', '0201': 'LoadBreakSwitch',
    '0202': 'Disconnector', '0203': 'GroundDisconnector',
    '0302': 'Fuse', '0111': 'PowerTransformer',
    '0311': 'BusbarSection', '370000': 'EnergyConsumer',
    '0116': 'SurgeArrester', '0305': 'PotentialTransformer',
    '0306': 'CurrentTransformer', '0309': 'FaultIndicator',
}


class SvgInteractiveEditorV2:
    def __init__(self, beautifier: SvgBeautifier):
        self.b = beautifier
        if not self.b.devices:
            self.b._prepare_internal_data()
        self._inserted_stations = []
        self._inserted_devices = []

    def _find_id_by_name(self, name_query: str) -> Optional[str]:
        for pid, d in self.b.devices.items():
            if d.get('name') == name_query:
                return pid
            if name_query in d.get('name', ''):
                return pid
        return name_query if name_query in self.b.devices else None

    def _resolve_type(self, type_input: str) -> Optional[str]:
        if type_input in DEVICE_TYPE_MAP.values():
            return type_input
        return DEVICE_TYPE_MAP.get(type_input.strip())

    def _find_symbol_by_type(self, dev_type: str) -> str:
        kw = TYPE_SYMBOL_KW.get(dev_type, '')
        if not kw or not self.b.doc or self.b.doc.root is None:
            return ''
        defs = self.b.doc.root.find(f'{{{SVG_NS}}}defs')
        if defs is None:
            return ''
        for s in defs.findall(f'{{{SVG_NS}}}symbol'):
            sid = s.get('id', '')
            if kw in sid:
                return '#' + sid
        return ''

    def _gen_id(self) -> str:
        return f'NEW_{uuid.uuid4().hex[:8].upper()}'

    def add_device(self, device_type, name, upstream_query,
                   downstream_query=None, container_query=None):
        print(f"\n[Editor] 新增设备: {name} (类型={device_type})")
        dev_type = self._resolve_type(device_type)
        if not dev_type:
            print(f"  [错误] 未知设备类型: {device_type}")
            print(f"  支持的类型: {', '.join(DEVICE_TYPE_MAP.keys())}")
            return False

        up_id = self._find_id_by_name(upstream_query)
        if not up_id:
            print(f"  [错误] 找不到上游设备: {upstream_query}")
            return False

        down_id = self._find_id_by_name(downstream_query) if downstream_query else None

        new_id = self._gen_id()
        sym = self._find_symbol_by_type(dev_type)

        ssjg = ''
        if container_query:
            for cid, c in self.b.containers.items():
                if container_query in c.get('name', '') or cid == container_query:
                    ssjg = cid
                    break
        if not ssjg:
            ssjg = self.b.devices[up_id].get('ssjg', '')

        self.b.devices[new_id] = {
            'id': new_id, 'type': dev_type, 'name': name,
            'ssjg': ssjg, 'glinks': [], 'symbol': sym, 'vclass': 'lkv10',
            'layer': TYPE_LAYER.get(dev_type, 'Unknown'),
            'orig_x': 0.0, 'orig_y': 0.0,
        }
        self.b.adj[new_id] = set()

        if ssjg and ssjg in self.b.containers:
            if new_id not in self.b.containers[ssjg]['members']:
                self.b.containers[ssjg]['members'].append(new_id)

        self.b.adj[up_id].add(new_id)
        self.b.adj[new_id].add(up_id)

        if down_id:
            if down_id in self.b.adj.get(up_id, set()):
                self.b.adj[up_id].remove(down_id)
            if up_id in self.b.adj.get(down_id, set()):
                self.b.adj[down_id].remove(up_id)
            self.b.adj[new_id].add(down_id)
            self.b.adj[down_id].add(new_id)
            print(f"  [插入] {up_id} -> {new_id} -> {down_id}")
        else:
            print(f"  [分支] {up_id} -> {new_id}")

        self._inserted_devices.append({
            'id': new_id, 'up_id': up_id, 'down_id': down_id,
        })
        print(f"  [成功] 设备 {name} ({new_id}) 已新增")
        return True

    def add_station(self, station_id, station_name, upstream_query,
                    downstream_query, internal_switch_ids):
        print(f"\n[Editor] 新增站房 {station_id} ({station_name})")
        up_id = self._find_id_by_name(upstream_query)
        down_id = self._find_id_by_name(downstream_query)
        if not up_id or not down_id:
            print(f"  [错误] 找不到设备: {upstream_query} / {downstream_query}")
            return False

        if down_id in self.b.adj.get(up_id, set()):
            self.b.adj[up_id].remove(down_id)
        if up_id in self.b.adj.get(down_id, set()):
            self.b.adj[down_id].remove(up_id)

        cid = f"STATION_{station_id}"
        self.b.containers[cid] = {
            'id': cid, 'name': station_name, 'type': 'Substation',
            'psr_id': cid, 'members': []
        }

        sym = self._find_symbol_by_type('0307')
        sw_full_ids = []
        for sw_id in internal_switch_ids:
            full_id = f"SW_{sw_id}"
            self.b.devices[full_id] = {
                'id': full_id, 'type': '0307', 'name': f'开关{sw_id}',
                'ssjg': cid, 'glinks': [], 'symbol': sym, 'vclass': 'lkv10',
                'layer': 'Breaker', 'orig_x': 0.0, 'orig_y': 0.0,
            }
            self.b.containers[cid]['members'].append(full_id)
            sw_full_ids.append(full_id)
            self.b.adj[full_id] = set()

        sw1, sw2, sw3 = sw_full_ids[0], sw_full_ids[1], sw_full_ids[2]
        self.b.adj[up_id].add(sw1)
        self.b.adj[sw1].add(up_id)
        self.b.adj[sw3].add(down_id)
        self.b.adj[down_id].add(sw3)
        self.b.adj[sw1].add(sw3)
        self.b.adj[sw3].add(sw1)

        self._inserted_stations.append({
            'cid': cid, 'up_id': up_id, 'down_id': down_id,
            'switches': sw_full_ids,
        })
        print(f"  [成功] 上游{up_id}->SW1, SW3->下游{down_id}, SW1<->SW3连通")
        return True

    def delete_device(self, dev_query):
        print(f"\n[Editor] 删除设备: {dev_query}")
        target_id = self._find_id_by_name(dev_query)
        if not target_id:
            print(f"  [错误] 找不到设备 {dev_query}")
            return False

        neighbors = list(self.b.adj.get(target_id, set()))
        conductive_neighbors = [
            n for n in neighbors
            if n != target_id
            and n in self.b.devices
            and self.b.devices[n]['type'] in CONDUCTIVE_TYPES
        ]

        del self.b.devices[target_id]
        if target_id in self.b.pos:
            del self.b.pos[target_id]
        for n in neighbors:
            if target_id in self.b.adj.get(n, set()):
                self.b.adj[n].remove(target_id)
        if target_id in self.b.adj:
            del self.b.adj[target_id]
        for cid, c in self.b.containers.items():
            if target_id in c['members']:
                c['members'].remove(target_id)

        if len(conductive_neighbors) >= 2:
            n1 = conductive_neighbors[0]
            for n2 in conductive_neighbors[1:]:
                self.b.adj[n1].add(n2)
                self.b.adj[n2].add(n1)
            print(f"  [修复] 连通 {len(conductive_neighbors)} 个导电邻居")
        elif len(conductive_neighbors) == 1:
            print(f"  [提示] 仅1个导电邻居，无需连通")
        else:
            print(f"  [警告] 无导电邻居，删除后可能悬空")

        print(f"  [成功] 设备 {target_id} 已删除")
        return True

    def reposition_inserted(self):
        for st in self._inserted_stations:
            up_id, down_id = st['up_id'], st['down_id']
            sw_ids, cid = st['switches'], st['cid']
            if up_id not in self.b.pos or down_id not in self.b.pos:
                continue
            ux, uy = self.b.pos[up_id]
            dx, dy = self.b.pos[down_id]
            cx = (ux + dx) / 2
            cy = max(uy, dy) + 90
            for i, sw in enumerate(sw_ids):
                self.b.pos[sw] = (cx, cy + i * 70)
            if cid in self.b.containers:
                ms = [m for m in self.b.containers[cid]['members'] if m in self.b.pos]
                if len(ms) >= 2:
                    xs = [self.b.pos[m][0] for m in ms]
                    ys = [self.b.pos[m][1] for m in ms]
                    self.b.cont_box[cid] = (
                        min(xs) - 30, min(ys) - 30,
                        max(xs) + 30, max(ys) + 30,
                    )

        for dv in self._inserted_devices:
            new_id, up_id, down_id = dv['id'], dv['up_id'], dv['down_id']
            if new_id not in self.b.pos or up_id not in self.b.pos:
                continue
            ux, uy = self.b.pos[up_id]
            if down_id and down_id in self.b.pos:
                dx, dy = self.b.pos[down_id]
                self.b.pos[new_id] = ((ux + dx) / 2, (uy + dy) / 2)
            else:
                self.b.pos[new_id] = (ux, uy + 80)

    def save(self, output_path=None):
        out = output_path or self.b.output_path
        self.b.layout()
        self.reposition_inserted()
        self.b.render(out)
        print(f"[Editor] 已保存: {out}")
        return out


def interactive_cli():
    print("=" * 60)
    print("SVG 配电网单线图 交互式编辑器")
    print("=" * 60)

    file_path = input("原始SVG路径: ").strip()
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return

    out_path = input("保存路径 (默认 output/svg/edited.svg): ").strip() or "output/svg/edited.svg"

    b = SvgBeautifier(file_path, output_path=out_path)
    b._prepare_internal_data()
    b.repair()
    editor = SvgInteractiveEditorV2(b)

    while True:
        print("\n  1. 新增站房(含内部开关)")
        print("  2. 新增单个设备(开关/刀闸/配变等)")
        print("  3. 删除设备")
        print("  4. 查看当前设备列表")
        print("  5. 渲染保存并退出")
        print("  6. 放弃退出")
        choice = input("选择 (1-6): ").strip()

        if choice == '1':
            sid = input("站房编号: ").strip()
            sname = input("站房名称: ").strip() or f"站房{sid}"
            up = input("上游设备名称: ").strip()
            down = input("下游设备名称: ").strip()
            sw_str = input("站内开关编号(逗号分隔,至少3个): ").strip()
            switches = [s.strip() for s in sw_str.split(',') if s.strip()]
            if len(switches) < 3:
                print("至少需要3个开关")
                continue
            editor.add_station(sid, sname, up, down, switches)

        elif choice == '2':
            dtype = input("设备类型(开关/刀闸/配变/负荷开关/熔断器/用户等): ").strip()
            name = input("设备名称: ").strip()
            up = input("上游设备名称: ").strip()
            down = input("下游设备名称(留空则作为分支): ").strip()
            cont = input("所属容器(留空则继承上游): ").strip()
            editor.add_device(dtype, name, up, down or None, cont or None)

        elif choice == '3':
            dev = input("要删除的设备名称: ").strip()
            editor.delete_device(dev)

        elif choice == '4':
            keyword = input("搜索关键词(留空显示全部): ").strip()
            count = 0
            for pid, d in editor.b.devices.items():
                if not editor.b.is_real_device(d['type']):
                    continue
                if keyword and keyword not in d.get('name', ''):
                    continue
                print(f"  {pid}: {d['name']} (类型={d['type']})")
                count += 1
                if count >= 50:
                    print("  ... (仅显示前50条)")
                    break

        elif choice == '5':
            editor.save(out_path)
            break

        elif choice == '6':
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        interactive_cli()
    else:
        print("使用 python svg_io/svg_editor.py --cli 进入交互模式")
