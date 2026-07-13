# Design System

The visual language for this profile draws from Apple, Linear, Vercel, Raycast, Stripe, and Framer: glass panels over an animated aurora, generous spacing, monospace terminal typography, thin borders, and a single three-stop accent gradient that carries through every element from the hero border to the favicon.

All tokens live in [`theme.json`](../theme.json) and are consumed by the SVG generator (`.build/generate_svgs.py`).

## Color Tokens

### Dark theme (default)

| Token | Value | Usage |
|-------|-------|-------|
| `background` | `#030712` | Card canvas |
| `panel` | `#0F172A` | Glass panels (at 72% opacity over aurora) |
| `panelSecondary` | `#111C33` | Reserved for nested surfaces |
| `textPrimary` | `#F8FAFC` | Headline, info values, pill labels |
| `textSecondary` | `#94A3B8` | Terminal prompts, social labels |
| `textMuted` | `#64748B` | Panel captions, title-bar text |
| `border` | `#1E293B` | Panel strokes, dividers |
| `accent.violet` | `#7C3AED` | Gradient stop 1, aurora blob 1 |
| `accent.cyan` | `#22D3EE` | Gradient stop 2, cursors, particles, ASCII fill |
| `accent.emerald` | `#10B981` | Gradient stop 3, status dot, uptime line |

### Light theme

| Token | Value | Usage |
|-------|-------|-------|
| `background` | `#FFFFFF` | Card canvas |
| `panel` | `#F8FAFC` | Glass panels |
| `textPrimary` | `#0F172A` | Headline, info values |
| `textSecondary` | `#475569` | Secondary text |
| `border` | `#E2E8F0` | Panel strokes, dividers |
| `accent.blue` | `#2563EB` | Gradient stop 1 |
| `accent.cyan` | `#06B6D4` | Gradient stop 2 (decorative only) |
| `accent.emerald` | `#10B981` | Gradient stop 3 (decorative only) |
| text-safe cyan | `#0E7490` | Info labels, terminal output (5.12:1 contrast) |
| text-safe emerald | `#047857` | Uptime line (5.24:1 contrast) |

The light theme deliberately splits **decorative accents** (kept vivid for gradients, strokes, glows) from **text accents** (darkened variants that pass WCAG AA on `#F8FAFC`). See the [accessibility report](./accessibility-report.md) for the full contrast matrix.

## Typography

| Role | Stack | Size |
|------|-------|------|
| Terminal / mono | `ui-monospace, 'Cascadia Code', Consolas, 'Courier New', monospace` | 11–25 px |
| UI sans (favicon, fallbacks) | `'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif` | — |

No external fonts are used anywhere — GitHub's camo proxy strips external references from README images, so every glyph renders from system font stacks. Monospace is load-bearing: the typing animation's clip-path math assumes a fixed advance width (`0.602 × font-size`), which only holds in monospace.

Type scale (from `theme.json`): hero name 25 px / rotating role 15 px / info rows 13.5 px / captions 12 px / ASCII art 11 px.

## Layout

- Canvas: **1180 × 610**, `viewBox`-driven so it scales fluidly at `width="100%"` in the README.
- Card radius 24 px; panel radius 20 px; 28 px outer gutter; 24 px gap between panels.
- **Left panel** 420 px wide (≈38% of content width): ASCII avatar + terminal tail.
- **Right panel** 680 px wide: title bar → typed name → rotating role → divider → 8 info rows (27 px rhythm) → skill pills → divider → social row.

## Surface & Depth Recipe

Each glass panel is built from four layers:

1. Panel fill at `fill-opacity="0.72"` so the aurora glows through.
2. A vertical glass-reflection gradient (`#FFF` at 10% → 3% → 0%).
3. A 1 px top "catch-light" line at 12% opacity.
4. A 1 px border in the theme `border` color.

Depth ordering (back to front): background fill → aurora blobs (46 px blur) → pulsing radial lights → noise (feTurbulence at 3–5% opacity) → particles → scanline → card-level glass reflection → shimmering gradient border (sharp pass + blurred bloom pass) → panels → content.

## Iconography

Social icons are inline `<path>` data only: the official GitHub and LinkedIn 16 px glyphs (scaled 1.45×), plus a stroked globe and envelope drawn from primitives. No external images.
