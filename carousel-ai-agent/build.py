import math, random, pathlib
OUT = pathlib.Path(__file__).parent
REPO = OUT.parent
wm_dark = (REPO/"Logo Dark.svg").read_text()
wm_light = (REPO/"Logo-Light.svg").read_text()

def contours(cx, cy, n=14, base=60, step=46, seed=3, focal=2, cls_focal="cta"):
    rnd = random.Random(seed)
    harm = [(k, rnd.uniform(0.04,0.11), rnd.uniform(0, 6.28)) for k in (2,3,5)]
    out = []
    for i in range(n):
        r0 = base + i*step
        pts = []
        for j in range(120):
            a = j/120*2*math.pi
            r = r0*(1 + sum(amp*(1+i*0.04)*math.sin(k*a+ph+i*0.07) for k,amp,ph in harm))
            pts.append(f"{cx+r*math.cos(a):.1f},{cy+r*math.sin(a)*0.82:.1f}")
        cls = "contour" + (" major" if i%3==2 else "") + (f" {cls_focal}" if i==focal else "")
        out.append(f'<path class="{cls}" d="M{" L".join(pts)} Z"/>')
    return f'<svg class="topo" viewBox="0 0 1080 1350" preserveAspectRatio="none">{"".join(out)}</svg>'

compass = '''<span class="compass"><svg viewBox="0 0 22 22"><circle cx="11" cy="11" r="9" class="c-ring"/><circle cx="11" cy="11" r="5" class="c-ring"/><line x1="11" y1="2" x2="11" y2="6" class="c-n"/><line x1="20" y1="11" x2="16" y2="11" class="c-tick"/><line x1="11" y1="20" x2="11" y2="16" class="c-tick"/><line x1="2" y1="11" x2="6" y2="11" class="c-tick"/><circle cx="11" cy="11" r="1.2" class="c-dot"/></svg></span>'''

def eyebrow(num, label):
    return f'<div class="eyebrow">{compass}<span class="bracket">[ {num} ]</span><span>{label}</span></div>'

def footer(i, dark, swipe=True):
    wm = wm_light if dark else wm_dark
    right = f'<span class="swipe">Swipe <span class="arr">→</span></span>' if swipe else '<span class="swipe">Save for later</span>'
    return f'<footer><div class="wm">{wm}</div><div class="fr"><span class="pg">0{i} / 04</span>{right}</div></footer>'

S = []
# Slide 1 — dark hero
S.append(f'''<section class="slide dark">
{contours(900, 1040, n=15, base=40, step=44, seed=7, focal=1, cls_focal="lime")}
<div class="mask m1"></div>
<div class="inner">
  {eyebrow("01","AI collaboration")}
  <h1 class="h-hero">You're working with an AI agent. But who's actually <em>steering the work?</em></h1>
  <div class="body-stack">
    <p class="lead">AI agents can plan, make decisions, edit files and complete tasks.</p>
    <p class="lead dim">But giving an agent a task isn't the same as knowing how to guide its work.</p>
  </div>
  <div class="callout dark-callout"><span class="live"></span>The quality of the outcome depends on both.</div>
</div>
{footer(1, True)}
</section>''')

# Slide 2 — cream, 3 inputs
items2 = [("The problem","you're trying to solve."),("The context","and information it needs."),("The constraints","and requirements it must follow.")]
cards2 = "".join(f'<div class="row-card"><span class="idx">0{k+1}</span><div class="rc-text"><strong>{a}</strong> {b}</div></div>' for k,(a,b) in enumerate(items2))
S.append(f'''<section class="slide cream">
{contours(1020, 140, n=10, base=40, step=40, seed=11, focal=-1)}
<div class="mask m2"></div>
<div class="inner">
  {eyebrow("02","What goes in")}
  <h2 class="h-sec">The agent works with <em>the context you give it.</em></h2>
  <p class="lead">What you provide shapes what the agent produces.</p>
  <div class="stack">{cards2}</div>
  <div class="note"><span class="note-bar"></span><p>Miss important details, and the agent may solve the wrong problem<span class="dash">—</span>even if the output looks right.</p></div>
</div>
{footer(2, False)}
</section>''')

# Slide 3 — cream, 2x2 decisions
items3 = [("Accept","what works."),("Question","assumptions."),("Correct","mistakes."),("Redirect","the work when needed.")]
cards3 = "".join(f'<div class="grid-card"><div class="gc-top"><span class="idx">0{k+1}</span><span class="tick"></span></div><div class="gc-verb">{a}</div><div class="gc-obj">{b}</div></div>' for k,(a,b) in enumerate(items3))
S.append(f'''<section class="slide cream">
<div class="inner">
  {eyebrow("03","What comes back")}
  <h2 class="h-sec">But the agent also <em>shapes your next decision.</em></h2>
  <p class="lead">The agent makes suggestions, changes and returns results. You decide what happens next.</p>
  <div class="grid4">{cards3}</div>
  <p class="closing">Knowing when to trust or challenge the agent is essential to effective AI collaboration.</p>
</div>
{footer(3, False)}
</section>''')

# Slide 4 — dark, 4-step loop
items4 = [("Understand","the problem."),("Direct","the agent."),("Review","its work."),("Validate","the result.")]
steps = "".join(f'<div class="step"><div class="marks">{"<span></span>"*9}</div><span class="sidx">0{k+1}</span><div class="sverb">{a}</div><div class="sobj">{b}</div></div>' for k,(a,b) in enumerate(items4))
S.append(f'''<section class="slide dark">
{contours(140, 1220, n=13, base=40, step=46, seed=21, focal=1, cls_focal="lime")}
<div class="mask m4"></div>
<div class="inner">
  {eyebrow("04","The human in the loop")}
  <h2 class="h-sec">Good AI work requires <em>human judgment</em> throughout.</h2>
  <p class="lead dim">Working with AI isn't about handing over the entire task. It's about guiding the work towards the right outcome.</p>
  <div class="steps">{steps}</div>
  <p class="closer">AI can do the work. <span class="w">But the decisions around that work still matter.</span></p>
</div>
{footer(4, True, swipe=False)}
</section>''')

CSS = (OUT/"style.css").read_text()
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>AI Agent Carousel</title><style>{CSS}</style></head><body>{"".join(S)}</body></html>'''
(OUT/"carousel.html").write_text(html)
print("ok")
