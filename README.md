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

The site is served from GitHub Pages at
`https://benergy80.github.io/chilab-studio-website/` until the cutover finishes.

Cutover to `chilabstudio.com` is approved. It happens in two steps, in this order.

### Step 1, DNS at GoDaddy (registrar login required)

`chilabstudio.com` uses GoDaddy nameservers (`ns09/ns10.domaincontrol.com`).
In GoDaddy, Domain Settings, DNS, replace the Squarespace records with these.

Delete the four A records pointing at Squarespace
(198.185.159.144, 198.185.159.145, 198.49.23.144, 198.49.23.145)
and the `www` CNAME pointing at `ext-sq.squarespace.com`. Then add:

| Type  | Name | Value                    | TTL    |
|-------|------|--------------------------|--------|
| A     | @    | 185.199.108.153          | 1 hour |
| A     | @    | 185.199.109.153          | 1 hour |
| A     | @    | 185.199.110.153          | 1 hour |
| A     | @    | 185.199.111.153          | 1 hour |
| CNAME | www  | benergy80.github.io      | 1 hour |

Optional, for IPv6, add AAAA records for `@`:
`2606:50c0:8000::153`, `2606:50c0:8001::153`,
`2606:50c0:8002::153`, `2606:50c0:8003::153`.

Verify with:

```bash
dig +short chilabstudio.com A
dig +short www.chilabstudio.com CNAME
```

### Step 2, tell GitHub Pages about the domain

Only after step 1 resolves. Adding this first makes the github.io URL redirect
to a domain that still answers as Squarespace.

```bash
printf 'chilabstudio.com\n' > CNAME
git add CNAME && git commit -m "Point Pages at chilabstudio.com" && git push
```

Then wait for the certificate and turn on HTTPS:

```bash
gh api repos/Benergy80/chilab-studio-website/pages | python3 -m json.tool
gh api -X PUT repos/Benergy80/chilab-studio-website/pages -f https_enforced=true
```

Squarespace can be cancelled once step 1 is live. The site no longer loads
anything from the Squarespace CDN; the original URLs are kept in
`content/legacy-squarespace-urls.json`.
