# Friends of Woodmont Park

Website for **Friends of Woodmont Park**, a new community nonprofit serving the Woodmont neighborhood of North Chesterfield, Virginia.

🌳 **Live**: https://woodmontfriends.github.io

## About the organization

Friends of Woodmont Park is a Virginia nonstock corporation whose mission is to preserve, protect, and promote the quality of life for all residents in the Woodmont neighborhood and surrounding area through sustainable improvements and collective community effort. 501(c)(3) tax-exempt status is pending.

Our first project is restoring the old tennis courts behind the Woodmont Recreation Association pool into a multi-use community sport court.

We work alongside — and are grateful for — our community partners:

- [Woodmont Civic Association](https://woodmontbonair.com)
- [Woodmont Recreation Association](https://woodmont4fun.org)

## Development

Nuxt 3 + [Content Wind](https://content-wind.nuxt.space) (@nuxt/content v2) — content lives in Markdown under `content/`.

```bash
yarn install    # deps
yarn dev        # local dev server
yarn generate   # static build → ./dist
```

Pushing to `main` deploys to GitHub Pages via Actions; PRs get a build check (`.github/workflows/nuxtjs.yml`).

### Editing content

- Home page: `content/1.index.md`
- MDC components available in Markdown: `::hero`, `::card-grid` + `::info-card{title="..."}` (see `components/content/`)
