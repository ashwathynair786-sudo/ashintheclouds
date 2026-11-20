import math, random, pathlib
OUT = pathlib.Path(__file__).parent
REPO = OUT.parent
wm_dark = (REPO / "Logo Dark.svg").read_text()
wm_light = (REPO / "Logo-Light.svg").read_text()

def contours(cx, cy, n=14, base=60, step=46, seed=3, focal=2, cls_focal="lime"):
    rnd = random.Random(seed)
    harm = [(k, rnd.uniform(0.04, 0.11), rnd.uniform(0, 6.28)) for k in (2, 3, 5)]
    out = []
    for i in range(n):
        r0 = base + i * step
        pts = []
        for j in range(120):
            a = j / 120 * 2 * math.pi
            r = r0 * (1 + sum(amp * (1 + i * 0.04) * math.sin(k * a + ph + i * 0.07) for k, amp, ph in harm))
            pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a) * 0.82:.1f}")
        cls = "contour" + (" major" if i % 3 == 2 else "") + (f" {cls_focal}" if i == focal else "")
        out.append(f'<path class="{cls}" d="M{" L".join(pts)} Z"/>')
    return f'<svg class="topo" viewBox="0 0 1080 1350" preserveAspectRatio="none">{"".join(out)}</svg>'

TICK = '<svg viewBox="0 0 14 14"><path d="M2.5 7.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg viewBox="0 0 24 24"><path d="M12 4v16M5 13l7 7 7-7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def footer(i, dark, last=False):
    wm = wm_light if dark else wm_dark
    right = '<span class="swipe">Save for later</span>' if last else '<span class="swipe">Swipe <span class="arr">→</span></span>'
    return f'<footer><div class="wm">{wm}</div><div class="fr"><span class="pg">0{i} / 04</span>{right}</div></footer>'

S = []

# 1 — Cover (dark)
S.append(f'''<section class="slide dark">
{contours(930, 1060, n=15, base=40, step=44, seed=5, focal=1)}
<div class="mask m1"></div>
<div class="inner">
  <h1 class="cover-h"><span class="pre">The workforce is evolving.</span>Are your skills <em>evolving with it?</em></h1>
</div>
{footer(1, True)}
</section>''')

# 2 — The shift (cream)
old = ["Knowledge.", "Technical expertise.", "Individual output."]
new = ["Working effectively with AI.", "Making informed decisions.", "Evaluating AI-generated work."]
old_html = "".join(f'<li>{t}</li>' for t in old)
new_html = "".join(f'<li><span class="tk">{TICK}</span>{t}</li>' for t in new)
S.append(f'''<section class="slide cream">
<div class="inner">
  <div class="then">
    <h2 class="blk-h">Yesterday's workplace measured:</h2>
    <ul class="then-list">{old_html}</ul>
  </div>
  <div class="shift-arrow">{ARROW}</div>
  <div class="now">
    <h2 class="blk-h">Today's workplace <em>also demands:</em></h2>
    <ul class="now-list">{new_html}</ul>
  </div>
</div>
{footer(2, False)}
</section>''')

# 3 — What organisations need (cream)
needs = [("Understand", "the problem."), ("Direct AI", "towards the right solution."),
         ("Recognise", "when AI gets it wrong."), ("Validate", "the final outcome.")]
rows = "".join(f'<div class="need"><span class="nidx">0{k+1}</span><p><strong>{a}</strong> {b}</p></div>' for k, (a, b) in enumerate(needs))
S.append(f'''<section class="slide cream">
<div class="inner">
  <h2 class="h-sec">An <em>AI-ready workforce</em> needs people who can:</h2>
  <div class="needs">{rows}</div>
</div>
{footer(3, False)}
</section>''')

# 4 — Closing (dark)
S.append(f'''<section class="slide dark">
{contours(120, 1240, n=13, base=40, step=46, seed=21, focal=1)}
<div class="mask m4"></div>
<div class="inner">
  <h2 class="close-h"><span class="pre">The future of work isn't about replacing human skills with AI.</span>It's about making human skills <em>more valuable</em> with AI.</h2>
  <div class="product">
    <div class="p-name"><span class="live"></span>HackerEarth WorkScore</div>
    <p class="p-line">Measure AI fluency.<br>Understand workforce readiness.</p>
  </div>
</div>
{footer(4, True, last=True)}
</section>''')

CSS = (REPO / "carousel-ai-agent" / "style.css").read_text().replace('url("../', 'url("../')
EXTRA = (OUT / "extra.css").read_text()
html = f'<!doctype html><html><head><meta charset="utf-8"><title>Future Skills Carousel</title><style>{CSS}\n{EXTRA}</style></head><body>{"".join(S)}</body></html>'
(OUT / "carousel.html").write_text(html)
print("ok")
