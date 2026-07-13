#!/usr/bin/env python3
"""Convert Aaditya's real portrait photo into the ASCII grid used by the hero SVGs.

Source photo: the portfolio site portrait (Port/Portfolio/public/images/aaditya-photo.png,
full-body on transparent background). We crop to head & shoulders, normalize contrast,
resample onto a monospace character grid, and map brightness onto a multi-level density
ramp. The output is written as a Python list literal (ascii_face.py) which
generate_svgs.py imports, plus a rendered PNG for side-by-side visual QA.

Tunables live in CONFIG so the crop/gamma/ramp can be iterated quickly.
"""
import os

from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # source photo (408x612 RGBA, subject on transparent bg)
    "src": r"C:\Users\IT.Pune\Desktop\Port\Portfolio\public\images\aaditya-photo.png",
    # head-and-shoulders crop box (left, top, right, bottom) in source pixels
    "crop": (155, 104, 275, 234),
    # character grid — sized for the hero left panel (~372px inner width)
    "cols": 56,
    "rows": 29,
    # font cell aspect (advance width / line height) of the SVG monospace metrics
    # (10.5px mono advance 6.32px / 13px line height)
    "cell_aspect": 0.486,
    # gamma < 1 brightens midtones (face detail), > 1 darkens
    "gamma": 1.06,
    # unsharp mask (radius, percent) to keep glasses/eyes/beard edges at grid scale
    "unsharp": (3, 130),
    # subject pixels darker than this are flattened to the floor level, which
    # removes suit-fabric texture noise and leaves a clean silhouette
    "shadow_flatten": 92,
    # dark-to-bright density ramp (no & < > " chars — SVG text safe)
    "ramp": " .':;li!~+xomXOM@",
    # autocontrast clip percentages (low, high)
    "clip": (2, 2),
    # brightness assigned to dark subject cores: hair/beard vs suit (below neckline)
    "hair_level": 82,
    "suit_level": 44,
    # crop-space row where the suit/collar region starts (position-based split,
    # since hair and suit are both near-black in luminance)
    "suit_row": 100,
}


def photo_to_grid(cfg=CONFIG):
    im = Image.open(cfg["src"]).convert("RGBA")
    im = im.crop(cfg["crop"])
    # erode the subject mask slightly so unsharp halos at the crop boundary
    # don't produce stray bright characters along the silhouette edge
    alpha = im.getchannel("A").filter(ImageFilter.MinFilter(5))
    lum = im.convert("L")
    # contrast-normalize luminance within the subject only
    lum = ImageOps.autocontrast(lum, cutoff=cfg["clip"], mask=alpha.point(lambda a: 255 if a > 128 else 0))
    # gamma correction for midtone detail
    lut = [round(255 * (i / 255) ** cfg["gamma"]) for i in range(256)]
    lum = lum.point(lut)
    # edge emphasis so glasses/eyes/beard boundaries survive the tiny grid
    r, pct = cfg["unsharp"]
    lum = lum.filter(ImageFilter.UnsharpMask(radius=r, percent=pct, threshold=2))
    # subject silhouette floor: dark hair/suit must stay visible against the
    # empty background, so subject pixels never fall below `floor`
    flat = cfg["shadow_flatten"]
    hair, suit = cfg["hair_level"], cfg["suit_level"]
    suit_row = cfg["suit_row"]
    lp, ap = lum.load(), alpha.load()
    w, h = lum.size
    for y in range(h):
        for x in range(w):
            if ap[x, y] <= 128:
                lp[x, y] = 0  # background -> space
                continue
            v = lp[x, y]
            if y >= suit_row and v < 120:
                lp[x, y] = suit  # uniform suit/collar silhouette
            elif v < flat:
                lp[x, y] = hair  # solid hair/beard core
            else:
                lp[x, y] = hair + (v - flat) * (255 - hair) // (255 - flat)
    # resample to grid (BOX = clean area average, no ringing halos)
    im = lum.resize((cfg["cols"], cfg["rows"]), Image.BOX)
    ramp = cfg["ramp"]
    n = len(ramp)
    px = im.load()
    lines = []
    for y in range(cfg["rows"]):
        # keep uniform width: the SVG centers each line (text-anchor=middle),
        # so all rows must have identical advance width to stay grid-aligned
        lines.append("".join(ramp[min(px[x, y] * n // 256, n - 1)] for x in range(cfg["cols"])))
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def render_preview(lines, out_png, scale=2):
    """Render the ASCII grid to a PNG (fixed-width font) for visual comparison."""
    cw, lh = 8 * scale, 16 * scale
    img = Image.new("RGB", (max(len(l) for l in lines) * cw + 20, len(lines) * lh + 20), "#030712")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("consola.ttf", 13 * scale)
    except OSError:
        font = ImageFont.load_default()
    for i, line in enumerate(lines):
        d.text((10, 10 + i * lh), line, fill="#22D3EE", font=font)
    img.save(out_png)


def main():
    lines = photo_to_grid()
    out_py = os.path.join(HERE, "ascii_face.py")
    with open(out_py, "w", encoding="utf-8", newline="\n") as f:
        f.write('"""ASCII portrait of Aaditya Padiya generated by photo_to_ascii.py '
                'from the real portfolio photo. Regenerate with that script; do not hand-edit."""\n')
        f.write("ASCII_FACE = [\n")
        for line in lines:
            f.write(f"    {line!r},\n")
        f.write("]\n")
    print(f"wrote {out_py}: {len(lines)} rows x {max(len(l) for l in lines)} cols")
    render_preview(lines, os.path.join(HERE, "photo", "ascii_preview.png"))
    # side-by-side: source crop next to ascii render
    src = Image.open(CONFIG["src"]).convert("RGBA").crop(CONFIG["crop"])
    bgc = Image.new("RGBA", src.size, (3, 7, 18, 255))
    src = Image.alpha_composite(bgc, src).convert("RGB")
    asc = Image.open(os.path.join(HERE, "photo", "ascii_preview.png"))
    src = src.resize((round(src.width * asc.height / src.height), asc.height), Image.LANCZOS)
    combo = Image.new("RGB", (src.width + asc.width + 10, asc.height), "#030712")
    combo.paste(src, (0, 0))
    combo.paste(asc, (src.width + 10, 0))
    combo.save(os.path.join(HERE, "photo", "ascii_side_by_side.png"))
    print("wrote photo/ascii_preview.png and photo/ascii_side_by_side.png")


if __name__ == "__main__":
    main()
