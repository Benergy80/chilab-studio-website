#!/usr/bin/env python3
"""Compose content/projects.json from scraped source material.

Sources (scraped once into /tmp/chilab-scrape):
  full.json  -> chilabstudio.com pages + selected benstagl.com pages
  rez.json   -> rezally.com works index
Copy is curated here; image lists are pulled from the source dumps.
"""
import json, os, re, sys

SRC = "/tmp/chilab-scrape"
full = json.load(open(f"{SRC}/full.json"))
rez = {p["url"]: p for p in json.load(open(f"{SRC}/rez.json"))}

def cl(page, n=None):
    return full[page]["imgs"][:n] if n else full[page]["imgs"]

def bs(page, n=None):
    return full["bs/" + page]["imgs"][:n] if n else full["bs/" + page]["imgs"]

def rz(key, n=None):
    return rez[key]["imgs"][:n] if n else rez[key]["imgs"]

def local(slug, count):
    return [f"assets/img/{slug}/{i:02d}.jpg" for i in range(1, count + 1)]

P = []

P.append(dict(
    slug="ohare-terminal-5", title="a murmuration", sub="Public artwork, O'Hare Terminal 5",
    year="2023", place="Chicago, IL", cat="Public Art",
    lead="Four hundred and fifty feet of wall in Terminal 5, and nearly six hundred convex aluminum discs charting two centuries of immigration to Illinois.",
    credits=["Artist: Jina Valentine", "Commissioned by DCASE and the Chicago Department of Aviation",
             "Finishing: EH Schwab, Pioneer Metal, Gatto Metal"],
    materials="Zinc plated steel, anodized aluminum",
    body=[
        "In the corridors of Chicago's O'Hare International Airport, a sweeping narrative of immigration and diversity unfolds across 450 feet of wall. \"a murmuration,\" conceived by artist Jina Valentine and brought to life by ChiLab Studio, is a piece of data visualization built at architectural scale.",
        "Using census data from 1850 to 2040, the installation translates demographic information into an array of colors and sizes. Nearly 600 convex aluminum discs were crafted, each varying to represent a different immigrant population and period. A color coding system ties each disc's hue to a continent of origin.",
        "Eighty of the discs carry engraved phrases contributed by community partners, in their own languages, on the themes of home, welcome, and community.",
        "Material selection was driven by the environment. Zinc plated steel and anodized aluminum were chosen for durability and finish stability in a high traffic terminal, and the install was sequenced around live airport operations.",
    ], imgs=cl("ohare-terminal-5.html")))

P.append(dict(
    slug="uber-spiral-stair", title="Grand Spiral Stair", sub="Uber Freight HQ, Old Post Office",
    year="2022", place="Chicago, IL", cat="Architectural",
    lead="A sixteen foot diameter stair finished in a custom blue toned patina, inspired by the building's historical spiral mail chutes.",
    credits=["Architect: Gensler Chicago", "Fabrication partner: Parenti & Raffaelli"],
    materials="Fabricated steel, custom blue patina, mirror",
    body=[
        "In the heart of Chicago's Old Post Office, now home to Uber Freight's headquarters, the Grand Spiral Stair is more than vertical circulation. It is a piece of the building's history returned in contemporary form.",
        "The geometry takes its cue from the spiral mail chutes that once moved letters through the building. The finish is a custom blue toned patina that reads close to oil rubbed bronze, and an infinity mirror at the top extends the spiral past the ceiling.",
        "Produced in collaboration with Gensler Chicago, the stair merges art, technology, and function inside a landmark structure.",
    ], imgs=cl("uber-freight.html")))

P.append(dict(
    slug="uber-feature-wall", title="Parametric Feature Wall", sub="Uber Freight HQ, Old Post Office",
    year="2021", place="Chicago, IL", cat="Architectural",
    lead="A cast metal wall derived from the bird's eye view of a shipping yard, modeled parametrically and cast component by component.",
    credits=["Architect: Gensler", "Fabrication partner: Parenti & Raffaelli"],
    materials="Cast aluminum",
    body=[
        "The wall draws from an unexpected source: the view of a shipping yard from space. The reference ties Uber Freight's mission directly to the architecture of its office.",
        "Using Grasshopper, we built a parametric model tuned to the exact constraints of the space, then sliced the model into individual cast components, each one unique but part of a continuous field.",
        "Mold creation was automated so the volume of unique parts stayed economical, and the castings were finished and assembled on site into a single continuous surface.",
    ], imgs=cl("uber-freight-wall.html")))

P.append(dict(
    slug="knoll-marquee", title="KNOLL Showroom Marquee", sub="811 W Fulton Market",
    year="2019", place="Chicago, IL", cat="Architectural",
    lead="Chrome tubes rising from the sixth floor to the seventh floor skylight, with the KNOLL name in dark bronze.",
    credits=["With CNL Projects, Gensler, and KNOLL"],
    materials="Chrome plated tube, dark bronze",
    body=[
        "In Chicago's West Loop, ChiLab produced an architectural sculpture that works as both a functional marquee and a brand statement for the KNOLL showroom.",
        "Chrome tubes arranged in a row soar from the 6th floor to the skylight on the 7th, creating a vertical presence that pulls the eye upward. The KNOLL name is spelled in dark bronze letters mounted to the tubes, tying the screen to the 24 foot bronze table that anchors the showroom floor.",
        "The chrome and bronze palette was chosen against the warm red marble of the entry, so the sculpture reads as part of the room rather than an object placed in it.",
        "The design is a nod to Harry Bertoia, whose work for KNOLL in the 1950s still sets the terms for the company's design language.",
    ], imgs=cl("knoll.html")))

P.append(dict(
    slug="st-nicholas-crosses", title="Glass Crosses", sub="St. Nicholas Greek Orthodox Church, National Shrine",
    year="2022", place="New York, NY", cat="Glass",
    lead="Four hundred and twenty hand cast and polished glass crosses set into Pentelic marble doors at the 9/11 Memorial.",
    credits=["Architect: Santiago Calatrava", "Glass: Ally Reza"],
    materials="Optically clear leaded glass, Pentelic marble",
    body=[
        "St. Nicholas Greek Orthodox Church sits within the National Shrine at Ground Zero. Taking part in the adornment of a monument with that weight went beyond Chicago or New York and into the national record.",
        "The crosses are cast from a high quality, optically clear leaded glass chosen to capture and refract light. Each one was cast, cold worked, and polished by hand, then set into CNC machined openings in the Pentelic marble doors.",
        "The work demanded technical precision and an understanding of what the crosses would mean once installed.",
    ], imgs=local("st-nicholas-crosses", 18)))

P.append(dict(
    slug="st-nicholas-icon-stands", title="Icon Stands", sub="St. Nicholas Greek Orthodox Church, National Shrine",
    year="2022", place="New York, NY", cat="Architectural",
    lead="Matching pairs of bronze pedestals at the chapel entry, engineered with Santiago Calatrava.",
    credits=["Architect: Santiago Calatrava"],
    materials="Cast and fabricated bronze, Pentelic marble",
    body=[
        "The gravity defying stature of the pedestal design was an engineering problem as much as a design one, resolved in collaboration with Santiago Calatrava.",
        "In matching pairs, the bronze pedestals serve the entryway of the chapel, ordained with iconographic tablets. As guests enter, the pedestals function as bases for prayer.",
        "Contemporary metalworking meets an ancient stone: the pedestals carry Pentelic marble, the same quarry that supplied the Parthenon.",
    ], imgs=cl("st-nicholas-podiums.html")))

P.append(dict(
    slug="illinois-state-capitol", title="Illinois State Capitol Handrails", sub="Office of the Architect of the Capitol",
    year="2018", place="Springfield, IL", cat="Restoration",
    lead="Circa 1870 iron handrails on the fourth floor gallery, restored and brought to ADA compliance without losing their period character.",
    credits=["Office of the Architect of the Capitol"],
    materials="Cast iron, bronze, milled hardwood",
    body=[
        "After removing layers of failing faux paint and documenting dozens of missing or broken ornamental pieces, we digitally modeled replacement components from archival profiles.",
        "New upper ornamental details and toe kick elements were developed as 3D models, then translated into match plate sand patterns with engineered gating. Masters were 3D printed directly into the pattern boards, molded in resin bonded sand, and cast in iron to integrate with the originals.",
        "For repairs to original rail sections, lost wax reproductions of missing details were produced, assembled, and patinated to match the existing finish.",
        "A custom mill worked wooden handrail cap was fitted atop the ironwork, providing both a crown and the height required for ADA compliance.",
    ], imgs=cl("il-state-capital.html")))

P.append(dict(
    slug="flight-of-butterflies", title="Flight of Butterflies", sub="Peggy Notebaert Nature Museum",
    year="2024", place="Chicago, IL", cat="Public Art",
    lead="Twenty nine cast aluminum butterfly sculptures installed across Chicago, each finished by a local artist.",
    credits=["Peggy Notebaert Nature Museum", "29 Chicago artists"],
    materials="Cast aluminum, steel, artist applied finishes",
    body=[
        "Flight of Butterflies features 29 uniquely adorned butterfly sculptures installed across Chicago, from Lakeview to South Shore to Austin. Our team designed and crafted the butterflies, providing the foundation for local artists to embellish and bring them to life.",
        "Each butterfly was digitally designed in two motifs, the Regal Fritillary and the Black Swallowtail, then 3D rendered to produce molds for the cast aluminum bodies. Custom CNC cut wood served as the positive for the molds, which kept production controlled given the quantity and the schedule.",
        "Every casting was hand finished to a state that would take paint, so each artist could work directly on the surface.",
        "Where an artist's work had not been built for the outdoors, we supplied material samples and methods that kept their idea intact while making it survive a Chicago year.",
    ], imgs=cl("flightofthebutterflies.html")))

P.append(dict(
    slug="magnificent-mile-tulips", title="Tulips on The Magnificent Mile", sub="The Magnificent Mile Association",
    year="2025", place="Chicago, IL", cat="Public Art",
    lead="Five oversized tulip sculptures placed along Michigan Avenue for the city's annual spring bloom.",
    credits=["The Magnificent Mile Association", "CNL Projects", "Artist: Aiden Kelley"],
    materials="Fabricated metal, automotive finish",
    body=[
        "In the spring of 2025, in partnership with The Magnificent Mile Association and CNL Projects, we developed five custom tulip sculptures with artist Aiden Kelley for the city's signature street.",
        "Chicago's annual tulip bloom blankets the Mile with color. These sculptures were an opportunity to put public sculpture and Chicago's floral tradition in the same frame.",
        "Each tulip was installed at a different point along the stretch. The sculpture at 625 N. Michigan Avenue shows the Official Magnificent Mile Tulip in brilliant yellow with orange accents, cultivated specifically for Michigan Avenue's displays and bred to hold up in Chicago's unpredictable spring.",
    ], imgs=cl("magnificent-mile-tulips.html")))

P.append(dict(
    slug="skims", title="SKIMS Storefronts", sub="Cast glass window displays",
    year="2024", place="Miami, Atlanta, Houston", cat="Glass",
    lead="Cast glass logo displays engineered for the brand's first brick and mortar storefronts.",
    credits=["Design: Willo Perron, Perron-Roettinger Studio", "Glass: Ally Reza", "Lamination and install: AGNORA"],
    materials="Cast glass, laminated architectural glass",
    body=[
        "In 2024 we developed storefront displays for SKIMS locations across the US. The project was a union of artistic vision and large scale engineering, and it pushed the limits of architectural glass fabrication.",
        "Designed by Willo Perron of Perron-Roettinger Studio, the logo appears to emerge from the storefront window, a sleek effect in keeping with the brand.",
        "Bringing it to life took the combined expertise of Perron-Roettinger Studio, ChiLab Studio, and AGNORA, North America's leader in large format glass. Traditional casting technique met contemporary lamination and structural glazing.",
    ], imgs=cl("skims.html")))

P.append(dict(
    slug="jardin-de-gargolas", title="Jardin de Gargolas", sub="YolloCalli Arts Reach",
    year="2024", place="Chicago, IL", cat="Public Art",
    lead="Student designed garden gargoyles taken from 3D model to cast aluminum sculpture.",
    credits=["YolloCalli Arts Reach", "Artist educator: Secret of Manna"],
    materials="Cast aluminum, dark patina",
    body=[
        "In collaboration with YolloCalli Arts Reach and artist educator Secret of Manna, we helped bring students' 3D digital garden gargoyle designs into the physical world.",
        "Starting in fall 2023, students conceptualized their creations in design software. By spring the project had become a fabrication and exhibition class. We printed the sculptures in house and prepared them for casting.",
        "The 3D printed sculptures became the positive for a resin sand mold system, a lost PLA process that gives a direct translation between the digital design and its metal duplicate.",
        "Once cast, the gargoyle pieces were welded together and finished with a dark patina.",
    ], imgs=cl("jardin-de-gargolas.html")))

P.append(dict(
    slug="homebound", title="Homebound", sub="Leonard Suryajaya, E(art)h Chicago",
    year="2023", place="Chicago, IL", cat="Public Art",
    lead="A CNC cut aluminum collage in Grant Park, built to survive a Chicago spring.",
    credits=["Artist: Leonard Suryajaya", "E(art)h Chicago"],
    materials="CNC cut aluminum, printed finish",
    body=[
        "In the spring of 2023 we collaborated with Chicago based photographer Leonard Suryajaya on Homebound, a public land art installation at the northern end of the Grant Park waterfront trail. Homebound was one of twelve pieces supported by the E(art)h Chicago collective and installed in neighborhoods across the city.",
        "Mirroring the collage language of Suryajaya's photographs, we used CNC cut aluminum panels pieced together as a three dimensional puzzle, translating work he had previously made in wrapped and layered materials into something that could live outdoors.",
        "The formation takes the shape of a Maneki-Neko, the lucky cat, surrounded by silhouettes of fruit, reading as a dismantled fruit stand and referencing the artist's upbringing in Indonesia.",
    ], imgs=cl("homebound.html")))

P.append(dict(
    slug="st-alfred", title="St. Alfred", sub="Wicker Park storefront",
    year="2023", place="Chicago, IL", cat="Retail",
    lead="Storefront redesign for the Wicker Park location, produced with Chelsea Lombardo.",
    credits=["With Chelsea Lombardo"], materials="Metal, glass, millwork",
    body=["Wicker Park storefront redesign produced in collaboration with Chelsea Lombardo."],
    imgs=cl("st-alfred.html")))

P.append(dict(
    slug="methodology-table", title="Methodology Table", sub="Solid cast glass end table, ongoing since 2016",
    year="2016", place="Private client", cat="Furniture",
    lead="A solid cast glass end table, produced in an ongoing series for a private client.",
    credits=["Glass: Ally Reza"], materials="Solid cast glass",
    body=["Solid cast glass end table for a private client. An ongoing fabrication relationship running from 2016 to the present."],
    imgs=cl("methodology-table.html") + rz("methodology")))

P.append(dict(
    slug="360-n-green", title="360 N Green Reception", sub="Sterling Bay",
    year="2024", place="Chicago, IL", cat="Architectural",
    lead="Reception desk for Sterling Bay at 360 N Green.",
    credits=["Sterling Bay"], materials="Metal, stone, millwork",
    body=["Reception desk at 360 N Green for Sterling Bay. Industrial design, architecture, and interior detailing carried through a single fabricated element."],
    imgs=cl("360.html")))

P.append(dict(
    slug="pritzker-reception-desk", title="Pritzker Group Reception Desk", sub="Bronze clad desk and credenza",
    year="2020", place="Chicago, IL", cat="Architectural",
    lead="Bronze clad reception desk and bronze framed credenza for the Pritzker Group offices.",
    credits=["Direction: Gensler", "With Imperial Woodworking and Lazuli Studio"],
    materials="Bronze, patina, hardwood",
    body=["Bronze clad reception desk and bronze framed credenza created for the Pritzker Group offices in Chicago. Developed and executed by ChiLab in collaboration with Imperial Woodworking and Lazuli Studio at the direction of Gensler."],
    imgs=bs("pritsker-group-reception-desk.html", 8)))

P.append(dict(
    slug="unfolding-chair", title="Solid Cast Bronze Unfolding Chair", sub="One hundred pounds of solid bronze",
    year="2013", place="WANTED DESIGN, New York", cat="Furniture",
    lead="The 1941 Krueger steel folding chair, cast solid in bronze and stripped of its ability to fold.",
    credits=["With Bo Rodda, Jason Gillette, Max Davis, Kuan Wen Chiu"],
    materials="Solid cast bronze",
    body=[
        "The Unfolding Chair takes a second look at what might be the most common chair ever made. The 1941 steel folding chair by Krueger Metal Products was designed for utility and economy, made from excess metal from steel companies, light enough to fold and nest, and commonly sold for two dollars.",
        "By producing the image of that chair in solid bronze and removing its ability to fold and nest, the design trades functional value for material value, thus unfolding the design.",
        "Exhibited at WANTED DESIGN NYC in the Chicagoland presentation.",
    ], imgs=bs("solid-cast-bronze-unfolding-chair.html")))

P.append(dict(
    slug="boolean-lamp", title="The Boolean Lamp and Pendant", sub="Industrial design, product design",
    year="2014", place="Chicago, IL", cat="Lighting",
    lead="A hand blown pendant and table lamp built from a boolean intersection of two primitive forms.",
    credits=[], materials="Hand blown glass, metal",
    body=["A lamp and pendant family developed in house, taking its geometry from the boolean intersection of two primitive volumes. Produced in hand blown glass and later scaled into the Kuma's West Loop interior."],
    imgs=bs("the-boolean-lamp-and-pendant.html")))



P.append(dict(
    slug="kumas-west-loop", title="Kuma's Corner West Loop", sub="Lighting, metalwork, furnishings",
    year="2018", place="Chicago, IL", cat="Retail",
    lead="Custom lighting, metalwork, furnishings, and artistic details for the Fulton Market location.",
    credits=[], materials="Hand blown glass, rusted steel, LED",
    body=[
        "Development and manufacture of custom lighting, metalwork, selected furnishings, and artistic details for the Kuma's Corner West Loop location at Peoria and Fulton Market.",
        "Hand blown Boolean pendants and custom below bar shadow boxes encircle the bar, with five larger Boolean pendants produced for the west wall portals. The below bar LED shadow boxes carry a rusted steel patina.",
    ], imgs=bs("kumas-west-loop.html")))

P.append(dict(
    slug="jail-debris", title="Jail Debris", sub="Maria Gaspar",
    year="2023", place="Chicago, IL", cat="Glass",
    lead="Twenty three cast lead crystal bars and bricks taken from a demolished Chicago corrections facility.",
    credits=["Artist: Maria Gaspar", "Glass: Ally Reza"],
    materials="Lead crystal, polished",
    body=["Rubber molds were taken from bars and bricks salvaged from a demolished Chicago corrections facility, then cast in lead crystal and polished on selected faces. Twenty three elements in total, produced for artist Maria Gaspar."],
    imgs=rz("jail-debris")))

P.append(dict(
    slug="palimpsest-apple", title="Apple", sub="Industry of the Ordinary",
    year="2024", place="Driehaus Museum, Chicago", cat="Glass",
    lead="A cast glass apple, molded from a freshly bitten one.",
    credits=["Industry of the Ordinary", "Glass: Ally Reza"],
    materials="Cast glass",
    body=["A rubber mold was taken from a freshly bitten apple, capturing the moment and the texture of the bite, then cast in glass for the artist collective Industry of the Ordinary."],
    imgs=rz("apple")))

P.append(dict(
    slug="star-award", title="Star Award", sub="Cast lead crystal trophy",
    year="2022", place="Chicago, IL", cat="Glass",
    lead="A cast lead crystal star for a national football league MVP, hand polished, masked, and etched.",
    credits=["Glass: Ally Reza"], materials="Lead crystal",
    body=["Cast lead crystal star form produced as an MVP award. Hand polished, masked, and etched."],
    imgs=rz("star-award")))

P.append(dict(
    slug="woven-vessels", title="Woven Vessels", sub="Candone Wharton",
    year="2022", place="Chicago, IL", cat="Glass",
    lead="Cast lead crystal vessels molded from the artist's earthenware originals.",
    credits=["Artist: Candone Wharton", "Glass: Ally Reza"], materials="Lead crystal",
    body=["Rubber molds were taken from Candone Wharton's earthenware sculptures and translated into cast lead crystal, carrying the woven surface of the original into a transparent material."],
    imgs=rz("woven-vessels")))

P.append(dict(
    slug="annular-sconce", title="Annular Sconce", sub="Fused glass and hammered bronze",
    year="2019", place="Chicago, IL", cat="Lighting",
    lead="A thirty inch diameter sconce in fused glass and hammered bronze.",
    credits=["Glass: Ally Reza"], materials="Fused glass, hammered bronze",
    body=["Fused glass and hammered bronze sconce, 30 inch diameter by 3 inch deep."],
    imgs=rz("annular-sconce-1")))

out = {"projects": P}
os.makedirs(os.path.dirname(__file__), exist_ok=True)
json.dump(out, open(os.path.join(os.path.dirname(__file__), "projects.json"), "w"), indent=1)
missing = [p["slug"] for p in P if not p["imgs"]]
print(f"{len(P)} projects, {sum(len(p['imgs']) for p in P)} images. missing imgs: {missing}")
