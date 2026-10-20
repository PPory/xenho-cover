# Direct 模式：直接出图（Single-shot）

Direct 模式必须先按 Prompt 模式完整编译出最终提示词，再出图。本文件只管出图这一层，不改风格和提示词编译规则。

出图有两个后端：

- **默认 `codex`**：本机 Codex CLI 的内置生图（GPT Image）。用 ChatGPT 登录、走 ChatGPT 套餐的生图额度，不需要 API key，不经代理。
- **备选 `api`**：任意 OpenAI 兼容的图像接口（官方接口、中转或代理都行），默认模型 `gpt-image-2`。用 `--backend api` 指定。

不用 Grsai。

## 最高优先级：每个画幅最多出一次图

**一个用户封面请求，每个画幅最多发一次图片请求。** 公众号是横版 `2.35:1` + 方版 `1:1` 两个画幅，所以脚本各跑一次、共两次；其他平台只有一个画幅，只跑一次。两份提示词不同，请求指纹也不同，下面的防重复机制按画幅各自生效。

「宿主没拿到 stdout」和「请求没发出去」是两回事。生成脚本一旦启动，就可能已经在出图；此后**禁止为了拿输出再跑一次**。

以下情况一律不自动重试：

- stdout 为空、工具没捕获输出；
- 结果解析失败；
- 超时或连接中断，无法确定是否已经在出图；
- 结果文件暂时不存在，或仍是 `submitting`。

这些情况只能读结果文件，然后跟用户说明。要再出一张，必须是用户明确说「重新生成 / 再来一版 / 再试一次 / 换一个结果」。

## 默认后端：本机 Codex

前提：装了 Codex CLI（`codex` 在 PATH 上），并且 `codex login` 用 ChatGPT 账号登录过。不需要任何配置文件。

脚本做的事：

- 跑一次 `codex exec --skip-git-repo-check -s read-only -c model_reasoning_effort="low" -C <空的临时目录> -`，指令从 stdin 传入。指令要求 Codex 只调用一次内置生图工具，把提示词原样交给它（不改写、不翻译），不建文件、不跑命令。
- 从输出里拿 `session id`，到 `~/.codex/generated_images/<session id>/` 取图，复制到 `--out`。设了 `CODEX_HOME` 时以它为准。
- Codex 的生图工具没有尺寸参数，比例用文字要：「aspect ratio 3:4 (for example 1536x2048)」。2026-10 实测 3:4 出 1086×1448，2.35:1 出 1922×818，1:1 出 1254×1254，都对得上。偏差超过 1% 时，装了 Pillow 会居中裁出一份 `-cropped`。
- 一张大约 1–1.5 分钟，默认超时 600 秒。
- `--codex-model` 或 `XENHO_COVER_CODEX_MODEL` 可以指定 Codex 用的模型，不填就用 Codex 自己 config 里的默认模型。推理强度固定为 low，因为 Codex 在这里只是把提示词转给生图工具。

几条要知道的：

- **没有 `background: "opaque"` 参数**：只能靠提示词「色彩」段那句「整张图完全不透明」。脚本出图后会检查，透明处超过 1% 时结果里带 `transparent_warning`。这时不要交付这张图，告诉用户，问要不要重出（重出算新的一次出图）。
- **用的是 ChatGPT 套餐的生图额度**：额度用完、没登录、断网时，Codex 会非 0 退出，结果是 `category: "codex"`，`codex_output` 里有它最后几行输出。把原因转述给用户，比如「Codex 没登录，在终端跑一次 `codex login` 再说出图」。
- **找不到 codex**：结果是 `category: "codex_missing"`，没有发出任何请求。告诉用户先装 Codex CLI 并登录，或者改用 `--backend api`。

## 备选后端：图像接口（`--backend api`）

脚本按以下顺序找配置，找到即用：

1. 环境变量 `XENHO_COVER_BASE_URL`、`XENHO_COVER_API_KEY`、`XENHO_COVER_MODEL`；
2. `--env-file <dotenv>` 里的同名变量；
3. 同一个 dotenv 里工作台的 `AGENT_LLM_BASE_URL`、`AGENT_LLM_API_KEY`。

想长期用这个后端，可以设环境变量 `XENHO_COVER_BACKEND=api`，不用每次都加参数。

几条硬规矩：

- 密钥永远不进提示词、聊天、日志或存档。脚本输出会做脱敏。
- 缺配置时脚本返回 `category: auth`，不会发请求。
- `~/.xenho-cover/config.json` 是 WorkBuddy 版留下的 Grsai 配置，本脚本**不读也不改**。

| 模型 | 端点 | 比例怎么传 | 图在哪 |
| --- | --- | --- | --- |
| `gpt-image-2`（默认，其他 `gpt-image-*` 同） | `{base}/images/generations` | `size`：按设计比例算出的精确尺寸（见下表），并带 `background: "opaque"` | `data[0].b64_json` 或 `data[0].url` |
| `gemini-3.1-flash-image`（`--model` 指定） | `{base}/chat/completions` | 顶层 `image_config: {aspect_ratio, image_size}` | `choices[0].message.images[].image_url.url`（data URL） |

- **`background: "opaque"` 必须带**：不带时，物件摄影类画面（小票、瓶子、便利贴）会被当成去底产品图，输出透明底 PNG，底色整张丢失（2026-10 实测）。
- **有的代理挑账号时会跳过免费账号**：只有免费账号时，gpt-image 永远返回 `auth_not_found`。这不是配置坏了。改用默认的 Codex 后端，或者接入付费账号，或者用 `--model gemini-3.1-flash-image`。
- **请求必须带 User-Agent**：接口前面有 Cloudflare 时，urllib 默认的 UA 会被以 1010 拦下。脚本已经带上。
- **经 Cloudflare 的请求超过 100 秒会断开**（HTTP 524），图可能已经出了、额度也花了却收不到。gemini 默认不传 `image_size`（接口默认 1K，约 25–65 秒；2026-10-02 实测 2K 的 3:4 要 135 秒）。`--image-size 2K` 只在不经 Cloudflare 时用。

## 比例

| 平台 | 设计比例 | Codex / gpt-image 尺寸 | gemini 比例 | 交付 |
| --- | --- | --- | --- | --- |
| 公众号 · 横版 | 2.35:1 | 1920×816 | 21:9（1584×672） | 原图 |
| 公众号 · 方版 | 1:1 | 1536×1536 | 1:1 | 原图；和横版一起用 `wechat_combine.py` 拼成 3.35:1 |
| X | 5:2 | 2560×1024 | 21:9 | gpt-image 原图；gemini 居中裁到 5:2 |
| 小红书 / 视频号 | 3:4 | 1536×2048 | 3:4 | 原图 |
| YouTube | 16:9 | 2048×1152 | 16:9 | 原图 |

- Codex 后端的尺寸是写进指令的示例，实际出图尺寸由 Codex 决定，比例一致。
- gpt-image 的其他比例：长边 2048、两边取 16 的倍数；长短边之比超过 3:1 的画不了，脚本直接拒绝。Codex 底层也是 gpt-image，同样受这个限制。
- gemini 只认这些比例：`1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9 1:4 4:1 1:8 8:1`。
- 本机装了 Pillow 时，脚本自动居中裁出一份 `-cropped`；没装就在结果里给出 `crop_note`。
- 提示词里写的始终是**设计比例**，构图按它安排。
- `--ratio 3.35:1` 会被脚本直接拒绝（不出图）：它是公众号的上传拼合图，不是生成比例。

## 公众号：两张出图 + 拼合

1. 横版、方版两份提示词各存一个 `prompt.txt`，各定一个结果文件和出图路径（`<slug>-header.png`、`<slug>-square.png`）。
2. `cover_generate.py` 各执行一次：`--ratio "2.35:1"` 和 `--ratio "1:1"`。同样不管 stdout，各自只读自己的结果文件。
3. 两张都成功后执行一次：

```text
python -X utf8 "<skill>/scripts/wechat_combine.py" "<slug>-header.png" "<slug>-square.png" --out "<slug>-wechat.png"
```

   它把横版居中裁到精确的 2.35:1、方版裁到 1:1，统一高度后左右拼接，输出 JSON 里有拼合图路径和框选提示（2.35:1 框拖到最左、1:1 框拖到最右）。拼合是本地操作、不花额度，失败可以重跑。退出码 3、`category: "transparent"` 表示某张是透明底抠图（底色丢了），不拼，告诉用户是哪一张、问要不要重出那一张（重出要用户同意，算新的一次出图）。
4. 只成功一张：不重试另一张，交付成功的那张，另一张给已编译的提示词。

## 唯一允许的生成路径

不要自己调 Codex、也不要用宿主的 HTTP 工具直接 POST。所有出图都走 `scripts/cover_generate.py`：它负责防重复、请求指纹、持久化状态和结果文件。

步骤：

1. 用宿主的文件写入能力，把最终提示词直接存成 UTF-8 临时文件；同时定好结果文件和出图路径。
2. 只执行一次：

```text
python -X utf8 "<skill>/scripts/cover_generate.py" --prompt-file "<prompt.txt>" --ratio "3:4" --result-file "<result.json>" --out "~/.claude/data/xenho-cover/<YYYYMMDD>-<slug>.png"
```

   Codex 一张要 1 分钟以上，宿主的命令超时要留够（建议 10 分钟）。用图像接口时加 `--backend api --env-file "<.env>"`。

3. **执行后不管 stdout 是什么，都不要再跑。直接读 `<result.json>`。**

配置有疑问时，先用 `--dry-run` 看后端、codex 路径（或端点、模型）和比例对不对。它不调用 Codex、不联网，也不写任何状态。

## 防重复机制

请求指纹 = SHA-256(端点 + 完整请求体)。请求体里包含后端、模型、比例和完整提示词（Codex 后端是完整的指令文本）。状态存在：

```text
~/.xenho-cover/jobs/<fingerprint>/
├── state.json
├── result.json
├── submit.lock
└── history/
```

脚本保证：

1. 启动 Codex 或发 POST 之前，先写 `state = submitting`，再写好宿主指定的结果文件，标明「请求可能已发出，禁止自动重试」。
2. 同一请求 30 分钟内再跑，直接复用结果，不再出图（`reused: true`）。
3. 上一次停在 `submitting` 或 `uncertain` 时，直接拦下新的请求。
4. 同一请求并发运行时，由 `submit.lock` 挡住第二次。
5. 只有用户明确要求重新生成，才允许加 `--force-new`。它不是出错后的恢复开关。

## 结果文件

成功：

```json
{ "ok": true, "status": "succeeded", "backend": "codex", "image_path": "…/cover.png", "cropped_path": null, "transparent_warning": null, "api_request_sent": true, "safe_to_retry": false, "reused": false }
```

- `reused: true`：没有发新请求。
- `transparent_warning` 不为空：图是透明底抠图，不交付，见上文。
- `status: "uncertain"`：Codex 超时或连接断了，可能已经在出图。`safe_to_retry: false`，不要再跑。Codex 超时的图可能稍后出现在 `~/.codex/generated_images/` 里。
- `category: "codex"`：Codex 出错退出，把 `codex_output` 里的原因说给用户听。
- `category: "codex_missing"`：没装 Codex，没有发出请求。
- `category: "http"`（api 后端）：带 `status_code`，把 `error` 里的原因说给用户听。例如 `auth_not_found` 就是上面说的免费账号问题。

## 失败回退

1. 读 `<result.json>`。
2. `api_request_sent: true` 时，不再生成。
3. 用一句话说明原因，并说下一步该怎么做。
4. 交付已经编译好的提示词（Prompt 模式）。不要让用户重新提供文章、平台、标题或风格。
