import pathlib
OUT = pathlib.Path(__file__).parent
REPO = OUT.parent
# reuse contour + footer helpers from carousel-future-skills
src = (REPO / "carousel-future-skills" / "build.py").read_text().split("S = []")[0]
ns = {"__file__": str(REPO / "carousel-future-skills" / "build.py")}
exec(src, ns)
contours, footer = ns["contours"], ns["footer"]

S = []

# 1 — dark with hands photo
S.append(f'''<section class="slide dark">
<div class="photo"></div>
<div class="inner bottom">
  <h1 class="h">The final output doesn't tell you <em>everything</em> about someone's AI skills.</h1>
  <div class="body">
    <p>Two people can use the same AI tool and produce similar results. But the way they reach that result can be very different.</p>
    <p>One may simply accept the first answer. The other may question, refine and validate it before using it.</p>
  </div>
</div>
{footer(1, True)}
</section>''')

# 2 — cream
S.append(f'''<section class="slide cream">
<div class="inner">
  <h2 class="h">It starts with <em>understanding the problem.</em></h2>
  <div class="body">
    <p>Effective AI use begins before the first prompt.</p>
    <div class="qcard"><p>Can someone identify what needs to be solved, provide the right context and explain what a successful outcome should look like?</p></div>
    <p>Without that clarity, even a convincing AI response can miss the actual requirement.</p>
  </div>
</div>
{footer(2, False)}
</section>''')

# 3 — cream
flags = "".join(f'<span class="flag"><i></i>{t}</span>' for t in ["Errors", "Missing details", "Incorrect assumptions"])
S.append(f'''<section class="slide cream">
<div class="inner">
  <h2 class="h">The important part is knowing when to <em>question the answer.</em></h2>
  <div class="body">
    <p>AI can produce confident responses that contain errors, missing details or incorrect assumptions.</p>
    <div class="flags">{flags}</div>
    <p>People need to review the output, check whether it meets the requirements and make corrections when something doesn't add up.</p>
  </div>
</div>
{footer(3, False)}
</section>''')

# 4 — dark closing
S.append(f'''<section class="slide dark">
{contours(900, 1080, n=15, base=40, step=44, seed=13, focal=1)}
<div class="mask m1"></div>
<div class="inner">
  <h2 class="h big">The quality of the work depends on <em>the thinking behind it.</em></h2>
</div>
{footer(4, True, last=True)}
</section>''')

CSS = (REPO / "carousel-ai-agent" / "style.css").read_text()
EXTRA = (OUT / "extra.css").read_text()
html = f'<!doctype html><html><head><meta charset="utf-8"><title>Thinking Behind Carousel</title><style>{CSS}\n{EXTRA}</style></head><body>{"".join(S)}</body></html>'
(OUT / "carousel.html").write_text(html)
print("ok")
