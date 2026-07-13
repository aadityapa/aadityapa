# v12 Accessibility Report

Date: 2026-07-13 · Scope: all 13 shipped SVGs + README embeds.

## Semantic Structure — PASS on all 13 files

Every SVG (hero pair, five visualization pairs, favicon) carries:

- `role="img"` on the root element.
- `aria-labelledby="t d"` pointing at `<title id="t">` and `<desc id="d">` as the first children.
- A genuine long description in `<desc>` (theme, layout, and the actual content shown — companies and dates in the timeline, certification names in the badges, project names in the grid), so a screen-reader user receives the same information the animation reveals.
- README `<img>` fallbacks with descriptive `alt` text for all six `<picture>` blocks and all external stat cards.

## Contrast Audit (WCAG 2.1)

Measured with the WCAG relative-luminance formula. All six visualization families use the same token system, so one matrix covers the family. AA requires 4.5:1 for normal text, 3:1 for large text and graphical objects.

### Dark theme (text on `#0F172A` panels)

| Foreground | Usage | Ratio | Verdict |
|------------|-------|------:|---------|
| `#F8FAFC` | names, values, card titles | **17.06:1** | AAA |
| `#94A3B8` | secondary text, descriptions | **6.96:1** | AA (AAA large) |
| `#22D3EE` | accent labels, section headers | **9.88:1** | AAA |
| `#10B981` | status text, uptime lines | **7.04:1** | AAA |
| `#64748B` | muted captions only | **3.75:1** | large-text AA; never used for body copy |
| `#F8FAFC` on `#030712` | canvas-level headings | **19.24:1** | AAA |

### Light theme (text on `#F8FAFC` panels)

| Foreground | Usage | Ratio | Verdict |
|------------|-------|------:|---------|
| `#0F172A` | names, values, card titles | **17.06:1** | AAA |
| `#475569` | secondary text | **7.24:1** | AAA |
| `#0E7490` (text-safe cyan) | accent labels, section headers | **5.12:1** | AA |
| `#047857` (text-safe emerald) | status text | **5.24:1** | AA |
| `#64748B` | muted captions | **4.55:1** | AA |
| `#0F172A` on `#FFFFFF` | canvas-level headings | **17.85:1** | AAA |

The light theme's vivid accents `#06B6D4` (2.34:1) and `#10B981` (2.42:1) fail AA as text, so **every generator** (hero and all five v12 generators) substitutes the darkened `a2text`/`a3text` tokens wherever accent color renders text; the vivid values are reserved for strokes, gradients, and glows. This split is enforced in code, not by convention — verified by inspecting the light renders of all six families.

## ASCII Portrait

The photo-derived portrait is painted in `#22D3EE` on the dark panel (9.88:1) and in the text-safe palette on light. It is decorative-adjacent (the `<desc>` describes it as a portrait of Aaditya generated from his photo), so contrast is not load-bearing for comprehension.

## Motion Safety

- Nothing flashes faster than ~1 Hz (the terminal cursors); WCAG 2.3.1's threshold is 3 flashes/second.
- Ambient loops are slow: orbits 60–90 s, aurora 23–31 s, dash flows 2.5–11 s, shimmer sweeps ~7 s.
- All intro reveals use `fill="freeze"`; a viewer whose environment suppresses SMIL (or who pauses animations) still gets complete static content because text exists in the DOM regardless of animation state.
- SMIL cannot query `prefers-reduced-motion` without CSS (which GitHub strips from README SVGs) — documented limitation, mitigated by pacing.

## Non-Reliance on Color

- Timeline nodes pair date ranges + role text with each node; the "current" state is shown by both a pulsing halo and the word "Present".
- Project statuses are text pills ("LIVE", "IN DEV", "PRODUCTION", "DEPLOYED"), not color dots alone.
- Certifications carry issuer + year text; "VERIFIED" is a labelled pill.
- Info rows in the hero pair a `❯ label` keyword with each value.
