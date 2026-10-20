"""wechat_combine.py 的离线测试：造两张纯色假图，检查拼合比例和左右来源。

python -X utf8 tests/test_wechat_combine.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "wechat_combine.py"
RED, BLUE = (220, 30, 30), (30, 60, 220)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    # gemini 21:9 comes back 1584x672 (slightly wider than 2.35); the square is larger and gets scaled down
    Image.new("RGB", (1584, 672), RED).save(tmp / "header.png")
    Image.new("RGB", (1024, 1024), BLUE).save(tmp / "square.png")
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(tmp / "header.png"), str(tmp / "square.png"),
                           "--out", str(tmp / "out" / "wechat.png")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = json.loads(proc.stdout)
    w, h = out["size"]
    assert h == 672 and abs(w / h - 3.35) < 0.01, out
    hx0, _, hx1, _ = out["header_box"]
    sx0, _, sx1, _ = out["square_box"]
    assert hx0 == 0 and hx1 == sx0 and sx1 == w and sx1 - sx0 == h and abs(hx1 / h - 2.35) < 0.005, out
    with Image.open(out["combined_path"]) as image:
        assert image.getpixel((5, h // 2)) == RED and image.getpixel((hx1 - 5, h // 2)) == RED
        assert image.getpixel((sx0 + 5, h // 2)) == BLUE and image.getpixel((w - 5, h // 2)) == BLUE

    # default output path, and a missing file is reported instead of crashing
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(tmp / "header.png"), str(tmp / "square.png")],
                          capture_output=True, text=True)
    assert proc.returncode == 0 and (tmp / "header-wechat.png").exists(), proc.stdout
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(tmp / "nope.png"), str(tmp / "square.png")],
                          capture_output=True, text=True)
    assert proc.returncode == 1 and not json.loads(proc.stdout)["ok"], proc.stdout

    # a cut-out with a transparent background is refused, not flattened into black edges
    cutout = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    cutout.paste((250, 250, 245, 255), (300, 0, 724, 900))
    cutout.save(tmp / "cutout.png")
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(tmp / "header.png"), str(tmp / "cutout.png"),
                           "--out", str(tmp / "refused.png")], capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert proc.returncode == 3 and out["category"] == "transparent" and not (tmp / "refused.png").exists(), out
    # an RGBA file that is fully opaque still goes through
    Image.new("RGBA", (1024, 1024), (30, 60, 220, 255)).save(tmp / "opaque.png")
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), str(tmp / "header.png"), str(tmp / "opaque.png"),
                           "--out", str(tmp / "opaque-out.png")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout

print("wechat_combine: ok")
