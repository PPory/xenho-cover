# 药剂师标签

```yaml
id: apothecary-label
name: 药剂师标签
input_modes: [text]
subjects: [typography, object]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/apothecary-label/STYLE.md
color_schemes:
  - {id: A, name: 琥珀玻璃, vessel: "#7A3E12", label: "#F3EEE3", text: "#1B1B1B", default: true}
color_lock: 只用这一套配色（即 example-image 里样图的配色），不换色；新配色要先出图给用户确认再加
style_anchors:
  - 高端香氛与护肤品牌的包装标签语言：一张纸标签贴在玻璃瓶身上，瓶身局部特写满幅（看不到瓶口瓶底）
  - 标签内全部居中对称：顶部等宽小字 → 细衬线宋体主标题 → 细横线 → 副标题 → 两行配方式等宽小字 → 底部大号细体编号
  - 一张手工加贴的批次小贴纸略微倾斜，压在标签上沿
  - 真实摄影质感：玻璃的柔和反光与深浅、纸张纹理、浅景深、柔和侧光
  - 克制、仪式感、「配方」的隐喻：把一个方法写成一剂配方
cover_shape_adaptation:
  - 竖版（3:4）：标签竖长，占画面宽度 60–65%，居中
  - 横版（2.35:1 / 5:2 / 16:9）：改拍两三只并排的瓶子，中间那只的标签正对镜头承载全部文字，两侧瓶子虚化、标签只露空白边——或改为一只横卧的瓶子，标签横向展开；标签内仍居中对称
  - 主标题 2–3 行，字号中等，行距宽松
micro_type:
  - {slot: 标签顶部, example: "FORMULA FOR FREELANCERS", rule: 一行极小等宽西文}
  - {slot: 配方行, example: "REPEAT ×3 — THEN DELEGATE / BLENDED IN 2026", rule: 两行打字机等宽西文}
  - {slot: 底部编号, example: "N°03", rule: 大号细衬线}
  - {slot: 批次贴纸, example: "BATCH 10.20", rule: 一行等宽西文}
must_preserve:
  - 真实玻璃与纸张的材质和光
  - 标签内的居中对称与层级
  - 克制的色彩（瓶色 + 纸色 + 一个文字色）
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 出现真实香氛或护肤品牌名、logo
  - 瓶子全身入镜变成产品广告图、背景加花瓣水珠等电商道具
  - 中文用打字机字体（中文一律细衬线宋体）
  - 标签文字超出微排版槽位、写成成分表长段
```

## 风格意图

Le Labo / Aesop 式的包装排版：一只琥珀色玻璃瓶的局部，一张手工感纸标签，打字机字与细衬线宋体，居中对称。把一个观点或方法包装成一剂「配方」——克制、有品味、有仪式感。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `cloth-book-jacket`：著作感；本风格是配方感、生活方式品味。
- `archive-index-card`：档案与秩序；本风格是仪式与质感。
- `concept-still-life`：一个超现实物件讲观点；本风格的物件只是标签的载体。

## 适用

- 方法论、「配方」式干货、习惯与仪式、个人工作流
- 需要「有品味、高级」气质的小红书与公众号封面

## 避免

- 强冲击、宣言式观点
- 硬核技术、数据类内容
