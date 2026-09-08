"""
混合智能校验系统 (Hybrid Intelligence Verification System)
============================================================

架构：电力拓扑图算法 + GNN 图注意力 + 时空模型 + 规则约束 四路融合

├── feature_engineering.py   — 特征工程：从拓扑图/遥测数据中提取图结构特征
├── gat_layer.py             — 图注意力网络层（GAT）：可学习节点嵌入 + 异常注意力分数
├── spatio_temporal.py       — 时空模型：1D-CNN + LSTM 时序异常检测
├── rule_engine.py           — 确定性规则引擎：拓扑/电气规则兜底
├── fusion_layer.py          — 融合决策层：三路信号加权融合 + 置信度计算
└── hybrid_checker.py         — 主校验器：整合全部模块，统一输出

融合策略：
  - GNN 置信度高 → 以 GNN 为准（数据驱动，隐式拓扑关系）
  - 规则命中 → 以规则为准（确定性，零误判）
  - 时空异常 → 参考（需要历史数据支持）
  - 三路全阳性 → 高置信度确认
  - 三路矛盾   → 降级为"需人工复核"
"""

from .hybrid_checker import HybridIntelligenceChecker, run_hybrid_intelligence_check

__all__ = ["HybridIntelligenceChecker", "run_hybrid_intelligence_check"]
