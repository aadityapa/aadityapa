# Accessibility Report

For the v12 audit covering all 13 SVGs (contrast matrix, semantics, motion inventory), see [`reports/accessibility-report.md`](../reports/accessibility-report.md); this document covers the hero and favicon in depth.

## Semantic Structure

Both hero SVGs and the favicon carry a full accessibility layer:

- `role="img"` on the root `<svg>` element.
- `aria-labelledby="t d"` pointing at a `<title id="t">` and `<desc id="d">`.
- The `<desc>` is a genuine long description (theme, layout, name, roles, profile facts, and social links) — a screen-reader user gets the same information a sighted user sees animate in.
- The README `<img>` fallback carries a descriptive `alt` attribute repeating name and title.

## Contrast Audit (WCAG 2.1)

Measured with the WCAG relative-luminance formula against the effective panel background of each theme. AA requires 4.5:1 for normal text, 3:1 for large text and graphical objects.

### Dark theme (text on `#0F172A` panels)

| Foreground | Usage | Ratio | Verdict |
|------------|-------|-------|---------|
| `#F8FAFC` | name, info values, pill labels | **17.06:1** | AAA |
| `#94A3B8` | secondary/terminal text | **6.96:1** | AA (AAA large) |
| `#22D3EE` | info labels, terminal output | **9.88:1** | AAA |
| `#10B981` | uptime line | **7.04:1** | AAA |
| `#64748B` | muted captions (12 px) | **3.75:1** | large-text AA; used only for decorative captions |
| `#F8FAFC` on `#030712` | canvas-level text | **19.24:1** | AAA |

### Light theme (text on `#F8FAFC` panels)

| Foreground | Usage | Ratio | Verdict |
|------------|-------|-------|---------|
| `#0F172A` | name, info values | **17.06:1** | AAA |
| `#475569` | secondary text | **7.24:1** | AAA |
| `#0E7490` (darkened cyan) | info labels, terminal output | **5.12:1** | AA |
| `#047857` (darkened emerald) | uptime line | **5.24:1** | AA |
| `#64748B` | muted captions | **4.55:1** | AA |

Design note: the vivid light-theme accents `#06B6D4` (2.32:1) and `#10B981` (2.42:1) failed AA as text, so the generator uses them **only for decorative strokes, gradients, and glows**, substituting the darkened `#0E7490` / `#047857` variants wherever they render text. This is enforced in the generator (`a2text` / `a3text` tokens), not by hand. The rotating role titles are painted with a dedicated text-safe gradient (`#agt`) whose middle and end stops use the darkened variants in the light theme; the vivid gradient (`#ag`) remains reserved for decorative pill strokes.

## Motion Safety

- No element flashes faster than ~1 Hz (the blinking cursors), far below the WCAG 2.3.1 threshold of three flashes per second.
- Ambient motion (aurora, particles, scanline) is slow (9–31 s cycles) and low-contrast.
- SMIL cannot query `prefers-reduced-motion` without CSS (which GitHub strips); users who disable animations at the OS/browser level get the frozen first frame, which still contains all text content because reveals use `fill="freeze"` and the underlying text exists in the DOM regardless of opacity state.

## Non-Reliance on Color

- Info rows pair a `❯ label` keyword with each value — meaning never depends on hue alone.
- Terminal output lines carry their own prompts (`root@aadityapa:~$`).
- Social links pair every icon with a text label.

## README Accessibility

- All stats/badge images include `alt` text naming the metric and user.
- The `<picture>` element serves theme-appropriate art to both color schemes rather than forcing dark-on-light or light-on-dark mismatches.
- Section headings use a proper hierarchy (`##` throughout, single `#`-free top since the hero is the masthead).
