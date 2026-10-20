# 艺术馆展览海报

```yaml
id: exhibition-poster
name: 艺术馆展览海报
input_modes: [text]
subjects: [typography]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/exhibition-poster/STYLE.md
color_schemes:
  - {id: A, name: 冷灰荧光橙, bg: "#E6E6E3", text: "#121212", sticker: "#FF5A36", default: true}
  - {id: B, name: 白底荧光绿, bg: "#F4F4F1", text: "#121212", sticker: "#C6F432"}
  - {id: C, name: 黑底荧光粉, bg: "#121212", text: "#F2F2EE", sticker: "#FF4FA3"}
style_anchors:
  - 欧洲当代美术馆的展览识别：超粗紧凑的中文黑体主标题撑满上半部，左右边距统一窄
  - 下半部一条细黑线 + 严格等宽三栏信息排版，左对齐、顶部对齐
  - 一个荧光油墨质感的实心贴纸圆打破秩序，圆内两行粗体西文
  - 最底部一行宽字距小字横贯全宽，两端对齐
  - 字号靠「撑满」而不是「拉伸」：字形保持标准比例
cover_shape_adaptation:
  - 竖版（3:4）：主标题 3 行撑满上 70%；三栏信息在下 25%；贴纸圆放在标题右侧边缘的空白处
  - 横版（2.35:1 / 5:2 / 16:9）：主标题 1–2 行撑满上 65% 的宽度；三栏信息在下部横向展开（可扩成四栏）；贴纸圆放在右上角空白处
  - 贴纸圆的位置由标题的空白决定：放在行尾留出的空白里，不压任何汉字
micro_type:
  - {slot: 贴纸圆内, example: "NOW / AUTOMATED", rule: 两行粗体西文}
  - {slot: 第一栏, example: 副标题中文拆两行, rule: 中文副标题放这里}
  - {slot: 第二栏, example: "XENHO / NOTES NO.03", rule: 两行}
  - {slot: 第三栏, example: "2026.10.20 — / ONGOING", rule: 两行}
  - {slot: 底部全宽行, example: "REPEAT — REPEAT — REPEAT — DELEGATE", rule: 宽字距小字，两端对齐}
must_preserve:
  - 主标题的尺度与紧凑（撑满画面宽度）
  - 三栏信息的严格对齐
  - 荧光贴纸圆的唯一性与印刷荧光质感
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 贴纸圆压在任何汉字上（实测会把字压坏）
  - 把字横向拉伸或纵向压扁来撑满（只能靠字号）
  - 加插画、照片、图标、渐变
  - 第二个荧光色或第二个图形
  - 编造真实美术馆名、真实展期地址
```

## 风格意图

Kunsthalle 与当代美术馆的展览海报语言：巨大的紧凑黑体标题撑满上半部，下半部是严谨的多栏信息，一个荧光贴纸圆打破秩序。冷静、当代、有文化机构的权威感，在信息流里音量很大。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `giant-numeral`：巨物是一个单字形；本风格的巨物就是中文标题本身。
- `polish-grain-collage`：颗粒、散落、先锋拼贴；本风格是干净、对齐、机构感。

## 适用

- 宣言、强观点、隆重发布、年度复盘
- 标题 6–12 字、能拆成 2–3 个有力短行的内容
- 自有产品发布（产品名做巨字）

## 避免

- 标题很长、无法拆成短行的内容
- 安静内省、温暖叙事类内容
