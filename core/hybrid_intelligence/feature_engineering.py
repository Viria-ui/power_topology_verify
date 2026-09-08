"""
特征工程模块 (Feature Engineering)
=================================

从拓扑图 + 遥测数据中提取三类特征，供 GNN / 时空模型 / 规则引擎使用：

1. 图结构特征（Graph Features）
   - 节点度、邻居类型分布、介数中心性、PageRank、聚类系数
   - 到最近电源的路径长度（拓扑深度）
   - 连通分量成员资格

2. 设备属性特征（Device Features）
   - 设备类型 equip_type、电压等级、归属馈线
   - 开关状态（合位/分位/未知）
   - ssjg 容器归属（是否为站内开关）

3. 时序统计特征（Telemetry Features）
   - 电流 IA/IB/IC 的均值/标准差/变异系数
   - 有功功率 AP 的滑动均值/波动率
   - 电压 UA/UB/UC 的不平衡度
   - 状态跳变次数（分合位切换）
   - 缺失数据比例
"""

from __future__ import annotations
import logging
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

import numpy as np
import networkx as nx

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# 全局设备类型分组（用于特征计算）
# ------------------------------------------------------------------
SWITCH_TYPES = {"1705", "1706", "1707", "0307", "0201", "0202", "0203", "0209"}
BREAKER_TYPES = {"0307"}
LOAD_SWITCH_TYPES = {"0201", "0209"}
ISOLATOR_TYPES = {"0202", "0203"}
TRANSFORMER_TYPES = {"1041", "1042", "1043", "1044", "1010"}
BUS_TYPES = {"1001", "1002", "1003"}
CAPACITOR_TYPES = {"2101", "2102"}

# ------------------------------------------------------------------
# 特征容器
# ------------------------------------------------------------------

class DeviceFeatures:
    """单个设备的完整特征向量"""

    def __init__(self, equip_id: str):
        self.equip_id = equip_id

        # === 图结构特征 ===
        self.degree: int = 0                      # 节点度（拓扑图中邻居数量）
        self.neighbor_type_diversity: int = 0       # 邻居设备类型种类数
        self.avg_neighbor_degree: float = 0.0      # 邻居平均度
        self.betweenness: float = 0.0              # 介数中心性（拓扑关键性）
        self.pagerank: float = 0.0                 # PageRank 得分
        self.clustering_coef: float = 0.0           # 聚类系数
        self.topo_depth: int = -1                  # 到最近电源的拓扑距离（跳数）
        self.in_same_component: bool = True         # 是否与电源同连通分量
        self.component_size: int = 0               # 所在连通分量大小

        # === 设备属性特征 ===
        self.equip_type: str = ""
        self.voltage_type: str = ""
        self.feeder_id: str = ""
        self.is_source: bool = False
        self.switch_status: str = "UNKNOWN"
        self.is_in_container: bool = False          # 是否位于站房容器内
        self.container_id: str = ""

        # === 时序统计特征 ===
        self.current_ia_mean: float = 0.0
        self.current_ib_mean: float = 0.0
        self.current_ic_mean: float = 0.0
        self.current_std: float = 0.0
        self.voltage_ua: float = 0.0
        self.voltage_ub: float = 0.0
        self.voltage_uc: float = 0.0
        self.voltage_imbalance: float = 0.0        # 三相电压不平衡度
        self.active_power: float = 0.0
        self.reactive_power: float = 0.0
        self.power_factor: float = 0.0
        self.has_telemetry: bool = False           # 是否有遥测数据
        self.telemetry_missing_ratio: float = 0.0  # 数据缺失率

        # === 时序动态特征 ===
        self.status_flapping: bool = False         # 是否频繁分合
        self.current_volatility: float = 0.0       # 电流波动率
        self.power_volatility: float = 0.0         # 功率波动率
        self.trend_slope: float = 0.0              # 功率趋势斜率

        # === GNN 嵌入向量 ===
        self.gnn_embedding: Optional[np.ndarray] = None   # GAT 输出嵌入
        self.gnn_attention_score: float = 0.0            # GAT 异常注意力分数
        self.gnn_anomaly_prob: float = 0.0              # GAT 异常概率

        # === 时空模型输出 ===
        self.temporal_anomaly_score: float = 0.0   # 时序异常分数
        self.temporal_status: str = "NORMAL"       # NORMAL / ANOMALY / MISSING

    # ------------------------------------------------------------------
    # 转为特征向量（供 GNN / 时空模型使用）
    # ------------------------------------------------------------------
    def to_feature_vector(self) -> np.ndarray:
        """将数值特征聚合为固定长度向量（供 PyTorch 使用）"""
        return np.array([
            self.degree,
            self.neighbor_type_diversity,
            self.avg_neighbor_degree,
            self.betweenness,
            self.pagerank,
            self.clustering_coef,
            float(self.topo_depth if self.topo_depth >= 0 else 99),
            float(self.in_same_component),
            float(self.component_size),
            # 设备属性
            1.0 if self.is_source else 0.0,
            1.0 if self.is_in_container else 0.0,
            1.0 if self.has_telemetry else 0.0,
            # 时序
            self.current_ia_mean,
            self.current_ib_mean,
            self.current_ic_mean,
            self.current_std,
            self.voltage_ua,
            self.voltage_ub,
            self.voltage_uc,
            self.voltage_imbalance,
            self.active_power,
            self.reactive_power,
            self.power_volatility,
            self.telemetry_missing_ratio,
        ], dtype=np.float32)

    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "degree": self.degree,
            "topo_depth": self.topo_depth,
            "is_source": self.is_source,
            "has_telemetry": self.has_telemetry,
            "voltage_imbalance": round(self.voltage_imbalance, 4),
            "power_volatility": round(self.power_volatility, 4),
            "gnn_anomaly_prob": round(self.gnn_anomaly_prob, 4),
            "temporal_anomaly_score": round(self.temporal_anomaly_score, 4),
            "gnn_attention_score": round(self.gnn_attention_score, 4),
        }


# ------------------------------------------------------------------
# 主特征工程类
# ------------------------------------------------------------------

class FeatureEngineering:
    """
    从 TopologyGraph + 遥测数据中提取全部特征

    参数:
        topo: TopologyGraph 实例（必须已完成 build_graph_from_terminal）
        telemetry_data: dict — {equip_id: [row, ...]}，时序数据列表
        switch_status_map: dict — {equip_id: "CLOSE"/"OPEN"}
    """

    FEATURE_DIM = 24   # to_feature_vector() 输出维度

    def __init__(
        self,
        topo,               # TopologyGraph
        telemetry_data: Optional[dict] = None,
        switch_status_map: Optional[dict] = None,
    ):
        self.topo = topo
        self.telemetry_data = telemetry_data or {}
        self.switch_status_map = switch_status_map or {}
        self._device_features: Dict[str, DeviceFeatures] = {}
        self._graph_metrics: Optional[dict] = None

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------

    def run_all(self) -> Dict[str, DeviceFeatures]:
        """
        执行全量特征提取（幂等，多次调用直接返回缓存结果）

        返回: {equip_id: DeviceFeatures}
        """
        if self._device_features:
            return self._device_features

        logger.info("[特征工程] 开始提取特征，设备数量=%d", len(self.topo.device_map))

        # Step 1: 图结构指标（一次性批量计算）
        self._compute_graph_metrics()

        # Step 2: 设备属性特征
        self._extract_device_attributes()

        # Step 3: 图结构特征（填充到每个 DeviceFeatures）
        self._extract_graph_features()

        # Step 4: 时序统计特征
        self._extract_telemetry_features()

        # Step 5: 拓扑深度（到电源的路径长度）
        self._compute_topo_depth()

        logger.info(
            "[特征工程] 完成，共提取 %d 个设备特征，遥测覆盖=%d 台",
            len(self._device_features),
            sum(1 for f in self._device_features.values() if f.has_telemetry),
        )
        return self._device_features

    def get_features(self, equip_id: str) -> Optional[DeviceFeatures]:
        """获取单个设备的特征（未执行则自动执行）"""
        if not self._device_features:
            self.run_all()
        return self._device_features.get(equip_id)

    def get_feature_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        获取全局特征矩阵（供 GNN / 时空模型训练使用）
        返回: (N×24 特征矩阵, equip_id 列表)
        """
        if not self._device_features:
            self.run_all()

        ids = list(self._device_features.keys())
        mat = np.stack([self._device_features[eid].to_feature_vector() for eid in ids])
        return mat, ids

    # ------------------------------------------------------------------
    # Step 1: 批量计算图结构指标
    # ------------------------------------------------------------------

    def _compute_graph_metrics(self):
        """一次性计算全图 NetworkX 指标"""
        G = self.topo.graph
        if G.number_of_nodes() == 0:
            self._graph_metrics = {}
            return

        logger.info("[特征工程] 计算图结构指标（节点=%d, 边=%d）",
                    G.number_of_nodes(), G.number_of_edges())

        # 只在设备节点子图上计算（避免端子节点干扰）
        device_nodes = set(self.topo.device_map.keys())
        subG = G.subgraph(device_nodes).copy()

        # 度分布
        degree_dict = dict(subG.degree())

        # 介数中心性（O(N×E)，大图可采样）
        n = subG.number_of_nodes()
        if n <= 500:
            betweenness = nx.betweenness_centrality(subG)
        else:
            logger.warning("[特征工程] 节点数>%d，用采样估计介数中心性", 500)
            betweenness = nx.betweenness_centrality(subG, k=min(100, n))

        # PageRank
        try:
            pagerank = nx.pagerank(subG, max_iter=100)
        except Exception:
            # 节点 ID 是字符串，需要按节点数做兜底，避免 TypeError
            pagerank = {n: 1.0 / max(len(subG.nodes), 1) for n in subG.nodes()}

        # 聚类系数
        clustering = nx.clustering(subG)

        # 连通分量
        components = list(nx.connected_components(subG))
        comp_of_node = {}
        for comp in components:
            for n in comp:
                comp_of_node[n] = comp

        self._graph_metrics = {
            "degree": degree_dict,
            "betweenness": betweenness,
            "pagerank": pagerank,
            "clustering": clustering,
            "components": components,
            "comp_of_node": comp_of_node,
        }

    # ------------------------------------------------------------------
    # Step 2: 设备属性特征
    # ------------------------------------------------------------------

    def _extract_device_attributes(self):
        for equip_id, dev in self.topo.device_map.items():
            feat = DeviceFeatures(equip_id)
            feat.equip_type = dev.equip_type or ""
            feat.voltage_type = dev.voltage_type or ""
            feat.feeder_id = dev.feeder_id or ""
            feat.is_source = dev.is_source
            feat.switch_status = self.switch_status_map.get(
                equip_id,
                dev.switch_status or "UNKNOWN"
            )
            feat.is_in_container = bool(getattr(dev, "ssjg", None))
            feat.container_id = getattr(dev, "ssjg", "") or ""
            self._device_features[equip_id] = feat

    # ------------------------------------------------------------------
    # Step 3: 图结构特征
    # ------------------------------------------------------------------

    def _extract_graph_features(self):
        if not self._graph_metrics:
            return
        G = self.topo.graph
        deg = self._graph_metrics["degree"]
        bet = self._graph_metrics["betweenness"]
        pr = self._graph_metrics["pagerank"]
        clu = self._graph_metrics["clustering"]
        comp_of = self._graph_metrics["comp_of_node"]
        components = self._graph_metrics["components"]

        for equip_id, feat in self._device_features.items():
            if equip_id not in G.nodes:
                continue
            feat.degree = deg.get(equip_id, 0)
            feat.betweenness = bet.get(equip_id, 0.0)
            feat.pagerank = pr.get(equip_id, 0.0)
            feat.clustering_coef = clu.get(equip_id, 0.0)

            # 邻居类型多样性
            neighbors = list(G.neighbors(equip_id))
            neighbor_types = set()
            for n in neighbors:
                if n in self.topo.device_map:
                    dev = self.topo.device_map[n]
                    neighbor_types.add(dev.equip_type or "")
            feat.neighbor_type_diversity = len(neighbor_types)

            # 邻居平均度
            if neighbors:
                neighbor_degrees = [deg.get(n, 0) for n in neighbors]
                feat.avg_neighbor_degree = sum(neighbor_degrees) / len(neighbor_degrees)

            # 连通分量信息
            if equip_id in comp_of:
                comp = comp_of[equip_id]
                feat.component_size = len(comp)
                # 检查是否含电源
                feat.in_same_component = any(
                    self.topo.device_map.get(n, None) and
                    self.topo.device_map[n].is_source
                    for n in comp
                )

    # ------------------------------------------------------------------
    # Step 4: 时序统计特征
    # ------------------------------------------------------------------

    def _extract_telemetry_features(self):
        for equip_id in self._device_features:
            feat = self._device_features[equip_id]
            rows = self._get_telemetry_rows(equip_id)

            if not rows:
                feat.has_telemetry = False
                feat.telemetry_missing_ratio = 1.0
                continue

            feat.has_telemetry = True

            # 电流
            ia_vals = [self._safe_float(r.get("IA", 0)) for r in rows]
            ib_vals = [self._safe_float(r.get("IB", 0)) for r in rows]
            ic_vals = [self._safe_float(r.get("IC", 0)) for r in rows]
            feat.current_ia_mean = self._mean(ia_vals)
            feat.current_ib_mean = self._mean(ib_vals)
            feat.current_ic_mean = self._mean(ic_vals)
            feat.current_std = (
                self._std(ia_vals + ib_vals + ic_vals) if (ia_vals or ib_vals or ic_vals) else 0.0
            )

            # 电压 & 不平衡度
            ua_vals = [self._safe_float(r.get("UA", 0)) for r in rows]
            ub_vals = [self._safe_float(r.get("UB", 0)) for r in rows]
            uc_vals = [self._safe_float(r.get("UC", 0)) for r in rows]
            feat.voltage_ua = self._mean(ua_vals)
            feat.voltage_ub = self._mean(ub_vals)
            feat.voltage_uc = self._mean(uc_vals)
            feat.voltage_imbalance = self._compute_voltage_imbalance(ua_vals, ub_vals, uc_vals)

            # 功率
            ap_vals = [self._safe_float(r.get("AP", 0)) for r in rows]
            rp_vals = [self._safe_float(r.get("RP", 0)) for r in rows]
            feat.active_power = self._mean(ap_vals)
            feat.reactive_power = self._mean(rp_vals)
            if abs(feat.active_power) > 1.0:
                feat.power_factor = min(1.0, abs(feat.active_power) /
                                        (abs(feat.active_power) + abs(feat.reactive_power) + 1e-6))
            # 波动率
            feat.current_volatility = self._cv(ia_vals)
            feat.power_volatility = self._cv(ap_vals)

            # 数据缺失率（以 QUALITY 字段判断）
            total = len(rows)
            missing = sum(1 for r in rows if str(r.get("QUALITY", "1")) == "0")
            feat.telemetry_missing_ratio = missing / max(total, 1)

    # ------------------------------------------------------------------
    # Step 5: 拓扑深度（到电源的最短路径）
    # ------------------------------------------------------------------

    def _compute_topo_depth(self):
        G = self.topo.graph
        source_nodes = [
            e.equip_id for e in self.topo.device_map.values() if e.is_source
        ]
        if not source_nodes:
            logger.warning("[特征工程] 拓扑图中无电源节点，无法计算 topo_depth")
            return

        # BFS 从所有电源同步扩散
        depth = {n: 0 for n in source_nodes}
        queue = list(source_nodes)
        visited = set(source_nodes)

        logger.info("[特征工程] BFS 计算 topo_depth，%d 个电源节点", len(source_nodes))
        while queue:
            cur = queue.pop(0)
            cur_depth = depth[cur]
            for nxt in G.neighbors(cur):
                if nxt not in visited:
                    visited.add(nxt)
                    depth[nxt] = cur_depth + 1
                    queue.append(nxt)

        for equip_id in self._device_features:
            self._device_features[equip_id].topo_depth = depth.get(equip_id, -1)

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _get_telemetry_rows(self, equip_id: str) -> list:
        key = str(equip_id)
        raw = self.telemetry_data.get(key, [])
        if isinstance(raw, dict):
            return [raw]
        return raw if isinstance(raw, list) else []

    @staticmethod
    def _safe_float(v) -> float:
        try:
            return float(v) if v is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _mean(vals: list) -> float:
        v = [x for x in vals if x != 0.0]
        return sum(v) / len(v) if v else 0.0

    @staticmethod
    def _std(vals: list) -> float:
        if not vals:
            return 0.0
        m = sum(vals) / len(vals)
        return (sum((x - m) ** 2 for x in vals) / max(len(vals) - 1, 1)) ** 0.5

    @staticmethod
    def _cv(vals: list) -> float:
        """变异系数 (CV) = std/mean"""
        m = FeatureEngineering._mean(vals)
        if m == 0:
            return 0.0
        return FeatureEngineering._std(vals) / abs(m)

    @staticmethod
    def _compute_voltage_imbalance(ua, ub, uc) -> float:
        vals = [v for v in [FeatureEngineering._mean(ua), FeatureEngineering._mean(ub),
                             FeatureEngineering._mean(uc)] if v > 1.0]
        if len(vals) < 2:
            return 0.0
        un = sum(vals) / len(vals)
        if un < 1.0:
            return 0.0
        return max(abs(v - un) for v in vals) / un
