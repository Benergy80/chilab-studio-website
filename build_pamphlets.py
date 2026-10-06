#!/usr/bin/env python3
"""Project pamphlets for the ChiLab Studio site.

Writes work/<slug>-pamphlet.html: a print-ready, US Letter sheet document in
the site's own editorial system (Inter Tight, cream paper, oxide accent, the
five-column grid), plus pamphlets.html, the download index.

The HTML is the source of truth. make_pamphlet_pdfs.py renders each page to
assets/pdf/<slug>-pamphlet.pdf with headless Chrome.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(ROOT, "content")

# A pamphlet is a leave-behind, not the archive. Cap the plates so the longest
# project (18 images) does not turn into a fourteen-page document.
MAX_PLATES = 8


def e(s):
    return html.escape(str(s), quote=True)


def load():
    site = json.load(open(os.path.join(C, "site.json")))
    projects = json.load(open(os.path.join(C, "projects.json")))["projects"]
    manifest = json.load(open(os.path.join(C, "manifest.json")))
    for p in projects:
        p["plates"] = manifest.get(p["slug"], [])
        p["cover"] = p.get("cover") or (p["plates"][0]["src"] if p["plates"] else None)
    return site, projects


# ---------------------------------------------------------------- sheets

def run_head(p, site):
    return (f'<div class="run-head">'
            f'<div class="mark">{e(site["name"])}</div>'
            f'<div class="c-mid">{e(p["title"])}</div>'
            f'<div class="c-end">{e(p["cat"])}</div>'
            f'</div>')


def run_foot(p, site, no, total):
    return (f'<div class="run-foot">'
            f'<div>chilabstudio.com</div>'
            f'<div class="c-mid">{e(p["place"])} &nbsp;/&nbsp; {e(p["year"])}</div>'
            f'<div class="c-end">{no:02d} / {total:02d}</div>'
            f'</div>')


def title_class(title):
    n = len(title)
    if n > 34:
        return " xlong"
    if n > 20:
        return " long"
    return ""


def cover_sheet(p, site, no, total):
    shot = ""
    if p["cover"]:
        shot = (f'<div class="cover-shot">'
                f'<img src="../{e(p["cover"])}" alt="{e(p["title"])}"></div>')
    return f"""<section class="sheet">
{run_head(p, site)}
<div class="cover-body">
  <div class="cover-type">
    <p class="cover-kicker">{e(p['cat'])} &nbsp;/&nbsp; {e(p['year'])} &nbsp;/&nbsp; {e(p['place'])}</p>
    <h1 class="cover-title{title_class(p['title'])}">{e(p['title'])}</h1>
    <p class="cover-sub">{e(p['sub'])}</p>
  </div>
  {shot}
</div>
{run_foot(p, site, no, total)}
</section>"""


def text_sheet(p, site, no, total, band=None):
    meta = [("Year", p["year"]), ("Location", p["place"]),
            ("Category", p["cat"]), ("Materials", p["materials"])]
    rail = ('<section><h2>Details</h2><ul>' + "".join(
        f'<li>{e(k)}<br><span class="val">{e(v)}</span></li>' for k, v in meta)
        + '</ul></section>')
    if p["credits"]:
        rail += ('<section><h2>Credits</h2><ul>' + "".join(
            f'<li>{e(c)}</li>' for c in p["credits"]) + '</ul></section>')
    rail += ('<section><h2>Studio</h2><ul>'
             f'<li>{e(site["name"])}</li>'
             f'<li class="val">{e(site["city"])}</li>'
             f'<li class="val">Established {e(site["founded"])}</li>'
             '</ul></section>')
    if p.get("story"):
        # A case study reads in beats. Labelled sections, same small-caps rail
        # vocabulary as the metadata, so the page still reads as one system.
        body = "".join(
            f'<h3 class="beat">{e(sec["label"])}</h3>'
            + "".join(f"<p>{e(t)}</p>" for t in sec["text"])
            for sec in p["story"])
    else:
        body = "".join(f"<p>{e(t)}</p>" for t in p["body"])
    band_html = ""
    if band:
        band_html = (f'<div class="text-band">'
                     f'<img src="../{e(band["src"])}" alt="{e(p["title"])}">'
                     f'<figcaption class="no">01 &nbsp; {e(p["title"])}</figcaption>'
                     f'</div>')
    return f"""<section class="sheet">
{run_head(p, site)}
<div class="text-body">
  <p class="lede">{e(p['lead'])}</p>
  <div class="prose">{body}</div>
  <div class="rail">{rail}</div>
  {band_html}
</div>
{run_foot(p, site, no, total)}
</section>"""


def plate_pages(imgs):
    """Group plates into sheets so each sheet fills its page.

    Consecutive images of the same orientation form a run. Portraits chunk four
    to a sheet in a 2x2, landscapes two to a sheet stacked. Leftovers fall back
    to the pair or solo layout whose aspect ratio suits them. Every slot crops
    with object-fit, so nothing is ever stretched.
    """
    runs, cur = [], []
    for x in imgs:
        tall = x["h"] > x["w"]
        if cur and (cur[0]["h"] > cur[0]["w"]) != tall:
            runs.append(cur)
            cur = []
        cur.append(x)
    if cur:
        runs.append(cur)

    pages = []
    for run in runs:
        tall = run[0]["h"] > run[0]["w"]
        i = 0
        while i < len(run):
            left = len(run) - i
            if tall:
                take = 4 if left >= 4 else (2 if left >= 2 else 1)
                layout = {4: "quad", 2: "pair-tall", 1: "solo-tall"}[take]
            else:
                take = 2 if left >= 2 else 1
                layout = {2: "stack-2", 1: "solo-wide"}[take]
            pages.append((layout, run[i:i + take]))
            i += take
    return pages


def plate_sheet(p, site, layout, imgs, start_no, no, total):
    plates = "".join(
        f'<figure class="plate">'
        f'<img src="../{e(x["src"])}" alt="{e(p["title"])}, plate {start_no + n:02d}">'
        f'<figcaption class="no">{start_no + n:02d} &nbsp; {e(p["title"])}</figcaption>'
        f'</figure>'
        for n, x in enumerate(imgs))
    return f"""<section class="sheet">
{run_head(p, site)}
<div class="plates {layout}">{plates}</div>
{run_foot(p, site, no, total)}
</section>"""


def also_sheet(p, site, no, total, start):
    """Related work made for the same client that is not part of the story."""
    also = p["also"]
    plates = "".join(
        f'<figure class="plate">'
        f'<img src="../{e(src)}" alt="{e(also["label"])}, plate {start + n:02d}">'
        f'<figcaption class="no">{start + n:02d} &nbsp; {e(also["label"])}</figcaption>'
        f'</figure>'
        for n, src in enumerate(also["imgs"]))
    return f"""<section class="sheet">
{run_head(p, site)}
<div class="also-body">
  <div class="also-head"><h2>{e(also["label"])}</h2><p>{e(also["text"])}</p></div>
  <div class="plates stack-2">{plates}</div>
</div>
{run_foot(p, site, no, total)}
</section>"""


def close_sheet(p, site, no, total):
    # capabilities are [name, description] pairs; the pamphlet wants the names.
    caps = "".join(f'<li>{e(c[0])}</li>' for c in site["capabilities"][:8])
    return f"""<section class="sheet">
{run_head(p, site)}
<div class="close-body">
  <h2 class="close-title">Bring us a drawing,<br>a model, or a hunch.</h2>
  <div class="close-col close-a">
    <h2>The studio</h2>
    <p>{e(site['tagline'])}</p>
    <p>{e(site['name'])}, {e(site['city'])}. Established {e(site['founded'])}.</p>
  </div>
  <div class="close-col close-b">
    <h2>What we do</h2>
    <ul>{caps}</ul>
  </div>
  <div class="close-col close-c">
    <h2>Contact</h2>
    <p class="oxide">{e(site['email'])}</p>
    <p>chilabstudio.com</p>
    <p>Instagram @chilabstudio</p>
  </div>
</div>
{run_foot(p, site, no, total)}
</section>"""


# ---------------------------------------------------------------- documents

def build_pamphlet(p, site):
    also_imgs = set(p.get("also", {}).get("imgs", []))
    imgs = [x for x in p["plates"]
            if x["src"] != p["cover"] and x["src"] not in also_imgs][:MAX_PLATES]
    # Without a story the first plate rides the text sheet as a wide band, so a
    # short page does not end in white. A story fills the page on its own.
    band = imgs.pop(0) if imgs and not p.get("story") else None
    pages = plate_pages(imgs)
    total = 3 + len(pages) + (1 if p.get("also") else 0)
    sheets = [cover_sheet(p, site, 1, total),
              text_sheet(p, site, 2, total, band)]
    plate_no = 2 if band else 1
    for n, (layout, imgs) in enumerate(pages):
        sheets.append(plate_sheet(p, site, layout, imgs, plate_no, 3 + n, total))
        plate_no += len(imgs)
    if p.get("also"):
        sheets.append(also_sheet(p, site, total - 1, total, plate_no))
    sheets.append(close_sheet(p, site, total, total))

    title = f"{p['title']} pamphlet / {site['name']}"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(p['lead'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(p['lead'])}">
<meta property="og:type" content="article">
<link rel="icon" href="data:,">
<meta name="theme-color" content="#f4f3ef">
<link rel="stylesheet" href="../assets/css/pamphlet.css">
</head>
<body>
<div class="viewer-bar">
  <span class="name">{e(site['name'])} &nbsp;/&nbsp; {e(p['title'])}</span>
  <nav>
    <a href="../assets/pdf/{e(p['slug'])}-pamphlet.pdf" download>Download PDF</a>
    <a href="{e(p['slug'])}.html">Project page</a>
    <a href="../pamphlets.html">All pamphlets</a>
  </nav>
</div>
<main class="stack">
{''.join(sheets)}
</main>
</body>
</html>
"""
    open(os.path.join(ROOT, "work", p["slug"] + "-pamphlet.html"), "w").write(doc)
    return total


def build_index(site, projects, counts):
    rows = "".join(
        f'<li class="pamphlet-row">'
        f'<span class="c1">{e(p["cat"])}</span>'
        f'<span class="c2"><a href="work/{e(p["slug"])}-pamphlet.html">{e(p["title"])}</a>'
        f'<br><span class="sub">{e(p["sub"])}</span></span>'
        f'<span class="c3">{e(p["year"])}</span>'
        f'<span class="c4">{counts[p["slug"]]} pages</span>'
        f'<span class="c5"><a href="assets/pdf/{e(p["slug"])}-pamphlet.pdf" download>PDF</a></span>'
        f'</li>'
        for p in projects)
    return rows


def main():
    site, projects = load()
    os.makedirs(os.path.join(ROOT, "assets", "pdf"), exist_ok=True)
    counts = {p["slug"]: build_pamphlet(p, site) for p in projects}
    print(f"built {len(projects)} pamphlets, "
          f"{sum(counts.values())} sheets")
    return counts


if __name__ == "__main__":
    main()
