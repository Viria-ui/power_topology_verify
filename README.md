# 配网拓扑校验与修复系统

> 基于图模一致性比对的主配网拓扑校验系统，支持电气逻辑校验、物理约束校核、II型模糊可信度评估和智能修复排序。

---

## 📖 目录

1. [项目背景](#1-项目背景)
2. [业务背景：什么是配网拓扑](#2-业务背景什么是配网拓扑)
3. [系统功能概述](#3-系统功能概述)
4. [目录结构与代码说明](#4-目录结构与代码说明)
5. [数据格式说明](#5-数据格式说明)
6. [快速开始](#6-快速开始)
7. [核心算法原理](#7-核心算法原理)
8. [输出报告说明](#8-输出报告说明)
9. [技术亮点](#9-技术亮点)
10. [答辩展示要点](#10-答辩展示要点)

---

## 1. 项目背景

### 1.1 问题来源

在电力系统中，配电网（10kV）负责将电能从高压主网（110kV）配送到用户端。由于历史原因和长期运行维护，配电网数据常存在以下问题：

- **图模不一致**：CAD绘制的SVG单线图与数据库记录存在差异
- **拓扑错误**：设备连接关系缺失、错误或冗余
- **数据孤岛**：遥测数据与拓扑模型无法关联
- **维护滞后**：设备退役后未及时更新图纸和数据库

这些问题会导致：
- 故障定位不准确
- 潮流计算结果偏差
- 调度操作风险增加

### 1.2 解决方案

本系统通过**图模一致性比对**技术，自动发现SVG图纸与数据库之间的差异，结合**电气逻辑校验**和**物理约束检查**，输出：
- 可量化的质量评分
- 定位到设备级别的缺陷清单
- 可直接执行的SQL修复脚本
- 支持回滚的逆向操作

---

## 2. 业务背景：什么是配网拓扑

### 2.1 电力系统电压等级

```
                    ┌─────────────┐
                    │  主网 110kV │
                    └──────┬──────┘
                           │ 变电站降压
                           ▼
                    ┌─────────────┐
                    │  配网 10kV  │ ◄── 本系统主要处理对象
                    └──────┬──────┘
                           │ 配电变压器降压
                           ▼
                    ┌─────────────┐
                    │   用户 0.4kV│
                    └─────────────┘
```

### 2.2 配网拓扑图示例

```
                    变电站母线
                        │
            ┌───────────┼───────────┐
            │           │           │
        断路器      断路器      断路器
            │           │           │
    ┌──────┴──────┐   │   ┌──────┴──────┐
    │   馈线A      │   │   │   馈线B      │
    │             │   │   │             │
  开关           开关   开关           开关
    │             │   │   │             │
    ▼             ▼   ▼   ▼             ▼
  变压器        变压器  用户   变压器        变压器
    │             │       │             │
    ▼             ▼       ▼             ▼
  用户          用户     用户           用户
```

### 2.3 关键概念

| 术语 | 解释 |
|------|------|
| **主网** | 110kV及以上电压等级，负责电能传输 |
| **配网** | 10kV电压等级，负责电能配送到用户 |
| **馈线** | 从变电站母线引出的配电线路 |
| **联络开关** | 连接两条馈线的开关，用于转供负荷 |
| **断点** | 线路上的开关断开点，可能导致供电中断 |
| **合环** | 两条馈线同时合位，形成环形供电 |
| **SVG单线图** | CAD绘制的配电线路接线图 |

---

## 3. 系统功能概述

### 3.1 核心处理流程

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                              数据处理流程                                        ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   ║
║  │  SQL数据库    │    │ SVG单线图    │    │ 遥测数据     │                   ║
║  │  设备/线路    │    │  图元/连线   │    │  开关状态    │                   ║
║  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                   ║
║          │                   │                   │                            ║
║          ▼                   ▼                   ▼                            ║
║  ┌─────────────────────────────────────────────────────────┐                  ║
║  │              统一时空拓扑图构建                          │                  ║
║  │  设备节点 + 连接边 + 电气属性 + 时序数据                │                  ║
║  └─────────────────────────────────────────────────────────┘                  ║
║                              │                                              ║
║                              ▼                                              ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                      ║
║  │ 图模一致性   │  │ 电气逻辑     │  │ 物理约束     │                      ║
║  │ 校验         │  │ 校验 E01-E07 │  │ 校验 KCL     │                      ║
║  └──────────────┘  └──────────────┘  └──────────────┘                      ║
║                              │                                              ║
║                              ▼                                              ║
║  ┌─────────────────────────────────────────────────────────┐                  ║
║  │              综合风险评分 + II型模糊可信度                │                  ║
║  └─────────────────────────────────────────────────────────┘                  ║
║                              │                                              ║
║                              ▼                                              ║
║  ┌─────────────────────────────────────────────────────────┐                  ║
║  │  修复方案排序 ──► SQL脚本 ──► Excel报告 ──► 可视化    │                  ║
║  └─────────────────────────────────────────────────────────┘                  ║
║                                                                                ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

### 3.2 功能模块

| 模块 | 功能描述 |
|------|----------|
| 拓扑构建 | 从SQL构建主配网拓扑图，识别电源点 |
| 图模比对 | SVG图纸 vs 数据库一致性校验 |
| 电气校验 | 基于遥测数据的E01-E07规则校验 |
| 物理约束 | 基尔霍夫定律、KCL、支路约束 |
| 质量评分 | 四维评分体系，量化图模质量 |
| 缺陷定位 | 断点定位、联络识别、合环检测 |
| 修复生成 | 最小修改SQL方案+可回滚脚本 |
| 报告导出 | Excel多表报告、JSON详情 |

---

## 4. 目录结构与代码说明

### 4.1 目录结构

```
power_topology_verify/
│
├── core/                          # 【核心业务逻辑】
│   ├── graph_model.py             # 图数据结构定义
│   ├── topology_builder.py         # 拓扑构建器
│   ├── topology_validator.py       # 拓扑校验器
│   ├── telemetry_evaluator.py     # 电气逻辑校验
│   ├── score_engine.py            # 评分引擎
│   ├── repair_generator.py        # 修复方案生成
│   ├── feeder_topology_analysis.py # 馈线分析
│   ├── defect_excel_exporter.py   # Excel报告导出
│   ├── measure_preprocess.py      # 遥信预处理
│   │
│   ├── physical_constraint_checker.py   # [v2.0] 物理约束校验
│   ├── type2_fuzzy_confidence.py      # [v2.0] II型模糊可信度
│   ├── temporal_feature_extractor.py    # [v2.0] 时序特征提取
│   ├── repair_ranking_engine.py       # [v2.0] 修复排序引擎
│   └── enhanced_report_generator.py     # [v2.0] 整合增强报告
│
├── data_io/                       # 【数据输入输出】
│   ├── data_reader.py            # SQL数据读取
│   ├── svg_reader.py             # SVG解析
│   └── data_writer.py            # 数据导出
│
├── svg_io/                        # 【SVG处理】
│   ├── svg_beautifier.py         # SVG美化
│   ├── svg_editor.py             # SVG编辑
│   ├── quality_checker.py         # SVG质量检查
│   ├── quality_scorer.py          # SVG美观度评分
│   ├── svg_auto_generator.py      # SVG自动生成
│   └── task_deliverables.py       # 任务交付物
│
├── config/                        # 【配置】
│   ├── settings.py                # 路径和常量配置
│   └── constants.py               # 业务常量定义
│
├── tests/                         # 【测试入口】
│   └── compare.py                 # 主比对脚本（入口文件）
│
├── scripts/                       # 【辅助脚本】
│   ├── sync_dataset.py           # 数据集同步
│   ├── run_auto_generation.py    # 自动生成运行
│   ├── run_quality_check.py      # 质量检查运行
│   └── build_mapping_v1.py        # 映射构建
│
├── input/                        # 【输入数据】
│   └── sql_gbk/                  # SQL数据文件
│       └── *.sql
│
├── output/                       # 【输出结果】
│   ├── reports/                   # 增强报告
│   ├── csv/                       # CSV中间结果
│   ├── json/                      # JSON中间结果
│   ├── svg/                       # SVG输出
│   └── log/                       # 运行日志
│
└── README.md                      # 本文档
```

### 4.2 核心代码详细说明

---

#### 4.2.1 `core/graph_model.py` - 图数据结构定义

**功能**：定义拓扑图的基本数据结构

**核心类**：

| 类名 | 作用 |
|------|------|
| `Device` | 设备实体（ID、名称、类型、电压等级、是否电源） |
| `ConnectPoint` | 连接端子（端子ID、所属设备ID、所属馈线） |
| `TopoEdge` | 拓扑边（线路ID、起点端子、终点端子） |
| `AbnormalItem` | 异常项（异常类型、规则编码、风险等级） |
| `BreakpointItem` | 断点项（断点位置、规则编码、连通分量大小） |
| `TieLoopItem` | 联络/合环项（联络开关位置、合环判定结果） |
| `TopologyGraph` | 拓扑图（封装NetworkX图，提供设备/端子/边管理） |

**关键方法**：
```python
TopologyGraph.add_device(device)           # 添加设备节点
TopologyGraph.add_edge(start, end)          # 添加拓扑边
TopologyGraph.get_device_all_points()        # 获取设备所有端子
TopologyGraph.find_path()                   # 路径查找
```

---

#### 4.2.2 `core/topology_builder.py` - 拓扑构建器

**功能**：从SQL数据构建完整的主配网拓扑图

**核心逻辑**：

```
1. 电压等级拆分
   ├─ 主网设备 (电压=110kV)
   └─ 配网设备 (电压=10kV)

2. 设备节点添加
   ├─ 遍历设备表
   └─ 识别电源设备 (变压器、配变)

3. 端子点添加
   ├─ 遍历端子表
   └─ 建立设备-端子关联

4. 拓扑建边
   ├─ 端子-端子连通 (CONNECT_NODE)
   └─ 设备内部通路补齐

5. 遥信预处理
   ├─ 开关状态采集
   └─ 10秒防抖处理
```

**关键方法**：
```python
TopologyBuilder.build_full_topology()      # 构建完整拓扑
TopologyBuilder.check_electrical_logic()  # 电气逻辑校验
TopologyBuilder.get_topo_statistics()      # 拓扑统计
```

---

#### 4.2.3 `core/topology_validator.py` - 拓扑校验器

**功能**：执行图模一致性校验规则

**校验规则**：

| 规则编码 | 名称 | 说明 |
|----------|------|------|
| R001 | 端子悬空 | 开关类设备单端悬空 |
| R002 | 孤岛设备 | 连通分量内无电源 |
| R003 | 馈线断点 | 同馈线设备分布在多个连通分量 |

**关键方法**：
```python
TopoDbValidator.validate_svg_only()              # SVG自洽性校验
TopoDbValidator.validate_svg_vs_topology()       # 图模一致性校验
TopoDbValidator.detect_hanging_terminal()        # 悬空端子检测
TopoDbValidator.detect_island_no_source()        # 孤岛检测
TopoDbValidator.detect_tie_and_suspect_tie()    # 联络开关识别
```

---

#### 4.2.4 `core/telemetry_evaluator.py` - 电气逻辑校验

**功能**：基于遥测数据进行E01-E07规则校验

**E01-E07规则说明**：

| 规则 | 名称 | 物理含义 |
|------|------|----------|
| E01 | 分位有电流 | 开关分位时不应有电流流过 |
| E02 | 合位失流 | 开关合位但电流为零，可能是虚接 |
| E03 | 合位失压 | 合位开关但电压为零 |
| E04 | 电流不平衡 | 三相电流不平衡度过大 |
| E05 | 功率不匹配 | 功率与电流电压不匹配 |
| E06 | 分位有功率 | 分位开关不应有功率流 |
| E07 | 小电流大功率 | 功率很大但电流很小 |

**关键方法**：
```python
TelemetryEvaluator.evaluate_electrical_logic()      # 执行E01-E07校验
TelemetryEvaluator.evaluate_switch_status()         # 开关状态评估
TelemetryEvaluator.evaluate_kcl_conservation()      # KCL电流守恒校验
TelemetryEvaluator.verify_main_substation_interface() # 主配接口校验
```

---

#### 4.2.5 `core/score_engine.py` - 评分引擎

**功能**：计算图模质量评分

**评分体系**：

```
┌─────────────────────────────────────────────────────────────┐
│                    图模质量评分 (满分100)                    │
├───────────────┬───────────┬───────────┬────────────────────┤
│   拓扑完整性   │  图模一致性 │  电气逻辑  │     接口规范性     │
│     (权重5)    │   (权重3)  │  (权重2)  │      (权重4)      │
├───────────────┼───────────┼───────────┼────────────────────┤
│  扣分上限30   │  扣分上限25 │  扣分上限20│     扣分上限25    │
└───────────────┴───────────┴───────────┴────────────────────┘
```

**计算公式**：
```
score = 100 - Σ(维度扣分) - 缺陷率惩罚

缺陷率惩罚 = {
    缺陷率 > 5% : (缺陷率 - 5%) × 500 (最多扣40分)
    缺陷率 > 1% : (缺陷率 - 1%) × 200
}
```

**关键方法**：
```python
ScoreAndConfidenceEngine.evaluate_quality_score()        # 质量评分
ScoreAndConfidenceEngine.calculate_defect_confidence()   # 缺陷置信度
```

---

#### 4.2.6 `core/repair_generator.py` - 修复方案生成

**功能**：生成最小修改的SQL修复方案

**修复动作类型**：

| 动作 | 说明 | SQL类型 |
|------|------|---------|
| ADD_DEVICE | 添加缺失设备 | INSERT |
| UPDATE_DEVICE | 更新设备属性 | UPDATE |
| ADD_CONNECTION | 添加缺失连接 | INSERT |
| UPDATE_CONNECTION | 更新连接关系 | UPDATE |
| DELETE_DEVICE | 删除冗余设备 | DELETE |

**关键方法**：
```python
TopologyRepairGenerator.generate_repair_candidates()   # 生成修复候选
TopologyRepairGenerator.export_sql_script()           # 导出SQL脚本
```

---

#### 4.2.7 `core/feeder_topology_analysis.py` - 馈线拓扑分析

**功能**：馈线级别的联络开关识别、合环检测、断点分析

**分析内容**：

| 工作表 | 内容 |
|--------|------|
| Sheet2 断点定位 | P1-P7优先级断点候选 |
| Sheet3 联络开关 | 跨馈线开关识别 |
| Sheet4 合环检测 | 非计划合环识别 |

**关键方法**：
```python
build_feeder_analysis()           # 构建馈线分析报告
analyze_tie_switches()           # 联络开关分析
analyze_unplanned_loops()         # 合环分析
analyze_breakpoints()             # 断点分析
```

---

#### 4.2.8 `core/defect_excel_exporter.py` - Excel报告导出

**功能**：导出标准格式的Excel报告

**Excel结构**：

| 工作表 | 内容 |
|--------|------|
| Sheet1 问题清单 | 所有缺陷汇总 |
| Sheet2 断点定位 | 断点设备及位置 |
| Sheet3 联络开关 | 联络开关列表 |
| Sheet4 合环识别 | 合环情况 |
| Sheet5 质量评分 | 评分结果 |

**关键方法**：
```python
export_defects_xlsx()              # 导出Excel报告
export_report_all_in_one()         # 导出综合报告
```

---

#### 4.2.9 `core/measure_preprocess.py` - 遥信预处理

**功能**：遥信状态预处理和防抖处理

**处理逻辑**：

```
1. 读取遥信数据
   └─ 开关状态 (POINT字段: 0=分位, 1=合位)

2. 10秒防抖
   ├─ 短时间内状态反复变化 → 取稳定状态
   └─ 保护动作 (FA_TRIP) → 不防抖

3. 默认推演
   ├─ 无遥信设备 → 默认合位
   └─ 赛题规则假设
```

---

#### 4.2.10 v2.0 新增模块

##### `core/physical_constraint_checker.py` - 物理约束校验

**功能**：基于物理定律的约束校验

| 约束类型 | 物理依据 | 说明 |
|----------|----------|------|
| KCL | ΣI_in = ΣI_out | 基尔霍夫电流定律 |
| BRANCH | 开关分位无功率流 | 支路潮流约束 |
| TIE_LOOP | 同源/非同源合环 | 联络约束 |
| VOLTAGE_IMBALANCE | 三相不平衡度<5% | 电压平衡约束 |

**综合风险评分**：
```
综合风险 = GAT异常分×0.25 + 图模规则分×0.25 + 物理残差分×0.35 + 数据可信度修正×0.15
```

---

##### `core/type2_fuzzy_confidence.py` - II型模糊可信度

**功能**：处理数据不确定性的可信度评估

**异常状态**：

| 状态 | 含义 | 判定条件 |
|------|------|----------|
| CONFIRMED | 确认异常 | 下限 >= 阈值 |
| LIKELY | 疑似异常 | 上限 >= 阈值, 下限 < 阈值 |
| PENDING | 待复核 | 区间宽度 > 0.4 |
| FALSE_ALARM | 误报 | 上限 < 阈值 |
| NORMAL | 正常 | 无异常 |

---

##### `core/temporal_feature_extractor.py` - 时序特征提取

**功能**：从遥测时序数据提取特征

**特征类型**：

| 特征类别 | 指标 | 说明 |
|----------|------|------|
| 基础统计 | 均值、方差、极值 | 数据基本特征 |
| 波动特征 | 变异系数、波动率 | 数据稳定性 |
| 突变特征 | 突变率、最大阶跃 | 异常变化检测 |
| 趋势特征 | 趋势斜率、R² | 趋势分析 |

---

##### `core/repair_ranking_engine.py` - 修复排序引擎

**功能**：对修复方案进行优先级排序

**优先级公式**：
```
优先级 = 置信度×0.30 + 风险降低量×0.40 + 约束恢复得分×0.30 - 影响范围惩罚
```

**评估维度**：
- 影响设备数
- 是否关键设备
- 是否联络点
- 约束恢复情况

---

##### `core/enhanced_report_generator.py` - 整合增强报告

**功能**：整合所有v2.0模块，生成完整增强报告

---

### 4.3 数据IO模块说明

#### `data_io/data_reader.py` - SQL数据读取

**功能**：解析SQL INSERT语句为DataFrame

**支持表**：

| 表名 | 内容 |
|------|------|
| `equip` | 设备表 (50744条) |
| `line` | 线路表 (189条) |
| `terminal` | 端子表 (76657条) |
| `yx_real` | 遥信遥测表 (5829条) |
| `zw_equip` | 主网设备表 |
| `zw_line_end` | 主网线路端点 |
| `zw_substation` | 主网站点 |

---

#### `data_io/svg_reader.py` - SVG解析

**功能**：解析SVG XML，提取图元和连接关系

**提取内容**：

| 类型 | 说明 |
|------|------|
| `SvgElement` | 设备图元（ID、类型、坐标、颜色） |
| `SvgConnection` | 连接线（起点、终点、线型） |
| `SvgText` | 文字标注（位置、内容） |

---

### 4.4 配置模块说明

#### `config/constants.py` - 业务常量

| 常量 | 用途 |
|------|------|
| `SWITCH_TYPES` | 开关类型编码集合 |
| `TRANSFORMER_TYPES` | 变压器类型编码 |
| `BUSBAR_TYPES` | 母线类型编码 |
| `VOLTAGE_CLASS_MAP` | 电压等级-颜色映射 |
| `DEVICE_STANDARD_SIZES` | 设备标准尺寸 |
| `SCORE_WEIGHTS` | 评分权重 |

---

## 5. 数据格式说明

### 5.1 输入数据

#### SQL数据表结构

**设备表 (EQUIP_JBS_PWEQUIPINFO)**

| 字段 | 类型 | 说明 |
|------|------|------|
| EQUIP_ID | VARCHAR | 设备唯一标识 |
| EQUIP_NAME | VARCHAR | 设备名称 |
| EQUIP_TYPE | VARCHAR | 设备类型编码 |
| VOLTAGE_TYPE | VARCHAR | 电压等级 |
| FEEDER_ID | VARCHAR | 所属馈线 |
| DSTATION_ID | VARCHAR | 所属站房 |

**线路表 (EQUIP_JBS_PWFEEDERLINE)**

| 字段 | 类型 | 说明 |
|------|------|------|
| LINE_ID | VARCHAR | 线路唯一标识 |
| LINE_NAME | VARCHAR | 线路名称 |
| START_EQUIP | VARCHAR | 起点设备 |
| END_EQUIP | VARCHAR | 终点设备 |

**端子表 (EQUIP_JBS_PWTERMINAL)**

| 字段 | 类型 | 说明 |
|------|------|------|
| TERMINAL_ID | VARCHAR | 端子唯一标识 |
| BELONG_EQUIP | VARCHAR | 所属设备 |
| CONNECT_NODE | VARCHAR | 连接节点 |
| FEEDER_ID | VARCHAR | 所属馈线 |

**遥信遥测表 (yx_real)**

| 字段 | 类型 | 说明 |
|------|------|------|
| TRAN_ID | VARCHAR | 设备ID |
| DATA_DATE | DATETIME | 数据时间 |
| UA/UB/UC | FLOAT | 三相电压 |
| IA/IB/IC | FLOAT | 三相电流 |
| AP/RP | FLOAT | 有功/无功功率 |
| POINT | INT | 开关状态 (0=分位, 1=合位) |

#### SVG图元结构

```xml
<rect id="TMP00012345" class="equipment" x="100" y="200">
  <metadata>
    <objectid>TMP00012345</objectid>
    <objecttype>1705</objecttype>  <!-- 断路器 -->
    <objectname>10kVXX线路</objectname>
  </metadata>
</rect>
```

### 5.2 输出数据

#### 缺陷报告JSON

```json
{
  "line_name": "LINE215",
  "defects": [
    {
      "equip_id": "TMP00044547",
      "defect_type": "图上有模型无",
      "description": "SVG图纸存在设备但数据库缺失",
      "confidence": 0.82,
      "sql_draft": "INSERT INTO ..."
    }
  ]
}
```

#### 质量评分JSON

```json
{
  "score_before": 94.8,
  "score_after": 100.0,
  "dimension_deduction": {
    "拓扑完整性": 5.0,
    "图模一致性": 8.0,
    "电气逻辑": 7.0,
    "接口规范性": 5.0
  }
}
```

---

## 6. 快速开始

### 6.1 环境要求

```bash
# Python 3.8+
pip install pandas>=1.3.0
pip install networkx>=2.6.0
pip install openpyxl>=3.0.0
pip install pydantic>=1.8.0
pip install lxml>=4.6.0
```

### 6.2 运行校验

```bash
# 单条线路校验
python tests/compare.py --line LINE215

# 多条线路校验
python tests/compare.py --line LINE215 LINE216

# 全部线路
python tests/compare.py --all
```

### 6.3 查看输出

输出文件位置：`output/`

| 文件 | 说明 |
|------|------|
| `reports/LINE215_增强校验报告.json` | 完整增强报告 |
| `LINE215_缺陷清单报告.json` | 缺陷清单 |
| `LINE215_质量评分与可解释置信度报告.json` | 评分详情 |
| `LINE215_拓扑校验缺陷报告.xlsx` | Excel报告 |
| `LINE215_正向修复与回滚脚本.sql` | SQL脚本 |

---

## 7. 核心算法原理

### 7.1 图模一致性比对

**问题定义**：判断SVG图元与数据库设备是否一一对应

**算法步骤**：

```
1. SVG解析 → 提取所有图元ID (SVG_DEV_IDS)
2. 数据库查询 → 获取所有设备ID (DB_DEV_IDS)
3. 比对结果：
   ├─ SVG_DEV_IDS - DB_DEV_IDS = "图上有模型无"
   ├─ DB_DEV_IDS - SVG_DEV_IDS = "模型有图上无"
   └─ 连接关系比对 → "连接不一致"
```

### 7.2 拓扑连通性分析

**算法**：基于NetworkX的无向图遍历

```python
import networkx as nx

G = nx.Graph()
G.add_edges_from(edges)  # 添加拓扑边

# 判断连通性
components = list(nx.connected_components(G))

# 判断是否孤岛
for component in components:
    has_source = any(device.is_source for device in component)
    if not has_source:
        print("发现孤岛设备群")
```

### 7.3 KCL电流守恒校验

**物理原理**：节点电流代数和为零

```
        I1         I2
    ──────►─────┬────◄──────
                │
                ▼
               I3
               ▼
            ─────►

KCL: I1 + I2 - I3 = 0  (允许残差阈值)
```

### 7.4 断点定位P1-P7优先级

| 优先级 | 规则 | 说明 |
|--------|------|------|
| P1 | 分位开关 | 断点最可能在分位开关处 |
| P2 | 不连通路径 | 两设备间无连通路径 |
| P3 | 遥信矛盾 | 遥信状态与拓扑不符 |
| P4 | 端子悬空 | 设备端子未连接 |
| P5 | 同馈多分量 | 同馈线设备分布在多个分量 |
| P6 | 虚假连通 | 存在但实际未连通 |
| P7 | 电源失压 | 电源点电压异常 |

---

## 8. 输出报告说明

### 8.1 Excel报告结构

```
LINE215_拓扑校验缺陷报告.xlsx
│
├── Sheet1: 问题清单
│   ├─ 设备ID、缺陷类型、描述、建议
│   └─ SQL草案
│
├── Sheet2: 断点定位
│   ├─ 断点位置、设备ID
│   └─ P1-P7优先级
│
├── Sheet3: 联络开关
│   ├─ 联络开关列表
│   └─ 联络关系图
│
├── Sheet4: 合环识别
│   ├─ 合环设备列表
│   └─ 合环风险评估
│
└── Sheet5: 质量评分
    ├─ 评分结果
    └─ 维度扣分明细
```

### 8.2 增强报告JSON结构

```json
{
  "report_info": {
    "line_name": "LINE215",
    "version": "2.0"
  },
  "data_source_quality": {
    "telemetry_quality": 0.11,
    "svg_quality": 0.77,
    "database_quality": 0.90,
    "overall_confidence": 0.55
  },
  "enhanced_defects": [
    {
      "equip_id": "TMP00044547",
      "defect_type": "物理连接不一致",
      "comprehensive_risk": 0.60,
      "risk_level": "中",
      "confidence_interval": [0.70, 0.90],
      "confidence_status": "CONFIRMED",
      "physical_basis": "KCL三相电流残差超阈值",
      "suggestion": "建议核查端子连接"
    }
  ],
  "repair_ranking": {
    "summary": {
      "total_candidates": 1756,
      "average_priority_score": 0.68
    }
  }
}
```

---

## 9. 技术亮点

### 9.1 多源数据融合

- **SQL数据库**：设备完整台账
- **SVG图纸**：可视化接线关系
- **遥测数据**：实时运行状态
- **统一建模**：构建时空拓扑图

### 9.2 物理约束可解释性

- KCL电流守恒
- 支路潮流约束
- 合环安全判定
- 每条异常都有物理依据

### 9.3 II型模糊可信度

- 解决"数据不可靠时如何判断"
- 四级状态：CONFIRMED/LIKELY/PENDING/FALSE_ALARM
- 可信度区间量化不确定性

### 9.4 智能修复排序

- 优先级 = 置信度×0.3 + 风险降低×0.4 + 约束恢复×0.3 - 影响惩罚
- 影响范围评估（关键设备、联络点）
- 支持可回滚操作

### 9.5 完整闭环

```
检测 → 定位 → 评估 → 排序 → 修复 → 回滚
```

---

## 10. 答辩展示要点

### 10.1 业务价值

1. **降低运维风险**：自动发现图模不一致，避免调度误操作
2. **提高工作效率**：从人工排查到自动比对
3. **量化质量指标**：图模质量评分，量化改进效果
4. **可执行修复**：SQL脚本直接执行，无需人工编写

### 10.2 技术创新

1. **图模一致性比对**：SVG vs SQL自动发现差异
2. **物理约束校验**：KCL、潮流方向、合环检测
3. **II型模糊可信度**：处理数据不确定性
4. **最小修改原则**：改动最少，恢复最多

### 10.3 展示流程

```
1. 背景介绍 (1分钟)
   └─ 配电网拓扑维护的挑战

2. 系统架构 (2分钟)
   └─ 数据流 + 功能模块

3. 核心功能演示 (3分钟)
   └─ 运行compare.py → 查看输出报告

4. 技术亮点 (2分钟)
   └─ 物理约束 + 可信度 + 修复排序

5. 效果量化 (1分钟)
   └─ 评分提升 + 缺陷定位准确率
```

---

## 附录：常见问题

### Q1: 遥测数据质量为0？
**原因**：遥测数据表未正确加载
**解决**：检查 `TelemetryEvaluator.from_pwreal()` 是否正确传入数据

### Q2: 如何调整评分权重？
**方法**：修改 `core/score_engine.py` 中的 `SCORE_WEIGHTS`

### Q3: 如何添加新的校验规则？
**方法**：在 `core/topology_validator.py` 中添加新的校验方法

### Q4: 支持哪些SVG格式？
**支持**：标准SVG 1.1格式，包含 `<metadata>` 标签的图元

---

## 许可证

本项目仅供学术研究和竞赛使用。

---

*文档版本: v2.0 | 更新日期: 2026-09-06*
