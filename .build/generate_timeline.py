#!/usr/bin/env python3
"""Generator for assets/timeline-dark.svg and assets/timeline-light.svg.

Aaditya Padiya — Career Timeline: horizontal accent-gradient spine that draws
itself, five chronological nodes with alternating glass cards. Sibling of
generate_svgs.py. SMIL only, README-safe.
"""
import os

W, H = 1180, 620

THEMES = {
    "dark": {
        "bg": "#030712", "panel": "#0F172A", "panel2": "#111C33",
        "text": "#F8FAFC", "sub": "#94A3B8", "muted": "#64748B",
        "border": "#1E293B",
        "a1": "#7C3AED", "a2": "#22D3EE", "a3": "#10B981",
        "a2text": "#22D3EE", "a3text": "#10B981",
        "glassline": "#FFFFFF", "aurora_op": "0.55",
        "pill_fill": "#0B1526", "glow_op": "0.9",
        "desc": "dark",
    },
    "light": {
        "bg": "#FFFFFF", "panel": "#F8FAFC", "panel2": "#F1F5F9",
        "text": "#0F172A", "sub": "#475569", "muted": "#64748B",
        "border": "#E2E8F0",
        "a1": "#2563EB", "a2": "#06B6D4", "a3": "#10B981",
        "a2text": "#0E7490", "a3text": "#047857",
        "glassline": "#0F172A", "aurora_op": "0.22",
        "pill_fill": "#FFFFFF", "glow_op": "0.5",
        "desc": "light",
    },
}

MONO = "ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"

SPINE_Y = 312
SPINE_X0, SPINE_X1 = 70, 1110
SPINE_DUR = 2.5
SPINE_BEGIN = 0.4

# (dates, role lines, company lines, achievement lines, kind, current)
NODES = [
    ("2020 - 2023",
     ["BCA Information", "Technology"],
     ["Shri Shivaji Science", "College, Amravati"],
     ["Foundation in IT &", "computer applications"],
     "edu", False),
    ("Jan 2024 - Jan 2025",
     ["IT Manager / Desktop", "Support (L2)"],
     ["Mediprobe Consultancy", "Services, Pune"],
     ["99%+ uptime; -40% incident", "resolution time"],
     "job", False),
    ("Jan 2025 - Oct 2025",
     ["IT Engineer (L2/L3)"],
     ["Godrej Properties", "Limited, Pune"],
     ["Designed 350-user network:", "dual-ISP failover, 9 VLANs"],
     "job", False),
    ("Nov 2025 - Present",
     ["System Administrator"],
     ["CludoBits IT Solutions,", "Pune"],
     ["50+ endpoints at 99.9%", "uptime; AI/LLM deployments"],
     "job", True),
    ("Mar 2026 - Present",
     ["Director & CTO"],
     ["Nexovo Tech Services,", "Pune"],
     ["End-to-end IT solutions,", "cloud & product delivery"],
     "job", True),
]

NODE_X = [130, 362, 594, 826, 1058]
CARD_W = 206


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs(t):
    a1, a2, a3 = t["a1"], t["a2"], t["a3"]
    return f"""<defs>
<linearGradient id="ag" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/><stop offset="1" stop-color="{a3}"/>
</linearGradient>
<linearGradient id="sp" gradientUnits="userSpaceOnUse" x1="{SPINE_X0}" y1="0" x2="{SPINE_X1}" y2="0">
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
    p.append(f'''<g clip-path="url(#cv)" opacity="{t['aurora_op']}">
<circle cx="170" cy="120" r="240" fill="url(#b1)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;120 70;30 -40;0 0" dur="27s" repeatCount="indefinite"/>
</circle>
<circle cx="1000" cy="500" r="260" fill="url(#b2)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-140 -90;-30 50;0 0" dur="31s" repeatCount="indefinite"/>
</circle>
<circle cx="600" cy="80" r="200" fill="url(#b3)" filter="url(#fb)" opacity="0.8">
  <animateTransform attributeName="transform" type="translate" values="0 0;-80 100;90 30;0 0" dur="24s" repeatCount="indefinite"/>
</circle>
</g>''')
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="url(#gl)" clip-path="url(#cv)"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="1.6" opacity="0.9"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="3" opacity="0.22" filter="url(#fs)"/>')
    return "".join(p)


def header(t):
    return f'''<text x="30" y="52" font-family="{SANS}" font-size="21" font-weight="700" fill="{t['text']}">Career Timeline</text>
<text x="30" y="72" font-family="{MONO}" font-size="11.5" fill="{t['muted']}" xml:space="preserve">$ history --career --chronological</text>
<text x="{W-30}" y="52" font-family="{MONO}" font-size="12" fill="{t['a2text']}" text-anchor="end" xml:space="preserve">2020 &#8594; present</text>'''


def node_begin(nx):
    return SPINE_BEGIN + SPINE_DUR * (nx - SPINE_X0) / (SPINE_X1 - SPINE_X0)


def spine(t):
    L = SPINE_X1 - SPINE_X0
    p = []
    p.append(f'''<path d="M{SPINE_X0} {SPINE_Y} H{SPINE_X1}" stroke="{t['border']}" stroke-width="2" fill="none"/>
<path d="M{SPINE_X0} {SPINE_Y} H{SPINE_X1}" stroke="url(#sp)" stroke-width="3" stroke-linecap="round" fill="none" stroke-dasharray="{L}" stroke-dashoffset="{L}" filter="url(#fg)" opacity="{t['glow_op']}">
  <animate attributeName="stroke-dashoffset" from="{L}" to="0" begin="{SPINE_BEGIN}s" dur="{SPINE_DUR}s" fill="freeze"/>
</path>
<path d="M{SPINE_X0} {SPINE_Y} H{SPINE_X1}" stroke="url(#sp)" stroke-width="3" stroke-linecap="round" fill="none" stroke-dasharray="{L}" stroke-dashoffset="{L}">
  <animate attributeName="stroke-dashoffset" from="{L}" to="0" begin="{SPINE_BEGIN}s" dur="{SPINE_DUR}s" fill="freeze"/>
</path>''')
    # Patrolling glow dot (right then back, forever)
    p.append(f'''<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{SPINE_BEGIN+SPINE_DUR+0.2:.1f}s" dur="0.4s" fill="freeze"/>
<circle r="5" fill="{t['a2']}" filter="url(#fg)">
  <animateMotion path="M{SPINE_X0+8} {SPINE_Y} H{SPINE_X1-8} H{SPINE_X0+8}" dur="12s" begin="{SPINE_BEGIN+SPINE_DUR:.1f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>
</circle></g>''')
    return "".join(p)


def node_marker(t, nx, kind, current, begin):
    p = [f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>']
    p.append(f'''<circle cx="{nx}" cy="{SPINE_Y}" r="11" fill="{t['bg']}" stroke="url(#ag)" stroke-width="2"/>
<circle cx="{nx}" cy="{SPINE_Y}" r="5.5" fill="url(#ag)"/>
<circle cx="{nx}" cy="{SPINE_Y}" r="11" fill="none" stroke="{t['a2']}" stroke-width="1.5" opacity="0">
  <animate attributeName="r" values="11;24" begin="{begin+0.3:.2f}s" dur="2.6s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.7;0" begin="{begin+0.3:.2f}s" dur="2.6s" repeatCount="indefinite"/>
</circle>''')
    if current:
        p.append(f'''<circle cx="{nx}" cy="{SPINE_Y}" r="17" fill="none" stroke="{t['a3']}" stroke-width="2" filter="url(#fg)">
  <animate attributeName="opacity" values="0.9;0.25;0.9" dur="1.8s" repeatCount="indefinite"/>
  <animate attributeName="r" values="15;19;15" dur="1.8s" repeatCount="indefinite"/>
</circle>''')
    if kind == "edu":
        # graduation cap glyph beside the node
        gx, gy = nx + 20, SPINE_Y - 16
        p.append(f'''<g stroke="{t['a2text']}" stroke-width="1.6" fill="none" stroke-linejoin="round">
<path d="M{gx} {gy} l11 4.5 l-11 4.5 l-11 -4.5 Z"/>
<path d="M{gx-6} {gy+6.5} v5 c0 2.5 12 2.5 12 0 v-5"/>
<path d="M{gx+11} {gy+4.5} v7"/>
</g>''')
    p.append("</g>")
    return "".join(p)


def node_card(t, i, nx, above, data, begin):
    dates, role, company, achieve, kind, current = data
    pad = 14
    lh_role, lh_co, lh_ach = 17, 14.5, 13.5
    ch = (22 + 8 + len(role) * lh_role + 4 + len(company) * lh_co + 6
          + len(achieve) * lh_ach + pad - 2)
    cx = min(max(nx - CARD_W / 2, 34), W - 34 - CARD_W)
    if above:
        cy = SPINE_Y - 34 - ch
        stem = f"M{nx} {SPINE_Y-11} V{cy+ch+2}"
    else:
        cy = SPINE_Y + 34
        stem = f"M{nx} {SPINE_Y+11} V{cy-2}"
    p = [f'''<g opacity="0">
<animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.45s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" values="0 {'10' if above else '-10'};0 0" begin="{begin:.2f}s" dur="0.45s" fill="freeze"/>
<path d="{stem}" stroke="{t['sub']}" stroke-width="1.3" stroke-dasharray="3 3" opacity="0.8"/>
<rect x="{cx:.0f}" y="{cy:.0f}" width="{CARD_W}" height="{ch:.0f}" rx="14" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<rect x="{cx:.0f}" y="{cy:.0f}" width="{CARD_W}" height="{ch:.0f}" rx="14" fill="url(#gl)"/>
<rect x="{cx+12:.0f}" y="{cy+1:.0f}" width="{CARD_W-70}" height="1" fill="{t['glassline']}" opacity="0.12"/>
<rect x="{cx:.0f}" y="{cy:.0f}" width="3" height="{ch:.0f}" rx="1.5" fill="url(#ag)" opacity="0.85"/>''']
    tx = cx + pad + 3
    ty = cy + 22
    p.append(f'<text x="{tx:.0f}" y="{ty:.0f}" font-family="{MONO}" font-size="10" fill="{t["a2text"]}" xml:space="preserve">{esc(dates)}</text>')
    if current:
        p.append(f'''<circle cx="{cx+CARD_W-20:.0f}" cy="{ty-4:.0f}" r="3.2" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
</circle>''')
    ty += 8
    for ln in role:
        ty += lh_role
        p.append(f'<text x="{tx:.0f}" y="{ty:.0f}" font-family="{SANS}" font-size="13" font-weight="700" fill="{t["text"]}">{esc(ln)}</text>')
    ty += 4
    for ln in company:
        ty += lh_co
        p.append(f'<text x="{tx:.0f}" y="{ty:.0f}" font-family="{SANS}" font-size="11" fill="{t["sub"]}">{esc(ln)}</text>')
    ty += 6
    for ln in achieve:
        ty += lh_ach
        p.append(f'<text x="{tx:.0f}" y="{ty:.0f}" font-family="{SANS}" font-size="10.5" fill="{t["muted"]}">{esc(ln)}</text>')
    p.append("</g>")
    return "".join(p)


def timeline(t):
    p = [spine(t)]
    for i, data in enumerate(NODES):
        nx = NODE_X[i]
        above = i % 2 == 0
        nb = node_begin(nx)
        p.append(node_marker(t, nx, data[4], data[5], nb))
        p.append(node_card(t, i, nx, above, data, nb + 0.15))
    return "".join(p)


def build(theme_key):
    t = THEMES[theme_key]
    title = "Aaditya Padiya — Career Timeline"
    desc = (f"Animated {t['desc']}-theme career timeline for Aaditya Padiya: BCA IT (2020-2023), "
            "IT Manager at Mediprobe Consultancy (2024), IT Engineer at Godrej Properties (2025), "
            "System Administrator at CludoBits IT Solutions (Nov 2025-present) and Director &amp; CTO "
            "at Nexovo Tech Services (Mar 2026-present).")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{defs(t)}
{background(t)}
{header(t)}
{timeline(t)}
</svg>'''


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for key in ("dark", "light"):
        out = os.path.join(root, "assets", f"timeline-{key}.svg")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(key))
        print(f"timeline-{key}.svg: {os.path.getsize(out)} bytes")
