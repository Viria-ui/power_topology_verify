# 配网拓扑校验与修复系统

基于图模一致性比对的主配网拓扑校验系统，支持电气逻辑校验、物理约束校核、II型模糊可信度评估和智能修复排序。

## 版本历史

- **v2.0** (2026-09-06): 增强版 - 新增物理约束校验、II型模糊可信度、时序特征工程、智能修复排序
- **v1.x**: 基础版 - 图模一致性校验、缺陷报告生成、SQL修复草案

## 功能架构

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        配网拓扑校验与修复闭环流程                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  【数据输入】                                                                ║
║    SQL数据库 ─ SVG配网单线图 ─ 遥测数据 ─ 新能源出力数据                    ║
║           ↓              ↓              ↓              ↓                   ║
║                                                                              ║
║  【统一时空拓扑图构建】                                                      ║
║    ┌─────────────────────────────────────────────────────────┐              ║
║    │  设备节点  ──  连接边  ──  电气量属性  ──  时序数据   │              ║
║    └─────────────────────────────────────────────────────────┘              ║
║                              ↓                                              ║
║                                                                              ║
║  【多源异常检测】                                                            ║
║    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    ║
║    │ 图模规则校验 │  │ 时序特征分析 │  │ 物理约束校验 │                    ║
║    │ (SVG vs SQL) │  │ (滑动窗口)   │  │ (KCL/功率)   │                    ║
║    └──────────────┘  └──────────────┘  └──────────────┘                    ║
║                              ↓                                              ║
║                                                                              ║
║  【综合风险评分】                                                            ║
║    综合风险 = GAT异常分×0.25 + 图模规则分×0.25 + 物理残差分×0.35            ║
║               + 数据可信度修正×0.15                                          ║
║                              ↓                                              ║
║                                                                              ║
║  【II型模糊可信度】                                                          ║
║    ┌─────────────────────────────────────────────────────────┐              ║
║    │ CONFIRMED │ LIKELY │ PENDING │ FALSE_ALARM │ NORMAL     │              ║
║    └─────────────────────────────────────────────────────────┘              ║
║                              ↓                                              ║
║                                                                              ║
║  【修复方案排序】                                                            ║
║    优先级 = 置信度×0.3 + 风险降低量×0.4 + 约束恢复×0.3 - 影响惩罚           ║
║                              ↓                                              ║
║                                                                              ║
║  【输出成果】                                                                ║
║    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    ║
║    │ 增强缺陷报告 │  │ 修复SQL脚本  │  │ 回滚SQL脚本  │                    ║
║    │ (Excel/JSON) │  │ (正向修复)   │  │ (可回滚)     │                    ║
║    └──────────────┘  └──────────────┘  └──────────────┘                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 目录结构

```
power_topology_verify/
├── core/                           # 核心模块
│   ├── graph_model.py              # 图模型定义
│   ├── topology_builder.py          # 拓扑构建器
│   ├── topology_validator.py        # 拓扑校验器
│   ├── telemetry_evaluator.py      # 电气逻辑校验(E01-E07)
│   ├── score_engine.py             # 评分引擎
│   ├── repair_generator.py        # 修复候选生成
│   ├── feeder_topology_analysis.py # 馈线拓扑分析
│   ├── defect_excel_exporter.py    # Excel报告导出
│   ├── measure_preprocess.py       # 遥信预处理
│   ├── physical_constraint_checker.py  # [v2.0] 物理约束校验
│   ├── type2_fuzzy_confidence.py  # [v2.0] II型模糊可信度
│   ├── temporal_feature_extractor.py  # [v2.0] 时序特征工程
│   ├── repair_ranking_engine.py    # [v2.0] 修复排序引擎
│   └── enhanced_report_generator.py # [v2.0] 整合增强报告
├── data_io/                        # 数据IO模块
│   ├── data_reader.py              # SQL数据读取
│   ├── svg_reader.py               # SVG解析
│   └── data_writer.py              # 数据导出
├── svg_io/                         # SVG处理模块
│   ├── svg_beautifier.py           # SVG美化
│   └── ...
├── config/
│   ├── settings.py                 # 配置文件
│   └── constants.py                 # 常量定义
├── tests/
│   └── compare.py                  # 主比对脚本
├── output/                         # 输出目录
│   ├── reports/                    # 增强报告
│   ├── svg/                        # SVG输出
│   └── log/                        # 日志
└── README.md                       # 本文档
```

## 核心模块说明

### v1.x 基础模块

| 模块 | 功能 | 关键类/方法 |
|------|------|-------------|
| `topology_builder.py` | 构建主配网拓扑图 | `TopologyBuilder.build_full_topology()` |
| `telemetry_evaluator.py` | 电气逻辑校验 E01-E07 | `evaluate_electrical_logic()` |
| `score_engine.py` | 四维质量评分 | `evaluate_quality_score()` |
| `repair_generator.py` | SQL修复草案生成 | `generate_repair_candidates()` |
| `defect_excel_exporter.py` | Excel报告导出 | `export_defects_xlsx()` |

### v2.0 增强模块

| 模块 | 功能 | 关键类/方法 |
|------|------|-------------|
| `physical_constraint_checker.py` | 物理约束校验 | `check_kcl_node_balance()`, `check_branch_constraint()`, `check_tie_loop_detection()` |
| `type2_fuzzy_confidence.py` | II型模糊可信度 | `calculate_anomaly_confidence()`, `EnhancedAnomalyReport` |
| `temporal_feature_extractor.py` | 时序特征提取 | `extract_features()`, `detect_power_anomaly()` |
| `repair_ranking_engine.py` | 修复方案排序 | `process_repair_candidates()`, `generate_ranked_repair_report()` |
| `enhanced_report_generator.py` | 整合增强报告 | `EnhancedReportGenerator.generate_full_report()` |

## 使用方法

### 基础校验 (v1.x)

```bash
# 单条线路校验
python tests/compare.py --line LINE215

# 多条线路校验
python tests/compare.py --line LINE215 LINE216

# 全部线路
python tests/compare.py --all
```

### 增强校验 (v2.0)

增强模块已在 `compare.py` 中自动集成，运行基础命令即可生成增强报告：

```bash
python tests/compare.py --line LINE215
```

输出文件：
- `output/reports/LINE215_增强校验报告.json` - 完整增强报告

### API 调用示例

```python
# 导入增强报告生成器
from core.enhanced_report_generator import EnhancedReportGenerator

# 生成增强报告
generator = EnhancedReportGenerator(
    line_name="LINE215",
    defects=defects_list,
    device_map=device_map,
    telemetry_data=telemetry_data,
    svg_device_map=svg_map,
    switch_status_map=switch_status,
)

report = generator.generate_full_report()

# 保存报告
generator.save_report()
```

## 增强报告格式

### 数据源质量

```json
{
  "telemetry_quality": 0.85,    // 遥测数据质量
  "svg_quality": 0.90,          // SVG图模质量
  "database_quality": 0.95,     // 数据库质量
  "overall_confidence": 0.88     // 综合可信度
}
```

### II型模糊可信度状态

| 状态 | 含义 | 建议 |
|------|------|------|
| `CONFIRMED` | 高可信度异常 | 直接整改 |
| `LIKELY` | 疑似异常 | 现场核查 |
| `PENDING` | 待复核 | 补充数据后复核 |
| `FALSE_ALARM` | 误报 | 确认无异常后关闭 |
| `NORMAL` | 正常 | 无需处理 |

### 物理约束校验类型

| 类型 | 说明 | 物理依据 |
|------|------|----------|
| `KCL` | 基尔霍夫电流定律 | ΣI_in = ΣI_out |
| `BRANCH` | 支路约束 | 开关分位无功率流 |
| `TIE_LOOP` | 合环检测 | 同源合环 vs 非计划合环 |
| `VOLTAGE_IMBALANCE` | 电压不平衡 | 三相电压不平衡度 < 5% |

### 综合风险评分

```
综合风险 = GAT异常分×0.25 + 图模规则分×0.25 + 物理残差分×0.35 + 数据可信度修正×0.15
```

### 修复优先级评分

```
优先级 = 置信度×0.30 + 风险降低量×0.40 + 约束恢复得分×0.30 - 影响范围惩罚
```

## 输出报告示例

### 增强异常报告表格

| 异常对象 | 异常类型 | 综合风险 | 可信度区间 | 可信度状态 | 物理依据 | 建议 |
|---|---|---:|---:|---:|---|---|
| TMP00044547 | 物理连接不一致 | 0.60 | [0.70, 0.90] | CONFIRMED | 端子连接错误 | 建议核查连接关系 |
| TMP00131880 | 逻辑连接不一致 | 0.55 | [0.65, 0.85] | LIKELY | 拓扑逻辑不符 | 现场核查 |

### 修复排序表格

| 排序 | 设备ID | 动作 | 优先级 | 风险降低 | 约束恢复 |
|---|---|---|---|---|---|
| 1 | TMP00044547 | ADD_CONNECTION | 0.85 | 0.90 | 0.95 |
| 2 | TMP00131880 | UPDATE_CONNECTION | 0.78 | 0.80 | 0.70 |

## 依赖要求

```
pandas>=1.3.0
networkx>=2.6.0
openpyxl>=3.0.0
```

## 技术亮点

### 1. 多源数据融合
- SQL数据库 + SVG图纸 + 遥测数据 + 新能源出力

### 2. 物理约束可解释性
- KCL电流平衡、支路约束、合环检测
- 每条异常都有物理依据支撑

### 3. II型模糊可信度
- 解决"数据不可靠时如何做判断"
- CONFIRMED/LIKELY/PENDING/FALSE_ALARM 四级状态

### 4. 智能修复排序
- 优先级 = 置信度×0.3 + 风险降低量×0.4 + 约束恢复×0.3 - 影响惩罚
- 影响范围评估（关键设备、联络点）

### 5. 完整可回滚
- 正向修复SQL + 逆向回滚SQL

## 答辩展示要点

1. **数据流清晰**：SQL→SVG→遥测→统一拓扑图→异常检测→报告
2. **物理可解释**：每个异常都有基尔霍夫定律等物理依据
3. **可信度透明**：II型模糊集合处理数据不确定性
4. **闭环完整**：检测→排序→修复→回滚
5. **量化指标**：评分、置信度、风险等级、修复成功率

## 常见问题

### Q: 增强报告生成失败？
检查新模块是否正确导入：
```python
from core.enhanced_report_generator import EnhancedReportGenerator
```

### Q: 遥测质量为0？
确保 `measure_preprocess.py` 正确匹配开关类型（使用 `constants.SWITCH_TYPES`）

### Q: 如何调整权重？
修改对应模块中的权重常量：
- `physical_constraint_checker.py`: `ComprehensiveRiskScore.WEIGHTS`
- `repair_ranking_engine.py`: `RepairCandidate.calculate_priority()`

## 许可证

本项目仅供学术研究和竞赛使用。
