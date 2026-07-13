# GitHub Actions Workflow Validation Report

**Validation date:** 2026-07-13
**Repository:** `aadityapa/aadityapa` (GitHub profile repository, pre-push local validation)
**Workflows validated:** `.github/workflows/` — `snake.yml`, `svg-validate.yml`, `markdown-lint.yml`, `link-check.yml`, `svg-optimize.yml`, `health-check.yml`

**Tooling used:**

- Strict YAML parsing with Python `yaml.safe_load` (PyYAML) — all 6 files parsed cleanly; the YAML 1.1 `on:` → boolean `True` key quirk was accounted for.
- **actionlint v1.7.12** (official binary) — ran against all 6 workflows: **0 errors, exit code 0**. Note: actionlint's optional `shellcheck` and `pyflakes` integrations were not available on the validation machine, so `run:` shell/python bodies were reviewed manually instead.
- Local simulation of every embedded Python script (`svg-validate.yml`, `health-check.yml`) against the actual repo files.
- Local run of `markdownlint-cli2` with the repo's `.markdownlint.json` against `README.md` and `docs/**/*.md` — **0 errors**.
- Live GitHub API queries for the latest release of every referenced action.
- Cron field-by-field validation (5-field syntax, ranges).

No workflow files were modified. All fixes below are **recommendations only**.

---

## Summary Table

| Workflow | Syntax | Permissions | Versions | Paths | Triggers | Compatibility | Overall |
|---|---|---|---|---|---|---|---|
| `snake.yml` | PASS | PASS | WARN | PASS | WARN | PASS | **WARN** |
| `svg-validate.yml` | PASS | PASS | WARN | WARN | WARN | PASS | **WARN** |
| `markdown-lint.yml` | PASS | PASS | WARN | PASS | WARN | PASS | **WARN** |
| `link-check.yml` | PASS | PASS | WARN | PASS | PASS | WARN | **WARN** |
| `svg-optimize.yml` | PASS | PASS | WARN | WARN | WARN | PASS | **WARN** |
| `health-check.yml` | PASS | PASS | WARN | PASS | PASS | WARN | **WARN** |

**No FAIL-level findings.** All six workflows are syntactically valid, schema-correct, declare explicit `permissions:` blocks, use only Linux/bash-compatible commands on valid `ubuntu-latest` runners, reference no non-existent secrets, and have no unpinned `@main`/`@master` action refs. All warnings are listed individually below.

---

## Check details (what passed)

### 1. YAML syntax & GitHub Actions schema — all PASS

- All 6 files parse with `yaml.safe_load` without error.
- Every workflow has `name`, a trigger block (`on`, parsed as YAML boolean `True` key — handled), and `jobs`.
- Every job declares `runs-on: ubuntu-latest` (valid runner label) and a non-empty `steps` list; every step has exactly one of `uses:`/`run:`.
- Every job declares a `timeout-minutes` (5–10 min) — good practice.
- **actionlint v1.7.12 reported zero issues.**

### 2. Permissions — all PASS

| Workflow | Declared permissions | Assessment |
|---|---|---|
| `snake.yml` | `contents: write` | Correct — required to push to the `output` branch. |
| `svg-validate.yml` | `contents: read` | Correct — read-only job. |
| `markdown-lint.yml` | `contents: read` | Correct — read-only job. |
| `link-check.yml` | `contents: read`, `issues: write` | Correct — `issues: write` is required by the `peter-evans/create-issue-from-file` step and is present. |
| `svg-optimize.yml` | `contents: read` | Correct — dry-run only, writes to `/tmp`. |
| `health-check.yml` | `contents: read` | Correct — read-only job. |

No workflow relies on default token permissions; because permissions are explicit at workflow level, the repository "Workflow permissions" setting (read-only vs read/write default) does **not** need to be changed for `snake.yml` to work.

### 3. Action versions — inventory (latest release as of 2026-07-13 in parentheses)

| Workflow | Action reference | Latest | Status |
|---|---|---|---|
| snake.yml | `Platane/snk@v3` | v3.5.0 | **Current major** ✔ |
| snake.yml | `crazy-max/ghaction-github-pages@v4` | v5.0.0 | WARN — one major behind (W2) |
| svg-validate.yml, markdown-lint.yml, link-check.yml, svg-optimize.yml, health-check.yml | `actions/checkout@v4` | v7.0.0 | WARN — works, Node 20 runtime (W1) |
| svg-validate.yml, health-check.yml | `actions/setup-python@v5` | v6.3.0 | WARN — works, Node 20 runtime (W1) |
| svg-optimize.yml | `actions/setup-node@v4` | v6.4.0 | WARN — works, Node 20 runtime (W1) |
| markdown-lint.yml | `DavidAnson/markdownlint-cli2-action@v18` | v24.0.0 | WARN — six majors behind (W3) |
| link-check.yml | `lycheeverse/lychee-action@v2` | v2.9.0 | **Current major** ✔ |
| link-check.yml | `peter-evans/create-issue-from-file@v5` | v6.0.0 | WARN — one major behind (W4) |

- **No deprecated/shut-down actions**: no `actions/checkout@v3` or older, no `actions/setup-node@v3` or older, no `actions/upload-artifact`/`download-artifact` v3 usage at all.
- **No unpinned refs**: no `@main` / `@master` references anywhere.
- `Platane/snk@v3` is the current major and receives updates on the v3 tag — good.

### 4. Artifact / output paths — PASS (with two WARNs)

- `snake.yml` generates `dist/github-snake.svg`, `dist/github-snake-dark.svg`, `dist/github-snake.gif` and publishes `dist/` to the **root of the `output` branch**.
- `README.md` (lines 123–125) references:
  - `https://raw.githubusercontent.com/aadityapa/aadityapa/output/github-snake-dark.svg` ✔ exact match
  - `https://raw.githubusercontent.com/aadityapa/aadityapa/output/github-snake.svg` ✔ exact match
  - The `.gif` output is generated but not referenced anywhere — harmless (informational I1).
- `svg-optimize.yml` references `assets/dark.svg`, `assets/light.svg`, `favicon.svg`, `.svgo.config.mjs` — all exist. Output goes to `/tmp/` (dry run), consistent with `contents: read`.
- `link-check.yml` reads `./lychee/out.md` — this is the default report path written by `lycheeverse/lychee-action`. Correct.
- `health-check.yml`'s 18 required files all exist in the repo; the README-reference scan finds `./LICENSE`, `./assets/dark.svg`, `./docs/animation-report.md`, `./docs/design-system.md`, `./favicon.svg` — all exist. **Simulated locally: PASS.**
- `svg-validate.yml`'s embedded script was **simulated locally against the real SVGs: PASS** (no banned constructs, no external refs beyond the exempted SVG namespace, no duplicate ids, all under 1 MB).
- Path-scope mismatch in `svg-validate.yml` (W7) and hardcoded file list in `svg-optimize.yml` (W8) — see warnings.

### 5. Triggers — all crons valid; several minor WARNs

| Workflow | Triggers | Cron check | workflow_dispatch |
|---|---|---|---|
| snake.yml | schedule `0 */12 * * *`, push→main, dispatch | Valid, every 12 h — reasonable | ✔ present |
| svg-validate.yml | push (paths), PR (paths) | n/a | ✘ absent (W11) |
| markdown-lint.yml | push (paths), PR (paths) | n/a | ✘ absent (W11) |
| link-check.yml | schedule `0 6 * * 1` (Mon 06:00 UTC), push→main (md paths), dispatch | Valid, weekly — reasonable | ✔ present |
| svg-optimize.yml | push (paths), PR (paths), dispatch | n/a | ✔ present |
| health-check.yml | schedule `0 5 * * 0` (Sun 05:00 UTC), dispatch | Valid, weekly — reasonable | ✔ present |

- All path filters use valid GitHub glob syntax (`assets/**.svg`, `**.md`) and genuinely match the files they validate (`assets/dark.svg`, `assets/light.svg`, `favicon.svg`, `README.md`, `docs/*.md`).
- `snake.yml` has `workflow_dispatch` as required for manual first-run bootstrap. ✔

### 6. GitHub compatibility — PASS

- Runner label `ubuntu-latest` used everywhere — valid.
- All `run:` steps are bash/Linux-idiomatic: heredocs (`python - <<'EOF'`), `$(...)` substitution, `stat -c%s` (GNU coreutils — correct for Ubuntu, would only break on macOS), `npx`, `for f in ...; do ... done`. **No PowerShell or Windows-isms.**
- Tools installed before use: SVGO via `npm install --no-save svgo@3` after `setup-node`; Python via `setup-python` before `python` heredocs; `python3` in `svg-optimize.yml` uses the runner's preinstalled interpreter (present on ubuntu-latest); lychee, markdownlint, snk are self-contained actions.
- Secrets: only `secrets.GITHUB_TOKEN` is referenced (`snake.yml` line 39) — available by default in every run. **No references to non-existent secrets.**
- `markdownlint-cli2` was run locally with the repo config: 0 errors, so `markdown-lint.yml` will pass on first push.

---

## All warnings (individually listed)

No failures were found. 13 warnings + 2 informational notes, in descending severity:

### W1 — Node 20-based action majors will emit deprecation warnings

- **Files/steps:**
  - `svg-validate.yml` lines 23, 26 (`actions/checkout@v4`, `actions/setup-python@v5`)
  - `markdown-lint.yml` line 22 (`actions/checkout@v4`)
  - `link-check.yml` line 24 (`actions/checkout@v4`)
  - `svg-optimize.yml` lines 25, 28 (`actions/checkout@v4`, `actions/setup-node@v4`)
  - `health-check.yml` lines 18, 21 (`actions/checkout@v4`, `actions/setup-python@v5`)
- **Severity:** Medium (will run today, but generates runner deprecation annotations; GitHub is migrating actions to the Node 24 runtime)
- **Fix:** Bump to the current Node 24-based majors: `actions/checkout@v7` (v5+ acceptable), `actions/setup-python@v6`, `actions/setup-node@v6`. No input changes required for the usage in these workflows.

### W2 — `crazy-max/ghaction-github-pages@v4` is one major behind

- **File/step:** `snake.yml` line 34, step "Publish to output branch"
- **Severity:** Medium
- **Fix:** Bump to `crazy-max/ghaction-github-pages@v5` (v5.0.0). Inputs `target_branch`/`build_dir` are unchanged. Alternatively, `Platane/snk/svg-only@v3` + `peaceiris/actions-gh-pages` is a common equivalent stack, but the current action works.

### W3 — `DavidAnson/markdownlint-cli2-action@v18` is six majors behind

- **File/step:** `markdown-lint.yml` line 25, step "Lint markdown files"
- **Severity:** Medium (still functional; misses newer markdownlint rules and fixes)
- **Fix:** Bump to `@v24` (v24.0.0). The `globs` input is unchanged. Re-run lint after bumping since newer markdownlint versions add rules.

### W4 — `peter-evans/create-issue-from-file@v5` is one major behind

- **File/step:** `link-check.yml` line 45, step "Open issue on broken links (scheduled runs only)"
- **Severity:** Low
- **Fix:** Bump to `@v6` (v6.0.0). Inputs `title`/`content-filepath`/`labels` are unchanged.

### W5 — First-push race: README snake URLs 404 until the `output` branch exists

- **Files:** `snake.yml` (creates the branch), `README.md` lines 123–125, `link-check.yml` (scans those URLs)
- **Severity:** Medium (expected transient state, but has visible effects)
- **Detail:** `raw.githubusercontent.com/aadityapa/aadityapa/output/github-snake*.svg` will 404 until the first successful `snake.yml` run pushes the `output` branch (`crazy-max/ghaction-github-pages` **does create the branch automatically** on first run, so no manual branch creation is needed). Because `snake.yml` triggers on push to `main`, the gap is typically only a few minutes. During the gap: the README snake section renders as a broken image, and a `link-check` run would report the two raw URLs as broken — on push runs this is harmless (`fail: false`), and an issue is only filed on *scheduled* runs, so a false-positive issue is unlikely but possible if the snake job fails on its first attempts.
- **Fix (recommended, not applied):** After the first push, manually trigger `snake.yml` via workflow_dispatch and confirm the `output` branch appears before relying on the README render. Optionally add `--exclude "raw.githubusercontent.com/aadityapa/aadityapa/output"` to lychee's args until the branch exists, or leave as-is since the check is self-healing.

### W6 — Scheduled workflows auto-disable after 60 days of repository inactivity

- **Files:** `snake.yml` line 6, `link-check.yml` line 6, `health-check.yml` line 6
- **Severity:** Low (GitHub platform behavior, not a config error)
- **Detail:** GitHub disables `schedule` triggers in repos with no commit activity for 60 days. On a profile repo with a 12-hourly snake this matters: if you stop committing for 2 months, the snake stops updating.
- **Fix:** No config change possible; be aware you may need to re-enable workflows from the Actions tab after long inactivity, or keep occasional commit activity.

### W7 — `svg-validate.yml`: trigger paths broader than the validated set

- **File/step:** `svg-validate.yml` — trigger paths lines 5–8 (`assets/**.svg` matches nested SVGs) vs. script line 37 (`glob.glob("assets/*.svg")` matches only the top level of `assets/`)
- **Severity:** Low (currently no nested SVGs exist, so no practical gap today)
- **Fix:** In the embedded script use `glob.glob("assets/**/*.svg", recursive=True) + glob.glob("assets/*.svg")` (or `pathlib.Path("assets").rglob("*.svg")`) so any future nested SVG that triggers the workflow is actually validated.

### W8 — `svg-optimize.yml`: hardcoded SVG file list

- **File/step:** `svg-optimize.yml` line 37, step "Dry-run SVGO with SMIL-safe config" (`for f in assets/dark.svg assets/light.svg favicon.svg`), and the matching hardcoded tuple in step "Verify SMIL animations survived optimization" (line 49)
- **Severity:** Low
- **Detail:** The trigger fires for *any* `assets/**.svg`, but only the three hardcoded files are checked; a newly added SVG would trigger the workflow yet never be optimized/verified. Also, the SMIL-verification expectations (`animateMotion` required except favicon) are baked to these exact files.
- **Fix:** Derive the file list dynamically (`for f in assets/*.svg favicon.svg`) and make the SMIL assertions data-driven, or accept the tight coupling since the repo's SVG set is intentionally fixed.

### W9 — `health-check.yml`: `lstrip("./")` is a latent path bug

- **File/step:** `health-check.yml` line 48 inside step "Verify required files and README references": `p = r.lstrip("./")`
- **Severity:** Low (no current README reference hits it — verified by local simulation)
- **Detail:** `str.lstrip("./")` strips *any* leading `.` and `/` characters, not the literal prefix `./`. A README reference like `./.gitignore` would become `gitignore` and be falsely reported missing (or worse, a wrong file found).
- **Fix:** Use `p = r.removeprefix("./")` (Python ≥3.9; the workflow pins 3.12, so it's available).

### W10 — Duplicate runs for same-repo pull requests

- **Files:** `svg-validate.yml`, `markdown-lint.yml`, `svg-optimize.yml` — each has `push` with **no branch filter** plus `pull_request` on the same paths
- **Severity:** Low (wasted minutes only; free for public repos)
- **Detail:** Pushing to a PR branch in the same repository fires both the `push` and `pull_request` events, running each workflow twice per commit.
- **Fix:** Add `branches: [main]` to the `push` trigger of these three workflows (PRs remain covered by `pull_request`), or add a `concurrency` group. For a single-maintainer profile repo pushed directly to `main`, this is mostly theoretical.

### W11 — No `workflow_dispatch` on `svg-validate.yml` and `markdown-lint.yml`

- **Files:** `svg-validate.yml` lines 3–12, `markdown-lint.yml` lines 3–11
- **Severity:** Low
- **Detail:** These two workflows can only be triggered by matching path changes; you cannot re-run them manually from the Actions tab (only re-run past runs). The other four workflows all have `workflow_dispatch`.
- **Fix:** Add `workflow_dispatch:` to the `on:` block of both.

### W12 — `pull_request` path filters narrower than `push` path filters

- **Files/lines:**
  - `svg-validate.yml` lines 10–12: PR paths omit `.github/workflows/svg-validate.yml`
  - `markdown-lint.yml` lines 10–11: PR paths omit `.markdownlint.json` and the workflow file
  - `svg-optimize.yml` lines 11–13: PR paths omit `.svgo.config.mjs` and the workflow file
- **Severity:** Low
- **Detail:** A PR that only changes the lint config or the workflow itself would not run the corresponding check, while a direct push would. Slight CI-coverage inconsistency.
- **Fix:** Mirror the `push` path lists in the `pull_request` blocks.

### W13 — `snake.yml` push trigger has no path filter

- **File/lines:** `snake.yml` lines 8–10
- **Severity:** Low (informational-adjacent)
- **Detail:** Every push to `main` — including README typo fixes — regenerates and force-publishes the snake, in addition to the 12-hour schedule. The `concurrency` group (lines 15–17) correctly prevents overlapping runs, so this only costs runner minutes.
- **Fix:** Either accept it (it guarantees the `output` branch exists immediately after first push — which mitigates W5), or restrict with a `paths` filter / drop the push trigger once the branch is bootstrapped.

### Informational (no action needed)

- **I1 — Unreferenced snake GIF:** `snake.yml` line 31 generates `dist/github-snake.gif` (with valid snk query-string color syntax), but nothing references it. Harmless; remove the line or use the GIF somewhere if you like.
- **I2 — SVGO pinned to v3:** `svg-optimize.yml` line 33 installs `svgo@3` while SVGO v4 exists. This appears intentional (the `.svgo.config.mjs` SMIL-safe config targets v3's API) and the pin is a *good* practice; just note it when eventually upgrading the config.

---

## Cross-workflow review

- **No conflicting writers:** only `snake.yml` writes anywhere (the `output` branch); all other workflows are read-only. No two workflows push to the same ref, and `snake.yml` has its own `concurrency` group.
- **First-push behavior:** a single initial push to `main` will trigger `snake.yml`, `markdown-lint.yml`, `link-check.yml`, `svg-validate.yml`, and `svg-optimize.yml` simultaneously (5 concurrent jobs). All are independent and expected to pass — the embedded validation scripts and markdownlint were simulated locally against the current tree and all pass. `health-check.yml` runs only on schedule/dispatch and its checks also pass locally. The only transient issue is W5 (snake URLs 404 for the few minutes before the first `snake.yml` run completes).
- **Repo settings required:** none strictly. Explicit workflow-level `permissions:` blocks mean the default "Workflow permissions" setting doesn't matter; `GITHUB_TOKEN` with `contents: write` is sufficient for the `output` branch push. Only an enterprise/org policy restricting token permissions could block it (not applicable to a personal profile repo). Actions must simply be enabled for the repository (default).
- **No duplicate/conflicting triggers between different workflows:** `markdown-lint` and `link-check` both react to `**.md` pushes, and `svg-validate`/`svg-optimize` both react to SVG pushes — these are complementary checks, not conflicts.

---

*Report generated 2026-07-13. Validation only — no workflow files were modified.*

---

## Addendum — production audit follow-up (2026-07-13, same day)

The production-readiness audit applied the recommended fixes after this report was written. Current workflow state (verify against the files themselves):

- **W1/W2/W3/W4 resolved:** actions bumped to `actions/checkout@v7`, `actions/setup-python@v6`, `actions/setup-node@v6`, `DavidAnson/markdownlint-cli2-action@v24`, `peter-evans/create-issue-from-file@v6`, `crazy-max/ghaction-github-pages@v5`. markdownlint re-run with the v24-era engine (markdownlint-cli2 v0.23 / markdownlint v0.41): 0 errors.
- **W7 resolved:** `svg-validate.yml` now globs `assets/**/*.svg` recursively.
- **W8 partially resolved:** the SVGO dry-run loop is now `for f in assets/*.svg favicon.svg`; the SMIL-survival assertions intentionally stay pinned to the three shipped files.
- **W9 resolved:** `health-check.yml` uses `removeprefix("./")`.
- **W10/W11/W12 resolved:** `push` triggers restricted to `main`, `workflow_dispatch` added to `svg-validate.yml` and `markdown-lint.yml`, and `pull_request` path filters mirror `push` filters.
- **I1 resolved:** the unreferenced snake GIF output was removed from `snake.yml`.
- **W5, W6, W13, I2:** accepted as-is (documented platform behavior / intentional choices).
