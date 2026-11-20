import importlib.util, pathlib
OUT = pathlib.Path(__file__).parent
REPO = OUT.parent
# reuse contour + footer helpers from carousel-future-skills
spec = importlib.util.spec_from_file_location("fs", REPO / "carousel-future-skills" / "build.py")
src = (REPO / "carousel-future-skills" / "build.py").read_text().split("S = []")[0]
ns = {"__file__": str(REPO / "carousel-future-skills" / "build.py")}
exec(src, ns)
contours, footer = ns["contours"], ns["footer"]

signs = [
    ("Problem Analysis", "They understand the problem before asking AI to solve it."),
    ("Agent Steering", "They give AI clear instructions and redirect it when needed."),
    ("Judgment", "They know when to trust AI and when to question it."),
    ("Quality Validation", "They review, test and verify what AI produces."),
    ("Outcomes", "They make sure the final work actually solves the problem."),
]

def progress(active):
    segs = "".join(f'<span class="seg{" on" if i in active else ""}"><b>0{i+1}</b></span>' for i in range(5))
    return f'<div class="progress">{segs}</div>'

def card(i):
    t, d = signs[i]
    return f'<div class="sign"><div class="s-top"><span class="s-num">0{i+1}</span><h3>{t}</h3></div><p>{d}</p></div>'

S = []
S.append(f'''<section class="slide dark">
{contours(930, 1080, n=15, base=40, step=44, seed=9, focal=1)}
<div class="mask m1"></div>
<div class="inner">
  <div class="big5">5</div>
  <h1 class="cover-h">signs someone knows how to work with <em>AI.</em></h1>
  <p class="cover-sub">It's more than writing good prompts.</p>
</div>
{footer(1, True)}
</section>''')

S.append(f'''<section class="slide cream">
<div class="inner">
  {progress({0,1,2})}
  <div class="signs">{card(0)}{card(1)}{card(2)}</div>
</div>
{footer(2, False)}
</section>''')

S.append(f'''<section class="slide cream">
<div class="inner">
  {progress({3,4})}
  <div class="signs two">{card(3)}{card(4)}</div>
</div>
{footer(3, False)}
</section>''')

S.append(f'''<section class="slide dark">
{contours(120, 1240, n=13, base=40, step=46, seed=21, focal=1)}
<div class="mask m4"></div>
<div class="inner">
  <h2 class="close-h"><span class="pre">These skills are becoming essential across the modern workforce.</span>But how do you <em>measure them?</em></h2>
  <div class="product">
    <div class="p-name"><span class="live"></span>HackerEarth WorkScore</div>
    <p class="p-line">Evaluates AI fluency through real tasks, candidate actions and evidence-backed scoring.</p>
  </div>
  <div class="cta">See beyond the AI output <span>→</span></div>
</div>
{footer(4, True, last=True)}
</section>''')

CSS = (REPO / "carousel-ai-agent" / "style.css").read_text()
BASE = (REPO / "carousel-future-skills" / "extra.css").read_text()
EXTRA = (OUT / "extra.css").read_text()
html = f'<!doctype html><html><head><meta charset="utf-8"><title>Five Signs Carousel</title><style>{CSS}\n{BASE}\n{EXTRA}</style></head><body>{"".join(S)}</body></html>'
(OUT / "carousel.html").write_text(html)
print("ok")
