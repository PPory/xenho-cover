# 字格填字系统

```yaml
id: tile-crossword
name: 字格填字系统
input_modes: [text]
subjects: [typography]
outputs: [cover, poster]
default_ratio: "3:4"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 核心表达, 补充背景, 情绪倾向, 不想出现的元素]
source: styles/tile-crossword/STYLE.md
color_schemes:
  - {id: A, name: 薰衣草靛, paper: "#E9E6F7", line: "#5A4FCF", fill: "#1B1464", vignette: "#8C84E8", default: true}
  - {id: B, name: 薄荷墨绿, paper: "#E4F1EA", line: "#2F8F68", fill: "#0F3D2E", vignette: "#7CC4A4"}
  - {id: C, name: 杏橙赭, paper: "#F6ECDF", line: "#D2692A", fill: "#5A2410", vignette: "#F0A774"}
  - {id: D, name: 冷灰黑, paper: "#ECECEA", line: "#555555", fill: "#141414", vignette: "#A8A8A4"}
style_anchors:
  - 「Design Through System & Play」：严格的同尺寸方格网，像填字游戏一样横竖拼成一块不规则形状——系统 + 玩心
  - 主标题每个字（每个西文字母）单独占一格，被深色实心填满、字为白色粗体无衬线；标题沿格子横向、纵向转折排布
  - 方格有破格：4–5 格被轻微旋转 5°–15° 像碰歪的瓷砖，若干格空着，2–3 格浅色半透明填充
  - 单一色系：浅色细纹纸底 + 同色系细线描边 + 同色系深色填充 + 四周柔和暗角渐晕
  - 四角与边缘是一套微排版系统：大号细体 + 粗体的叠排名称、期号、竖排小字、条形码——小字是质感，不是说明
cover_shape_adaptation:
  - 竖版（3:4）：方格群居中偏上，占画面 60–70%；四角布置微排版
  - 横版（2.35:1 / 5:2 / 16:9）：方格群横向展开，标题优先横向一排排进格子，纵向转折至多一次；方格群占画面宽度 65–75% 居中偏右，左侧边缘放竖排小字，四角微排版保留
  - 副标题放进一行连续的空方格里（小号、同色系深色），或贴在方格群下边缘
  - 标题字数多于 12 时，只取 A 层短标题进格子，B 层作副标题
micro_type:
  - {slot: 左上角名称, example: "XENHO / NOTES", rule: 两行，上行大号细体、下行粗体，允许被画面边缘轻微裁切}
  - {slot: 右上角栏目, example: "AUTOMATION / SELECTED NOTES", rule: 两行右对齐小字}
  - {slot: 左侧竖排, example: "DESIGN THROUGH SYSTEM & PLAY", rule: 一行极小字}
  - {slot: 左下角档案, example: "A FREELANCER'S CHECKLIST / ARCHIVE NO.03", rule: 两行小字 + 一条只有线条的条形码}
  - {slot: 右下角期号, example: "VOL.03", rule: 大号细体，允许被画面右下边缘轻微裁切}
  - {slot: 某个空格内, example: "2026", rule: 至多一处}
must_preserve:
  - 一字一格——这是汉字准确率最高的排法，也是本风格的身份证
  - 单一色系的纯度与暗角渐晕
  - 网格秩序 + 少量破格的张力（破格 ≤ 5 格）
  - 主标题完整、汉字正确、清晰可读
avoid_when_applying_to_cover:
  - 把两个汉字挤进一格，或一个汉字跨两格
  - 写有标题字的方格被旋转（只旋转空格或微排版格）
  - 方格大小不一、变成随意拼贴
  - 色系超过一个，或加入插画、照片、图标
  - 微排版写成解释性句子
```

## 风格意图

设计专业作品集封面式的「系统 + 玩心」：一块像填字游戏的方格网，标题的每个字被放进一个深色方块，几个方格被碰歪，四角布满档案式小字。纯排版，一个色系，有设计师的秩序感也有趣味。该风格只负责视觉语言；平台适配、长文提炼和通用封面约束由 `xenho-cover` 工作流负责。参考图见 `refs/tile-crossword/`。

## 与库内其他风格的分工

- `bw-type-specimen`：巨型衬线字的正负空间；本风格是方格系统 + 单色调。
- `exhibition-poster`：巨字撑满 + 多栏信息；本风格是小格子里的字 + 角落小字，更像作品集与档案。

## 适用

- 个人品牌、系列专栏、方法论、设计与创作类内容
- 自有产品发布（产品名逐字入格，非常醒目）
- 标题 4–12 字的观点文

## 避免

- 标题极长且无法拆出短标题的内容
- 需要情绪画面、摄影氛围的内容
