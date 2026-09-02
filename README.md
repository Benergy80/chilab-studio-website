# ChiLab Studio Website

Static website draft for ChiLab Studio.

## Build

```bash
python3 build.py
```

The generator reads:

- `content/site.json`
- `content/projects.json`
- `content/manifest.json`

It writes the root pages and project pages in `work/`.

## Design

Design contract files live in `design/`:

- `COMMIT-SHEET.md`
- `SYSTEM-SHEET.md`
- `DESIGN.md`

## Local Preview

```bash
python3 -m http.server 3112 --bind 127.0.0.1
```

## Domain

Leave GitHub Pages on the default GitHub URL until the DNS cutover is approved.
When `chilabstudio.com` is ready to move, add a `CNAME` file containing:

```text
chilabstudio.com
```
