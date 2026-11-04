# ContextCon: Remember Everything — Logo

![Preview](preview-sheet.png)

## The mark
- **Three nested open rings** form the "C" of *Context* and *Con*. They stand for layered, persistent memory (and the database underneath it).
- **The open side faces an incoming agent node** (the outlined circle). A link carries what that agent learned into the **shared core** that every ring wraps around: one agent's learning becomes every agent's advantage.
- **The trace line under the wordmark** ends in the same node. It works as a decision trace and ties the tagline back to the mark.

## Files
| Variant | Files |
|---|---|
| Horizontal (primary) | `contextcon-logo-horizontal-{dark,light}[-transparent].{svg,png}` |
| Stacked | `contextcon-logo-stacked-{dark,light}[-transparent].{svg,png}` |
| Icon / avatar (512×512, rounded) | `contextcon-icon-{dark,light}.{svg,png}` |

All text is converted to outlines, so the SVGs need no fonts installed. PNGs are exported at 4× (logos) and 2× (icons).
Use `-dark` on dark backgrounds and `-light` on light backgrounds.

## Palette
| Role | Hex |
|---|---|
| Night (background / ink) | `#0B0A1F` |
| Violet (gradient start) | `#8B5CF6` |
| Cyan (gradient end) | `#22D3EE` |
| Signal lime (core, dark version) | `#C8FF3D` |
| Muted lavender (tagline, dark) | `#A9A6C9` |
| Muted slate (tagline, light) | `#5B5878` |

## Type
- Wordmark: **Bricolage Grotesque ExtraBold**, tracking −2.5%
- Tagline: **Geist SemiBold**, uppercase, tracking +22%

## Regenerate
`python3 generate.py` (needs `pip install fonttools`; run from the repo root, where the font files live).
