#!/usr/bin/env python3
"""Convert Aaditya's portrait photo into the ASCII grid used by the hero SVGs.

Primary source: assets/source-portrait.png (professional three-quarter portrait).
The pipeline preserves pose asymmetry (quiff sweep, beard contour, glasses band),
applies histogram equalization / gamma / unsharp within a subject mask, and maps
luminance onto a multi-level density ramp. Output: ascii_face.py + QA PNGs.

Tunables live in CONFIG for quick visual iteration.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# SVG-safe density ramp (no & — escaped separately; < > " handled by generate_svgs esc())
RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

CONFIG = {
  # versioned portrait (copied from user-attached screenshot)
  "src": os.path.join(ROOT, "assets", "source-portrait.png"),
  # head-and-shoulders crop (left, top, right, bottom) in source pixels
  "crop": (55, 15, 580, 565),
  # character grid — sized for hero left panel (font 10.5 / lh 13, ~372px inner width)
  "cols": 56,
  "rows": 29,
  # monospace cell aspect (advance / line-height) from generate_svgs.py metrics
  "cell_aspect": 0.486,
  # background luminance threshold (portrait has warm gray studio bg)
  "bg_lum": 200,
  # CLAHE-style equalization clip limit (percent)
  "eq_clip": 2.5,
  # gamma < 1 lifts midtones (skin/glasses); > 1 deepens shadows
  "gamma": 0.85,
  # unsharp mask (radius, percent, threshold)
  "unsharp": (2, 180, 1),
  # local contrast boost after equalization (1.0 = none)
  "contrast": 1.22,
  # edge emphasis blend (0–1) to keep glasses/beard at grid scale
  "edge_blend": 0.35,
  # floor for dark subject pixels (hair/beard silhouette)
  "shadow_floor": 78,
  "hair_level": 88,
  "suit_level": 52,
  # crop-space row fraction where blazer/turtleneck dominates (0–1)
  "suit_frac": 0.77,
  "ramp": RAMP,
}


def _bg_mask(rgb: Image.Image, lum_thresh: float) -> Image.Image:
    """Build subject mask from luminance + corner flood (warm gray studio bg)."""
    arr = rgb.load()
    w, h = rgb.size
    lum = rgb.convert("L")
    lp = lum.load()
    # seed background from corners / top edge
    bg = set()
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    for x in range(0, w, 8):
        seeds.append((x, 0))
        seeds.append((x, h - 1))
    for y in range(0, h, 8):
        seeds.append((0, y))
        seeds.append((w - 1, y))
    stack = [s for s in seeds if lp[s[0], s[1]] >= lum_thresh]
    while stack:
        x, y = stack.pop()
        if (x, y) in bg:
            continue
        if lp[x, y] < lum_thresh:
            continue
        bg.add((x, y))
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in bg:
                if lp[nx, ny] >= lum_thresh - 6:
                    stack.append((nx, ny))
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for x, y in bg:
        mp[x, y] = 0
    for y in range(h):
        for x in range(w):
            if (x, y) not in bg:
                mp[x, y] = 255
    # soften mask edge slightly
    return mask.filter(ImageFilter.GaussianBlur(1.2))


def photo_to_grid(cfg=CONFIG):
    im = Image.open(cfg["src"]).convert("RGB")
    im = im.crop(cfg["crop"])
    w, h = im.size

    mask = _bg_mask(im, cfg["bg_lum"])
    lum = im.convert("L")

    # histogram equalization within subject
    lum = ImageOps.equalize(lum, mask=mask.point(lambda a: 255 if a > 64 else 0))
    lum = ImageOps.autocontrast(lum, cutoff=cfg["eq_clip"], mask=mask)

    # gamma
    g = cfg["gamma"]
    lut = [min(255, round(255 * (i / 255) ** g)) for i in range(256)]
    lum = lum.point(lut)

    # contrast stretch on subject
    c = cfg["contrast"]
    if c != 1.0:
        lum = lum.point(lambda v: min(255, max(0, round(128 + (v - 128) * c))))

    # unsharp + edge blend for glasses / beard boundaries
    r, pct, thr = cfg["unsharp"]
    sharp = lum.filter(ImageFilter.UnsharpMask(radius=r, percent=pct, threshold=thr))
    edges = lum.filter(ImageFilter.FIND_EDGES).point(lambda v: min(255, v * 2))
    eb = cfg["edge_blend"]
    lp, sp, ep, mp = lum.load(), sharp.load(), edges.load(), mask.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y] < 64:
                lp[x, y] = 0
                continue
            v = int(sp[x, y] * (1 - eb) + min(255, sp[x, y] + ep[x, y] * 0.35) * eb)
            lp[x, y] = v

    # silhouette floors: hair/beard core + blazer block (position-based suit split)
    floor = cfg["shadow_floor"]
    hair, suit = cfg["hair_level"], cfg["suit_level"]
    suit_y = int(h * cfg["suit_frac"])
    for y in range(h):
        for x in range(w):
            if mp[x, y] < 64:
                lp[x, y] = 0
                continue
            v = lp[x, y]
            if y >= suit_y and v < 130:
                lp[x, y] = suit
            elif v < floor:
                lp[x, y] = hair
            elif v < floor + 40:
                # transition band — keeps beard contour readable
                t = (v - floor) / 40
                lp[x, y] = int(hair + t * (v - hair))

    # resample to monospace grid (account for tall cells)
    cols, rows = cfg["cols"], cfg["rows"]
    aspect = cols * cfg["cell_aspect"] / rows
    # fit crop into grid aspect by center-crop if needed
    cur_aspect = w / h
    if cur_aspect > aspect:
        # too wide — trim sides (preserve three-quarter offset: keep slightly more left for quiff)
        new_w = int(h * aspect)
        left = int((w - new_w) * 0.42)  # bias toward viewer-left (quiff side)
        im_box = (left, 0, left + new_w, h)
        lum = lum.crop(im_box)
        mask = mask.crop(im_box)
    elif cur_aspect < aspect:
        new_h = int(w / aspect)
        top = max(0, (h - new_h) // 3)  # keep more headroom for quiff
        lum = lum.crop((0, top, w, top + new_h))
        mask = mask.crop((0, top, w, top + new_h))

    # apply mask one more time after aspect crop
    lp2, mp2 = lum.load(), mask.load()
    lw, lh = lum.size
    for y in range(lh):
        for x in range(lw):
            if mp2[x, y] < 64:
                lp2[x, y] = 0

    grid = lum.resize((cols, rows), Image.LANCZOS)
    ramp = cfg["ramp"]
    n = len(ramp)
    px = grid.load()
    lines = []
    for y in range(rows):
        lines.append("".join(ramp[min(px[x, y] * n // 256, n - 1)] for x in range(cols)))
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    # uniform width for SVG text-anchor=middle centering
    cols = cfg["cols"]
    lines = [ln.ljust(cols)[:cols] for ln in lines]
    return lines


def render_preview(lines, out_png, scale=3, fg="#22D3EE", bg="#030712"):
    """Render ASCII grid to PNG with monospace metrics close to the SVG."""
    cw, lh = int(6.32 * scale), int(13 * scale)
    img = Image.new("RGB", (max(len(l) for l in lines) * cw + 20, len(lines) * lh + 20), bg)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("consola.ttf", int(10.5 * scale))
    except OSError:
        try:
            font = ImageFont.truetype("CascadiaMono.ttf", int(10.5 * scale))
        except OSError:
            font = ImageFont.load_default()
    for i, line in enumerate(lines):
        d.text((10, 10 + i * lh), line, fill=fg, font=font)
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    img.save(out_png)


def side_by_side(cfg, lines, preview_png, out_png):
    src = Image.open(cfg["src"]).convert("RGB").crop(cfg["crop"])
    asc = Image.open(preview_png)
    # match heights
    nh = asc.height
    nw = round(src.width * nh / src.height)
    src = src.resize((nw, nh), Image.LANCZOS)
    combo = Image.new("RGB", (nw + asc.width + 16, nh), "#030712")
    combo.paste(src, (0, 0))
    combo.paste(asc, (nw + 16, 0))
    d = ImageDraw.Draw(combo)
    d.text((8, 4), "source crop", fill="#64748B")
    d.text((nw + 24, 4), "ASCII render", fill="#64748B")
    combo.save(out_png)


def write_ascii_face(lines, out_py):
    with open(out_py, "w", encoding="utf-8", newline="\n") as f:
        f.write('"""ASCII portrait of Aaditya Padiya generated by photo_to_ascii.py '
                'from assets/source-portrait.png. Regenerate with that script; do not hand-edit."""\n')
        f.write("ASCII_FACE = [\n")
        for line in lines:
            f.write(f"    {line!r},\n")
        f.write("]\n")


def main():
    cfg = CONFIG
    photo_dir = os.path.join(HERE, "photo")
    os.makedirs(photo_dir, exist_ok=True)
    lines = photo_to_grid(cfg)
    out_py = os.path.join(HERE, "ascii_face.py")
    write_ascii_face(lines, out_py)
    preview = os.path.join(photo_dir, "ascii_preview.png")
    render_preview(lines, preview)
    side = os.path.join(photo_dir, "ascii_side_by_side_v2.png")
    side_by_side(cfg, lines, preview, side)
    cols = max(len(l) for l in lines)
    print(f"wrote {out_py}: {len(lines)} rows x {cols} cols")
    print(f"wrote {preview}")
    print(f"wrote {side}")
    return lines


if __name__ == "__main__":
    main()
