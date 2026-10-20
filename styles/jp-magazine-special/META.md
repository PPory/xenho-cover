# 日本杂志特集

```yaml
id: jp-magazine-special
name: 日本杂志特集
input_modes: [text]
subjects: [object, typography]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/jp-magazine-special/STYLE.md
color_schemes:
  - {id: A, name: 番茄红, bg: "#E8442E", text: "#FFFFFF", default: true}
color_lock: 只用这一套配色（即 example-image 里样图的配色），不换色；新配色要先出图给用户确认再加
style_anchors:
  - 日本生活方式杂志（BRUTUS / POPEYE 一路）的特集封面：明亮纯色底 + 自造粗衬线西文刊名 + 大胆的特集标题 + 一张干净的去底物件照片
  - 对每个微小排版细节的执着：竖排横排混用、字号层级极丰富、细线引出的物件注释标签——热闹但有秩序
  - 物件照片是真实摄影、去底、柔和投影落在纯色底上；物件是本次隐喻的载体
  - 特集标题里的一个关键词放进圆角矩形反白框里强调
  - 底部期号年份 + 只有线条的条形码
cover_shape_adaptation:
  - 竖版（3:4）：刊名顶部撑满宽度，特集标题在刊名下，物件照片在中下部，左侧竖排副标题
  - 横版（2.35:1 / 5:2 / 16:9）：刊名放左上（宽度约画面 45%），特集标题在其下方左对齐，物件照片在右侧 50%，注释标签围绕物件
  - 物件只有一个（或一组同类物），去底干净
micro_type:
  - {slot: 刊名, example: "NOTES", rule: 自造的粗衬线西文刊名，不得是真实杂志名}
  - {slot: 期号, example: "NO.03", rule: 刊名右下角极小字}
  - {slot: 注释标签, example: "TO-DO ×3 / AUTO", rule: 1–2 处，细线指向物件}
  - {slot: 底部, example: "SPECIAL ISSUE / 2026", rule: 一行小字 + 线条条形码}
must_preserve:
  - 纯色底的明亮饱和
  - 字号层级的丰富与秩序
  - 去底物件照片的真实质感
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 文字加白色光晕、外发光、描边阴影（样图翻过车，显廉价）——所有字都是干净平涂
  - 使用 BRUTUS、POPEYE、Casa 等真实刊名或近似字形
  - 物件超过一组、画面变成商品陈列
  - 物件用插画或 3D 渲染代替摄影
```

## 风格意图

日本生活方式杂志的特集封面：一面明亮纯色，一个自造刊名，一句大胆的特集标题，一张干净的去底物件照，周围是层级极丰富、对齐极讲究的小字与注释。热闹但有秩序，精致又亲和。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `concept-still-life`：一个超现实物件 + 大标题，杂志内页的单张大片；本风格是完整的杂志封面系统（刊名、特集、注释、条码）。
- `retro-halftone-pop`：漫画半调与情绪；本风格是摄影与编辑排版。

## 适用

- 生活方式、好物、工具推荐、习惯养成、轻松但精致的干货
- 小红书封面（信息流里抢眼、亲和）

## 避免

- 严肃深度长文、东方安静气质
- 找不到一个可以拍的物件的抽象题目
