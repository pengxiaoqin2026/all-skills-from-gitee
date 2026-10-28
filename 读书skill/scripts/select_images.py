import argparse
import os
import random
import shutil
import sys
from pathlib import Path


for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


OUT = r"E:\codex_one"
RECORD = os.path.join(OUT, "选图使用记录.txt")
HISTORY = 4  # 最近 4 个视频用过的图不再重复使用
NAMES = ["片头.png", "正文1段.png", "正文2段.png", "正文3段.png", "正文4段.png"]
EXT = {".png", ".jpg", ".jpeg", ".webp"}


def load_history(path):
    """读取使用记录，返回最近 HISTORY 行（每行是图片标识列表，旧→新）。"""
    records = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                items = [x.strip() for x in line.split("|") if x.strip()]
                records.append(items)
    return records[-HISTORY:]


def main():
    ap = argparse.ArgumentParser(
        description="读书skill正片随机选图：同一视频内不重复，且最近4个视频用过的图不重复"
    )
    ap.add_argument("style_dir", help="风格素材目录，如 E:\\素材库\\电影感")
    ap.add_argument("--out", default=OUT, help="输出目录（默认 E:\\codex_one）")
    ap.add_argument("--record", default=RECORD, help="使用记录文件（默认 E:\\codex_one\\选图使用记录.txt）")
    ap.add_argument("--seed", type=int, default=None, help="随机种子，固定后结果可复现")
    ap.add_argument("--dry-run", action="store_true", help="只预览选中结果，不复制文件、不写记录")
    args = ap.parse_args()

    style = Path(args.style_dir)
    if not style.is_dir():
        sys.exit(f"[错误] 素材目录不存在：{style}")

    keys = sorted(
        f"{style.name}{os.sep}{p.name}"
        for p in style.iterdir()
        if p.is_file() and p.suffix.lower() in EXT
    )
    if len(keys) < 5:
        sys.exit(
            f"[错误] 候选图片不足 5 张（当前 {len(keys)}），无法保证本视频内不重复，请补充素材：{style}"
        )

    recent = load_history(args.record)
    used = {key for rec in recent for key in rec}
    pool = [key for key in keys if key not in used]

    if len(pool) < 5:
        order = []
        for rec in reversed(recent):
            for key in rec:
                if key not in order:
                    order.append(key)
        lru = list(reversed(order))  # 越久没用越靠前
        extra = [key for key in lru if key not in pool][: 5 - len(pool)]
        print(
            f"[警告] 排除最近 {len(recent)} 个视频用图后可用池仅 {len(pool)} 张，"
            f"按最久未使用优先放宽复用 {len(extra)} 张：{extra}"
        )
        pool += extra

    rng = random.Random(args.seed)
    chosen = rng.sample(pool, 5)
    assert len(chosen) == len(set(chosen)) == 5

    print("本轮随机选中：")
    for idx, (key, dst) in enumerate(zip(chosen, NAMES), 1):
        print(f"  {idx}. {key}  ->  {dst}")

    if args.dry_run:
        print("[dry-run] 未复制文件、未写记录。记录将保留最近", HISTORY, "行。")
        return

    for key, dst in zip(chosen, NAMES):
        filename = key.split(os.sep, 1)[1]
        shutil.copy2(style / filename, os.path.join(args.out, dst))

    records = (recent + [chosen])[-HISTORY:]
    os.makedirs(os.path.dirname(args.record), exist_ok=True)
    with open(args.record, "w", encoding="utf-8") as f:
        for rec in records:
            f.write("|".join(rec) + "\n")
    print(f"已复制并重命名到 {args.out}，使用记录已更新：{args.record}")


if __name__ == "__main__":
    main()
