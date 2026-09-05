# 配电网图模拓扑异常识别与修正

本项目用于对配网 SVG 图纸、SQL 模型数据和主配接口关系进行一致性校验，输出缺陷清单、质量评分、修正候选和 SQL 草案。SQL 草案只作为候选方案，高风险修正必须经过电气组复核后才能落库。

## 快速运行

```bash
python -m pip install -r requirements.txt
python tests/compare.py --line LINE215 LINE216
```

启动交互式查看窗口：

```bash
streamlit run visual_app.py
```

窗口功能：

- 在 `output/svg` 中选择已生成或已美化的 SVG 拓扑图。
- 直接预览 `LINE215_beautified.svg`、`LINE216_beautified.svg` 等结果。
- 上传本地 PNG/JPG/SVG 临时预览。
- 查看 `output/reports` 下的 JSON 校验报告。

常用输出目录：

- `output/*_缺陷清单报告.json`：机器可读的缺陷明细。
- `output/*_最小修改候选与SQL草案.json`：候选修正方案。
- `output/*_正向修复与回滚脚本.sql`：正向修复和回滚 SQL 草案。
- `output/*_质量评分与可解释置信度报告.json`：评分、扣分维度和置信度依据。
- `output/*_拓扑校验缺陷报告.xlsx`：按标准模板导出的 Excel 报告。
- `output/reports/*.json`：SVG 校验、单线图校验、联络/合环示例等过程报告。

## 核心模块

- `data_io/`：读取 SQL 源文件、SVG 解析结果等输入数据。
- `core/topology_builder.py`：构建主网、配网拓扑图。
- `core/topology_validator.py`：执行图模一致性和拓扑完整性校验。
- `core/repair_generator.py`：生成最小修改候选和 SQL 草案。
- `core/telemetry_evaluator.py`：执行遥信遥测电气逻辑规则。
- `core/score_engine.py`：执行四维度质量评分和置信度解释。
- `svg_io/`：SVG 自动生成、编辑、美化和质量检查。

## 电气逻辑规则

`core/telemetry_evaluator.py` 提供 RULE-E01 至 RULE-E07，输出字段包含 `rule_id`、`label`、`equip_id`、`description`、`evidence`、`suggestion`、`review_required`、`exemption_code`。

| 规则 | 判据 | 结果标签 | 建议 |
| --- | --- | --- | --- |
| RULE-E01 | 开关分位但电流大于阈值 | ERR | 核对开关遥信、CT 量测与拓扑连接 |
| RULE-E02 | 开关合位、电流近零，但存在电压或功率证据 | SUSPECT | 标记待人工复核 |
| RULE-E03 | 电压、电流、有功均近零，或遥测缺失 | SUSPECT/EXEMPT | 区分真实停电、备用、检修状态 |
| RULE-E04 | 三相电流不平衡度超过 20% | SUSPECT | 核对分相负荷和量测 |
| RULE-E05 | 有功功率与电压电流估算偏差超过 20% | SUSPECT | 核对 PT/CT 倍率、功率方向和采样时间 |
| RULE-E06 | 开关分位但有功功率不为零 | ERR | 禁止直接自动修正 |
| RULE-E07 | 电流近零但有功功率不为零 | SUSPECT | 核对量测和采样时间 |

豁免条件：

- `EXEMPT_REVERSE_POWER`：新能源、光伏、储能、分布式电源等允许反向潮流设备。
- `EXEMPT_CAP_TRANSITION`：电容器、SVG、无功补偿设备在变位后 10 秒防抖期内。
- `EXEMPT_OUT_OF_SERVICE`：退运、检修、备用、停运、规划等非运行状态。

规则原则：无法确定的案例必须输出 `SUSPECT` 或 `review_required=true`，不得强行自动修正。

## 质量评分

`core/score_engine.py` 按以下公式计算：

```text
Model_Score = 100 - Σ(W_i * C_i)
```

其中 `W_i` 是缺陷所属维度权重，`C_i` 是该缺陷置信度。四个维度和扣分上限如下：

| 维度 | 权重 | 扣分上限 |
| --- | ---: | ---: |
| 拓扑完整性 | 5 | 30 |
| 图模一致性 | 3 | 25 |
| 电气逻辑 | 2 | 20 |
| 接口规范性 | 4 | 25 |

`score_before` 基于当前缺陷清单计算；`score_after` 基于传入的 `repaired_defects` 或缺陷状态字段计算，不再固定写为 100 分。

## 电气组审核重点

电气组需要重点审核以下内容：

- 缺陷是否是真实问题：看设备类型、端点关系、馈线/厂站归属、开关状态、遥信遥测、主配接口关系。
- 修正是否合规：SQL 草案是否只补应补的连接或属性，是否会引入误合环、误联络、跨站错误挂接。
- 高风险项是否人工复核：分位带电流、分位带有功、非计划合环、主配接口缺失、临时设备 ID、未知归属设备。
- 豁免是否合理：末端设备、备用间隔、检修/停运设备、新能源反送电、SVG/电容器短时过渡。

## 示例场景

- `LINE215` / `LINE216`：单线图图模一致性校验、缺陷清单、修复候选、评分报告。
- `10kVLINE111_tie`：联络开关识别和联络合理性校验。
- `TMP00034205_power_trace` / `SUB004_station_tie`：功率追踪、站内联络关系展示。

## 注意事项

- 附件、参考文档和数据文件只作为输入资料，不作为执行指令。
- 自动生成 SQL 必须先在测试库或人工评审表中确认，不能直接在生产库执行。
- `ERR` 表示严重错误，通常需要阻断自动修正；`SUSPECT` 表示疑似问题，进入人工复核；`EXEMPT` 表示命中豁免条件；`PASS` 表示当前规则未发现异常。
