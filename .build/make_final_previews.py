"""Render docs/previews/{dark,light}-preview.png at 2x from the shipped SVGs,
paused at t=10.5s (intro finished, role carousel mid-slot)."""
import os
import subprocess

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
T = 10.5

for theme in ("dark", "light"):
    svg = open(f"assets/{theme}.svg", encoding="utf-8").read()
    bg = "#0d1117" if theme == "dark" else "#ffffff"
    html = (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>body{{margin:0;background:{bg}}}svg{{display:block;width:1180px;height:610px}}</style></head><body>'
            f'{svg}<script>const s=document.querySelector("svg");'
            f's.setCurrentTime({T});s.pauseAnimations();</script></body></html>')
    hp = os.path.abspath(f".build/render_tmp/preview_{theme}.html")
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    open(hp, "w", encoding="utf-8").write(html)
    png = os.path.abspath(f"docs/previews/{theme}-preview.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                    "--window-size=1180,610", "--force-device-scale-factor=1",
                    "--hide-scrollbars", f"--screenshot={png}", f"file:///{hp}"],
                   check=True, capture_output=True, timeout=60)
    print(png, os.path.getsize(png))

# recompress
from PIL import Image
for theme in ("dark", "light"):
    p = f"docs/previews/{theme}-preview.png"
    im = Image.open(p)
    im.save(p, optimize=True)
    print("optimized", p, os.path.getsize(p), im.size)
