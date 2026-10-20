# 软陶 3D

```yaml
id: soft-clay-3d
name: 软陶 3D
input_modes: [text]
subjects: [object, scene]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/soft-clay-3d/STYLE.md
color_schemes:
  - {id: A, name: 蜜桃糖果, bg: "#F6D5C1", palette: ["#FFF6EC", "#A9C8F0", "#9ED9C4", "#F5D27A"], text: "#3B2A22", default: true}
color_lock: 只用这一套配色（即 example-image 里样图的配色），不换色；新配色要先出图给用户确认再加
style_anchors:
  - Google Material 3 Expressive / Airbnb 式亲和三维：圆润、柔软、哑光，像可以捏的软陶玩具
  - 一个由 2–3 个软陶物件组成的小场景讲隐喻：一个装置、一个开口、一叠卡片、一个按钮
  - 糖果色板：一个底色 + 四个点缀色，全部低饱和柔和
  - 哑光黏土材质、柔和全局光照、浅景深、柔和接触阴影
  - 圆润粗体中文（圆体质感）主标题
cover_shape_adaptation:
  - 竖版（3:4）：主标题在上部居中两行，软陶场景在中下部
  - 横版（2.35:1 / 5:2 / 16:9）：主标题在左侧，场景在右侧 55%；小几何软陶点缀物散在两侧
  - 动作用物件之间的关系表达（卡片滑进开口、球滚下坡道），避免画手
micro_type:
  - {slot: 角落小字, example: "NO.03", rule: 可选，一处小号圆体}
must_preserve:
  - 哑光黏土材质与柔和光
  - 糖果色板的柔和统一
  - 圆润造型——不出现尖角
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 画手、人物（3D 手部比例与手指是翻车高发区）——用物件互动表达动作
  - 亮面塑料、金属、玻璃反光
  - 高饱和撞色、霓虹
  - 场景元素超过 5 个、变成玩具陈列
```

## 风格意图

亲和型品牌的 3D 视觉：软陶般圆润哑光的小物件组成一个小装置，糖果色，柔光。让复杂的事看起来轻松好玩、门槛很低。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `notion-doodle`：同为亲和易读，但那是手绘线稿信息图；本风格是 3D 软陶小场景。
- `concept-still-life`：真实摄影 + 硬光；本风格是柔和渲染的软陶。

## 适用

- 教程、入门、工具推荐、新手向内容
- 需要「亲和、好上手、不吓人」的封面

## 避免

- 严肃深度、宣言、批判类内容
