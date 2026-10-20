#!/usr/bin/env python3
"""Join a 2.35:1 header and a 1:1 square into one 3.35:1 WeChat cover upload.

WeChat takes a single cover image and lets you frame a 2.35:1 crop (header in the
subscription feed) and a 1:1 crop (share card, article list) on it. Putting two
purpose-built compositions side by side lets each frame land on a complete design:
drag the 2.35:1 frame to the far left and the 1:1 frame to the far right.

No model can draw 3.35:1 in one go (gpt-image caps at 3:1, gemini jumps from 21:9 to
4:1), so the two panels are generated separately and joined here. Needs Pillow.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cover_generate import MAX_TRANSPARENT_SHARE, crop_box, transparent_share  # noqa: E402

HEADER_RATIO = 2.35
FRAMING_HINT = "上传后在公众号后台：2.35:1 框拖到最左，1:1 框拖到最右"


def combine(header_path: Path, square_path: Path, out_path: Path) -> dict:
    from PIL import Image  # type: ignore

    with Image.open(header_path) as header_src, Image.open(square_path) as square_src:
        see_through = {str(path): round(share, 3) for path, share in ((header_path, transparent_share(header_src)), (square_path, transparent_share(square_src))) if share > MAX_TRANSPARENT_SHARE}
        if see_through:
            return {"ok": False, "category": "transparent", "transparent_share": see_through,
                    "error": "这张图是透明底抠图，底色丢了，拼上去透明处会变黑或变白。重出这一张，提示词「色彩」段要写明整张不透明、底色铺满四边"}
        header = header_src.convert("RGB").crop(crop_box(*header_src.size, HEADER_RATIO))
        square = square_src.convert("RGB").crop(crop_box(*square_src.size, 1.0))
    height = min(header.height, square.height)
    header_w = round(height * HEADER_RATIO)
    header = header.resize((header_w, height), Image.LANCZOS)
    square = square.resize((height, height), Image.LANCZOS)
    canvas = Image.new("RGB", (header_w + height, height))
    canvas.paste(header, (0, 0))
    canvas.paste(square, (header_w, 0))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)
    return {"ok": True, "combined_path": str(out_path), "size": [canvas.width, canvas.height],
            "header_box": [0, 0, header_w, height], "square_box": [header_w, 0, header_w + height, height],
            "hint": FRAMING_HINT}


def main() -> int:
    parser = argparse.ArgumentParser(description="Join a 2.35:1 header and a 1:1 square into a 3.35:1 WeChat cover")
    parser.add_argument("header", help="2.35:1 header image (other shapes are center-cropped)")
    parser.add_argument("square", help="1:1 square image (other shapes are center-cropped)")
    parser.add_argument("--out", help="Output path; defaults to <header>-wechat.png next to the header")
    args = parser.parse_args()
    header, square = Path(args.header).expanduser(), Path(args.square).expanduser()
    out = Path(args.out).expanduser() if args.out else header.with_name(header.stem + "-wechat.png")
    for path in (header, square):
        if not path.is_file():
            print(json.dumps({"ok": False, "error": f"Image not found: {path}"}, ensure_ascii=False))
            return 1
    try:
        import PIL  # type: ignore  # noqa: F401
    except ImportError:
        print(json.dumps({"ok": False, "error": "需要 Pillow：先 pip install pillow 再重跑；两张单图本身仍可用"}, ensure_ascii=False))
        return 2
    result = combine(header, square, out)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())
