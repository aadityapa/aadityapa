"""Conservative size optimizer for the hero SVGs. SMIL-safe by construction:
never touches animate/animateTransform/animateMotion structure, only hoists
inheritable presentation attributes, collapses inter-element whitespace
outside <text>, and trims trailing zeros in numeric timing values.

Reads  .build/opt_{theme}.svg (pristine copies of assets/)
Writes .build/opt_{theme}.svg in place.
"""
import re
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
ET.register_namespace("", SVG)

FONT_STACK = "ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace"
ANIM = {f"{{{SVG}}}{t}" for t in ("animate", "animateTransform", "animateMotion")}
TEXTY = {f"{{{SVG}}}{t}" for t in ("text", "tspan", "title", "desc")}


def ln(tag):
    return tag.rsplit("}", 1)[-1]


def trim_num(s):
    """15.0 -> 15, 0.5000 -> 0.5, 0.0000 -> 0; leaves ints/other alone."""
    if "." in s:
        s = s.rstrip("0").rstrip(".")
        if s in ("", "-"):
            s = "0"
    return s


def trim_list(v):
    return ";".join(trim_num(x.strip()) for x in v.split(";"))


def trim_clock(v):
    m = re.fullmatch(r"([0-9.]+)s", v.strip())
    return trim_num(m.group(1)) + "s" if m else v


def optimize(path):
    tree = ET.parse(path)
    root = tree.getroot()
    texts = [el for el in root.iter() if el.tag == f"{{{SVG}}}text"]

    # 1. Hoist font-family to the root (inherited property). Every text that
    #    sets it uses the same stack. xml:space must STAY per-element: Chrome
    #    does not inherit it into <text>, and collapsing spaces breaks the
    #    ASCII avatar centering — only drop it where whitespace is trivial.
    assert all(el.get("font-family") in (None, FONT_STACK) for el in texts)
    root.set("font-family", FONT_STACK)
    for el in texts:
        el.attrib.pop("font-family", None)
        if el.get(XML_SPACE) == "preserve":
            content = "".join(el.itertext())
            if not re.search(r"^\s|\s$|\s\s", content):
                del el.attrib[XML_SPACE]

    # 2. ASCII-avatar block: hoist font-size/text-anchor/fill shared by the 18
    #    display lines onto their filtered <g>, and by the 18 mask lines onto
    #    the <mask>. Both are inherited by content.
    for holder in root.iter():
        kids = [c for c in holder if c.tag == f"{{{SVG}}}text"
                and c.get("font-size") == "10.5"]
        if len(kids) < 10:
            continue
        for attr in ("font-size", "text-anchor", "fill"):
            vals = {c.get(attr) for c in kids}
            if len(vals) == 1 and None not in vals:
                holder.set(attr, vals.pop())
                for c in kids:
                    del c.attrib[attr]

    # 3. Trim trailing zeros in SMIL numeric lists and clock values.
    for el in root.iter():
        if el.tag in ANIM:
            for attr in ("values", "keyTimes"):
                v = el.get(attr)
                if v and re.fullmatch(r"[0-9 .;\-]+", v):
                    el.set(attr, trim_list(v))
            for attr in ("begin", "dur"):
                v = el.get(attr)
                if v:
                    el.set(attr, trim_clock(v))

    # 4. Collapse whitespace-only text/tails outside of <text> content.
    parent = {c: p for p in root.iter() for c in p}

    def inside_text(el):
        cur = el
        while cur is not None:
            if cur.tag in TEXTY:
                return True
            cur = parent.get(cur)
        return False

    for el in root.iter():
        if el.tag in TEXTY or inside_text(el):
            continue
        if el.text is not None and not el.text.strip():
            el.text = None
        for c in el:
            if c.tail is not None and not c.tail.strip() and c.tag not in TEXTY:
                c.tail = None
            elif c.tag in TEXTY and c.tail is not None and not c.tail.strip():
                c.tail = None

    out = ET.tostring(root, encoding="unicode")
    n_anim = len(re.findall(r"<animate(?:Transform|Motion)?[\s>]", out))
    assert n_anim == 183, f"animation count {n_anim} != 183 (v12 hero + 29-row portrait)"
    open(path, "w", encoding="utf-8", newline="\n").write(out)
    print(path, "->", len(out.encode("utf-8")), "bytes, animations:", n_anim)


for theme in ("dark", "light"):
    optimize(f".build/opt_{theme}.svg")
