#!/usr/bin/env python3
"""Build the Friends of Woodmont Park sign designs and vinyl cut files.

Text is shaped with HarfBuzz (so kerning is real), converted to outlines with
fontTools, and merged with skia-pathops, so overlapping glyph contours from the
variable fonts don't turn into stray cut lines. Nothing here has been cut on a
real machine yet.

Setup (keep this out of the repo):
    python3 -m venv /tmp/signs-venv
    /tmp/signs-venv/bin/pip install fonttools uharfbuzz skia-pathops resvg-py
    Download PlayfairDisplay[wght].ttf and Outfit[wght].ttf from github.com/google/fonts

Run:
    /tmp/signs-venv/bin/python build_signs.py --fonts /path/to/font/dir

To change the workday date, edit DATE_LINE below or pass --date, then re-run:
    build_signs.py --fonts DIR --date "Sat, Dec 12 · 9–11 AM"

Coordinates are in hundredths of an inch; every SVG states its size in inches.
"""
import argparse
import csv
import json
import shutil
import tempfile
from pathlib import Path

import pathops
import resvg_py
import uharfbuzz as hb
from fontTools.misc.bezierTools import splitCubicAtT
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent

GREEN, YELLOW, PALE = "#1f3a2e", "#f2c230", "#eef3ec"
COLORS = {"pale": PALE, "yellow": YELLOW}
FONT_FILES = {"serif": "PlayfairDisplay[wght].ttf", "sans": "Outfit[wght].ttf"}

# Placeholder copy that the board hasn't approved. Change it here and re-run.
TRAIL_NAME = ("Woodmont", "Park Trails")
ARROW_RIGHT_LABEL = "Footbridge"
ARROW_LEFT_LABEL = "Old courts"
DATE_LINE = "Sat, Nov 14 · 9–11 AM"  # example only
ALT_DATE_LINE = "Join us today"  # a strip that never goes out of date

# Initial run: how many of each sign. Change these and the gang sheets follow.
RUN = {"trailhead": 1, "workday-yard": 2, "trail-blaze": 6,
       "trail-arrow-footbridge": 2, "trail-arrow-old-courts": 2}

UNTESTED = ("UNTESTED: this cut file has not been run on a real vinyl cutter. "
            "Do a small test cut first and check the size against a ruler.")


class Fonts:
    """Static, overlap-free instances of the variable fonts, one per weight."""

    def __init__(self, font_dir):
        self.dir = Path(font_dir)
        self.tmp = Path(tempfile.mkdtemp(prefix="signs-fonts-"))
        self.cache = {}

    def get(self, family, weight):
        key = (family, weight)
        if key not in self.cache:
            vf = TTFont(self.dir / FONT_FILES[family])
            inst = instancer.instantiateVariableFont(
                vf, {"wght": weight}, overlap=instancer.OverlapMode.REMOVE)
            path = self.tmp / f"{family}-{weight}.ttf"
            inst.save(path)
            tt = TTFont(path)
            face = hb.Face(hb.Blob.from_file_path(str(path)))
            self.cache[key] = (tt, tt.getGlyphSet(), hb.Font(face), tt["head"].unitsPerEm)
        return self.cache[key]

    def close(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


def text_path(fonts, text, family, weight, size, x, y, anchor="start"):
    """Outline one line of text. size, x and y are in sign units (0.01 in)."""
    tt, glyphs, font, upem = fonts.get(family, weight)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    names = tt.getGlyphOrder()
    advance = sum(p.x_advance for p in buf.glyph_positions)
    s = size / upem
    ox = x - (advance * s if anchor == "end" else advance * s / 2 if anchor == "middle" else 0)
    out = pathops.Path()
    pen = out.getPen(glyphSet=glyphs)
    cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        tx = ox + (cx + pos.x_offset) * s
        ty = y - pos.y_offset * s
        glyphs[names[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, tx, ty)))
        cx += pos.x_advance
    # Merge, so touching letters and overlapping contours become one clean outline.
    out.simplify(fix_winding=True, keep_starting_points=False)
    return out


def rect_path(x, y, w, h, r=0):
    p = pathops.Path()
    pen = p.getPen()
    k = 0.5523 * r
    if r:
        pen.moveTo((x + r, y))
        pen.lineTo((x + w - r, y))
        pen.curveTo((x + w - r + k, y), (x + w, y + r - k), (x + w, y + r))
        pen.lineTo((x + w, y + h - r))
        pen.curveTo((x + w, y + h - r + k), (x + w - r + k, y + h), (x + w - r, y + h))
        pen.lineTo((x + r, y + h))
        pen.curveTo((x + r - k, y + h), (x, y + h - r + k), (x, y + h - r))
        pen.lineTo((x, y + r))
        pen.curveTo((x, y + r - k), (x + r - k, y), (x + r, y))
    else:
        pen.moveTo((x, y))
        pen.lineTo((x + w, y))
        pen.lineTo((x + w, y + h))
        pen.lineTo((x, y + h))
    pen.closePath()
    return p


def trail_curve(x, y, scale):
    """The icon's trail line, turned from a stroke into a filled outline.

    The icon runs this curve off its bottom edge and clips it. A sign has no
    clip, so the curve is shortened until its round cap ends on the icon's edge.
    """
    p0, p1, p2, p3 = (10, 66), (18, 54), (44, 56), (32, 44)
    width = 5
    lo, hi = 0.0, 0.5
    for _ in range(30):
        t = (lo + hi) / 2
        y_at = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        lo, hi = (t, hi) if y_at + width / 2 > 64 else (lo, t)
    _, seg = splitCubicAtT(p0, p1, p2, p3, hi)
    line = pathops.Path()
    pen = TransformPen(line.getPen(), (scale, 0, 0, scale, x, y))
    pen.moveTo(seg[0])
    pen.curveTo(seg[1], seg[2], seg[3])
    pen.endPath()
    line.stroke(width * scale, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    line.convertConicsToQuads()
    line.simplify(fix_winding=True)
    return line


def icon_blaze(x, y, size):
    s = size / 64
    return rect_path(x + 25 * s, y + 11 * s, 14 * s, 29 * s, 2.5 * s), trail_curve(x, y, s)


def arrow_path(x, cy, length, head, shaft, direction):
    """A solid arrow, drawn rather than taken from a font so it's easy to cut."""
    h, t = head / 2, shaft / 2
    d = 1 if direction == "right" else -1
    tip = x + d * length
    neck = tip - d * head * 0.85
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo((x, cy - t))
    for pt in [(neck, cy - t), (neck, cy - h), (tip, cy), (neck, cy + h), (neck, cy + t), (x, cy + t)]:
        pen.lineTo(pt)
    pen.closePath()
    p.simplify(fix_winding=True)
    return p


def to_d(path):
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    p = pathops.Path(path)
    p.convertConicsToQuads()
    p.draw(pen)
    return pen.getCommands()


def transformed(path, fn_matrix):
    out = pathops.Path()
    path.draw(TransformPen(out.getPen(), fn_matrix))
    return out


class Piece:
    """One separately cuttable group: a line of text or a shape."""

    def __init__(self, pid, color, path, swap=False):
        self.id, self.color, self.path, self.swap = pid, color, path, swap
        self.bounds = path.bounds
        self.area = abs(path.area) / 1e4  # square inches

    @property
    def w(self):
        return (self.bounds[2] - self.bounds[0]) / 100

    @property
    def h(self):
        return (self.bounds[3] - self.bounds[1]) / 100


def build_signs(fonts, date_line):
    T = lambda *a, **k: text_path(fonts, *a, **k)
    signs = {}

    rect, curve = icon_blaze(520, 110, 760)
    signs["trailhead"] = dict(
        title="Trailhead sign", size=(18, 24), stock="3 mm aluminum composite, dark green",
        radius=30, holes=[(900, 90), (900, 2340)], pieces=[
            Piece("blaze-rectangle", "yellow", rect),
            Piece("trail-line", "pale", curve),
            Piece("name-line-1", "pale", T(TRAIL_NAME[0], "serif", 700, 220, 900, 1090, "middle")),
            Piece("name-line-2", "pale", T(TRAIL_NAME[1], "serif", 700, 220, 900, 1320, "middle")),
            Piece("cared-for", "pale", T("Cared for by your neighbors,", "sans", 500, 105, 900, 1560, "middle")),
            Piece("fwp-name", "yellow", T("Friends of Woodmont Park", "sans", 700, 105, 900, 1690, "middle")),
            Piece("lend-a-hand", "pale", T("Lend a hand:", "sans", 500, 90, 900, 1835, "middle")),
            Piece("website", "pale", T("woodmontfriends.org", "sans", 600, 130, 900, 1985, "middle")),
            Piece("wra-line-1", "pale", T("Land owned by the Woodmont", "sans", 500, 65, 900, 2200, "middle")),
            Piece("wra-line-2", "pale", T("Recreation Association", "sans", 500, 65, 900, 2290, "middle")),
        ])

    rect, curve = icon_blaze(60, 70, 560)
    signs["workday-yard"] = dict(
        title="Workday yard sign", size=(24, 18), stock="4 mm corrugated plastic, dark green, vertical flutes",
        radius=0, holes=[], guide_y=1320, pieces=[
            Piece("blaze-rectangle", "yellow", rect),
            Piece("trail-line", "pale", curve),
            Piece("name-line-1", "pale", T("Friends of", "serif", 700, 190, 620, 275)),
            Piece("name-line-2", "pale", T("Woodmont Park", "serif", 700, 190, 620, 490)),
            Piece("volunteer", "yellow", T("Volunteer", "sans", 800, 310, 1200, 910, "middle")),
            Piece("cleanup", "yellow", T("cleanup", "sans", 800, 310, 1200, 1210, "middle")),
            Piece("date-line", "pale", T(date_line, "sans", 700, 155, 1200, 1520, "middle"), swap=True),
            Piece("website", "pale", T("woodmontfriends.org", "sans", 500, 115, 1200, 1700, "middle")),
        ])

    signs["trail-blaze"] = dict(
        title="Trail blaze marker", size=(3, 6), stock="3 mm aluminum composite, dark green",
        radius=15, holes=[(150, 35), (150, 565)], pieces=[
            Piece("blaze", "yellow", rect_path(70, 70, 160, 460, 20)),
        ])

    signs["trail-arrow-footbridge"] = dict(
        title="Direction arrow (label is a placeholder)", size=(14, 4), stock="3 mm aluminum composite, dark green",
        radius=20, holes=[(70, 100), (70, 300)], pieces=[
            Piece("label", "pale", T(ARROW_RIGHT_LABEL, "sans", 600, 150, 150, 252)),
            Piece("arrow", "pale", arrow_path(1000, 200, 250, 150, 44, "right")),
        ])

    signs["trail-arrow-old-courts"] = dict(
        title="Direction arrow (label is a placeholder)", size=(14, 4), stock="3 mm aluminum composite, dark green",
        radius=20, holes=[(1330, 100), (1330, 300)], pieces=[
            Piece("arrow", "pale", arrow_path(400, 200, 250, 150, 44, "left")),
            Piece("label", "pale", T(ARROW_LEFT_LABEL, "sans", 600, 150, 470, 252)),
        ])
    return signs


def svg_open(w_in, h_in, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_in:g}in" height="{h_in:g}in" '
            f'viewBox="0 0 {w_in * 100:g} {h_in * 100:g}"{extra}>')


def design_svg(sign):
    w, h = sign["size"]
    parts = [svg_open(w, h), f"<title>{sign['title']}: proof, not a cut file</title>",
             f'<rect id="stock" width="{w * 100}" height="{h * 100}" rx="{sign["radius"]}" fill="{GREEN}"/>']
    for x, y in sign["holes"]:
        parts.append(f'<circle class="mounting-hole" cx="{x}" cy="{y}" r="16" fill="#8b8374"/>')
    if sign.get("guide_y"):
        parts.append(f'<line id="swap-guide-not-cut" x1="120" x2="{w * 100 - 120}" y1="{sign["guide_y"]}" '
                     f'y2="{sign["guide_y"]}" stroke="{PALE}" stroke-width="8" stroke-dasharray="30 30" opacity=".45"/>')
    for p in sign["pieces"]:
        parts.append(f'<path id="{p.id}" fill="{COLORS[p.color]}" fill-rule="nonzero" d="{to_d(p.path)}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def reg_marks(w, h):
    """Two matching crosses for lining up the second color. Peel them off after."""
    arm, t = 25, 4
    d = ""
    for cx, cy in [(45, 45), (w * 100 - 45, h * 100 - 45)]:
        cross = pathops.Path()
        cross.addPath(rect_path(cx - arm, cy - t, 2 * arm, 2 * t))
        cross.addPath(rect_path(cx - t, cy - arm, 2 * t, 2 * arm))
        cross.simplify(fix_winding=True)
        d += to_d(cross)
    return d


def cut_svg(sign, name, color, pieces, marks=True):
    w, h = sign["size"]
    parts = [svg_open(w, h, f' data-vinyl="{color}"'), f"<!-- {UNTESTED} -->",
             f"<title>{name}: {color} vinyl at full size. UNTESTED on a real cutter.</title>"]
    if marks:
        parts.append(f'<g id="registration-marks" fill="#000"><path d="{reg_marks(w, h)}"/></g>')
    for p in pieces:
        parts.append(f'<path id="{p.id}" fill="#000" fill-rule="nonzero" d="{to_d(p.path)}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def gang(items, width_in, gap=0.25):
    """Shelf-pack pieces across the cuttable width. Returns placements and length.

    A piece wider than the cut width turns 90 degrees and runs along the feed.
    """
    placed, oriented = [], []
    for sign, piece in items:
        rotate = piece.w > width_in
        w, h = (piece.h, piece.w) if rotate else (piece.w, piece.h)
        if w > width_in:
            raise ValueError(f"{sign}/{piece.id} won't fit in {width_in} in")
        oriented.append((sign, piece, rotate, w, h))
    oriented.sort(key=lambda o: -o[4])
    y = 0.0
    x = 0.0
    shelf = 0.0
    for sign, piece, rotate, w, h in oriented:
        if x + w > width_in:
            y += shelf + gap
            x, shelf = 0.0, 0.0
        placed.append((sign, piece, rotate, x, y))
        x += w + gap
        shelf = max(shelf, h)
    return placed, y + shelf


def gang_svg(color, placed, width_in, length):
    parts = [svg_open(width_in, round(length + 0.01, 2), f' data-vinyl="{color}"'), f"<!-- {UNTESTED} -->",
             f"<title>All {color} pieces for the initial run, nested for a {width_in} in cut width. UNTESTED.</title>"]
    for i, (sign, piece, rotate, x, y) in enumerate(placed):
        bx0, by0, bx1, by1 = piece.bounds
        if rotate:
            # Turn 90 degrees clockwise, then move the bounding box to (x, y).
            m = (0, 1, -1, 0, x * 100 + by1, y * 100 - bx0)
        else:
            m = (1, 0, 0, 1, x * 100 - bx0, y * 100 - by0)
        parts.append(f'<path id="{sign}.{piece.id}.{i}" fill="#000" fill-rule="nonzero" '
                     f'd="{to_d(transformed(piece.path, m))}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def render_png(svg_text, path, width):
    path.write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg_text, width=width, dpi=96)))


def contact_sheet(signs):
    """A one-image proof: all signs at the same scale, on their posts."""
    bench_w, bench_h = 7400, 3300
    ground = 3180
    parts = [svg_open(bench_w / 100, bench_h / 100), f'<rect width="{bench_w}" height="{bench_h}" fill="#f4efe6"/>',
             f'<rect y="{ground}" width="{bench_w}" height="{bench_h - ground}" fill="#cfc6b4"/>']

    def place(name, x, y):
        s = signs[name]
        inner = design_svg(s).split("\n", 1)[1].rsplit("</svg>", 1)[0]
        return f'<g transform="translate({x} {y})">{inner}</g>'

    post = lambda x, y0, w=356: f'<rect x="{x - w / 2}" y="{y0}" width="{w}" height="{ground - y0}" fill="#8b7a5e"/>'
    leg = lambda x, y0: f'<rect x="{x - 12}" y="{y0}" width="24" height="{ground - y0}" fill="#7d7d78"/>'
    # Trailhead on a 4x4 post.
    parts += [post(1150, 150), place("trailhead", 250, 200)]
    # Yard sign on an H-stake, drawn with its 30 in wire stake.
    yard_y = ground - 1800 - 1000
    parts += [leg(2850, yard_y + 1700), leg(3850, yard_y + 1700), place("workday-yard", 2150, yard_y)]
    # Trail post with blaze and two arrows.
    # The arrows bolt on at their plain end and reach out from the post, like a fingerpost.
    parts += [post(6000, 600), place("trail-blaze", 5850, 720), place("trail-arrow-footbridge", 5822, 1400),
              place("trail-arrow-old-courts", 4778, 1850)]
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, help="folder holding the two variable font files")
    ap.add_argument("--date", default=DATE_LINE, help="workday date line text")
    args = ap.parse_args()

    fonts = Fonts(args.fonts)
    signs = build_signs(fonts, args.date)

    design_dir, cut_dir = HERE / "designs", HERE / "cut-untested"
    for d in (design_dir, cut_dir):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir()

    rows = []
    for name, sign in signs.items():
        w, h = sign["size"]
        svg = design_svg(sign)
        stem = f"{name}-{w}x{h}in"
        (design_dir / f"{stem}.svg").write_text(svg)
        render_png(svg, design_dir / f"{stem}.png", max(600, w * 60))
        for color in sorted({p.color for p in sign["pieces"]}):
            fixed = [p for p in sign["pieces"] if p.color == color and not p.swap]
            two_color = len({p.color for p in sign["pieces"]}) > 1
            (cut_dir / f"{name}__{color}.svg").write_text(cut_svg(sign, name, color, fixed, marks=two_color))
        for p in sign["pieces"]:
            rows.append(dict(sign=name, piece=p.id, color=p.color, width_in=round(p.w, 2), height_in=round(p.h, 2),
                             x_from_left_in=round(p.bounds[0] / 100, 2), y_from_top_in=round(p.bounds[1] / 100, 2),
                             vinyl_area_sq_in=round(p.area, 1), swappable=p.swap))

    # The swappable strips get their own files, so a new date never touches the rest.
    alt = Piece("date-line", "pale", text_path(fonts, ALT_DATE_LINE, "sans", 700, 155, 1200, 1520, "middle"), swap=True)
    yard = signs["workday-yard"]
    date_piece = next(p for p in yard["pieces"] if p.swap)
    (cut_dir / "workday-yard__date-line__pale.svg").write_text(cut_svg(yard, "workday-yard date line", "pale", [date_piece], marks=False))
    (cut_dir / "workday-yard__alt-join-us-today__pale.svg").write_text(cut_svg(yard, "workday-yard alternate strip", "pale", [alt], marks=False))
    rows.append(dict(sign="workday-yard", piece="alt-join-us-today", color="pale", width_in=round(alt.w, 2), height_in=round(alt.h, 2),
                     x_from_left_in=round(alt.bounds[0] / 100, 2), y_from_top_in=round(alt.bounds[1] / 100, 2),
                     vinyl_area_sq_in=round(alt.area, 1), swappable=True))

    # A small first cut: the two thinnest lines, plus a 2 in square to check the scale.
    test = pathops.Path()
    test.addPath(rect_path(0, 0, 200, 200))
    thin_a = next(p for p in yard["pieces"] if p.id == "name-line-2")
    thin_b = next(p for p in signs["trailhead"]["pieces"] if p.id == "wra-line-1")
    a_path = transformed(thin_a.path, (1, 0, 0, 1, 230 - thin_a.bounds[0], -thin_a.bounds[1]))
    b_path = transformed(thin_b.path, (1, 0, 0, 1, 230 - thin_b.bounds[0], 180 - thin_b.bounds[1]))
    (cut_dir / "test-cut-first.svg").write_text("\n".join([
        svg_open(17, 2.5), f"<!-- {UNTESTED} -->",
        "<title>Test cut: 2 in square plus the thinnest lettering. UNTESTED on a real cutter.</title>",
        f'<path id="scale-square-2in" fill="#000" d="{to_d(test)}"/>',
        f'<path id="yard-name-line" fill="#000" d="{to_d(a_path)}"/>',
        f'<path id="smallest-line" fill="#000" d="{to_d(b_path)}"/>',
        "</svg>"]))

    # Gang sheets for the initial run: one spare "Join us today" strip per yard sign.
    run_items = {"pale": [], "yellow": []}
    for name, sign in signs.items():
        for _ in range(RUN[name]):
            for p in sign["pieces"]:
                run_items[p.color].append((name, p))
    for _ in range(RUN["workday-yard"]):
        run_items["pale"].append(("workday-yard", alt))

    summary = {"run": RUN, "colors": {}}
    for color, items in run_items.items():
        info = {"pieces": len(items), "measured_sq_in": round(sum(p.area for _, p in items), 1),
                "piece_bbox_sq_in": round(sum(p.w * p.h for _, p in items), 1)}
        for label, width in (("12in", 11.5), ("24in", 23.0)):
            placed, length = gang(items, width)
            sheet_dir = cut_dir / f"gang-{label}"
            sheet_dir.mkdir(exist_ok=True)
            (sheet_dir / f"all-{color}-pieces.svg").write_text(gang_svg(color, placed, width, length))
            info[f"length_in_{label}"] = round(length, 1)
            info[f"longest_piece_in_{label}"] = round(max(max(p.w, p.h) for _, p in items), 1)
        summary["colors"][color] = info
    summary["per_sign"] = {}
    for name, sign in signs.items():
        per = {}
        for p in sign["pieces"]:
            per.setdefault(p.color, 0)
            per[p.color] += p.area
        summary["per_sign"][name] = {k: round(v, 1) for k, v in per.items()}

    with (HERE / "piece-placement.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (HERE / "cut-measurements.json").write_text(json.dumps(summary, indent=2) + "\n")

    sheet = contact_sheet(signs)
    render_png(sheet, design_dir / "all-signs-proof.png", 1600)
    fonts.close()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
