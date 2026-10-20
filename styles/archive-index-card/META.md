# 档案索引卡

```yaml
id: archive-index-card
name: 档案索引卡
input_modes: [text]
subjects: [typography, object]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/archive-index-card/STYLE.md
color_schemes:
  - {id: A, name: 暖灰卡纸, bg: "#CFCBC2", card: "#F6F1E4", rule_red: "#C8372D", rule_blue: "#9DB4CF", text: "#1E1E1E", default: true}
  - {id: B, name: 牛皮纸, bg: "#B9976B", card: "#F6F1E4", rule_red: "#C8372D", rule_blue: "#9DB4CF", text: "#1E1E1E"}
  - {id: C, name: 墨绿呢, bg: "#2F4A3E", card: "#F6F1E4", rule_red: "#C8372D", rule_blue: "#9DB4CF", text: "#1E1E1E"}
style_anchors:
  - 图书馆卡片目录 / 设计档案登记卡：一张米白索引卡正面平视放在纯色卡纸底上，对称、克制
  - 卡片是真实的表格排版：顶部红色细横线 + 浅蓝细横格线，底部中央一个打孔圆洞
  - 主标题用粗壮中文黑体印在卡片上部大格里
  - 下部是打字机等宽字段行（字段名 ...... 内容），字段名与内容用细点线连接
  - 一枚略倾斜的圆形红色橡皮印章盖在卡片一角，油墨不均、边缘缺损——印章文字就是本次的结论
cover_shape_adaptation:
  - 竖版（3:4）：卡片横放居中偏上，占画面宽度 80%；卡外底部一行极小等宽字
  - 横版（2.35:1 / 5:2 / 16:9）：卡片横放居中，高度占画面 75%，两侧留出纯色底；可在卡片左侧露出第二张卡片的边缘（只露边，无字）暗示一整盒档案
micro_type:
  - {slot: 字段行, example: "SUBJECT ........ AUTOMATION / FILED ........ 2026.10 / REF. ........ NO.03", rule: 2–3 行打字机等宽西文}
  - {slot: 印章, example: "AUTO", rule: 一个短词，西文大写}
  - {slot: 卡外底部, example: "XENHO ARCHIVE", rule: 一行极小等宽字}
must_preserve:
  - 真实卡片的纸张厚度、打孔、红蓝格线
  - 字段行的打字机等宽质感与点线
  - 橡皮印章的油墨不均
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 中文用打字机字体（中文一律标准黑体，打字机字体只给西文与数字）
  - 卡片透视倾斜、堆满桌面的道具
  - 字段行写成中文长句或解释性句子
  - 印章写中文或长句
```

## 风格意图

图书馆卡片目录与设计档案的视觉语言：一张被郑重登记的索引卡，红蓝格线、打字机字段、一枚红色印章。把一个观点「归档」——它被整理过、被确认过。Wes Anderson 式的对称秩序。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `thermal-receipt`：同为纸质单据，但小票是「算账」的幽默；索引卡是「归档」的郑重。
- `apothecary-label`：标签是配方与仪式感；索引卡是档案与秩序感。

## 适用

- 读书笔记、知识管理、整理归档、复盘、定义一个概念
- 需要「被认真整理过」的气质

## 避免

- 情绪浓烈、需要画面冲击的内容
