# 蓝图技术图纸

```yaml
id: blueprint-drawing
name: 蓝图技术图纸
input_modes: [text]
subjects: [system, diagram]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/blueprint-drawing/STYLE.md
color_schemes:
  - {id: A, name: 普鲁士蓝晒图, bg: "#123C7A", line: "#F2F4F8", default: true}
  - {id: B, name: 赭红晒图, bg: "#7A2E1E", line: "#F6EFE6"}
  - {id: C, name: 白底蓝线, bg: "#F4F1EA", line: "#1F4FA3"}
style_anchors:
  - 建筑与工业设计的晒图蓝图（cyanotype）：深普鲁士蓝底、白色细线工程制图、晒图纸的斑驳与纸纹
  - 全画面极淡坐标网格线；四角白色图框角线
  - 主图是一张把本次「系统 / 流程 / 结构」画成工程图的线稿：模块、连接件、带箭头的尺寸标注、圆心十字、虚线中心线
  - 右下角标准图签栏（title block）：细线表格，格内极小等宽字——天然的微排版位置
  - 主标题白色细体无衬线（工程字气质）
cover_shape_adaptation:
  - 竖版（3:4）：工程图在上半部，主标题在中下部左对齐，图签栏在右下角
  - 横版（2.35:1 / 5:2 / 16:9）：工程图在右侧 60%，主标题在左侧中部，图签栏在右下角
  - 工程图的主体要表达本次内容的结构（输入→处理→输出、循环、层级、分支），不画具体机械产品
micro_type:
  - {slot: 尺寸标注, example: "×1 / ×2 / ×3", rule: 2–4 处极小西文或数字}
  - {slot: 节点标注, example: "AUTO", rule: 一处短词，带引线}
  - {slot: 图签栏, example: "PROJECT: AUTOMATION / DWG NO. 03 / DRAWN: XENHO / DATE: 2026.10", rule: 四格等宽小字}
must_preserve:
  - 晒图纸的材质感与单色线稿
  - 工程制图的规范语汇（尺寸线、中心线、圆心十字、图框、图签栏）
  - 线宽统一、精确
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 画成科幻 HUD、发光全息、赛博界面
  - 加彩色、渐变、3D 透视渲染
  - 工程图里写中文小字（标注一律西文或数字）
  - 画具体的机器人、芯片、电脑
```

## 风格意图

建筑与工业设计的蓝图：深蓝晒图纸上的白色工程线稿，把一个系统、一套流程、一个方法画成可施工的图纸。理性、精确、有手工晒图的温度。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `cyber-industrial-panel`：黑色装甲面板 + 科幻工业感；本风格是纸上的工程图，复古理性。
- `dot-matrix-spec`：产品规格书的点阵与标注；本风格是完整的工程制图。
- `notion-doodle`：手绘信息图、亲和；本风格精确、专业。

## 适用

- 系统搭建、架构、工作流、流程设计、方法论拆解
- 「我是怎么搭了一个 X」类内容

## 避免

- 情绪叙事、生活方式
- 没有结构可画的题目
