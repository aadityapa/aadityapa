# ASCII Portrait Regeneration — 2026-07-13

## Source
- **Primary:** `assets/source-portrait.png` (copied from user-attached screenshot `Screenshot_2026-07-13_145313`)
- **Replaced:** portfolio full-body PNG crop (generic symmetric output)

## Grid
- **56 × 29** monospace cells (cell aspect 0.486, font 10.5 / lh 13)
- **70-level** density ramp
- Crop box: `(55, 15, 580, 565)` on 638×761 source

## Iterations
4 parameter variants tested (`v1_base`, `v2_tighter`, `v3_glasses`, `v4_quiff`); **v3_glasses** selected for edge emphasis and glasses band readability.

## QA artifacts
- Side-by-side: `.build/photo/ascii_side_by_side_v2.png`
- Hero avatar crop: `.build/photo/hero_avatar_crop.png`
- Previews: `docs/previews/dark-preview.png`, `docs/previews/light-preview.png`

## Shipped sizes
| File | Bytes | Animations |
|------|------:|-----------:|
| `assets/dark.svg` | 46,730 | 183 |
| `assets/light.svg` | 46,731 | 183 |

## Visual verdict
Portrait is clearly asymmetric three-quarter pose with quiff mass on viewer-left, dense beard block, and blazer shoulders. Recognizable vs. prior symmetric `@#%*` mask. Glasses appear as a subtle lighter horizontal band — readable at close zoom but not bold at banner scale.
