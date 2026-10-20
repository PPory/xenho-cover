"""cover_generate.py 的离线测试：假 Codex + 本机假代理，不联网、不花额度。

python -X utf8 tests/test_cover_generate.py
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "cover_generate.py"
# 1×1 PNG
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
calls = []
mode = {"value": "ok"}


class Proxy(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["content-length"])))
        calls.append({"path": self.path, "body": body, "ua": self.headers.get("user-agent"), "auth": self.headers.get("authorization")})
        if mode["value"] == "hang":
            self.close_connection = True
            return  # drop the connection without a response
        if self.path.endswith("/images/generations"):
            payload = {"data": [{"b64_json": base64.b64encode(PNG).decode()}]}
        else:
            payload = {"choices": [{"message": {"content": "", "images": [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(PNG).decode()}}]}}]}
        data = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run(tmp, *extra, env_extra=None):
    env = {**os.environ, "XENHO_COVER_BACKEND": "api", "XENHO_COVER_BASE_URL": base, "XENHO_COVER_API_KEY": "test-key-0123456789"}
    env.pop("XENHO_COVER_MODEL", None)
    env.update(env_extra or {})
    result_file = Path(tmp) / "result.json"
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "--prompt", "封面测试：汉字必须正确", "--ratio", "3:4",
                           "--jobs-dir", str(Path(tmp) / "jobs"), "--out", str(Path(tmp) / "cover.png"),
                           "--result-file", str(result_file), "--timeout", "5", *extra], capture_output=True, text=True, env=env)
    assert "test-key-0123456789" not in proc.stdout + proc.stderr, "key leaked to output"
    return proc.returncode, json.loads(result_file.read_text(encoding="utf-8"))


server = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}/v1"

with tempfile.TemporaryDirectory() as tmp:
    # dry run: no network, no state
    code, out = run(tmp, "--dry-run")
    assert code == 0 and out["dry_run"] and out["api_ratio"] == "1536x2048" and not calls and not (Path(tmp) / "jobs").exists(), out

    # first run: one request, gpt-image by default on the api backend, exact 3:4 size, opaque background, UA set, image saved
    code, out = run(tmp)
    assert code == 0 and out["ok"] and not out["reused"] and not out["crop_note"], out
    assert len(calls) == 1 and calls[0]["path"] == "/v1/images/generations", calls
    assert calls[0]["body"]["model"] == "gpt-image-2" and calls[0]["body"]["size"] == "1536x2048" and calls[0]["body"]["background"] == "opaque", calls[0]
    assert calls[0]["ua"].startswith("xenho-cover/"), calls[0]
    assert Path(out["image_path"]).read_bytes() == PNG

    # same request again: reused, nothing new sent
    code, out = run(tmp)
    assert code == 0 and out["reused"] and len(calls) == 1, (out, calls)

    # explicit new one goes through
    code, out = run(tmp, "--force-new")
    assert code == 0 and not out["reused"] and len(calls) == 2, out

with tempfile.TemporaryDirectory() as tmp:
    # dropped connection: uncertain, never retried, and a rerun is blocked
    mode["value"] = "hang"
    code, out = run(tmp)
    assert code == 1 and out["status"] == "uncertain" and out["api_request_sent"] and not out["safe_to_retry"], out
    sent = len(calls)
    code, out = run(tmp)
    assert code == 3 and out["reused"] and len(calls) == sent, (out, len(calls))
    mode["value"] = "ok"

with tempfile.TemporaryDirectory() as tmp:
    # gemini is still available by name: chat/completions with image_config
    code, out = run(tmp, env_extra={"XENHO_COVER_MODEL": "gemini-3.1-flash-image"})
    assert code == 0 and calls[-1]["path"] == "/v1/chat/completions" and calls[-1]["body"]["image_config"] == {"aspect_ratio": "3:4"}, calls[-1]

with tempfile.TemporaryDirectory() as tmp:
    def dry(ratio, model=None):
        extra = ["--model", model] if model else []
        proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "--prompt", "x", "--ratio", ratio, "--dry-run", "--backend", "api", "--base-url", base, *extra],
                              capture_output=True, text=True, env={**os.environ, "XENHO_COVER_API_KEY": "k"})
        return json.loads(proc.stdout)

    # gpt-image sizes hit each platform ratio; other ratios get a 2048 long edge; wider than 3:1 is refused
    for ratio, size in {"2.35:1": "1920x816", "5:2": "2560x1024", "16:9": "2048x1152", "1:1": "1536x1536", "9:16": "1152x2048"}.items():
        assert dry(ratio)["api_ratio"] == size, (ratio, dry(ratio))
    assert not dry("3.5:1")["ok"] and not dry("3.35:1")["ok"]
    # 5:2 maps to 21:9 for gemini
    assert dry("5:2", "gemini-3.1-flash-image")["api_ratio"] == "21:9"

server.shutdown()

# ---- codex backend (the default): a fake codex that logs its call and drops an image where Codex would
FAKE_CODEX = r'''
import json, os, sys, uuid
from pathlib import Path
stdin = sys.stdin.buffer.read().decode("utf-8")
with open(os.environ["FAKE_CODEX_LOG"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "stdin": stdin}, ensure_ascii=False) + "\n")
sid = str(uuid.uuid4())
print("OpenAI Codex (fake)\nsession id: " + sid, flush=True)
mode = os.environ.get("FAKE_CODEX_MODE", "ok")
if mode == "fail":
    print("Error: not signed in. Run codex login")
    sys.exit(1)
if mode != "noimage":
    from PIL import Image
    folder = Path(os.environ["CODEX_HOME"]) / "generated_images" / sid
    folder.mkdir(parents=True)
    image = Image.new("RGBA", (1086, 1448), (0, 0, 0, 0)) if mode == "transparent" else Image.new("RGB", (1086, 1448), (200, 30, 30))
    image.save(folder / "ig_0001.png")
print("DONE")
'''


def run_codex(tmp, *extra, mode="ok", installed=True):
    tmp = Path(tmp)
    fake = tmp / "fake_codex.py"
    fake.write_text(FAKE_CODEX, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if not k.startswith("XENHO_COVER_")}
    env.update({"CODEX_HOME": str(tmp / "codex-home"), "FAKE_CODEX_LOG": str(tmp / "codex-calls.jsonl"), "FAKE_CODEX_MODE": mode})
    if installed:
        env["XENHO_COVER_CODEX"] = str(fake)
    else:
        env["PATH"] = str(tmp)  # no codex anywhere
    result_file = tmp / "result.json"
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "--prompt", "封面测试：汉字必须正确", "--ratio", "3:4",
                           "--jobs-dir", str(tmp / "jobs"), "--out", str(tmp / "cover.png"), "--result-file", str(result_file),
                           "--timeout", "60", *extra], capture_output=True, text=True, env=env)
    log = tmp / "codex-calls.jsonl"
    codex_calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
    return proc.returncode, json.loads(result_file.read_text(encoding="utf-8")), codex_calls


with tempfile.TemporaryDirectory() as tmp:
    # dry run: codex found, size asked for in words, nothing run
    code, out, codex_calls = run_codex(tmp, "--dry-run")
    assert code == 0 and out["backend"] == "codex" and "aspect ratio 3:4 (for example 1536x2048)" in out["size_hint"] and not codex_calls, out

    # first run: one codex exec, read-only, prompt passed verbatim with the size hint, image copied out
    code, out, codex_calls = run_codex(tmp)
    assert code == 0 and out["ok"] and out["backend"] == "codex" and not out["reused"] and not out["transparent_warning"], out
    assert len(codex_calls) == 1, codex_calls
    argv, stdin = codex_calls[0]["argv"], codex_calls[0]["stdin"]
    assert argv[0] == "exec" and "--skip-git-repo-check" in argv and argv[argv.index("-s") + 1] == "read-only" and argv[-1] == "-", argv
    assert "封面测试：汉字必须正确" in stdin and "aspect ratio 3:4" in stdin and "exactly once" in stdin, stdin
    assert Path(out["image_path"]).exists() and not out["cropped_path"], out

    # same request again: reused, codex not run again
    code, out, codex_calls = run_codex(tmp)
    assert code == 0 and out["reused"] and len(codex_calls) == 1, (out, codex_calls)

with tempfile.TemporaryDirectory() as tmp:
    # codex not installed: nothing sent, the user is told what to do
    code, out, codex_calls = run_codex(tmp, installed=False)
    assert code == 2 and out["category"] == "codex_missing" and not out["api_request_sent"] and "codex login" in out["error"], out

with tempfile.TemporaryDirectory() as tmp:
    # codex fails (e.g. not signed in): terminal error with its output, no retry
    code, out, codex_calls = run_codex(tmp, mode="fail")
    assert code == 1 and out["category"] == "codex" and "not signed in" in out["codex_output"] and not out["safe_to_retry"], out

with tempfile.TemporaryDirectory() as tmp:
    # codex finishes without an image
    code, out, codex_calls = run_codex(tmp, mode="noimage")
    assert code == 1 and out["category"] == "response" and out["status"] == "failed", out

with tempfile.TemporaryDirectory() as tmp:
    # a transparent cut-out is saved but flagged
    code, out, codex_calls = run_codex(tmp, mode="transparent")
    assert code == 0 and out["transparent_warning"], out

print("cover_generate: ok")
