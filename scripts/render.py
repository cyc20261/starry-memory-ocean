#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render.py — 星空记忆海 · 渲染器

把 collect_memories.py 产出的 JSON + 星云背景图，注入 HTML 模板，
生成一个自包含（离线可开、无外部依赖）的星空记忆海网页。

用法：
  python render.py --data memories.json --out "星空记忆海.html"
  python render.py --data memories.json --out out.html --title "我的记忆宇宙" --no-bg
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
TEMPLATE = os.path.join(SKILL_DIR, "assets", "ocean-template.html")
DEFAULT_BG = os.path.join(SKILL_DIR, "assets", "nebula-bg.png")


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="星空记忆海 · 渲染器")
    ap.add_argument("--data", required=True, help="collect_memories.py 输出的 JSON")
    ap.add_argument("--out", default="", help="输出 HTML 路径；留空则打印到 stdout")
    ap.add_argument("--title", default="星空记忆海", help="页面标题")
    ap.add_argument("--bg", default=DEFAULT_BG, help="星云背景图路径")
    ap.add_argument("--no-bg", action="store_true", help="不使用背景图（纯 CSS 星空）")
    args = ap.parse_args()

    data = json.loads(read_text(args.data))
    template = read_text(TEMPLATE)

    # 背景图 -> data URI
    bg_uri = ""
    if not args.no_bg and os.path.isfile(args.bg):
        with open(args.bg, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        ext = os.path.splitext(args.bg)[1].lstrip(".").lower() or "png"
        if ext == "jpg":
            ext = "jpeg"
        bg_uri = "data:image/%s;base64,%s" % (ext, b64)

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    gen_time = data.get("meta", {}).get("generated_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = template
    html = html.replace("__OCEAN_TITLE__", args.title)
    html = html.replace("__OCEAN_DATA__", payload)
    html = html.replace("__OCEAN_BG__", bg_uri)
    html = html.replace("__OCEAN_BGCLASS__", "has-img" if bg_uri else "")
    html = html.replace("__OCEAN_TIME__", gen_time)
    html = html.replace("__OCEAN_COUNT__", str(data.get("meta", {}).get("total", len(data.get("memories", [])))))

    if args.out:
        out_path = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        size_kb = os.path.getsize(out_path) / 1024.0
        print("已生成星空记忆海 -> %s (%.0f KB, %d 条记忆)" %
              (out_path, size_kb, len(data.get("memories", []))))
    else:
        sys.stdout.buffer.write(html.encode("utf-8"))


if __name__ == "__main__":
    main()
