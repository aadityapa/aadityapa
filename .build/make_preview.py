"""Produce a final-state preview copy of the hero SVGs for visual QA."""
import re

for theme in ("dark", "light"):
    src = open(f"assets/{theme}.svg", encoding="utf-8").read()
    s = re.sub(r'(?<!stop-)opacity="0"', 'opacity="1"', src)
    s = re.sub(r'(<clipPath id="tn"><rect[^>]*?width=)"0"', r'\1"800"', s)
    # Hide all role layers except one so the carousel doesn't stack in the still.
    roles = re.findall(r'<text[^>]*font-size="15" font-weight="600"[^>]*>.*?</text>', s)
    for i, r in enumerate(roles):
        if i != 2:
            s = s.replace(r, "")
    open(f".build/test_{theme}.svg", "w", encoding="utf-8").write(s)
    print(f"test_{theme}.svg written")
