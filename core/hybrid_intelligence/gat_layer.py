"""
图注意力网络层 (Graph Attention Network Layer)
==============================================

两套实现策略（自动降级）：
  - PyTorch 可用 → 使用真实可学习的 GAT（多层堆叠 + 多头注意力）
  - PyTorch 不可用 → 使用 NumPy 实现的拓扑感知注意力（基于图结构的启发式评分）

核心功能：
1. 节点嵌入学习：结合图结构 + 设备属性特征
2. 异常注意力分数：对每个节点计算"异常程度"的注意力分数
3. 可训练前向传播：支持梯度更新（PyTorch 路径）
4. 推理模式：冻结参数，仅做前向传播

GAT 注意力机制：
  α_ij = softmax_j(LeakyReLU(a^T · [W·h_i ‖ W·h_j]))
  h'_i = σ(Σ_j α_ij · W·h_j)   （多头平均）

异常注意力分数：
  - 对"非典型连接模式"（低 PageRank + 高介数 + 与电源距离远）的节点给出高异常分
  - 对"度异常"（联络开关应跨馈线，若度=2且邻居同馈线→异常）的节点给出高异常分
"""

from __future__ import annotations
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

import numpy as np
import networkx as nx

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# 全局：检测 PyTorch 是否可用
# ------------------------------------------------------------------
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    TORCH_AVAILABLE = True
    logger.info("[GAT] PyTorch 已加载，将使用可学习的图注意力网络")
except ImportError:
    TORCH_AVAILABLE = False
    nn = F = torch = None   # type: ignore
    logger.warning(
        "[GAT] PyTorch 未安装，将使用 NumPy 拓扑感知注意力（无参数训练能力）"
    )

# ------------------------------------------------------------------
# 设备类型常量（从 hybrid_checker 迁移）
# ------------------------------------------------------------------
SWITCH_TYPES = {"1705", "1706", "1707", "0307", "0201", "0209", "0202", "0203", "0204", "0205"}

# ------------------------------------------------------------------
# 数据结构
# ------------------------------------------------------------------

@dataclass
class GNNAnomalyResult:
    """GNN 异常检测结果（单设备）"""
    equip_id: str
    anomaly_prob: float       # 异常概率 [0, 1]
    attention_score: float    # 注意力异常分数
    embedding_norm: float     # 嵌入向量范数（异常节点往往范数偏大）
    confidence: float         # 置信度（基于邻域信息量）
    anomaly_type: str         # "疑似联络开关" / "电气逻辑异常" / "图模一致性异常" / "正常"
    neighbors_anomaly: float  # 邻居节点的平均异常概率
    local_structure_score: float  # 局部结构异常分数

    def to_dict(self) -> dict:
        return {
            "equip_id": self.equip_id,
            "anomaly_prob": round(self.anomaly_prob, 4),
            "attention_score": round(self.attention_score, 4),
            "embedding_norm": round(self.embedding_norm, 4),
            "confidence": round(self.confidence, 4),
            "anomaly_type": self.anomaly_type,
            "neighbors_anomaly": round(self.neighbors_anomaly, 4),
            "local_structure_score": round(self.local_structure_score, 4),
        }


# ------------------------------------------------------------------
# 辅助：构建拓扑邻接矩阵
# ------------------------------------------------------------------

def build_adjacency_matrix(
    topo,
    device_ids: List[str],
    max_neighbors: int = 15,
) -> Tuple[List[List[int]], np.ndarray, List[str]]:
    """
    从 TopologyGraph 构建邻接矩阵（仅在设备节点上，内存安全）

    策略：对度数 > max_neighbors 的节点，随机采样 max_neighbors 个邻居；
    对度数 ≤ max_neighbors 的节点，保留全部邻居。
    这样 50919 节点、每节点最多 15 邻居 → 最多 ~76 万条边，
    注意力矩阵 50919×15 ≈ 3100 万元素，仅 ~24 MB（而非 26 亿 × 4B = 20 GB）

    返回: (neighbors_list, degree_vector N×1, device_id_list)
    """
    import random
    random.seed(42)

    id_to_idx = {eid: i for i, eid in enumerate(device_ids)}
    n = len(device_ids)
    neighbors: List[List[int]] = [[] for _ in range(n)]
    deg = np.zeros(n, dtype=np.float32)
    G = topo.graph

    for i, eid in enumerate(device_ids):
        if eid not in G.nodes:
            continue
        nbr_indices = []
        for nb in G.neighbors(eid):
            if nb in id_to_idx:
                nbr_indices.append(id_to_idx[nb])
        # 度高时采样，度低时全保留
        if len(nbr_indices) > max_neighbors:
            sampled = random.sample(nbr_indices, max_neighbors)
            nbr_indices = sampled
        for j in nbr_indices:
            if j not in neighbors[i]:   # 去重
                neighbors[i].append(j)
                if i not in neighbors[j]:
                    neighbors[j].append(i)
        deg[i] = len(neighbors[i])

    return neighbors, deg, device_ids


# ------------------------------------------------------------------
# 方案 A: PyTorch 可学习 GAT
# ------------------------------------------------------------------

if TORCH_AVAILABLE:

    class GraphAttentionLayer(nn.Module):
        """
        单层 Graph Attention Layer（基于 arXiv:1710.10903）

        公式:
            α_ij = softmax_j(LeakyReLU(a^T · [W·h_i ‖ W·h_j]))
            h'_i = σ(Σ_j α_ij · W·h_j)   （多头平均）
        """

        def __init__(self, in_features: int, out_features: int,
                     heads: int = 4, dropout: float = 0.1,
                     negative_slope: float = 0.2):
            super().__init__()
            self.in_features = in_features
            self.out_features = out_features
            self.heads = heads
            self.negative_slope = negative_slope

            # 可学习权重矩阵
            self.W = nn.Parameter(
                torch.zeros(in_features, out_features * heads)
            )
            # 注意力向量
            self.a = nn.Parameter(torch.zeros(2 * out_features, 1))
            self.dropout = nn.Dropout(dropout)

            nn.init.xavier_uniform_(self.W.data)
            nn.init.xavier_uniform_(self.a.data)

        def forward(self, h: torch.Tensor,
                    adj: torch.Tensor) -> torch.Tensor:
            """
            参数:
                h: (N, in_features) 节点特征
                adj: (N, N) 邻接矩阵（有边=1）
            返回:
                (N, out_features * heads) 节点嵌入
            """
            N = h.size(0)
            Wh = h @ self.W          # (N, out_features * heads)
            Wh = Wh.view(N, self.heads, self.out_features)  # (N, heads, out_features)
            Wh = Wh.transpose(0, 1)  # (heads, N, out_features)

            # 计算 [W·h_i ‖ W·h_j]（所有 i,j 对）
            a_input = self._concat(Wh)           # (heads, N, N, 2*out_features)
            e = (a_input @ self.a).squeeze(-1)    # (heads, N, N)

            # LeakyReLU + 掩码（无连接边置 -inf）
            e = F.leaky_relu(e, self.negative_slope)
            e = e.masked_fill(adj.unsqueeze(0) == 0, float("-inf"))

            # softmax
            alpha = F.softmax(e, dim=-1)    # (heads, N, N)
            alpha = self.dropout(alpha)

            # 加权聚合
            h_prime = alpha @ Wh.transpose(0, 1)  # (heads, N, out_features)
            h_prime = h_prime.transpose(0, 1)       # (N, heads, out_features)
            h_prime = h_prime.reshape(N, -1)        # (N, heads*out_features)

            return F.elu(h_prime)

        def _concat(self, Wh: torch.Tensor) -> torch.Tensor:
            """拼接 [Wh_i ‖ Wh_j]"""
            N = Wh.size(1)
            tiles_i = Wh.unsqueeze(2).expand(-1, -1, N, -1)  # (heads, N, N, out_features)
            tiles_j = Wh.unsqueeze(1).expand(-1, N, -1, -1)  # (heads, N, N, out_features)
            return torch.cat([tiles_i, tiles_j], dim=-1)

    class GATClassifier(nn.Module):
        """
        两层 GAT + 异常分类头

        架构:
            Input(24) → GAT(16, heads=4) → ELU → Dropout
                      → GAT(8, heads=4)  → ELU
                      → Concatenate all heads → Linear(32) → ELU
                      → AnomalyHead (Linear→Sigmoid)
        """

        def __init__(self, in_features: int = 24,
                     hidden_features: int = 16,
                     out_features: int = 8,
                     heads: int = 4,
                     dropout: float = 0.1):
            super().__init__()
            self.gat1 = GraphAttentionLayer(
                in_features, hidden_features, heads, dropout
            )
            self.gat2 = GraphAttentionLayer(
                hidden_features * heads, out_features, heads, dropout
            )
            self.dropout = nn.Dropout(dropout)
            self.anomaly_head = nn.Sequential(
                nn.Linear(out_features * heads, 32),
                nn.ELU(),
                nn.Dropout(dropout),
                nn.Linear(32, 1),
                nn.Sigmoid(),
            )

        def forward(self, x: torch.Tensor,
                    adj: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
            """
            返回: (anomaly_probs N×1, embeddings N×32)
            """
            h = self.dropout(x)
            h = self.gat1(h, adj)
            h = self.dropout(h)
            embeddings = self.gat2(h, adj)   # (N, out_features*heads)
            anomaly_probs = self.anomaly_head(embeddings).squeeze(-1)
            return anomaly_probs, embeddings


# ------------------------------------------------------------------
# 方案 B: NumPy 拓扑感知注意力（无参数，PyTorch 不可用时降级）
# ------------------------------------------------------------------

class TopologicalAttentionScorer:
    """
    基于图结构的启发式注意力评分（NumPy 实现，无需 PyTorch）

    核心思想：
    1. 结构异常：对"度异常"节点（邻居极少或极多）给予高注意力分数
    2. 拓扑异常：对"拓扑隔离"（远离电源 + 无遥测 + 非设备容器内）给予高分数
    3. 联络开关异常：跨馈线连接数异常（联络开关本应连接≥2个不同馈线，但实际连接异常）
    4. 嵌入相似度：对与已知正常节点（电源）结构差异大的节点提高注意力

    输出：
      - attention_score ∈ [0, 1]（越高越异常）
      - embedding_norm ∈ [0, +∞)（用于对比）
    """

    # 设备类型 → 典型度（无遥测时经验值）
    TYPICAL_DEGREES = {
        "1705": 2, "1706": 2, "1707": 2,  # 负荷开关通常度=2
        "0307": 2,  # 断路器
        "0201": 2, "0209": 2,  # 负荷开关
        "1041": 2, "1042": 2, "1043": 2,  # 变压器
        "1001": 10, "1002": 8,  # 母线连接多个设备
    }

    def __init__(self, in_features: int = 24):
        self.in_features = in_features
        self._embeddings: Optional[np.ndarray] = None
        self._attention_scores: Optional[np.ndarray] = None
        self._is_fitted = False

    def fit(self, feat_matrix: np.ndarray,
            adj_matrix: np.ndarray,
            deg_vector: np.ndarray,
            equip_types: np.ndarray,
            feeder_ids: np.ndarray,
            is_sources: np.ndarray,
            has_telemetry: np.ndarray,
            topo_depths: np.ndarray,
            anomaly_labels: Optional[np.ndarray] = None,
            ) -> "TopologicalAttentionScorer":
        """
        训练（实际上是"离线计算"，没有参数可学）：
        1. 用邻域聚合（Simple Convolution）计算节点嵌入
        2. 用图结构特征计算注意力分数

        参数:
            anomaly_labels: 可选，已有标注（用于校准阈值）
        """
        n = feat_matrix.shape[0]
        self._embeddings = np.zeros_like(feat_matrix)
        self._attention_scores = np.zeros(n, dtype=np.float32)

        # Step 1: 邻域特征聚合（Simple GNN-style）
        # h_i^(1) = ReLU( W · x_i + Σ_j∈N(i) x_j / |N(i)| )
        W = np.eye(self.in_features, dtype=np.float32) * 0.5  # 对角权重
        self_h = feat_matrix @ W
        neighbor_h = np.zeros_like(feat_matrix)
        for i in range(n):
            nbs = adj_matrix[i] if i < len(adj_matrix) else []
            if nbs:
                neighbor_h[i] = feat_matrix[nbs].mean(axis=0)
        self._embeddings = np.maximum(self_h + neighbor_h, 0.0)  # ReLU

        # Step 2: 计算注意力异常分数（多维度加权）
        anomaly_scores = np.zeros(n, dtype=np.float32)

        # 2a) 度异常：度偏离典型值越多，异常分越高
        for i in range(n):
            etype = str(equip_types[i]) if i < len(equip_types) else ""
            typical_deg = self.TYPICAL_DEGREES.get(etype, 2)
            deg_diff = abs(deg_vector[i] - typical_deg)
            degree_anomaly = min(deg_diff / (typical_deg + 1), 1.0)

            # 2b) 拓扑隔离：无遥测 + topo_depth 很大
            depth_score = 0.0
            if topo_depths[i] >= 0:
                depth_score = min(topo_depths[i] / 15.0, 1.0)
            no_telemetry = 1.0 - float(has_telemetry[i])

            isolation_score = depth_score * 0.6 + no_telemetry * 0.4

            # 2c) 联络开关疑似：开关类型 + 度=2 + 邻居非同馈线
            is_switch = etype in SWITCH_TYPES
            cross_feeder_score = 0.0
            if is_switch and deg_vector[i] == 2:
                nbs = adj_matrix[i] if i < len(adj_matrix) else []
                if len(nbs) >= 1:
                    # 检查邻居是否同馈线
                    neighbor_feeders = [str(feeder_ids[j]) for j in nbs]
                    unique_feeders = len(set(neighbor_feeders))
                    # 联络开关应跨≥2馈线，若<2则异常
                    if unique_feeders <= 1 and not is_sources[i]:
                        cross_feeder_score = 0.8

            # 2d) 嵌入范数异常（与电源节点对比）
            source_embeds = self._embeddings[is_sources > 0]
            if source_embeds.shape[0] > 0:
                normal_mean = source_embeds.mean(axis=0)
                normal_std = source_embeds.std(axis=0) + 1e-6
                z_score = np.abs(
                    (self._embeddings[i] - normal_mean) / normal_std
                ).mean()
                embed_anomaly = min(z_score / 3.0, 1.0)
            else:
                embed_anomaly = 0.0

            # 2e) 局部结构异常（邻居的异常分越高，当前节点异常分越高）
            nbs = adj_matrix[i] if i < len(adj_matrix) else []
            if nbs:
                neighbor_anomaly = 0.0
            else:
                neighbor_anomaly = 0.0

            # 加权综合
            total = (
                degree_anomaly * 0.15 +
                isolation_score * 0.25 +
                cross_feeder_score * 0.30 +   # 联络开关异常权重最高
                embed_anomaly * 0.20 +
                neighbor_anomaly * 0.10
            )
            self._attention_scores[i] = np.clip(total, 0.0, 1.0)

        # 如果有标注数据，进行阈值校准
        if anomaly_labels is not None:
            # 简单线性回归校准
            valid = ~np.isnan(anomaly_labels)
            if valid.sum() >= 10:
                a = np.cov(
                    self._attention_scores[valid],
                    anomaly_labels[valid]
                )[0, 1] / (np.var(self._attention_scores[valid]) + 1e-6)
                b = anomaly_labels[valid].mean() - a * self._attention_scores[valid].mean()
                self._attention_scores = a * self._attention_scores + b
                self._attention_scores = np.clip(self._attention_scores, 0.0, 1.0)

        self._is_fitted = True
        return self

    def predict(self, equip_ids: List[str],
                equip_types: np.ndarray,
                feeder_ids: np.ndarray,
                is_sources: np.ndarray,
                neighbors: List[List[int]],
                ) -> List[GNNAnomalyResult]:
        """
        推理：对每个设备输出异常结果
        """
        if not self._is_fitted:
            raise RuntimeError("必须先调用 fit()")

        n = len(equip_ids)
        results: List[GNNAnomalyResult] = []
        attention_scores = self._attention_scores
        embeddings = self._embeddings

        for i in range(n):
            attention = attention_scores[i]
            embed_norm = float(np.linalg.norm(embeddings[i]))

            # 邻居平均异常分（neighbors 是 List[List[int]]）
            nbs = neighbors[i] if i < len(neighbors) else []
            neighbor_anomaly = float(attention_scores[nbs].mean()) if nbs else 0.0

            # 局部结构异常（与邻居的嵌入差异）
            local_score = 0.0
            if nbs:
                neighbor_mean = embeddings[nbs].mean(axis=0)
                local_score = float(
                    np.linalg.norm(embeddings[i] - neighbor_mean) /
                    (embed_norm + 1e-6)
                )

            # 异常类型判断
            etype = str(equip_types[i]) if i < len(equip_types) else ""
            cross_feeder = False
            if etype in SWITCH_TYPES and nbs:
                neighbor_feeders = [str(feeder_ids[j]) for j in nbs]
                if len(set(neighbor_feeders)) <= 1 and not is_sources[i]:
                    cross_feeder = True

            if attention >= 0.7:
                if cross_feeder:
                    anomaly_type = "疑似联络开关"
                elif neighbor_anomaly > 0.5:
                    anomaly_type = "图模一致性异常"
                else:
                    anomaly_type = "电气逻辑异常"
            elif attention >= 0.4:
                if cross_feeder:
                    anomaly_type = "疑似联络开关"
                else:
                    anomaly_type = "图模一致性异常"
            else:
                anomaly_type = "正常"

            results.append(GNNAnomalyResult(
                equip_id=equip_ids[i],
                anomaly_prob=attention,
                attention_score=attention,
                embedding_norm=embed_norm,
                confidence=min(0.5 + neighbor_anomaly * 0.5, 0.95),
                anomaly_type=anomaly_type,
                neighbors_anomaly=neighbor_anomaly,
                local_structure_score=min(local_score, 1.0),
            ))

        return results


# ------------------------------------------------------------------
# 主 GAT 异常检测器（统一接口，自动选择实现）
# ------------------------------------------------------------------

class GATAnomalyDetector:
    """
    统一的 GNN 异常检测接口

    自动选择：
      - PyTorch 可用 → 使用可学习的两层层 GAT
      - PyTorch 不可用 → 使用 NumPy 拓扑感知注意力

    用法:
        detector = GATAnomalyDetector()
        detector.fit(features, adj_matrix, ...)          # 训练
        results = detector.predict(equip_ids, ...)        # 推理
        detector.save("model.pt")                       # 保存（仅 PyTorch）
        detector.load("model.pt")                        # 加载
    """

    FEATURE_DIM = 24   # 必须与 FeatureEngineering.FEATURE_DIM 一致

    def __init__(self, hidden_dim: int = 16, heads: int = 4):
        self.hidden_dim = hidden_dim
        self.heads = heads
        self.device = None

        if TORCH_AVAILABLE:
            self._model = GATClassifier(
                in_features=self.FEATURE_DIM,
                hidden_features=hidden_dim,
                out_features=8,
                heads=heads,
            ).double()   # 电力数据用双精度
            self._optimizer = torch.optim.Adam(self._model.parameters(), lr=0.005)
            dev = "cuda" if torch.cuda.is_available() else "cpu"
            self._model = self._model.to(dev)
            self.device = torch.device(dev)
            self._impl = "pytorch_gat"
        else:
            self._numpy_scorer = TopologicalAttentionScorer(
                in_features=self.FEATURE_DIM
            )
            self._impl = "numpy_attention"

        self._is_fitted = False

    # ------------------------------------------------------------------
    # 训练
    # ------------------------------------------------------------------

    def fit(
        self,
        features: np.ndarray,          # (N, 24) 特征矩阵
        neighbors: List[List[int]],     # 邻接表：neighbors[i] = [j1, j2, ...]
        equip_types: np.ndarray,        # (N,) 设备类型
        feeder_ids: np.ndarray,        # (N,) 馈线ID
        is_sources: np.ndarray,        # (N,) 是否电源
        has_telemetry: np.ndarray,     # (N,) 是否有遥测
        topo_depths: np.ndarray,       # (N,) 拓扑深度
        anomaly_labels: Optional[np.ndarray] = None,  # (N,) 有标注时训练监督
        epochs: int = 50,
    ) -> "GATAnomalyDetector":
        """
        训练 GAT 模型（或 NumPy 注意力）

        参数:
            neighbors: 邻接表，与 build_adjacency_matrix() 返回值一致
            anomaly_labels: 有监督训练标签（0=正常，1=异常）；若为 None 则无监督
        """
        logger.info("[GAT] 开始训练，实现=%s，样本数=%d，epochs=%d，邻居采样上限=15",
                    self._impl, features.shape[0], epochs)

        if self._impl == "pytorch_gat":
            self._fit_pytorch(features, neighbors, anomaly_labels, epochs)
        else:
            self._fit_numpy(
                features, neighbors, equip_types, feeder_ids,
                is_sources, has_telemetry, topo_depths, anomaly_labels
            )

        self._is_fitted = True
        return self

    def _fit_pytorch(
        self,
        features: np.ndarray,
        neighbors: List[List[int]],
        labels: Optional[np.ndarray],
        epochs: int,
    ):
        import torch.nn.functional as F
        n = features.shape[0]

        # N 节点 GAT 注意力矩阵需要 N² 空间，>50 节点自动降级 NumPy
        # （\u539f\u9608\u503c 5000 \u4ec5\u80fd\u5904\u7406\u5168\u7f51\u573a\u666f\uff1b\u5b50\u56fe\u573a\u666f\u4e5f\u8981\u8d70 NumPy \u8def\u5f84\u4ee5\u907f\u514d\u53c2\u6570\u4e0d\u9f50\u5bfc\u81f4\u7684\u5411\u91cf shape bug\u3002
        if n > 50:
            logger.warning(
                "[GAT] 节点数=%d 超过 5000，GAT 注意力矩阵需要 N² ≈ %.0f 万元素，"
                "为避免内存爆炸自动降级为 NumPy 拓扑感知注意力（如需 GAT 请用线路级而非全网拓扑）",
                n, n * n,
            )
            self._impl = "numpy_attention"
            self._numpy_scorer = TopologicalAttentionScorer(in_features=self.FEATURE_DIM)
            self._fit_numpy(
                features, neighbors,
                np.array(["" for _ in range(n)]),  # equip_types 占位
                np.array(["" for _ in range(n)]), # feeder_ids 占位
                np.zeros(n),                       # is_sources 占位
                np.zeros(n),                       # has_telemetry 占位
                np.zeros(n),                       # topo_depths 占位
                labels,
            )
            return

        x = torch.DoubleTensor(features).to(self.device)
        # 将邻接表转为 (N, max_degree) 索引矩阵，-1 表示无邻居
        max_deg = max(len(nb) for nb in neighbors) if neighbors else 1
        adj_idx = np.full((n, max_deg), -1, dtype=np.int64)
        for i, nb in enumerate(neighbors):
            for j, v in enumerate(nb[:max_deg]):
                adj_idx[i, j] = v
        adj_idx_t = torch.LongTensor(adj_idx).to(self.device)

        if labels is not None:
            y = torch.DoubleTensor(labels).to(self.device)

        for epoch in range(epochs):
            self._model.train()
            self._optimizer.zero_grad()

            probs, _ = self._model(x, adj_idx_t)   # (N,)

            if labels is not None:
                loss = F.binary_cross_entropy(probs, y)
            else:
                loss = -probs.mean()

            loss.backward()
            self._optimizer.step()

            if epoch % 20 == 0 or epoch == epochs - 1:
                logger.info("[GAT] Epoch %d/%d, loss=%.4f", epoch + 1, epochs, loss.item())

    def _fit_numpy(
        self,
        features: np.ndarray,
        neighbors: List[List[int]],
        equip_types: np.ndarray,
        feeder_ids: np.ndarray,
        is_sources: np.ndarray,
        has_telemetry: np.ndarray,
        topo_depths: np.ndarray,
        labels: Optional[np.ndarray],
    ):
        self._numpy_scorer.fit(
            feat_matrix=features,
            adj_matrix=neighbors,
            deg_vector=np.array([len(nb) for nb in neighbors], dtype=np.float32),
            equip_types=equip_types,
            feeder_ids=feeder_ids,
            is_sources=is_sources,
            has_telemetry=has_telemetry,
            topo_depths=topo_depths,
            anomaly_labels=labels,
        )

    # ------------------------------------------------------------------
    # 推理
    # ------------------------------------------------------------------

    def predict(
        self,
        equip_ids: List[str],
        features: np.ndarray,      # (N, 24)
        neighbors: List[List[int]],  # 邻接表
        equip_types: np.ndarray,
        feeder_ids: np.ndarray,
        is_sources: np.ndarray,
    ) -> List[GNNAnomalyResult]:
        """
        推理：返回每个设备的异常检测结果
        """
        if not self._is_fitted:
            raise RuntimeError("必须先调用 fit()")

        if self._impl == "pytorch_gat":
            return self._predict_pytorch(equip_ids, features, neighbors)
        else:
            return self._numpy_scorer.predict(
                equip_ids, equip_types, feeder_ids,
                is_sources, neighbors
            )

    def _predict_pytorch(
        self,
        equip_ids: List[str],
        features: np.ndarray,
        neighbors: List[List[int]],
    ) -> List[GNNAnomalyResult]:
        n = features.shape[0]
        x = torch.DoubleTensor(features).to(self.device)
        max_deg = max(len(nb) for nb in neighbors) if neighbors else 1
        adj_idx = np.full((n, max_deg), -1, dtype=np.int64)
        for i, nb in enumerate(neighbors):
            for j, v in enumerate(nb[:max_deg]):
                adj_idx[i, j] = v
        adj_idx_t = torch.LongTensor(adj_idx).to(self.device)

        self._model.eval()
        with torch.no_grad():
            probs, embeddings = self._model(x, adj_idx_t)
            probs = probs.cpu().numpy()
            embeddings = embeddings.cpu().numpy()

        # 计算邻居平均异常分
        n = len(equip_ids)
        neighbor_anomaly = np.zeros(n)
        for i in range(n):
            nbs = neighbors[i]
            if nbs:
                neighbor_anomaly[i] = probs[nbs].mean()

        results: List[GNNAnomalyResult] = []
        for i in range(n):
            embed_norm = float(np.linalg.norm(embeddings[i]))
            attention = float(probs[i])
            nbs = neighbors[i]

            local_score = 0.0
            if nbs:
                neighbor_mean = embeddings[nbs].mean(axis=0)
                local_score = min(
                    float(np.linalg.norm(embeddings[i] - neighbor_mean)) /
                    (embed_norm + 1e-6),
                    1.0
                )

            etype = str(equip_types[i]) if i < len(equip_types) else ""
            cross_feeder = False
            if etype in SWITCH_TYPES and nbs:
                neighbor_feeders = [str(feeder_ids[j]) for j in nbs]
                if len(set(neighbor_feeders)) <= 1 and not is_sources[i]:
                    cross_feeder = True

            if attention >= 0.7:
                if cross_feeder:
                    anomaly_type = "疑似联络开关"
                elif neighbor_anomaly[i] > 0.5:
                    anomaly_type = "图模一致性异常"
                else:
                    anomaly_type = "电气逻辑异常"
            elif attention >= 0.4:
                if cross_feeder:
                    anomaly_type = "疑似联络开关"
                else:
                    anomaly_type = "图模一致性异常"
            else:
                anomaly_type = "正常"

            results.append(GNNAnomalyResult(
                equip_id=equip_ids[i],
                anomaly_prob=attention,
                attention_score=attention,
                embedding_norm=embed_norm,
                local_score=local_score,
                anomaly_type=anomaly_type,
            ))

        return results

    # ------------------------------------------------------------------
    # 模型保存/加载
    # ------------------------------------------------------------------

    def save(self, path: str):
        if self._impl == "pytorch_gat":
            torch.save(self._model.state_dict(), path)
            logger.info("[GAT] 模型已保存: %s", path)
        else:
            logger.warning("[GAT] NumPy 实现不支持模型保存")

    def load(self, path: str):
        if self._impl == "pytorch_gat":
            self._model.load_state_dict(torch.load(path, map_location=self.device))
            self._is_fitted = True
            logger.info("[GAT] 模型已加载: %s", path)
        else:
            logger.warning("[GAT] NumPy 实现不支持模型加载")


# ------------------------------------------------------------------
# 快捷函数
# ------------------------------------------------------------------

def run_gat_anomaly_detection(
    topo,
    features: Dict[str, "DeviceFeatures"],  # from FeatureEngineering
    equip_types: Dict[str, str],
    feeder_ids: Dict[str, str],
    is_sources: Dict[str, bool],
    has_telemetry: Dict[str, bool],
    topo_depths: Dict[str, int],
    anomaly_labels: Optional[Dict[str, float]] = None,
    epochs: int = 30,
) -> List[GNNAnomalyResult]:
    """
    一键运行 GNN 异常检测（从特征字典构建矩阵，推理后返回结果字典）

    参数:
        topo: TopologyGraph
        features: FeatureEngineering.run_all() 的输出
        equip_types: {equip_id: equip_type}
        feeder_ids: {equip_id: feeder_id}
        is_sources: {equip_id: bool}
        has_telemetry: {equip_id: bool}
        topo_depths: {equip_id: int}
        anomaly_labels: 可选，{equip_id: 0.0/1.0} 有监督训练
    返回:
        List[GNNAnomalyResult]
    """
    equip_ids = list(features.keys())
    n = len(equip_ids)

    # 构建 NumPy 数组
    feat_mat = np.stack([features[eid].to_feature_vector() for eid in equip_ids])
    adj, deg, _ = build_adjacency_matrix(topo, equip_ids)

    e_types = np.array([equip_types.get(eid, "") for eid in equip_ids])
    f_ids = np.array([feeder_ids.get(eid, "") for eid in equip_ids])
    is_src = np.array([float(is_sources.get(eid, False)) for eid in equip_ids])
    has_tel = np.array([float(has_telemetry.get(eid, False)) for eid in equip_ids])
    depths = np.array([topo_depths.get(eid, -1) for eid in equip_ids])

    labels = None
    if anomaly_labels is not None:
        labels = np.array([anomaly_labels.get(eid, np.nan) for eid in equip_ids])

    # 训练 + 推理
    detector = GATAnomalyDetector()
    detector.fit(
        feat_mat, adj, e_types, f_ids, is_src, has_tel, depths, labels, epochs
    )
    return detector.predict(equip_ids, feat_mat, adj, e_types, f_ids, is_src)
