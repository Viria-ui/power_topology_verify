# 配电网图模拓扑智能识别与校验系统

> 基于图模一致性比对的主配网拓扑校验系统，覆盖 **电气逻辑校验（E01-E07）**、**物理约束校核（KCL）**、**II 型模糊可信度**、**修复方案排序**，以及 **GNN + 时空融合的混合智能校验**（全网 + 单馈线子图双层报告，2026-09 新增）。

---

## 目录

1. [快速开始](#1-快速开始)
2. [系统功能](#2-系统功能)
3. [核心算法](#3-核心算法)
4. [输出产物](#4-输出产物)
5. [测试结果](#5-测试结果)
6. [目录结构](#6-目录结构)
7. [数据格式要点](#7-数据格式要点)
8. [安全须知](#8-安全须知)

---

## 1. 快速开始

### 1.1 环境

```bash
python --version   # Python 3.10+
pip install -r requirements.txt
```

依赖：`pydantic>=2.0`、`networkx>=3.0`、`lxml>=4.9`、`openpyxl>=3.1`、`jinja2>=3.0`、`torch>=2.0`、`torch_geometric>=2.4`。
**`torch` 默认装 CPU 版**；装 PyTorch 不会更快（详见 §3.4 GAT 内存安全）。

### 1.2 运行

```bash
# ===== 单线路完整流程（推荐用法，2026-09 新增）=====
python main.py --line LINE111                       # 解析 → 图模比对 → 美化 → 出图
python main.py --line LINE111 --hybrid              # 再加混合智能校验（全网 + 子图双报告）
python main.py --line LINE111 --hybrid --repair     # 再算"修复后评分"（不写库）
python main.py --line LINE111 --no-svg              # 跳过 SVG 相关步骤

# 只解析 SVG
python main.py --parse-only LINE111

# 全网模式（未改动）
python main.py --all                                # 全功能（建议配合 --line 指定线路）
python main.py --topo                               # 仅拓扑校验（全网）
python main.py --svg                                # 仅 SVG 编辑与自动出图
python main.py --compare LINE215 LINE216            # 多线路图模比对

# 工具脚本
python scripts/run_all_tests.py                     # 综合测试
python run_beautify.py                              # SVG 美化独立入口
```

### 1.3 v3.0 新增参数

| 参数 | 用途 |
|---|---|
| `--line NAME` | 单条线路全流程（SVG 解析 → 增强报告 → 图模比对 → 美化 → 出图） |
| `--parse-only NAME` | 只解析 SVG、生成两份 JSON，不跑校验 |
| `--hybrid` | 在 `--line` 流程里启用混合智能校验（GNN + 时空 + 规则） |
| `--repair` | 把"物理/逻辑层"确定性修复候选视为已采纳，重算 `score_after`（不写库） |
| `--no-beautify` | 跳过 SVG 美化（仅 `--line` 模式生效） |
| `--no-svg` | 跳过全部 SVG 相关步骤 |

### 1.4 典型产物（`--line LINE111 --hybrid --repair`）

| 文件 | 说明 |
|---|---|
| `output/reports/LINE111_增强校验报告.json` | **全网**混合智能校验（GNN + 时空 + 规则 + 物理约束） |
| `output/reports/LINE111_TMP00000033_subgraph_hybrid_report.json` | **馈线子图**混合智能校验（含跨馈线边界节点） |
| `output/json/LINE111.svg_elements.json` | SVG 元素解析（自动生成） |
| `output/LINE111_缺陷清单报告.json` | 图模缺陷清单（R001-R003、E01-E07） |
| `output/LINE111_最小修改候选与SQL草案.json` | 修复候选 + 拓扑变更摘要 |
| `output/LINE111_正向修复与回滚脚本.sql` | 可执行的 SQL 草案（含回滚） |
| `output/LINE111_质量评分与可解释置信度报告.json` | `score_before → score_after` |
| `output/LINE111_拓扑校验缺陷报告.xlsx` | 标准 Excel 缺陷报告 |
| `output/svg/10kVLINE111_beautified.svg` | 美化后的 SVG |
| `output/svg/LINE111_single_line.svg` | 自动生成的单线图 |
| `output/reports/10kVLINE111_美化质量对比报告.json` | 美化前后质量对比 |

数据库**不会被改动**，所有 SQL 仅作为草案，需人工审核后再执行。

### 1.5 性能参考（实测，LINE111）

| 步骤 | 耗时 |
|---|---|
| 主配网拓扑构建 | ≈ 30 s |
| 全网混合智能校验（NumPy 兜底） | ≈ 2 min |
| 馈线子图混合智能校验 | ≈ 15 s |
| 图模比对 + 评分 + SQL 生成 | ≈ 5 s |
| SVG 美化 | ≈ 3 s |
| 自动出图 | ≈ 5 s |
| **合计** | **≈ 3 min** |

---

## 2. 系统功能

### 2.1 功能模块

| 模块 | 功能 | 算法 | 全库实测结果（2026-09） |
|---|---|---|---|
| 拓扑完整性 | 悬空 / 孤岛 / 断点 / 联络 / 合环 | NetworkX 连通性 | 异常 9565、断点 561、联络合环 235 |
| 图模一致性 | SVG vs DB 比对 | ID 集合差集 | LINE215：图有模无 1、模有图无 49（非设备图元豁免后）；物理连接不一致 3487 |
| 电气逻辑 E01-E07 | 遥测规则 | PWREAL 规则匹配 | 3272（E01=119/E02=440/E03=1287/E04=980/E05=323/E06=56/E07=67） |
| 主配网接口 | 主网站与配网对接 | CN 拓扑拼接（Q41） | 189 条馈线通过 148、失败 41 |
| 质量自评分 | 四维评分 | `Model_Score = 100 − Σ(Wᵢ×Cᵢ)` | 见 `output/质量评分报告` |
| SVG 美化 | 标准化排版 | 力导向布局 | LINE215/LINE216/10kVLINE018 美化完成 |
| SVG 自动生成 | 单线图 / 联络图 / 电源追溯图 | 拓扑遍历渲染 | 5 种输出（详见 §4） |
| 混合智能校验 *（v3.0）* | GAT + 时空 + 规则融合 | NumPy 拓扑感知注意力兜底 | `--hybrid` 触发，详见 §3.4 |

### 2.2 数据规模

| 数据 | 数量 | 说明 |
|---|---|---|
| 配网设备 | 50,744 | 配网设备台账 |
| 馈线 | 189 | 配电线路 |
| 端子 | 76,657 | 设备连接端子 |
| 遥信遥测 | 5,829 | 实时运行数据 |
| 主网站点 | 10 | 110 kV 变电站 |
| 主网设备 | 1,167 | 主网设备台账 |
| SVG 图 | 200+ | 配电网接线图 |

---

## 3. 核心算法

### 3.1 图模一致性比对

```
SVG 解析 → SVG_DEV_IDS
DB 查询  → DB_DEV_IDS
差集运算 → svg_only（图有模无）∪ db_only（模有图无）
          → 一致：SVG_DEV_IDS ∩ DB_DEV_IDS
连接比对 → 同一 CONNECT_NODE 的端子互连 vs SVG <line> 连接
```

### 3.2 拓扑连通性与异常

- **悬空 R001**：开关类（1705-1709）只有 1 个连接端子
- **孤岛 R002**：连通分量内无电源设备
- **断点 R003**：同一馈线设备分布在多个连通分量，按 P1-P7 定位
  - P1 分位开关 → P2 不连通路径 → P3 遥信矛盾 → P4 端子悬空 → P5 同馈多分量 → P6 虚假连通 → P7 电源失压
- **联络 R_TIE_001**：分位状态 + 两侧连通不同馈线
- **合环 R_LOOP_001**：环内电源数 ≠ 2

### 3.3 电气逻辑 E01-E07

| 规则 | 名称 | 判定条件 |
|---|---|---|
| E01 | 分位有电流 | POINT=0 ∧ \|I\| > 阈值 |
| E02 | 合位失流 | POINT=1 ∧ \|I\| < 阈值 |
| E03 | 合位失压 | POINT=1 ∧ U < 阈值 |
| E04 | 电流不平衡 | max(\|Ia−Ib\|,\|Ib−Ic\|,\|Ic−Ia\|) > 阈值 |
| E05 | 功率不匹配 | P ≠ U × I |
| E06 | 分位有功率 | POINT=0 ∧ P > 阈值 |
| E07 | 小电流大功率 | P > 阈值 ∧ I < 阈值 |

### 3.4 混合智能校验（GNN + 时空 + 规则）

**GAT 内存安全（5 万节点不 OOM）**：旧实现 `np.zeros((N,N))` 需 ~10 GB → 必 OOM。
新实现：`build_adjacency_matrix` 返回**邻接表** + 邻居采样（≤15）+ `n > 50` 自动走 NumPy `TopologicalAttentionScorer`。

**双层报告设计**：

| 报告 | 范围 | 节点规模 | 用途 |
|---|---|---|---|
| `*_增强校验报告.json` | 全网 | 50,919 设备 | 全局图模一致性 + 联络 + 主配接口可疑点 |
| `*_subgraph_hybrid_report.json` | 单馈线 + 跨馈线边界 | ≈ 1,000-3,000 设备 | 聚焦"这条线"的 GNN / 时空 / 规则异常 |

**综合风险公式**：
```
综合风险 = GAT 异常分×0.25 + 图模规则分×0.25
         + 物理残差分×0.35 + 数据可信度修正×0.15
```

### 3.5 修复排序

```
优先级 = 置信度×0.30 + 风险降低量×0.40 + 约束恢复得分×0.30 − 影响范围惩罚
```
**`--repair` 仅采纳** `ADD_CONNECTION`、`UPDATE_VOLTAGE_TYPE` 等**有 DB 依据、可逆**的 SQL，排除 `ADD_DEVICE` / `ADD_SVG_ELEMENT` / `REVIEW`，避免刷到虚假 100 分。

### 3.6 四维评分

| 维度 | 权重 | 扣分上限 | 单项扣分 |
|---|---|---|---|
| 拓扑完整性 | 5 | 30 | 悬空 -0.5 / 孤岛 -2 / 断点 -1 / 联络异常 -0.3 |
| 图模一致性 | 3 | 25 | 图有模无 -0.5 / 模有图无 -0.3 / 连接不一致 -1 |
| 电气逻辑 | 2 | 20 | E01-E06 -0.2~0.5 / E07 -1 |
| 接口规范性 | 4 | 25 | 漏拼 -1 / 错拼 -2 |

`Model_Score = max(0, 100 − Σ(各维度扣分))`，规范书 v1.1 不叠加缺陷率惩罚。

### 3.7 II 型模糊可信度

异常状态判定（不只"正常/异常"二值）：

| 状态 | 判定条件 |
|---|---|
| CONFIRMED | 置信区间下限 ≥ 阈值 |
| LIKELY | 区间包含阈值 |
| PENDING | 区间宽度 > 0.4 |
| FALSE_ALARM | 上限 < 阈值 |
| NORMAL | 无异常 |

---

## 4. 输出产物

### 4.1 Excel 缺陷报告（`*_拓扑校验缺陷报告.xlsx`）

| Sheet | 内容 |
|---|---|
| Sheet1 问题清单 | 设备ID、缺陷类型、规则编码、描述、SQL 草案 |
| Sheet2 断点定位 | P1-P7 优先级断点候选（418 个） |
| Sheet3 联络开关 | 跨馈线开关识别（214 个） |
| Sheet4 合环识别 | 非计划合环识别（19 个） |
| Sheet5 质量评分 | 四维评分明细 |

### 4.2 SVG 自动生成产物

| 任务 | 图形类型 | 节点 | 边 |
|---|---|---|---|
| LINE215 单线图 | 单馈线完整单线图 | 1,313 | 1,299 |
| LINE216 单线图 | 单馈线完整单线图 | 1,644 | 1,646 |
| 10kVLINE111 联络图 | 馈线联络关系图 | 3 | 42 |
| SUB004 联络总图 | 全站间联络总图 | 180 | 1,580 |
| TMP00034205 电源追溯图 | 电源追溯路径图 | 254 | 253 |

### 4.3 修复候选 JSON 结构（节选）

```json
{
  "line_name": "LINE215",
  "repair_candidates": [{
    "repair_id": "R001",
    "defect_type": "图有模无",
    "equip_id": "TMP00044547",
    "action": "ADD_DEVICE",
    "sql_draft": "INSERT INTO PWEQUIPINFO (...) VALUES (...);",
    "rollback_sql": "DELETE FROM PWEQUIPINFO WHERE EQUIP_ID='TMP00044547';",
    "priority": 1.0,
    "confidence": 0.85
  }]
}
```

---

## 5. 测试结果

### 5.1 任务一：图模质量校验

| 测试任务 | 结果 |
|---|---|
| 1.1 悬空检测 | 218 个 |
| 1.2 断点定位 | 418 个 |
| 1.3 联络开关 | 214 个 |
| 1.5 合环检测 | 19 个 |
| 2.1 图有模无 | 440 个 |
| 2.2 模有图无 | 306 个 |
| 电气逻辑 E01-E07 | 4,458 条 |
| 修正前评分 | 23.9 分 |

**任务 1.2-1**：拓扑找 TMP00013138 至 TMP00047197 中间断点 → 设备不存在：TMP00047197
**任务 1.2-2**：拓扑找 TMP00007913 至 TMP00007907 中间断点 → 路径长度：9 跳

### 5.2 任务二：SVG 美化专项

| 线路 | 图元数 | 物理连接 | 断点修复 | 连通分量变化 |
|---|---|---|---|---|
| LINE215 | 1,431 | 962 | 26 → 7 | 84 → 6 |
| LINE216 | 1,645 | 660 | 29 → 2 | 214 → 1 |
| 10kVLINE018 | 383 | 167 → 355 | 0 | 61 → 3（+46.9 分） |

**2026-09-10 P1-P4 修复效果**：

| 修复项 | 修复前 | 修复后 |
|---|---|---|
| P1 ZWLINEEND 映射数 | 0 | 149（线路名称标准化匹配） |
| P2 电气缺陷过滤（全网→馈线） | 3,554 | 299 |
| P3 拓扑构建耗时 | 重复构建 | 单次执行（节省 ≈ 50%） |
| P4 美化质量（10kVLINE018） | 39.6 | 86.5（绝对尺寸阈值 `MIN_DEVICE_SIZE=15.0`） |

### 5.3 v3.0 混合智能校验（实测，LINE111）

| 报告 | 节点规模 | 耗时 | 典型产物 |
|---|---|---|---|
| 全网 | 50,919 | ≈ 2 min | `LINE111_增强校验报告.json` |
| 馈线子图 | ≈ 1,000-3,000 | ≈ 15 s | `LINE111_TMP00000033_subgraph_hybrid_report.json` |

---

## 6. 目录结构

```
power_topology_verify/
├── main.py                  # 命令行入口（--all/--topo/--line/--hybrid/--repair/--svg…）
├── requirements.txt         # Python 依赖
├── readme.md                # 本文档
│
├── core/                    # 核心业务逻辑
│   ├── graph_model.py       # Device / ConnectPoint / TopoEdge / TopologyGraph
│   ├── topology_builder.py  # 从 SQL 构建拓扑图（含主配网接口拼接）
│   ├── topology_validator.py# 图模一致性校验 R001-R003、联络、合环
│   ├── telemetry_evaluator.py# 电气逻辑 E01-E07
│   ├── measure_preprocess.py# 遥信去噪 / 10s 防抖 / 状态推演
│   ├── score_engine.py      # 四维评分 + II 型模糊可信度
│   ├── repair_generator.py  # SQL 修复方案 + 回滚
│   ├── feeder_topology_analysis.py # 馈线联络 / 合环 / 断点分析
│   ├── defect_excel_exporter.py    # Excel 缺陷报告
│   ├── physical_constraint_checker.py # KCL / 支路 / 联络约束
│   ├── type2_fuzzy_confidence.py   # II 型模糊可信度
│   ├── temporal_feature_extractor.py # 时序特征
│   ├── repair_ranking_engine.py   # 修复排序
│   ├── enhanced_report_generator.py # 整合增强报告 + 全网/子图双层
│   └── hybrid_intelligence/   # GAT + 时空 + 规则融合（v3.0）
│
├── data_io/                 # SQL / SVG 读写
├── svg_io/                  # SVG 美化 / 编辑 / 自动生成 / 质量评分
├── config/                  # settings.py / constants.py / rule_config.json
├── scripts/                 # run_all_tests / quick_test / svg_pipeline / visualization
├── tests/                   # 单元测试 + compare.py 入口
│
├── input/sql_gbk/           # 输入数据（GBK 编码）
├── output/                  # 输出：csv/ json/ svg/ reports/ sql/ log/
├── 数据集更新版20260729/    # 比赛数据集 V1（200+ SVG + SQL）
├── 数据集更新版20260821/    # 增量补丁（标准输出模板 + 更新脚本）
├── 参考文件/                # 制图规范 / 校验规则 / 设备模型规范
└── docs/                    # api_doc.md + 样例数据
```

> 详细类结构与方法说明见 [`docs/api_doc.md`](docs/api_doc.md)。

---

## 7. 数据格式要点

### 7.1 SQL 关键表

| 表 | 关键字段 | 用途 |
|---|---|---|
| `EQUIP_JBS_PWEQUIPINFO` | `EQUIP_ID, EQUIP_NAME, EQUIP_TYPE, VOLTAGE_TYPE, FEEDER_ID` | 配网设备台账 |
| `EQUIP_JBS_PWFEEDERLINE` | `LINE_ID, LINE_NAME, START_ST_ID, START_EQUIP, END_EQUIP` | 馈线 |
| `EQUIP_JBS_PWTERMINAL` | `TERMINAL_ID, BELONG_EQUIP, CONNECT_NODE, FEEDER_ID` | 端子建边 |
| `EQUIP_JBS_PWREAL` | `TRAN_ID, UA/UB/UC, IA/IB/IC, AP, RP, POINT, QUALITY` | 遥信遥测 |
| `EQUIP_JBS_ZW*` | 主网设备/站点/端子/线端/量测 | 主网侧 + 接口校验 |

**设备类型编码**：

| 编码 | 类型 |
|---|---|
| 1705 / 1706 / 1707 / 1708 / 1709 | 断路器 / 负荷开关 / 隔离开关 / 分段开关 / 用户分界开关 |
| 0110 / 0111 | 配电变压器 / 主变压器 |
| 1710 / 0311 | 母线 / 开关柜母线 |
| 1730 / 1731 | 负荷 / 配变 |

### 7.2 SVG 图元

```xml
<g id="TMP00012345" class="equipment switch">
  <rect .../>
  <metadata>
    <objectid>TMP00012345</objectid>
    <objecttype>1705</objecttype>
    <objectname>10kVXX线路开关001</objectname>
    <feederid>FEEDER-A</feederid>
  </metadata>
</g>
<line x1="..." y1="..." x2="..." y2="..."/>  <!-- 设备间连线 -->
```

---

## 8. 安全须知

本系统生成的 SQL 修复脚本在对**生产数据库**执行 `UPDATE/DELETE` 前：

- 必须在**测试环境**完成逆向回滚脚本（Rollback SQL）的验证；
- 涉及**高压开关状态推演与合环操作**建议时，必须经线下**人工调度员**核查，严禁直接联动自动化执行机构；
- 数据库**不会被本系统自动改动**，所有 SQL 仅作为草案。

---

*文档版本: v3.1 | 更新日期: 2026-09-10（精简版）*
