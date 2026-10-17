# ABH — Agentic Banking Hackathon social media kit

Built from `abh hackathon branding.pdf`: Aeonik Fono (Regular headlines at -3% tracking / 110% leading, Bold CTA),
Airwallex Orange `#FA4402` on black, the ABH logos, and the brand nebula imagery with the pixel-notch motif.
Sets 1–3 share one layout; only the imagery and copy change. Set 4 is type-only.
Email banners carry the headline only (no subline) to keep them uncluttered. Each image panel uses the exact square cut the brand
guide applies to that image (orange: top-right, cyan: top-left, violet: bottom-left).

Each set has the same four formats:

| Format | Size | File |
| --- | --- | --- |
| Instagram story | 1080 × 1920 | `ABH-instagram-story-1080x1920.png` |
| LinkedIn | 1200 × 1200 | `ABH-linkedin-1200x1200.png` |
| Facebook | 1200 × 628 | `ABH-facebook-1200x628.png` |
| Email banner | 600 × 250 (+ @2x 1200 × 500 for retina) | `ABH-email-600x250.png`, `ABH-email-600x250@2x.png` |

| Set | Look | Copy |
| --- | --- | --- |
| `exports/set-1-black` | Black canvas, orange imagery panel | Banking needs a new playbook. / Will you write it? / Bring your boldest ideas to the Agentic Banking Hackathon. |
| `exports/set-2-cyan` | Black canvas, cyan/orange imagery panel | Everyone talks about the future of finance. / Few actually build it. / Be one of them. Join the Agentic Banking Hackathon. |
| `exports/set-3-violet` | Black canvas, violet/orange imagery panel | (same as set 2) |
| `exports/set-4-type` | Black canvas, type only (no imagery) | What if banking could think for itself? / Let’s find out. / Explore what’s possible at the Agentic Banking Hackathon. |

Sets 2 and 3 use the full-resolution versions (from the brand PDF) of the supplied
`DTS_Misc_1_(Nick_Fancher)…ID5049-horizontal-3` and `…ID15129-vertical-6` backgrounds, which were too small to use directly.

`source/` holds the editable HTML layouts (`set1-*` … `set4-*`, shared `kit.css`). Edit the copy there and
re-export with Playwright by screenshotting each page at its exact viewport size.
