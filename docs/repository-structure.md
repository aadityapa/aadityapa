# Repository Structure

```text
.
├── README.md                     Profile page: hero <picture>, badges, visualizations, stats, snake
├── LICENSE                       MIT © 2026 Aaditya Padiya
├── .gitignore                    OS/editor/tooling exclusions + .build allowlist
├── robots.txt                    Crawl policy + sitemap pointer
├── sitemap.xml                   Profile, portfolio, LinkedIn, project URLs
├── favicon.svg                   Animated "AP" monogram (rotating accent gradient)
├── profile.json                  Structured profile (synced subset of data/profile.json)
├── skills.json                   Skill taxonomy by category (11 categories)
├── theme.json                    Design tokens: colors, type scale, radii, spacing, effects
├── metadata.json                 Repository metadata: author, assets, workflows, keywords
├── .markdownlint.json            Rules for markdown.yml (long-line/HTML/heading rules relaxed)
├── .svgo.config.mjs              SMIL-safe SVGO config used by optimize-svg.yml
│
├── data/
│   └── profile.json              Canonical v12 profile: identity, timeline, certifications,
│                                 grouped skills, projects with API-verified repo links
│
├── assets/                       All SMIL-animated, no JS/CSS, dark+light pairs
│   ├── dark.svg / light.svg              Hero banner (1180×610, 179 animations each,
│   │                                     photo-derived ASCII portrait)
│   ├── ecosystem-dark/-light.svg         Orbital technology map (1180×760)
│   ├── architecture-dark/-light.svg      8-section architecture showcase (1180×800)
│   ├── timeline-dark/-light.svg          Career timeline with 5 nodes (1180×620)
│   ├── certifications-dark/-light.svg    4 certification badge cards (1180×360)
│   └── projects-dark/-light.svg          8 featured project cards (1180×740)
│
├── docs/
│   ├── design-system.md          Tokens, typography, layout, surface recipes, v12 components
│   ├── animation-report.md       Full animation inventory with timings
│   ├── svg-optimization-report.md  Sizes, techniques, SVGO overrides
│   ├── performance-report.md     Payload, render cost, network behavior
│   ├── accessibility-report.md   Contrast matrix, semantics, motion safety
│   ├── readme-validation-report.md   URL/embed audit of README.md (v11 baseline)
│   ├── workflow-validation-report.md Deep validation of the workflows (v11 baseline)
│   ├── repository-structure.md   This file
│   └── previews/                 Rendered stills of the hero (t≈10.5 s, intro settled)
│       ├── dark-preview.png
│       └── light-preview.png
│
├── reports/                      Fresh v12 reports with measured data
│   ├── validation-report.md      XML/SMIL/id/ref/size gate results for all 13 SVGs
│   ├── optimization-report.md    Per-file sizes, optimization passes, budgets
│   ├── accessibility-report.md   Contrast ratios, titles/descs, motion inventory
│   └── performance-report.md     Payload totals, filter costs, render measurements
│
├── .build/                       Local tooling (tracked scripts document how art is produced)
│   ├── generate_svgs.py          Hero generator (both themes)
│   ├── generate_ecosystem.py     Ecosystem generator
│   ├── generate_architecture.py  Architecture generator
│   ├── generate_timeline.py      Timeline generator
│   ├── generate_certifications.py Certifications generator
│   ├── generate_projects.py      Projects generator
│   ├── photo_to_ascii.py         Real photo → ASCII portrait pipeline (Pillow)
│   ├── ascii_face.py             Generated ASCII grid consumed by generate_svgs.py
│   ├── optimize_svgs.py          SMIL-safe post-generation size optimizer
│   ├── make_preview.py           Final-state SVG stills for visual QA
│   ├── make_final_previews.py    Headless-Chrome renderer for docs/previews/*.png
│   └── validate.py               Quality gate: XML/JSON/YAML/path/size checks
│
└── .github/workflows/
    ├── snake.yml                 Contribution snake → `output` branch (12 h cron + manual)
    ├── stats-refresh.yml         Daily re-dispatch of the snake so the profile stays fresh
    ├── validate-svg.yml          XML well-formedness + GitHub-compat rules on push/PR
    ├── markdown.yml              markdownlint-cli2 on README + docs + reports
    ├── link-check.yml            lychee scan (weekly cron + push); opens issue on failures
    ├── optimize-svg.yml          SVGO dry-run + SMIL-survival assertion on every assets SVG
    └── repository-health.yml     Weekly: required files, README refs, JSON parse
```

## How the Pieces Connect

- `README.md` is the only file GitHub renders on the profile; it references the six `<picture>` pairs in `assets/`, `favicon.svg`, `LICENSE`, and the docs/reports.
- Every SVG in `assets/` is emitted by a generator in `.build/` — edit the generator and regenerate rather than hand-editing XML. The hero additionally goes through `.build/optimize_svgs.py` (SMIL-safe minifier).
- The ASCII portrait chain: portfolio photo → `photo_to_ascii.py` → `ascii_face.py` → `generate_svgs.py` → `assets/dark.svg`/`light.svg`.
- **`.build/` policy:** the tooling scripts above are tracked in git on purpose (they document how the artwork is produced and let anyone regenerate it). Everything else `.build/` accumulates locally — test SVGs, render screenshots, scratch analyses — is ignored via `.gitignore` (`.build/*` with explicit `!` exceptions) and never ships.
- `data/profile.json` is the canonical structured profile (v12); the root `profile.json` keeps the original flat schema in sync for backwards compatibility. The generators embed data that mirrors both.
- `theme.json` documents the same tokens the generators hardcode; if you change a color, change it in both places and regenerate.
- The snake images referenced in the README (`raw.githubusercontent.com/…/output/github-snake*.svg`) do not exist until `snake.yml` has run once on GitHub.

## Setup Checklist (after pushing)

1. Create a repository named exactly **`aadityapa`** (username/username) so GitHub treats the README as the profile page.
2. Push `main`, then run the **Contribution Snake** workflow manually once (Actions → Contribution Snake → Run workflow) to create the `output` branch.
3. Under *Settings → Actions → General*, ensure workflow permissions allow **Read and write** (the snake workflow pushes to `output`; `stats-refresh.yml` needs `actions: write`, which it declares).
4. Verify the hero and all five visualization sections render on the profile in both light and dark appearance settings.
