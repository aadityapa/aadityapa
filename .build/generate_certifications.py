#!/usr/bin/env python3
"""Generator for assets/certifications-dark.svg and assets/certifications-light.svg.

Aaditya Padiya — Certifications: four glass badge cards with rotating-gradient
medallions, glyphs, VERIFIED pills and shimmer sweeps. Sibling of
generate_svgs.py. SMIL only, README-safe.
"""
import os

W, H = 1180, 360

THEMES = {
    "dark": {
        "bg": "#030712", "panel": "#0F172A", "panel2": "#111C33",
        "text": "#F8FAFC", "sub": "#94A3B8", "muted": "#64748B",
        "border": "#1E293B",
        "a1": "#7C3AED", "a2": "#22D3EE", "a3": "#10B981",
        "a2text": "#22D3EE", "a3text": "#10B981",
        "glassline": "#FFFFFF", "aurora_op": "0.55",
        "pill_fill": "#0B1526", "glow_op": "0.9", "shimmer_op": "0.07",
        "desc": "dark",
    },
    "light": {
        "bg": "#FFFFFF", "panel": "#F8FAFC", "panel2": "#F1F5F9",
        "text": "#0F172A", "sub": "#475569", "muted": "#64748B",
        "border": "#E2E8F0",
        "a1": "#2563EB", "a2": "#06B6D4", "a3": "#10B981",
        "a2text": "#0E7490", "a3text": "#047857",
        "glassline": "#0F172A", "aurora_op": "0.22",
        "pill_fill": "#FFFFFF", "glow_op": "0.5", "shimmer_op": "0.05",
        "desc": "light",
    },
}

MONO = "ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"

CARD_W, CARD_H, GAP = 262, 250, 24
MARGIN_X = (W - 4 * CARD_W - 3 * GAP) / 2  # 30
CARD_Y = 82

# (name lines, issuer, year, glyph key)
CERTS = [
    (["Responsive Web", "Design"], "freeCodeCamp", None, "web"),
    (["Machine Learning", "with Python"], "freeCodeCamp", None, "ml"),
    (["MS-CIT"], "MKCL", "2016", "mon"),
    (["CCC"], "NIELIT", "2018", "kbd"),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs(t):
    a1, a2, a3 = t["a1"], t["a2"], t["a3"]
    parts = [f"""<defs>
<linearGradient id="ag" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/><stop offset="1" stop-color="{a3}"/>
</linearGradient>
<linearGradient id="mg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/><stop offset="1" stop-color="{a3}"/>
  <animateTransform attributeName="gradientTransform" type="rotate" values="0 0.5 0.5;360 0.5 0.5" dur="10s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="bs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.25" stop-color="{a2}"/>
  <stop offset="0.5" stop-color="{a3}"/><stop offset="0.75" stop-color="{a2}"/>
  <stop offset="1" stop-color="{a1}"/>
  <animateTransform attributeName="gradientTransform" type="rotate" from="0 {W//2} {H//2}" to="360 {W//2} {H//2}" dur="14s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0.35">
  <stop offset="0" stop-color="{t['glassline']}" stop-opacity="0"/>
  <stop offset="0.5" stop-color="{t['glassline']}" stop-opacity="{t['shimmer_op']}"/>
  <stop offset="1" stop-color="{t['glassline']}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="b1" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{a1}" stop-opacity="0.8"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="b2" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{a2}" stop-opacity="0.7"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{t['glassline']}" stop-opacity="0.10"/>
  <stop offset="0.18" stop-color="{t['glassline']}" stop-opacity="0.03"/>
  <stop offset="1" stop-color="{t['glassline']}" stop-opacity="0"/>
</linearGradient>
<filter id="fb" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="46"/>
</filter>
<filter id="fg" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="3.2" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="fs" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="9"/>
</filter>
<clipPath id="cv"><rect x="0" y="0" width="{W}" height="{H}" rx="24"/></clipPath>"""]
    for i in range(4):
        cx = MARGIN_X + i * (CARD_W + GAP)
        parts.append(f'<clipPath id="cc{i+1}"><rect x="{cx:.0f}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="14"/></clipPath>')
    parts.append("</defs>")
    return "".join(parts)


def background(t):
    p = []
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>')
    p.append(f'''<g clip-path="url(#cv)" opacity="{t['aurora_op']}">
<circle cx="200" cy="90" r="200" fill="url(#b1)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;110 60;30 -30;0 0" dur="27s" repeatCount="indefinite"/>
</circle>
<circle cx="980" cy="300" r="220" fill="url(#b2)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-130 -70;-30 40;0 0" dur="31s" repeatCount="indefinite"/>
</circle>
</g>''')
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="url(#gl)" clip-path="url(#cv)"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="1.6" opacity="0.9"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="3" opacity="0.22" filter="url(#fs)"/>')
    return "".join(p)


def header(t):
    return f'''<text x="30" y="46" font-family="{SANS}" font-size="20" font-weight="700" fill="{t['text']}">Certifications</text>
<text x="30" y="65" font-family="{MONO}" font-size="11" fill="{t['muted']}" xml:space="preserve">$ credentials --verified</text>
<text x="{W-30}" y="46" font-family="{MONO}" font-size="12" fill="{t['a2text']}" text-anchor="end" xml:space="preserve">4 credentials</text>'''


def glyph(t, key, mx, my):
    """Glyph drawn inside a medallion centred on (mx,my)."""
    if key == "web":
        return f'<text x="{mx:.0f}" y="{my+5:.0f}" font-family="{MONO}" font-size="15" font-weight="700" fill="{t["a2text"]}" text-anchor="middle" xml:space="preserve">&lt;/&gt;</text>'
    if key == "ml":
        # tiny neural net: 2-3-1 nodes with edges
        l = [(mx - 13, my - 8), (mx - 13, my + 8)]
        m = [(mx, my - 12), (mx, my), (mx, my + 12)]
        r = [(mx + 13, my)]
        e = []
        for a in l:
            for b in m:
                e.append(f'M{a[0]:.0f} {a[1]:.0f} L{b[0]:.0f} {b[1]:.0f}')
        for b in m:
            e.append(f'M{b[0]:.0f} {b[1]:.0f} L{r[0][0]:.0f} {r[0][1]:.0f}')
        dots = "".join(f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="2.6" fill="{t["a2text"]}"/>' for p in l + m + r)
        return f'<path d="{" ".join(e)}" stroke="{t["sub"]}" stroke-width="1" fill="none" opacity="0.85"/>{dots}'
    if key == "mon":
        return f'''<g stroke="{t['a2text']}" stroke-width="1.8" fill="none">
<rect x="{mx-14:.0f}" y="{my-12:.0f}" width="28" height="18" rx="2.5"/>
<path d="M{mx-6:.0f} {my+12:.0f} h12 M{mx:.0f} {my+6:.0f} v6"/>
</g>'''
    # kbd
    keys = "".join(
        f'<circle cx="{mx-9+k*6:.0f}" cy="{my-3:.0f}" r="1.1" fill="{t["a2text"]}"/>' for k in range(4)
    ) + "".join(
        f'<circle cx="{mx-9+k*6:.0f}" cy="{my+2:.0f}" r="1.1" fill="{t["a2text"]}"/>' for k in range(4)
    )
    return f'''<rect x="{mx-16:.0f}" y="{my-9:.0f}" width="32" height="20" rx="3" stroke="{t['a2text']}" stroke-width="1.8" fill="none"/>
{keys}<path d="M{mx-8:.0f} {my+7:.0f} h16" stroke="{t['a2text']}" stroke-width="1.4"/>'''


def card(t, i):
    name, issuer, year, gkey = CERTS[i]
    x = MARGIN_X + i * (CARD_W + GAP)
    y = CARD_Y
    ccx = x + CARD_W / 2
    begin = 0.25 + i * 0.18
    mx, my, mr = ccx, y + 62, 33
    p = [f'''<g opacity="0">
<animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>
<animateTransform attributeName="transform" type="scale" values="0.94;1" begin="{begin:.2f}s" dur="0.5s" fill="freeze" additive="sum"/>
<animateTransform attributeName="transform" type="translate" values="{ccx*0.06:.1f} {(y+CARD_H/2)*0.06:.1f};0 0" begin="{begin:.2f}s" dur="0.5s" fill="freeze" additive="sum"/>
<rect x="{x:.0f}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="14" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<rect x="{x:.0f}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="14" fill="url(#gl)"/>
<rect x="{x+14:.0f}" y="{y+1}" width="{CARD_W-80}" height="1" fill="{t['glassline']}" opacity="0.12"/>''']
    # Medallion: rotating-gradient ring + inner disc + glyph
    p.append(f'''<circle cx="{mx:.0f}" cy="{my}" r="{mr}" fill="none" stroke="url(#mg)" stroke-width="2.6" filter="url(#fg)" opacity="{t['glow_op']}"/>
<circle cx="{mx:.0f}" cy="{my}" r="{mr}" fill="none" stroke="url(#mg)" stroke-width="2.6"/>
<circle cx="{mx:.0f}" cy="{my}" r="{mr-7}" fill="{t['panel2']}" fill-opacity="0.9" stroke="{t['border']}" stroke-width="1"/>
{glyph(t, gkey, mx, my)}''')
    # Name (up to 2 lines), issuer, year
    ny = y + 128
    for ln in name:
        p.append(f'<text x="{ccx:.0f}" y="{ny}" font-family="{SANS}" font-size="14" font-weight="700" fill="{t["text"]}" text-anchor="middle">{esc(ln)}</text>')
        ny += 18
    iy = y + 172
    p.append(f'<text x="{ccx:.0f}" y="{iy}" font-family="{SANS}" font-size="11" fill="{t["sub"]}" text-anchor="middle">{esc(issuer)}</text>')
    if year:
        p.append(f'<text x="{ccx:.0f}" y="{iy+17}" font-family="{MONO}" font-size="10.5" fill="{t["a2text"]}" text-anchor="middle" xml:space="preserve">{year}</text>')
    # VERIFIED pill
    pw, ph = 86, 20
    px, py = ccx - pw / 2, y + CARD_H - 36
    p.append(f'''<rect x="{px:.0f}" y="{py}" width="{pw}" height="{ph}" rx="{ph/2}" fill="{t['pill_fill']}" fill-opacity="0.9" stroke="{t['a3']}" stroke-width="1" opacity="0.95"/>
<circle cx="{px+13:.0f}" cy="{py+ph/2}" r="2.6" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.25;1" dur="{1.8+i*0.3:.1f}s" repeatCount="indefinite"/>
</circle>
<text x="{px+22:.0f}" y="{py+13.5}" font-family="{MONO}" font-size="9" fill="{t['a3text']}" letter-spacing="1.2" xml:space="preserve">VERIFIED</text>''')
    # Shimmer sweep every ~7s
    p.append(f'''<g clip-path="url(#cc{i+1})"><rect x="{x-90:.0f}" y="{y-20}" width="70" height="{CARD_H+40}" fill="url(#sh)" transform="skewX(-18)">
  <animateTransform attributeName="transform" type="translate" values="0 0;{CARD_W+190} 0" dur="7s" begin="{1.5+i*0.8:.1f}s" repeatCount="indefinite" additive="sum"/>
</rect></g>''')
    p.append("</g>")
    return "".join(p)


def build(theme_key):
    t = THEMES[theme_key]
    title = "Aaditya Padiya — Certifications"
    desc = (f"Animated {t['desc']}-theme certification badges for Aaditya Padiya: Responsive Web Design "
            "(freeCodeCamp), Machine Learning with Python (freeCodeCamp), MS-CIT (MKCL, 2016) and "
            "CCC (NIELIT, 2018), each shown as a verified glass badge with an animated medallion.")
    cards = "".join(card(t, i) for i in range(4))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{defs(t)}
{background(t)}
{header(t)}
{cards}
</svg>'''


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for key in ("dark", "light"):
        out = os.path.join(root, "assets", f"certifications-{key}.svg")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(key))
        print(f"certifications-{key}.svg: {os.path.getsize(out)} bytes")
