# 瑞士音乐会海报

```yaml
id: swiss-concert-poster
name: 瑞士音乐会海报
input_modes: [text]
subjects: [concept, rhythm]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/swiss-concert-poster/STYLE.md
color_schemes:
  - {id: A, name: 黑白信号红, bg: "#111111", form: "#F2F2F0", accent: "#E4002B", default: true}
  - {id: B, name: 白黑, bg: "#F2F2F0", form: "#111111", accent: "#E4002B"}
  - {id: C, name: 深蓝白黄, bg: "#14213D", form: "#F2F2F0", accent: "#FCA311"}
style_anchors:
  - Josef Müller-Brockmann 音乐会海报：用纯几何图形的数学节律表达内容——弧、圆、条、方块按严格比例重复、递增、旋转
  - 节律是主角：一组几何单元重复若干次后，在某一处发生变化（换成强调色、换方向、继续扩展），这个变化就是隐喻
  - 线宽统一、边缘锐利、平面印刷感，无纹理无阴影
  - 隐形 12 栏网格；所有元素对齐网格
  - 主标题粗体无衬线中文，严格左对齐网格，分 2–3 行
cover_shape_adaptation:
  - 竖版（3:4）：几何节律占上半部 55–60%，主标题在左下，副标题对齐同一左边线
  - 横版（2.35:1 / 5:2 / 16:9）：几何节律横向展开占右侧 60%，主标题在左侧三分之一，底部对齐网格
  - 几何单元的选择要贴内容：重复→同一单元并排；扩散→同心递增；转折→旋转角度递增；累积→条带逐级加长
micro_type:
  - {slot: 底部小字, example: "XENHO · 2026", rule: 可选，一行极小字，对齐标题左边线}
must_preserve:
  - 数学般精确的节律与比例
  - 三色以内、平涂、锐利
  - 网格对齐的左对齐排版
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 并排的同心弧组读成 Wi-Fi / 信号 / 声波图标（样图翻过车）——弧组之间要有旋转角度变化或改用圆、条、方块
  - 有机形、手绘、插画、照片
  - 渐变、阴影、纹理、3D
  - 几何单元摆放随意、不成比例
```

## 风格意图

Müller-Brockmann 式瑞士国际主义：客观、数学、节律。不画任何具象物，用几何单元的重复与变化表达内容——像一段被看见的音乐。理性、秩序、冲击力强。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `swiss-grid-scrawl`：瑞士网格印刷品 + 满纸手迹的「秩序 vs 失控」；本风格是纯粹的秩序。
- `swiss-punk-layers`：网屏叠印、打破瑞士规范；本风格是规范本身。
- `tanaka-geometry`：几何拼出具象形象；本风格只有抽象节律。

## 适用

- 系统、方法、结构化思考、流程与节奏类内容
- 需要「理性、秩序、冲击力」的封面

## 避免

- 温暖叙事、情绪浓的个人故事
- 需要具象形象才能讲清的题目
