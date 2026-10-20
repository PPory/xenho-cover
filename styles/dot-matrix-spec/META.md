# 点阵规格书

```yaml
id: dot-matrix-spec
name: 点阵规格书
input_modes: [text]
subjects: [typography, diagram]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/dot-matrix-spec/STYLE.md
color_schemes:
  - {id: A, name: 冷白橙红, bg: "#F2F2F0", dot: "#111111", accent: "#FF4F1F", default: true}
  - {id: B, name: 炭黑橙, bg: "#161616", dot: "#F2F2F0", accent: "#FF6A1F"}
  - {id: C, name: 铝灰黄, bg: "#D9D9D6", dot: "#111111", accent: "#F5C400"}
style_anchors:
  - Teenage Engineering 说明书 + Nothing 点阵字体：冷白底、黑色圆点像素字、一点橙红、工业规格书式的精确排版
  - 一个巨大的点阵符号（数字、乘号、箭头、短词）由圆形实心点构成，是画面主角；其中一部分点用强调色
  - 极细浅灰点阵网格铺满全画面，像工程笔记纸
  - 说明书式标注：细黑引线从点阵字引出，末端一行等宽小字（FIG.01 —— ……）
  - 主标题中等字重现代黑体，克制，字号约为点阵字高度的四分之一；下方细横线 + 三栏规格表
  - 四角十字裁切标记
cover_shape_adaptation:
  - 竖版（3:4）：点阵符号占上半部，主标题与规格表在下半部，左对齐
  - 横版（2.35:1 / 5:2 / 16:9）：点阵符号在右侧 55%，主标题与规格表在左侧，规格表可改为两栏
  - 点阵符号选择：题目有数字用数字（可加 ×、+、%）；没有就用一个箭头、一个西文短词（≤4 字母）或一个几何符号
micro_type:
  - {slot: 图注, example: "FIG.01 — REPEAT, THEN DELEGATE", rule: 一行等宽西文，带引线}
  - {slot: 规格表, example: "MODEL / XN-03 · MODE / AUTO · YEAR / 2026", rule: 2–3 栏，每栏小号字段名 + 值}
  - {slot: 裁切标记, example: 四角十字, rule: 无文字}
must_preserve:
  - 圆点像素字的工业感与精确
  - 冷白 + 黑 + 一个强调色
  - 说明书式标注与规格表
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 中文用点阵 / 像素字体（点阵只给西文、数字、符号；中文一律标准黑体）
  - 发光 LED 效果、霓虹、渐变、3D
  - 规格表写成中文长句
  - Nothing / Teenage Engineering 的 logo 与产品
```

## 风格意图

Teenage Engineering 产品说明书与 Nothing 点阵字体语言的结合：冷白纸、黑色圆点像素字、一点橙红、工业规格书的标注与表格。像一份设计精良的硬件说明书第一页。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `cyber-industrial-panel`：黑色装甲面板、未来感；本风格是白色纸质说明书、理性克制。
- `blueprint-drawing`：完整工程制图；本风格是点阵字 + 规格表，更图形化。
- `giant-numeral`：巨型无衬线数字作结构；本风格的数字是点阵、有标注，更「产品」。

## 适用

- AI 工具、效率、数码、工作流、产品评测
- 标题带数字或能提炼出一个符号的内容

## 避免

- 温暖叙事、东方气质、情绪类内容
