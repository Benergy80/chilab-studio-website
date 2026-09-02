#!/usr/bin/env python3
"""Download project images to assets/img/<slug>/ and record local paths."""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
data = json.load(open(os.path.join(ROOT, "content", "projects.json")))

def url_for(u):
    if "squarespace-cdn.com" in u:
        return u + "?format=2000w"
    return u

def grab(args):
    slug, i, u = args
    d = os.path.join(IMG, slug)
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, f"{i:02d}.jpg")
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        return slug, i, True
    r = subprocess.run(["curl", "-sL", "--max-time", "60", url_for(u), "-o", dst],
                       capture_output=True)
    ok = r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 5000
    if not ok and os.path.exists(dst):
        os.remove(dst)
    return slug, i, ok

jobs = []
for p in data["projects"]:
    for i, u in enumerate(p["imgs"], 1):
        jobs.append((p["slug"], i, u))

with ThreadPoolExecutor(max_workers=12) as ex:
    results = list(ex.map(grab, jobs))

failed = [(s, i) for s, i, ok in results if not ok]
print(f"downloaded {len(results)-len(failed)}/{len(results)}; failed: {failed}")
