#!/usr/bin/env python3
"""Full quality gate: SVG XML/compat checks, JSON parse, YAML parse, README path check."""
import xml.etree.ElementTree as ET
import re
import collections
import json
import os
import sys
import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
fail = 0


def check(label, ok, detail=""):
    global fail
    mark = "PASS" if ok else "FAIL"
    if not ok:
        fail += 1
    print(f"[{mark}] {label}" + (f" - {detail}" if detail else ""))


# --- SVGs ---
svg_files = sorted(glob.glob(os.path.join(ROOT, "assets", "*.svg"))) + [os.path.join(ROOT, "favicon.svg")]
for path in svg_files:
    f = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if not os.path.exists(path):
        check(f, False, "missing")
        continue
    src = open(path, encoding="utf-8").read()
    try:
        ET.fromstring(src)
        check(f"{f} well-formed XML", True)
    except ET.ParseError as e:
        check(f"{f} well-formed XML", False, str(e))
        continue
    banned = [b for b in ("<script", "<style", "foreignObject", "javascript:") if b in src]
    check(f"{f} no script/style/foreignObject", not banned, str(banned))
    ext = re.findall(r"https?://[^\"'\s>]+", src.replace("http://www.w3.org/2000/svg", ""))
    check(f"{f} no external refs", not ext, str(ext))
    ids = re.findall(r'id="([^"]+)"', src)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    check(f"{f} unique ids ({len(set(ids))})", not dup, str(dup))
    unresolved = sorted({r for r in re.findall(r"url\(#([^)]+)\)", src) if r not in ids}
                        | {r for r in re.findall(r'href="#([^"]+)"', src) if r not in ids})
    check(f"{f} all url(#)/href refs resolve", not unresolved, str(unresolved))
    check(f"{f} has title+desc", "<title" in src and "<desc" in src)
    n_anim = len(re.findall(r"<animate(?:Transform|Motion)?[\s>]", src))
    check(f"{f} SMIL-animated ({n_anim} animations)", n_anim > 0)
    size = os.path.getsize(path)
    check(f"{f} size {size/1024:.1f} KB < 150 KB", size < 150 * 1024)

# --- JSON ---
for f in glob.glob(os.path.join(ROOT, "*.json")) + glob.glob(os.path.join(ROOT, "data", "*.json")):
    rel = os.path.relpath(f, ROOT)
    try:
        json.load(open(f, encoding="utf-8"))
        check(f"{rel} valid JSON", True)
    except Exception as e:
        check(f"{rel} valid JSON", False, str(e))

# --- YAML workflows ---
try:
    import yaml
    for f in glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml")):
        rel = os.path.relpath(f, ROOT)
        try:
            data = yaml.safe_load(open(f, encoding="utf-8"))
            ok = isinstance(data, dict) and "jobs" in data
            check(f"{rel} valid workflow YAML", ok)
        except Exception as e:
            check(f"{rel} valid workflow YAML", False, str(e))
except ImportError:
    print("[WARN] pyyaml not installed; skipping YAML checks")

# --- README relative paths ---
readme = os.path.join(ROOT, "README.md")
if os.path.exists(readme):
    src = open(readme, encoding="utf-8").read()
    refs = re.findall(r'(?:src|href)="(\./[^"]+)"', src)
    refs += [m for m in re.findall(r"\]\((\./[^)]+)\)", src)]
    missing = []
    for r in sorted(set(refs)):
        p = os.path.join(ROOT, r.lstrip("./").replace("/", os.sep))
        if not os.path.exists(p):
            missing.append(r)
    check(f"README relative paths exist ({len(set(refs))} refs)", not missing, str(missing))

# --- sitemap XML ---
try:
    ET.parse(os.path.join(ROOT, "sitemap.xml"))
    check("sitemap.xml well-formed", True)
except Exception as e:
    check("sitemap.xml well-formed", False, str(e))

print()
print("RESULT:", "ALL CHECKS PASSED" if fail == 0 else f"{fail} FAILURES")
sys.exit(1 if fail else 0)
