#!/usr/bin/env python3
"""Generator for assets/ecosystem-dark.svg and assets/ecosystem-light.svg —
Aaditya Padiya technology-ecosystem orbit map.

GitHub-README-safe: SMIL animations only, no <script>/<style>/foreignObject,
no external refs, system font stacks only.
"""
import math
import os

W, H = 1180, 760
CX, CY = 590.0, 386.0
R_IN, R_OUT = 195.0, 310.0

THEMES = {
    "dark": {
        "bg": "#030712",
        "panel": "#0F172A",
        "panel2": "#111C33",
        "text": "#F8FAFC",
        "sub": "#94A3B8",
        "muted": "#64748B",
        "border": "#1E293B",
        "a1": "#7C3AED", "a2": "#22D3EE", "a3": "#10B981",
        "a2text": "#22D3EE", "a3text": "#10B981",
        "glassline": "#FFFFFF",
        "aurora_op": "0.55",
        "particle": "#22D3EE",
        "glow_op": "0.9",
        "pill_fill": "#0B1526",
        "desc": "dark",
    },
    "light": {
        "bg": "#FFFFFF",
        "panel": "#F8FAFC",
        "panel2": "#F1F5F9",
        "text": "#0F172A",
        "sub": "#475569",
        "muted": "#64748B",
        "border": "#E2E8F0",
        "a1": "#2563EB", "a2": "#06B6D4", "a3": "#10B981",
        "a2text": "#0E7490", "a3text": "#047857",
        "glassline": "#0F172A",
        "aurora_op": "0.22",
        "particle": "#2563EB",
        "glow_op": "0.5",
        "pill_fill": "#FFFFFF",
        "desc": "light",
    },
}

MONO = "ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"

INNER = ["Python", "AWS", "Docker", "Linux", "Git", "DevOps"]
OUTER = ["React", "Cloud", "Networking", "FastAPI", "Node", "Postgres", "Redis", "AI"]

IN_START, IN_STEP = -90.0, 60.0
OUT_START, OUT_STEP = -67.5, 45.0

# (inner index, outer index) pairs whose initial angles nearly line up.
CROSS_LINKS = [(0, 0), (1, 1), (3, 4), (4, 5)]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pos(r, deg):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def defs(t):
    a1, a2, a3 = t["a1"], t["a2"], t["a3"]
    return f"""<defs>
<linearGradient id="ag" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/><stop offset="1" stop-color="{a3}"/>
</linearGradient>
<linearGradient id="bs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.25" stop-color="{a2}"/>
  <stop offset="0.5" stop-color="{a3}"/><stop offset="0.75" stop-color="{a2}"/>
  <stop offset="1" stop-color="{a1}"/>
  <animateTransform attributeName="gradientTransform" type="rotate" from="0 {W//2} {H//2}" to="360 {W//2} {H//2}" dur="14s" repeatCount="indefinite"/>
</linearGradient>
<radialGradient id="b1" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{a1}" stop-opacity="0.8"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="b2" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{a2}" stop-opacity="0.7"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="b3" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{a3}" stop-opacity="0.6"/><stop offset="1" stop-color="{a3}" stop-opacity="0"/>
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
<clipPath id="cv"><rect x="0" y="0" width="{W}" height="{H}" rx="24"/></clipPath>
</defs>"""


def background(t):
    p = []
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>')
    # Aurora blobs (kept lighter than the hero — this sits mid-README)
    p.append(f'''<g clip-path="url(#cv)" opacity="{t['aurora_op']}">
<circle cx="170" cy="140" r="280" fill="url(#b1)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;120 80;30 -40;0 0" dur="28s" repeatCount="indefinite"/>
</circle>
<circle cx="1010" cy="600" r="300" fill="url(#b2)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-140 -90;-30 50;0 0" dur="33s" repeatCount="indefinite"/>
</circle>
<circle cx="900" cy="90" r="220" fill="url(#b3)" filter="url(#fb)" opacity="0.8">
  <animateTransform attributeName="transform" type="translate" values="0 0;-80 110;90 30;0 0" dur="25s" repeatCount="indefinite"/>
</circle>
</g>''')
    # Floating particles
    dots = []
    seeds = [(140, 560, 1.8, 17, "M0 0 C 30 -60, 90 -40, 60 -120"),
             (320, 110, 1.4, 21, "M0 0 C -40 50, 40 100, -20 150"),
             (1040, 300, 2.0, 18, "M0 0 C 40 -70, -40 -100, 30 -160"),
             (1100, 640, 1.5, 20, "M0 0 C -30 60, 40 110, -20 170"),
             (90, 320, 1.6, 19, "M0 0 C 40 60, -40 120, 30 180")]
    for cx, cy, r, dur, path in seeds:
        dots.append(f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t['particle']}" opacity="0.5" filter="url(#fg)">
  <animateMotion path="{path}" dur="{dur}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.15;0.55;0.15" dur="{dur/3:.1f}s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'<g clip-path="url(#cv)">{"".join(dots)}</g>')
    # Glass reflection across whole card
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="url(#gl)" clip-path="url(#cv)"/>')
    # Border shimmer
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="1.6" opacity="0.9"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="3" opacity="0.25" filter="url(#fs)"/>')
    return "".join(p)


def header(t):
    return f'''<text x="36" y="46" font-family="{MONO}" font-size="12.5" fill="{t['muted']}" xml:space="preserve">// tech.ecosystem --orbits 2 --nodes 14</text>
<circle cx="{W-40}" cy="42" r="4" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
</circle>
<text x="{W-56}" y="46" font-family="{MONO}" font-size="12" fill="{t['muted']}" text-anchor="end" xml:space="preserve">core + ecosystem</text>'''


def rings(t):
    return f'''<circle cx="{CX:.0f}" cy="{CY:.0f}" r="{R_IN:.0f}" fill="none" stroke="{t['border']}" stroke-width="1.2" stroke-dasharray="3 7" opacity="0.6"/>
<circle cx="{CX:.0f}" cy="{CY:.0f}" r="{R_OUT:.0f}" fill="none" stroke="{t['border']}" stroke-width="1.2" stroke-dasharray="3 7" opacity="0.6"/>'''


def spokes(t):
    p = ["<g>"]
    # Radial spokes centre -> inner ring, with travelling pulse dots.
    for i in range(len(INNER)):
        deg = IN_START + i * IN_STEP
        nx, ny = pos(R_IN, deg)
        p.append(f'<path d="M{CX:.0f} {CY:.0f} L{nx:.1f} {ny:.1f}" stroke="{t["border"]}" stroke-width="1" opacity="0.3"/>')
        beg = i * 0.55
        p.append(f'''<circle r="3" fill="{t['a2']}" filter="url(#fg)" opacity="0">
  <animateMotion path="M{CX:.0f} {CY:.0f} L{nx:.1f} {ny:.1f}" dur="3s" begin="{beg:.2f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.15;0.75;1" dur="3s" begin="{beg:.2f}s" repeatCount="indefinite"/>
</circle>''')
    # A few links between the rings, with slower outbound pulses.
    for k, (ii, oi) in enumerate(CROSS_LINKS):
        ideg = IN_START + ii * IN_STEP
        odeg = OUT_START + oi * OUT_STEP
        x1, y1 = pos(R_IN, ideg)
        x2, y2 = pos(R_OUT, odeg)
        p.append(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{t["a2"]}" stroke-width="1" opacity="0.22"/>')
        beg = 0.8 + k * 0.9
        p.append(f'''<circle r="2.6" fill="{t['a3']}" filter="url(#fg)" opacity="0">
  <animateMotion path="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" dur="4s" begin="{beg:.2f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.15;0.75;1" dur="4s" begin="{beg:.2f}s" repeatCount="indefinite"/>
</circle>''')
    p.append("</g>")
    return "".join(p)


def orbit_layer(t, names, radius, node_r, dur, clockwise, start_deg, step_deg):
    """Ring of glass nodes orbiting the centre. Each node's content is
    counter-rotated by an equal-and-opposite animateTransform so labels
    stay upright while orbiting."""
    to = 360 if clockwise else -360
    p = [f'''<g>
<animateTransform attributeName="transform" type="rotate" from="0 {CX:.0f} {CY:.0f}" to="{to} {CX:.0f} {CY:.0f}" dur="{dur}s" repeatCount="indefinite"/>''']
    for i, name in enumerate(names):
        deg = start_deg + i * step_deg
        nx, ny = pos(radius, deg)
        fs = 12 if len(name) <= 5 else (11 if len(name) <= 8 else 10)
        breathe = 3.6 + (i % 4) * 0.5
        p.append(f'''<g>
<animateTransform attributeName="transform" type="rotate" from="0 {nx:.1f} {ny:.1f}" to="{-to} {nx:.1f} {ny:.1f}" dur="{dur}s" repeatCount="indefinite"/>
<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r + 2.5}" fill="none" stroke="url(#ag)" stroke-width="2.5" opacity="0.3" filter="url(#fs)">
  <animate attributeName="opacity" values="0.15;0.5;0.15" dur="{breathe:.1f}s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/>
</circle>
<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r}" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r}" fill="url(#gl)"/>
<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{node_r}" fill="none" stroke="url(#ag)" stroke-width="1.2" opacity="0.85"/>
<text x="{nx:.1f}" y="{ny + 4:.1f}" font-family="{MONO}" font-size="{fs}" fill="{t['text']}" text-anchor="middle">{esc(name)}</text>
</g>''')
    p.append("</g>")
    return "".join(p)


def center_node(t):
    return f'''<g>
<circle cx="{CX:.0f}" cy="{CY:.0f}" r="92" fill="url(#b2)" opacity="0.3">
  <animate attributeName="opacity" values="0.18;0.42;0.18" dur="5s" repeatCount="indefinite"/>
</circle>
<circle cx="{CX:.0f}" cy="{CY:.0f}" r="76" fill="none" stroke="url(#ag)" stroke-width="2" opacity="0.7">
  <animate attributeName="r" values="76;96" dur="3.2s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.65;0" dur="3.2s" repeatCount="indefinite"/>
</circle>
<circle cx="{CX:.0f}" cy="{CY:.0f}" r="75" fill="{t['panel']}" fill-opacity="0.85" stroke="{t['border']}" stroke-width="1"/>
<circle cx="{CX:.0f}" cy="{CY:.0f}" r="75" fill="url(#gl)"/>
<circle cx="{CX:.0f}" cy="{CY:.0f}" r="75" fill="none" stroke="url(#ag)" stroke-width="1.6" opacity="0.9"/>
<text x="{CX:.0f}" y="{CY - 6:.0f}" font-family="{MONO}" font-size="16" font-weight="700" fill="{t['text']}" text-anchor="middle">Aaditya</text>
<text x="{CX:.0f}" y="{CY + 16:.0f}" font-family="{MONO}" font-size="16" font-weight="700" fill="{t['text']}" text-anchor="middle">Padiya</text>
</g>'''


def build(theme_key):
    t = THEMES[theme_key]
    title = "Aaditya Padiya — Technology Ecosystem"
    desc = (f"Animated {t['desc']}-theme orbit map of Aaditya Padiya's technology ecosystem: "
            "a central glass node with his name, an inner orbit of core skills (Python, AWS, "
            "Docker, Linux, Git, DevOps) and an outer orbit of ecosystem technologies (React, "
            "Cloud, Networking, FastAPI, Node, Postgres, Redis, AI), connected by pulsing "
            "energy lines.")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{defs(t)}
{background(t)}
{header(t)}
{rings(t)}
{spokes(t)}
{orbit_layer(t, INNER, R_IN, 34, 60, True, IN_START, IN_STEP)}
{orbit_layer(t, OUTER, R_OUT, 38, 90, False, OUT_START, OUT_STEP)}
{center_node(t)}
</svg>'''
    return svg


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for key in ("dark", "light"):
        out = os.path.join(root, "assets", f"ecosystem-{key}.svg")
        content = build(key)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"ecosystem-{key}.svg: {os.path.getsize(out)} bytes")
