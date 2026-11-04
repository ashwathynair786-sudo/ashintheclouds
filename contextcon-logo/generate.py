import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")  # Geist Mono + Space Grotesk (SIL OFL)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
F = lambda n: TTFont(os.path.join(FD, n))
MONO_B, MONO_M = F("geist-mono-latin-700-normal.woff"), F("geist-mono-latin-500-normal.woff")
GROT_B = F("space-grotesk-latin-700-normal.woff")

def text_path(font, text, size, x, y, tracking=0.0):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm; s = size / upm
    pen = SVGPathPen(gs); cx = 0.0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + cx * s, y)))
        cx += hmtx[g][0] + tracking * upm
    return pen.getCommands(), (cx - tracking * upm) * s

def cap(font, size): return font["OS/2"].sCapHeight * size / font["head"].unitsPerEm
def xh(font, size): return font["OS/2"].sxHeight * size / font["head"].unitsPerEm

CYAN, VIOLET, LIME = "#00E5FF", "#7C4DFF", "#B6FF3B"
THEMES = {
  "dark":  dict(bg="#07070D", ink="#F4F4F8", muted="#8A8AA3", dim="#FFFFFF", dimop=.08, core=LIME, glow=True, cyan=CYAN),
  "light": dict(bg="#F6F6F9", ink="#07070D", muted="#5E5E78", dim="#07070D", dimop=.08, core="#07070D", glow=False, cyan="#00A3D9"),
}

def defs(u, t):
    glow = (f'<filter id="glow{u}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (f'<defs><linearGradient id="g{u}" x1="0" y1="0" x2="120" y2="120" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{t["cyan"]}"/></linearGradient>'
            f'<linearGradient id="h{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{t["cyan"]}"/></linearGradient>'
            f'{glow}</defs>')

def G(t, u): return f' filter="url(#glow{u})"' if t["glow"] else ""

# ---------------- marks (all drawn in a 120x120 box) ----------------
def mark_grid(t, u):
    """MEMORY GRID: a 5x5 matrix of memory cells; the lit cells spell a C,
    the core cell glows lime: shared memory every agent writes to."""
    C = {(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,1),(4,2),(4,3),(4,4)}
    out = [f'<g>']
    lit = []
    for r in range(5):
        for c in range(5):
            x, y = c * 25, r * 25
            if (r, c) in C:
                lit.append(f'<rect x="{x}" y="{y}" width="20" height="20" rx="3"/>')
            elif (r, c) == (2, 2):
                pass
            else:
                out.append(f'<rect x="{x}" y="{y}" width="20" height="20" rx="3" fill="{t["dim"]}" fill-opacity="{t["dimop"]}"/>')
    out.append(f'<g fill="url(#g{u})">' + "".join(lit) + '</g>')
    out.append(f'<rect x="50" y="50" width="20" height="20" rx="3" fill="{t["core"]}"{G(t,u)}/>')
    # write-path: core -> open side of the C
    out.append(f'<rect x="75" y="57" width="45" height="6" rx="3" fill="{t["core"]}" opacity=".9"/>')
    return "".join(out) + "</g>"

def mark_term(t, u):
    """CONTEXT WINDOW: two bold brackets hold a live block cursor: an agent session that never starts from zero."""
    l = "M42 0 H14 Q0 0 0 14 V106 Q0 120 14 120 H42 V101 H20 V19 H42 Z"
    r = "M78 0 H106 Q120 0 120 14 V106 Q120 120 106 120 H78 V101 H100 V19 H78 Z"
    return (f'<path d="{l}" fill="url(#g{u})"/><path d="{r}" fill="url(#g{u})"/>'
            f'<rect x="46" y="32" width="28" height="56" rx="3" fill="{t["core"]}"{G(t,u)}/>')

def mark_circuit(t, u):
    """CIRCUIT: a chamfered C traced like a PCB bus; traces feed a central core chip."""
    outer = "M104 8 H34 L8 34 V86 L34 112 H104"
    inner = "M86 32 H46 L32 46 V74 L46 88 H86"
    s = (f'<path d="{outer}" fill="none" stroke="url(#g{u})" stroke-width="12" stroke-linejoin="miter" stroke-linecap="butt"/>'
         f'<path d="{inner}" fill="none" stroke="url(#g{u})" stroke-width="6" stroke-linejoin="miter" stroke-linecap="butt" opacity=".75"/>')
    for (x, y, r) in [(104, 8, 7), (104, 112, 7), (86, 32, 5), (86, 88, 5)]:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["bg"]}" stroke="{t["cyan"]}" stroke-width="3"/>'
    s += f'<path d="M60 60 H112" stroke="{t["core"]}" stroke-width="3"/>'
    s += f'<circle cx="114" cy="60" r="5" fill="{t["bg"]}" stroke="{t["core"]}" stroke-width="3"/>'
    s += f'<rect x="50" y="50" width="20" height="20" rx="2" transform="rotate(45 60 60)" fill="{t["core"]}"{G(t,u)}/>'
    return s

# ---------------- wordmarks ----------------
def wm_grid(t, u, x, base, size):
    d1, w1 = text_path(GROT_B, "CONTEXT", size, x, base, 0.01)
    d2, w2 = text_path(GROT_B, "CON", size, x + w1 + .01*size, base, 0.01)
    return f'<path d="{d1}" fill="{t["ink"]}"/><path d="{d2}" fill="url(#h{u})"/>', w1 + w2 + .01*size, cap(GROT_B, size)

def wm_term(t, u, x, base, size):
    d1, w1 = text_path(MONO_B, "context", size, x, base, -0.02)
    d2, w2 = text_path(MONO_B, "con", size, x + w1 - .02*size, base, -0.02)
    cw = size * 0.5; cx = x + w1 + w2 + size * 0.06
    xht = xh(MONO_B, size)
    cur = f'<rect x="{cx:.1f}" y="{base - cap(MONO_B,size):.1f}" width="{cw*0.62:.1f}" height="{cap(MONO_B,size):.1f}" fill="{t["core"]}"{G(t,u)}/>'
    return f'<path d="{d1}" fill="{t["ink"]}"/><path d="{d2}" fill="url(#h{u})"/>' + cur, cx + cw*0.62 - x, cap(MONO_B, size)

def wm_circuit(t, u, x, base, size):
    d1, w1 = text_path(GROT_B, "Context", size, x, base, -0.03)
    d2, w2 = text_path(GROT_B, "Con", size, x + w1 - .03*size, base, -0.03)
    return f'<path d="{d1}" fill="{t["ink"]}"/><path d="{d2}" fill="url(#h{u})"/>', w1 + w2 - .03*size, cap(GROT_B, size)

def tag(t, x, base, size, parts, track):
    """parts: list of (text, color_key or hex)."""
    s = ""; cx = x
    for txt, col in parts:
        d, w = text_path(MONO_M, txt, size, cx, base, track)
        s += f'<path d="{d}" fill="{t.get(col, col)}"/>'; cx += w + track * size
    return s, cx - x

TAGS = {
  "grid":    ([("// ", "core"), ("REMEMBER_EVERYTHING", "muted")], 0.08),
  "term":    ([("$ ", "core"), ("remember --everything", "muted")], 0.0),
  "circuit": ([("[ ", "core"), ("REMEMBER EVERYTHING", "muted"), (" ]", "core")], 0.14),
}
MARKS = dict(grid=mark_grid, term=mark_term, circuit=mark_circuit)
WMS = dict(grid=wm_grid, term=wm_term, circuit=wm_circuit)

def svg(w, h, body, t, u, bg):
    rect = f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="ContextCon: Remember Everything"><title>ContextCon: Remember Everything</title>{defs(u,t)}{rect}{body}</svg>\n')

def horizontal(c, th, bg=True):
    t = THEMES[th]; u = f"{c}h{th}{int(bg)}"
    pad, M, size, ts = 56, 128, 84, 22
    wm0, ww, capH = WMS[c](t, u, 0, 0, size)
    block = capH + 26 + cap(MONO_M, ts)
    H = M + pad * 2; top = (H - block) / 2
    tx = pad + M + 40
    wm, ww, _ = WMS[c](t, u, tx, top + capH, size)
    tg, tw = tag(t, tx + 2, top + block, ts, *TAGS[c])
    W = round(tx + max(ww, tw) + pad)
    body = f'<g transform="translate({pad} {pad}) scale({M/120})">{MARKS[c](t,u)}</g>' + wm + tg
    return svg(W, H, body, t, u, bg)

def stacked(c, th, bg=True):
    t = THEMES[th]; u = f"{c}s{th}{int(bg)}"
    pad, M, size, ts = 64, 168, 92, 24
    _, ww, capH = WMS[c](t, u, 0, 0, size)
    _, tw = tag(t, 0, 0, ts, *TAGS[c])
    W = round(max(ww, tw) + pad * 2)
    base = pad + M + 56 + capH
    wm, _, _ = WMS[c](t, u, (W - ww) / 2, base, size)
    tb = base + 30 + cap(MONO_M, ts)
    tg, _ = tag(t, (W - tw) / 2, tb, ts, *TAGS[c])
    H = round(tb + pad)
    body = f'<g transform="translate({(W-M)/2} {pad}) scale({M/120})">{MARKS[c](t,u)}</g>' + wm + tg
    return svg(W, H, body, t, u, bg)

def icon(c, th):
    t = THEMES[th]; u = f"{c}i{th}"; S, inner = 512, 300
    o = (S - inner) / 2
    body = (f'<rect width="{S}" height="{S}" rx="112" fill="{t["bg"]}"/>'
            f'<g transform="translate({o} {o}) scale({inner/120})">{MARKS[c](t,u)}</g>')
    return svg(S, S, body, t, u, False)

if __name__ == "__main__":
    concepts = sys.argv[2].split(",") if len(sys.argv) > 2 else list(MARKS)
    for c in concepts:
        for th in THEMES:
            for bg in (True, False):
                sfx = "" if bg else "-transparent"
                open(os.path.join(OUT, f"contextcon-{c}-horizontal-{th}{sfx}.svg"), "w").write(horizontal(c, th, bg))
                open(os.path.join(OUT, f"contextcon-{c}-stacked-{th}{sfx}.svg"), "w").write(stacked(c, th, bg))
            open(os.path.join(OUT, f"contextcon-{c}-icon-{th}.svg"), "w").write(icon(c, th))
    print("written to", OUT)
