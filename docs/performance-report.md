# Performance Report

For the v12 measured totals (all 13 SVGs, 351 KB family payload, 922 animations) see [`reports/performance-report.md`](../reports/performance-report.md); this document explains the techniques.

## Payload

| Asset | Size | Gzip-friendly? |
|-------|------|----------------|
| `assets/dark.svg` | 44,009 B | Yes — repetitive XML compresses to roughly a quarter over the wire |
| `assets/light.svg` | 44,010 B | Yes |
| Five visualization pairs | 14.8–35.3 KB each | Yes |
| `favicon.svg` | 1,420 B | Yes |
| `README.md` | ~15 KB | Yes |

The browser downloads exactly **one file per `<picture>` pair** (the media query picks dark or light), so a visit costs ≈183 KB of first-party SVG. Everything else on the profile page (stats cards, badges, snake) is third-party and lazy-rendered by GitHub.

## Why the SVGs Render Cheaply

1. **Transform/opacity-dominated motion.** The overwhelming majority of the 179 hero animations (and the visualization files' loops) mutate only `opacity`, `transform`, dash offsets, or clip/gradient offsets — properties compositors handle without relayout. The 8 `animateMotion` particles move tiny 1.2–2.4 px circles.
2. **Blur budget is bounded.** The expensive `feGaussianBlur stdDeviation="46"` aurora filter applies to exactly 4 circles. Glow (`stdDeviation="3.2"`) and soft-shadow (`9`) filters are shared definitions applied to small regions (icons, pills, text groups), not the full canvas.
3. **Static turbulence.** The `feTurbulence` noise runs over one static rect with no animated filter parameters, so it rasterizes once.
4. **No layout thrash by design.** SMIL timelines are declarative; the browser schedules them natively with no script ticks, no `requestAnimationFrame`, no style recalculation.
5. **defs reuse.** 17 shared definitions (9 gradients, 4 filters, 1 mask, 1 pattern, 2 clipPaths) mean the render tree references, not duplicates, every visual recipe.

## Network Behavior on GitHub

- GitHub proxies README images through `camo.githubusercontent.com` with long-lived caching; after first load the SVG serves from cache.
- The SVGs reference **zero external resources** (fonts, images, scripts), so there is exactly one request per theme and no render-blocking dependency chain.
- System font stacks (`Segoe UI` / `ui-monospace` cascade) eliminate font download and FOUT entirely.

## Third-Party Widgets

Stats cards (github-readme-stats mirror, streak-stats, activity-graph, komarev) are served by their own CDNs and cached by camo. They are `<img>` elements — if any service is slow or down, the rest of the page renders unaffected. The contribution snake is pre-rendered by the `snake.yml` workflow every 12 hours (plus a daily `stats-refresh.yml` dispatch) and served as a static SVG from the `output` branch, costing nothing at view time.

## CI Guardrails

- `validate-svg.yml` fails the build if any shipped SVG exceeds 1 MB or gains external references.
- `optimize-svg.yml` tracks the SVGO-optimized size of every `assets/*.svg` on each change and asserts no SMIL element is lost, making size or animation regressions visible in the job log.
