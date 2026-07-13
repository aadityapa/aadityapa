#!/usr/bin/env python3
"""Generator for assets/dark.svg and assets/light.svg — Aaditya Padiya GitHub profile hero.

GitHub-README-safe: SMIL animations only, no <script>/<style>/foreignObject,
no external refs, system font stacks only.
"""
import os

W, H = 1180, 610

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
        "noise_op": "0.05",
        "particle": "#22D3EE",
        "scan_op": "0.05",
        "glow_op": "0.9",
        "pill_fill": "#0B1526",
        "shadow_op": "0.55",
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
        "noise_op": "0.03",
        "particle": "#2563EB",
        "scan_op": "0.04",
        "glow_op": "0.5",
        "pill_fill": "#FFFFFF",
        "shadow_op": "0.12",
        "desc": "light",
    },
}

MONO = "ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- ASCII avatar
ASCII_ART = [
    "            .:-=======-:.            ",
    "        .=*%@@@@@@@@@@@@%*=.         ",
    "      -#@@@@@@@@@@@@@@@@@@@@#-       ",
    "    .*@@@@@@@@@@@@@@@@@@@@@@@@*.     ",
    "   .#@@@@@%#*+==-::-==+*#%@@@@@#.    ",
    "   *@@@@%=.            .=%@@@@*      ",
    "  -@@@@#.    .::    ::.    .#@@@@-   ",
    "  #@@@%    -%@@%.  .%@@%-    %@@@#   ",
    "  @@@@+    +@@@@.  .@@@@+    +@@@@   ",
    "  @@@@+     -==:    :==-     +@@@@   ",
    "  #@@@%.                    .%@@@#   ",
    "  -@@@@*       .-==-.       *@@@@-   ",
    "   *@@@@#-    +%@@@@%+    -#@@@@*    ",
    "   .#@@@@@%*=:.      .:=*%@@@@@#.    ",
    "     *@@@@@@@@@%####%@@@@@@@@@*      ",
    "      -#@@@@@@@@@@@@@@@@@@@@#-       ",
    "        .=*%@@@@@@@@@@@@%*=.         ",
    "            .:-=======-:.            ",
]

TERMINAL_TAIL = [
    ("root@aadityapa:~$ whoami", "sub"),
    ("system.administrator", "a2"),
    ("root@aadityapa:~$ uptime", "sub"),
    ("99.9% | 3+ yrs in production", "a3"),
]

ROLES = [
    "System Administrator",
    "Cloud Engineer (AWS)",
    "DevOps Engineer",
    "AI Infrastructure Engineer",
    "Network Engineer",
    "Full Stack Developer",
    "SRE / AIOps Builder",
    "Linux Administrator",
    "Open Source Contributor",
]

INFO_ROWS = [
    ("location", "Pune, Maharashtra, India"),
    ("education", "BCA - Information Technology (2020-2023)"),
    ("experience", "3+ years | IT Infrastructure & Cloud"),
    ("company", "CludoBits IT Solutions Pvt. Ltd."),
    ("portfolio", "aadityapadiya.vercel.app"),
    ("linkedin", "in/aaditya-padiya-7b64372"),
    ("email", "aadityapadiya@gmail.com"),
    ("focus", "AI Infrastructure | AIOps | Self-Healing Systems"),
]

SKILLS = [
    "AWS", "Linux", "Windows Server", "Docker", "Networking",
    "Active Directory", "CI/CD", "Python", "Ollama / LLMs",
    "Intune", "FastAPI", "Next.js",
]

GH_PATH = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 "
           "0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13"
           "-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66."
           "07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.0"
           "8-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 "
           ".27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.1"
           "5 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 "
           "0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z")

LI_PATH = ("M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 "
           ".633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 "
           "12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-"
           ".015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1."
           "248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431."
           "568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1"
           ".184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0"
           " 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z")


def defs(t):
    a1, a2, a3 = t["a1"], t["a2"], t["a3"]
    return f"""<defs>
<linearGradient id="ag" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/><stop offset="1" stop-color="{a3}"/>
</linearGradient>
<linearGradient id="agt" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{t['a2text']}"/><stop offset="1" stop-color="{t['a3text']}"/>
</linearGradient>
<linearGradient id="bs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.25" stop-color="{a2}"/>
  <stop offset="0.5" stop-color="{a3}"/><stop offset="0.75" stop-color="{a2}"/>
  <stop offset="1" stop-color="{a1}"/>
  <animateTransform attributeName="gradientTransform" type="rotate" from="0 {W//2} {H//2}" to="360 {W//2} {H//2}" dur="14s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="sw" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
  <stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/><stop offset="1" stop-color="{a3}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-{W} 0;{W} 0;-{W} 0" dur="9s" repeatCount="indefinite"/>
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
<linearGradient id="sc" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{a2}" stop-opacity="0"/>
  <stop offset="0.5" stop-color="{a2}" stop-opacity="{t['scan_op']}"/>
  <stop offset="1" stop-color="{a2}" stop-opacity="0"/>
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
<filter id="nz" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="n"/>
  <feColorMatrix in="n" type="saturate" values="0"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.6" intercept="0"/></feComponentTransfer>
</filter>
<pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="2" fill="{t['glassline']}" opacity="0.045"/>
</pattern>
<clipPath id="cv"><rect x="0" y="0" width="{W}" height="{H}" rx="24"/></clipPath>
</defs>"""


def background(t):
    p = []
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>')
    # Aurora blobs
    p.append(f'''<g clip-path="url(#cv)" opacity="{t['aurora_op']}">
<circle cx="180" cy="120" r="300" fill="url(#b1)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;140 90;40 -50;0 0" dur="26s" repeatCount="indefinite"/>
</circle>
<circle cx="980" cy="480" r="320" fill="url(#b2)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-160 -100;-40 60;0 0" dur="31s" repeatCount="indefinite"/>
</circle>
<circle cx="640" cy="40" r="240" fill="url(#b3)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-90 130;110 40;0 0" dur="23s" repeatCount="indefinite"/>
</circle>
<circle cx="380" cy="560" r="220" fill="url(#b1)" filter="url(#fb)" opacity="0.7">
  <animateTransform attributeName="transform" type="translate" values="0 0;120 -140;-60 -30;0 0" dur="29s" repeatCount="indefinite"/>
</circle>
</g>''')
    # Radial pulsing lights
    p.append(f'''<g clip-path="url(#cv)">
<circle cx="238" cy="300" r="200" fill="url(#b2)" opacity="0.16">
  <animate attributeName="opacity" values="0.10;0.24;0.10" dur="6s" repeatCount="indefinite"/>
</circle>
<circle cx="810" cy="290" r="260" fill="url(#b1)" opacity="0.10">
  <animate attributeName="opacity" values="0.06;0.16;0.06" dur="8s" repeatCount="indefinite"/>
</circle>
</g>''')
    # Noise texture
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" filter="url(#nz)" opacity="{t["noise_op"]}"/>')
    # Floating particles
    dots = []
    seeds = [(120, 500, 2, 15, "M0 0 C 30 -60, 90 -40, 60 -120"),
             (300, 90, 1.6, 19, "M0 0 C -40 50, 40 100, -20 150"),
             (560, 540, 2.4, 17, "M0 0 C 50 -50, -30 -110, 40 -170"),
             (760, 110, 1.4, 21, "M0 0 C -50 60, 50 90, -30 160"),
             (930, 520, 2, 16, "M0 0 C 40 -70, -40 -100, 30 -160"),
             (1080, 200, 1.6, 18, "M0 0 C -30 60, 40 110, -20 170"),
             (480, 200, 1.2, 22, "M0 0 C 40 60, -40 120, 30 180"),
             (860, 420, 1.8, 20, "M0 0 C -50 -50, 40 -110, -30 -160")]
    for cx, cy, r, dur, path in seeds:
        dots.append(f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t['particle']}" opacity="0.5" filter="url(#fg)">
  <animateMotion path="{path}" dur="{dur}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.15;0.6;0.15" dur="{dur/3:.1f}s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'<g clip-path="url(#cv)">{"".join(dots)}</g>')
    # Slow scanline
    p.append(f'''<g clip-path="url(#cv)"><rect x="0" y="-120" width="{W}" height="110" fill="url(#sc)">
  <animateTransform attributeName="transform" type="translate" values="0 0;0 {H+240}" dur="11s" repeatCount="indefinite"/>
</rect></g>''')
    # Glass reflection across whole card
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="url(#gl)" clip-path="url(#cv)"/>')
    # Border shimmer
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="1.6" opacity="0.9"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="3" opacity="0.25" filter="url(#fs)"/>')
    return "".join(p)


def left_panel(t):
    x, y, w, h = 28, 28, 420, 554
    p = []
    p.append(f'''<g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#gl)"/>
<rect x="{x+18}" y="{y+1}" width="{w-120}" height="1" fill="{t['glassline']}" opacity="0.12"/>''')
    # Pulsing light behind ASCII
    p.append(f'''<circle cx="{x+w/2}" cy="{y+220}" r="150" fill="url(#b2)" opacity="0.25">
  <animate attributeName="opacity" values="0.15;0.4;0.15" dur="5s" repeatCount="indefinite"/>
  <animate attributeName="r" values="140;165;140" dur="7s" repeatCount="indefinite"/>
</circle>''')
    # Panel header
    p.append(f'''<text x="{x+24}" y="{y+34}" font-family="{MONO}" font-size="12" fill="{t['muted']}" xml:space="preserve">// avatar.render()</text>
<circle cx="{x+w-30}" cy="{y+30}" r="4" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
</circle>''')
    # ASCII art with staggered reveal + gradient sweep via mask + floating
    rows = []
    art_x = x + w / 2
    art_y0 = y + 72
    lh = 15
    for i, line in enumerate(ASCII_ART):
        begin = 0.4 + i * 0.14
        rows.append(f'''<text x="{art_x:.0f}" y="{art_y0 + i*lh}" font-family="{MONO}" font-size="11" text-anchor="middle" xml:space="preserve" fill="{t['a2']}" opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>{esc(line)}</text>''')
    mask_rows = []
    for i, line in enumerate(ASCII_ART):
        mask_rows.append(f'<text x="{art_x:.0f}" y="{art_y0 + i*lh}" font-family="{MONO}" font-size="11" text-anchor="middle" xml:space="preserve" fill="#FFFFFF">{esc(line)}</text>')
    art_h = len(ASCII_ART) * lh
    p.append(f'''<g filter="url(#fg)" opacity="{t['glow_op']}">
<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0;0 4;0 0" dur="9s" repeatCount="indefinite"/>
{''.join(rows)}
<mask id="am">{''.join(mask_rows)}</mask>
<g mask="url(#am)" opacity="0"><animate attributeName="opacity" values="0;0.9" begin="3.2s" dur="0.8s" fill="freeze"/>
  <rect x="{x}" y="{art_y0-14}" width="{w}" height="{art_h+10}" fill="url(#sw)"/>
</g>
</g>''')
    # CRT scanlines over avatar zone
    p.append(f'<rect x="{x+12}" y="{art_y0-20}" width="{w-24}" height="{art_h+16}" fill="url(#crt)" rx="10"/>')
    # Terminal tail lines
    ty = art_y0 + art_h + 34
    tail = []
    for i, (line, colkey) in enumerate(TERMINAL_TAIL):
        begin = 3.4 + i * 0.5
        col = t[colkey + "text"] if colkey in ("a2", "a3") else t["sub"]
        prefix = "" if line.startswith("root@") else "  "
        tail.append(f'''<text x="{x+24}" y="{ty + i*24}" font-family="{MONO}" font-size="12.5" fill="{col}" xml:space="preserve" opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin:.1f}s" dur="0.3s" fill="freeze"/>{prefix}{esc(line)}</text>''')
    # blinking block cursor at end
    tail.append(f'''<rect x="{x+24}" y="{ty + len(TERMINAL_TAIL)*24 - 11}" width="8" height="14" fill="{t['a2']}" opacity="0">
  <animate attributeName="opacity" values="0;0" begin="0s" dur="5.4s" fill="freeze"/>
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" begin="5.4s" dur="1.1s" repeatCount="indefinite"/>
</rect>''')
    p.append("".join(tail))
    p.append("</g>")
    return "".join(p)


def typing_name(t, x, y):
    text = "Hi, I'm Aaditya Padiya"
    fs = 25
    ch = fs * 0.602
    n = len(text)
    dur = 1.9
    widths = ";".join(f"{i*ch:.1f}" for i in range(n + 1))
    # Cursor x is an absolute coordinate: clip widths offset by the text origin.
    xvals = ";".join(f"{x + i*ch:.1f}" for i in range(n + 1))
    keytimes = ";".join(f"{i/n:.4f}" for i in range(n + 1))
    end_x = x + n * ch
    return f'''<clipPath id="tn"><rect x="{x}" y="{y-fs}" width="0" height="{fs+12}">
  <animate attributeName="width" values="{widths}" keyTimes="{keytimes}" calcMode="discrete" begin="0.9s" dur="{dur}s" fill="freeze"/>
</rect></clipPath>
<g clip-path="url(#tn)"><text x="{x}" y="{y}" font-family="{MONO}" font-size="{fs}" font-weight="700" fill="{t['text']}" xml:space="preserve">{esc(text)}</text></g>
<text x="{end_x + 10:.0f}" y="{y}" font-size="{fs}" opacity="0">👋<animate attributeName="opacity" values="0;1" begin="{0.9+dur:.1f}s" dur="0.3s" fill="freeze"/><animateTransform attributeName="transform" type="rotate" values="0 {end_x+22:.0f} {y};14 {end_x+22:.0f} {y};-8 {end_x+22:.0f} {y};0 {end_x+22:.0f} {y}" begin="{0.9+dur:.1f}s" dur="1.6s" repeatCount="3"/></text>
<rect x="{x}" y="{y-fs+4}" width="12" height="{fs}" fill="{t['a2']}" opacity="0.9">
  <animate attributeName="x" values="{xvals}" keyTimes="{keytimes}" calcMode="discrete" begin="0.9s" dur="{dur}s" fill="freeze"/>
  <animate attributeName="opacity" values="0.9;0.9;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
</rect>'''


def rotating_roles(t, x, y):
    n = len(ROLES)
    seg = 3.0
    cycle = n * seg
    parts = [f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="15" fill="{t["sub"]}" xml:space="preserve">&gt; </text>']
    rx = x + 18
    for i, role in enumerate(ROLES):
        t0 = i * seg / cycle
        t1 = (i * seg + 0.45) / cycle
        t2 = ((i + 1) * seg - 0.45) / cycle
        t3 = (i + 1) * seg / cycle
        if i == 0:
            kt = f"0;{t2:.4f};{t3:.4f};0.999;1"
            vals = "1;1;0;0;0"
        elif i == len(ROLES) - 1:
            kt = f"0;{t0:.4f};{t1:.4f};{t2:.4f};1"
            vals = "0;0;1;1;0"
        else:
            kt = f"0;{t0:.4f};{t1:.4f};{t2:.4f};{t3:.4f};1"
            vals = "0;0;1;1;0;0"
        parts.append(f'''<text x="{rx}" y="{y}" font-family="{MONO}" font-size="15" font-weight="600" fill="url(#agt)" filter="url(#fg)" xml:space="preserve" opacity="0"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{cycle}s" begin="3s" repeatCount="indefinite"/>{esc(role)}</text>''')
    # Block cursor rides the end of whichever role is currently visible.
    ch = 15 * 0.602
    ends = [f"{rx + len(r) * ch + 6:.0f}" for r in ROLES]
    ckt = ";".join(f"{i / n:.4f}" for i in range(n)) + ";1"
    cvals = ";".join(ends) + f";{ends[0]}"
    parts.append(f'''<rect x="{ends[0]}" y="{y-13}" width="9" height="16" fill="{t['a2']}">
  <animate attributeName="x" values="{cvals}" keyTimes="{ckt}" calcMode="discrete" dur="{cycle}s" begin="3s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>
</rect>''')
    return "".join(parts)


def right_panel(t):
    x, y, w, h = 472, 28, 680, 554
    p = []
    p.append(f'''<g>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#gl)"/>
<rect x="{x+18}" y="{y+1}" width="{w-160}" height="1" fill="{t['glassline']}" opacity="0.12"/>''')
    # Terminal title bar
    p.append(f'''<path d="M{x} {y+44} h{w}" stroke="{t['border']}" stroke-width="1"/>
<circle cx="{x+26}" cy="{y+22}" r="5.5" fill="#FF5F57"/>
<circle cx="{x+46}" cy="{y+22}" r="5.5" fill="#FEBC2E"/>
<circle cx="{x+66}" cy="{y+22}" r="5.5" fill="#28C840"/>
<text x="{x+w/2:.0f}" y="{y+26}" font-family="{MONO}" font-size="12" fill="{t['muted']}" text-anchor="middle" xml:space="preserve">aaditya@cludobits: ~/profile</text>''')
    # Typing name + roles
    p.append(typing_name(t, x + 30, y + 92))
    p.append(rotating_roles(t, x + 30, y + 126))
    p.append(f'<path d="M{x+30} {y+148} h{w-60}" stroke="{t["border"]}" stroke-width="1"/>')
    # Info rows
    iy0 = y + 172
    step = 27
    label_w = 118
    rows = []
    for i, (label, value) in enumerate(INFO_ROWS):
        begin = 3.0 + i * 0.32
        ry = iy0 + i * step
        rows.append(f'''<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.4s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" values="14 0;0 0" begin="{begin:.2f}s" dur="0.4s" fill="freeze"/>
<text x="{x+30}" y="{ry}" font-family="{MONO}" font-size="13.5" fill="{t['a2text']}" xml:space="preserve">❯ {label}</text>
<text x="{x+30+label_w+22}" y="{ry}" font-family="{MONO}" font-size="13.5" fill="{t['text']}" xml:space="preserve">{esc(value)}</text>
</g>''')
    p.append("".join(rows))
    # Skills
    sy = iy0 + len(INFO_ROWS) * step + 16
    p.append(f'<text x="{x+30}" y="{sy}" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}" xml:space="preserve">$ skills --top</text>')
    pills = []
    px, py = x + 30, sy + 14
    pill_h = 27
    fs = 12
    gap = 10
    max_x = x + w - 30
    idx = 0
    for skill in SKILLS:
        pw = round(len(skill) * fs * 0.62 + 26)
        if px + pw > max_x:
            px = x + 30
            py += pill_h + 10
        begin = 5.8 + idx * 0.12
        gbeg = idx * 0.3
        pills.append(f'''<g opacity="0"><animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>
<rect x="{px}" y="{py}" width="{pw}" height="{pill_h}" rx="{pill_h/2}" fill="none" stroke="url(#ag)" stroke-width="1.4" filter="url(#fs)" opacity="0.5">
  <animate attributeName="opacity" values="0.15;0.75;0.15" dur="3.6s" begin="{gbeg:.1f}s" repeatCount="indefinite"/>
</rect>
<rect x="{px}" y="{py}" width="{pw}" height="{pill_h}" rx="{pill_h/2}" fill="{t['pill_fill']}" fill-opacity="0.85" stroke="url(#ag)" stroke-width="1"/>
<text x="{px+pw/2:.0f}" y="{py+18}" font-family="{MONO}" font-size="{fs}" fill="{t['text']}" text-anchor="middle" xml:space="preserve">{esc(skill)}</text>
</g>''')
        px += pw + gap
        idx += 1
    p.append("".join(pills))
    # Divider + socials
    soy = py + pill_h + 24
    p.append(f'<path d="M{x+30} {soy-14} h{w-60}" stroke="{t["border"]}" stroke-width="1"/>')
    p.append(socials(t, x + 30, soy + 4))
    p.append("</g>")
    return "".join(p)


def socials(t, x, y):
    s = 1.45  # scale for 16px paths -> ~23px
    parts = [f'<g filter="url(#fg)" opacity="{t["glow_op"]}">']
    # GitHub icon + handle
    parts.append(f'''<g transform="translate({x},{y}) scale({s})"><path d="{GH_PATH}" fill="{t['text']}"/></g>
<text x="{x+34}" y="{y+17}" font-family="{MONO}" font-size="13" fill="{t['sub']}" xml:space="preserve">github.com/aadityapa</text>''')
    # LinkedIn
    lx = x + 218
    parts.append(f'''<g transform="translate({lx},{y}) scale({s})"><path d="{LI_PATH}" fill="{t['a2']}"/></g>
<text x="{lx+34}" y="{y+17}" font-family="{MONO}" font-size="13" fill="{t['sub']}" xml:space="preserve">linkedin</text>''')
    # Portfolio globe (primitive strokes)
    gx = lx + 120
    gc = t["a3"]
    parts.append(f'''<g transform="translate({gx},{y})" stroke="{gc}" stroke-width="1.6" fill="none">
<circle cx="11.5" cy="11.5" r="10"/><ellipse cx="11.5" cy="11.5" rx="4.4" ry="10"/>
<path d="M1.5 11.5 h20 M3.2 6 h16.6 M3.2 17 h16.6"/></g>
<text x="{gx+34}" y="{y+17}" font-family="{MONO}" font-size="13" fill="{t['sub']}" xml:space="preserve">aadityapadiya.vercel.app</text>''')
    # Email envelope (icon only; address already in info rows)
    ex = gx + 248
    mc = t["a1"]
    parts.append(f'''<g transform="translate({ex},{y})" stroke="{mc}" stroke-width="1.6" fill="none">
<rect x="1" y="3.5" width="21" height="16" rx="3"/><path d="M2 5.5 L11.5 13 L21 5.5"/></g>''')
    parts.append("</g>")
    # Slow shared glow pulse
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1" begin="7s" dur="0.6s" fill="freeze"/>'
            + "".join(parts) + "</g>")


def build(theme_key):
    t = THEMES[theme_key]
    title = "Aaditya Padiya — System Administrator, Cloud &amp; AI Infrastructure Engineer"
    desc = (f"Animated {t['desc']}-theme profile banner for Aaditya Padiya: an ASCII-art avatar inside a "
            "glass terminal, with typing name animation, rotating role titles, profile details "
            "(Pune India, BCA IT, 3+ years experience, CludoBits IT Solutions), animated skill pills "
            "and social links for GitHub, LinkedIn, portfolio and email.")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{defs(t)}
{background(t)}
{left_panel(t)}
{right_panel(t)}
</svg>'''
    return svg


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for key in ("dark", "light"):
        out = os.path.join(root, "assets", f"{key}.svg")
        content = build(key)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"{key}.svg: {os.path.getsize(out)} bytes")
