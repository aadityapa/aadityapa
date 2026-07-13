# v12 Optimization Report

Date: 2026-07-13 · Budget: **< 150 KB per SVG** (hard gate in `.build/validate.py`).

## Shipped Sizes

| File | Bytes | KB | % of budget |
|------|------:|---:|------------:|
| `assets/dark.svg` | 44,009 | 43.0 | 28.7% |
| `assets/light.svg` | 44,010 | 43.0 | 28.7% |
| `assets/projects-dark.svg` | 36,167 | 35.3 | 23.6% |
| `assets/projects-light.svg` | 36,168 | 35.3 | 23.6% |
| `assets/architecture-dark.svg` | 33,078 | 32.3 | 21.5% |
| `assets/architecture-light.svg` | 33,079 | 32.3 | 21.5% |
| `assets/ecosystem-dark.svg` | 22,433 | 21.9 | 14.6% |
| `assets/ecosystem-light.svg` | 22,434 | 21.9 | 14.6% |
| `assets/timeline-dark.svg` | 18,192 | 17.8 | 11.8% |
| `assets/timeline-light.svg` | 18,193 | 17.8 | 11.9% |
| `assets/certifications-dark.svg` | 15,144 | 14.8 | 9.9% |
| `assets/certifications-light.svg` | 15,145 | 14.8 | 9.9% |
| `favicon.svg` | 1,420 | 1.4 | 0.9% |
| **Total README payload (SVGs)** | **359,472** | **351.0** | — |

A dark-mode viewer downloads only the dark half plus the favicon (≈183 KB total) since `<picture>` sources are theme-gated.

## Hero Optimization Pass (v12, 2026-07-13)

The regenerated hero (photo portrait + neural constellation grew the raw output) went through the SMIL-safe local optimizer `.build/optimize_svgs.py`:

| Stage | dark.svg | light.svg |
|-------|---------:|----------:|
| Raw generator output | 55,328 B | 55,329 B |
| After `.build/optimize_svgs.py` | 44,009 B (−20.5%) | 44,010 B (−20.5%) |
| After SVGO 3 (dry-run comparison) | 46,388 B (**larger**) | 46,368 B (**larger**) |

**Decision: ship the Python-optimized files.** SVGO 3 (with the SMIL-safe config) *increased* size on this input — its re-serialization expands multi-byte text and reorders attributes with no structural wins left after the Python pass, so it stays a CI dry-run check (asserting SMIL survival) rather than a production step.

What the optimizer does (unchanged from v11, retuned for v12 metrics): hoists the shared monospace `font-family` to the root, hoists ASCII-block `font-size`/`text-anchor`/`fill` (now keyed on the 10.5 px portrait rows) onto the group and mask, keeps `xml:space="preserve"` only where whitespace is significant, trims trailing zeros in SMIL `values`/`keyTimes`/`begin`/`dur`, and collapses inter-element whitespace. It asserts exactly **179 animations** survive per file, and a headless-Chrome pixel-diff of the forced t=30 s frame against the unoptimized files came back **byte-identical** for both themes.

The typing-cursor `<rect>` remains a rect (never converted to a path); the SVGO configs keep `convertShapeToPath: false` and `mergePaths: false` for the same reason.

## Why the Visualization SVGs Ship Un-minified

The five new families are emitted by their generators at 14.8–35.3 KB — already 76–90% under budget. Their generators use the same lean techniques as the hero (single `<defs>` per file, 2–4 char ids, shared gradients/filters referenced by `url(#…)`, no base64, procedural glyphs instead of images), so a further minification pass would save single-digit KB at real risk to SMIL semantics. CI still dry-runs SVGO over every `assets/*.svg` on each push (`optimize-svg.yml`) and fails if any animation element would be lost.

## Render-Cost Notes

- Blur filters are the only expensive primitives; each file keeps the 46 px aurora blur on ≤4 circles.
- The hero's neural constellation is stroke-dash and opacity animation only — no filters — so it stays on the GPU-friendly compositing path.
- All motion elsewhere is transform/opacity/dashoffset; `feTurbulence` noise runs once over a static rect per file.
