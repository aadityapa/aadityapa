# SVG Optimization Report

For the full v12 sizing table (all 13 files) and the v12 optimization decision log, see [`reports/optimization-report.md`](../reports/optimization-report.md).

## File Sizes (as shipped, v12)

| File | Size | Budget | Headroom |
|------|------|--------|----------|
| `assets/dark.svg` | 44,009 B (43.0 KB) | < 150 KB | 71% under budget |
| `assets/light.svg` | 44,010 B (43.0 KB) | < 150 KB | 71% under budget |
| Five visualization pairs | 14.8–35.3 KB each | < 150 KB | 76–90% under budget |
| `favicon.svg` | 1,420 B (1.4 KB) | — | — |

Both hero files carry 179 live animations each (the v12 photo portrait + neural constellation added ~68 over v11). Sizes reflect the post-generation pass of `.build/optimize_svgs.py`, a SMIL-safe local optimizer that hoists shared inherited attributes (font stack, `xml:space`, portrait-block fill/size/anchor), trims redundant trailing zeros in SMIL numeric lists, and collapses inter-element whitespace — a ~20% reduction over raw generator output with a pixel-identical render (verified by headless-Chrome diff).

## How the Size Was Kept Down

1. **Single-definition reuse** — every gradient, filter, mask, and pattern is defined once in `<defs>` and referenced by `url(#id)`. The accent gradient `#ag` alone is referenced by 24 elements (pill strokes and fills); its text-safe sibling `#agt` (darkened middle/end stops in the light theme for WCAG AA) paints the 9 role-carousel layers.
2. **Short IDs** — all IDs are 2–3 characters (`ag`, `agt`, `bs`, `sw`, `b1`–`b3`, `gl`, `sc`, `fb`, `fg`, `fs`, `nz`, `crt`, `cv`, `am`, `tn`). 19 unique IDs per file, zero duplicates (verified in CI).
3. **Generated output** — both themes are emitted by one Python generator (`.build/generate_svgs.py`), so the dark/light variants can't drift structurally and share identical animation timing tables.
4. **Path-based icons** — GitHub/LinkedIn glyphs are single compact `<path>` elements; globe and envelope are 3–4 stroke primitives instead of embedded images.
5. **Procedural texture** — noise comes from one `feTurbulence` filter on one rect, not a bitmap; CRT scanlines are a 4×4 `<pattern>`.
6. **No base64, no external refs** — nothing embedded, nothing fetched.

## SVGO Configuration (`.svgo.config.mjs`)

The `optimize-svg.yml` workflow runs SVGO 3 as a **dry-run check** (output to `/tmp`, never overwriting sources) with these overrides, all chosen to protect the SMIL system:

| Override | Why |
|----------|-----|
| `cleanupIds: false` | IDs are referenced by `url(#…)` in masks/filters/gradients and would break if minified/removed |
| `removeViewBox: false` | `viewBox` drives responsive scaling in the README |
| `collapseGroups: false` / `moveElemsAttrsToGroup: false` | groups carry `animateTransform` children and shared opacity/filters |
| `removeHiddenElems: false` | intro elements start at `opacity="0"` and would be treated as hidden |
| `removeUselessDefs: false` | defs referenced only from animated attributes can be misdetected |
| `cleanupNumericValues` / `convertPathData` at precision 3 | keyTimes like `0.0167` must survive rounding |
| `removeTitle: false` / `removeDesc: false` | accessibility layer |

A post-optimization CI step asserts that `<animate>`, `<animateTransform>`, and `<animateMotion>` all still exist in the optimized output, so any future SVGO regression fails the build rather than silently shipping a static banner.

## Render-Cost Considerations

- The three most expensive filters (46 px Gaussian aurora blur) are applied to only 4 circles, pre-blurred once per frame by the compositor.
- `feTurbulence` runs once over a static rect (no animated filter parameters).
- Total filtered elements: 4 aurora + 1 noise + glow/soft-shadow users; all other motion is transform/opacity-only, which stays on the GPU-friendly path.

## Optimization Pass — 2026-07-13 (v11 baseline, historical)

A minification pass was applied to the shipped files (Python pre-pass + SVGO 3 with the repo config, `convertShapeToPath`/`mergePaths` additionally disabled because they rewrite SMIL-animated `<rect>` targets):

| File | Before | After | Reduction |
|------|--------|-------|-----------|
| `assets/dark.svg` | 41,481 B (40.5 KB) | 31,408 B (30.7 KB) | −24.3% |
| `assets/light.svg` | 41,482 B (40.5 KB) | 31,388 B (30.7 KB) | −24.3% |

What changed: the shared monospace `font-family` stack was hoisted to the root element (removed from 85 text elements per file); `font-size`/`text-anchor`/`fill` were hoisted onto the ASCII-avatar group and mask; `xml:space="preserve"` was kept only where whitespace is significant (avatar art and indented terminal lines — Chrome does not inherit it, so it stays per-element); trailing zeros were trimmed from SMIL `values`/`keyTimes`/`begin`/`dur`; inter-element whitespace was collapsed. No gradients, filters, masks, or clipPaths were merged or removed — analysis confirmed zero duplicate definitions and zero unused IDs (18 unique IDs per file, all referenced). All 110 animations per file (85 animate, 17 animateTransform, 8 animateMotion) survived byte-for-byte in timing semantics, verified by animation-signature comparison plus a pixel-identical headless-Chrome render of the forced final frame against the pre-optimization files.
