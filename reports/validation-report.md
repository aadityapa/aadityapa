# v12 Validation Report

Date: 2026-07-13 · Scope: all 13 shipped SVGs, 5 JSON data files, 7 workflow YAMLs, README references.
Gate script: `.build/validate.py` (run locally; the same checks run in CI via `validate-svg.yml` and `repository-health.yml`).

## SVG Gate — all 13 files PASS

Checks per file: strict XML parse (`xml.etree.ElementTree`), no `<script>`/`<style>`/`foreignObject`/`javascript:`, no external references (only the SVG xmlns), no duplicate ids, every `url(#…)`/`href="#…"` reference resolves, `<title>` + `<desc>` present, SMIL-animated, size under the 150 KB budget.

| File | Size | Animations | Unique ids | viewBox | Result |
|------|-----:|-----------:|-----------:|---------|--------|
| `assets/dark.svg` | 43.0 KB | 179 | 20 | 0 0 1180 610 | PASS |
| `assets/light.svg` | 43.0 KB | 179 | 20 | 0 0 1180 610 | PASS |
| `assets/ecosystem-dark.svg` | 21.9 KB | 68 | 12 | 0 0 1180 760 | PASS |
| `assets/ecosystem-light.svg` | 21.9 KB | 68 | 12 | 0 0 1180 760 | PASS |
| `assets/architecture-dark.svg` | 32.3 KB | 76 | 14 | 0 0 1180 800 | PASS |
| `assets/architecture-light.svg` | 32.3 KB | 76 | 14 | 0 0 1180 800 | PASS |
| `assets/timeline-dark.svg` | 17.8 KB | 40 | 13 | 0 0 1180 620 | PASS |
| `assets/timeline-light.svg` | 17.8 KB | 40 | 13 | 0 0 1180 620 | PASS |
| `assets/certifications-dark.svg` | 14.8 KB | 24 | 17 | 0 0 1180 360 | PASS |
| `assets/certifications-light.svg` | 14.8 KB | 24 | 17 | 0 0 1180 360 | PASS |
| `assets/projects-dark.svg` | 35.3 KB | 73 | 11 | 0 0 1180 740 | PASS |
| `assets/projects-light.svg` | 35.3 KB | 73 | 11 | 0 0 1180 740 | PASS |
| `favicon.svg` | 1.4 KB | 2 | 4 | 0 0 64 64 | PASS |

Total: **922 SMIL animation elements** across the family; zero JavaScript, zero CSS, zero external fetches.

## Visual Render Gate — headless Chrome

Every file was rendered in both themes with headless Chrome (`--headless=new`, SVG inlined into an HTML harness, timeline seeked via `setCurrentTime()` + `pauseAnimations()` in the harness — never inside the SVG) and inspected:

- **Hero (t=10.5 s)**: layout intact; ASCII portrait renders centered with uniform-width rows; info rows, pills, and socials aligned; neural constellation visible behind glass without stealing contrast.
- **Hero caret regression (t=1.8 s, t=2.3 s)**: the typing caret rides the typed edge mid-animation. Cursor `x` values are absolute canvas coordinates (`502 → 833.3`), not zero-based offsets — re-verified after the v12 regeneration.
- **Hero optimization equivalence (t=30 s)**: pixel-diff of pre- vs post-optimization renders is byte-empty (`ImageChops.difference` bbox `None`) for both themes.
- **Ecosystem (t=7 s and t=30 s)**: both rings in different orbital positions; all 14 labels upright (counter-rotation verified); no node clipping.
- **Architecture / Timeline / Certifications / Projects (t=30 s)**: no text overflow, no card collisions, no clipped edges in either theme; timeline additionally checked mid-draw at t=1.2 s (spine tip ~32%, node 2 fading in).
- **ASCII portrait recognizability**: side-by-side comparison against the source photo (`.build/photo/ascii_side_by_side.png`) — silhouette, quiff hairstyle, beard, and face tones read clearly; glasses appear as a darker band (limit of a 56×25 character grid).

## Data & Config Gate

| Check | Result |
|-------|--------|
| `profile.json`, `skills.json`, `theme.json`, `metadata.json`, `data/profile.json` parse | PASS |
| Root `profile.json` consistent with `data/profile.json` (same identity, experience, projects; root keeps flat legacy schema) | PASS |
| 7 workflow YAMLs parse with `jobs` + explicit `permissions` blocks | PASS |
| README: all 11 relative references exist on disk | PASS |
| README markdownlint (`markdownlint-cli2` with repo `.markdownlint.json`) | 0 errors |
| All 6 `<picture>` blocks: dark + light `<source>` + `<img>` fallback with alt | PASS |
| `sitemap.xml` well-formed | PASS |
| `.gitignore` allowlist covers all 12 tracked `.build/` scripts | PASS |

## Known External Dependencies (not gated)

- `github-readme-stats.shion.dev` (stats + top-langs) — community HA mirror, verified HTTP 200 on 2026-07-13; the canonical vercel.app instance is paused (503).
- `streak-stats.demolab.com`, `github-readme-activity-graph.vercel.app`, `komarev.com` — verified live.
- Snake SVGs exist only after `snake.yml` runs on GitHub (already live on the `output` branch).
- `github-profile-trophy.vercel.app` returned 402 and was **removed** from the README.
