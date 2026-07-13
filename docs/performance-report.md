# Performance Report

## Payload

| Asset | Size | Gzip-friendly? |
|-------|------|----------------|
| `assets/dark.svg` | 32,518 B | Yes — repetitive XML compresses to roughly a quarter over the wire |
| `assets/light.svg` | 32,519 B | Yes |
| `favicon.svg` | 1,420 B | Yes |
| `README.md` | ~13 KB | Yes |

The browser downloads exactly **one** hero SVG (the `<picture>` element's media query picks dark or light), so the profile's first-party image payload is ~32 KB. Everything else on the profile page (stats cards, badges, snake) is third-party and lazy-rendered by GitHub.

## Why the SVGs Render Cheaply

1. **Transform/opacity-dominated motion.** 103 of the 111 animations mutate only `opacity`, `transform`, or clip/gradient offsets — properties compositors handle without relayout. The 8 `animateMotion` particles move tiny 1.2–2.4 px circles.
2. **Blur budget is bounded.** The expensive `feGaussianBlur stdDeviation="46"` aurora filter applies to exactly 4 circles. Glow (`stdDeviation="3.2"`) and soft-shadow (`9`) filters are shared definitions applied to small regions (icons, pills, text groups), not the full canvas.
3. **Static turbulence.** The `feTurbulence` noise runs over one static rect with no animated filter parameters, so it rasterizes once.
4. **No layout thrash by design.** SMIL timelines are declarative; the browser schedules them natively with no script ticks, no `requestAnimationFrame`, no style recalculation.
5. **defs reuse.** 17 shared definitions (9 gradients, 4 filters, 1 mask, 1 pattern, 2 clipPaths) mean the render tree references, not duplicates, every visual recipe.

## Network Behavior on GitHub

- GitHub proxies README images through `camo.githubusercontent.com` with long-lived caching; after first load the SVG serves from cache.
- The SVGs reference **zero external resources** (fonts, images, scripts), so there is exactly one request per theme and no render-blocking dependency chain.
- System font stacks (`Segoe UI` / `ui-monospace` cascade) eliminate font download and FOUT entirely.

## Third-Party Widgets

Stats cards (github-readme-stats, streak-stats, activity-graph, trophies, komarev) are served by their own CDNs and cached by camo. They are `<img>` elements — if any service is slow or down, the rest of the page renders unaffected. The contribution snake is pre-rendered by the `snake.yml` workflow every 12 hours and served as a static SVG from the `output` branch, costing nothing at view time.

## CI Guardrails

- `svg-validate.yml` fails the build if either hero SVG exceeds 1 MB or gains external references.
- `svg-optimize.yml` tracks the SVGO-optimized size on every asset change, making size regressions visible in the job log.
