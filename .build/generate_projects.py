#!/usr/bin/env python3
"""Generator for assets/projects-dark.svg and assets/projects-light.svg —
Aaditya Padiya featured-projects showcase grid.

GitHub-README-safe: SMIL animations only, no <script>/<style>/foreignObject,
no external refs, system font stacks only.
"""
import os

W, H = 1180, 740
MX = 28          # outer margin
GAP = 24
COLS = 4
CW = (W - 2 * MX - (COLS - 1) * GAP) // COLS   # 263
CH = 290
GY = 84          # grid top

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
        "pill_fill": "#FFFFFF",
        "desc": "light",
    },
}

MONO = "ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"

# name lines (max 2), category, status, 3 desc lines (<=34 chars), chips
PROJECTS = [
    (["Nexovo Self-Healing", "Cloud"], "AIOPS/SRE", "PRODUCTION",
     ["AI-native AIOps platform with", "real-time incident detection,", "AI RCA and escalation workflows."],
     ["Python", "Streamlit", "FastAPI", "Render"]),
    (["TrustOCR AI"], "AI/BLOCKCHAIN", "LIVE",
     ["Blockchain-verified document AI:", "browser OCR, AI structuring, on-", "chain SHA-256 registry."],
     ["Next.js", "Solidity", "Hardhat", "Ollama"]),
    (["Corporate Network", "Infra"], "NETWORKING", "DEPLOYED",
     ["Enterprise network for 350 users:", "SonicWALL dual-ISP failover, 9", "VLANs, HP Gen10 DMZ server."],
     ["SonicWALL", "L3", "VLAN", "Firewall"]),
    (["HealthEcosystem"], "HEALTHCARE SAAS", "IN DEV",
     ["Multi-tenant healthcare SaaS:", "LIMS, EHR, PMS, billing, PACS/RIS,", "ABDM compliance and AI."],
     ["TypeScript", "NestJS", "Next.js", "EKS"]),
    (["EduAI"], "AI/EDTECH", "IN DEV",
     ["Multi-tenant SaaS for AI-powered", "education, Classes 1-10 across", "CBSE/ICSE/State boards."],
     ["TypeScript", "Turborepo", "Next.js", "AI"]),
    (["Real Estate ERP"], "ENTERPRISE SAAS", "IN DEV",
     ["Enterprise-grade multi-tenant", "SaaS platform for Indian real", "estate developers."],
     ["TypeScript", "Next.js", "Postgres"]),
    (["AI Interview Model"], "AI", "LIVE",
     ["AI-powered interview platform", "with Python model backend and", "TypeScript frontend."],
     ["Python", "TypeScript", "AI", "Vercel"]),
    (["Ritika Infotech"], "WEB/SEO", "LIVE",
     ["SEO-optimized business website", "ranking on Google; domain,", "hosting and production ops."],
     ["HTML", "CSS", "JS", "SEO"]),
]

GREEN_STATUSES = ("LIVE", "PRODUCTION", "DEPLOYED")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


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
<circle cx="200" cy="120" r="280" fill="url(#b1)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;130 80;30 -40;0 0" dur="27s" repeatCount="indefinite"/>
</circle>
<circle cx="990" cy="590" r="300" fill="url(#b2)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-150 -90;-40 50;0 0" dur="32s" repeatCount="indefinite"/>
</circle>
</g>''')
    # Sparse floating particles
    dots = []
    seeds = [(150, 640, 1.6, 18, "M0 0 C 30 -60, 90 -40, 60 -120"),
             (1030, 130, 1.5, 21, "M0 0 C -40 50, 40 100, -20 150"),
             (610, 700, 1.8, 19, "M0 0 C 40 -70, -40 -100, 30 -160")]
    for cx, cy, r, dur, path in seeds:
        dots.append(f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t['particle']}" opacity="0.4" filter="url(#fg)">
  <animateMotion path="{path}" dur="{dur}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.1;0.45;0.1" dur="{dur/3:.1f}s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'<g clip-path="url(#cv)">{"".join(dots)}</g>')
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="url(#gl)" clip-path="url(#cv)"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="1.6" opacity="0.9"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="3" opacity="0.25" filter="url(#fs)"/>')
    return "".join(p)


def header(t):
    return f'''<circle cx="40" cy="48" r="4" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
</circle>
<text x="54" y="53" font-family="{MONO}" font-size="14" fill="{t['muted']}" xml:space="preserve">$ projects --featured</text>
<text x="{W-36}" y="53" font-family="{MONO}" font-size="12" fill="{t['muted']}" text-anchor="end" xml:space="preserve">8 results</text>'''


def chip_w(label):
    return round(len(label) * 10 * 0.62 + 16)


def card(t, idx, x, y, name_lines, category, status, desc_lines, chips):
    begin = 0.3 + idx * 0.18
    p = [f'''<g opacity="0">
<animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" values="0 12;0 0" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>''']
    # Breathing border glow behind the panel
    p.append(f'''<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="20" fill="none" stroke="url(#ag)" stroke-width="2.5" opacity="0.2" filter="url(#fs)">
  <animate attributeName="opacity" values="0.1;0.4;0.1" dur="4.5s" begin="{idx*0.6:.1f}s" repeatCount="indefinite"/>
</rect>''')
    # Glass panel
    p.append(f'''<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="20" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="20" fill="url(#gl)"/>
<rect x="{x+16}" y="{y+1}" width="{CW-80}" height="1" fill="{t['glassline']}" opacity="0.12"/>''')
    # Status badge (top-right)
    scol = t["a3text"] if status in GREEN_STATUSES else t["a2text"]
    bw = round(len(status) * 9 * 0.62 + 26)
    bx = x + CW - 16 - bw
    p.append(f'''<rect x="{bx}" y="{y+16}" width="{bw}" height="20" rx="10" fill="{t['pill_fill']}" fill-opacity="0.85" stroke="{scol}" stroke-opacity="0.5" stroke-width="1"/>
<circle cx="{bx+11}" cy="{y+26}" r="3" fill="{scol}">
  <animate attributeName="opacity" values="1;0.25;1" dur="1.8s" begin="{idx*0.3:.1f}s" repeatCount="indefinite"/>
</circle>
<text x="{bx+19}" y="{y+29.5}" font-family="{MONO}" font-size="9" fill="{scol}" xml:space="preserve">{esc(status)}</text>''')
    # Category label
    p.append(f'<text x="{x+18}" y="{y+30}" font-family="{MONO}" font-size="10" letter-spacing="1" fill="{t["a2text"]}" xml:space="preserve">{esc(category)}</text>')
    # Project name (up to 2 lines)
    for j, line in enumerate(name_lines):
        p.append(f'<text x="{x+18}" y="{y+66+j*21}" font-family="{SANS}" font-size="15.5" font-weight="700" fill="{t["text"]}">{esc(line)}</text>')
    # Accent underline
    p.append(f'<rect x="{x+18}" y="{y+96}" width="34" height="2.5" rx="1.25" fill="url(#ag)" opacity="0.8"/>')
    # Description (3 lines)
    for j, line in enumerate(desc_lines):
        p.append(f'<text x="{x+18}" y="{y+124+j*17}" font-family="{SANS}" font-size="11.5" fill="{t["sub"]}">{esc(line)}</text>')
    # Tech chips (wrap into rows near the bottom)
    chip_h = 21
    cx0 = x + 18
    max_x = x + CW - 16
    px, py = cx0, y + CH - 62
    for k, label in enumerate(chips):
        pw = chip_w(label)
        if px + pw > max_x:
            px = cx0
            py += chip_h + 7
        p.append(f'''<rect x="{px}" y="{py}" width="{pw}" height="{chip_h}" rx="{chip_h/2}" fill="{t['pill_fill']}" fill-opacity="0.85" stroke="url(#ag)" stroke-width="1">
  <animate attributeName="stroke-opacity" values="0.55;1;0.55" dur="3.4s" begin="{(idx*0.4+k*0.5):.1f}s" repeatCount="indefinite"/>
</rect>
<text x="{px+pw/2:.0f}" y="{py+14.5}" font-family="{MONO}" font-size="10" fill="{t['text']}" text-anchor="middle" xml:space="preserve">{esc(label)}</text>''')
        px += pw + 7
    p.append("</g>")
    return "".join(p)


def build(theme_key):
    t = THEMES[theme_key]
    title = "Aaditya Padiya — Featured Projects"
    desc = (f"Animated {t['desc']}-theme showcase of eight featured projects by Aaditya Padiya: "
            "Nexovo Self-Healing Cloud (AIOps), TrustOCR AI (blockchain document AI), Corporate "
            "Network Infrastructure, HealthEcosystem (healthcare SaaS), EduAI (AI edtech), "
            "Real Estate ERP, AI Interview Model and Ritika Infotech, each shown as a glass "
            "card with category, description, tech chips and live status.")
    cards = []
    for i, (name_lines, category, status, desc_lines, chips) in enumerate(PROJECTS):
        col, row = i % COLS, i // COLS
        x = MX + col * (CW + GAP)
        y = GY + row * (CH + GAP)
        cards.append(card(t, i, x, y, name_lines, category, status, desc_lines, chips))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{defs(t)}
{background(t)}
{header(t)}
{"".join(cards)}
</svg>'''
    return svg


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for key in ("dark", "light"):
        out = os.path.join(root, "assets", f"projects-{key}.svg")
        content = build(key)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"projects-{key}.svg: {os.path.getsize(out)} bytes")
