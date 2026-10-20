# 颗粒渐变光晕

```yaml
id: grainy-gradient
name: 颗粒渐变光晕
input_modes: [text]
subjects: [atmosphere]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/grainy-gradient/STYLE.md
color_schemes:
  - {id: A, name: 日落到天空, bg: "#F5F2EC", orbs: ["#FF7A45", "#B79CFF", "#6FB7FF"], text: "#141414", default: true}
  - {id: B, name: 森林晨雾, bg: "#F1F3EE", orbs: ["#9ED38B", "#F5D76E", "#7FC8C2"], text: "#141414"}
  - {id: C, name: 夜色, bg: "#121318", orbs: ["#5E6AD2", "#E25C9B", "#F2A65A"], text: "#F2F2EE"}
style_anchors:
  - 当代品牌视觉的柔焦色彩光晕 + 均匀胶片颗粒：温暖、现代、好看
  - 2–4 个高度虚化、彼此融合的色彩光球，光球的数量、位置、明暗关系承载隐喻（如最后一个更亮更扩散）
  - 细腻均匀的胶片颗粒覆盖全画面——让渐变有质感、不廉价
  - 大号中粗现代无衬线标题左上对齐，干净利落
  - 除光球外无任何图形、线条、图标
cover_shape_adaptation:
  - 竖版（3:4）：标题在左上，光球在中下部
  - 横版（2.35:1 / 5:2 / 16:9）：标题在左侧三分之一，光球横向排布在右侧 60%，可从右边缘出血
  - 光球之间的关系要有意义：并列、递进、融合、一个脱离
micro_type:
  - {slot: 右上编号, example: "N°03", rule: 一处极小字}
must_preserve:
  - 光球的柔焦与融合
  - 胶片颗粒的质感
  - 极简：光球 + 文字，没有别的
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 光滑无颗粒的数码渐变（廉价感）
  - 光球边缘清晰、变成实心圆或气泡
  - 加图标、线框、3D 物体、粒子特效
  - 光球压在标题上导致文字可读性下降
```

## 风格意图

当代品牌视觉里的「颗粒渐变」：浅底上几团柔焦色彩光晕，覆一层胶片颗粒，配一行干净的大字。没有具体创意物件，靠色彩与氛围取胜，适合当轻内容的系列底板。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `cyber-industrial-panel`：冷峻单色面板；本风格温暖彩色、只有氛围。
- `hara-emptiness`：同样极简，但那是安静的物；本风格是情绪的色。

## 适用

- 情绪、趋势、轻观点、周记与月度复盘
- 需要「好看、现代、不费脑」的系列化封面

## 避免

- 需要一眼读出具体创意的观点文（本风格没有隐喻物件）
- 严肃、硬核、教程类内容
