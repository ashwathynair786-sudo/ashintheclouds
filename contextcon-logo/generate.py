import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

REPO = "/home/user/ashintheclouds"
OUT = os.path.join(REPO, "contextcon-logo")
DISPLAY = TTFont(os.path.join(REPO, "BricolageGrotesque-ExtraBold.ttf"))
LABEL = TTFont(os.path.join(REPO, "Geist-SemiBold.ttf"))

def text_path(font, text, size, x, y, tracking=0.0):
    """Return (svg path d, advance width) for text outlined at baseline (x, y)."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm; s = size / upm
    # simple pair kerning from kern table if present
    kern = {}
    if "kern" in font:
        for st in font["kern"].kernTables:
            kern.update(st.kernTable)
    pen = SVGPathPen(gs); cx = 0.0; prev = None
    for ch in text:
        g = cmap[ord(ch)]
        if prev and (prev, g) in kern: cx += kern[(prev, g)]
        tp = TransformPen(pen, (s, 0, 0, -s, x + cx * s, y))
        gs[g].draw(tp)
        cx += hmtx[g][0] + tracking * upm
        prev = g
    width = (cx - tracking * upm) * s
    return pen.getCommands(), width

def cap_height(font, size):
    os2 = font["OS/2"]; return os2.sCapHeight * size / font["head"].unitsPerEm

# ---------- palette ----------
VIOLET, CYAN, LIME = "#8B5CF6", "#22D3EE", "#C8FF3D"
THEMES = {
    "dark":  dict(bg="#0B0A1F", ink="#FFFFFF", muted="#A9A6C9", core=LIME, ring="#FFFFFF"),
    "light": dict(bg="#FFFFFF", ink="#0B0A1F", muted="#5B5878", core="#0B0A1F", ring="#0B0A1F"),
}

def defs(uid):
    return f'''<defs>
  <linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/>
  </linearGradient>
  <linearGradient id="t{uid}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/>
  </linearGradient>
</defs>'''

def arc(cx, cy, r, gap_deg):
    """Open arc ('C') with its mouth facing right, gap of +/-gap_deg around 0deg."""
    a0, a1 = math.radians(gap_deg), math.radians(360 - gap_deg)
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return f"M{x0:.2f} {y0:.2f} A{r} {r} 0 1 1 {x1:.2f} {y1:.2f}", (x0, y0), (x1, y1)

def mark(t, uid, ox=0, oy=0, scale=1.0):
    """The ContextCon mark, drawn in a 120x120 box.
    Three nested memory rings (the C of Context/Con) open toward an incoming agent node;
    a link carries that agent's learning to the shared core every ring wraps around."""
    cx, cy = 56, 60
    parts = []
    rings = [(50, 40, 9), (35, 52, 9), (20, 72, 9)]
    for r, gap, w in rings:
        d, p0, p1 = arc(cx, cy, r, gap)
        parts.append(f'<path d="{d}" fill="none" stroke="url(#g{uid})" stroke-width="{w}" stroke-linecap="round"/>')
    # knowledge link from incoming agent node to core
    nx = cx + 58
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{nx-7}" y2="{cy}" stroke="{t["ring"]}" stroke-width="4" stroke-linecap="round"/>')
    parts.append(f'<circle cx="{nx}" cy="{cy}" r="7" fill="none" stroke="{t["ring"]}" stroke-width="4"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{t["core"]}"/>')
    return f'<g transform="translate({ox} {oy}) scale({scale})">' + "".join(parts) + "</g>"

def svg(w, h, body, t, uid, bg=True, title="ContextCon: Remember Everything"):
    rect = f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{defs(uid)}{rect}{body}</svg>\n')

def wordmark(t, uid, x, baseline, size):
    d1, w1 = text_path(DISPLAY, "Context", size, x, baseline, tracking=-0.025)
    d2, w2 = text_path(DISPLAY, "Con", size, x + w1 - 0.01*size, baseline, tracking=-0.025)
    body = f'<path d="{d1}" fill="{t["ink"]}"/><path d="{d2}" fill="url(#t{uid})"/>'
    return body, w1 + w2 - 0.01*size

def tagline(t, x, baseline, size, span, align="left"):
    """Tracked tagline plus a 'trace' line ending in a node, filling `span` px."""
    text = "REMEMBER EVERYTHING"; track = 0.22
    _, w = text_path(LABEL, text, size, 0, 0, tracking=track)
    capH = cap_height(LABEL, size); my = baseline - capH / 2
    node_r = size * 0.22; gap = size * 0.7; sw = max(1.5, size * 0.09)
    def trace(x0, x1, node_at_end=True):
        nx = x1 - node_r if node_at_end else x0 + node_r
        lx0, lx1 = (x0, nx - node_r) if node_at_end else (nx + node_r, x1)
        return (f'<line x1="{lx0:.2f}" y1="{my:.2f}" x2="{lx1:.2f}" y2="{my:.2f}" stroke="{t["muted"]}" stroke-width="{sw:.2f}" stroke-linecap="round" opacity=".55"/>'
                f'<circle cx="{nx:.2f}" cy="{my:.2f}" r="{node_r:.2f}" fill="none" stroke="{t["muted"]}" stroke-width="{sw:.2f}" opacity=".9"/>')
    if align == "left":
        d, _ = text_path(LABEL, text, size, x, baseline, tracking=track)
        return f'<path d="{d}" fill="{t["muted"]}"/>' + trace(x + w + gap, x + span)
    tx = x + (span - w) / 2
    d, _ = text_path(LABEL, text, size, tx, baseline, tracking=track)
    return trace(x, tx - gap, node_at_end=False) + f'<path d="{d}" fill="{t["muted"]}"/>' + trace(tx + w + gap, x + span)

def horizontal(theme, bg=True):
    t = THEMES[theme]; uid = f"h{theme}{int(bg)}"
    pad = 48; mark_size = 152; size = 96
    capH = cap_height(DISPLAY, size)
    tag_size = 20
    gap_text = 22
    block_h = capH + gap_text + cap_height(LABEL, tag_size)
    H = mark_size + pad * 2
    top = (H - block_h) / 2
    tx = pad + mark_size + 34
    wm, ww = wordmark(t, uid, tx, top + capH, size)
    tg = tagline(t, tx + 4, top + block_h, tag_size, ww - 6)
    W = tx + ww + pad
    body = mark(t, uid, pad, pad, mark_size / 120) + wm + tg
    return svg(round(W), H, body, t, uid, bg)

def stacked(theme, bg=True):
    t = THEMES[theme]; uid = f"s{theme}{int(bg)}"
    pad = 64; mark_size = 200; size = 104; tag_size = 22
    _, ww = wordmark(t, uid, 0, 0, size)
    W = round(ww + pad * 2)
    capH = cap_height(DISPLAY, size)
    my = pad
    base = my + mark_size + 48 + capH
    tx = (W - ww) / 2
    wm, _ = wordmark(t, uid, tx, base, size)
    tag_base = base + 30 + cap_height(LABEL, tag_size)
    tg = tagline(t, tx + 4, tag_base, tag_size, ww - 6, align="center")
    H = round(tag_base + pad)
    body = mark(t, uid, (W - mark_size) / 2 - 2.25 * mark_size / 120, my, mark_size / 120) + wm + tg
    return svg(W, H, body, t, uid, bg)

def icon(theme, bg=True):
    t = THEMES[theme]; uid = f"i{theme}{int(bg)}"
    S = 512; inner = 360
    body = mark(t, uid, (S - inner) / 2 - 2.25 * inner / 120, (S - inner) / 2, inner / 120)
    if bg:
        body = f'<rect width="{S}" height="{S}" rx="112" fill="{t["bg"]}"/>' + body
    return svg(S, S, body, t, uid, bg=False)

files = {}
for th in THEMES:
    files[f"contextcon-logo-horizontal-{th}.svg"] = horizontal(th)
    files[f"contextcon-logo-horizontal-{th}-transparent.svg"] = horizontal(th, bg=False)
    files[f"contextcon-logo-stacked-{th}.svg"] = stacked(th)
    files[f"contextcon-logo-stacked-{th}-transparent.svg"] = stacked(th, bg=False)
    files[f"contextcon-icon-{th}.svg"] = icon(th)
for name, content in files.items():
    open(os.path.join(OUT, name), "w").write(content)
print("\n".join(files))
