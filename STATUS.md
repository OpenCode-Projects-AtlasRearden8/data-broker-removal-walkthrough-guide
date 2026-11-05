# STATUS

**Project:** Data Broker Removal Walkthrough Guide
**Owner:** Asdale Dynamics, LLC (Dylan Asdale) — Indiana
**Type:** education-only guide + private static checklist site
**Status:** complete and verified, checked in to local git (no remote, never pushed)

## What was built

### docs/ — eight markdown guides (start at `docs/00-index.md`)

- `00-index.md` — overview + table of contents + honest expectations
- `01-what-are-data-brokers.md` — who brokers are, where the data comes from
- `02-state-removal-rights.md` — state privacy-law deletion rights (incl. Indiana's
  Jan-2026 law), federal rights (FCRA prescreen opt-out etc.), CA/VT broker registries
- `03-walkthrough.md` — the core step-by-step process (find → request → confirm →
  log → re-check), with a "removal kit" checklist
- `04-request-templates.md` — 6 free copy-paste templates: generic, state-law,
  firm follow-up, postal letter, polite nudge, AG/FTC escalation
- `05-opt-out-pages.md` — opt-out lanes for ~15 major people-search sites,
  marketing-data firms, LexisNexis/CLEAR, Google/Bing removal tools
- `06-renewals-calendar.md` — the 1/3/6/12-month renewal schedule + a working
  `.ics` snippet to import reminders
- `07-stay-off-going-forward.md` — forward hygiene: credit freezes, aliases,
  burner address, LLC/registered-agent separation, quarterly monitoring,
  escalation ladder incl. DV/high-risk priorities

### site/ — static HTML checklist (no build step, offline-first)

- `index.html` — 42-item tickable checklist in 6 sections + ICS copy block
- `app.js` — localStorage progress save, progress bar, live filter, print,
  reset, ICS clipboard copy (with execCommand fallback)
- `style.css` — warm, readable styling, mobile-responsive, print stylesheet

### Root files

- `README.md` — how to run/verify, related Asdale Dynamics projects
  (distinct from `safe-share-redactor-cli` and `privacy-comfort-handbook`),
  safety rules (no scraping, own data only)
- `LICENSE` — MIT, exact line: `Copyright (c) 2026 Asdale Dynamics, LLC`
- `scripts/verify.py` — offline verification suite (33 checks)

## How to run / use

- **Guides:** open `docs/00-index.md`. Nothing to install.
- **Checklist site:** open `site/index.html` directly, or serve it:
  `python3 -m http.server 8000 --directory site` → http://localhost:8000
- **Verify everything:** `python3 scripts/verify.py`

## Verification results (all passing)

```
[1] docs present + all internal cross-references resolve      ✓ (15/15)
[2] site/index.html: tags balanced, assets local, no network   ✓ (4/4)
[3] node --check site/app.js                                   ✓
[4] site/style.css braces balanced, anchors present            ✓ (2/2)
[5] LICENSE exact copyright line; README credits LLC           ✓ (3/3)
[6] secrets/keys pattern scan across repo                      ✓
[7] template/personal-data hygiene; no-scraping policy shown   ✓ (4/4)
```

- `node --check site/app.js` — clean
- Live-serve smoke test: `python3 -m http.server 8712 --directory site` +
  curl → index (200, 10,331 bytes), app.js (200), style.css (200)

## Design decisions

- **No build tooling.** Plain HTML/CSS/JS on purpose: never breaks, works
  offline, zero telemetry, easy to audit in 5 minutes.
- **localStorage only.** Progress never leaves the browser; no cookies,
  analytics, or external assets (verified by check #2).
- **Education-only guardrails built in:** no-scraping policy stated in README,
  docs, verification script, and the site itself; templates warn against
  submitting anyone's data but your own; no fake personal names in templates.
- **Hedged factual claims.** Broker opt-out paths and state-law lists are
  marked "verify current"; the verifier cross-checks every internal reference.

## Known gaps / honest limitations

1. **Broker opt-out URLs change often.** The table in docs/05 is a starting
   map, deliberately hedged; real maintenance here is periodic link-checking
   by hand (we don't auto-scrape, by policy).
2. **State-law list is a snapshot** ("as of late 2026"). New state laws pass
   yearly; the doc tells readers how to verify (IAPP tracker, state AG).
3. **The `.ics` sample dates are placeholders** — the docs and site tell the
   user to edit DTSTART before importing.
4. **No automated browser test** of the checklist (no headless browser in this
   environment). Verified via syntax check, tag balance, and HTTP smoke test;
   behavioral logic is small and reviewed by hand.
5. **The checklist count (42) is hardcoded nowhere** — it's computed from the
   DOM, so adding items just works (verifier checks the mechanism, not the
   number).
6. **No screenshots** — intentional, to keep the repo free of any example
   person's data.
