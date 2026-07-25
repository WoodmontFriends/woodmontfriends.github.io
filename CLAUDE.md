# Friends of Woodmont Park — Claude Code Context

Website and project space for **Friends of Woodmont Park (FWP)**, a Virginia nonstock corporation (incorporated April 22, 2026) serving the Woodmont neighborhood and surrounding area of North Chesterfield, VA. Currently a single-page static "coming soon" site on GitHub Pages.

- **Live**: https://woodmontfriends.github.io · **GitHub org**: https://github.com/WoodmontFriends
- **501(c)(3) status**: applied / pending — do NOT describe donations as tax-deductible until confirmed.

## Mission (verbatim from the Articles of Incorporation)

> To preserve, protect, and promote the quality of life for all residents in the Woodmont neighborhood and surrounding area of North Chesterfield, Virginia, through sustainable improvements and collective community effort.

## Who you're working with

The user (Gabe) is a founding director of FWP and **President of the Woodmont Civic Association**. FWP's board has five founding directors: Max (President), Gabe, Andrew, Peter, Christina. Weekly virtual stand-ups: Wednesdays 3:30 PM.

Apply the same lens as WCA work — welcoming, professional, optimistic; "how does this help our neighbors?"; don't over-engineer (volunteer-run org); spelling/grammar must be perfect on anything public.

**Public-repo rule**: everything in this repo is public. Board-internal material (legal docs, finance, meeting notes, personal details) lives in the Google Drive shared drive, never here. Board members are referred to by first name only.

## Sister organizations

- **Woodmont Civic Association (WCA)** — woodmontbonair.com · repos: `~/repos/woodmont-civic.github.io` (Nuxt 3 static site), `~/repos/wca-crm` (Next.js CRM)
- **Woodmont Recreation Association (WRA)** — woodmont4fun.org · pool/rec club; FWP's first project is on WRA grounds (contact: Eric)
- FWP is legally independent of both; they're community partners, not parent orgs.

## First project: tennis court restoration

Restore the old tennis courts behind the WRA pool into a **multi-use sport court** (pickleball, basketball half-courts, flexible event space) — final design driven by community input. Near-term: cleanup days, drainage fixes, boardwalk repair. Funding ideas in play: CSX community grant (~$5k rolling), Richmond ToolBank tool rental, in-kind donations of equipment/labor.

## What the org needs (weave into public copy where relevant)

- Volunteers (cleanup days, trail work, events)
- Grant writers / fundraising help
- Donations (post-501(c)(3)) and in-kind contributions (tools, materials, equipment, expertise)
- Community input on what the space should become

## Stack & deploy

Plain HTML/CSS, no build step. `index.html` is the whole site. Merging to `main` deploys via GitHub Pages (org pages repo — no workflow needed).

Roadmap: single-page static site → SPA with an admin backend (stack TBD; Nuxt 3 is the house pattern from WCA). When that work starts, this file gets updated.

## Google Drive (private)

`FWP Board Internal` shared drive, mounted locally at:
`/Users/gabeduke/Library/CloudStorage/GoogleDrive-gabeduke@gmail.com/Shared drives/FWP Board Internal`

- `01_Governance & Legal/` — Articles of Incorporation, Bylaws, director consents, Perkins Law docs
- `02_Finance & Accounting/` — receipts
- `03_Meeting Notes/` — meeting notes (gdoc) and walkabout PDFs

Reading from this drive is fine; never copy its contents into this repo.
