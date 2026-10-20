#!/usr/bin/env python3
"""Single-shot cover image client for an OpenAI-compatible image API (relay or proxy),
with duplicate-request protection.

The guarantee is conservative: one invocation creates at most one image request.
Re-running the same request shortly afterwards reuses the cached result instead of
POSTing again. If a previous request may have been sent but no final response was
recorded, the script refuses to retry automatically.

Two protocols, picked by model name:
- gpt-image-* (default gpt-image-2): POST {base}/images/generations with a custom size
  computed from the design ratio and an opaque background; the image comes back as
  data[0].b64_json or data[0].url. (Some proxies skip free-plan accounts for these models.)
- gemini-*-image: POST {base}/chat/completions with a top-level image_config.aspect_ratio;
  the image comes back as a data URL in choices[0].message.images[].image_url.url.

Standard library only (Pillow is used for the final crop when it happens to be
installed). Secrets come from XENHO_COVER_API_KEY or an --env-file and are never printed.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "gpt-image-2"
DEFAULT_JOBS_DIR = Path.home() / ".xenho-cover" / "jobs"
DEFAULT_OUT_DIR = Path.home() / ".claude" / "data" / "xenho-cover"
USER_AGENT = "xenho-cover/3.0-single-shot"
# Platform design ratio -> ratio the image API can produce. 21:9 comes back as
# 1584x672 (2.357), which is the WeChat 2.35:1 cover as is; X 5:2 is center-cropped.
PLATFORM_RATIO_ALIASES = {"2.35:1": "21:9", "5:2": "21:9"}
GEMINI_RATIOS = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1"}
# gpt-image takes any size whose edges are multiples of 16, long:short <= 3, and 0.65M-8.3M pixels.
# Platform ratios get hand-picked sizes that hit the ratio exactly; anything else gets a 2048 long edge.
GPT_IMAGE_SIZES = {"2.35:1": "1920x816", "5:2": "2560x1024", "3:4": "1536x2048", "16:9": "2048x1152", "1:1": "1536x1536"}
GPT_IMAGE_MAX_RATIO = 3.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(text: str) -> str:
    text = re.sub(r"sk-[A-Za-z0-9_\-]{8,}", "sk-[REDACTED]", text)
    return re.sub(r"(Bearer\s+)[A-Za-z0-9_\-.]{8,}", r"\1[REDACTED]", text)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return data


def read_env_file(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    env: dict[str, str] = {}
    for line in Path(path).expanduser().read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def resolve_config(args: argparse.Namespace) -> tuple[str, str, str]:
    """XENHO_COVER_* first; an --env-file may supply them or the workbench's AGENT_LLM_* pair."""
    file_env = read_env_file(args.env_file)

    def pick(*names: str) -> str:
        for name in names:
            value = os.environ.get(name) or file_env.get(name)
            if value:
                return value.strip()
        return ""

    base = (args.base_url or pick("XENHO_COVER_BASE_URL", "AGENT_LLM_BASE_URL")).rstrip("/")
    key = pick("XENHO_COVER_API_KEY", "AGENT_LLM_API_KEY")
    model = args.model or pick("XENHO_COVER_MODEL", "COVER_IMAGE_MODEL") or DEFAULT_MODEL
    return base, key, model


def read_prompt(args: argparse.Namespace) -> str:
    prompt = args.prompt if args.prompt is not None else Path(args.prompt_file).read_text(encoding="utf-8-sig")
    prompt = prompt.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not prompt:
        raise RuntimeError("Prompt is empty")
    return prompt


def is_gpt_image(model: str) -> bool:
    return model.lower().startswith("gpt-image")


def ratio_value(ratio: str) -> float:
    w, h = (float(x) for x in ratio.split(":"))
    return w / h


def gpt_image_size(ratio: str) -> str:
    if ratio in GPT_IMAGE_SIZES:
        return GPT_IMAGE_SIZES[ratio]
    value = ratio_value(ratio)
    if max(value, 1 / value) > GPT_IMAGE_MAX_RATIO:
        raise RuntimeError(f"gpt-image cannot draw {ratio}: the long edge may be at most 3x the short edge")
    snap = lambda x: max(16, round(x / 16) * 16)  # noqa: E731
    width, height = (2048, snap(2048 / value)) if value >= 1 else (snap(2048 * value), 2048)
    return f"{width}x{height}"


def api_ratio_for(requested: str, model: str) -> str:
    requested = requested.strip()
    if not re.fullmatch(r"\d+(\.\d+)?:\d+(\.\d+)?", requested):
        raise RuntimeError(f"Ratio must look like 3:4 or 2.35:1, got {requested!r}")
    if requested == "3.35:1":
        raise RuntimeError("3.35:1 is the WeChat combined upload, not a generation ratio: generate 2.35:1 and 1:1 separately, then join them with scripts/wechat_combine.py")
    if is_gpt_image(model):
        return gpt_image_size(requested)
    api_ratio = PLATFORM_RATIO_ALIASES.get(requested, requested)
    if api_ratio not in GEMINI_RATIOS:
        raise RuntimeError(f"Unsupported ratio {requested}. Use one of: {', '.join(sorted(GEMINI_RATIOS))} (2.35:1 and 5:2 map to 21:9)")
    return api_ratio


def build_request(base: str, model: str, prompt: str, api_ratio: str, image_size: str) -> tuple[str, dict[str, Any]]:
    if is_gpt_image(model):
        # opaque: object shots otherwise come back as transparent cut-outs with the background colour gone
        return f"{base}/images/generations", {"model": model, "prompt": prompt, "n": 1, "size": api_ratio, "background": "opaque"}
    config: dict[str, Any] = {"aspect_ratio": api_ratio}
    if image_size:
        config["image_size"] = image_size
    return f"{base}/chat/completions", {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "image_config": config,
        "stream": False,
    }


def request_fingerprint(endpoint: str, body: dict[str, Any]) -> str:
    canonical = endpoint + "\n" + json.dumps(body, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def extract_image(payload: dict[str, Any]) -> tuple[bytes | None, str, str | None]:
    """Returns (bytes, extension, remote_url)."""
    images = (((payload.get("choices") or [{}])[0].get("message") or {}).get("images")) or []
    for item in images:
        url = ((item or {}).get("image_url") or {}).get("url") or ""
        if url.startswith("data:"):
            head, _, data = url.partition(",")
            return base64.b64decode(data), "jpg" if "jpeg" in head else "webp" if "webp" in head else "png", None
        if url:
            return None, "png", url
    for item in payload.get("data") or []:
        if item.get("b64_json"):
            return base64.b64decode(item["b64_json"]), "png", None
        if item.get("url"):
            return None, "png", item["url"]
    return None, "png", None


def crop_box(width: int, height: int, target: float) -> tuple[int, int, int, int]:
    """Largest centered box with width / height == target."""
    if width / height > target:
        new_w = round(height * target)
        return ((width - new_w) // 2, 0, (width - new_w) // 2 + new_w, height)
    new_h = round(width / target)
    return (0, (height - new_h) // 2, width, (height - new_h) // 2 + new_h)


def center_crop(path: Path, ratio: str) -> Path | None:
    """Crop to the design ratio when Pillow is installed; otherwise leave the original."""
    try:
        from PIL import Image  # type: ignore
    except Exception:
        return None
    target = ratio_value(ratio)
    with Image.open(path) as image:
        width, height = image.size
        if abs(width / height - target) < 0.01:
            return None
        out = path.with_name(path.stem + "-cropped" + path.suffix)
        image.crop(crop_box(width, height, target)).save(out)
        return out


def emit(payload: dict[str, Any], result_file: Path | None, code: int = 0) -> int:
    if result_file is not None:
        atomic_json(result_file, payload)
    print(json.dumps(payload, ensure_ascii=False))
    return code


def archive_previous(job_dir: Path) -> None:
    files = [job_dir / "state.json", job_dir / "result.json"]
    if not any(f.exists() for f in files):
        return
    history = job_dir / "history"
    history.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    for f in files:
        if f.exists():
            shutil.copy2(f, history / f"{stamp}-{f.name}")


def parse_iso(value: str | None) -> float | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp() if value else None
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Single-shot cover image client (OpenAI-compatible image API)")
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Final compiled image prompt")
    prompt_group.add_argument("--prompt-file", help="UTF-8 file containing the final prompt")
    parser.add_argument("--ratio", required=True, help='Design ratio, e.g. "3:4", "2.35:1", "5:2"')
    parser.add_argument("--env-file", help="dotenv file with XENHO_COVER_* or the workbench AGENT_LLM_BASE_URL / AGENT_LLM_API_KEY")
    parser.add_argument("--base-url", help="Override the proxy base URL (…/v1)")
    parser.add_argument("--model", help=f"Override model; defaults to {DEFAULT_MODEL}")
    parser.add_argument("--image-size", default="", help='gemini only: "" (omit, the API default 1K), "1K" or "2K"; 2K can exceed the 100 s Cloudflare limit')
    parser.add_argument("--out", help="Where to save the image (extension follows the returned format)")
    parser.add_argument("--timeout", type=int, default=240, help="HTTP timeout seconds")
    parser.add_argument("--result-file", help="Known JSON output path for the host to read after execution")
    parser.add_argument("--jobs-dir", default=str(DEFAULT_JOBS_DIR), help="Persistent duplicate-guard directory")
    parser.add_argument("--dedupe-minutes", type=int, default=30, help="Reuse finished identical requests within this window")
    parser.add_argument("--force-new", action="store_true", help="New request despite cached state; only after the user explicitly asks")
    parser.add_argument("--dry-run", action="store_true", help="Resolve config and print the request shape; no network, no state")
    args = parser.parse_args()
    result_file = Path(args.result_file).expanduser() if args.result_file else None

    try:
        base, key, model = resolve_config(args)
        prompt = read_prompt(args)
        api_ratio = api_ratio_for(args.ratio, model)
        endpoint, body = build_request(base or "<missing>", model, prompt, api_ratio, args.image_size)
        fingerprint = request_fingerprint(endpoint, body)
        if args.dry_run:
            shown = {k: v for k, v in body.items() if k not in {"prompt", "messages"}}
            return emit({"ok": bool(base and key), "dry_run": True, "endpoint": endpoint, "model": model,
                         "requested_ratio": args.ratio, "api_ratio": api_ratio, "body": shown,
                         "prompt_chars": len(prompt), "has_key": bool(key), "request_fingerprint": fingerprint,
                         "api_request_sent": False}, result_file, 0 if base and key else 2)
        if not base or not key:
            return emit({"ok": False, "category": "auth",
                         "error": "Missing base URL or key: set XENHO_COVER_BASE_URL / XENHO_COVER_API_KEY or pass --env-file",
                         "api_request_sent": False, "safe_to_retry": True}, result_file, 2)

        job_dir = Path(args.jobs_dir).expanduser() / fingerprint
        state_path, cached_path, lock_path = job_dir / "state.json", job_dir / "result.json", job_dir / "submit.lock"
        job_dir.mkdir(parents=True, exist_ok=True)
        state = load_json(state_path)
        state_status = state.get("state")

        def context(payload: dict[str, Any], reused: bool) -> dict[str, Any]:
            out = dict(payload, request_fingerprint=fingerprint, job_dir=str(job_dir), reused=reused)
            if result_file is not None:
                out["result_file"] = str(result_file)
            return out

        # A previous request may have left us without a final response. Never guess it
        # failed; block automatic retries until the user explicitly asks for a new one.
        if state_status in {"submitting", "uncertain"} and not args.force_new:
            cached = load_json(cached_path) or {
                "ok": False, "category": "duplicate_guard", "status": state_status,
                "error": "A previous identical request may already have been sent. Automatic retry is blocked to avoid double billing.",
                "api_request_sent": True, "safe_to_retry": False,
            }
            return emit(context(cached, True), result_file, 3)

        # Finished identical requests are reused for a short window: this is what stops an
        # agent from re-running the command because it did not see stdout.
        if state_status in {"succeeded", "terminal_error"} and not args.force_new:
            updated = parse_iso(state.get("updated_at") or state.get("created_at"))
            if updated and (time.time() - updated) / 60 <= max(args.dedupe_minutes, 0):
                cached = load_json(cached_path) or {"ok": False, "category": "duplicate_guard", "status": state_status,
                                                    "error": "Identical request finished recently; nothing new was sent.",
                                                    "api_request_sent": True, "safe_to_retry": False}
                return emit(context(cached, True), result_file, 0 if cached.get("ok") else 1)

        if args.force_new and lock_path.exists():
            if time.time() - lock_path.stat().st_mtime > args.timeout + 60:
                lock_path.unlink(missing_ok=True)
            else:
                return emit(context({"ok": False, "category": "duplicate_guard", "status": "busy",
                                     "error": "An identical request is still in progress; nothing new was sent.",
                                     "api_request_sent": False, "safe_to_retry": False}, True), result_file, 3)
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()}\ncreated_at={utc_now()}\n".encode("utf-8"))
            os.close(fd)
        except FileExistsError:
            return emit(context({"ok": False, "category": "duplicate_guard", "status": "busy",
                                 "error": "Another identical generation is running; nothing new was sent.",
                                 "api_request_sent": False, "safe_to_retry": False}, True), result_file, 3)

        try:
            if args.force_new or state_status:
                archive_previous(job_dir)
            started = utc_now()
            state = {"state": "submitting", "created_at": started, "updated_at": started, "request_fingerprint": fingerprint,
                     "requested_ratio": args.ratio, "api_ratio": api_ratio, "model": model, "endpoint": endpoint}
            atomic_json(state_path, state)
            # Known result file before the POST: if the host loses stdout or kills us, it
            # still reads that a request may have gone out.
            if result_file is not None:
                atomic_json(result_file, context({"ok": False, "category": "submitting", "status": "submitting",
                                                  "error": "Request is being submitted. Do not retry automatically.",
                                                  "api_request_sent": True, "safe_to_retry": False,
                                                  "requested_ratio": args.ratio, "api_ratio": api_ratio}, False))

            def finish(payload: dict[str, Any], next_state: str, code: int) -> int:
                payload = context(dict(payload, api_request_sent=True, safe_to_retry=False,
                                       requested_ratio=args.ratio, api_ratio=api_ratio, model=model), False)
                atomic_json(cached_path, payload)
                state.update({"state": next_state, "updated_at": utc_now()})
                atomic_json(state_path, state)
                return emit(payload, result_file, code)

            request = urllib.request.Request(endpoint, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), method="POST", headers={
                "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json",
                # Cloudflare in front of the proxy rejects urllib's default UA (error 1010)
                "User-Agent": USER_AGENT,
            })
            try:
                with urllib.request.urlopen(request, timeout=args.timeout) as response:
                    raw = response.read().decode("utf-8", errors="replace")
            except urllib.error.HTTPError as exc:
                text = exc.read().decode("utf-8", errors="replace")
                return finish({"ok": False, "category": "http", "status": "failed", "status_code": exc.code,
                               "error": redact(text[:1000] or str(exc))}, "terminal_error", 1)
            except Exception as exc:
                # Once urlopen() was entered, a transport error is ambiguous: the server may
                # already be generating. Treat it as possibly billed.
                return finish({"ok": False, "category": "uncertain_network", "status": "uncertain",
                               "error": redact(str(getattr(exc, "reason", exc))),
                               "note": "The server may have received the request. Automatic retry is blocked."}, "uncertain", 1)

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                return finish({"ok": False, "category": "response", "status": "failed",
                               "error": "Response is not valid JSON", "body": redact(raw[:1000])}, "terminal_error", 1)
            data, ext, remote_url = extract_image(payload)
            if data is None and not remote_url:
                text = (((payload.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
                return finish({"ok": False, "category": "response", "status": "failed",
                               "error": "The response contains no image", "model_text": redact(str(text)[:300])}, "terminal_error", 1)
            if data is None:
                with urllib.request.urlopen(urllib.request.Request(remote_url, headers={"User-Agent": USER_AGENT}), timeout=args.timeout) as r:
                    data = r.read()
            out = Path(args.out).expanduser() if args.out else DEFAULT_OUT_DIR / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{fingerprint[:8]}.{ext}"
            out = out.with_suffix("." + ext)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            cropped = center_crop(out, args.ratio)
            # gpt-image sizes hit the design ratio; gemini's 21:9 already is the 2.35:1 cover; anything else needs a crop
            needs_crop = not is_gpt_image(model) and args.ratio not in {api_ratio, "2.35:1"}
            return finish({"ok": True, "category": "success", "status": "succeeded", "image_path": str(out),
                           "cropped_path": str(cropped) if cropped else None, "bytes": len(data),
                           "crop_note": f"Generated at {api_ratio}; center-crop to {args.ratio} before uploading" if needs_crop and not cropped else None},
                          "succeeded", 0)
        finally:
            # A hard kill skips this; the stale lock plus state=submitting then block a duplicate on purpose.
            try:
                lock_path.unlink(missing_ok=True)
            except Exception:
                pass
    except Exception as exc:
        return emit({"ok": False, "category": "client", "error": redact(str(exc)),
                     "api_request_sent": False, "safe_to_retry": True}, result_file, 1)


if __name__ == "__main__":
    sys.exit(main())
