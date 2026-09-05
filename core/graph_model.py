"""设备/端点/边 拓扑图数据结构定义。"""
from pydantic import BaseModel
import networkx as nx
from typing import Optional, Dict
from collections import defaultdict


class Device(BaseModel):
    equip_id: str
    equip_name: Optional[str] = None
    equip_type: Optional[str] = None
    voltage_type: Optional[str] = None
    feeder_id: Optional[str] = None
    dsubstation_id: Optional[str] = None
    is_source: bool = False
    switch_status: Optional[str] = None


class ConnectPoint(BaseModel):
    point_id: str
    belong_equip_id: str
    feeder_id: Optional[str] = None


class TopoEdge(BaseModel):
    line_id: str
    start_point: str
    end_point: Optional[str] = None
    line_name: Optional[str] = None


class AbnormalItem(BaseModel):
    trace_uuid: str
    equip_id: str
    point_id: str
    line_id: Optional[str] = None
    rule_code: str
    rule_desc: str
    check_result: str
    review_status: str = "待复核"
    detail: str
    dimension: str = "拓扑完整性"   # 缺陷维度：拓扑完整性/图模一致性/电气逻辑/接口规范性
    risk_level: str = "中"          # 低/中/高


class BreakpointItem(BaseModel):
    trace_uuid: str
    equip_id: str
    point_id: str
    line_id: Optional[str] = None
    component_size: int
    rule_code: str
    rule_desc: str
    detail: str
    check_result: str = "ERR"
    dimension: str = "拓扑完整性"


class TieLoopItem(BaseModel):
    trace_uuid: str
    equip_id: str
    point_id: str
    line_id: Optional[str] = None
    result_type: str  # 联络 / 合环
    rule_code: str
    rule_desc: str
    detail: str
    switch_status: Optional[str] = None      # 分位/合位
    risk_level: str = "中"                   # 低/中/高
    review_required: bool = False            # 是否待人工复核
    left_feeder: Optional[str] = None        # 左侧馈线
    right_feeder: Optional[str] = None       # 右侧馈线
    left_station: Optional[str] = None       # 左侧厂站
    right_station: Optional[str] = None      # 右侧厂站
    source_count: int = 0                     # 连通区内电源点数量（合环判定用）
    is_planned_loop: bool = False             # 是否计划合环


class TopologyGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.device_map: dict[str, Device] = {}
        self.point_map: dict[str, ConnectPoint] = {}
        # 端子按所属设备建立索引，供大规模拓扑校验快速查询。
        self._points_by_equip: dict[str, list[str]] = defaultdict(list)
        self.edge_map: dict[str, TopoEdge] = {}
        self.abnormal_list: list[AbnormalItem] = []
        self.breakpoint_list: list[BreakpointItem] = []
        self.tie_loop_list: list[TieLoopItem] = []
        self.electrical_defects: list[dict] = []

        self.switch_state_map: Dict[str, str] = {}
        self.switch_state_source: Dict[str, str] = {}

    # ---- 两点间断点定位（标准输出 Sheet2 API） ----
    def find_breakpoint_between(self, equip_a: str, equip_b: str) -> list[dict]:
        """
        Sheet2 标准输出 API：给定两个设备ID（起点/终点），沿路径串点，
        返回断点(包括分位开关/物理断线/端子悬空)列表，用于 TMP0013138~TMP08047197 等任务。

        断点按 P1-P7 优先级降序输出：
          P1: 分位开关(开关-端子映射+switch_state_map)
          P2: 物理连通路径不存在(两点不连通)
          P3: 遥信-遥测矛盾(开关合位但两侧电压矛盾)
          P4: 单端子悬空(端子degree=0且非末端豁免)
          P5: 同馈线分多分量(馈线级R003)
          P6: 虚假连通(有GLink但端子无边)
          P7: 电源侧失压

        返回 list[dict]，每项：
          {priority, equip_id, point_id, breakpoint_type, detail, path_devices}
        """
        import networkx as nx_

        results: list[dict] = []
        if not equip_a or not equip_b:
            return results
        G = self.graph
        equip_points_a = self._points_by_equip.get(equip_a, [])
        equip_points_b = self._points_by_equip.get(equip_b, [])
        if not equip_points_a or not equip_points_b:
            results.append({
                "priority": "P2", "equip_id": f"{equip_a}<->{equip_b}", "point_id": "",
                "breakpoint_type": "端点设备无有效端子",
                "detail": f"输入设备缺少端子信息 a({len(equip_points_a)})/b({len(equip_points_b)})",
                "path_devices": [],
            })
            return results

        best_path: list[str] = []
        found = False
        pa_list = equip_points_a
        pb_list = equip_points_b
        for pa in pa_list:
            if not G.has_node(pa):
                continue
            for pb in pb_list:
                if not G.has_node(pb):
                    continue
                try:
                    p = nx_.shortest_path(G, pa, pb)
                    if not best_path or len(p) < len(best_path):
                        best_path = p
                        found = True
                except (nx_.NetworkXNoPath, nx_.NodeNotFound):
                    continue
        if not found:
            results.append({
                "priority": "P2", "equip_id": f"{equip_a}<->{equip_b}", "point_id": "",
                "breakpoint_type": "两点间无物理连通路径",
                "detail": f"输入两点在端子图不连通，疑似全局断点",
                "path_devices": [equip_a, equip_b],
            })
            return results

        path_devs: list[str] = []
        seen = set()
        for node in best_path:
            if node in self.point_map:
                pt = self.point_map[node]
                eid = pt.belong_equip_id
                if eid and eid not in seen:
                    path_devs.append(eid)
                    seen.add(eid)
            elif node in self.device_map and node not in seen:
                path_devs.append(node)
                seen.add(node)

        # P1: 路径上的分位开关（最高优先级，发现即终止后续检测）
        p1_found = False
        for eid in path_devs:
            dev = self.device_map.get(eid)
            if dev is None:
                continue
            e_type = str(dev.equip_type or "")
            from core.constants import SWITCH_TYPES as _ST
            if e_type in _ST or (dev.switch_status is not None):
                status = (self.switch_state_map.get(eid)
                          or dev.switch_status
                          or "close")
                # 统一状态映射：CLOSE/合位/1 → 合位，OPEN/分位/0 → 分位
                if str(status).upper() in {"OPEN", "分位", "0"}:
                    results.append({
                        "priority": "P1", "equip_id": eid,
                        "point_id": ",".join(self._points_by_equip.get(eid, [])[:5]),
                        "breakpoint_type": "[P1]路径上的分位开关(分位断点)",
                        "detail": f"开关{eid}[{dev.equip_name or ''}]状态={status}(分位) 切断两点间路径；开关分合位判定: 分位",
                        "path_devices": path_devs,
                        "switch_status_tag": "分位",
                        "yx_yz_conflict_tag": "",
                    })
                    p1_found = True
        # P1 命中时跳过 P2-P7（断点已定位，无需重复报告）
        if p1_found:
            _PRI_ORDER = {"P1": 0, "P2": 1, "P3": 2, "P4": 3, "P5": 4, "P6": 5, "P7": 6}
            for r in results:
                if not r["breakpoint_type"].startswith("[P"):
                    r["breakpoint_type"] = f"[{r.get('priority','P?')}]{r['breakpoint_type']}"
            results.sort(key=lambda x: _PRI_ORDER.get(x.get("priority", "P?"), 99))
            return results
        # P3: 遥信-遥测矛盾（开关合位标记 + 但一侧无电流/电压矛盾）
        try:
            if self.electrical_defects:
                for ed in self.electrical_defects:
                    eid_ed = ed.get("equip_id")
                    if eid_ed in path_devs and ed.get("rule_code") in ("RULE-E01", "RULE-E02", "RULE-E05"):
                        dev3 = self.device_map.get(eid_ed)
                        st = (self.switch_state_map.get(eid_ed) or (dev3.switch_status if dev3 else None) or "close")
                        if st in {"close", "合位", "1"}:
                            results.append({
                                "priority": "P3", "equip_id": eid_ed,
                                "point_id": ",".join(self._points_by_equip.get(eid_ed, [])[:5]),
                                "breakpoint_type": "[P3]遥信遥测矛盾(合位但失流/功率不匹配)",
                                "detail": ed.get("detail", "") + f" 开关状态={st}(合位)",
                                "path_devices": path_devs,
                                "switch_status_tag": "合位",
                                "yx_yz_conflict_tag": f"矛盾[{ed.get('rule_code','')}]",
                            })
        except Exception:
            pass
        # P4: 路径端子悬空
        for node in best_path:
            if G.has_node(node) and G.degree(node) <= 1 and node in self.point_map:
                pt = self.point_map[node]
                eid = pt.belong_equip_id
                dev = self.device_map.get(eid)
                from core.constants import TERMINAL_EXEMPT_TYPES as _TEX
                if dev and (dev.equip_type or "") not in _TEX:
                    results.append({
                        "priority": "P4", "equip_id": eid, "point_id": node,
                        "breakpoint_type": "[P4]路径上单端子悬空",
                        "detail": f"端子{node}仅{G.degree(node)}度连接，设备类型{dev.equip_type}",
                        "path_devices": path_devs,
                        "switch_status_tag": "",
                        "yx_yz_conflict_tag": "",
                    })
                    break
        # P5: 同馈线分多分量（馈线级连通性缺陷）
        try:
            import networkx as nx5
            feeder_of_path = set()
            for pn in path_devs:
                dv = self.device_map.get(pn)
                if dv and dv.feeder_id:
                    feeder_of_path.add(dv.feeder_id)
            if len(feeder_of_path) == 1:
                only_fid = next(iter(feeder_of_path))
                feed_nodes = set()
                for nid, nd in self.device_map.items():
                    if nd.feeder_id == only_fid:
                        feed_nodes.add(nid)
                        feed_nodes.update(self._points_by_equip.get(nid, []))
                subg_feed = G.subgraph(feed_nodes) if feed_nodes else None
                if subg_feed is not None and subg_feed.number_of_nodes() > 0:
                    ncomp = nx5.number_connected_components(subg_feed)
                    if ncomp > 1:
                        results.append({
                            "priority": "P5", "equip_id": f"FEEDER:{only_fid}",
                            "point_id": "",
                            "breakpoint_type": f"[P5]同馈线分多连通分量({ncomp}个)",
                            "detail": f"馈线{only_fid}的设备图存在{ncomp}个连通分量，疑似存在全局断点",
                            "path_devices": path_devs,
                            "switch_status_tag": "",
                            "yx_yz_conflict_tag": "",
                        })
        except Exception:
            pass
        # P6: 虚假连通（SVG GLink存在但端子无边）
        try:
            import networkx as nx6
            for idx_a in range(len(path_devs)):
                for idx_b in range(idx_a + 1, len(path_devs)):
                    ea, eb = path_devs[idx_a], path_devs[idx_b]
                    da, db = self.device_map.get(ea), self.device_map.get(eb)
                    if not da or not db:
                        continue
                    gl_a = getattr(da, "glink_refs", None) or []
                    gl_b = getattr(db, "glink_refs", None) or []
                    share_gl = set(gl_a) & set(gl_b)
                    if not share_gl:
                        continue
                    pts_a = self._points_by_equip.get(ea, [])
                    pts_b = self._points_by_equip.get(eb, [])
                    has_real_conn = False
                    for pa in pts_a:
                        for pb in pts_b:
                            if G.has_node(pa) and G.has_node(pb) and nx6.has_path(G, pa, pb):
                                if len(nx6.shortest_path(G, pa, pb)) <= 12:
                                    has_real_conn = True; break
                        if has_real_conn: break
                    if not has_real_conn and (len(pts_a) > 0 and len(pts_b) > 0):
                        results.append({
                            "priority": "P6", "equip_id": f"{ea}<->{eb}",
                            "point_id": "",
                            "breakpoint_type": "[P6]虚假连通(共有GLink但端子图无有效路径)",
                            "detail": f"GLink交集{list(share_gl)[:3]}但端子图最短路径>12跳/不连通",
                            "path_devices": path_devs,
                            "switch_status_tag": "",
                            "yx_yz_conflict_tag": "",
                        })
                        break
                else:
                    continue
                break
        except Exception:
            pass
        # P7: 电源失压(若提供了electrical_defects则查E03)
        if self.electrical_defects:
            for d in self.electrical_defects:
                if d.get("equip_id") in path_devs and d.get("rule_code") == "RULE-E03":
                    results.append({
                        "priority": "P7", "equip_id": d.get("equip_id"), "point_id": "",
                        "breakpoint_type": "[P7]路径电源侧失压(E03合位失压)",
                        "detail": d.get("detail", ""),
                        "path_devices": path_devs,
                        "switch_status_tag": "合位",
                        "yx_yz_conflict_tag": "",
                    })
                    break
        # 若命中了P1-P7但断点类型没带[priority]前缀（旧代码路径），补前缀保证分类输出
        _PRI_ORDER = {"P1": 0, "P2": 1, "P3": 2, "P4": 3, "P5": 4, "P6": 5, "P7": 6}
        for r in results:
            if not r["breakpoint_type"].startswith("[P"):
                r["breakpoint_type"] = f"[{r.get('priority','P?')}]{r['breakpoint_type']}"
        results.sort(key=lambda x: _PRI_ORDER.get(x.get("priority", "P?"), 99))
        return results

    def add_device(self, dev: Device):
        self.device_map[dev.equip_id] = dev
        self.graph.add_node(dev.equip_id, node_type="device", dev_info=dev.model_dump())

    def add_point(self, pt: ConnectPoint):
        old_point = self.point_map.get(pt.point_id)
        if old_point is not None and old_point.belong_equip_id != pt.belong_equip_id:
            self._points_by_equip[old_point.belong_equip_id].remove(pt.point_id)
        self.point_map[pt.point_id] = pt
        if pt.point_id not in self._points_by_equip[pt.belong_equip_id]:
            self._points_by_equip[pt.belong_equip_id].append(pt.point_id)
        self.graph.add_node(pt.point_id, node_type="point", pt_info=pt.model_dump())

    def add_edge(self, edge: TopoEdge):
        self.edge_map[edge.line_id] = edge
        if edge.end_point:
            self.graph.add_edge(edge.start_point, edge.end_point, edge_info=edge.model_dump())

    def link_device_point(self, equip_id: str, point_id: str):
        if equip_id in self.device_map and point_id in self.point_map:
            self.graph.add_edge(equip_id, point_id, edge_type="terminal")
            
    def get_device_all_points(self, equip_id: str) -> list[str]:
        """获取某设备下属全部端子point_id"""
        return list(self._points_by_equip.get(equip_id, []))

    def get_all_source_equip(self) -> list[str]:
        src_list = []
        for eid, dev in self.device_map.items():
            if dev.is_source:
                src_list.append(eid)
        return src_list


# 新增：设备内部端点连通生成函数（解决导入报错）
def build_device_internal_edges(topo: TopologyGraph, equip_row, term_list: list[str]):
    """
    为单台设备生成内部连通边（完整数值码覆盖 JBS_ZD_OBJECT 字典表。

    内部通路匹配优先级（数值码+中文名+CIM类名三栖兼容：
      1703=配变  1705=断路器 1706=负荷开关 1707=隔离开关
      1708=熔断器 1709=接地刀闸 1710=母线
      0110/0111=变压器  0311=母线
    """
    equip_id = str(equip_row.get("EQUIP_ID", equip_row.get("equip_id", "")))
    equip_type = str(equip_row.get("EQUIP_TYPE", equip_row.get("equip_type", "")))
    if not equip_id or len(term_list) is None:
        return
    term_list = [t for t in term_list if t]
    if len(term_list) < 2:
        return

    t = equip_type.strip()
    sw_numeric = {
        # 开关类：两端直通。
        "1705", "1706", "1707", "1708", "1709",
        "0307", "0201", "0202", "0203", "0302", "0305", "0306", "0309",
    }
    sw_cn = {"断路器", "负荷开关", "隔离开关", "刀闸", "接地刀闸", "熔断器", "组合开关"}
    sw_cim = {"Breaker", "LoadBreakSwitch", "Disconnector",
              "GroundDisconnector", "Fuse", "CompositeSwitch"}
    trafo_numeric = {"1703", "0110", "0111"}
    trafo_cn = {"变压器", "配变", "主变"}
    trafo_cim = {"PowerTransformer"}
    bus_numeric = {"1710", "0311"}
    bus_cn = {"母线"}
    bus_cim = {"BusbarSection"}

    is_switch = (t in sw_numeric) or (t in sw_cn) or (t in sw_cim)
    is_trafo = (t in trafo_numeric) or (t in trafo_cn) or (t in trafo_cim)
    is_bus = (t in bus_numeric) or (t in bus_cn) or (t in bus_cim)

    # 1. 变压器：高压 ↔ 低压（两端子直连；若端子>=2则前两端，若>2则取首末两端子作为高低压）
    if is_trafo:
        pts = sorted(term_list)
        e = TopoEdge(
            line_id=f"INT_TRAFO_{equip_id}",
            start_point=pts[0],
            end_point=pts[-1],
            line_name=f"设备{equip_id}({equip_type})内部变压通路"
        )
        topo.add_edge(e)
        return
    # 2. 开关类：进线端子 ↔ 出线端子（2端子直连，3端子以上全部两两连通（组合开关多通路）
    if is_switch:
        if len(term_list) == 2:
            e = TopoEdge(
                line_id=f"INT_SWITCH_{equip_id}",
                start_point=term_list[0],
                end_point=term_list[1],
                line_name=f"设备{equip_id}内部开关通路"
            )
            topo.add_edge(e)
        else:
            for i in range(len(term_list)):
                for j in range(i + 1, len(term_list)):
                    e = TopoEdge(
                        line_id=f"INT_SW_MULTI_{equip_id}_{i}_{j}",
                        start_point=term_list[i],
                        end_point=term_list[j],
                        line_name=f"多端口开关{equip_id}内部多通路"
                    )
                    topo.add_edge(e)
        return
    # 3. 母线：所有端子两两互通
    if is_bus:
        for i in range(len(term_list)):
            for j in range(i + 1, len(term_list)):
                e = TopoEdge(
                    line_id=f"INT_BUS_{equip_id}_{i}_{j}",
                    start_point=term_list[i],
                    end_point=term_list[j],
                    line_name=f"母线{equip_id}内部连通"
                )
                topo.add_edge(e)
        return
    # 电流/电压互感器、电容器、普通直通负荷类：端子数>=2时两端连通作为默认策略
    if len(term_list) == 2:
        e = TopoEdge(
            line_id=f"INT_PASS_{equip_id}",
            start_point=term_list[0],
            end_point=term_list[1],
            line_name=f"设备{equip_id}默认内部通路"
        )
        topo.add_edge(e)
