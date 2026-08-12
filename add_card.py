"""
Add a new card to writing-cards/data.json.

Usage (modify CARD, then run):
    python3 add_card.py

Script:
1. Reads data.json
2. Appends card with auto-assigned id
3. Sorts by id, writes back with indent
4. Optionally git commit + push
"""

CARD = {
    "type": "名言",          # 名言 | 诗词 | 知识 | 文案 | 其他
    "title": "",             # 可选标题
    "content": "卡片正文内容",
    "source": "出处/作者",
    "tags": ["标签1", "标签2"],
    "gradient": 1,           # 1-12 渐变方案
    "createdAt": "2026-08-12"
}

import json
import subprocess
import sys
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data.json"
PUSH = "--push" in sys.argv


def main():
    cards = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    next_id = max(int(c["id"]) for c in cards) + 1

    card = dict(CARD, id=next_id)
    cards.append(card)
    cards.sort(key=lambda c: int(c["id"]))

    DATA_PATH.write_text(
        json.dumps(cards, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Added card [{next_id}]: {CARD.get('title') or CARD.get('content', '')[:30]}...")
    print(f"Total: {len(cards)} cards")

    if PUSH:
        name = CARD.get("title") or CARD.get("content", "")[:20]
        for cmd in [
            ["git", "add", "data.json"],
            ["git", "commit", "-m", f"新增卡片: {name}"],
            ["git", "push"],
        ]:
            r = subprocess.run(cmd, cwd=DATA_PATH.parent, env={
                **__import__("os").environ,
                "GIT_SSL_NO_VERIFY": "1",
            })
            if r.returncode != 0:
                print(f"Command failed: {' '.join(cmd)}")
                sys.exit(1)
        print("Pushed to GitHub.")


if __name__ == "__main__":
    main()
