# Animation Report

Complete inventory of the SMIL animation system across all shipped SVGs (v12). Dark/light pairs share identical timing; only colors differ. Everything is `<animate>`, `<animateTransform>`, or `<animateMotion>` — no CSS, no JavaScript, which is what keeps the banners alive inside GitHub's sandboxed README renderer.

## Hero Timeline Overview

The intro plays as a choreographed sequence over ~7.6 s, then hands off to infinite ambient loops.

| Time (s) | Event |
|----------|-------|
| 0.0 | Aurora, neural constellation, particles, scanline, border shimmer, noise all running (infinite) |
| 0.35 – 3.3 | ASCII portrait reveals line by line (25 rows × 0.11 s stagger) |
| 0.9 – 2.8 | "Hi, I'm Aaditya Padiya" types out (22 discrete steps) |
| 2.8 | Wave emoji pops in and rocks ±14° for 3 cycles |
| 3.0 – 5.2 | 8 profile info rows slide in (0.32 s stagger) |
| 3.0 | Rotating role carousel begins (27 s cycle, infinite) |
| 3.3 | Gradient sweep starts flowing across the ASCII portrait (masked) |
| 3.4 – 4.9 | Terminal tail lines print (`whoami`, `uptime`) |
| 5.4 | Left-panel block cursor starts blinking (infinite) |
| 5.8 – 7.1 | 12 skill pills fade in (0.12 s stagger) |
| 7.0 | Social row fades in; glow pulses continue (infinite) |

## Hero Ambient Loop Inventory

| Animation | Element | Type | Duration | Notes |
|-----------|---------|------|----------|-------|
| Aurora blob 1 | violet radial, 300 r | `animateTransform` translate | 26 s | keyframed drift, 4 waypoints |
| Aurora blob 2 | cyan radial, 320 r | `animateTransform` translate | 31 s | counter-drift |
| Aurora blob 3 | emerald radial, 240 r | `animateTransform` translate | 23 s | |
| Aurora blob 4 | violet radial, 220 r | `animateTransform` translate | 29 s | |
| Neural constellation | 14 nodes + 16 dashed edges | `animate` dashoffset/opacity/r | 4–11 s | staggered pulses, 12–16% layer opacity |
| Portrait breathe | ASCII group | `animateTransform` scale 1→1.012 | 7 s | nested around portrait center |
| Radial light L | cyan glow behind avatar | `animate` opacity 0.10→0.24 | 6 s | |
| Radial light R | violet glow | `animate` opacity 0.06→0.16 | 8 s | |
| Border shimmer | card stroke gradient | `animateTransform` rotate 0→360° | 14 s | sharp stroke + blurred bloom copy |
| Gradient sweep | `#sw` gradient | `animateTransform` translate ±1180 px | 9 s | masked to ASCII glyphs |
| Scanline | 110 px gradient bar | `animateTransform` translate | 11 s | full canvas traversal |
| Particles ×8 | 1.2–2.4 px circles | `animateMotion` on cubic paths | 15–22 s | each with opacity breathing at dur/3 |
| Avatar float | ASCII group | `animateTransform` translate ±5 px | 9 s | |
| Avatar backlight | radial circle | `animate` opacity + r | 5 s / 7 s | dual animation |
| Status dot | left panel header | `animate` opacity | 2 s | |
| Role carousel | 9 `<text>` layers | `animate` opacity, keyTimes gated | 27 s | 3 s per role, 0.45 s crossfade |
| Role cursor | 9×16 rect | `animate` x (discrete, 27 s) + opacity blink (1 s) | 27 s / 1 s | rides the end of the visible role, forever-blinking |
| Name cursor | 12 px rect | `animate` x (typing) + opacity blink | 1.9 s / 1.1 s | tracks typed width in absolute coordinates, then blinks |
| Left cursor | 8×14 rect | `animate` opacity, discrete | 1.1 s | begins 5.4 s |
| Skill pill glows | 12 gradient strokes | `animate` opacity 0.15→0.75 | 3.6 s | staggered 0.3 s apart |
| Favicon gradient | `#fag` | `animateTransform` rotate | 8 s | |
| Favicon dot | 2.4 px circle | `animate` opacity | 2.4 s | |

**Totals per hero SVG: 179 animation elements** — 153 `animate`, 18 `animateTransform`, 8 `animateMotion` (counted from the shipped files). The favicon adds 2 more (rotating gradient + pulsing dot).

## v12 Visualization Inventory

Counted from the shipped files (dark/light pairs are identical):

| File | Animations | Signature motion |
|------|-----------:|------------------|
| `ecosystem-*.svg` | 68 | Counter-rotating orbital rings (60 s / 90 s) with per-node upright counter-rotation, traveling pulse dots (`animateMotion`), center-node glow pulse |
| `architecture-*.svg` | 76 | Dash-offset flows on connectors, CI/CD pipeline patrol dot with sequenced stage glows, LED blink racks, monitoring chart self-draw, security scan sweep |
| `timeline-*.svg` | 40 | Spine self-draw (stroke-dasharray reveal), sequential node pops with pulse halos, patrol glow dot on infinite loop |
| `certifications-*.svg` | 24 | Rotating medallion gradient rings, staggered scale-pop reveals, shimmer sweeps every ~7 s, VERIFIED pill pulses |
| `projects-*.svg` | 73 | Staggered card fade+rise reveals, status-dot pulses, breathing border glows, chip shimmer |

Grand total across the 13 shipped SVGs: **922 animation elements** (2×179 hero + 2×68 ecosystem + 2×76 architecture + 2×40 timeline + 2×24 certifications + 2×73 projects + 2 favicon).

## Technique Notes

- **Typing effect** — a `<clipPath>` rect whose `width` steps through 23 discrete values (`calcMode="discrete"`, one per character) exposes the pre-rendered text; a separate cursor rect animates its `x` through the same value list, so the caret rides the typed edge, then settles into an infinite blink.
- **Role carousel** — nine stacked `<text>` layers share one 27 s clock; each layer's `keyTimes` gate opens for its 3 s slot with 0.45 s fade edges. The first and last layers get asymmetric keyTimes so the loop seam is invisible.
- **Gradient over ASCII** — the ASCII rows are duplicated into a `<mask>`; a rect filled with the animated sweep gradient sits behind the mask, so the moving color only paints the glyph pixels.
- **Line-by-line reveal** — every reveal uses `fill="freeze"` so the final state persists after the intro.
- **Reduced-motion** — SMIL cannot read `prefers-reduced-motion` without CSS; the mitigation is pacing (nothing flashes faster than the ~1 Hz cursors, well under the 3-flashes-per-second WCAG 2.3.1 threshold).
