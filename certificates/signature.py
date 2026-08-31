"""The certificate's signature mark: an abstract, hand-crafted flourish.

One source of geometry, rendered two ways: as inline SVG for the on-screen
diploma, and drawn on a ReportLab canvas for the PDF, so the two never drift.

It is deliberately illegible (no name, no words) and given natural stroke-weight
variation by splitting the main stroke into runs of decreasing width, from a
heavy leading loop down to a fine terminal hairline. Coordinates live in a
300 x 130 viewBox (y-down, SVG convention); the PDF drawer flips y.
"""

from __future__ import annotations

VBW, VBH = 300, 130
INK = "#1f3350"

# Variant A, "ascending flourish": a tall leading loop, three cursive humps, a
# rising terminal, then a separate underline sweep with a curl at the left.
_MAIN = [
    (22, 88), (30, 58), (44, 26), (64, 34), (56, 66), (74, 78), (88, 46),
    (102, 74), (120, 48), (136, 76), (154, 46), (174, 72), (198, 42),
    (224, 30), (252, 46), (276, 28), (292, 20),
]
# (upto_segment_index, width): heavy leading stroke tapering to a fine terminal.
_MAIN_RUNS = [(4, 3.4), (11, 2.7), (16, 1.7)]

_LINE = [(258, 102), (205, 108), (140, 106), (78, 108), (38, 100),
         (24, 90), (40, 86), (62, 96)]
_LINE_WIDTH = 2.1

_TENSION = 1 / 6


def _catmull(pts):
    """Smooth Catmull-Rom spline through pts as cubic beziers.

    Returns (start_point, [(c1x, c1y, c2x, c2y, x, y), ...]).
    """
    n = len(pts)
    segs = []
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < n else pts[i + 1]
        c1x = p1[0] + (p2[0] - p0[0]) * _TENSION
        c1y = p1[1] + (p2[1] - p0[1]) * _TENSION
        c2x = p2[0] - (p3[0] - p1[0]) * _TENSION
        c2y = p2[1] - (p3[1] - p1[1]) * _TENSION
        segs.append((c1x, c1y, c2x, c2y, p2[0], p2[1]))
    return pts[0], segs


def _strokes():
    """The signature as a list of (start, beziers, width) runs."""
    start, segs = _catmull(_MAIN)
    out = []
    i0 = 0
    for upto, width in _MAIN_RUNS:
        sub = segs[i0:upto]
        if sub:
            out.append((_MAIN[i0], sub, width))
        i0 = upto
    lstart, lsegs = _catmull(_LINE)
    out.append((lstart, lsegs, _LINE_WIDTH))
    return out


def _d(start, beziers):
    d = f"M{round(start[0], 1)} {round(start[1], 1)}"
    for (c1x, c1y, c2x, c2y, x, y) in beziers:
        d += (
            f"C{round(c1x, 1)} {round(c1y, 1)} "
            f"{round(c2x, 1)} {round(c2y, 1)} "
            f"{round(x, 1)} {round(y, 1)}"
        )
    return d


def svg(color: str = INK) -> str:
    """Inline SVG of the signature mark (overflow-visible; scales to its box)."""
    paths = "".join(
        f'<path d="{_d(start, beziers)}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
        for (start, beziers, width) in _strokes()
    )
    return (
        f'<svg viewBox="0 0 {VBW} {VBH}" xmlns="http://www.w3.org/2000/svg" '
        f'style="overflow:visible" aria-hidden="true">{paths}</svg>'
    )


def draw(c, x, y, w, h, color=None):
    """Draw the signature on a ReportLab canvas inside the box (x, y, w, h).

    (x, y) is the box's bottom-left in points; y is flipped from the viewBox.
    """
    from reportlab.lib.colors import HexColor

    sx, sy = w / VBW, h / VBH
    sw = (sx + sy) / 2
    ink = HexColor(color or INK)

    def tx(px):
        return x + px * sx

    def ty(py):
        return y + (VBH - py) * sy

    c.saveState()
    c.setStrokeColor(ink)
    c.setLineCap(1)
    c.setLineJoin(1)
    for (start, beziers, width) in _strokes():
        c.setLineWidth(max(0.4, width * sw))
        p = c.beginPath()
        p.moveTo(tx(start[0]), ty(start[1]))
        for (c1x, c1y, c2x, c2y, ex, ey) in beziers:
            p.curveTo(tx(c1x), ty(c1y), tx(c2x), ty(c2y), tx(ex), ty(ey))
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()
