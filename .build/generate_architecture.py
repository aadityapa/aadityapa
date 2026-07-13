#!/usr/bin/env python3
"""Generator for assets/architecture-dark.svg and assets/architecture-light.svg.

Aaditya Padiya — Architecture & Infrastructure Showcase: 8 glass cards in a
4x2 grid, each with an animated mini-diagram. Sibling of generate_svgs.py.
GitHub-README-safe: SMIL only, no <script>/<style>/foreignObject, no external refs.
"""
import os

W, H = 1180, 800

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

MARGIN = 28
GAP = 24
GRID_TOP = 92
COLS, ROWS = 4, 2
CW = (W - 2 * MARGIN - (COLS - 1) * GAP) / COLS          # 263
CH = (H - GRID_TOP - MARGIN - (ROWS - 1) * GAP) / ROWS   # 330


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
<marker id="ah" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0.5 0.5 L7 4 L0.5 7.5 Z" fill="{t['sub']}"/>
</marker>
</defs>"""


def background(t):
    p = []
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>')
    p.append(f'''<g clip-path="url(#cv)" opacity="{t['aurora_op']}">
<circle cx="150" cy="110" r="230" fill="url(#b1)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;110 70;30 -40;0 0" dur="27s" repeatCount="indefinite"/>
</circle>
<circle cx="1010" cy="640" r="250" fill="url(#b2)" filter="url(#fb)">
  <animateTransform attributeName="transform" type="translate" values="0 0;-130 -90;-30 50;0 0" dur="31s" repeatCount="indefinite"/>
</circle>
<circle cx="620" cy="360" r="190" fill="url(#b3)" filter="url(#fb)" opacity="0.8">
  <animateTransform attributeName="transform" type="translate" values="0 0;-80 110;90 30;0 0" dur="24s" repeatCount="indefinite"/>
</circle>
</g>''')
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="24" fill="url(#gl)" clip-path="url(#cv)"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="1.6" opacity="0.9"/>')
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22.5" fill="none" stroke="url(#bs)" stroke-width="3" opacity="0.22" filter="url(#fs)"/>')
    return "".join(p)


def header(t):
    return f'''<text x="{MARGIN+2}" y="58" font-family="{SANS}" font-size="21" font-weight="700" fill="{t['text']}">Architecture &amp; Infrastructure Showcase</text>
<text x="{MARGIN+2}" y="78" font-family="{MONO}" font-size="11.5" fill="{t['muted']}" xml:space="preserve">$ blueprint --render --all-systems</text>
<text x="{W-MARGIN}" y="58" font-family="{MONO}" font-size="12" fill="{t['a2text']}" text-anchor="end" xml:space="preserve">// how i build</text>
<circle cx="{W-MARGIN-118}" cy="54" r="4" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
</circle>'''


def card_shell(t, x, y, label, idx):
    """Glass card chrome + label; returns opening markup (caller closes group)."""
    return f'''<rect x="{x:.0f}" y="{y:.0f}" width="{CW:.0f}" height="{CH:.0f}" rx="14" fill="{t['panel']}" fill-opacity="0.72" stroke="{t['border']}" stroke-width="1"/>
<rect x="{x:.0f}" y="{y:.0f}" width="{CW:.0f}" height="{CH:.0f}" rx="14" fill="url(#gl)"/>
<rect x="{x+14:.0f}" y="{y+1:.0f}" width="{CW-80:.0f}" height="1" fill="{t['glassline']}" opacity="0.12"/>
<text x="{x+16:.0f}" y="{y+27:.0f}" font-family="{MONO}" font-size="11" font-weight="600" fill="{t['a2text']}" letter-spacing="1.5" xml:space="preserve">{esc(label)}</text>
<text x="{x+CW-16:.0f}" y="{y+27:.0f}" font-family="{MONO}" font-size="10" fill="{t['muted']}" text-anchor="end" xml:space="preserve">0{idx}</text>
<path d="M{x+16:.0f} {y+38:.0f} h{CW-32:.0f}" stroke="{t['border']}" stroke-width="1"/>'''


def box(t, x, y, w, h, label, fs=10, rx=8, dash=None, label_fill=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    lf = label_fill or t["sub"]
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" '
            f'fill="{t["panel2"]}" fill-opacity="0.9" stroke="{t["border"]}" stroke-width="1.2"{d}/>'
            f'<text x="{x+w/2:.0f}" y="{y+h/2+fs*0.36:.0f}" font-family="{MONO}" font-size="{fs}" '
            f'fill="{lf}" text-anchor="middle" xml:space="preserve">{esc(label)}</text>')


def flow_line(t, d, dur="1.6s", dash="5 5", width="1.4", arrow=True, color=None):
    c = color or t["sub"]
    m = ' marker-end="url(#ah)"' if arrow else ""
    return (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}" stroke-dasharray="{dash}"{m}>'
            f'<animate attributeName="stroke-dashoffset" from="20" to="0" dur="{dur}" repeatCount="indefinite"/></path>')


# ---------------------------------------------------------------- 8 diagrams
def d_enterprise(t, x, y):
    """Layered client/app/data tiers with flowing arrows."""
    cx = x + CW / 2
    bw, bh, gap = 176, 48, 36
    ty0 = y + 62
    p = []
    tiers = [("CLIENT TIER", t["a2text"]), ("APP TIER", t["sub"]), ("DATA TIER", t["a3text"])]
    for i, (lbl, col) in enumerate(tiers):
        by = ty0 + i * (bh + gap)
        p.append(box(t, cx - bw / 2, by, bw, bh, lbl, fs=10.5, label_fill=col))
        p.append(f'<rect x="{cx-bw/2:.0f}" y="{by:.0f}" width="4" height="{bh}" rx="2" fill="url(#ag)" opacity="0.85"/>')
        if i < 2:
            ay0, ay1 = by + bh + 3, by + bh + gap - 5
            p.append(flow_line(t, f"M{cx-26:.0f} {ay0:.0f} V{ay1:.0f}", dur="1.4s"))
            p.append(flow_line(t, f"M{cx+26:.0f} {ay1:.0f} V{ay0:.0f}", dur="1.8s"))
    p.append(f'<text x="{cx:.0f}" y="{y+CH-20:.0f}" font-family="{MONO}" font-size="9.5" fill="{t["muted"]}" text-anchor="middle" xml:space="preserve">request / response flow</text>')
    return "".join(p)


def d_microservices(t, x, y):
    """Gateway fanning out to 3 services with pulsing status dots."""
    cx = x + CW / 2
    gy = y + 66
    p = [box(t, cx - 62, gy, 124, 38, "API GATEWAY", fs=10.5, label_fill=t["a2text"])]
    sy = y + 208
    sw, sh, sgap = 66, 44, 13
    total = 3 * sw + 2 * sgap
    sx0 = cx - total / 2
    names = ["AUTH", "ORDERS", "USERS"]
    for i, nm in enumerate(names):
        sx = sx0 + i * (sw + sgap)
        scx = sx + sw / 2
        p.append(flow_line(t, f"M{cx:.0f} {gy+38:.0f} C{cx:.0f} {gy+80:.0f} {scx:.0f} {sy-42:.0f} {scx:.0f} {sy-4:.0f}",
                           dur=f"{1.5+i*0.3:.1f}s", arrow=False))
        p.append(box(t, sx, sy, sw, sh, nm, fs=9.5))
        p.append(f'''<circle cx="{sx+sw-9:.0f}" cy="{sy+9:.0f}" r="3" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.25;1" dur="{1.6+i*0.5:.1f}s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'<text x="{cx:.0f}" y="{y+CH-20:.0f}" font-family="{MONO}" font-size="9.5" fill="{t["muted"]}" text-anchor="middle" xml:space="preserve">3 services | healthy</text>')
    return "".join(p)


def d_cloud(t, x, y):
    """Cloud above a VPC rect containing EC2/S3/RDS, with traveling dots."""
    cx = x + CW / 2
    cy = y + 66
    p = []
    p.append(f'''<path d="M{cx-34:.0f} {cy+12:.0f} a14 14 0 0 1 2-27 a19 19 0 0 1 36-6 a13 13 0 0 1 14 20 a11 11 0 0 1-6 13 Z"
 fill="{t['panel2']}" fill-opacity="0.9" stroke="url(#ag)" stroke-width="1.4"/>
<text x="{cx:.0f}" y="{cy+3:.0f}" font-family="{MONO}" font-size="9" fill="{t['a2text']}" text-anchor="middle" xml:space="preserve">AWS</text>''')
    vx, vy, vw, vh = x + 26, y + 118, CW - 52, 158
    p.append(f'<rect x="{vx:.0f}" y="{vy:.0f}" width="{vw:.0f}" height="{vh:.0f}" rx="10" fill="none" stroke="{t["sub"]}" stroke-width="1.2" stroke-dasharray="6 5" opacity="0.8"/>')
    p.append(f'<text x="{vx+10:.0f}" y="{vy+18:.0f}" font-family="{MONO}" font-size="9" fill="{t["muted"]}" xml:space="preserve">VPC 10.0.0.0/16</text>')
    p.append(flow_line(t, f"M{cx:.0f} {cy+14:.0f} V{vy-4:.0f}", dur="1.5s"))
    bw, bh = 58, 34
    ec2 = (vx + 16, vy + 32)
    s3 = (vx + vw - 16 - bw, vy + 32)
    rds = (cx - bw / 2, vy + vh - bh - 16)
    p.append(box(t, *ec2, bw, bh, "EC2", fs=9.5, label_fill=t["a2text"]))
    p.append(box(t, *s3, bw, bh, "S3", fs=9.5, label_fill=t["a2text"]))
    p.append(box(t, *rds, bw, bh, "RDS", fs=9.5, label_fill=t["a3text"]))
    l1 = f"M{ec2[0]+bw/2:.0f} {ec2[1]+bh:.0f} L{rds[0]+10:.0f} {rds[1]:.0f}"
    l2 = f"M{s3[0]+bw/2:.0f} {s3[1]+bh:.0f} L{rds[0]+bw-10:.0f} {rds[1]:.0f}"
    for i, d in enumerate((l1, l2)):
        p.append(f'<path d="{d}" fill="none" stroke="{t["border"]}" stroke-width="1.3"/>')
        p.append(f'''<circle r="3" fill="{t['a2']}" filter="url(#fg)">
  <animateMotion path="{d[1:]}" dur="{2.2+i*0.6:.1f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.2;1;0.2" dur="{2.2+i*0.6:.1f}s" repeatCount="indefinite"/>
</circle>''')
    return "".join(p)


def d_cicd(t, x, y):
    """COMMIT/BUILD/TEST/DEPLOY chips, traveling dot, sequenced glow."""
    p = []
    stages = ["COMMIT", "BUILD", "TEST", "DEPLOY"]
    chw, chh, chgap = 51, 24, 8
    total = 4 * chw + 3 * chgap
    px0 = x + (CW - total) / 2
    pyc = y + 128
    cycle = 4.8
    p.append(f'<text x="{x+CW/2:.0f}" y="{y+72:.0f}" font-family="{MONO}" font-size="10" fill="{t["muted"]}" text-anchor="middle" xml:space="preserve">$ pipeline run --prod</text>')
    for i, st in enumerate(stages):
        sx = px0 + i * (chw + chgap)
        t0, t1 = i * 0.25, (i + 1) * 0.25
        if i == 0:
            kt, vals = f"0;{t1:.2f};{t1+0.04:.2f};1", "1;1;0.25;0.25"
        elif i == len(stages) - 1:
            kt = f"0;{t0:.2f};{t0+0.04:.2f};1"
            vals = "0.25;0.25;1;1"
        else:
            kt = f"0;{t0:.2f};{t0+0.04:.2f};{t1:.2f};{t1+0.04:.2f};1"
            vals = "0.25;0.25;1;1;0.25;0.25"
        p.append(f'''<rect x="{sx:.0f}" y="{pyc-chh/2:.0f}" width="{chw}" height="{chh}" rx="12" fill="{t['pill_fill']}" fill-opacity="0.9" stroke="url(#ag)" stroke-width="1.2">
  <animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{cycle}s" repeatCount="indefinite"/>
</rect>
<text x="{sx+chw/2:.0f}" y="{pyc+3:.0f}" font-family="{MONO}" font-size="8.5" fill="{t['text']}" text-anchor="middle" xml:space="preserve">{st}</text>''')
        if i < 3:
            axc = sx + chw + chgap / 2
            p.append(f'<path d="M{axc-3:.0f} {pyc-4:.0f} L{axc+2:.0f} {pyc:.0f} L{axc-3:.0f} {pyc+4:.0f}" fill="none" stroke="{t["sub"]}" stroke-width="1.3"/>')
    dot_path = f"M{px0+6:.0f} {pyc+chh/2+14:.0f} H{px0+total-6:.0f}"
    p.append(f'<path d="{dot_path}" stroke="{t["border"]}" stroke-width="1.2"/>')
    p.append(f'''<circle r="4" fill="url(#ag)" filter="url(#fg)">
  <animateMotion path="{dot_path[1:]}" dur="{cycle}s" repeatCount="indefinite"/>
</circle>''')
    ly0 = pyc + 66
    logs = [("build: passed  (42s)", "sub"), ("tests: 218 ok", "sub"), ("deploy: success", "a3text")]
    for i, (line, col) in enumerate(logs):
        c = t[col] if col != "sub" else t["sub"]
        p.append(f'''<text x="{px0+4:.0f}" y="{ly0+i*20:.0f}" font-family="{MONO}" font-size="9.5" fill="{c}" xml:space="preserve" opacity="0"><animate attributeName="opacity" values="0;1" begin="{1.2+i*0.5:.1f}s" dur="0.4s" fill="freeze"/>&gt; {esc(line)}</text>''')
    return "".join(p)


def d_monitoring(t, x, y):
    """Self-drawing line chart, blinking alert dot, uptime caption."""
    gx, gy, gw, gh = x + 26, y + 62, CW - 52, 150
    p = [f'<rect x="{gx:.0f}" y="{gy:.0f}" width="{gw:.0f}" height="{gh:.0f}" rx="8" fill="{t["panel2"]}" fill-opacity="0.55" stroke="{t["border"]}" stroke-width="1"/>']
    for i in range(1, 4):
        yy = gy + gh * i / 4
        p.append(f'<path d="M{gx+8:.0f} {yy:.0f} h{gw-16:.0f}" stroke="{t["border"]}" stroke-width="0.8" opacity="0.7"/>')
    pts = [(0.00, 0.72), (0.12, 0.55), (0.24, 0.62), (0.36, 0.38), (0.48, 0.50),
           (0.60, 0.28), (0.72, 0.42), (0.84, 0.18), (1.00, 0.30)]
    coords = [(gx + 12 + px * (gw - 24), gy + 14 + py * (gh - 34)) for px, py in pts]
    dpath = "M" + " L".join(f"{cx:.0f} {cy:.0f}" for cx, cy in coords)
    length = sum(((coords[i+1][0]-coords[i][0])**2 + (coords[i+1][1]-coords[i][1])**2) ** 0.5
                 for i in range(len(coords) - 1))
    L = int(length + 10)
    p.append(f'''<path d="{dpath}" fill="none" stroke="url(#ag)" stroke-width="2" stroke-linejoin="round" stroke-dasharray="{L}" stroke-dashoffset="{L}" filter="url(#fg)">
  <animate attributeName="stroke-dashoffset" from="{L}" to="0" begin="1s" dur="2.6s" fill="freeze"/>
</path>''')
    ax, ay = coords[7]
    p.append(f'''<circle cx="{ax:.0f}" cy="{ay:.0f}" r="4" fill="{t['a2']}" filter="url(#fg)" opacity="0">
  <animate attributeName="opacity" values="0;0" dur="3.4s" fill="freeze"/>
  <animate attributeName="opacity" values="1;0.15;1" begin="3.4s" dur="1.4s" repeatCount="indefinite"/>
</circle>
<circle cx="{ax:.0f}" cy="{ay:.0f}" r="4" fill="none" stroke="{t['a2']}" opacity="0">
  <animate attributeName="r" values="4;12" begin="3.4s" dur="1.4s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.8;0" begin="3.4s" dur="1.4s" repeatCount="indefinite"/>
</circle>''')
    cy2 = gy + gh + 34
    p.append(f'''<text x="{gx:.0f}" y="{cy2:.0f}" font-family="{MONO}" font-size="10.5" fill="{t['a3text']}" xml:space="preserve">99.9% uptime</text>
<text x="{gx+gw:.0f}" y="{cy2:.0f}" font-family="{MONO}" font-size="9.5" fill="{t['muted']}" text-anchor="end" xml:space="preserve">p95 latency: 84ms</text>''')
    return "".join(p)


def d_infrastructure(t, x, y):
    """Server rack with blinking LEDs + NAS box."""
    rx0, ry0, rw, rh = x + 30, y + 62, 118, 176
    p = [f'<rect x="{rx0:.0f}" y="{ry0:.0f}" width="{rw}" height="{rh}" rx="8" fill="{t["panel2"]}" fill-opacity="0.9" stroke="{t["border"]}" stroke-width="1.3"/>']
    for i in range(4):
        sy = ry0 + 12 + i * 40
        p.append(f'<rect x="{rx0+10:.0f}" y="{sy:.0f}" width="{rw-20}" height="30" rx="4" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1"/>')
        for k in range(3):
            lx = rx0 + 22 + k * 12
            col = t["a3"] if (i + k) % 3 else t["a2"]
            p.append(f'''<circle cx="{lx:.0f}" cy="{sy+9:.0f}" r="2.4" fill="{col}">
  <animate attributeName="opacity" values="1;0.15;1" dur="{0.9 + (i*3+k)*0.23:.2f}s" repeatCount="indefinite"/>
</circle>''')
        p.append(f'<path d="M{rx0+64:.0f} {sy+20:.0f} h{rw-84}" stroke="{t["border"]}" stroke-width="1"/>')
        p.append(f'<path d="M{rx0+64:.0f} {sy+24:.0f} h{rw-84}" stroke="{t["border"]}" stroke-width="1"/>')
    p.append(f'<text x="{rx0+rw/2:.0f}" y="{ry0+rh+20:.0f}" font-family="{MONO}" font-size="9.5" fill="{t["sub"]}" text-anchor="middle" xml:space="preserve">RACK-01</text>')
    nx, ny, nw, nh = rx0 + rw + 24, ry0 + 54, 62, 68
    p.append(f'<rect x="{nx:.0f}" y="{ny:.0f}" width="{nw}" height="{nh}" rx="6" fill="{t["panel2"]}" fill-opacity="0.9" stroke="{t["border"]}" stroke-width="1.3"/>')
    for i in range(2):
        p.append(f'<rect x="{nx+8:.0f}" y="{ny+10+i*22:.0f}" width="{nw-16}" height="14" rx="3" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1"/>')
        p.append(f'''<circle cx="{nx+nw-14:.0f}" cy="{ny+17+i*22:.0f}" r="2" fill="{t['a3']}">
  <animate attributeName="opacity" values="1;0.2;1" dur="{1.3+i*0.7:.1f}s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'<text x="{nx+nw/2:.0f}" y="{ny+nh+18:.0f}" font-family="{MONO}" font-size="9.5" fill="{t["sub"]}" text-anchor="middle" xml:space="preserve">NAS</text>')
    p.append(flow_line(t, f"M{rx0+rw:.0f} {ry0+88:.0f} H{nx:.0f}", dur="1.8s", arrow=False))
    return "".join(p)


def d_networking(t, x, y):
    """Firewall -> L3 switch -> 3 VLANs with packet dots."""
    cx = x + CW / 2
    fy = y + 56
    p = [box(t, cx - 56, fy, 112, 34, "FIREWALL", fs=9.5, label_fill=t["a2text"])]
    for i in range(3):
        p.append(f'<path d="M{cx-56:.0f} {fy+9+i*8:.0f} h112" stroke="{t["border"]}" stroke-width="0.9" opacity="0.9"/>')
    p.append(f'<rect x="{cx-56:.0f}" y="{fy:.0f}" width="112" height="34" rx="8" fill="none" stroke="url(#ag)" stroke-width="1.2" opacity="0.7"/>')
    p.append(f'<text x="{cx:.0f}" y="{fy+21:.0f}" font-family="{MONO}" font-size="9.5" fill="{t["a2text"]}" text-anchor="middle" xml:space="preserve">FIREWALL</text>')
    swy = fy + 78
    p.append(box(t, cx - 62, swy, 124, 30, "L3 SWITCH", fs=9.5))
    vy = swy + 84
    vw, vh, vgap = 64, 38, 14
    total = 3 * vw + 2 * vgap
    vx0 = cx - total / 2
    links = [f"M{cx:.0f} {fy+34:.0f} V{swy-2:.0f}"]
    for i in range(3):
        vx = vx0 + i * (vw + vgap)
        vcx = vx + vw / 2
        links.append(f"M{cx:.0f} {swy+30:.0f} C{cx:.0f} {swy+58:.0f} {vcx:.0f} {vy-30:.0f} {vcx:.0f} {vy-2:.0f}")
        p.append(box(t, vx, vy, vw, vh, f"VLAN {10*(i+1)}", fs=8.5, label_fill=t["a3text"]))
    for i, d in enumerate(links):
        p.append(f'<path d="{d}" fill="none" stroke="{t["border"]}" stroke-width="1.3"/>')
        p.append(f'''<circle r="2.6" fill="{t['a2']}" filter="url(#fg)">
  <animateMotion path="{d[1:]}" dur="{1.6+i*0.4:.1f}s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.15;1;0.15" dur="{1.6+i*0.4:.1f}s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/>
</circle>''')
    return "".join(p)


def d_security(t, x, y):
    """Shield with glow pulse, lock glyph, vertical scanning line."""
    cx = x + CW / 2
    sy = y + 64
    sw2, sh2 = 62, 132
    shield = (f"M{cx:.0f} {sy:.0f} L{cx+sw2:.0f} {sy+24:.0f} V{sy+70:.0f} "
              f"C{cx+sw2:.0f} {sy+108:.0f} {cx+30:.0f} {sy+124:.0f} {cx:.0f} {sy+sh2:.0f} "
              f"C{cx-30:.0f} {sy+124:.0f} {cx-sw2:.0f} {sy+108:.0f} {cx-sw2:.0f} {sy+70:.0f} "
              f"V{sy+24:.0f} Z")
    p = []
    p.append(f'''<path d="{shield}" fill="{t['panel2']}" fill-opacity="0.6" stroke="url(#ag)" stroke-width="2" filter="url(#fg)">
  <animate attributeName="stroke-width" values="1.6;2.6;1.6" dur="3.6s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.75;1;0.75" dur="3.6s" repeatCount="indefinite"/>
</path>''')
    lx, ly = cx, sy + 66
    p.append(f'''<g stroke="{t['text']}" stroke-width="2" fill="none">
<path d="M{lx-9:.0f} {ly:.0f} v-8 a9 9 0 0 1 18 0 v8"/>
<rect x="{lx-14:.0f}" y="{ly:.0f}" width="28" height="22" rx="4" fill="{t['panel']}"/>
</g>
<circle cx="{lx:.0f}" cy="{ly+10:.0f}" r="3" fill="{t['a2']}">
  <animate attributeName="opacity" values="1;0.4;1" dur="2.4s" repeatCount="indefinite"/>
</circle>''')
    p.append(f'''<clipPath id="shc"><path d="{shield}"/></clipPath>
<g clip-path="url(#shc)"><rect x="{cx-sw2:.0f}" y="{sy-8:.0f}" width="{2*sw2}" height="7" fill="{t['a2']}" opacity="0.35">
  <animateTransform attributeName="transform" type="translate" values="0 0;0 {sh2+14};0 0" dur="4.2s" repeatCount="indefinite"/>
</rect></g>''')
    p.append(f'''<text x="{cx:.0f}" y="{sy+sh2+34:.0f}" font-family="{MONO}" font-size="9.5" fill="{t['muted']}" text-anchor="middle" xml:space="preserve">zero trust | least privilege</text>
<text x="{cx:.0f}" y="{sy+sh2+52:.0f}" font-family="{MONO}" font-size="9.5" fill="{t['a3text']}" text-anchor="middle" xml:space="preserve">threats blocked: 100%</text>''')
    return "".join(p)


CARDS = [
    ("ENTERPRISE ARCHITECTURE", d_enterprise),
    ("MICROSERVICES", d_microservices),
    ("CLOUD ARCHITECTURE", d_cloud),
    ("CI/CD PIPELINE", d_cicd),
    ("MONITORING", d_monitoring),
    ("INFRASTRUCTURE", d_infrastructure),
    ("NETWORKING", d_networking),
    ("SECURITY", d_security),
]


def grid(t):
    p = []
    for i, (label, fn) in enumerate(CARDS):
        col, row = i % COLS, i // COLS
        x = MARGIN + col * (CW + GAP)
        y = GRID_TOP + row * (CH + GAP)
        begin = 0.2 + i * 0.14
        p.append(f'''<g opacity="0">
<animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" values="0 16;0 0" begin="{begin:.2f}s" dur="0.5s" fill="freeze"/>
{card_shell(t, x, y, label, i + 1)}
{fn(t, x, y)}
</g>''')
    return "".join(p)


def build(theme_key):
    t = THEMES[theme_key]
    title = "Aaditya Padiya — Architecture &amp; Infrastructure Showcase"
    desc = (f"Animated {t['desc']}-theme board of eight architecture diagrams by Aaditya Padiya: "
            "enterprise tiers, microservices, cloud VPC, CI/CD pipeline, monitoring, "
            "server infrastructure, networking with VLANs, and security shield.")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
{defs(t)}
{background(t)}
{header(t)}
{grid(t)}
</svg>'''


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "..")
    for key in ("dark", "light"):
        out = os.path.join(root, "assets", f"architecture-{key}.svg")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(key))
        print(f"architecture-{key}.svg: {os.path.getsize(out)} bytes")
