#!/usr/bin/env python3
"""Normalize downloaded images and write content/manifest.json with dimensions."""
import json, os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
MAXW = 1800
data = json.load(open(os.path.join(ROOT, "content", "projects.json")))

manifest = {}
dropped = []
for p in data["projects"]:
    slug = p["slug"]
    d = os.path.join(IMG, slug)
    entries = []
    if not os.path.isdir(d):
        manifest[slug] = entries
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".jpg"):
            continue
        path = os.path.join(d, fn)
        try:
            im = Image.open(path)
            im = ImageOps.exif_transpose(im).convert("RGB")
        except Exception:
            os.remove(path); dropped.append(f"{slug}/{fn}"); continue
        w, h = im.size
        if w < 600 or h < 400:
            os.remove(path); dropped.append(f"{slug}/{fn} ({w}x{h})"); continue
        if w > MAXW:
            h = round(h * MAXW / w); w = MAXW
            im = im.resize((w, h), Image.LANCZOS)
        im.save(path, "JPEG", quality=82, optimize=True, progressive=True)
        entries.append({"src": f"assets/img/{slug}/{fn}", "w": w, "h": h})
    manifest[slug] = entries

json.dump(manifest, open(os.path.join(ROOT, "content", "manifest.json"), "w"), indent=1)
total = sum(len(v) for v in manifest.values())
empty = [k for k, v in manifest.items() if not v]
print(f"{total} images kept across {len(manifest)} projects; dropped {len(dropped)}")
for x in dropped: print("  drop", x)
if empty: print("EMPTY:", empty)
