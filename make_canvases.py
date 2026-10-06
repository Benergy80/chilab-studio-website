#!/usr/bin/env python3
"""Turn a built pamphlet into Claude Design canvas working files.

One canvas per project: every pamphlet sheet becomes a .dc.html artboard at
816x1056 (US Letter at 96 px/inch), laid out in a row by canvas.json.

Geometry mirrors assets/css/pamphlet.css exactly, converted pt -> px at 4/3,
inches -> px at 96, and written as inline styles so the canvas properties
panel can edit them.
"""
import base64
import json
import os
import shutil
import subprocess
import sys

import build_pamphlets as bp

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "design", "canvas")
FONT = os.path.join(ROOT, "assets", "fonts", "inter-tight-latin.woff2")

PAGE_W, PAGE_H = 816, 1056
PAD, GAP = 48, 18
INNER_W = PAGE_W - 2 * PAD            # 720
COL = (INNER_W - 4 * GAP) / 5         # 129.6

INK, PAPER, MUTED = "#20201d", "#f4f3ef", "#77756e"
RULE, PANEL, OXIDE = "#2a2a28", "#e8e5dc", "#9f3f27"
STACK = "'Inter Tight', 'Arial Narrow', Arial, Helvetica, sans-serif"

IMG_BUDGET = 70000


def pt(v):
    """Points to CSS px at 96 px/inch."""
    return round(v * 4 / 3, 2)


def e(s):
    return bp.e(s)


# ---------------------------------------------------------------- images

def downsample(src, dest, budget=IMG_BUDGET):
    """Shrink a plate until it fits the canvas per-file budget."""
    for width, quality in ((1100, 60), (1000, 50), (900, 45), (800, 38), (700, 30)):
        subprocess.run(["sips", "-Z", str(width), "-s", "format", "jpeg",
                        "-s", "formatOptions", str(quality), src, "--out", dest],
                       capture_output=True, check=True)
        if os.path.getsize(dest) <= budget:
            return os.path.getsize(dest)
    return os.path.getsize(dest)


# ---------------------------------------------------------------- chrome

def font_face():
    b64 = base64.b64encode(open(FONT, "rb").read()).decode()
    return (f"@font-face{{font-family:'Inter Tight';font-style:normal;"
            f"font-weight:100 900;font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")


def shell(inner, title):
    """One artboard: the sheet, its embedded face, and nothing else."""
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
    {font_face()}
    body {{ margin: 0; font-family: {STACK}; }}
    a {{ color: {OXIDE}; }} a:hover {{ color: {INK}; }}
  </style>
</helmet>
<div style="width: {PAGE_W}px; height: {PAGE_H}px; padding: {PAD}px; background: {PAPER}; color: {INK}; font-family: {STACK}; font-size: {pt(10)}px; line-height: 1.32; display: flex; flex-direction: column; box-sizing: border-box; overflow: hidden;">
{inner}
</div>
</x-dc>
</body>
</html>
"""


def band(p, side, no=None, total=None):
    """Running head or foot."""
    edge = (f"border-bottom: 1px solid {RULE}; padding-bottom: 6px;" if side == "head"
            else f"border-top: 1px solid {RULE}; padding-top: 6px;")
    if side == "head":
        a, b, c = e(SITE["name"]), e(p["title"]), e(p["cat"])
    else:
        a = "chilabstudio.com"
        b = f'{e(p["place"])} &nbsp;/&nbsp; {e(p["year"])}'
        c = f"{no:02d} / {total:02d}"
    strong = f"color: {INK}; font-weight: 700; letter-spacing: 0; text-transform: none;"
    return (f'<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); '
            f'gap: {GAP}px; align-items: baseline; font-size: {pt(7.5)}px; line-height: 1.1; '
            f'letter-spacing: 0.06em; text-transform: uppercase; color: {MUTED}; {edge}">'
            f'<div style="{strong if side == "head" else ""}">{a}</div>'
            f'<div style="grid-column: 2 / 5;">{b}</div>'
            f'<div style="grid-column: 5; text-align: right;">{c}</div>'
            f'</div>')


def img(src, alt, extra=""):
    return (f'<img src="{src}" alt="{e(alt)}" style="width: 100%; height: 100%; '
            f'object-fit: cover; display: block; {extra}">')


def plate_no(n, title):
    return (f'<div style="position: absolute; left: 0; bottom: 0; padding: 4px 8px; '
            f'background: {PAPER}; font-size: {pt(7)}px; letter-spacing: 0.06em; '
            f'text-transform: uppercase; color: {MUTED};">{n:02d} &nbsp; {e(title)}</div>')


# ---------------------------------------------------------------- sheets

def cover(p, no, total, shot):
    cls = bp.title_class(p["title"])
    size = {" xlong": pt(31), " long": pt(40)}.get(cls, pt(52))
    shot_html = ""
    if shot:
        shot_html = (f'<div style="margin-top: 23px; flex: 1; min-height: 0; '
                     f'overflow: hidden; background: {PANEL};">{img(shot, p["title"])}</div>')
    return shell(
        band(p, "head") +
        f'<div style="flex: 1; min-height: 0; display: flex; flex-direction: column; padding: 27px 0 19px;">'
        f'<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: {GAP}px;">'
        f'<div style="grid-column: 1 / 6; margin: 0 0 13px; font-size: {pt(8)}px; letter-spacing: 0.07em; '
        f'text-transform: uppercase; color: {OXIDE}; font-weight: 600;">'
        f'{e(p["cat"])} &nbsp;/&nbsp; {e(p["year"])} &nbsp;/&nbsp; {e(p["place"])}</div>'
        f'<h1 style="grid-column: 1 / 6; margin: 0; font-weight: 900; font-size: {size}px; '
        f'line-height: 0.92; letter-spacing: -0.015em;">{e(p["title"])}</h1>'
        f'<p style="grid-column: 1 / 5; margin: 11px 0 0; font-size: {pt(13)}px; line-height: 1.14; '
        f'color: {MUTED}; max-width: 34ch;">{e(p["sub"])}</p>'
        f'</div>{shot_html}</div>' +
        band(p, "foot", no, total),
        p["title"])


def text(p, no, total, band_img):
    meta = [("Year", p["year"]), ("Location", p["place"]),
            ("Category", p["cat"]), ("Materials", p["materials"])]
    def rail_sec(h, items):
        lis = "".join(f'<li style="margin-bottom: 3px;">{x}</li>' for x in items)
        return (f'<div style="padding-top: 5px; margin-bottom: 14px; border-top: 1px solid {RULE};">'
                f'<h2 style="margin: 0 0 5px; font-size: {pt(7.5)}px; text-transform: uppercase; '
                f'letter-spacing: 0.06em; color: {MUTED}; font-weight: 500;">{h}</h2>'
                f'<ul style="list-style: none; margin: 0; padding: 0;">{lis}</ul></div>')

    rail = rail_sec("Details", [f'{e(k)}<br><span style="color: {MUTED};">{e(v)}</span>'
                                for k, v in meta])
    if p["credits"]:
        rail += rail_sec("Credits", [e(c) for c in p["credits"]])
    rail += rail_sec("Studio", [e(SITE["name"]),
                                f'<span style="color: {MUTED};">{e(SITE["city"])}</span>',
                                f'<span style="color: {MUTED};">Established {e(SITE["founded"])}</span>'])

    beat = (f'margin: 0 0 5px; padding-top: 5px; border-top: 1px solid #d6d2c8; '
            f'font-size: {pt(7.5)}px; text-transform: uppercase; letter-spacing: 0.06em; '
            f'color: {OXIDE}; font-weight: 600;')
    para = 'margin: 0 0 13px; max-width: 62ch;'
    if p.get("story"):
        body = "".join(
            f'<h3 style="{beat if i else beat.replace("padding-top: 5px; ", "").replace("border-top: 1px solid #d6d2c8; ", "")}">{e(sec["label"])}</h3>'
            + "".join(f'<p style="{para}">{e(t)}</p>' for t in sec["text"])
            for i, sec in enumerate(p["story"]))
    else:
        body = "".join(f'<p style="{para}">{e(t)}</p>' for t in p["body"])
    band_html = ""
    if band_img:
        band_html = (f'<div style="grid-column: 1 / 6; margin-top: 27px; aspect-ratio: 16 / 7; '
                     f'overflow: hidden; background: {PANEL}; position: relative;">'
                     f'{img(band_img, p["title"])}{plate_no(1, p["title"])}</div>')

    return shell(
        band(p, "head") +
        f'<div style="flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); '
        f'gap: {GAP}px; align-content: start; padding: 29px 0 0;">'
        f'<p style="grid-column: 1 / 5; margin: 0 0 25px; font-size: {pt(17)}px; line-height: 1.12; '
        f'font-weight: 500; max-width: 32ch;">{e(p["lead"])}</p>'
        f'<div style="grid-column: 1 / 4;">{body}</div>'
        f'<div style="grid-column: 4 / 6; font-size: {pt(8.5)}px; line-height: 1.2;">{rail}</div>'
        f'{band_html}</div>' +
        band(p, "foot", no, total),
        p["title"])


LAYOUTS = {
    "quad":      ("display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); "
                  "grid-template-rows: repeat(2, minmax(0, 1fr)); height: 100%;", None),
    "stack-2":   ("display: grid; grid-template-rows: repeat(2, minmax(0, 1fr)); height: 100%;", None),
    "pair-tall": ("display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); "
                  "align-content: center; height: 100%;", "aspect-ratio: 2 / 3;"),
    "solo-wide": ("display: grid; align-content: center; height: 100%;", "aspect-ratio: 3 / 2;"),
    "solo-tall": ("display: grid; justify-content: center; height: 100%;",
                  "aspect-ratio: 3 / 4; height: 100%; width: auto;"),
}


def plates(p, no, total, layout, shots, start):
    frame, slot = LAYOUTS[layout]
    cells = "".join(
        f'<figure style="position: relative; margin: 0; min-height: 0; overflow: hidden; '
        f'background: {PANEL}; {slot or ""}">{img(src, p["title"])}'
        f'{plate_no(start + i, p["title"])}</figure>'
        for i, src in enumerate(shots))
    return shell(
        band(p, "head") +
        f'<div style="flex: 1; min-height: 0; padding: 21px 0; {frame} gap: {GAP}px;">{cells}</div>' +
        band(p, "foot", no, total),
        p["title"])


def closing(p, no, total):
    def col(area, h, inner):
        return (f'<div style="grid-column: {area}; font-size: {pt(9)}px; line-height: 1.26;">'
                f'<h2 style="margin: 0 0 6px; padding-top: 5px; border-top: 1px solid {RULE}; '
                f'font-size: {pt(7.5)}px; text-transform: uppercase; letter-spacing: 0.06em; '
                f'color: {MUTED}; font-weight: 500;">{h}</h2>{inner}</div>')

    caps = "".join(f'<li style="margin-bottom: 3px; color: {MUTED};">{e(c[0])}</li>'
                   for c in SITE["capabilities"][:8])
    return shell(
        band(p, "head") +
        f'<div style="flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); '
        f'gap: {GAP}px; align-content: end; padding: 29px 0 24px;">'
        f'<h2 style="grid-column: 1 / 6; margin: 0 0 23px; font-weight: 900; font-size: {pt(30)}px; '
        f'line-height: 0.98; letter-spacing: -0.01em;">Bring us a drawing,<br>a model, or a hunch.</h2>'
        + col("1 / 3", "The studio",
              f'<p style="margin: 0 0 10px;">{e(SITE["tagline"])}</p>'
              f'<p style="margin: 0 0 10px;">{e(SITE["name"])}, {e(SITE["city"])}. '
              f'Established {e(SITE["founded"])}.</p>')
        + col("3 / 5", "What we do",
              f'<ul style="list-style: none; margin: 0; padding: 0;">{caps}</ul>')
        + col("5 / 6", "Contact",
              f'<p style="margin: 0 0 10px; color: {OXIDE};">{e(SITE["email"])}</p>'
              f'<p style="margin: 0 0 10px;">chilabstudio.com</p>'
              f'<p style="margin: 0 0 10px;">Instagram @chilabstudio</p>')
        + '</div>' +
        band(p, "foot", no, total),
        p["title"])


# ---------------------------------------------------------------- assembly

def build(p):
    d = os.path.join(OUT, p["slug"])
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)

    # every plate the pamphlet uses, downsampled to the canvas budget
    used, names = [], {}
    for x in [{"src": p["cover"]}] + [x for x in p["plates"] if x["src"] != p["cover"]][:bp.MAX_PLATES]:
        src = os.path.join(ROOT, x["src"])
        name = os.path.basename(x["src"])
        dest = os.path.join(d, name)
        downsample(src, dest)
        names[x["src"]] = name
        used.append(dest)

    rest = [x for x in p["plates"] if x["src"] != p["cover"]][:bp.MAX_PLATES]
    band_img = names[rest.pop(0)["src"]] if rest and not p.get("story") else None
    pages = bp.plate_pages(rest)
    total = 3 + len(pages)

    files = [("Main.dc.html", cover(p, 1, total, names.get(p["cover"]))),
             ("Text.dc.html", text(p, 2, total, band_img))]
    n = 2 if band_img else 1
    for i, (layout, imgs) in enumerate(pages, 1):
        files.append((f"Plates{i}.dc.html",
                      plates(p, 2 + i, total, layout, [names[x["src"]] for x in imgs], n)))
        n += len(imgs)
    files.append(("Closing.dc.html", closing(p, total, total)))

    for name, src in files:
        open(os.path.join(d, name), "w").write(src)

    boards = []
    for i, (name, _) in enumerate(files):
        boards.append({"file": name, "x": i * (PAGE_W + 100), "y": 0,
                       "w": PAGE_W, "h": PAGE_H, "print": "fixed"})
    json.dump({"artboards": boards, "launch": {"view": "canvas"}},
              open(os.path.join(d, "canvas.json"), "w"), indent=2)

    return d, [n for n, _ in files], used


def main():
    global SITE
    SITE, projects = bp.load()
    by = {p["slug"]: p for p in projects}
    slugs = sys.argv[1:] or [p["slug"] for p in projects]
    for slug in slugs:
        d, names, imgs = build(by[slug])
        weight = sum(os.path.getsize(i) for i in imgs)
        print(f"{slug:<26} {len(names)} artboards, {len(imgs)} images, {weight/1e6:.2f} MB")


if __name__ == "__main__":
    main()
