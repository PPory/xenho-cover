# 瑞士朋克层叠

```yaml
id: swiss-punk-layers
name: 瑞士朋克层叠
input_modes: [text]
subjects: [typography, texture]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/swiss-punk-layers/STYLE.md
color_schemes:
  - {id: A, name: 青黑, paper: "#EFEBE1", ink1: "#00A3D9", ink2: "#111111", default: true}
color_lock: 只用这一套配色（即 example-image 里样图的配色），不换色；新配色要先出图给用户确认再加
style_anchors:
  - Wolfgang Weingart 打破瑞士规范的方式：把网点、莫尔纹、叠印网屏当作图形本身，层层叠压出纵深
  - 只用两色油墨（一个彩色 + 黑），叠印处自然变深
  - 几块粗网点矩形阶梯式错位叠放，叠压处出现莫尔纹；一块不同角度的网屏斜压上去打破秩序
  - 粗细不一的黑色水平铅条线与小黑方块贯穿画面
  - 主标题粗体黑字阶梯式分段错位排列，与网屏阶梯呼应
cover_shape_adaptation:
  - 竖版（3:4）：网屏阶梯从左上到右下贯穿画面中部，主标题分 3 段沿阶梯错位，副标题与微排版在左下
  - 横版（2.35:1 / 5:2 / 16:9）：网屏阶梯从左到右横向展开，主标题分 2 段错位排在左半；斜压网屏在右侧
  - 中文标题只与留白和极淡的网点区重叠——笔画下方不能是密集网点或莫尔纹
micro_type:
  - {slot: 右上竖排, example: "TYPOGRAPHIC NOTES 03", rule: 一行极小黑字竖排}
  - {slot: 左下角, example: "XENHO / 2026", rule: 两行小字}
must_preserve:
  - 网点与莫尔纹的真实印刷感
  - 层叠带来的纵深与张力
  - 两色油墨的限制
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 汉字压在密集网点或莫尔纹上（样图里「遍」字因此发糊）——网屏可以叠西文和留白，中文笔画下方保持干净
  - 超过两色油墨
  - 数码感渐变、发光、故障风 glitch
  - 插画、照片主体
```

## 风格意图

Wolfgang Weingart 的「瑞士朋克」：从瑞士国际主义内部打破它——网点、莫尔纹、叠印网屏不再被隐藏，而是成为画面本身。理性的底子，实验的表情。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `swiss-concert-poster`：瑞士规范本身，干净几何；本风格是打破规范的层叠实验。
- `riso-two-ink`：同为双色印刷，但那是手绘插画 + 孔版颗粒的温度；本风格是网屏与排版的实验。
- `polish-grain-collage`：颗粒拼贴、字符散落；本风格保留网格逻辑。

## 适用

- 创作、设计、实验性观点、打破常规类话题
- 需要「理性 + 张力」的封面

## 避免

- 安静、温暖、生活方式类内容
- 标题很长的内容（阶梯错位会把长标题拆散）
