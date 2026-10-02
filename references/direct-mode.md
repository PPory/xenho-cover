# Direct 模式：经 CPA 直接出图（Single-shot）

Direct 模式必须先按 Prompt 模式完整编译出最终提示词，再调用图片接口。本文件只管出图这一层，不改风格和提示词编译规则。

图片接口走 CPA（CLIProxyAPI，OpenAI 兼容代理），不用 Grsai。

## 最高优先级：一次请求最多出一次图

**一个用户封面请求，最多发一次图片请求。**

「宿主没拿到 stdout」和「请求没发出去」是两回事。生成脚本一旦启动，就可能已经发出 POST；此后**禁止为了拿输出再跑一次**。

以下情况一律不自动重试：

- stdout 为空、工具没捕获输出；
- 结果解析失败；
- 超时或连接中断，无法确定服务端是否已经在出图；
- 结果文件暂时不存在，或仍是 `submitting`。

这些情况只能读结果文件，然后跟用户说明。要再出一张，必须是用户明确说「重新生成 / 再来一版 / 再试一次 / 换一个结果」。

## 配置

脚本按以下顺序找配置，找到即用：

1. 环境变量 `XENHO_COVER_BASE_URL`、`XENHO_COVER_API_KEY`、`XENHO_COVER_MODEL`；
2. `--env-file <dotenv>` 里的同名变量；
3. 同一个 dotenv 里工作台的 `AGENT_LLM_BASE_URL`、`AGENT_LLM_API_KEY`。

最省事的做法是直接指向工作台的 `.env`，不另存密钥：

```text
--env-file "D:/desktop桌面/01--Areas/02--代码开发/04--vibecoding/content-studio/workbench/.env"
```

几条硬规矩：

- 密钥永远不进提示词、聊天、日志或存档。脚本输出会做脱敏。
- 缺配置时脚本返回 `category: auth`，不会发请求。
- `~/.xenho-cover/config.json` 是 WorkBuddy 版留下的 Grsai 配置，本脚本**不读也不改**。

## 模型与端点

| 模型 | 端点 | 比例怎么传 | 图在哪 |
| --- | --- | --- | --- |
| `gemini-3.1-flash-image`（默认） | `{base}/chat/completions` | 顶层 `image_config: {aspect_ratio, image_size}` | `choices[0].message.images[].image_url.url`（data URL） |
| `gpt-image-*` | `{base}/images/generations` | `size`：横 `1536x1024`、竖 `1024x1536`、方 `1024x1024` | `data[0].b64_json` 或 `data[0].url` |

- **`gpt-image-*` 目前用不了**：CPA 给这类模型挑账号时会跳过 Free 计划的 codex 账号（`isFreeCodexAuth`），只有 Free 账号时永远返回 `auth_not_found`。接入付费 ChatGPT 账号之前用 gemini。
- **请求必须带 User-Agent**：CPA 前面有 Cloudflare，urllib 默认的 UA 会被以 1010 拦下。
- **默认不传 `image_size`（接口默认 1K）**：2026-10-02 实测 2K 的 3:4 要 135 秒，CPA 前面的 Cloudflare 100 秒就断开（HTTP 524），图可能已经出了、额度也花了却收不到。1K 约 25–65 秒。`--image-size 2K` 只在直连、不经 Cloudflare 时用。

## 比例

| 平台 | 设计比例 | gemini 收到的比例 | 交付 |
| --- | --- | --- | --- |
| 公众号 | 2.35:1 | 21:9 | 原图即可（实测 1584×672 = 2.357） |
| X | 5:2 | 21:9 | 居中裁到 5:2 |
| 小红书 / 视频号 | 3:4 | 3:4 | 原图 |
| YouTube | 16:9 | 16:9 | 原图 |

- 其他比例只能用 gemini 支持的：`1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9 1:4 4:1 1:8 8:1`。
- 本机装了 Pillow 时，脚本自动居中裁出一份 `-cropped`；没装就在结果里给出 `crop_note`。
- 提示词里写的始终是**设计比例**，构图按它安排。

## 唯一允许的生成路径

不要用宿主自己的 HTTP 工具直接 POST。所有出图都走 `scripts/cover_generate.py`：它负责防重复、请求指纹、持久化状态和结果文件。

步骤：

1. 用宿主的文件写入能力，把最终提示词直接存成 UTF-8 临时文件；同时定好结果文件和出图路径。
2. 只执行一次：

```text
python -X utf8 "<skill>/scripts/cover_generate.py" --prompt-file "<prompt.txt>" --ratio "3:4" --env-file "<.env>" --result-file "<result.json>" --out "~/.claude/data/xenho-cover/<YYYYMMDD>-<slug>.png"
```

3. **执行后不管 stdout 是什么，都不要再跑。直接读 `<result.json>`。**

配置有疑问时，先用 `--dry-run` 看端点、模型和比例对不对。它不联网，也不写任何状态。

## 防重复机制

请求指纹 = SHA-256(端点 + 完整请求体)，请求体里包含模型、比例和完整提示词。状态存在：

```text
~/.xenho-cover/jobs/<fingerprint>/
├── state.json
├── result.json
├── submit.lock
└── history/
```

脚本保证：

1. 发 POST 之前先写 `state = submitting`，再写好宿主指定的结果文件，标明「请求可能已发出，禁止自动重试」。
2. 同一请求 30 分钟内再跑，直接复用结果，不再 POST（`reused: true`）。
3. 上一次停在 `submitting` 或 `uncertain` 时，直接拦下新的 POST。
4. 同一请求并发运行时，由 `submit.lock` 挡住第二次。
5. 只有用户明确要求重新生成，才允许加 `--force-new`。它不是出错后的恢复开关。

## 结果文件

成功：

```json
{ "ok": true, "status": "succeeded", "image_path": "…/cover.jpg", "cropped_path": null, "api_request_sent": true, "safe_to_retry": false, "reused": false }
```

- `reused: true`：没有发新请求。
- `status: "uncertain"`：连接断了，服务端可能已经在出图。`safe_to_retry: false`，不要再跑。
- `category: "http"`：带 `status_code`，把 `error` 里的原因说给用户听。例如 `auth_not_found` 就是上面说的 Free 账号问题。

## 失败回退

1. 读 `<result.json>`。
2. `api_request_sent: true` 时，不再生成。
3. 用一句话说明原因。
4. 交付已经编译好的提示词（Prompt 模式）。不要让用户重新提供文章、平台、标题或风格。
