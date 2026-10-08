"""Generate a square (1:1) topographic contour SVG in the style of the *_10m.svg maps.

Usage: python3 generate_contours.py [seed] [output.svg]
"""
import sys
from collections import defaultdict

import numpy as np

SIZE = 800          # output is SIZE x SIZE
STEP = 2            # grid spacing in px
LEVELS = 26         # number of contour lines
BG = "#f7f5f0"
STROKE = "#33414d"
WIDTH = 0.55


def value_noise(n, cells, rng):
    """Smooth value noise on an n x n grid with `cells` lattice cells per side."""
    lattice = rng.random((cells + 2, cells + 2))
    t = np.linspace(0, cells, n, endpoint=False)
    i = t.astype(int)
    f = t - i
    f = f * f * (3 - 2 * f)  # smoothstep
    fy, fx = np.meshgrid(f, f, indexing="ij")
    iy, ix = np.meshgrid(i, i, indexing="ij")
    a = lattice[iy, ix]
    b = lattice[iy, ix + 1]
    c = lattice[iy + 1, ix]
    d = lattice[iy + 1, ix + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def terrain(n, rng):
    y, x = np.mgrid[0:1:n * 1j, 0:1:n * 1j]
    h = np.zeros((n, n))
    # a dominant off-centre summit plus a couple of lesser ridges
    for cx, cy, amp, r in [(0.46, 0.44, 1.0, 0.22), (0.78, 0.76, 0.45, 0.13),
                           (0.16, 0.80, 0.35, 0.15), (0.82, 0.18, 0.28, 0.11)]:
        h += amp * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r))
    # fractal noise for natural, crinkly edges
    amp, cells = 0.35, 3
    for _ in range(7):
        h += amp * (value_noise(n, cells, rng) - 0.5)
        amp *= 0.5
        cells *= 2
    return h


# marching-squares edge table: case -> list of (edge, edge); edges 0=top 1=right 2=bottom 3=left
CASES = {1: [(3, 2)], 2: [(2, 1)], 3: [(3, 1)], 4: [(0, 1)], 5: [(3, 0), (2, 1)],
         6: [(0, 2)], 7: [(3, 0)], 8: [(0, 3)], 9: [(0, 2)], 10: [(0, 1), (3, 2)],
         11: [(0, 1)], 12: [(3, 1)], 13: [(2, 1)], 14: [(3, 2)]}


def contour_segments(h, level):
    n = h.shape[0]
    segs = []

    def pt(r, c, edge):
        if edge == 0:   # top: (r,c)-(r,c+1)
            a, b, p, q = h[r, c], h[r, c + 1], (r, c), (r, c + 1)
        elif edge == 1:  # right: (r,c+1)-(r+1,c+1)
            a, b, p, q = h[r, c + 1], h[r + 1, c + 1], (r, c + 1), (r + 1, c + 1)
        elif edge == 2:  # bottom: (r+1,c)-(r+1,c+1)
            a, b, p, q = h[r + 1, c], h[r + 1, c + 1], (r + 1, c), (r + 1, c + 1)
        else:            # left: (r,c)-(r+1,c)
            a, b, p, q = h[r, c], h[r + 1, c], (r, c), (r + 1, c)
        t = (level - a) / (b - a)
        return (round((p[1] + t * (q[1] - p[1])) * STEP, 1),
                round((p[0] + t * (q[0] - p[0])) * STEP, 1))

    above = h > level
    idx = (above[:-1, :-1] * 8 + above[:-1, 1:] * 4 +
           above[1:, 1:] * 2 + above[1:, :-1] * 1)
    for r, c in zip(*np.nonzero((idx > 0) & (idx < 15))):
        for e1, e2 in CASES[int(idx[r, c])]:
            segs.append((pt(r, c, e1), pt(r, c, e2)))
    return segs


def chain(segs):
    """Join loose segments into polylines."""
    adj = defaultdict(list)
    for i, (a, b) in enumerate(segs):
        adj[a].append(i)
        adj[b].append(i)
    used = [False] * len(segs)
    lines = []
    for i in range(len(segs)):
        if used[i]:
            continue
        used[i] = True
        line = list(segs[i])
        for end in (True, False):  # grow forwards, then backwards
            while True:
                tip = line[-1] if end else line[0]
                nxt = next((j for j in adj[tip] if not used[j]), None)
                if nxt is None:
                    break
                used[nxt] = True
                a, b = segs[nxt]
                p = b if a == tip else a
                line.append(p) if end else line.insert(0, p)
        lines.append(line)
    return lines


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    out = sys.argv[2] if len(sys.argv) > 2 else f"contours_square_{seed}.svg"
    rng = np.random.default_rng(seed)
    n = SIZE // STEP + 1
    h = terrain(n, rng)
    levels = np.linspace(h.min(), h.max(), LEVELS + 2)[1:-1]

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" '
             f'width="{SIZE}" height="{SIZE}">',
             f'  <rect width="100%" height="100%" fill="{BG}"/>']
    for lvl in levels:
        for line in chain(contour_segments(h, lvl)):
            if len(line) < 4:
                continue
            d = "M " + " L ".join(f"{x},{y}" for x, y in line)
            parts.append(f'  <path d="{d}" fill="none" stroke="{STROKE}" '
                         f'stroke-width="{WIDTH}" stroke-linejoin="round"/>')
    parts.append("</svg>")
    with open(out, "w") as f:
        f.write("\n".join(parts) + "\n")
    print(out)


if __name__ == "__main__":
    main()
