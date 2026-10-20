# Riso 双色印刷

```yaml
id: riso-two-ink
name: Riso 双色印刷
input_modes: [text]
subjects: [illustration, hands, object]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/riso-two-ink/STYLE.md
color_schemes:
  - {id: A, name: 荧光粉 + 中蓝, paper: "#F3EEE2", ink1: "#FF48B0", ink2: "#0078BF", overprint: 深紫, default: true}
  - {id: B, name: 黄 + 蓝, paper: "#F3EEE2", ink1: "#FFE800", ink2: "#0078BF", overprint: 深绿}
  - {id: C, name: 橙 + 绿, paper: "#F3EEE2", ink1: "#FF6C2F", ink2: "#00A95C", overprint: 深褐}
style_anchors:
  - 独立出版 zine 的孔版印刷（Risograph）：只用两色油墨，叠印处自然混出第三色
  - Riso 特有的颗粒、油墨不均和 1–2mm 套色错位——手作的温度
  - 粗线条、扁平、略带稚拙的手绘插画：一个动作（一只手在做什么）讲清隐喻
  - 一大块网点圆形 / 色块压在插画后面
  - 超粗中文黑体主标题，用其中一色油墨印刷，带油墨不均
cover_shape_adaptation:
  - 竖版（3:4）：主标题在上部两行，插画占中下部，副标题在底部
  - 横版（2.35:1 / 5:2 / 16:9）：主标题在左侧，插画在右侧 55%，网点色块跨越中线连接两边
  - 插画动作要能讲清本次的「转折」：比如重复三次后第四笔变成别的东西
micro_type:
  - {slot: 角落小字, example: "ZINE NO.03", rule: 可选，一处小字，用另一色油墨}
must_preserve:
  - 只有两色油墨 + 叠印第三色
  - 颗粒、套色错位、油墨不均的印刷物理感
  - 手绘的稚拙与温度
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 数码平滑插画、矢量扁平插画感（就失去 riso 了）
  - 超过两色油墨、渐变、阴影
  - 套色错位过大导致汉字重影难读（标题错位 ≤ 1mm）
  - 写实人物脸部
```

## 风格意图

独立出版 zine 的孔版印刷：两色油墨、颗粒、套色错位，稚拙的手绘插画，用一个动作讲一个观点。人味最重、最轻松的一类。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。

## 与库内其他风格的分工

- `swiss-punk-layers`：同为双色印刷，但那是网屏与排版实验；本风格是手绘插画。
- `retro-halftone-pop`：CMYK 粗网点 + 动画线稿 + 高饱和撞色；本风格是两色孔版、更安静更手作。
- `notion-doodle`：黑白手绘信息图；本风格是彩色印刷插画。

## 适用

- 创作者日常、个人表达、轻松观点、习惯与方法
- 需要「有人味、不 AI 感」的封面

## 避免

- 严肃权威、硬核技术、数据类内容
