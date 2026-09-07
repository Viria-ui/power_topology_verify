"""
混合智能校验器 (Hybrid Intelligence Checker)
==========================================

主入口：整合"拓扑图算法 + GNN 图注意力 + 时空模型 + 规则约束"四路，
统一输出综合异常报告。

使用方式:
    checker = HybridIntelligenceChecker(
        topo=topo,
        telemetry_data=telemetry_data,
        svg_document=svg_doc,
        switch_status_map=switch_status_map,
    )
    report = checker.run_all_checks()
    print(report["summary"])

架构:
    ┌─────────────────────────────────────────┐
    │          HybridIntelligenceChecker       │
    │                                         │
    │  ① FeatureEngineering                  │
    │     (拓扑图+遥测 → 特征向量)            │
    │           ↓                            │
    │  ② GNN + 时空 + 规则 并行执行           │
    │     ┌────────┐  ┌──────────┐  ┌─────┐  │
    │     │  GAT   │  │时空模型  │  │规则 │  │
    │     │(独立)  │  │(独立)    │  │引擎 │  │
    │     └────────┘  └──────────┘  └─────┘  │
    │           ↓            ↓          ↓      │
    │  ③ FusionLayer (三路加权融合)            │
    │           ↓                            │
    │  ④ 统一报告输出                         │
    └─────────────────────────────────────────┘
"""

from __future__ import annotations
import logging
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

from .feature_engineering import FeatureEngineering, DeviceFeatures
from .gat_layer import GATAnomalyDetector, GNNAnomalyResult, run_gat_anomaly_detection
from .spatio_temporal import SpatioTemporalDetector, TemporalAnomalyResult
from .rule_engine import HybridRuleEngine, RuleHit
from .fusion_layer import FusionLayer, FusionResult, FusionSummary

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# 报告数据结构
# ------------------------------------------------------------------

@dataclass
class HybridCheckReport:
    """混合智能校验完整报告"""
    line_name: str
    total_devices: int
    duration_seconds: float

    # 特征工程统计
    features_extracted: int
    telemetry_coverage: int
    gnn_enabled: bool
    temporal_enabled: bool

    # 各路结果统计
    gnn_anomaly_count: int
    temporal_anomaly_count: int
    rule_hit_count: int
    rule_deterministic_count: int
    fused_anomaly_count: int

    # 高风险统计
    high_risk_count: int
    medium_risk_count: int
    confirmed_count: int
    need_review_count: int

    # 最终融合结果
    fusion_summary: dict

    # 各路详细结果（按设备，存 .to_dict() 序列化结果）
    gnn_results: List[dict]
    temporal_results: List[dict]
    rule_hits: List[dict]
    fusion_results: List[dict]

    # 赛题重点关注结果
    suspected_tie_switches: List[dict]   # 疑似联络开关
    electrical_anomalies: List[dict]      # 电气逻辑异常
    graph_model_anomalies: List[dict]     # 图模一致性异常

    def to_dict(self) -> dict:
        return {
            "line_name": self.line_name,
            "total_devices": self.total_devices,
            "duration_seconds": round(self.duration_seconds, 2),
            "features_extracted": self.features_extracted,
            "telemetry_coverage": self.telemetry_coverage,
            "gnn_enabled": self.gnn_enabled,
            "temporal_enabled": self.temporal_enabled,
            "gnn_anomaly_count": self.gnn_anomaly_count,
            "temporal_anomaly_count": self.temporal_anomaly_count,
            "rule_hit_count": self.rule_hit_count,
            "rule_deterministic_count": self.rule_deterministic_count,
            "fused_anomaly_count": self.fused_anomaly_count,
            "high_risk_count": self.high_risk_count,
            "medium_risk_count": self.medium_risk_count,
            "confirmed_count": self.confirmed_count,
            "need_review_count": self.need_review_count,
            "fusion_summary": self.fusion_summary,
            "suspected_tie_switches": self.suspected_tie_switches,
            "electrical_anomalies": self.electrical_anomalies,
            "graph_model_anomalies": self.graph_model_anomalies,
        }


# ------------------------------------------------------------------
# 主校验器
# ------------------------------------------------------------------

class HybridIntelligenceChecker:
    """
    混合智能校验器

    参数:
        line_name: 线路名称（如 "LINE215"）
        topo: TopologyGraph 实例
        telemetry_data: {equip_id: [row, ...]} 遥测数据
        svg_document: SvgDocument 实例（可选）
        switch_status_map: {equip_id: "CLOSE"/"OPEN"} 开关状态（可选）
        enable_gnn: 是否启用 GNN 检测（默认 True）
        enable_temporal: 是否启用时空模型（默认 True）
        gat_epochs: GNN 训练轮数（默认 30）
    """

    def __init__(
        self,
        line_name: str,
        topo,                      # TopologyGraph
        telemetry_data: Optional[dict] = None,
        svg_document=None,          # SvgDocument（可选）
        switch_status_map: Optional[dict] = None,
        enable_gnn: bool = True,
        enable_temporal: bool = True,
        gat_epochs: int = 30,
    ):
        self.line_name = line_name
        self.topo = topo
        self.telemetry_data = telemetry_data or {}
        self.svg_doc = svg_document
        self.switch_status_map = switch_status_map or {}
        self.enable_gnn = enable_gnn
        self.enable_temporal = enable_temporal
        self.gat_epochs = gat_epochs

        self._feature_eng: Optional[FeatureEngineering] = None
        self._gat_detector: Optional[GATAnomalyDetector] = None
        self._temporal_detector: Optional[SpatioTemporalDetector] = None
        self._rule_engine: Optional[HybridRuleEngine] = None
        self._fusion_layer: Optional[FusionLayer] = None

        self._gnn_results: List[GNNAnomalyResult] = []
        self._temporal_results: List[TemporalAnomalyResult] = []
        self._rule_hits: List[RuleHit] = []
        self._fusion_summary: Optional[FusionSummary] = None

    # ==================================================================
    # 公共接口
    # ==================================================================

    def run_all_checks(self) -> HybridCheckReport:
        """
        执行全量混合智能校验（幂等）

        返回: HybridCheckReport
        """
        t0 = time.time()
        logger.info(
            "[混合智能] ====== 开始混合智能校验: %s ======",
            self.line_name,
        )

        # Step 1: 特征工程（所有路共享）
        self._run_feature_engineering()

        # Step 2: 三路并行执行
        if self.enable_gnn:
            self._run_gnn_detection()
        if self.enable_temporal:
            self._run_temporal_detection()
        self._run_rule_engine()

        # Step 3: 融合决策
        self._run_fusion()

        # Step 4: 生成报告
        report = self._build_report(time.time() - t0)

        logger.info(
            "[混合智能] ====== 校验完成: %.1fs, "
            "融合异常=%d, 高风险=%d, 确认=%d, 待复核=%d ======",
            report.duration_seconds,
            report.fused_anomaly_count,
            report.high_risk_count,
            report.confirmed_count,
            report.need_review_count,
        )

        return report

    def run_gnn_only(self) -> List[GNNAnomalyResult]:
        """仅运行 GNN 检测"""
        self._run_feature_engineering()
        self._run_gnn_detection()
        return self._gnn_results

    def run_temporal_only(self) -> List[TemporalAnomalyResult]:
        """仅运行时空模型"""
        self._run_feature_engineering()
        self._run_temporal_detection()
        return self._temporal_results

    def run_rules_only(self) -> List[RuleHit]:
        """仅运行规则引擎"""
        self._run_rule_engine()
        return self._rule_hits

    def get_fusion_result(self, equip_id: str) -> Optional[FusionResult]:
        """获取指定设备的融合结果"""
        if self._fusion_summary is None:
            return None
        for r in self._fusion_summary.results:
            if r.equip_id == equip_id:
                return r
        return None

    # ==================================================================
    # Step 1: 特征工程
    # ==================================================================

    def _run_feature_engineering(self):
        """从拓扑图和遥测数据中提取特征（所有路共享）"""
        if self._feature_eng is not None:
            return  # 幂等

        logger.info("[混合智能] Step 1/4: 特征工程...")
        self._feature_eng = FeatureEngineering(
            topo=self.topo,
            telemetry_data=self.telemetry_data,
            switch_status_map=self.switch_status_map,
        )
        self._feature_eng.run_all()

    # ==================================================================
    # Step 2a: GNN 检测
    # ==================================================================

    def _run_gnn_detection(self):
        """图注意力网络异常检测"""
        if self._gnn_results:
            return  # 幂等

        logger.info("[混合智能] Step 2a/4: GNN 图注意力检测...")
        features = self._feature_eng.run_all()
        feat_mat, equip_ids = self._feature_eng.get_feature_matrix()

        # 构建邻接矩阵
        from .gat_layer import build_adjacency_matrix
        adj, _, _ = build_adjacency_matrix(self.topo, equip_ids)

        # 构建属性字典
        equip_types = {
            eid: str(self.topo.device_map[eid].equip_type or "")
            for eid in equip_ids
        }
        feeder_ids = {
            eid: str(self.topo.device_map[eid].feeder_id or "")
            for eid in equip_ids
        }
        is_sources = {
            eid: bool(self.topo.device_map[eid].is_source)
            for eid in equip_ids
        }
        has_telemetry = {eid: bool(features[eid].has_telemetry) for eid in equip_ids}
        topo_depths = {eid: int(features[eid].topo_depth) for eid in equip_ids}

        # 训练 + 推理
        self._gat_detector = GATAnomalyDetector()
        # 构建 numpy 属性数组（与 equip_ids 顺序一致）
        e_types_arr = np.array([equip_types.get(eid, "") for eid in equip_ids])
        f_ids_arr   = np.array([feeder_ids.get(eid, "") for eid in equip_ids])
        is_src_arr  = np.array([float(is_sources.get(eid, 0)) for eid in equip_ids])
        has_tel_arr = np.array([float(has_telemetry.get(eid, 0)) for eid in equip_ids])
        depths_arr  = np.array([topo_depths.get(eid, -1) for eid in equip_ids])

        self._gat_detector.fit(
            features=feat_mat,
            adj_matrix=adj,
            equip_types=e_types_arr,
            feeder_ids=f_ids_arr,
            is_sources=is_src_arr,
            has_telemetry=has_tel_arr,
            topo_depths=depths_arr,
            anomaly_labels=None,
            epochs=self.gat_epochs,
        )

        self._gnn_results = self._gat_detector.predict(
            equip_ids=equip_ids,
            features=feat_mat,
            adj_matrix=adj,
            equip_types=e_types_arr,
            feeder_ids=f_ids_arr,
            is_sources=is_src_arr,
        )

        # 回填到 DeviceFeatures
        for r in self._gnn_results:
            feat = features.get(r.equip_id)
            if feat:
                feat.gnn_embedding = r.embedding_norm  # 标量作为代理
                feat.gnn_attention_score = r.attention_score
                feat.gnn_anomaly_prob = r.anomaly_prob

        n_anomaly = sum(1 for r in self._gnn_results if r.anomaly_prob >= 0.45)
        logger.info(
            "[混合智能] GNN 检测完成: %d 设备, %d 个异常（异常率=%.1f%%）",
            len(self._gnn_results), n_anomaly,
            100 * n_anomaly / max(len(self._gnn_results), 1),
        )

    # ==================================================================
    # Step 2b: 时空模型检测
    # ==================================================================

    def _run_temporal_detection(self):
        """时空模型异常检测"""
        if self._temporal_results:
            return  # 幂等

        logger.info("[混合智能] Step 2b/4: 时空模型检测...")
        self._temporal_detector = SpatioTemporalDetector(window_size=60)
        self._temporal_detector.fit(
            telemetry_data=self.telemetry_data,
            anomaly_labels=None,
            epochs=10,
        )
        self._temporal_results = self._temporal_detector.predict(
            telemetry_data=self.telemetry_data,
        )

        # 回填到 DeviceFeatures
        features = self._feature_eng.run_all()
        for r in self._temporal_results:
            feat = features.get(r.equip_id)
            if feat:
                feat.temporal_anomaly_score = r.anomaly_score

        n_anomaly = sum(1 for r in self._temporal_results if r.status == "ANOMALY")
        logger.info(
            "[混合智能] 时空模型检测完成: %d 设备, %d 个异常（异常率=%.1f%%）",
            len(self._temporal_results), n_anomaly,
            100 * n_anomaly / max(len(self._temporal_results), 1),
        )

    # ==================================================================
    # Step 2c: 规则引擎
    # ==================================================================

    def _run_rule_engine(self):
        """确定性规则引擎执行"""
        if self._rule_hits:
            return  # 幂等

        logger.info("[混合智能] Step 2c/4: 确定性规则引擎...")
        self._rule_engine = HybridRuleEngine(
            topo=self.topo,
            telemetry_data=self.telemetry_data,
            svg_document=self.svg_doc,
            switch_status_map=self.switch_status_map,
        )
        self._rule_hits = self._rule_engine.run_all_rules()

        n_deterministic = sum(1 for h in self._rule_hits if h.is_deterministic)
        logger.info(
            "[混合智能] 规则引擎完成: %d 条命中, %d 条确定性规则",
            len(self._rule_hits), n_deterministic,
        )

    # ==================================================================
    # Step 3: 融合决策
    # ==================================================================

    def _run_fusion(self):
        """三路信号加权融合"""
        if self._fusion_summary is not None:
            return  # 幂等

        logger.info("[混合智能] Step 3/4: 融合决策...")
        self._fusion_layer = FusionLayer(
            gnn_weight=0.30,
            temporal_weight=0.25,
            rule_weight=0.45,
        )
        self._fusion_summary = self._fusion_layer.fuse(
            gnn_results=self._gnn_results,
            temporal_results=self._temporal_results,
            rule_hits=self._rule_hits,
        )

    # ==================================================================
    # Step 4: 生成报告
    # ==================================================================

    def _build_report(self, duration: float) -> HybridCheckReport:
        """构建完整报告"""

        # 赛题重点关注结果
        suspected_tie: List[dict] = []
        electrical_anom: List[dict] = []
        graph_anom: List[dict] = []

        for r in (self._fusion_summary.results if self._fusion_summary else []):
            d = r.to_dict()
            if r.anomaly_type == "疑似联络开关":
                suspected_tie.append(d)
            elif r.anomaly_type == "电气逻辑异常":
                electrical_anom.append(d)
            elif r.anomaly_type == "图模一致性异常":
                graph_anom.append(d)

        features = self._feature_eng.run_all() if self._feature_eng else {}
        n_telemetry = sum(1 for f in features.values() if f.has_telemetry)

        fs_dict = self._fusion_summary.to_dict() if self._fusion_summary else {}

        return HybridCheckReport(
            line_name=self.line_name,
            total_devices=len(self.topo.device_map),
            duration_seconds=duration,
            features_extracted=len(features),
            telemetry_coverage=n_telemetry,
            gnn_enabled=self.enable_gnn,
            temporal_enabled=self.enable_temporal,
            gnn_anomaly_count=fs_dict.get("gnn_anomaly_count", 0),
            temporal_anomaly_count=fs_dict.get("temporal_anomaly_count", 0),
            rule_hit_count=len(self._rule_hits),
            rule_deterministic_count=sum(1 for h in self._rule_hits if h.is_deterministic),
            fused_anomaly_count=fs_dict.get("fused_anomaly_count", 0),
            high_risk_count=fs_dict.get("high_risk_count", 0),
            medium_risk_count=fs_dict.get("medium_risk_count", 0),
            confirmed_count=fs_dict.get("confirmed_count", 0),
            need_review_count=fs_dict.get("need_review_count", 0),
            fusion_summary=fs_dict,
            gnn_results=[r.to_dict() for r in self._gnn_results],
            temporal_results=[r.to_dict() for r in self._temporal_results],
            rule_hits=[h.to_dict() for h in self._rule_hits],
            fusion_results=[r.to_dict() for r in (self._fusion_summary.results if self._fusion_summary else [])],
            suspected_tie_switches=suspected_tie,
            electrical_anomalies=electrical_anom,
            graph_model_anomalies=graph_anom,
        )


# ------------------------------------------------------------------
# 独立函数（直接调用，无需实例化）
# ------------------------------------------------------------------

def run_hybrid_intelligence_check(
    line_name: str,
    topo,
    telemetry_data: Optional[dict] = None,
    svg_document=None,
    switch_status_map: Optional[dict] = None,
    enable_gnn: bool = True,
    enable_temporal: bool = True,
    gat_epochs: int = 30,
) -> HybridCheckReport:
    """
    一键运行混合智能校验

    等价于:
        checker = HybridIntelligenceChecker(...)
        return checker.run_all_checks()
    """
    checker = HybridIntelligenceChecker(
        line_name=line_name,
        topo=topo,
        telemetry_data=telemetry_data,
        svg_document=svg_document,
        switch_status_map=switch_status_map,
        enable_gnn=enable_gnn,
        enable_temporal=enable_temporal,
        gat_epochs=gat_epochs,
    )
    return checker.run_all_checks()
