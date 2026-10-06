#!/usr/bin/env python3
"""Render each work/<slug>-pamphlet.html to assets/pdf/<slug>-pamphlet.pdf.

Serves the repo over localhost first: headless Chrome will not load the
self-hosted woff2 faces from a file:// page, so a file:// render silently
falls back to Arial.
"""
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 8731


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    handler = partial(QuietHandler, directory=ROOT)
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render(slug):
    url = f"http://127.0.0.1:{PORT}/work/{slug}-pamphlet.html"
    dest = os.path.join(OUT, f"{slug}-pamphlet.pdf")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=20000",
           f"--print-to-pdf={dest}", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(dest) or os.path.getsize(dest) < 20000:
        raise RuntimeError(f"{slug}: render failed\n{r.stderr[-800:]}")
    return os.path.getsize(dest)


def main():
    if not os.path.exists(CHROME):
        sys.exit("Google Chrome not found; install it or edit CHROME in this file.")
    os.makedirs(OUT, exist_ok=True)
    projects = json.load(open(os.path.join(ROOT, "content", "projects.json")))["projects"]
    only = sys.argv[1:]
    if only:
        projects = [p for p in projects if p["slug"] in only]
    httpd = serve()
    time.sleep(0.4)
    total = 0
    try:
        for i, p in enumerate(projects, 1):
            size = render(p["slug"])
            total += size
            print(f"  {i:2d}/{len(projects)}  {p['slug']:<28} {size/1e6:5.2f} MB")
    finally:
        httpd.shutdown()
    print(f"rendered {len(projects)} PDFs, {total/1e6:.1f} MB total")


if __name__ == "__main__":
    main()
