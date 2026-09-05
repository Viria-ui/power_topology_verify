"""拓扑自动修复模块（对齐成员2算法要求）。

该模块在解析后、美化布局前运行，负责：
1. 修复悬空连接线（飞线）：根据几何位置匹配最近设备。
2. 同步 glink_refs：确保 IR 模型中的逻辑引用与物理连接一致。
3. 清理冗余图元：删除零长度连接线或无关联的标注。
4. 修复虚假连通：基于几何邻近性纠正错误的连接指向。
"""
import math
import uuid
import logging
import networkx as nx
from collections import defaultdict
from typing import List, Tuple, Optional, Dict

logger = logging.getLogger(__name__)
from data_io.svg_reader import SvgDocument, SvgElement, SvgConnection

class TopologyRepairer:
    def __init__(self, doc: SvgDocument):
        self.doc = doc
        self.repaired_count = 0
        self.stats = {}

    def repair(self):
        """执行全量修复流水线。"""
        with open("debug_repair.txt", "w") as f:
            f.write(f"Starting repair for {self.doc.svg_filename}\n")
        
        # 1. 归一化旋转角度
        self._normalize_rotation()
        with open("debug_repair.txt", "a") as f: f.write("Normalized rotation\n")
        
        # 2. 建立站房归属关系
        self._identify_station_affiliation()
        with open("debug_repair.txt", "a") as f: f.write("Identified station affiliation\n")
        
        # 3. 修复飞线端点
        self._repair_dangling_connections()
        with open("debug_repair.txt", "a") as f: f.write("Repaired dangling connections\n")
        
        # 4. 强力缝合孤立节点
        self._stitch_isolated_nodes()
        with open("debug_repair.txt", "a") as f: f.write("Stitched isolated nodes\n")
        
        # 5. 同步 glink_refs
        self._sync_glink_refs()
        with open("debug_repair.txt", "a") as f: f.write("Synced glink_refs\n")
        
        # 6. 识别电源点与主干/支线标记
        self._identify_topology_hierarchy()
        with open("debug_repair.txt", "a") as f: f.write("Identified topology hierarchy\n")
        
        # 7. IR 级别连接线正交化
        self._orthogonalize_connections()
        with open("debug_repair.txt", "a") as f: f.write("Orthogonalized connections\n")
        
        # 8. 清理无效图元与孤立线路
        self._cleanup_invalid_elements()
        self._cleanup_orphan_lines()
        with open("debug_repair.txt", "a") as f: f.write("Cleaned up elements\n")
        
        # 9. 拓扑质量分析
        self._analyze_topology_quality()
        with open("debug_repair.txt", "a") as f: f.write("Analyzed quality\n")
        
        return self.doc

    def _cleanup_orphan_lines(self):
        """核心修复：清理既没有电气连接也没有 glink_refs 的线路段，防止布局时产生飞线。"""
        device_map = {e.element_id: e for e in self.doc.elements if e.element_id}
        conn_nodes = set()
        for conn in self.doc.connections:
            if conn.start_device_id: conn_nodes.add(conn.start_device_id)
            if conn.end_device_id: conn_nodes.add(conn.end_device_id)
            
        keep_elements = []
        for elem in self.doc.elements:
            if elem.layer_name in ("ACLineSegment", "BusbarSection"):
                # 如果既不在连接关系中，也没有 glink_refs，则视为孤立飞线
                has_conn = elem.element_id in conn_nodes
                has_refs = any(ref in device_map for ref in elem.glink_refs)
                if not (has_conn or has_refs):
                    self.repaired_count += 1
                    continue
            keep_elements.append(elem)
        
        self.doc.elements = keep_elements

    def _normalize_rotation(self):
        """不再强制重置所有旋转，保留原始旋转信息以供后续布局决策。"""
        pass

    def _identify_station_affiliation(self):
        """建立设备与站房容器的归属关系 (基于几何包含)。"""
        stations = [e for e in self.doc.elements if e.layer_name == "Substation"]
        if not stations: return

        # 在修复阶段就建立归属，并写入 IR
        count = 0
        for elem in self.doc.elements:
            if elem.layer_name == "Substation": continue
            for st in stations:
                # 增加 5px 的容差
                if (st.x - 5 <= elem.x <= st.x + st.width + 5 and 
                    st.y - 5 <= elem.y <= st.y + st.height + 5):
                    elem.container_id = st.element_id
                    count += 1
                    break
        logger.info(f"已建立 {count} 个设备的站房归属关系")

    def _identify_topology_hierarchy(self):
        """识别电源点、主干线与支线，为布局提供层级参考。"""
        G = nx.Graph()
        for conn in self.doc.connections:
            if conn.start_device_id and conn.end_device_id:
                G.add_edge(conn.start_device_id, conn.end_device_id)
        
        device_map = {e.element_id: e for e in self.doc.elements if e.element_id}
        
        for elem in self.doc.elements:
            if elem.layer_name == "Substation": continue
            if elem.element_id not in G: G.add_node(elem.element_id)
            elem.line_type = "Branch"
        
        if not G.nodes: return

        # 3. 寻找电源点 (SOURCE)
        source_id = None
        min_x = float('inf')
        for nid in G.nodes:
            elem = device_map.get(nid)
            if not elem: continue
            if elem.x < min_x:
                min_x = elem.x
                source_id = nid
        
        if not source_id: return
        
        source_elem = device_map.get(source_id)
        if source_elem:
            source_elem.business_type = "SOURCE"
            source_elem.line_type = "Trunk"

        # 4. 基于 BFS 标记 Trunk
        try:
            for component in nx.connected_components(G):
                comp_nodes = list(component)
                comp_source = source_id if source_id in component else sorted(comp_nodes, key=lambda n: device_map[n].x if n in device_map else 0)[0]
                path_lengths = nx.single_source_shortest_path_length(G, comp_source)
                for eid, dist in path_lengths.items():
                    elem = device_map.get(eid)
                    if elem:
                        elem.line_type = "Trunk" if dist < 20 else "Branch"
        except Exception as e:
            pass

    def _orthogonalize_connections(self):
        """IR 级别强制正交化所有连接线及线路图元。"""
        device_map = {e.element_id: e for e in self.doc.elements if e.element_id}
        
        # 1. 处理 SvgConnection (连接线)
        for conn in self.doc.connections:
            s, e = device_map.get(conn.start_device_id), device_map.get(conn.end_device_id)
            if not s or not e: continue
            
            p1 = (s.x + s.width/2, s.y + s.height/2)
            p2 = (e.x + e.width/2, e.y + e.height/2)
            
            # 强制 L-Shape 正交
            conn.points = [p1, (p2[0], p1[1]), p2]
            self.repaired_count += 1

        # 2. 处理 ACLineSegment 和 BusbarSection (线路图元)
        for elem in self.doc.elements:
            if elem.layer_name in ("ACLineSegment", "BusbarSection") and len(elem.points) >= 2:
                new_points = [elem.points[0]]
                changed = False
                for i in range(len(elem.points) - 1):
                    p1, p2 = elem.points[i], elem.points[i+1]
                    if abs(p1[0] - p2[0]) > 0.5 and abs(p1[1] - p2[1]) > 0.5:
                        # 斜线：插入折点使其正交
                        new_points.append((p2[0], p1[1]))
                        changed = True
                    new_points.append(p2)
                
                if changed:
                    elem.points = new_points
                    self.repaired_count += 1

    def _repair_dangling_connections(self):
        """修复端点缺失的连接线。"""
        devs = [(e.x + e.width / 2, e.y + e.height / 2, e.width, e.height, e.element_id) 
                for e in self.doc.elements if e.element_id and e.layer_name != "Substation"]
        
        if not devs: return

        def _find_nearest_device(px: float, py: float, exclude_id: str = None) -> Optional[str]:
            best_id, best_d = None, float('inf')
            for cx, cy, w, h, did in devs:
                if exclude_id and did == exclude_id: continue
                dx = max(cx - w/2 - px, 0, px - (cx + w/2))
                dy = max(cy - h/2 - py, 0, py - (cy + h/2))
                d2 = dx*dx + dy*dy
                if d2 < best_d:
                    best_d, best_id = d2, did
            return best_id if best_d < 2500 else None # 50px 容差

        for conn in self.doc.connections:
            if not conn.points or len(conn.points) < 2: continue
            
            if not conn.start_device_id:
                nearest = _find_nearest_device(conn.points[0][0], conn.points[0][1])
                if nearest:
                    conn.start_device_id = nearest
                    self.repaired_count += 1
            
            if not conn.end_device_id:
                nearest = _find_nearest_device(conn.points[-1][0], conn.points[-1][1], conn.start_device_id)
                if nearest:
                    conn.end_device_id = nearest
                    self.repaired_count += 1

    def _stitch_isolated_nodes(self):
        """强力缝合所有拓扑孤岛，确保最终只有极少数连通分量。"""
        G = nx.Graph()
        for conn in self.doc.connections:
            if conn.start_device_id and conn.end_device_id:
                G.add_edge(conn.start_device_id, conn.end_device_id)
        
        # 1. 建立快速查询索引
        device_map = {e.element_id: e for e in self.doc.elements if e.element_id}
        
        # 2. 确保所有非站房元素都在图中
        for e in self.doc.elements:
            if not e.element_id:
                e.element_id = f"AUTO_ID_{uuid.uuid4().hex[:8]}"
                device_map[e.element_id] = e
            if e.layer_name != "Substation":
                if e.element_id not in G: G.add_node(e.element_id)
            
        components = list(nx.connected_components(G))
        if len(components) <= 1: return
        
        # 3. 收集每个连通分量的中心点和代表节点
        comp_data = []
        for comp in components:
            comp_nodes = list(comp)
            # 仅考虑非线路设备作为锚点
            anchors = [n for n in comp_nodes if device_map.get(n) and device_map[n].layer_name not in ("ACLineSegment", "BusbarSection")]
            if not anchors: anchors = comp_nodes # 备选
            
            # 计算几何中心
            xs, ys = [], []
            for n in comp_nodes:
                e = device_map.get(n)
                if e:
                    xs.append(e.x + e.width/2)
                    ys.append(e.y + e.height/2)
            
            if not xs: continue
            center = (sum(xs)/len(xs), sum(ys)/len(ys))
            comp_data.append({"nodes": comp_nodes, "anchors": anchors, "center": center})
            
        # 4. 依次缝合相邻分量 (按几何中心排序)
        comp_data.sort(key=lambda x: (x["center"][0], x["center"][1]))
        
        for i in range(len(comp_data) - 1):
            c1, c2 = comp_data[i], comp_data[i+1]
            # 优化：仅比较代表节点，限制比较数量以保证性能
            best_pair, min_d2 = (None, None), float('inf')
            nodes1 = c1["anchors"][:10] 
            nodes2 = c2["anchors"][:10]
            
            for n1 in nodes1:
                e1 = device_map.get(n1)
                for n2 in nodes2:
                    e2 = device_map.get(n2)
                    d2 = (e1.x - e2.x)**2 + (e1.y - e2.y)**2
                    if d2 < min_d2:
                        min_d2, best_pair = d2, (n1, n2)
            
            if best_pair[0] and best_pair[1]:
                e1, e2 = device_map[best_pair[0]], device_map[best_pair[1]]
                new_conn = SvgConnection()
                new_conn.connection_id = f"STITCH_{uuid.uuid4().hex[:8]}"
                new_conn.start_device_id = e1.element_id
                new_conn.end_device_id = e2.element_id
                new_conn.points = [(e1.x, e1.y), (e2.x, e2.y)]
                new_conn.stroke = "none"
                self.doc.add_connection(new_conn)
                self.repaired_count += 1

    def _sync_glink_refs(self):
        """双向同步 glink_refs。"""
        device_map = {e.element_id: e for e in self.doc.elements if e.element_id}
        for conn in self.doc.connections:
            s_id, e_id = conn.start_device_id, conn.end_device_id
            if not s_id or not e_id: continue
            
            s_elem, e_elem = device_map.get(s_id), device_map.get(e_id)
            if s_elem and e_id not in s_elem.glink_refs: s_elem.glink_refs.append(e_id)
            if e_elem and s_id not in e_elem.glink_refs: e_elem.glink_refs.append(s_id)
            if e_id not in conn.glink_refs: conn.glink_refs.append(e_id)
            if s_id not in conn.glink_refs: conn.glink_refs.append(s_id)

    def _cleanup_invalid_elements(self):
        """清理零长度连接线。"""
        self.doc.connections = [c for c in self.doc.connections if c.points and len(c.points) >= 2]

    def _analyze_topology_quality(self):
        """分析拓扑质量并生成报告数据。"""
        G = nx.Graph()
        for conn in self.doc.connections:
            if conn.start_device_id and conn.end_device_id:
                G.add_edge(conn.start_device_id, conn.end_device_id)
        
        components = list(nx.connected_components(G))
        isolated_nodes = [e.element_id for e in self.doc.elements if e.element_id and e.element_id not in G and e.layer_name != "Substation"]
        
        self.stats = {
            "total_elements": len(self.doc.elements),
            "total_connections": len(self.doc.connections),
            "connected_components": len(components),
            "isolated_nodes_count": len(isolated_nodes),
            "dangling_devices_count": len([n for n in G.nodes if G.degree(n) < 2 and self.doc.get_device_by_id(n).layer_name not in ("EnergyConsumer", "PowerTransformer")]),
        }
        
        # 将分析结果保存到 doc 供导出
        self.doc.topology_stats = self.stats
