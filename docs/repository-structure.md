# Repository Structure

```text
.
├── README.md                     Profile page: hero <picture>, badges, stats, snake, projects
├── LICENSE                       MIT © 2026 Aaditya Padiya
├── .gitignore                    OS/editor/tooling exclusions
├── robots.txt                    Crawl policy + sitemap pointer
├── sitemap.xml                   Profile, portfolio, LinkedIn, project URLs
├── favicon.svg                   Animated "AP" monogram (rotating accent gradient)
├── profile.json                  Full structured profile extracted from the resume
├── skills.json                   Skill taxonomy by category (11 categories)
├── theme.json                    Design tokens: colors, type scale, radii, spacing, effects
├── metadata.json                 Repository metadata: author, assets, workflows, keywords
├── .markdownlint.json            Rules for markdown-lint.yml (long-line/HTML/heading rules relaxed)
├── .svgo.config.mjs              SMIL-safe SVGO config used by svg-optimize.yml
│
├── assets/
│   ├── dark.svg                  Hero banner, dark theme (1180×610, 111 SMIL animations)
│   └── light.svg                 Hero banner, light theme (identical timing, light tokens)
│
├── docs/
│   ├── design-system.md          Tokens, typography, layout, surface recipes
│   ├── animation-report.md       Full animation inventory with timings
│   ├── svg-optimization-report.md  Sizes, techniques, SVGO overrides
│   ├── performance-report.md     Payload, render cost, network behavior
│   ├── accessibility-report.md   Contrast matrix, semantics, motion safety
│   ├── readme-validation-report.md   Full URL/embed audit of README.md
│   ├── workflow-validation-report.md Deep validation of all 6 workflows
│   ├── repository-structure.md   This file
│   └── previews/                 Rendered stills of the hero (t≈10.5 s, intro settled)
│       ├── dark-preview.png
│       └── light-preview.png
│
├── .build/                       Local tooling (not needed at runtime)
│   ├── generate_svgs.py          Single generator emitting both hero themes
│   ├── optimize_svgs.py          SMIL-safe post-generation size optimizer
│   ├── make_preview.py           Final-state SVG stills for visual QA
│   ├── make_final_previews.py    Headless-Chrome renderer for docs/previews/*.png
│   └── validate.py               Quality gate: XML/JSON/YAML/path/size checks
│
└── .github/workflows/
    ├── snake.yml                 Contribution snake → `output` branch (12 h cron + manual)
    ├── svg-validate.yml          XML well-formedness + GitHub-compat rules on push/PR
    ├── markdown-lint.yml         markdownlint-cli2 on README + docs
    ├── link-check.yml            lychee scan (weekly cron + push); opens issue on failures
    ├── svg-optimize.yml          SVGO dry-run + SMIL-survival assertion
    └── health-check.yml          Weekly: required files, README refs, JSON parse
```

## How the Pieces Connect

- `README.md` is the only file GitHub renders on the profile; it references `assets/*.svg`, `favicon.svg`, `LICENSE`, and two docs.
- `.build/generate_svgs.py` is the source of truth for both hero SVGs — edit it, regenerate, then run `.build/optimize_svgs.py` (SMIL-safe minifier) rather than hand-editing the XML. It embeds data that mirrors `profile.json` and `skills.json`.
- **`.build/` policy:** the four tooling scripts above are tracked in git on purpose (they document how the artwork is produced and let anyone regenerate it). Everything else `.build/` accumulates locally — test SVGs, render screenshots, scratch analyses — is ignored via `.gitignore` (`.build/*` with explicit `!` exceptions) and never ships.
- `docs/previews/*.png` are static stills of both hero themes for viewers who can't run the animation (and for design review); regenerate them with headless Chrome after any generator change: [dark preview](./previews/dark-preview.png) · [light preview](./previews/light-preview.png).
- `theme.json` documents the same tokens the generator hardcodes; if you change a color, change it in both places (generator + tokens) and regenerate.
- The snake images referenced in the README (`raw.githubusercontent.com/…/output/github-snake*.svg`) do not exist until `snake.yml` has run once on GitHub.

## Setup Checklist (after pushing)

1. Create a repository named exactly **`aadityapa`** (username/username) so GitHub treats the README as the profile page.
2. Push `main`, then run the **Contribution Snake** workflow manually once (Actions → Contribution Snake → Run workflow) to create the `output` branch.
3. Under *Settings → Actions → General*, ensure workflow permissions allow **Read and write** (the snake workflow pushes to `output`).
4. Verify the hero renders on the profile in both light and dark appearance settings.
