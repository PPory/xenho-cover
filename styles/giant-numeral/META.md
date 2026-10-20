# 巨型数字

```yaml
id: giant-numeral
name: 巨型数字
input_modes: [text]
subjects: [typography]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/giant-numeral/STYLE.md
color_schemes:
  - {id: A, name: 白黑信号红, bg: "#FFFFFF", glyph: "#111111", accent: "#E10600", default: true}
  - {id: B, name: 黑白克莱因蓝, bg: "#111111", glyph: "#F2F2F0", accent: "#1F3FD6"}
  - {id: C, name: 米黄黑橙, bg: "#F1ECDF", glyph: "#111111", accent: "#FF5A1F"}
style_anchors:
  - Experimental Jetset「把语言变成物件」：一个巨大的无衬线字形（数字优先）高过画面、从一侧和底部出血裁切，是整个版面的建筑结构
  - 黑白 + 一个强调色；强调色只出现在一条横贯全宽的粗色条上
  - Helvetica 般的中性无衬线；极端字号对比——巨字 vs 中号标题 vs 极小信息栏
  - 主标题落在巨字留出的白色空间里，左对齐，紧凑行距
  - 左下角一组像展览海报底栏的极小三行字
cover_shape_adaptation:
  - 竖版（3:4）：巨字从右侧和底部出血，露出约四分之三；色条横贯画面上部三分之一；标题在色条下方、巨字左侧
  - 横版（2.35:1 / 5:2 / 16:9）：巨字高度撑满画面高度并从右侧出血，占画面宽度 40–50%；色条横贯全宽位于上部；标题在左半区，三行以内
  - 巨字选择：标题含数字时用该数字；不含时用标题里一个关键西文字母或符号（如 A、?、→），并在提示词里写明这个字形
micro_type:
  - {slot: 色条内文字, example: "A FREELANCER'S AUTOMATION LIST", rule: 一行白色（或反色）粗体小字，左对齐}
  - {slot: 左下角三行, example: "XENHO / NOTES NO.03 / 2026", rule: 极小无衬线，左对齐}
must_preserve:
  - 巨字的尺度与出血裁切——它必须大到像建筑
  - 三色以内的极简色彩
  - 严格的左对齐与网格感
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 巨字完整出现在画面内（失去尺度感）或被缩小到与标题同级
  - 巨字用汉字（大幅裁切后汉字不可辨且易错）
  - 加插画、照片、纹理、渐变
  - 强调色出现超过一处
  - 标题压在巨字上导致笔画难辨（标题必须在白色空间里）
```

## 风格意图

荷兰晚期现代主义（Experimental Jetset）的展览海报语言：一个巨大的中性无衬线字形撑起整张版面，一条信号色横条打破秩序，标题和信息栏以极端字号对比排在留白里。语言即物件，冷静而有力。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `bw-type-specimen`：巨型**衬线**汉字的正负空间与反色；本风格是巨型**无衬线数字 / 字母**作结构，标题是独立的中号字。
- `exhibition-poster`：中文标题本身被放到极大；本风格的巨物是一个单字形，标题保持中号。

## 适用

- 标题带数字的内容：清单、N 个方法、第 N 期、年份复盘、数据观点
- 宣言、强观点、需要冷静权威感的内容

## 避免

- 抒情、温暖、生活方式类内容
- 标题里既没有数字也找不到一个可代表的西文字形的题目
