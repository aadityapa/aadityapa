# README Validation Report

**Repository:** `aadityapa/aadityapa` (GitHub profile README)
**Validated:** 2026-07-13
**Method:** Static parse of `README.md` (all markdown images/links, `<img>`, `<picture>`/`<source>`, `<a href>`), filesystem checks for relative paths, live HTTP GET of every external URL (Python `requests`, browser User-Agent, retries for flaky services), `npx markdownlint-cli` with the repo's `.markdownlint.json`.

---

## 1. Summary Verdict

| # | Check | Verdict | Notes |
|---|-------|---------|-------|
| 1 | Local asset paths | ✅ PASS | All 6 relative paths exist on disk |
| 2 | Badges (shields.io + komarev) | ✅ PASS | 37/37 return `200` with `image/svg+xml` |
| 3 | GitHub Stats card | ⚠️ SERVICE DOWN | `503 DEPLOYMENT_PAUSED` — the public `github-readme-stats.vercel.app` instance is paused; not a README or account problem |
| 4 | Streak Stats + Top Languages | ⚠️ MIXED | Streak: `200` OK with real data. Top Languages (same paused github-readme-stats instance): `503` |
| 5 | Activity graph + trophies | ⚠️ MIXED | Activity graph: `200` OK. Trophies: `402 DEPLOYMENT_DISABLED` — public instance disabled |
| 6 | Snake animation | ✅ CONFIG PASS (⏳ 404 until push) | Filenames/branch match `snake.yml` exactly; URLs will resolve after first workflow run |
| 7 | External hyperlinks | ⚠️ 1 REAL 404 | `github.com/aadityapa/ritikainfotech` returns 404. LinkedIn `999` = bot protection, likely fine. Everything else `200` |
| 8 | markdownlint | ✅ PASS | 0 errors with repo config |

**Additional structural checks:**

| Check | Verdict |
|-------|---------|
| `<picture>` dark/light hero block | ✅ Correctly structured (dark + light `prefers-color-scheme` sources, `<img>` fallback with alt text) |
| GitHub user `aadityapa` exists | ✅ Yes — verified via `github.com/aadityapa` (200) and `api.github.com/users/aadityapa` (200) |

### GitHub account status

The account **exists and is active**: login `aadityapa`, display name "Aaditya Padiya", **16 public repos**, created 2021-05-24, last updated 2026-07-13. Streak-stats already renders real data (205 contributions counted, longest streak 9 days), so stats services that are up will render normally — the failures below are service-side outages, not "user not found" errors.

---

## 2. Full URL Inventory

55 unique URLs/paths extracted from `README.md` (markdown images, markdown links, `<img src>`, `<source srcset>`, `<a href>`).

### 2.1 Local assets (6) — all exist on disk ✅

| Path | Referenced from | Exists |
|------|-----------------|--------|
| `./assets/dark.svg` | `<picture>` hero (source + img fallback) | ✅ |
| `./assets/light.svg` | `<picture>` hero (source) | ✅ |
| `./favicon.svg` | Footer monogram `<img>` | ✅ |
| `./docs/design-system.md` | Footer `<a href>` | ✅ |
| `./docs/animation-report.md` | Footer `<a href>` | ✅ |
| `./LICENSE` | Footer `<a href>` | ✅ |

### 2.2 Badges (37) — all `200 OK`, `image/svg+xml` ✅

36 × `img.shields.io` badges (Portfolio, LinkedIn, Email, GitHub, AWS, EC2, S3, CloudWatch, Vercel, Render, Windows Server, Linux, Ubuntu, Active Directory, Intune, SonicWALL, VLAN/VPN/DNS/DHCP, Docker, GitHub Actions, CI/CD, PowerShell, Shell Scripting, VMware, Hyper-V, Python, Ollama, OpenAI API, Next.js, React, FastAPI, Streamlit, Solidity, and the four "Connect" badges) — every one returned **HTTP 200** with content-type `image/svg+xml;charset=utf-8`.

1 × `komarev.com/ghpvc/?username=aadityapa` (profile views counter) — **HTTP 200**, `image/svg+xml`.

### 2.3 Stats services (5)

| URL (service) | Status | Content-Type | Interpretation |
|---------------|--------|--------------|----------------|
| `github-readme-stats.vercel.app/api?username=aadityapa&…` (stats card) | **503** | text/plain | Body: `The deployment is currently unavailable — DEPLOYMENT_PAUSED`. The shared public Vercel instance is paused (a recurring, well-known issue with this project's free public deployment). Retried 3× over ~10 s, same result. **Not** a "user not found" error — the request never reached the app. |
| `github-readme-stats.vercel.app/api/top-langs/?username=aadityapa&…` (top languages) | **503** | text/plain | Same paused instance, same `DEPLOYMENT_PAUSED` body, 3 retries. |
| `streak-stats.demolab.com?user=aadityapa&…` | **200** | image/svg+xml | ✅ Renders real data: 205 contributions, longest streak 9. Confirms the account has contribution activity. |
| `github-readme-activity-graph.vercel.app/graph?username=aadityapa&…` | **200** | image/svg+xml | ✅ OK |
| `github-profile-trophy.vercel.app/?username=aadityapa&…` | **402** | text/plain | Body: `Payment required — DEPLOYMENT_DISABLED`. The public trophy deployment is disabled on Vercel's side, 3 retries. Consider self-hosting the trophy service or removing/replacing this embed if it doesn't recover. |

### 2.4 Snake animation (2) — config verified, 404 expected until push ⏳

| URL | Status now |
|-----|-----------|
| `raw.githubusercontent.com/aadityapa/aadityapa/output/github-snake-dark.svg` | 404 |
| `raw.githubusercontent.com/aadityapa/aadityapa/output/github-snake.svg` | 404 |

**Workflow cross-check (`.github/workflows/snake.yml`):** the workflow (Platane/snk@v3 with `github_user_name: ${{ github.repository_owner }}` = `aadityapa`) generates `dist/github-snake.svg` (light), `dist/github-snake-dark.svg` (dark), and `dist/github-snake.gif`, then publishes `dist/` to the **`output`** branch via `crazy-max/ghaction-github-pages@v4`. The README references `…/aadityapa/aadityapa/output/github-snake-dark.svg` and `…/output/github-snake.svg` — **branch and filenames match exactly**. The 404s are expected: the `aadityapa/aadityapa` repo has not been pushed yet, so the `output` branch does not exist. The workflow triggers on push to `main`, every 12 h, and manual dispatch, so the snake will appear after the first push + workflow run.

### 2.5 External hyperlinks (10)

| URL | Status | Interpretation |
|-----|--------|----------------|
| `https://aadityapadiya.vercel.app` (portfolio) | 200 | ✅ |
| `https://github.com/aadityapa` | 200 | ✅ user exists |
| `https://github.com/aadityapa/Self-Healing-Cloud-Platform` | 200 | ✅ |
| `https://github.com/aadityapa/ocr` | 200 | ✅ |
| `https://github.com/aadityapa/corporate-network-infrastructure` | 200 | ✅ |
| `https://github.com/aadityapa/ritikainfotech` | **404** | ❌ **Real broken link.** The repo `ritikainfotech` does not exist (or is private) under `aadityapa`, even though the account has 16 public repos. Fix: create/rename/publish the repo, or point the link elsewhere. |
| `https://ritikainfotech.in` (live site) | 200 | ✅ the live-site link next to it works |
| `https://ocr-chi-ivory.vercel.app` (TrustOCR live) | 200 | ✅ |
| `https://www.linkedin.com/in/aaditya-padiya-7b64372` | 999 | ⚠️ Blocked by LinkedIn bot protection (standard for automated requests) — likely fine in a real browser; verify manually once. |
| `mailto:aadityapadiya@gmail.com` | n/a | ✅ syntactically valid mailto |

Probes (not in README, run for verification): `https://api.github.com/users/aadityapa` → 200, JSON confirms user.

---

## 3. Items that cannot pass until after the repo is pushed

1. **Snake animation (both URLs, §2.4)** — requires the `aadityapa/aadityapa` repo to exist on GitHub and the `Contribution Snake` workflow to run once (it will, on first push to `main`). Configuration verified correct; no action needed.

That is the only push-dependent item. The stats/top-langs/trophy failures are **not** push-dependent — they are outages of the shared public service deployments and would fail for any username today. The komarev counter, streak stats, and activity graph already work.

## 4. markdownlint output

```text
$ npx markdownlint-cli --config .markdownlint.json README.md
(no output — 0 errors)
exit code: 0
```

Config used: `.markdownlint.json` (default rules with MD001, MD013, MD033, MD041, MD045, MD060 disabled; MD024 siblings-only).

## 5. `<picture>` dark/light hero block

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/light.svg">
  <img src="./assets/dark.svg" alt="…" width="100%">
</picture>
```

✅ Correct for GitHub: both `prefers-color-scheme` `<source>` elements come before the `<img>` fallback, both srcset targets exist on disk, and the fallback `<img>` has a descriptive `alt` and a valid `src`. This is exactly the pattern GitHub documents for theme-aware images. The snake `<picture>` block at the bottom follows the same correct structure.

---

## 6. Action items

| Priority | Item |
|----------|------|
| 🔴 Fix before/at push | `github.com/aadityapa/ritikainfotech` is 404 — create or publish the repo, or update the link |
| 🟡 Monitor | `github-readme-stats.vercel.app` (stats + top-langs cards) is 503 `DEPLOYMENT_PAUSED`; if it stays down, self-host the instance or switch cards |
| 🟡 Monitor | `github-profile-trophy.vercel.app` is 402 `DEPLOYMENT_DISABLED`; consider self-hosting or removing the trophy embed |
| 🟢 No action | Snake 404s resolve automatically after first push + workflow run |
| 🟢 No action | LinkedIn 999 is bot protection, not a broken link |

---

## 7. Addendum — production audit follow-up (2026-07-13, same day)

- The broken `github.com/aadityapa/ritikainfotech` link was **removed**: the Ritika Infotech row in README.md now links directly to the live site `https://ritikainfotech.in` (200 OK), and the stale `github` key was dropped from that project in `profile.json`.
- The paused/disabled third-party embeds (`github-readme-stats` 503, `github-profile-trophy` 402) were re-tested during the audit with retries — still service-side outages affecting all usernames. Decision: **keep the embeds**. They are correct by construction, the profile degrades gracefully (GitHub hides broken `<img>` embeds rather than showing error boxes), and both services have historically recovered. `link-check.yml` already excludes these hosts so CI won't flap.
- `www.linkedin.com` was added to the lychee exclude list in `link-check.yml` so the permanent 999 bot-block cannot file false-positive issues on scheduled runs.
