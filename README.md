# getcontext-public

Public-facing site for **Get Context** — privacy policy, terms, docs, support.

Live at: https://get.context.select

## Hosting

GitHub Pages with custom domain. CNAME file in repo root sets `get.context.select`.

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Files

| File | Purpose |
|---|---|
| `index.html` | Landing page |
| `privacy.html` | Privacy policy (Zoom Marketplace requirement) |
| `terms.html` | Terms of service (Zoom Marketplace requirement) |
| `docs.html` | How the bot works |
| `support.html` | Contact info |
| `CNAME` | GitHub Pages custom domain config |

## Deploy

Push to `main`. GitHub Pages auto-publishes.

## Why this repo exists

Zoom Marketplace requires public URLs for privacy policy, terms, and support before approving an app. This repo is the minimum viable surface for that.
