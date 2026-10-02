# xenho-cover

Claude Code skill：把文章 / 主题变成封面图像提示词（Prompt 模式），或经 CPA 直接出图（Direct 模式），给辛禾自己发小红书、公众号、X、视频号、YouTube 时配封面用。

## 目标

- 输入一篇文章或一个主题，产出一份完整图像生成提示词；Direct 模式再经 CPA 出一张图（默认 `gemini-3.1-flash-image`），一次请求最多出一次图
- 风格库与工作流分离：加新风格只加 `styles/{id}/` 文件夹，不改 SKILL.md
- 最终提示词必须是「编译融合」的产物，不是「封面指令 + 风格原文」两段拼接

## 技术栈

- Markdown skill + 一个 Python 出图脚本（`scripts/cover_generate.py`，只用标准库；装了 Pillow 时顺手裁到设计比例）
- 架构参考 [adrianpunk/Punk-Skill](https://github.com/adrianpunk/Punk-Skill) 的 punk-cover

## 启动

本项目通过 junction 安装为 Claude Code skill：

```powershell
New-Item -ItemType Junction -Path $HOME/.claude/skills/xenho-cover -Target "<本仓库克隆路径>"
```

安装后在任意会话说「给这篇文章配个封面」即可触发。

## 部署

暂无（本地 skill，junction 即部署）。

## 目录约定

- `SKILL.md`：skill 入口，工作流 + 门控 + Gotchas
- `references/`：提示词结构模板（blueprint）、风格目录（catalog）、Direct 模式说明（direct-mode）
- `scripts/`：Direct 模式出图脚本；`tests/`：它的离线测试
- `styles/{style-id}/`：风格原子，每个风格两个文件——`META.md`（结构化锚点）+ `STYLE.md`（视觉语言描述）
- `refs/{style-id}/`：风格参考图，按风格分子目录存放，开发期校准风格原子用，运行时不加载
- 生成的提示词和图存档在用户 home 目录下的 `.claude/data/xenho-cover/`（skill 目录外，升级不丢）；防重复状态在 `~/.xenho-cover/jobs/`

## 下游副本

工作台（`content-studio/.agents/skills/xenho-cover/`）带一份风格库副本：blueprint、catalog、`styles/*/META.md`、`STYLE.md` 和缩略图。**这里是真源**，改完到 `content-studio/workbench` 跑 `npm run sync:cover-styles`。

## 加新风格的流程

1. 收集参考图放进 `refs/`
2. 新建 `styles/{new-id}/META.md` + `STYLE.md`（照 `anthropic-research` 的 schema）
3. 在 `references/style-catalog.md` 加一行
4. 风格 ≥ 3 个后，把 SKILL.md 门控从「单风格直用」改为「推荐 3 选 1」

## 验证

跑一遍端到端：拿一篇文章触发 skill → 应先问平台 → 选定后检查产出提示词：无 `{{占位符}}` 残留、无 STYLE.md 原文整段拼贴、标题层落在风格语言里。最终以实际出图对照 `refs/` 校准。

出图脚本改动后跑离线测试（不联网、不花额度）：

```bash
python -X utf8 tests/test_cover_generate.py
```
