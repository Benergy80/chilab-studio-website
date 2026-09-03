#!/usr/bin/env python3
"""Static build for the ChiLab Studio site draft.

Reads content/site.json, content/projects.json and content/manifest.json,
writes index.html, studio.html, capabilities.html, news.html, contact.html,
work/index.html and work/<slug>.html.
"""
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(ROOT, "content")

site = json.load(open(os.path.join(C, "site.json")))
projects = json.load(open(os.path.join(C, "projects.json")))["projects"]
manifest = json.load(open(os.path.join(C, "manifest.json")))

for p in projects:
    p["plates"] = manifest.get(p["slug"], [])
    p["cover"] = p.get("cover") or (p["plates"][0]["src"] if p["plates"] else None)
    # Grid/index thumbnail. Defaults to the second plate so a project never shows
    # the same frame as its hero and its card on the same page.
    p["card"] = p.get("card") or (p["plates"][1]["src"] if len(p["plates"]) > 1
                                  else p["cover"])

BY_SLUG = {p["slug"]: p for p in projects}
FEATURED = ["ohare-terminal-5", "uber-spiral-stair", "uber-feature-wall",
            "st-nicholas-crosses", "skims", "illinois-state-capitol",
            "knoll-marquee", "magnificent-mile-tulips", "flight-of-butterflies"]
HOME_FEATURE = "ohare-terminal-5"

NAV = [("work/index.html", "Work"), ("studio.html", "Studio"),
       ("capabilities.html", "Capabilities"), ("news.html", "News"),
       ("contact.html", "Contact")]


def e(s):
    return html.escape(str(s), quote=True)


def rel(depth, path):
    return ("../" * depth) + path


def social_links():
    links = [f'<a href="{e(site["instagram"])}">Instagram</a>']
    if site.get("twitter"):
        links.append(f'<a href="{e(site["twitter"])}">Twitter</a>')
    return " &nbsp; ".join(links)


def theme_toggle():
    return ('<button class="theme-toggle" type="button" data-theme-toggle'
            ' aria-label="Switch colour theme">'
            '<span data-when="dark">Dark mode</span>'
            '<span data-when="light">Light mode</span></button>')


def slugify(value):
    return e(value.lower().replace(" ", "-"))


def head(title, desc, depth, page):
    nav = "".join(
        f'<a href="{rel(depth, href)}"{" aria-current=\"page\"" if href == page else ""}>{e(label)}</a>'
        for href, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="data:,">
<meta name="theme-color" content="#f4f3ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161614" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="{rel(depth, 'assets/css/site.css')}">
<script>(function(){{var t;try{{t=localStorage.getItem("chilab-theme")}}catch(e){{}}if(t!=="dark"&&t!=="light"){{t="light"}}document.documentElement.setAttribute("data-theme",t)}})();</script>
</head>
<body>
<header class="shell grid masthead">
  <a class="wordmark" href="{rel(depth, 'index.html')}">ChiLab Studio</a>
  <nav>{nav}</nav>
</header>
<main>
"""


def foot(depth):
    return f"""</main>
<footer class="shell grid site-foot">
  <div class="c1">ChiLab Studio, {e(site['city'])}. Established {e(site['founded'])}.</div>
  <div class="c2"><a href="mailto:{e(site['email'])}">{e(site['email'])}</a></div>
  <div class="c3">{social_links()}</div>
</footer>
<script src="{rel(depth, 'assets/js/site.js')}" defer></script>
</body>
</html>
"""


def rail_block(title, inner):
    return f'<section><h2>{e(title)}</h2>{inner}</section>'


def press_list(limit=None):
    """Press mentions. Publication links out when the piece is online."""
    items = site["press"][:limit] if limit else site["press"]
    rows = []
    for it in items:
        pub = e(it["pub"])
        if it.get("url"):
            pub = f'<a href="{e(it["url"])}" rel="noopener">{pub}</a>'
        rows.append(f'<li>{e(it["year"])} &nbsp; {pub}'
                    f'<br><span style="color:var(--muted)">{e(it["text"])}</span></li>')
    return "<ul>" + "".join(rows) + "</ul>"


def home_rail(depth):
    cats = {}
    for p in projects:
        cats.setdefault(p["cat"], 0)
        cats[p["cat"]] += 1
    parts = [
        rail_block("Studio", f'<p>{e(site["tagline"])}</p>'
                             f'<p><a href="{rel(depth, "studio.html")}">About the studio</a></p>'),
        rail_block("Contact", f'<p>{e(site["city"])}</p>'
                              f'<p><a href="mailto:{e(site["email"])}">{e(site["email"])}</a></p>'
                              f'<p><a href="{e(site["instagram"])}">Instagram</a></p>'),
        rail_block("Index", "<ul>" + "".join(
            f'<li><a href="{rel(depth, "work/index.html")}#{slugify(c)}">{e(c)}</a> '
            f'<span style="color:var(--muted)">{n}</span></li>'
            for c, n in sorted(cats.items())) + "</ul>"),
        rail_block("Press", press_list(limit=6)),
    ]
    return "".join(parts)


def project_fact_list(items):
    return "<ul>" + "".join(f"<li>{e(label)}<br><span>{e(value)}</span></li>"
                            for label, value in items) + "</ul>"


def feature_block(p, depth):
    if not p or not p["cover"]:
        return ""
    facts = project_fact_list([
        ("Project", p["title"]),
        ("Type", p["cat"]),
        ("Place", p["place"]),
        ("Material", p["materials"]),
    ])
    return f"""<div class="home-feature">
  <a class="feature-image" href="{rel(depth, 'work/' + p['slug'] + '.html')}">
    <img src="{rel(depth, p['cover'])}" alt="{e(p['title'])}" loading="eager" width="1600" height="1100">
  </a>
  <div class="feature-copy rail">
    <section>
      <h2>Featured project</h2>
      <p class="feature-title"><a href="{rel(depth, 'work/' + p['slug'] + '.html')}">{e(p['title'])}</a></p>
      <p>{e(p['lead'])}</p>
      {facts}
    </section>
  </div>
</div>"""


def process_figure(img, depth, wide=False):
    klass = "process-plate process-plate-wide" if wide else "process-plate"
    return f"""<figure class="{klass}">
  <div class="frame"><img src="{rel(depth, img['src'])}" alt="{e(img['alt'])}" loading="lazy" width="{img['w']}" height="{img['h']}"></div>
  <figcaption>{e(img['caption'])}</figcaption>
</figure>"""


def process_grid(items, depth):
    return '<div class="process-grid">' + "".join(
        process_figure(img, depth) for img in items) + "</div>"


def work_card(p, depth):
    if not p["cover"]:
        return ""
    return f"""<a class="work-card" href="{rel(depth, 'work/' + p['slug'] + '.html')}" data-cat="{e(p['cat'])}" data-preview="{rel(depth, p['card'])}">
  <figure>
    <div class="frame"><img src="{rel(depth, p['card'])}" alt="{e(p['title'])}" loading="lazy" width="1200" height="900"></div>
    <figcaption><span class="name">{e(p['title'])}</span><span class="meta">{e(p['year'])}</span></figcaption>
    <div class="sub">{e(p['sub'])}</div>
  </figure>
</a>"""


# ---------------------------------------------------------------- home
def build_home():
    depth = 0
    h1 = "".join(f"<span>{e(l)}</span>" for l in site["hero"])
    deck = "".join(
        f'<div><div class="label">{e(d["label"])}</div><p>{e(d["text"])}</p></div>'
        for d in site["deck"])
    cards = "".join(work_card(BY_SLUG[s], depth) for s in FEATURED if s in BY_SLUG)
    feature = feature_block(BY_SLUG.get(HOME_FEATURE), depth)
    caps = "".join(
        f'<li><strong>{e(t)}</strong><span>{e(d)}</span></li>' for t, d in site["capabilities"])
    clients = "".join(f"<li>{e(c)}</li>" for c in site["clients"])
    news = "".join(
        f'<li><strong>{e(n["title"])}</strong><span>{e(n["date"])}. {e(n["text"])}</span></li>'
        for n in site["news"][:2])

    out = head(f"{site['name']} / Material problem solving, Chicago",
               site["tagline"], depth, "index.html")
    out += f"""<section class="shell grid hero">
  <div class="hero-main">
    <p class="kicker">{e(site['city'])} &nbsp;/&nbsp; Established {e(site['founded'])}</p>
    <h1 class="display">{h1}</h1>
    <div class="deck">{deck}</div>
  </div>
  <div class="hero-rail rail">{theme_toggle()}{home_rail(depth)}</div>
</section>

<section class="shell grid picture-ledger">
  <p class="section-no">00</p>
  <div class="section-body">
    <h2 class="section-title">Make it Cool, Make it Real.</h2>
    <p class="section-lede">Project development, specialty material fabrication, and installation for work that has to survive scale, weather, code, schedule, and scrutiny.</p>
  </div>
  <div class="section-rail rail">
    <section><h2>Materials</h2><p>Bronze, aluminum, iron, glass, marble, steel, light, finish, and the shop drawings that hold them together.</p></section>
  </div>
  <div class="section-wide">{feature}</div>
</section>

<section class="shell grid section">
  <p class="section-no">01</p>
  <div class="section-body">
    <h2 class="section-title">{e(site['sections']['works']['title'])}</h2>
    <p class="section-lede">{e(site['sections']['works']['lede'])}</p>
  </div>
  <div class="section-rail rail">
    <section><h2>All work</h2><p><a href="work/index.html">Index of {len(projects)} projects</a></p></section>
  </div>
  <div class="section-wide"><div class="works">{cards}</div>
    <p style="margin-top:var(--row)"><a href="work/index.html" style="font-weight:700;text-decoration:underline;text-underline-offset:4px">See all work</a></p>
  </div>
</section>

<section class="shell grid section">
  <p class="section-no">02</p>
  <div class="section-body">
    <h2 class="section-title">{e(site['sections']['capabilities']['title'])}</h2>
    <p class="section-lede">{e(site['sections']['capabilities']['lede'])}</p>
    <ul class="cap-list">{caps}</ul>
  </div>
  <div class="section-rail rail">
    <section><h2>More</h2><p><a href="capabilities.html">Capabilities in detail</a></p></section>
  </div>
  <div class="section-wide">{process_grid(site['process_images']['capabilities'], depth)}</div>
</section>

<section class="shell grid section">
  <p class="section-no">03</p>
  <div class="section-body">
    <h2 class="section-title">{e(site['sections']['studio']['title'])}</h2>
    <p class="section-lede">{e(site['sections']['studio']['lede'])}</p>
    <p style="max-width:62ch">{e(site['studio_body'][1])}</p>
    <p><a href="studio.html" style="font-weight:700;text-decoration:underline;text-underline-offset:4px">Read more</a></p>
  </div>
  <div class="section-rail rail">
    <section><h2>Recent</h2><ul class="stack-list">{news}</ul></section>
  </div>
  <div class="section-wide">{process_figure(site['process_images']['studio'], depth, wide=True)}</div>
  <div class="section-wide client-band">
    <div class="label">Selected clients and collaborators</div>
    <ul>{clients}</ul>
  </div>
</section>

<section class="shell grid section">
  <p class="section-no">04</p>
  <div class="section-body">
    <h2 class="section-title">{e(site['sections']['contact']['title'])}</h2>
    <p class="section-lede">{e(site['sections']['contact']['lede'])}</p>
  </div>
  <div class="section-rail rail">
    <section><h2>Studio</h2><p>{e(site['city'])}</p></section>
  </div>
  <div class="section-wide">
    <p class="contact-big" style="grid-column:auto"><a href="mailto:{e(site['email'])}">{e(site['email'])}</a></p>
  </div>
</section>
"""
    out += foot(depth)
    open(os.path.join(ROOT, "index.html"), "w").write(out)


# ---------------------------------------------------------------- work index
def build_work_index():
    depth = 1
    cats = sorted({p["cat"] for p in projects})
    filters = '<button aria-pressed="true" data-cat="all">All</button>' + "".join(
        f'<button id="{slugify(c)}" aria-pressed="false" data-cat="{e(c)}">{e(c)}</button>' for c in cats)
    rows = "".join(
        f'<a class="index-row" href="{e(p["slug"])}.html" data-cat="{e(p["cat"])}" data-preview="{rel(depth, p["card"])}">'
        f'<span class="no">{i:02d}</span>'
        f'<span class="t">{e(p["title"])}</span>'
        f'<span class="c">{e(p["cat"])}</span>'
        f'<span class="p">{e(p["place"])}</span>'
        f'<span class="y">{e(p["year"])}</span></a>'
        for i, p in enumerate(projects, 1))
    cards = "".join(work_card(p, depth) for p in projects)

    out = head(f"Work / {site['name']}",
               f"Index of {len(projects)} projects by ChiLab Studio.", depth, "work/index.html")
    out += f"""<section class="shell grid hero">
  <div class="hero-main">
    <p class="kicker">Index &nbsp;/&nbsp; {len(projects)} projects</p>
    <h1 class="display"><span>Work</span></h1>
  </div>
  <div class="hero-rail rail">{theme_toggle()}
    <section><h2>Note</h2><p>Projects produced by ChiLab Studio and its directors, including earlier work from the studio's glass practice.</p></section>
  </div>
</section>

<section class="shell">
  <div class="filters" id="filters">{filters}</div>
  <div class="index-preview-layout">
    <div class="index-list" id="rows">{rows}</div>
    <figure class="index-preview" aria-hidden="true">
      <img id="index-preview-img" src="{rel(depth, projects[0]['card'])}" alt="">
    </figure>
  </div>
  <div class="works" id="cards" style="margin-top:var(--row)">{cards}</div>
</section>
"""
    out += foot(depth)
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    open(os.path.join(ROOT, "work", "index.html"), "w").write(out)


# ---------------------------------------------------------------- project
def build_project(p, prev, nxt):
    depth = 1
    meta = [("Year", p["year"]), ("Location", p["place"]),
            ("Category", p["cat"]), ("Materials", p["materials"])]
    rail = rail_block("Details", "<ul>" + "".join(
        f'<li>{e(k)}<br><span style="color:var(--muted)">{e(v)}</span></li>' for k, v in meta) + "</ul>")
    if p["credits"]:
        rail += rail_block("Credits", "<ul>" + "".join(
            f'<li>{e(c)}</li>' for c in p["credits"]) + "</ul>")
    rail += rail_block("Index", f'<p><a href="index.html">All work</a></p>')

    body = "".join(f"<p>{e(t)}</p>" for t in p["body"])

    plates = []
    rest = p["plates"][1:]
    if p["plates"]:
        f0 = p["plates"][0]
        plates.append(
            f'<figure class="plate-wide"><div class="frame">'
            f'<img src="{rel(depth, f0["src"])}" alt="{e(p["title"])}" width="{f0["w"]}" height="{f0["h"]}"></div></figure>')
    i = 0
    while i < len(rest):
        a = rest[i]
        b = rest[i + 1] if i + 1 < len(rest) else None
        portrait_pair = b and a["h"] > a["w"] and b["h"] > b["w"]
        if portrait_pair:
            for x in (a, b):
                plates.append(
                    f'<figure class="plate-half"><div class="frame">'
                    f'<img src="{rel(depth, x["src"])}" alt="{e(p["title"])}" loading="lazy" width="{x["w"]}" height="{x["h"]}"></div></figure>')
            i += 2
        else:
            plates.append(
                f'<figure class="plate-main"><div class="frame">'
                f'<img src="{rel(depth, a["src"])}" alt="{e(p["title"])}" loading="lazy" width="{a["w"]}" height="{a["h"]}"></div></figure>')
            i += 1

    out = head(f"{p['title']} / {site['name']}", p["lead"], depth, "work/index.html")
    out += f"""<article>
<section class="shell grid project-head">
  <p class="kicker" style="grid-column:1 / 5">{e(p['cat'])} &nbsp;/&nbsp; {e(p['year'])}</p>
  <h1 class="project-title">{e(p['title'])}</h1>
  <p class="project-sub">{e(p['sub'])}</p>
  <div class="project-body">
    <p class="project-lede">{e(p['lead'])}</p>
    {body}
  </div>
  <div class="project-rail rail">{theme_toggle()}{rail}</div>
</section>

<section class="shell grid plates">{''.join(plates)}</section>

<section class="shell">
  <nav class="pager">
    <span>{f'<a href="{e(prev["slug"])}.html">&larr; {e(prev["title"])}</a>' if prev else ''}</span>
    <span>{f'<a href="{e(nxt["slug"])}.html">{e(nxt["title"])} &rarr;</a>' if nxt else ''}</span>
  </nav>
</section>
</article>
"""
    out += foot(depth)
    open(os.path.join(ROOT, "work", p["slug"] + ".html"), "w").write(out)


# ---------------------------------------------------------------- simple pages
def build_studio():
    depth = 0
    body = "".join(f"<p>{e(t)}</p>" for t in site["studio_body"])
    out = head(f"Studio / {site['name']}", site["tagline"], depth, "studio.html")
    out += f"""<section class="shell grid hero">
  <div class="hero-main">
    <p class="kicker">About</p>
    <h1 class="display"><span>Studio</span></h1>
    {process_figure(site['process_images']['studio'], depth, wide=True)}
  </div>
  <div class="hero-rail rail">{theme_toggle()}
    {rail_block("Founded", f"<p>{e(site['founded'])}, {e(site['city'])}</p>")}
    {rail_block("Contact", f'<p><a href="mailto:{e(site["email"])}">{e(site["email"])}</a></p>')}
    {rail_block("Press", press_list())}
  </div>
</section>

<section class="shell grid section">
  <p class="section-no">01</p>
  <div class="section-body prose" style="grid-column:2 / 5">{body}</div>
  <div class="section-rail rail">
    {rail_block("Selected clients", "<ul>" + "".join(f"<li>{e(c)}</li>" for c in site["clients"]) + "</ul>")}
  </div>
</section>
"""
    out += foot(depth)
    open(os.path.join(ROOT, "studio.html"), "w").write(out)


def build_capabilities():
    depth = 0
    caps = "".join(f'<li><strong>{e(t)}</strong><span>{e(d)}</span></li>' for t, d in site["capabilities"])
    out = head(f"Capabilities / {site['name']}", site["sections"]["capabilities"]["lede"],
               depth, "capabilities.html")
    out += f"""<section class="shell grid hero">
  <div class="hero-main">
    <p class="kicker">What the shop does</p>
    <h1 class="display"><span>Capabilities</span></h1>
    <p class="section-lede" style="margin-top:var(--row)">{e(site['sections']['capabilities']['lede'])}</p>
  </div>
  <div class="hero-rail rail">{theme_toggle()}
    {rail_block("Work", '<p><a href="work/index.html">See the index</a></p>')}
    {rail_block("Enquiries", f'<p><a href="mailto:{e(site["email"])}">{e(site["email"])}</a></p>')}
  </div>
</section>

<section class="shell grid section">
  <p class="section-no">01</p>
  <div class="section-body"><ul class="cap-list">{caps}</ul></div>
  <div class="section-wide">{process_grid(site['process_images']['capabilities'], depth)}</div>
</section>
"""
    out += foot(depth)
    open(os.path.join(ROOT, "capabilities.html"), "w").write(out)


def news_lede(depth):
    """The newest news item that has a project, shown beside the press rail."""
    item = next((n for n in site["news"]
                 if n.get("link") and n["link"] in BY_SLUG), None)
    if not item:
        return ""
    p = BY_SLUG[item["link"]]
    if not p["cover"]:
        return ""
    href = rel(depth, "work/" + p["slug"] + ".html")
    return f"""<figure class="news-lede">
  <a href="{href}"><img src="{rel(depth, p['cover'])}" alt="{e(p['title'])}" loading="eager" width="1600" height="1100"></a>
  <figcaption>
    <span class="name"><a href="{href}">{e(p['title'])}</a></span>
    <span class="meta">{e(item['date'])}</span>
  </figcaption>
</figure>"""


def build_news():
    depth = 0
    items = ""
    for n in site["news"]:
        link = (f'<p style="margin-top:6px"><a href="work/{e(n["link"])}.html" '
                f'style="text-decoration:underline;text-underline-offset:3px">View the project</a></p>'
                if n["link"] else "")
        cov = n.get("coverage") or []
        if cov:
            links = ", ".join(f'<a href="{e(c["url"])}" rel="noopener" '
                              f'style="text-decoration:underline;text-underline-offset:3px">'
                              f'{e(c["pub"])}</a>' for c in cov)
            link += (f'<p style="margin-top:6px;color:var(--muted)">Coverage: {links}</p>')
        items += (f'<li><strong>{e(n["title"])}</strong>'
                  f'<span>{e(n["date"])}. {e(n["text"])}{link}</span></li>')
    out = head(f"News / {site['name']}", "Press and recent work from ChiLab Studio.", depth, "news.html")
    out += f"""<section class="shell grid hero">
  <div class="hero-main">
    <p class="kicker">Press and announcements</p>
    <h1 class="display"><span>News</span></h1>
    {news_lede(depth)}
  </div>
  <div class="hero-rail rail">{theme_toggle()}
    {rail_block("Follow", f'<p>{social_links()}</p>')}
    {rail_block("Press", press_list())}
  </div>
</section>

<section class="shell grid section">
  <p class="section-no">01</p>
  <div class="section-body"><ul class="cap-list">{items}</ul></div>
</section>
"""
    out += foot(depth)
    open(os.path.join(ROOT, "news.html"), "w").write(out)


def build_contact():
    depth = 0
    out = head(f"Contact / {site['name']}", site["sections"]["contact"]["lede"], depth, "contact.html")
    out += f"""<section class="shell grid hero">
  <div class="hero-main">
    <p class="kicker">Commissions and collaborations</p>
    <h1 class="display"><span>Contact</span></h1>
    <p class="section-lede" style="margin-top:var(--row)">{e(site['sections']['contact']['lede'])}</p>
  </div>
  <div class="hero-rail rail">{theme_toggle()}
    {rail_block("Studio", f"<p>{e(site['city'])}</p>")}
    {rail_block("Social", f'<p>{social_links()}</p>')}
  </div>
</section>

<section class="shell grid section">
  <p class="section-no">01</p>
  <div class="section-body">
    <h2 class="section-title">Write to us</h2>
    <p class="contact-big" style="grid-column:auto;margin-top:var(--tight)"><a href="mailto:{e(site['email'])}">{e(site['email'])}</a></p>
    <p style="max-width:52ch;margin-top:var(--row)">Useful things to include: what the piece is, how big, where it goes, when it has to be there, and any drawings or references you already have. Budget range helps more than it hurts.</p>
  </div>
  <div class="section-rail rail">
    {rail_block("Also", '<p><a href="capabilities.html">Capabilities</a></p><p><a href="work/index.html">Work index</a></p>')}
  </div>
</section>
"""
    out += foot(depth)
    open(os.path.join(ROOT, "contact.html"), "w").write(out)


def main():
    build_home()
    build_work_index()
    for i, p in enumerate(projects):
        build_project(p, projects[i - 1] if i else None,
                      projects[i + 1] if i + 1 < len(projects) else None)
    build_studio()
    build_capabilities()
    build_news()
    build_contact()
    pages = 6 + 1 + len(projects)
    print(f"built {pages} pages, {sum(len(v) for v in manifest.values())} images")


if __name__ == "__main__":
    main()
