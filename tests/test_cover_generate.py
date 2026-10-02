"""cover_generate.py 的离线测试：本机假代理，不联网、不花额度。

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
    env = {**os.environ, "XENHO_COVER_BASE_URL": base, "XENHO_COVER_API_KEY": "test-key-0123456789"}
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
    assert code == 0 and out["dry_run"] and out["api_ratio"] == "3:4" and not calls and not (Path(tmp) / "jobs").exists(), out

    # first run: one request, gemini shape, UA set, image saved
    code, out = run(tmp)
    assert code == 0 and out["ok"] and not out["reused"], out
    assert len(calls) == 1 and calls[0]["path"] == "/v1/chat/completions", calls
    assert calls[0]["body"]["image_config"] == {"aspect_ratio": "3:4"}, calls[0]
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
    # gpt-image path and size by orientation
    code, out = run(tmp, env_extra={"XENHO_COVER_MODEL": "gpt-image-2.5-flare"})
    assert code == 0 and calls[-1]["path"] == "/v1/images/generations" and calls[-1]["body"]["size"] == "1024x1536", calls[-1]

with tempfile.TemporaryDirectory() as tmp:
    # 5:2 maps to 21:9 for gemini
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "--prompt", "x", "--ratio", "5:2", "--dry-run", "--base-url", base],
                          capture_output=True, text=True, env={**os.environ, "XENHO_COVER_API_KEY": "k"})
    assert json.loads(proc.stdout)["api_ratio"] == "21:9", proc.stdout

server.shutdown()
print("cover_generate: ok")
