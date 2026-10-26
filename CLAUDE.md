# Friends of Woodmont Park — Claude Code Context

Website and project space for **Friends of Woodmont Park (FWP)**, a Virginia nonstock corporation (incorporated April 22, 2026) serving the Woodmont neighborhood and surrounding area of North Chesterfield, VA. Markdown-driven static site (Nuxt 3) deployed to GitHub Pages via Actions.

- **Live**: https://woodmontfriends.org (also woodmontfriends.github.io) · **GitHub org**: https://github.com/WoodmontFriends
- **501(c)(3) status**: applied / pending — do NOT describe donations as tax-deductible until confirmed.

## Mission (verbatim from the Articles of Incorporation)

> To preserve, protect, and promote the quality of life for all residents in the Woodmont neighborhood and surrounding area of North Chesterfield, Virginia, through sustainable improvements and collective community effort.

## Who you're working with

The user (Gabe) is a founding director of FWP and **President of the Woodmont Civic Association**. FWP's board has five founding directors: Max (President), Gabe (Treasurer), Christina (Secretary), Andrew and Peter (at-large). Weekly virtual meetings: Fridays 4 PM (Google Meet).

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

Nuxt 3 + Content Wind (@nuxt/content v2, Markdown + MDC) + TailwindCSS + Pinceau (primary: emerald) · Yarn. Same stack family as the WCA site (`~/repos/woodmont-civic.github.io`) but intentionally leaner — no PWA/SEO modules yet.

**Analytics**: Google Analytics 4 via `nuxt-gtag` (same as WCA). The measurement ID is `gaMeasurementId` at the top of `nuxt.config.ts`; the tag is off while it's empty. GA4 enhanced measurement records page views and outbound clicks (sign-up form) with no extra code.

```bash
yarn install    # deps
yarn dev        # local dev server — start with run_in_background: true
yarn generate   # static build → ./dist
```

`.github/workflows/nuxtjs.yml` (mirrored from WCA): PRs against `main` get a build check; pushes to `main` deploy to GitHub Pages via Actions (Pages source must be set to "GitHub Actions").

**Domain**: `woodmontfriends.org` was bought through Google Workspace and is registered with Squarespace Domains, which also hosts DNS. The apex has GitHub Pages A records and `www` is a CNAME to `woodmontfriends.github.io`. The custom domain is set in the repo's Pages settings (no `CNAME` file, since the site deploys via Actions). Keep the Google Workspace MX and SPF records intact. The Squarespace account was created under `treasurer@woodmontfriends.org`, which was later renamed to `admin@`.

## Editing content

- Home page: `content/1.index.md` — frontmatter `navigation.title` / `layout` / `title` / `description` (WCA conventions). Each band of the page is an MDC component, so copy edits stay in Markdown:
  - `::park-hero{primary-label primary-href secondary-label secondary-href}` — dark hero with the name lockup; body is the tagline. An href of `signup` resolves to `signupUrl` in `app.config.ts`.
  - `::page-section{id title tone="paper|fern"}` — a titled section; optional `#aside` slot for a right-hand column (used for `::mission-quote`).
  - `::event-list` > `::event-item{month day weekday title}` — date-block events.
  - `::trail` > `::trail-stop{title}` — the phased plan, drawn as a trail with blaze markers. Only for content that really is a sequence.
  - `::help-list` > `::help-item{title}` — two-column list of ways to help.
  - `::contact-band{title}` — dark sign-up call-to-action, plus the email address with a Copy button (`components/EmailAddress.vue`; mailto alone does nothing on computers without a mail app) and the community calendar subscribe links.
  - `::calendar-callout{title}` — dark "add our calendar" card with Google and Apple/Outlook subscribe buttons for the public FWP Community Events calendar (`communityCalendarId` in `app.config.ts`, links built in `composables/useCommunityCalendar.ts`); body is optional copy. Used on the home page and `/projects`.
- Sign-ups go to a Google Form (`signupUrl` in `app.config.ts`) stored in the FWP Board Internal shared drive: name, email, volunteer interests, and a free-text note.
- Site shell: `components/AppLayout.vue` (header + footer) and `layouts/default.vue` override the Content Wind theme's blog chrome.
- Design: tokens and base styles in `assets/css/park.css`. Hemlock green `#1f3a2e`, blaze yellow `#f2c230` (the only accent: logo mark, main buttons, trail markers), fern tint `#eef3ec`. Zilla Slab headings and Public Sans body text, loaded from Google Fonts in `nuxt.config.ts`. Light mode only.
- Preview: `yarn generate`, then serve `dist/` (e.g. `python3 -m http.server` inside it). `yarn dev` has shown Nuxt's welcome page instead of the site.

## Feature flags

Flags live under `features` in `app.config.ts`. Wrap flagged page content in `::feature-flag{name="..."}` (default slot when on, `#off` slot otherwise); off pages get `noindex`. Preview a flag that's off with `?flag=<name>` (remembered in that browser; `?flag=off` clears it). Don't use `?preview=`, since Nuxt Content claims it for its own preview mode. Unlinked flagged pages need adding to `nitro.prerender.routes` in `nuxt.config.ts`.

## Nature map (`/nature`, flag `natureMap`)

`components/content/NatureMap.vue`: Leaflet map of iNaturalist observations, fetched in the browser from the public API (no backend). Settings under `nature` in `app.config.ts`: `projectSlug` (empty → search the box around the mapped areas and keep only sightings inside them) and `protectedGenera` (edible species shown only as ~150 m areas). The areas (park, Woodmont neighborhood, community centers & watershed) are outlines traced in Google My Maps, stored in `data/nature-areas.ts` as [lng, lat] rings; they also drive the "All areas" filter. Observations iNaturalist obscures or marks private are left off the map and counted in a note. Basemaps: OpenStreetMap tiles and Esri World Imagery (keep their attributions).

## Projects page (`/projects`)

`components/content/FwpProjects.vue` (`::fwp-projects`) fetches `publicBoardUrl` in `app.config.ts` (`https://admin.woodmontfriends.org/api/public/board`) in the browser, so board changes show without a rebuild. The admin app (private repo `fwp-admin`) is the single source of truth: a card appears here only when it has the `public` label, and only its title, column (Planned / In progress / Recently done), target month and topic chips leave the app. Finished cards older than 60 days come back as `archive` and show in a collapsed list. `components/content/FwpEvents.vue` (`::fwp-events`) lists upcoming events from `publicEventsUrl` (the public "FWP Community Events" Google Calendar, fed by public cards with a due date) with subscribe links; it renders nothing while the admin app reports the calendar off. The header, footer, home page and board page all link here; the old GitHub Projects board is retired.

## Google Drive (private)

`FWP Board Internal` shared drive, mounted locally at:
`/Users/gabeduke/Library/CloudStorage/GoogleDrive-gabeduke@gmail.com/Shared drives/FWP Board Internal`

- `01_Governance & Legal/` — Articles of Incorporation, Bylaws, director consents, Perkins Law docs
- `02_Finance & Accounting/` — receipts
- `03_Meeting Notes/` — meeting notes (gdoc) and walkabout PDFs

Reading from this drive is fine; never copy its contents into this repo.
