#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_memories.py — 星空记忆海 · 记忆采集器

把分散在 WorkBuddy 记忆体系里的 Markdown 文件，解析成统一的结构化 JSON，
供 render.py 渲染成星图。纯标准库实现，无第三方依赖。

采集来源（存在才读，不存在自动跳过）：
  用户级：
    ~/.workbuddy/MEMORY.md          长期规则        -> rules
    ~/.workbuddy/SOUL.md            人格/灵魂        -> soul
    ~/.workbuddy/IDENTITY.md        身份            -> soul
    ~/.workbuddy/USER.md            用户画像        -> user
  项目级（--workspace 指定，默认当前目录）：
    <ws>/.workbuddy/memory/MEMORY.md                -> project
    <ws>/.workbuddy/memory/YYYY-MM-DD.md            -> daily
    <ws>/.workbuddy/memory/*.md (其它)              -> topic

用法：
  python collect_memories.py --workspace "D:/cam-run-dodge" --out memories.json
  python collect_memories.py --workspace . --include-user --out memories.json

输出 JSON 结构：
{
  "meta": {"generated_at": "...", "sources": [...], "title": "..."},
  "memories": [
    {"id": "...", "title": "...", "content": "...", "layer": "soul",
     "source": "...", "date": "2026-09-28", "importance": 4,
     "tags": [...], "project": "cam-run-dodge"}
  ]
}
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime

# 层级 -> 元数据（渲染端会用到颜色/轨道，这里只给 key 和中文名）
LAYER_NAMES = {
    "soul": "灵魂/人格",
    "user": "用户画像",
    "rules": "长期规则",
    "project": "项目知识",
    "topic": "主题",
    "fact": "事实",
    "lesson": "经验教训",
    "daily": "日常日志",
}

DATE_RE = re.compile(r"(20\d{2})[-/年.](\d{1,2})[-/月.](\d{1,2})")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
NUM_RE = re.compile(r"^\s*\d+[.)]\s+(.*)$")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
CODE_RE = re.compile(r"`([^`]+)`")

IMPORTANT_WORDS = ("重要", "必须", "关键", "务必", "禁止", "默认", "长期", "永远", "CRITICAL", "MUST", "ALWAYS")


def _stable_id(text, source):
    raw = (source + "||" + text).encode("utf-8", errors="ignore")
    return "m" + hashlib.md5(raw).hexdigest()[:10]


def _norm_date(*candidates):
    for c in candidates:
        if not c:
            continue
        m = DATE_RE.search(str(c))
        if m:
            y, mo, d = m.groups()
            return "%04d-%02d-%02d" % (int(y), int(mo), int(d))
    return ""


def _extract_tags(text):
    tags = set()
    for m in LINK_RE.finditer(text):
        tags.add(m.group(1).strip())
    for m in CODE_RE.finditer(text):
        t = m.group(1).strip()
        if 1 < len(t) <= 24 and " " not in t:
            tags.add(t)
    return sorted(tags)[:8]


def _clean(text):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # markdown link/img
    text = LINK_RE.sub(r"\1", text)
    text = BOLD_RE.sub(r"\1", text)
    text = CODE_RE.sub(r"\1", text)
    text = re.sub(r"[*_~`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _importance(text, layer):
    base = {"soul": 5, "user": 4, "rules": 5, "project": 4,
            "topic": 3, "fact": 3, "lesson": 4, "daily": 2}.get(layer, 3)
    hit = sum(1 for w in IMPORTANT_WORDS if w.lower() in text.lower())
    return max(1, min(5, base + (1 if hit >= 2 else 0) - (1 if layer == "daily" and len(text) < 20 else 0)))


def _layer_for_file(path, ws):
    name = os.path.basename(path).lower()
    stem = name.replace(".md", "")
    if stem == "soul":
        return "soul"
    if stem == "identity":
        return "soul"
    if stem == "user":
        return "user"
    if stem == "memory" and ".workbuddy" in path.replace("\\", "/"):
        parent = os.path.basename(os.path.dirname(path)).lower()
        if parent == "memory":
            # 项目级 MEMORY.md vs 用户级：路径里含 workspace 即项目级
            norm_ws = os.path.abspath(ws).replace("\\", "/").lower()
            norm_p = os.path.abspath(path).replace("\\", "/").lower()
            return "project" if norm_p.startswith(norm_ws) else "rules"
        return "rules"
    if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", stem):
        return "daily"
    if "lesson" in stem or "经验" in stem:
        return "lesson"
    if "fact" in stem or "事实" in stem:
        return "fact"
    return "topic"


def parse_file(path, ws, project_name):
    """把一个 Markdown 文件解析成记忆条目列表。"""
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()
    except Exception:
        return []

    layer = _layer_for_file(path, ws)
    file_date = _norm_date(os.path.basename(path))
    project = project_name

    blocks = []  # (section_title, [text lines])
    cur_title = ""
    buf = []
    for line in lines:
        hm = HEAD_RE.match(line)
        if hm:
            if buf:
                blocks.append((cur_title, buf))
                buf = []
            cur_title = _clean(hm.group(2))
            continue
        if not line.strip():
            if buf:
                blocks.append((cur_title, buf))
                buf = []
            continue
        buf.append(line)
    if buf:
        blocks.append((cur_title, buf))

    out = []
    for section, body in blocks:
        # 每个 bullet / 编号项 / 独立段落成为一条记忆
        items = []
        para = []
        for line in body:
            bm = BULLET_RE.match(line) or NUM_RE.match(line)
            if bm:
                if para:
                    items.append(" ".join(para)); para = []
                items.append(bm.group(1))
            else:
                para.append(line.strip())
        if para:
            items.append(" ".join(para))

        for raw in items:
            cleaned = _clean(raw)
            if not cleaned or len(cleaned) < 2:
                continue
            # 跳过纯分隔线/纯符号
            if not re.search(r"[\w\u4e00-\u9fff]", cleaned):
                continue
            title = section if section and len(section) <= 40 else (cleaned[:28] + ("…" if len(cleaned) > 28 else ""))
            content = cleaned if not (section and section in cleaned) else cleaned
            date = _norm_date(raw, section) or file_date
            out.append({
                "id": _stable_id(section + "||" + content, path),
                "title": _clean(title) or "未命名记忆",
                "content": content,
                "layer": layer,
                "source": os.path.abspath(path).replace("\\", "/"),
                "date": date,
                "importance": _importance(content, layer),
                "tags": _extract_tags(raw),
                "project": project,
            })
    return out


def collect(workspace, include_user):
    workspace = os.path.abspath(workspace)
    project_name = os.path.basename(workspace.rstrip("/\\")) or "workspace"
    home = os.path.expanduser("~")
    sources = []
    memories = []

    candidates = []
    if include_user:
        candidates += [
            (os.path.join(home, ".workbuddy", "SOUL.md"), "user"),
            (os.path.join(home, ".workbuddy", "IDENTITY.md"), "user"),
            (os.path.join(home, ".workbuddy", "USER.md"), "user"),
            (os.path.join(home, ".workbuddy", "MEMORY.md"), "user"),
        ]
    memdir = os.path.join(workspace, ".workbuddy", "memory")
    if os.path.isdir(memdir):
        for fn in sorted(os.listdir(memdir)):
            if fn.lower().endswith(".md"):
                candidates.append((os.path.join(memdir, fn), "project"))

    seen = set()
    for path, scope in candidates:
        ap = os.path.abspath(path)
        if ap in seen or not os.path.isfile(ap):
            continue
        seen.add(ap)
        got = parse_file(path, workspace, project_name)
        if got:
            sources.append({"path": ap.replace("\\", "/"), "scope": scope, "count": len(got)})
            memories.extend(got)

    # 去重（内容相同）
    dedup = {}
    for m in memories:
        key = (m["layer"], m["content"][:80])
        if key not in dedup:
            dedup[key] = m
    memories = sorted(dedup.values(), key=lambda m: (-m["importance"], m["date"] or "9999"))

    return {
        "meta": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "workspace": workspace.replace("\\", "/"),
            "project": project_name,
            "sources": sources,
            "total": len(memories),
        },
        "memories": memories,
    }


def main():
    ap = argparse.ArgumentParser(description="星空记忆海 · 记忆采集器")
    ap.add_argument("--workspace", default=".", help="项目根目录（含 .workbuddy/memory）")
    ap.add_argument("--include-user", action="store_true", help="同时采集用户级 SOUL/IDENTITY/USER/MEMORY")
    ap.add_argument("--out", default="", help="输出 JSON 文件；留空则打印到 stdout")
    args = ap.parse_args()

    data = collect(args.workspace, args.include_user)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        out_path = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("已采集 %d 条记忆 -> %s" % (data["meta"]["total"], out_path))
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    main()
