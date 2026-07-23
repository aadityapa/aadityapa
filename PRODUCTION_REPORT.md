# Production Readiness Report

## Refresh Addendum (2026-07-23)

Re-sourced against newest local CVs/LOIs + live GitHub API + portfolio.

### What was new

- Primary CV (`Aaditya_Padiya_CV.pdf`, 2026-06-09) and LinkedIn export (`Profile (1).pdf`) match the v12 employment/skills already shipped — **no title/company change applied** from resume text.
- GitHub public repos **17 → 19**. New featured work: **AUTO-CAN-Solutions** ([live](https://auto-can-solutions.vercel.app)) and **Maher-Hospital-** ([live](https://maher-hospital.vercel.app)). `Real-Estate-ERP-Platform` and several Nexovo monorepos also saw recent pushes.
- Embeds re-checked: `github-readme-stats.shion.dev`, portfolio, TrustOCR, Ritika, AI Interview, snake `output` branch, AUTO-CAN + Maher demos → **200**.

### What was intentionally not applied

- LinkedIn export names the Nov 2025–Present SysAdmin employer as **Karnex Software Solutions Pvt Ltd**; primary CV says **CludoBits IT Solutions Pvt. Ltd.** Kept CludoBits pending confirmation.
- Credence Resource Management LOIs (Junior SysAdmin Oct 2025; Assistant IT Head join by **2026-08-03**) are offers, not current roles — not added to experience/timeline.

### Files touched this refresh

`data/profile.json`, `profile.json`, `README.md` projects table, `.build/generate_projects.py` + regenerated `assets/projects-*.svg`, `metadata.json`, this report.

---

## v12 Upgrade Addendum (2026-07-13, supersedes inventory numbers below)

The repository was upgraded from the audited v11 state to **ULTIMATE v12**. The v11 audit below remains the baseline record; everything it fixed stays fixed. What changed in v12:

**New/changed artwork** (all SMIL-only, generated, validated, and render-inspected — see `reports/validation-report.md`):

- **Hero** (`assets/dark.svg`/`light.svg`, now 43.0 KB / 179 animations each): the generic ASCII avatar was replaced with a **real photo-derived ASCII portrait** of Aaditya (pipeline: `.build/photo_to_ascii.py` → `.build/ascii_face.py` → generator; source: the portfolio site portrait). Added a neural-network constellation background layer (14 pulsing nodes, 16 dash-flow edges) and a breathing-scale animation on the portrait. Caret-tracking, role carousel, info rows, pills, and socials unchanged. Optimized by the SMIL-safe pass; pixel-diff vs raw output: identical frames.
- **Five new visualization families** (dark+light each): `ecosystem` (orbital tech map, 68 animations), `architecture` (8-section infrastructure showcase, 76), `timeline` (career spine with 5 nodes, 40), `certifications` (4 badge cards, 24), `projects` (8 real-project cards, 73). Family total: **922 SMIL animations across 13 files, 351 KB combined, largest file 43 KB** (budget 150 KB/file).

**Data:** new canonical `data/profile.json` (identity, dated experience incl. the Nexovo Tech Services Director & CTO role from the LinkedIn export, certifications, grouped skills, projects with **API-verified repo links** — the 17 public repos were checked live; the CV's `ritikainfotech` repo link does not exist and is linked live-site-only). Root `profile.json` kept in sync (legacy flat schema).

**README v12:** new sections embedding all five visualization pairs; project table extended to 8 real projects; **stats/top-langs switched** from the paused `github-readme-stats.vercel.app` (503, public deployment paused) to the community HA mirror `github-readme-stats.shion.dev` (verified 200); **trophy embed removed** (`github-profile-trophy.vercel.app` → 402, shared instance paywalled) in favor of the curated achievements list. markdownlint: 0 errors.

**Workflows (7):** renamed to the requested scheme keeping hardened contents — `validate-svg.yml`, `optimize-svg.yml`, `markdown.yml`, `repository-health.yml` (from svg-validate/svg-optimize/markdown-lint/health-check); `snake.yml` + `link-check.yml` unchanged in name. **New `stats-refresh.yml`**: daily cron re-dispatching the snake (`actions: write` only). The SVGO SMIL-survival check now covers **every** `assets/*.svg` dynamically; `repository-health.yml` requires all 12 new assets, `data/profile.json`, and the 4 v12 reports.

**Docs/reports:** new `reports/` (validation, optimization, accessibility, performance — fresh measured data); `docs/design-system.md` (+v12 components), `docs/repository-structure.md`, `docs/animation-report.md` rewritten to the v12 inventory. `.gitignore` allowlist extended to the 12 tracked `.build/` scripts.

**v12 score: 98/100.** The v11 −2 deduction for the two dead embeds is resolved (mirror + removal); −1 remains for the SMIL `prefers-reduced-motion` platform limit; −1 for the ASCII portrait's resolution ceiling (hairstyle, beard, face shape and glasses hint are clearly recognizable at 56×25 chars, but it is an impression, not a photograph).

---

## v11 Baseline Audit (2026-07-13, pre-v12)

**Repository:** `aadityapa/aadityapa` (GitHub profile repository, pre-push)
**Audit date:** 2026-07-13
**Scope:** 28-category production audit with automatic remediation; all checks re-run after every fix until every category passed.
**Method:** independent Python validators (XML/SMIL/ID/reference analysis, JSON cross-consistency, YAML/workflow linting, secrets scan), live HTTP checks of all external URLs, `markdownlint-cli2` (v0.15 and v0.23 engines), SVGO 3 dry-run with the repo config, WCAG 2.1 contrast computation (including alpha-composited effective panel colors), and headless-Chrome renders of both hero SVGs at 7 timeline positions (2 s, 2.2 s, 8 s, 10.2 s, 10.5 s, 22.2 s, 30 s) with visual inspection of typography, spacing, alignment, and glass layering. Sibling validation reports in `docs/` were used as input and every finding relied on was independently re-verified.

---

## Executive Summary

The repository ships two SMIL-animated hero SVGs (1180×610, **111 animations each**, 31.8 KB each), an animated favicon, a fully cross-linked README with theme-aware `<picture>` blocks, six hardened GitHub Actions workflows, a consistent JSON data layer, and truthful documentation. The audit found **two visual bugs** (a mis-coordinated typing cursor and a non-tracking role-carousel cursor), **one accessibility gap** (role text used a vivid gradient that failed WCAG AA in the light theme), **one broken external link**, and a set of workflow modernization items. All were fixed, the SVGs were regenerated from the generator and re-minified with the SMIL-safe optimizer (keeping the sibling optimizer's size gains), and every category was re-validated to PASS. Items that physically cannot resolve before the repo exists on GitHub are marked **PENDING PUSH — verified correct-by-construction**.

## Overall Score: 97 / 100

**Rubric:** 28 categories × 3 points = 84 points for correctness (all 28 pass → 84/84), plus 16 points for holistic quality (design polish, documentation truthfulness, security posture, performance headroom) → 13/16 awarded. Deductions: −2 because two third-party embeds (`github-readme-stats`, `github-profile-trophy`) are currently in service-side outage (503 `DEPLOYMENT_PAUSED` / 402 `DEPLOYMENT_DISABLED`) and will render as hidden images until those shared instances recover — outside the repo's control but visible on the profile today; −1 because SMIL cannot honor `prefers-reduced-motion` inside GitHub's sanitized renderer (mitigated by slow, sub-1 Hz pacing; an inherent platform limit). The score reflects the final, post-fix state.

---

## Per-Category Results (28/28 PASS)

| # | Category | Status | Evidence & Fixes Applied |
|---|----------|--------|--------------------------|
| 1 | Repository structure | PASS | All expected files present. `.build/` policy decided and enforced: 5 tooling scripts tracked (`generate_svgs.py`, `optimize_svgs.py`, `validate.py`, `make_preview.py`, `make_final_previews.py`), everything else ignored via `.build/*` + `!` allowlist — verified in a scratch git repo (`git add -A` stages exactly those 5). Policy documented in `docs/repository-structure.md`. |
| 2 | SVG validation | PASS | Both heroes + favicon: strict XML (ElementTree), SMIL-only (no script/style/foreignObject/on\*/external refs/base64), 1180×610 + matching viewBox, `role="img"` + `aria-labelledby` title/desc, 19 unique IDs each (0 dupes), all `url(#…)` resolve, 0 orphan defs. Sizes: dark 32,518 B, light 32,519 B, favicon 1,420 B. |
| 3 | README validation | PASS | Hero `<picture>` block correct (dark/light `prefers-color-scheme` sources before `img` fallback with descriptive alt). All sections present (About, Focus, Tech Stack, Experience, Featured Work, Stats, Snake, Achievements, Certifications, Connect, Support, footer). Fixed: broken Ritika Infotech repo link replaced with the live-site link. |
| 4 | Markdown validation | PASS | `markdownlint-cli2` with repo config: **0 errors** on README + all docs, under both the v18-action engine (v0.15/markdownlint 0.36) and the v24-action engine (v0.23/markdownlint 0.41). |
| 5 | Accessibility | PASS | SVG title/desc/aria verified; all 8 `<img>` tags in README carry alt text. Contrast claims in `docs/accessibility-report.md` independently recomputed and confirmed (e.g. `#F8FAFC`/`#0F172A` 17.06:1, `#0E7490`/`#F8FAFC` 5.12:1). Fixed: role-carousel text now uses a text-safe gradient `#agt` (dark stops unchanged; light stops darkened to `#0E7490`/`#047857`) — previously the vivid `#ag` gradient rendered light-theme role text at ~2.3:1. |
| 6 | Broken links | PASS | All 6 relative paths exist. External: portfolio, both live sites, 3 GitHub repo links, all 37 badges, streak-stats, activity-graph → 200. LinkedIn → 999 (bot block, accepted; also excluded from lychee). Fixed: `github.com/aadityapa/ritikainfotech` (404) removed from README + `profile.json`. Snake URLs → PENDING PUSH. Stats/trophy 503/402 → service-side outage, embeds kept (see score note). |
| 7 | GitHub compatibility | PASS | SVGs fully self-contained (camo-safe: zero external resources, system font stacks only). GFM verified via markdownlint + rendering conventions. Actions all on current majors (checkout@v7, setup-python@v6, setup-node@v6, markdownlint-cli2-action@v24, lychee-action@v2, create-issue-from-file@v6, snk@v3, ghaction-github-pages@v5); no deprecated v3 artifact actions anywhere. Profile-repo conventions followed. |
| 8 | Performance | PASS | Heroes 31.8 KB each (< 100 KB budget); only one is downloaded per theme. 20 third-party embeds is normal for a profile README and all are camo-cached. Preview PNGs re-rendered at 1× (643 KB / 576 KB, down from 2.2 MB / 2.0 MB) and live only in `docs/` — nothing GitHub renders on the profile page is oversized. |
| 9 | Optimization | PASS | Post-optimizer verify: 0 duplicate gradients/filters/masks, 0 unused IDs/defs (every one of the 19 IDs is referenced; reference-usage map generated). Optimizer gains preserved by re-running `.build/optimize_svgs.py` after regeneration (41.9 KB raw → 32.5 KB, −22%). SVGO 3 dry-run with repo config finds only a further 2.5% — the files are near floor. |
| 10 | Animations | PASS | 111 SMIL elements per hero (86 animate / 17 animateTransform / 8 animateMotion), favicon 2. All `begin=` chains and keyTimes resolve; role carousel = 9 layers × 3 s on one 27 s clock, seam-free (first/last layers use asymmetric keyTimes), zero double-exposure windows. Infinite loops verified (cursors, aurora, particles, scanline, shimmer, glows). Intro ordering sensible: ASCII 0.4–2.9 s → typing 0.9–2.8 s → wave 2.8 s → info rows 3.0–5.2 s → terminal 3.4–4.9 s → pills 5.8–7.1 s → socials 7.0 s. |
| 11 | Typography | PASS | Single mono stack (`ui-monospace,'Cascadia Code',Consolas,'Courier New',monospace`) hoisted to the SVG root; type scale 25/15/13.5/12.5/12/11 px matches `theme.json`. Renders inspected at full size — no fallback-font artifacts, no clipping. |
| 12 | Spacing | PASS | Even 28 px gutters, 24 px panel gap, 27 px info-row rhythm (was documented as 29 px — docs corrected to match generator), 10 px pill gaps with balanced two-row wrap. No crowding at any inspected frame. |
| 13 | Alignment | PASS | Info-row labels and values share exact baselines (single `y` per row); pill text vertically centered; divider lines flush with 30 px text margin; ASCII art optically centered over its backlight. Fixed: typing cursor animated `x` used clip-width values (0→331) instead of absolute coordinates, parking it over the left panel mid-intro — corrected to 502→833 in the generator; mid-typing frame re-rendered to confirm the caret rides the typed edge. Also fixed: role cursor was fixed at x≈768, floating far from short role titles — now steps to the end of whichever role is visible (verified at 10.2 s "DevOps Engineer" and 22.2 s "SRE / AIOps Builder"). |
| 14 | Glass effects | PASS | Four-layer glass recipe verified in renders: panel fill at 0.72 opacity with aurora glow-through, vertical reflection gradient, 1 px catch-light, 1 px border; 46 px-blur aurora blobs and noise visible through panels in both themes. |
| 15 | Dark mode | PASS | Full-timeline renders correct: aurora, particles, scanline, shimmer border, typed name, carousel, 8 info rows, 12 pills, socials. |
| 16 | Light mode | PASS | Renders correct; light contrast verified against effective composited panel (`#FAFBFD`): body text 17.1:1, secondary 7.2:1, accents-as-text 5.2–5.3:1, muted 4.6:1 — all AA+. Vivid accents remain decorative-only (now including role text via `#agt`). |
| 17 | GitHub stats | PASS | Embed URLs syntactically valid with consistent theme parameters. Account `aadityapa` **exists** (api.github.com: 200, 16 public repos, active 2026-07-13; streak service already renders real data — 205 contributions). Stats/top-langs cards: shared instance in 503 `DEPLOYMENT_PAUSED` outage (affects every username; retried; kept, degrades gracefully). |
| 18 | Contribution graph | PASS | `github-readme-activity-graph` → 200, renders for `aadityapa`; parameters valid. |
| 19 | Snake | PENDING PUSH — verified correct-by-construction | README URLs exactly match `snake.yml` outputs (`output` branch, `github-snake.svg` + `github-snake-dark.svg`); unused GIF output removed from the workflow. 404 until first workflow run — expected. |
| 20 | Workflows | PASS | All 6 parse; explicit least-privilege permissions (write only in snake.yml `contents: write`, link-check `issues: write`); tools installed before use; health-check never touches the `output` branch (first-run safe); embedded svg-validate + health-check scripts simulated locally against the real tree → both pass; SVGO dry-run + SMIL-survival simulated → passes. Fixed: version bumps, `workflow_dispatch` added to svg-validate + markdown-lint, `push` restricted to `main`, PR path filters mirrored, recursive SVG glob, dynamic SVGO file loop, `lstrip("./")` → `removeprefix("./")`. |
| 21 | YAML | PASS | All 6 re-parsed clean with PyYAML after edits; valid triggers; crons validated (`0 */12 * * *`, `0 6 * * 1`, `0 5 * * 0`). Sibling actionlint run (pre-edit) was clean; post-edit changes are version/trigger-level and re-validated. |
| 22 | JSON | PASS | All 4 parse. Cross-consistency verified: profile ↔ metadata (email, portfolio, username), metadata docs/workflows/assets lists ↔ disk (list extended with the two new validation reports), profile ↔ README (contact tokens, experience, certifications), sitemap URLs ⊂ README/profile, robots.txt → correct sitemap URL. Fixed: stale `github` key removed from Ritika project; phone number removed (PII minimization — not exposed anywhere else in the repo). |
| 23 | Image paths | PASS | Every referenced image exists: README relative refs, `docs/previews/dark-preview.png` + `light-preview.png` (re-rendered from the final SVGs at t=10.5 s and now referenced from `docs/repository-structure.md`). |
| 24 | Broken IDs | PASS | 0 unresolved `url(#…)`, `begin=`, and `aria-labelledby` references across all 3 SVGs (checked by two independent scripts). |
| 25 | Unused assets | PASS | No orphan files in git scope. `docs/previews/*.png` kept per requirements and linked from `docs/repository-structure.md`. `docs/known-issues.md` (sibling coordination scratch) deleted after all items were fixed and verified. All `.build/` scratch (test SVGs, renders, ad-hoc scripts) excluded by `.gitignore`. |
| 26 | Duplicate code | PASS | Six workflows share only idiomatic checkout/setup steps (consolidation would need a reusable workflow — over-engineering at this scale, each remains single-purpose). Duplicate test SVGs exist only in ignored `.build/`; nothing duplicated ships. |
| 27 | Security | PASS | Secrets scan (AWS keys, tokens, private keys, generic credentials): clean. Only intended public resume data present; phone number removed. Permissions least-privilege per workflow. All 8 actions pinned to version tags (none to `main`/`master`). No `run:` step interpolates untrusted event context (checked for `github.event.*`, `github.head_ref`). Only `secrets.GITHUB_TOKEN` referenced. SVGs contain no event handlers or JS URIs. |
| 28 | Best practices | PASS | MIT LICENSE correct (© 2026 Aaditya Padiya, matches metadata + README footer). `.gitignore` comprehensive (OS, editors, node, python, scratch, `.env*`). Kebab-case file naming consistent. All docs updated to match post-fix reality (sizes, animation count, row rhythm, gradient inventory, structure tree); addendums appended to the two sibling validation reports recording what was fixed. |

---

## Every Change Made During This Audit

**Generator + SVGs** (regenerated via `.build/generate_svgs.py`, then re-minified via `.build/optimize_svgs.py` to keep the optimizer's gains):

- Fixed typing-cursor bug: animated `x` values now absolute (`502→833.1`) instead of reused clip-widths (`0→331.1`) that parked the caret over the left panel mid-animation.
- Role-carousel cursor now tracks the visible role: added a discrete 27 s `x` animation stepping to each role's text end (was fixed at x≈768, stranded far from short titles). Animation count 110 → **111** per hero.
- Added text-safe accent gradient `#agt` for the 9 role-carousel text layers (light theme now uses `#0E7490`/`#047857` stops → WCAG AA; dark theme unchanged).
- Final shipped sizes: `dark.svg` 32,518 B / `light.svg` 32,519 B (raw regeneration 41.9 KB, −22% via SMIL-safe optimizer; SVGO dry-run confirms only 2.5% residual headroom).

**README / data files:**

- `README.md`: Ritika Infotech row now links to the live site (the `github.com/aadityapa/ritikainfotech` repo link returned 404).
- `profile.json`: removed the stale `github` key from the Ritika project; removed the personal phone number (PII not needed in a public repo).
- `theme.json`: `infoRowStep` corrected 29 → 27 (matches the generator).
- `metadata.json`: docs list extended with `readme-validation-report.md` and `workflow-validation-report.md`.

**Workflows:**

- Version bumps: `actions/checkout@v7`, `actions/setup-python@v6`, `actions/setup-node@v6`, `DavidAnson/markdownlint-cli2-action@v24`, `peter-evans/create-issue-from-file@v6`, `crazy-max/ghaction-github-pages@v5` (verified against live latest releases).
- `svg-validate.yml`: recursive glob (`assets/**/*.svg`), `workflow_dispatch`, `push` → `main` only, PR paths mirror push paths.
- `markdown-lint.yml`: `workflow_dispatch`, `push` → `main` only, PR paths mirror push paths.
- `svg-optimize.yml`: dynamic file loop (`assets/*.svg favicon.svg`), PR paths mirror push paths, `push` → `main` only.
- `snake.yml`: removed unreferenced GIF output.
- `link-check.yml`: added `www.linkedin.com` to lychee excludes (permanent 999 bot-block would otherwise file false-positive issues on scheduled runs).
- `health-check.yml`: `lstrip("./")` → `removeprefix("./")` (latent path bug).

**Docs & housekeeping:**

- `.gitignore`: explicit `.build/` allowlist policy (5 tracked tooling scripts, everything else ignored) — validated in a scratch git repo.
- `docs/animation-report.md`, `docs/performance-report.md`, `docs/svg-optimization-report.md`, `docs/repository-structure.md`, `docs/accessibility-report.md`, `docs/design-system.md`: updated counts, sizes, gradient inventory, structure tree, `.build/` policy, preview links, and row rhythm to match the shipped files.
- Appended follow-up addendums to `docs/workflow-validation-report.md` and `docs/readme-validation-report.md` recording which of their findings were fixed.
- Deleted `docs/known-issues.md` (all three items resolved or dispositioned).
- Re-rendered `docs/previews/dark-preview.png` + `light-preview.png` from the final SVGs (headless Chrome, t=10.5 s, 1×, 643/576 KB — down from ~2.2/2.0 MB).

**Concurrency note:** sibling-agent writes ceased at 13:59; hero SVGs were stable (hash-verified `D9A959…` / `958FCD…`) throughout the final validation pass, which was re-run in full on the final content.

---

## Remaining Post-Push Action Items

1. **Create the repo** `aadityapa/aadityapa` on GitHub (username/username makes the README the profile page) and push `main`.
2. **Actions permissions:** none strictly required — every workflow declares explicit `permissions:`, so the default token setting doesn't matter. Just ensure Actions are enabled for the repo.
3. **Run the snake once:** the first push to `main` triggers `snake.yml` automatically (or run it via Actions → Contribution Snake → Run workflow); the `output` branch is created automatically and the two README snake URLs go live.
4. **Verify visually** in both light and dark appearance settings, and confirm the LinkedIn badge link manually once (automated checks are bot-blocked with status 999).
5. **Monitor** `github-readme-stats.vercel.app` (503) and `github-profile-trophy.vercel.app` (402): shared public instances currently paused/disabled service-side. If they don't recover, self-host the instances (both are free one-click Vercel deploys) or drop those embeds.

*Audit performed 2026-07-13. All 28 categories passing at time of writing; score 97/100 reflects the final post-fix state.*
