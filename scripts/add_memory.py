#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_memory.py — 星空记忆海 · 记忆写入器

向工作区记忆海追加一条结构化记忆，写入
  <workspace>/.workbuddy/memory/ocean-notes.md
采集器 collect_memories.py 会自动读取该文件，星图随之更新。

用法：
  python add_memory.py --text "闯子偏好直接汇报，先给结论" --layer user --importance 5 --tags 偏好 汇报
  python add_memory.py --title "挥拳玩法" --text "小恶魔用挥拳击倒" --layer project --workspace D:/cam-run-dodge
  python add_memory.py --text "..." --date 2026-11-18 --tag 答辩 --tag Cam-Dodge

层级可选：soul user rules project topic fact lesson daily
"""

import argparse
import os
import sys
from datetime import datetime

VALID_LAYERS = {"soul", "user", "rules", "project", "topic", "fact", "lesson", "daily"}


def main():
    ap = argparse.ArgumentParser(description="星空记忆海 · 记忆写入器")
    ap.add_argument("--text", required=True, help="记忆正文")
    ap.add_argument("--title", default="", help="标题（可选，取正文前 24 字）")
    ap.add_argument("--layer", default="fact", help="层级: soul/user/rules/project/topic/fact/lesson/daily")
    ap.add_argument("--importance", type=int, default=3, help="重要性 1-5")
    ap.add_argument("--tags", nargs="*", default=[], help="标签列表（空格分隔）")
    ap.add_argument("--tag", action="append", default=[], help="单个标签，可重复")
    ap.add_argument("--project", default="", help="所属项目（可选）")
    ap.add_argument("--date", default="", help="日期 YYYY-MM-DD，默认今天")
    ap.add_argument("--workspace", default=".", help="项目根目录")
    args = ap.parse_args()

    layer = args.layer if args.layer in VALID_LAYERS else "fact"
    imp = max(1, min(5, args.importance))
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    tags = list(dict.fromkeys(args.tags + args.tag))
    title = (args.title or args.text[:24]).replace("\n", " ").strip()
    text = args.text.strip()

    memdir = os.path.join(os.path.abspath(args.workspace), ".workbuddy", "memory")
    os.makedirs(memdir, exist_ok=True)
    target = os.path.join(memdir, "ocean-notes.md")

    meta = " | 层级: %s | 重要性: %d | 日期: %s" % (layer, imp, date)
    if args.project:
        meta += " | 项目: %s" % args.project
    if tags:
        meta += " | 标签: %s" % " ".join("#" + t for t in tags)

    block = "\n## %s\n%s\n`%s`\n" % (title, text, meta.strip())

    existed = os.path.isfile(target)
    with open(target, "a", encoding="utf-8") as f:
        if not existed:
            f.write("# 星空记忆海 · 记忆流\n\n> 由 add_memory.py 写入，采集器自动读取。\n")
        f.write(block)

    print("已记录一条 %s 记忆 -> %s" % (layer, target.replace("\\", "/")))


if __name__ == "__main__":
    main()
