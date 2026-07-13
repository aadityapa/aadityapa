# SVG Validation Report — `assets/dark.svg` & `assets/light.svg`

**Validation date:** 2026-07-13
**Files validated:**

| File | Size | Elements | XML valid |
| --- | --- | --- | --- |
| `assets/dark.svg` | 41,481 bytes (40.5 KB) | 357 | Yes |
| `assets/light.svg` | 41,482 bytes (40.5 KB) | 357 | Yes |

**Method:** Static analysis with a strict XML parser (`xml.etree.ElementTree`) plus programmatic reference/geometry checks (`.build/deep_validate.py`), and visual verification by rendering both files with headless Chrome at 1180×610 — both via the final-state preview harness (`.build/make_preview.py`) and via SMIL timeline seeks (`svg.setCurrentTime()` at t = 2 s, 4.5 s, 8 s) with pixel-level sampling of the rendered PNGs.

---

## Verdict summary

| # | Check | dark.svg | light.svg |
| --- | --- | --- | --- |
| 1 | Pure SVG (no HTML elements / foreign namespaces) | PASS | PASS |
| 2 | No CSS (`<style>`, `style=""`, classes) | PASS | PASS |
| 3 | No JavaScript (`<script>`, `on*`, `javascript:`) | PASS | PASS |
| 4 | SMIL-only animations | PASS | PASS |
| 5 | Valid XML (strict parse, zero errors) | PASS | PASS |
| 6 | GitHub-compatible (no external refs, system fonts) | PASS | PASS |
| 7 | Dimensions 1180×610 + matching viewBox | PASS | PASS |
| 8 | Responsive (viewBox, sane preserveAspectRatio) | PASS | PASS |
| 9a | No clipping — static coordinate/text-width analysis | PASS | PASS |
| 9b | No clipping — visual render inspection | PASS | PASS |
| 10a | No overlapping text rows / exclusive role carousel | PASS | PASS |
| 10b | No overlapping elements — visual render inspection | **FAIL** | **FAIL** |
| 11 | No missing gradients; no orphan gradient defs | PASS | PASS |
| 12 | No duplicate IDs | PASS | PASS |
| 13 | No broken filters; valid primitives | PASS | PASS |
| 14 | No missing masks / clip-paths; all defs used | PASS | PASS |

**Overall:** Both files fail one check (10b) due to a single, identical misplaced-caret animation bug. All other checks pass. Details below.

---

## Failure detail (check 10b): typing caret frozen over the ASCII avatar

**Affected:** both files, identically. **Location:** lines 136–137 of `assets/dark.svg` and `assets/light.svg`.

```136:138:assets/dark.svg
<rect x="502" y="99" width="12" height="25" fill="#22D3EE" opacity="0.9">
  <animate attributeName="x" values="0.0;15.0;30.1;45.1;60.2;75.2;90.3;105.3;120.4;135.4;150.5;165.5;180.6;195.6;210.7;225.7;240.8;255.8;270.9;285.9;301.0;316.0;331.1" keyTimes="0.0000;0.0455;0.0909;0.1364;0.1818;0.2273;0.2727;0.3182;0.3636;0.4091;0.4545;0.5000;0.5455;0.5909;0.6364;0.6818;0.7273;0.7727;0.8182;0.8636;0.9091;0.9545;1.0000" calcMode="discrete" begin="0.9s" dur="1.9s" fill="freeze"/>
  <animate attributeName="opacity" values="0.9;0.9;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
</rect>
```

- The caret rect belongs to the typing-name animation in the **right** panel (name text starts at x=502, y=120). Its static `x="502"` is correct, but the `<animate attributeName="x">` values are **relative glyph offsets (0.0 … 331.1) that were never offset by the +502 panel origin**. They should be `502.0;517.0;…;833.1`.
- Consequence: from t=0.9 s to t=2.8 s the caret sweeps across canvas x=0 → 331 (through the **left** panel), and because of `fill="freeze"` it then **blinks indefinitely at canvas x≈331.1–343.1, y=99–124 — on top of the ASCII-art avatar** (left panel spans x=28–448; avatar rows at y=100/115 span x≈112–364). It never reaches its intended resting position (x≈833, beside the typed name and the 👋 emoji at x=843).
- Visually confirmed in headless-Chrome renders of the untouched originals at t=4.5 s and t=8 s (both themes): a solid cyan 12×25 block over the avatar's upper-right area. Pixel sample at (337, 111): `rgb(34,193,221)` = `#22D3EE` in dark, `rgb(28,187,215)` ≈ `#06B6D4` in light.
- Root cause is in the generator: `typing_name()` in `.build/generate_svgs.py` (lines 316–327) reuses the `widths` value list for both the `clipPath` rect **width** (correct — width is origin-independent) and the caret **x** (incorrect — needs `x + i*ch`).
- Per instructions the SVGs were **not** modified; the one-line fix would be to emit `f"{x + i*ch:.1f}"` for the caret's x values.

Note: the still frames produced by `.build/make_preview.py` mask this bug (they show the caret at its static x=502 because the preview strips animation state), which is likely why it slipped past earlier visual QA. Timeline-seek rendering of the original files exposes it.

---

## Check-by-check detail (identical results for both files unless noted)

### 1. Pure SVG

Every one of the 357 elements is in the `http://www.w3.org/2000/svg` namespace. Zero foreign-namespace elements, zero HTML elements, no `foreignObject`, `iframe`, `img`, `div`, `span`, no `<a>` anchors, no DOCTYPE/ENTITY declarations. Tag inventory: `svg` 1, `title` 1, `desc` 1, `defs` 1, `text` 86, `rect` 45, `g` 35, `circle` 20, `stop` 23, `path` 7, `linearGradient` 5, `radialGradient` 3, `filter` 4, `clipPath` 2, `mask` 1, `pattern` 1, `ellipse` 1, filter primitives 10, plus 110 animation elements.

### 2. No CSS

Zero `<style>` elements, zero `style=""` attributes, zero `class` attributes. All styling is via presentation attributes (`fill`, `stroke`, `opacity`, `font-family`, …).

### 3. No JavaScript

Zero `<script>` elements, zero `on*` event-handler attributes, zero `javascript:` hrefs. (There are no `href`/`xlink:href` attributes at all.)

### 4. SMIL-only animations

| Element | dark.svg | light.svg |
| --- | --- | --- |
| `animate` | 85 | 85 |
| `animateTransform` | 17 | 17 |
| `animateMotion` | 8 | 8 |
| `set` | 0 | 0 |
| **Total** | **110** | **110** |

No `animateColor`, no CSS animations/transitions, no other animation mechanisms.

### 5. Valid XML

Both files parse cleanly with a strict, non-recovering XML parser. Zero errors, zero warnings.

### 6. GitHub compatibility

- No `http(s)://`, `//`, or `file:` references anywhere (attributes or `url()` values).
- No `<image>` elements, no external fonts (`@font-face` impossible — no CSS).
- The single font stack is a pure system stack: `ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace`.
- All `url(#…)` references are local fragments. Fully self-contained; safe for GitHub's sanitizing camo proxy.

### 7. Dimensions

Both roots: `width="1180" height="610" viewBox="0 0 1180 610"` — exact match.

### 8. Responsive

`viewBox` present; `preserveAspectRatio` is unspecified, so the sane default `xMidYMid meet` applies. The image scales proportionally in README containers.

### 9. No clipping

- **Static:** all 86 text elements' extents were estimated (glyph advance ≈ 0.62 × font-size for the monospace stack, honoring `text-anchor`) and tested against the 1180×610 canvas and their panel bounds (left panel 28,28–448,582; right panel 472,28–1152,582). Zero overflows. Longest lines: focus row ends ≈ x=1044 (panel edge 1152); ASCII art rows span ≈ x=112–364 (panel 28–448); footer link row ends ≈ x=1111. The decorative blurred circles that extend past the canvas are all inside `clip-path="url(#cv)"` groups; zero unclipped overflow shapes.
- **Visual:** final-state PNGs rendered with headless Chrome (1180×610, confirmed pixel dimensions) were inspected in full and as 2× zoomed edge crops (right panel edge, left panel edge, footer strip). No cut-off glyphs at any panel edge in either theme. "Active Directory" and "Next.js" pills, the focus line, and the footer links all end well inside their panel.

### 10. No overlapping text

- **Rows:** all static/revealed text rows sit on distinct baselines (24–27 px spacing); pairwise horizontal-extent checks on shared baselines found zero collisions (label column ends ≈ x=597 max, value column starts x=642).
- **Role carousel:** 9 stacked `<text>` layers at (520, 154), each with an opacity `animate` over a shared 27 s cycle. Computed fully-visible windows are pairwise disjoint (3 s slot each with 0.45 s fade-out completing before the next fade-in starts) — exactly one role visible at a time. Confirmed visually at t=4.5 s ("System Administrator") and t=8 s ("Cloud Engineer (AWS)"): single role rendered.
- **However**, the misplaced typing caret documented above overlaps the ASCII-avatar text block — this is the sole overlap failure (10b), and it applies to both files.

### 11–14. Reference integrity (gradients, IDs, filters, masks)

**Defined IDs (18 per file):** `t`, `d` (title/desc, referenced by `aria-labelledby`), gradients `ag bs sw b1 b2 b3 gl sc`, filters `fb fg fs nz`, pattern `crt`, clipPaths `cv tn`, mask `am`.

| Category | Defined | Referenced | Broken refs | Orphans |
| --- | --- | --- | --- | --- |
| linearGradient | 5 (`ag bs sw gl sc`) | 5 | 0 | 0 |
| radialGradient | 3 (`b1 b2 b3`) | 3 | 0 | 0 |
| filter | 4 (`fb fg fs nz`) | 4 | 0 | 0 |
| mask | 1 (`am`) | 1 | 0 | 0 |
| clipPath | 2 (`cv tn`) | 2 | 0 | 0 |
| pattern | 1 (`crt`) | 1 | 0 | 0 |

- Reference usage counts: `ag`×33, `fg`×19, `fs`×13, `cv`×5, `fb`×4, `b1`×3, `b2`×3, `gl`×3, `bs`×2, and `am b3 crt nz sc sw tn`×1 each. Every `url(#id)` resolves; every defined paint server / filter / mask / clipPath is used. Zero orphan defs.
- **Duplicate IDs:** zero (18 unique IDs per file).
- **Filter primitives:** all primitives are standard (`feGaussianBlur`, `feMerge`/`feMergeNode`, `feTurbulence`, `feColorMatrix`, `feComponentTransfer`/`feFuncA`); the only named result (`b` in filter `fg`, `n` in filter `nz`) is defined before it is consumed; `in="SourceGraphic"` references are valid. No references to missing results.

---

## Warnings (non-failing)

1. **Misplaced caret bug** — reported as FAIL 10b above; also note the same rect briefly sweeps across the canvas border corner region (x=0–12) at t=0.9 s.
2. **`mask id="am"` and `clipPath id="tn"` are defined in the document body**, not inside `<defs>`. This is valid SVG and renders correctly everywhere tested, but is slightly unconventional.
3. **Emoji glyph (👋, U+1F44B)** on the name line is rendered from the platform emoji font; appearance varies by OS and it renders as a monochrome fallback in some renderers. Self-contained (no external font reference), so not a compatibility failure.
4. **Role-line blinking cursor** (`rect x="768" y="141"`) blinks from t=0, before the first role appears at t=3 s — cosmetic only; it sits clear of the widest role text (ends ≈ x=762).
5. `preserveAspectRatio` is implicit rather than explicit — the default (`xMidYMid meet`) is sane, listed here only for completeness.

---

## Rendered-preview confirmation

- Final-state stills (`.build/render_dark.png`, `.build/render_light.png`, 1180×610) rendered via headless Chrome from the `make_preview.py` harness: layout, pills, ASCII avatar, info rows, and footer links all correct and unclipped in both themes.
- Original, unmodified SVGs rendered with the SMIL timeline seeked to t=2 s, 4.5 s and 8 s (`.build/snap_*.png`): typing/reveal sequencing correct, exactly one carousel role visible per frame; caret defect visible as described.
- Edge-zoom crops (`.build/edge_right_*.png`, `.build/edge_left_*.png`, `.build/edge_bottom_*.png`) show no glyph clipping at any panel boundary.

**Bottom line:** both banners are clean, self-contained, GitHub-safe SMIL SVGs; the single defect to fix (in `.build/generate_svgs.py`, then regenerate) is the typing-caret `x` animation missing its +502 offset.
