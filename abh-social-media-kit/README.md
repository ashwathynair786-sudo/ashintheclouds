# ABH — Agentic Banking Hackathon social media kit

Built from `abh hackathon branding.pdf`: Aeonik Fono (Regular headlines at -3% tracking / 110% leading, Bold CTA),
Airwallex Orange `#FA4402` on black, the ABH logos, and the brand nebula imagery with the pixel-notch corner.

| Format | Size | File |
| --- | --- | --- |
| Instagram story | 1080 × 1920 | `exports/ABH-instagram-story-1080x1920.png` |
| LinkedIn | 1200 × 1200 | `exports/ABH-linkedin-1200x1200.png` |
| Facebook | 1200 × 628 | `exports/ABH-facebook-1200x628.png` |
| Email banner | 600 × 250 (+ @2x 1200 × 500 for retina) | `exports/ABH-email-600x250.png`, `exports/ABH-email-600x250@2x.png` |

Copy: "Banking needs a new playbook. / Will you write it? / Bring your boldest ideas to the Agentic Banking Hackathon."

`source/` holds the editable HTML layouts (one per format, shared `kit.css`). Edit the copy there and re-export with
Playwright by screenshotting each page at its exact viewport size.
