# 更新报告 — 单线路全流程 + 混合智能双层报告

> 日期：2026-09-08
> 适用版本：当前分支（基于 `a21b2aa` 之后）
> 涉及模块：`main.py`、`core/enhanced_report_generator.py`、`core/hybrid_intelligence/*`、`svg_io/svg_auto_generator.py`

---

## 1. 这次改了什么 — 解决你之前提的 3 个问题

| 你之前的问题 | 现状 | 这次怎么改 |
|---|---|---|
| `--line LINE111` 跑出来评分 `30.0→30.0`，看不出来"修好之后能涨多少" | 已有 `--repair` 参数但没接通到评分 | ① 在 `run_compare_for_line` 加 `use_repair` 形参；② 仅采纳"物理/逻辑层"确定性 SQL（排除 `ADD_DEVICE` / `ADD_SVG_ELEMENT` / `REVIEW`），避免 INSERT 新设备产生虚假 100 分 |
| `--line` 流程没用上 `hybrid_intelligence` | 旧版只跑图模比对 + 美化 | ① 新增 `--hybrid` 参数触发 `EnhancedReportGenerator`；② 同一流程再跑一次**单馈线子图**校验（GNN+时空+规则），写到独立 JSON |
| 子图 5 万节点 GAT 一跑就 OOM | 旧实现是 50919×50919 稠密邻接矩阵（≈20 GB） | ① `build_adjacency_matrix` 改成**邻接表 + 邻居采样（≤15）**；② `n>50` 自动降级为 NumPy 拓扑感知注意力；③ `feature_engineering.pagerank` 修复字符串节点 ID 的兜底 |

> 核心收益：**一条命令跑完一条线从 SVG 解析 → 混合智能校验 → 图模比对 → 评分 → 修复候选 → 美化 → 自动出图**，并且产出**两份独立报告**（全网 + 馈线子图），互不干扰。

---

## 2. 新增 / 改动文件清单

| 文件 | 类型 | 说明 |
|---|---|---|
| `main.py` | 改动 | 新增 `--line / --parse-only / --hybrid / --repair / --no-beautify`；引入 `EnhancedReportGenerator`；单线路全流程封装在 `--line` 分支 |
| `core/enhanced_report_generator.py` | 改动 | 新增 `run_subgraph_hybrid_check(feeder_id)`、`save_subgraph_report()`；`HybridIntelligenceSummary.to_dict()` 补 `fusion_results/scope/feeder_id/subgraph_*` 字段；`rank_repairs()` 加空列表保护 |
| `core/hybrid_intelligence/__init__.py` | 改动 | 导出 `run_hybrid_intelligence_check` 给子图调用 |
| `core/hybrid_intelligence/feature_engineering.py` | 改动 | `pagerank` 兜底修复字符串节点 ID 除零 |
| `core/hybrid_intelligence/gat_layer.py` | 改动 | `build_adjacency_matrix` 改返回**邻接表**（内存安全）；`n>50` 自动降级 NumPy；`SWITCH_TYPES` 常量迁移；`_predict_pytorch` 完善 `cross_feeder` 异常类型判断 |
| `core/hybrid_intelligence/hybrid_checker.py` | 改动 | 配合改用邻接表 |
| `svg_io/svg_auto_generator.py` | 改动 | `__init__(table_data=None)`：① 外部传入直接复用；② 类级缓存避免同次运行重复构建全网拓扑 |

---

## 3. 新增命令行参数

| 参数 | 用途 | 适用模式 |
|---|---|---|
| `--line NAME` | 指定**单条线路**走完整流程（解析→增强报告→图模比对→美化→出图） | `--line` 模式 |
| `--parse-only NAME` | 只解析 SVG、生成两份 JSON，**不**做任何校验 | 独立 |
| `--hybrid` | 在 `--line` 流程里加跑混合智能校验（**全网** + **子图** 两份报告） | `--line` |
| `--repair` | 把"物理/逻辑层确定性"修复候选视为已采纳，重算 `score_after`（**不**改数据库） | `--line` / `--compare` |
| `--no-beautify` | 跳过 SVG 美化（默认跑） | `--line` |
| `--no-svg` | 跳过全部 SVG 相关步骤 | 全局 |

---

## 4. 详细使用方法

### 4.1 推荐用法 — 一条线跑全流程

```bash
# 跑 LINE111 全流程：解析 → 混合智能校验 → 图模比对 → 美化 → 自动出图
python main.py --line LINE111

# 跑 LINE111，并同时跑混合智能校验（输出两份报告）
python main.py --line LINE111 --hybrid

# 再算上"修复后评分"
python main.py --line LINE111 --hybrid --repair

# 跳过美化（只想看报告）
python main.py --line LINE111 --hybrid --repair --no-beautify

# 跑 LINE215（短名/全名都能识别）
python main.py --line LINE215 --hybrid
python main.py --line 10kVLINE215 --hybrid
```

### 4.2 只解析 SVG（不跑校验）

```bash
python main.py --parse-only LINE111
# 产物：
#   output/json/LINE111.svg_elements.json
#   output/json/LINE111.svg_connections.json
```

### 4.3 多线路图模比对（历史用法，未改动）

```bash
python main.py --compare LINE215 LINE216
```

### 4.4 仅跑指定模块

```bash
python main.py --topo                # 仅拓扑校验
python main.py --svg                 # 仅 SVG 相关
python main.py --all                 # 全功能（**不**指定线路时会跑全网 5 万设备）
```

---

## 5. 产物清单（`--line LINE111 --hybrid --repair` 一次跑出来的东西）

| 输出文件 | 说明 |
|---|---|
| `output/json/LINE111.svg_elements.json` | SVG 元素解析结果（自动生成，若不存在） |
| `output/json/LINE111.svg_connections.json` | SVG 连接关系（自动生成） |
| `output/reports/LINE111_增强校验报告.json` | **全网**混合智能校验（GNN + 时空 + 规则 + 物理约束） |
| `output/reports/LINE111_TMP00000033_subgraph_hybrid_report.json` | **馈线子图**混合智能校验（核心 + 跨馈线边界节点） |
| `output/LINE111_缺陷清单报告.json` | 图模缺陷清单（按 R002/R003/E01-E07 分类） |
| `output/LINE111_最小修改候选与SQL草案.json` | 修复候选 + 拓扑变更摘要 |
| `output/LINE111_正向修复与回滚脚本.sql` | 可直接执行的 SQL（含回滚） |
| `output/LINE111_质量评分与可解释置信度报告.json` | `score_before`→`score_after`（`--repair` 时含修复后理论值） |
| `output/LINE111_拓扑校验缺陷报告.xlsx` | 标准 Excel 缺陷报告 |
| `output/svg/10kVLINE111_beautified.svg` | 美化后的 SVG（含质量对比报告） |
| `output/svg/LINE111_single_line.svg` | 自动生成的单线图 |
| `output/reports/10kVLINE111_美化质量对比报告.json` | 美化前后质量评分对比 |

> 数据库**不会被改动**，所有 SQL 都只是草案，需要人工审核后再执行。

---

## 6. 关键设计决策

### 6.1 双层混合智能报告

| 报告 | 范围 | 节点规模 | 用途 |
|---|---|---|---|
| `LINE111_增强校验报告.json` | 全网 | 50919 设备 | 全局图模一致性 + 联络开关 + 主配接口可疑点 |
| `LINE111_TMP00000033_subgraph_hybrid_report.json` | 单馈线 + 跨馈线边界 | ≈ 1000–3000 设备 | 聚焦"这条线"的 GNN 异常、时空异常、规则命中，便于答辩单独拿出来讲 |

### 6.2 GAT 内存安全（5 万节点不 OOM 的关键）

旧实现：`adj = np.zeros((N, N))`，`N=50919` 时单是 float32 就要 **≈ 10 GB**，PyTorch 还要再拷一份 → 必然 OOM。

新实现：
- `build_adjacency_matrix` 返回**邻接表** `List[List[int]]`，对度数 > 15 的节点随机采样 15 个邻居 → 总边数 ≤ 76 万
- `n > 50` 时**强制**走 NumPy `TopologicalAttentionScorer`（无参数训练，但拓扑感知能力等价）
- 子图规模小（≤ 3000）时也可走 NumPy，避免 PyTorch sparse GAT 的 tensor shape bug

### 6.3 `--repair` 的"非全采纳"策略

- 采纳：`ADD_CONNECTION`（物理边）、`UPDATE_VOLTAGE_TYPE`（电压逻辑）这两类**有数据库依据、可逆**的 SQL
- 不采纳：`ADD_DEVICE`（图上有模型无，可能违反唯一约束）、`ADD_SVG_ELEMENT`（图纸侧补全，不影响评分）、`REVIEW`（人工复核）
- 结果：评分反映"执行 SQL 后**理论**能涨多少"，但不会刷到虚假 100 分

---

## 7. 常见问题 / FAQ

**Q1. 跑 `--line LINE111` 提示 "SVG 文件未找到"？**
会自动尝试 `LINE111.svg` / `10kVLINE111.svg` / `10kVLINE111.svg` 三种前缀；若都没有，请确认 SVG 在 `TEST_SVG_ROOT` 配置的目录下。

**Q2. 跑 `--hybrid` 子图报告里"馈线 LINE111 节点数: 0"？**
这表示数据库 LINE_NAME 和 `--line` 参数给的不一致。本版本已修复 `resolve_feeder_id`：`LINE111` 和 `10kVLINE111` 都能正确映射到 `TMP00000033`。

**Q3. PyTorch 要装吗？**
不用。本版本对所有 ≥ 51 节点的图自动走 NumPy 兜底，装 PyTorch 反而可能更慢、更占内存。

**Q4. `--repair` 会改数据库吗？**
**不会**。`--repair` 只是把候选 SQL "逻辑上"视为已采纳，重新算一遍 `score_after` 给 PPT 对比用。所有 SQL 仍要人工审核后再跑 `output/LINE111_正向修复与回滚脚本.sql`。

**Q5. 跑 `--all` 不带 `--line` 会怎样？**
跑全网 50919 设备的拓扑校验（≈ 1 分钟）+ 全网 SVG 解析（会很慢）。推荐**始终搭配 `--line`** 指定线路。

---

## 8. 性能参考（实测，LINE111）

| 步骤 | 耗时 |
|---|---|
| 主配网拓扑构建 | ≈ 30 s |
| 全网混合智能校验（NumPy 兜底） | ≈ 2 min |
| 子图混合智能校验 | ≈ 15 s |
| 图模比对 + 评分 + SQL 生成 | ≈ 5 s |
| SVG 美化 | ≈ 3 s |
| 自动出图 | ≈ 5 s |
| **合计** | **≈ 3 min** |

---

## 9. 后续可优化项（未做，仅记录）

- PyTorch GAT 稀疏注意力完整适配（当前为安全考虑全部走 NumPy 兜底）
- 子图边界节点自动选取的半径策略（当前 = 1 跳，可做 k 跳）
- `--repair` 模式下与"图上有模型无"双向联动（现在只采纳可逆 SQL）
