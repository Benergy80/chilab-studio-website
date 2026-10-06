#!/usr/bin/env python3
"""Seed a Claude Design canvas for every generated pamphlet working set."""
import json
import os
import re
import subprocess
import sys

import build_pamphlets as bp

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "design", "canvas")
SK = "/private/tmp/claude-501/bundled-skills/2.1.261/fb29064bb11427fc0defa591fc093436/design"


def order(names):
    """Main, Text, Plates1..N, Closing - the reading order of the pamphlet."""
    rank = {"Main.dc.html": 0, "Text.dc.html": 1, "Closing.dc.html": 99}
    def key(n):
        if n in rank:
            return rank[n]
        return 2 + int(re.search(r"(\d+)", n).group(1))
    return sorted(names, key=key)


def main():
    site, projects = bp.load()
    by = {p["slug"]: p for p in projects}
    slugs = sys.argv[1:] or [p["slug"] for p in projects]
    for slug in slugs:
        d = os.path.join(OUT, slug)
        boards = order([f for f in os.listdir(d) if f.endswith(".dc.html")])
        images = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
        out = f"{slug}-pamphlet.html"
        cmd = ["node", os.path.join(SK, "seed-canvas.mjs"),
               "--template", os.path.join(SK, "payload.template.html"),
               "--out", out,
               "--title", f'{by[slug]["title"]} Pamphlet',
               "--canvas", "canvas.json"]
        for b in boards:
            cmd += ["--artboard", b]
        for i in images:
            cmd += ["--image", i]
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
        if r.returncode:
            print(f"FAIL {slug}: {r.stderr.strip()[:300]}")
            continue
        chk = subprocess.run(["node", os.path.join(SK, "seed-canvas.mjs"), "--check", out],
                             cwd=d, capture_output=True, text=True)
        size = os.path.getsize(os.path.join(d, out)) / 1e6
        state = "ok" if chk.stdout.startswith("ok:") else "CHECK FAILED"
        print(f"{slug:<26} {len(boards)} boards  {size:5.2f} MB  {state}")
        if chk.stderr.strip():
            print(f"    warn: {chk.stderr.strip()[:200]}")


if __name__ == "__main__":
    main()
