# Friends of Woodmont Park signs

About 80% finished, and expected to change. **Nothing here has been cut on a real machine.** Nothing has been approved by the FWP board or WRA, and nothing has been ordered.

- **Board proposal:** https://claude.ai/artifact/K5x7dNznPfro2jq9FUghqJ
- **Concept mock it started from:** https://claude.ai/artifact/APxQpHuQ2FknQihgLGzTaC
- **Shopping and cutter day:** [materials.md](materials.md), [materials.csv](materials.csv)

| Path | What it is |
|---|---|
| `designs/` | Real-size SVG and preview PNG per sign, plus `all-signs-proof.png`. Proofs only. |
| `cut-untested/<sign>__<color>.svg` | One outlined file per vinyl color per sign, at full size |
| `cut-untested/workday-yard__date-line__pale.svg` | The swappable date line (the date is an example) |
| `cut-untested/test-cut-first.svg` | A 2 in scale square plus the thinnest lettering. Cut this first. |
| `cut-untested/gang-12in/`, `gang-24in/` | Every piece in the run, nested by color for each cut width |
| `piece-placement.csv` | Size and position of every piece, for layout |
| `cut-measurements.json` | Vinyl area and roll length measured from the geometry |
| `build_signs.py` | Rebuilds all of the above. Setup notes are at the top of the file. |

Placeholder copy (trail name, arrow labels, date) lives at the top of `build_signs.py`. The blaze is a stand-in, not an approved logo. Fonts are Playfair Display and Outfit, under the SIL Open Font License, converted to outlines; font files and Python packages stay out of the repo.
