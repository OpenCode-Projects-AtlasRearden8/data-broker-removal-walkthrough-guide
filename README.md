# Data Broker Removal Walkthrough Guide

**Find the sites selling your personal info, remove yourself, and stay off —
free, manual, and legal. Plain-English guides plus a private, static,
one-page checklist you can keep and reuse.**

By **Asdale Dynamics, LLC** — Dylan Asdale's brand for beginner-friendly AI,
privacy, and life-admin guides. Education only; not legal advice.

## The need it fills

You search your own name, and people-search sites are selling your home address,
relatives, and phone number. Paid services remove some of it for a subscription.
This guide teaches the free, repeatable manual process — the same thing the paid
services (mostly) do — in one focused afternoon, then about 60 minutes a year.

## What's inside

```
docs/            step-by-step guides (start at docs/00-index.md)
  01  what data brokers are
  02  which states & laws give you removal rights
  03  the walkthrough (find → request → confirm → log)
  04  free request templates (email + postal, incl. state-law wording)
  05  opt-out pages & lanes for major brokers
  06  renewal calendar + ready-to-import .ics reminders
  07  keeping your data off going forward
site/            static HTML checklist (no build, no dependencies)
```

The checklist page (`site/index.html`) tracks your progress in your own browser's
localStorage, works offline, prints cleanly, and never sends your data anywhere.

## How to use it

**Reading the guides:** open `docs/00-index.md` and follow the links. Nothing
to install.

**Running the checklist site:** it's static HTML — just open it, no build step:

```bash
# option A: open the file directly
open site/index.html          # macOS
xdg-open site/index.html      # Linux
# (or double-click it in a file manager)

# option B: serve it (nicer for some browsers)
python3 -m http.server 8000 --directory site
# then visit http://localhost:8000
```

**Verification** (what we ran before shipping — see `STATUS.md` for results):

```bash
node --check site/app.js                       # JS syntax
python3 -m http.server 8000 --directory site & # then curl the page; expect 200
```

## How to use this guide responsibly

- Education only — not legal advice; verify current law before relying on it.
- **No scraping, no automation, no bulk requests.** Visit each broker's own
  opt-out page manually, like any normal visitor. Opt-out paths change often —
  confirm you're on the company's official domain before submitting anything.
- Only submit **your own** personal information. Never paste a full SSN, ID
  scan, or anyone else's details into any request.
- If a listing could put you in physical danger, prioritize the major
  people-search removals and Google's "Results about you" removal right away,
  and seek specialist safety help (docs/07).

## Related Asdale Dynamics projects

- **privacy-comfort-handbook** — the "why this matters and how to feel OK
  about it" handbook for home privacy in the AI era.
- **safe-share-redactor-cli** — a CLI for redacting text and files before
  sharing them.
- This repo is the *removal* walkthrough: hands-on, step-by-step, checklist-driven.

## Contributing

Fixes welcome — especially "this opt-out path moved" corrections. Keep the tone
friendly and beginner-first. No secrets, keys, or personal data in files, ever.

## License

MIT — see [LICENSE](LICENSE).
Copyright (c) 2026 Asdale Dynamics, LLC.
