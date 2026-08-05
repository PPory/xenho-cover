# xenho-cover

Claude Code skill：把文章 / 主题变成 Claude（Anthropic）官方风格的封面图像提示词，给辛禾自己发小红书、公众号、X 时配封面用。

## 目标

- 输入一篇文章或一个主题，产出一份可直接贴到 **image-2** 的完整图像生成提示词
- 风格库与工作流分离：加新风格只加 `styles/{id}/` 文件夹，不改 SKILL.md
- 最终提示词必须是「编译融合」的产物，不是「封面指令 + 风格原文」两段拼接

## 技术栈

- 纯 Markdown skill，无代码、无依赖
- 架构参考 [adrianpunk/Punk-Skill](https://github.com/adrianpunk/Punk-Skill) 的 punk-cover

## 启动

本项目通过 junction 安装为 Claude Code skill：

```powershell
New-Item -ItemType Junction -Path C:/Users/Lenovo/.claude/skills/xenho-cover -Target "D:/desktop桌面/01--Areas/02--代码开发/04--vibecoding/xenho-cover"
```

安装后在任意会话说「给这篇文章配个封面」即可触发。

## 部署

暂无（本地 skill，junction 即部署）。

## 目录约定

- `SKILL.md`：skill 入口，工作流 + 门控 + Gotchas
- `references/`：提示词结构模板（blueprint）和风格目录（catalog）
- `styles/{style-id}/`：风格原子，每个风格两个文件——`META.md`（结构化锚点）+ `STYLE.md`（视觉语言描述）
- `refs/{style-id}/`：风格参考图，按风格分子目录存放，开发期校准风格原子用，运行时不加载
- 生成的提示词存档在 `C:/Users/Lenovo/.claude/data/xenho-cover/`（skill 目录外，升级不丢）

## 加新风格的流程

1. 收集参考图放进 `refs/`
2. 新建 `styles/{new-id}/META.md` + `STYLE.md`（照 `anthropic-research` 的 schema）
3. 在 `references/style-catalog.md` 加一行
4. 风格 ≥ 3 个后，把 SKILL.md 门控从「单风格直用」改为「推荐 3 选 1」

## 验证

跑一遍端到端：拿一篇文章触发 skill → 应先问平台 → 选定后检查产出提示词：无 `{{占位符}}` 残留、无 STYLE.md 原文整段拼贴、标题层落在风格语言里。最终以 image-2 实际出图对照 `refs/` 校准。
