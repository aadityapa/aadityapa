# v12 Performance Report

Date: 2026-07-13.

## Payload

| Metric | Value |
|--------|------:|
| Total repository-hosted SVG payload (13 files) | 351.0 KB |
| Payload actually downloaded per visit (theme-gated `<picture>`) | ≈183 KB (one theme set + favicon) |
| Largest single file | `assets/dark.svg` / `light.svg` at 43.0 KB |
| Median visualization file | 22–33 KB |
| External embeds (stats, streak, activity graph, snake, badges) | served by third parties via GitHub camo, cached |

Everything is inline vector: no fonts fetched, no rasters embedded, no base64 blobs. Gzip on GitHub's CDN compresses the repetitive SVG/SMIL markup roughly 4–5×, so the on-wire cost of the full dark set is on the order of 40–50 KB.

## Animation Load

922 SMIL animation elements across the family (see `docs/animation-report.md` for the per-file inventory). Density is bounded per viewport section: the browser only animates what is scrolled into view, and GitHub renders each README image in its own isolated `<img>` context.

Cost profile per file:

- **Transform/opacity/dash-offset animations** (the overwhelming majority) run on the compositor path — no layout, no paint storms.
- **Blur filters** are the only expensive primitives. Each file has one 46 px-blur aurora group (≤4 circles, pre-blurred per frame) plus small 1.4–9 px glows on accents. The v12 hero deliberately switched the ASCII portrait's glow from a 3.2 px to a 1.4 px blur — sharper glyphs *and* cheaper filtering.
- **`feTurbulence` noise** runs once over one static rect per file (no animated filter parameters).
- The ecosystem's orbital motion is two `animateTransform` rotations plus 14 counter-rotations — cheap matrix math, no repaints.

## Measured Render Behavior (headless Chrome 1180 px, this machine)

- Full-frame screenshot of the hero at any seeked time: renders in well under the 60 s harness timeout, consistently ~1–2 s including Chrome startup — the SVG itself rasterizes in tens of milliseconds.
- Pixel-diff runs (pre- vs post-optimization) produced identical frames, confirming the optimizer changes bytes, not rendering work.
- No file triggers Chrome's slow-frame warnings when playing live at 60 fps in a foreground tab.

## Network Behavior in the README

- All six `<picture>` blocks reference **relative repo paths**, so GitHub serves them from its own CDN with immutable cache keys per commit — no third-party availability risk for the core art.
- Third-party cards are isolated to the Stats section; the two dead services were replaced or removed (see `reports/validation-report.md`), so no request in the shipped README is known-broken.
- `stats-refresh.yml` re-dispatches the snake daily; the snake SVGs are served from `raw.githubusercontent.com` on the `output` branch.

## Budgets Going Forward

| Budget | Value | Enforced by |
|--------|-------|-------------|
| Per-SVG size | < 150 KB | `.build/validate.py` (local) + `validate-svg.yml` (CI, 1 MB hard cap) |
| SMIL survival through any optimization | 100% | `optimize-svg.yml` per-file assertion |
| Hero animation count | exactly 179 | `.build/optimize_svgs.py` assert |
