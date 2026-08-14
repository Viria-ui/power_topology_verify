# SVG 拓扑图形美化算法分析与设计方案

## 一、问题诊断：为什么 AI 生成的美化代码不工作

### 1.1 三个核心 Bug（已修复）

| # | 问题 | 现象 | 根因 | 修复方案 |
|---|------|------|------|----------|
| 1 | 坐标缩放导致 viewBox 膨胀 | 文字不可见、图形溢出 | `_normalize_coordinate_scale` 将所有坐标乘以 18 倍因子，但未同步缩放设备尺寸和字号 | **禁用该步骤**，保持原始坐标空间 |
| 2 | Transform 处理丢失 scale 分量 | 设备图形偏移、变形 | `_normalize_device_icons` 将 transform 替换为仅 `rotate()`，丢失了原始的 `scale(0.02)` 分量，且 symbol 内容以 (0,0) 为中心 | 保留旋转分量，scale 由 width/height 属性控制，旋转中心使用新位置中心 |
| 3 | 文字位置不同步设备移动 | 文字标注与设备脱节 | `text_device_map` 在设备移动（步骤 3-8）之后才构建，导致设备移动时文字无法同步 | 将 `text_device_map` 构建提前到 `_build_station_map` 之后、`_normalize_device_icons` 之前 |

### 1.2 连锁 Bug（已修复）

| # | 问题 | 现象 | 根因 | 修复方案 |
|---|------|------|------|----------|
| 4 | 网格吸附只向右偏移 | 设备堆积在同一行，x 坐标达到 4000+ | `_snap_to_grid` 的去重逻辑遇到占用网格点时只向右偏移，1366 个设备全堆在同一行 | 改为先尝试向下偏移，再尝试向上，最后才向右偏移 |
| 5 | 站房 polygon 扩展不生效 | 站房始终为原始微小尺寸（7.8×3.3） | Substation 是 polygon 元素，`_assign_coords_by_layers` 更新了 `elem.width` 但 SVG Writer 对 polygon 使用原始 `points` 属性 | 同步更新 `shape_attrs["points"]`；修改 Writer 代码从 `shape_attrs` 读取最新 points |

---

## 二、美化算法架构设计

### 2.1 整体流水线（Pipeline）

```
原始 SVG
  │
  ├─ 1. 解析与中间模型构建（SvgDocument.parse）
  │     ├─ 提取设备图元（use/rect/polygon/path/circle）
  │     ├─ 提取连接关系（Connection）
  │     ├─ 提取文字标注（Text）
  │     └─ 构建 element_id → SvgElement 索引
  │
  ├─ 2. 站房映射（_build_station_map）
  │     ├─ 识别 Substation 图层的 polygon 元素
  │     ├─ 判断设备是否在站房包围盒内
  │     └─ 建立 device_id → station_id 映射
  │
  ├─ 3. 文字-设备关联（_build_text_device_map）
  │     ├─ 通过 object_id 直接匹配
  │     ├─ 通过 object_name 与 element_name 匹配
  │     └─ 建立 text_id → device_id 映射（确保后续同步移动）
  │
  ├─ 4. 备用间隔检测（_detect_spare_intervals）
  │     ├─ 识别 LoadBreakSwitch/Breaker 类型
  │     ├─ 业务类型判断 + 连接数 ≤ 1
  │     └─ 添加"备用"文字标注
  │
  ├─ 5. 设备图标标准化（_normalize_device_icons）
  │     ├─ 按设备类型设置标准尺寸（width/height）
  │     ├─ 以中心不变为原则修正 x/y
  │     ├─ 保留 transform 中的旋转分量
  │     └─ 同步连接线端点和文字位置
  │
  ├─ 6. 拓扑布局重构（_layout_by_topology）★核心★
  │     ├─ 使用 NetworkX 构建设备无向图
  │     ├─ 按站房分组设备
  │     ├─ BFS 分层（母线/变压器为根节点）
  │     ├─ 按层分配坐标（x=深度，y=纵向排列）
  │     ├─ 站房尺寸自适应扩展
  │     └─ 备用设备放站房右侧
  │
  ├─ 7. 网格吸附（_snap_to_grid）
  │     ├─ 动态网格 = max_dev_w + 8px 间距
  │     ├─ 站房外设备对齐到网格
  │     ├─ 同点去重：优先纵向偏移
  │     └─ 同步连接线端点
  │
  ├─ 8. 设备重叠消解（_resolve_device_overlaps）
  │     ├─ 检测站房内/外设备重叠
  │     ├─ 纵向偏移消除重叠
  │     └─ 迭代直到无重叠
  │
  ├─ 9. 连接线规范化（_normalize_connection_styles）
  │     ├─ 统一颜色（主干绿色、联络橙色、跨站紫色）
  │     ├─ 统一线宽（4.0px）
  │     └─ 统一线型
  │
  ├─ 10. 站房边框规范化（_normalize_station_styles）
  │     └─ 统一站房边框样式
  │
  ├─ 11. 连接线正交路由（_route_connections_to_edges）
  │     ├─ 端点贴设备边缘
  │     ├─ L 型正交路径
  │     └─ 避免斜向连线
  │
  ├─ 12. 文字样式规范化（_normalize_text_styles）
  │     ├─ 统一字号（标题 21.3px、关键设备 14px、普通 12px）
  │     ├─ 统一字重（关键设备加粗）
  │     ├─ 统一颜色（#262626）
  │     └─ 位置调整（紧贴设备）
  │
  ├─ 13. 文字碰撞避让（_resolve_text_collisions）
  │     ├─ 检测文字重叠
  │     ├─ 小字号优先避让
  │     └─ 过多重叠时隐藏次要文字
  │
  ├─ 14. viewBox 自适应（_adapt_viewbox）
  │     ├─ 计算所有设备+连接线+文字的边界
  │     ├─ 添加 48px 边距
  │     └─ 更新 SVG viewBox
  │
  └─ 15. 写回 SVG（write_svg）
        ├─ 结构级保真：保留原始 XML 节点结构
        ├─ 属性级更新：仅覆盖修改过的属性
        └─ polygon points 同步更新
```

### 2.2 核心算法详解

#### 2.2.1 拓扑布局重构（_layout_by_topology）

这是美化的核心算法，决定了设备在站房内的排列方式。

**算法步骤：**

```python
def _layout_by_topology(self):
    import networkx as nx
    
    # 1. 构建设备无向图
    G = nx.Graph()
    for elem in self.doc.elements:
        if elem.element_id and elem.layer_name != "Substation":
            G.add_node(elem.element_id, layer=elem.layer_name)
    
    for conn in self.doc.connections:
        if conn.start_device_id and conn.end_device_id:
            G.add_edge(conn.start_device_id, conn.end_device_id)
    
    # 2. 按站房分组
    station_devices = {}
    for dev_id, station_id in self.device_to_station.items():
        station_devices.setdefault(station_id, []).append(dev_id)
    
    # 3. 对每个站房：
    for sid, dev_ids in station_devices.items():
        sub_G = G.subgraph(dev_ids)
        
        # 3a. 选择根节点：母线 > 变压器 > 断路器 > 度数最大
        root = self._pick_root(sub_G)
        
        # 3b. BFS 分层（按电气拓扑深度）
        layers = self._bfs_layers(sub_G, root)
        # layers = {0: [母线], 1: [变压器, 断路器], 2: [隔离开关, 熔断器], ...}
        
        # 3c. 按层分配坐标
        self._assign_coords_by_layers(sid, layers, ...)
```

**坐标分配规则（_assign_coords_by_layers）：**

```
站房内坐标布局：

    ┌─────────────────────────────────┐
    │  layer 0  │  layer 1  │  layer 2  │  ← 从左到右（电源→负载）
    │  (母线)   │  (变压器) │  (断路器) │
    │           │           │           │
    │  ┌─────┐  │  ┌─────┐  │  ┌─────┐  │
    │  │设备1│  │  │设备1│  │  │设备1│  │  ← 从上到下（纵向排列）
    │  └─────┘  │  └─────┘  │  └─────┘  │
    │  ┌─────┐  │  ┌─────┐  │  ┌─────┐  │
    │  │设备2│  │  │设备2│  │  │设备2│  │
    │  └─────┘  │  └─────┘  │  └─────┘  │
    │           │           │           │
    │  备用设备放右侧 →      │           │
    │  ┌─────┐  │           │           │
    │  │备用 │  │           │           │
    │  └─────┘  │           │           │
    └─────────────────────────────────┘

    x 坐标 = station_x + 10 + layer_index * col_width
    y 坐标 = station_y + 10 + row_spacing * (row_index + 1) - device_height/2
```

#### 2.2.2 网格吸附算法（_snap_to_grid）

```
设备网格吸附规则：

1. 网格尺寸 = max_device_width + 8px = 32 + 8 = 40px
2. 站房内设备跳过（由拓扑布局确定）
3. 站房外设备吸附到最近网格点
4. 同点去重策略：
   a. 优先向下偏移一行
   b. 再尝试向上偏移一行
   c. 最后才向右偏移一列

示例（3个设备都吸附到 (320, 560)）：
  设备1 → (320, 560)  [原始位置]
  设备2 → (320, 600)  [向下偏移]
  设备3 → (320, 520)  [向上偏移]
  设备4 → (360, 560)  [向右偏移，因为上下都占用了]
```

#### 2.2.3 连接线正交路由（_route_connections_to_edges）

```
连接线正交路由规则：

1. 端点贴设备边缘：
   - 计算设备中心 → 连接线相邻点的方向
   - 端点移动到设备边缘的对应位置
   
2. L 型正交路径：
   - 如果起点和终点不在同一行/列
   - 添加中间转折点：mid_pt = (end_x, start_y)
   
示例：
  起点(100, 200) → 终点(300, 400)
  L型路由: (100, 200) → (300, 200) → (300, 400)
  
  起点(100, 200) → 终点(100, 400)
  直线: (100, 200) → (100, 400)  (已在同一列)
```

### 2.3 数据模型

```python
# SVG 中间模型
SvgDocument
  ├─ elements: List[SvgElement]     # 所有图元
  ├─ connections: List[SvgConnection] # 所有连接线
  ├─ texts: List[SvgText]            # 所有文字标注
  └─ viewBox: (x, y, width, height)

SvgElement
  ├─ element_id: str                 # 唯一标识 (如 "TMP00000284")
  ├─ element_type: str                # 中文类型名 (如 "断路器")
  ├─ layer_name: str                  # 英文图层名 (如 "Breaker")
  ├─ x, y: float                      # 左上角坐标
  ├─ width, height: float             # 宽高
  ├─ shape_tag: str                   # 形状标签 (use/rect/polygon/path)
  ├─ shape_attrs: dict                # 形状属性 (points/d/...)
  ├─ transform: str                   # transform 字符串
  └─ raw_element: ET.Element          # 原始 XML 节点（结构保真）

SvgConnection
  ├─ connection_id: str
  ├─ start_device_id: str             # 起点设备 ID
  ├─ end_device_id: str               # 终点设备 ID
  ├─ points: List[(x, y)]            # 路径点
  └─ line_type: str                   # 线型 (main_feeder/tie_line/...)

SvgText
  ├─ text_id: str
  ├─ object_id: str                   # 关联设备 ID
  ├─ content: str                     # 文字内容
  ├─ x, y: float                      # 位置
  ├─ font_size: float                 # 字号
  └─ text_role: str                   # 角色 (title/device_name/spare/...)
```

### 2.4 设备标准尺寸表

```python
DEVICE_STANDARD_SIZES = {
    "PowerTransformer": (28.0, 20.0),   # 变压器
    "Breaker": (24.0, 12.0),            # 断路器
    "BusbarSection": (32.0, 6.0),       # 母线
    "LoadBreakSwitch": (20.0, 10.0),    # 负荷开关
    "Disconnector": (20.0, 10.0),       # 隔离开关
    "GroundDisconnector": (20.0, 10.0), # 接地开关
    "Fuse": (16.0, 8.0),                # 熔断器
    "CompositeSwitch": (20.0, 10.0),   # 组合开关
    "CurrentTransformer": (16.0, 12.0),  # 电流互感器
    "PotentialTransformer": (16.0, 12.0),# 电压互感器
    "Junction": (8.0, 8.0),              # 连接点
    "EnergyConsumer": (20.0, 12.0),     # 用电设备
    "RemoteUnit": (16.0, 10.0),         # 远端单元
    "PoleCode": (16.0, 10.0),           # 杆塔
    "Other": (16.0, 10.0),              # 其他
}
```

### 2.5 电压等级配色方案

```python
VOLTAGE_COLORS = {
    "1000": "#FF0000",   # 1000kV - 红色
    "750":   "#FF6A00",  # 750kV - 橙色
    "500":   "#0000FF",  # 500kV - 蓝色
    "330":   "#722ED1",  # 330kV - 紫色
    "220":   "#00A854",  # 220kV - 绿色
    "110":   "#00A854",  # 110kV - 绿色
    "35":    "#1890FF",  # 35kV - 浅蓝色
    "10":    "#262626",  # 10kV - 黑色
}
```

---

## 三、关键设计决策

### 3.1 为什么不读取数据库拓扑信息？

**测试任务明确要求**："不读取数据库拓扑信息，仅依托 SVG 文件自身连接关系"。

这意味着：
- 拓扑关系必须从 SVG 中的连接线（Connection）反推
- 使用 NetworkX 构建无向图，通过图遍历确定设备间的电气连接关系
- 设备类型通过图层名（layer_name）识别
- 站房归属通过空间包围盒判断

### 3.2 为什么使用 BFS 分层？

BFS（广度优先搜索）从根节点（母线/变压器）开始分层，天然符合电气拓扑的"电源→负载"层级关系：
- Layer 0: 母线（电源侧）
- Layer 1: 变压器/断路器
- Layer 2: 隔离开关/熔断器
- Layer 3: 用电设备（负载侧）

这确保了"从左到右、先上后下"的布局原则。

### 3.3 为什么 polygon 元素需要特殊处理？

SVG 中的站房（Substation）使用 `<polygon>` 元素绘制，而非 `<rect>` 或 `<use>`。这带来两个挑战：
1. **尺寸更新**：polygon 的尺寸由 `points` 属性定义，修改 `width`/`height` 不会自动更新显示
2. **Writer 保真**：SVG Writer 为 polygon 保留原始 `points` 属性，不会根据 `width`/`height` 重建

**解决方案**：
- 在 beautifier 中同步更新 `shape_attrs["points"]`
- 在 Writer 中从 `shape_attrs` 读取最新 points

### 3.4 文字-设备关联时机

文字位置依赖于设备位置。如果在设备移动之后才建立关联，文字将无法同步移动。因此：
- `_build_text_device_map` 必须在 `_normalize_device_icons` 之前调用
- 设备移动时通过 `_sync_device_move` 同步更新关联文字的位置

---

## 四、代码架构

### 4.1 模块依赖

```
svg_beautifier.py (主模块)
    ├── data_io/svg_reader.py (SVG 解析)
    │     ├── SvgDocument
    │     ├── SvgElement
    │     ├── SvgConnection
    │     └── SvgText
    │
    ├── data_io/svg_writer.py (SVG 写回)
    │     └── write_svg(doc, path)
    │
    └── 外部依赖
          └── networkx (图构建与遍历)
```

### 4.2 类结构

```python
class SvgBeautifier:
    """SVG 拓扑图形美化器
    
    主流程: beautify() -> parse -> layout -> style -> write
    
    属性:
        doc: SvgDocument           # SVG 文档
        output_path: str           # 输出路径
        device_to_station: dict    # device_id → station_id
        text_device_map: dict      # text_id → device_id
        spare_device_ids: set      # 备用设备 ID 集合
    
    方法（按执行顺序）:
        beautify()                 # 主入口
        _build_station_map()       # 步骤1: 建站房映射
        _build_text_device_map()   # 步骤2: 建文字关联
        _detect_spare_intervals()  # 步骤3: 检测备用间隔
        _normalize_device_icons()  # 步骤4: 标准化设备尺寸
        _layout_by_topology()      # 步骤5: 拓扑布局
        _snap_to_grid()            # 步骤6: 网格吸附
        _resolve_device_overlaps() # 步骤7: 消解重叠
        _normalize_connection_styles() # 步骤8: 连接线样式
        _normalize_station_styles()    # 步骤9: 站房样式
        _route_connections_to_edges()  # 步骤10: 正交路由
        _normalize_text_styles()       # 步骤11: 文字样式
        _resolve_text_collisions()     # 步骤12: 文字避让
        _adapt_viewbox()               # 步骤13: viewBox适配
        _check_beautify_quality()      # 步骤14: 质量自检
```

---

## 五、测试与验证

### 5.1 测试用例

| 文件 | 设备数 | 连接数 | 站房数 | 状态 |
|------|--------|--------|--------|------|
| LINE215.svg | 1432 | 962 | 66 | ✅ 已通过 |
| LINE216.svg | 1606 | 660 | 21 | ✅ 已通过 |

### 5.2 质量自检指标

```
美化质量自检:
  文字总数: N, 可见: M, 隐藏: H (hide_rate%)
  文字重叠: 0 对 (0.0%)  ← 必须为 0
  文字越界: 0 个        ← 必须为 0
  设备越界: 0 个        ← 必须为 0
  连接线端点越界: 0 条   ← 必须为 0
```

### 5.3 输出文件位置

```
输出目录: 数据集更新版20260729/配网 svg/
  ├── LINE215_beautified.svg
  └── LINE216_beautified.svg
```

---

## 六、后续优化方向

### 6.1 近期优化

1. **连接线长度优化**：当前 grid snap 后部分连接线过长（LINE216 中最远连接点 x=19640），可考虑按连接关系重新排列设备
2. **站房内设备间距优化**：当前所有设备使用统一间距，可根据设备类型调整间距
3. **文字标注智能合并**：同类型设备的重复标注可合并显示

### 6.2 中期优化

1. **多视图支持**：支持从不同视图（如变电站全景、线路详情）展示拓扑
2. **交互编辑**：支持用户拖拽调整设备位置后自动重新布局
3. **批量处理**：支持整个目录的 SVG 文件批量美化

### 6.3 长期优化

1. **拓扑验证**：美化后自动校验图模一致性
2. **版本对比**：支持美化前后的差异对比
3. **导出格式**：支持 PNG、PDF 等多种导出格式

---

## 七、参考项目与技术栈

### 7.1 核心技术

| 技术 | 用途 | 版本 |
|------|------|------|
| Python | 主开发语言 | 3.8+ |
| NetworkX | 图构建与 BFS 遍历 | 2.6+ |
| ElementTree (xml.etree) | SVG XML 解析与写回 | 标准库 |

### 7.2 可参考的开源项目

| 项目 | 描述 | 相关技术 |
|------|------|----------|
| [PyVis](https://github.com/visjs/pyvis) | 网络可视化 | 力导向布局 |
| [Graphviz](https://graphviz.org/) | 图可视化工具 | DOT 语言、分层布局 |
| [D3.js](https://d3js.org/) | 数据驱动文档 | SVG 操作、缩放行为 |
| [svgwrite](https://github.com/mozman/svgwrite) | Python SVG 生成 | SVG 元素创建 |
| [cairosvg](https://github.com/Kozea/CairoSVG) | SVG 转 PNG/PDF | SVG 渲染 |

### 7.3 推荐布局算法

| 算法 | 适用场景 | 说明 |
|------|----------|------|
| Layered Layout (Sugiyama) | 层级化拓扑 | 自上而下分层，适合配电网 |
| Force-Directed (Fruchterman-Reingold) | 自由布局 | 力导向，适合网络图 |
| Circular Layout | 环形拓扑 | 设备围绕中心排列 |
| Grid Layout | 均匀分布 | 网格对齐，适合本项目 |

**本项目采用 Layered + Grid 混合布局**：站房内使用 Layered（拓扑分层），站房外使用 Grid（均匀分布）。

---

## 八、总结

### 8.1 已解决的核心问题

1. ✅ 坐标系一致性：禁用坐标缩放，保持原始坐标空间
2. ✅ Transform 正确性：保留旋转分量，scale 由 width/height 控制
3. ✅ 文字-设备同步：提前构建映射，移动时同步更新
4. ✅ 网格分布均匀化：双向偏移策略，避免单行堆积
5. ✅ 站房 polygon 更新：同步更新 points 属性
6. ✅ Writer 保真更新：polygon points 从 shape_attrs 读取

### 8.2 已验证的效果

- LINE215.svg: 1432 设备、962 连接、66 站房 → 美化成功
- LINE216.svg: 1606 设备、660 连接、21 站房 → 美化成功
- 文字重叠率: 0%
- 设备/连接线越界: 0
- viewBox 自适应完成

### 8.3 需要进一步优化

1. 连接线长度：部分连接线过长，需优化设备排列
2. 站房内间距：可按设备类型自适应调整
3. 文字智能合并：减少文字遮挡

---

*文档生成时间: 2025-07-16*
*代码版本: v2.1 (经过 6 项核心修复)*
