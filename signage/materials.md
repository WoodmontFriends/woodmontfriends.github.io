# Friends of Woodmont Park signs: materials and cutter day

**Estimated total: about $250** (likely $240 to $300) for the initial run below. Prices are estimates checked November 6, 2026. Nothing has been ordered, and nothing has been cut on a real machine.

**Initial run, an assumption:** 1 trailhead sign, 2 yard signs (one side each), 6 blaze plates, 4 arrow plates (2 of each label), and 2 marker posts.

The line-by-line order list with links is in [materials.csv](materials.csv). Exact piece sizes and positions are in [piece-placement.csv](piece-placement.csv).

## Three things that shape this list

1. **I couldn't find dark green stock in small quantities.** E Street's aluminum composite and USCutter's corrugated plastic list no green, and the other leads couldn't be verified: [a Home Depot green panel](https://www.homedepot.com/p/Falken-Design-24-in-x-48-in-x-1-8-in-Thick-Aluminum-Composite-ACM-Green-Sheet-Falken-Design-ACM-GR-1-8-2448/324727630) (page blocked, shade and price unknown) and [Sign Warehouse's colored aluminum](https://signwarehouse.com/products/aluminum-metal-sign-blank-18-in-x-24-in-8-colors) (about $28 each, conflicting page details). So this budget uses **white blanks wrapped in dark green vinyl**. If the cutter's owner can get green stock, drop the wrap (line 3) and re-price the blanks.
2. **Apply vinyl indoors in November.** Orafol's [Oracal 651 data sheet](https://www.orafol.com/products/americas/en/technical-data-sheet/oracal-651-intermediate-cal-id3542-technical-data-sheet-americas-en.pdf) sets a 46°F minimum application temperature. It rates colors for 6 years in vertical exposure, Climate Zone 1.
3. **The colors are matched by name, not measured.** No supplier published hex values. Get a swatch before buying the green.

| Design color | Hex | Stocked vinyl | Check |
|---|---|---|---|
| Deep green | `#1f3a2e` | Oracal 651 **613 Forest Green** | Compare with 060 Dark Green |
| Trail yellow | `#f2c230` | Oracal 651 **021 Yellow** | Compare with 020 Golden Yellow |
| Pale | `#eef3ec` | Oracal 651 **010 White** | 023 Cream is likely warmer |

## By sign type

Vinyl areas are measured from the cut files and agree with a pixel count of each file to within 0.2 sq in. Costs below are for items only that sign type uses; shared items are listed separately.

### Trailhead sign, 18 × 24 in (make 1): $53.27 plus shared items

- **Substrate:** 1 aluminum composite blank, 3 mm, with one 19 × 25 in piece of green wrap
- **Vinyl:** yellow 9.8 sq in, pale 27.2 sq in
- **Hardware:** one 4 × 4 × 8 ft post, 2 bags of concrete, 2 lag screws with nylon washers. Two holes are marked at 0.9 in and 23.4 in from the top.

### Workday yard sign, 24 × 18 in (make 2): $30.59 plus shared items

- **Substrate:** 2 corrugated sheets with vertical flutes, each with a 19 × 25 in piece of green wrap
- **Vinyl per sign:** yellow 30.1 sq in, pale 22.4 sq in (6.2 of that is the date line)
- **Hardware:** 2 H-stakes, from a 10-pack
- **Date strip:** Peeling a date off a vinyl wrap could lift the wrap. Instead, put each date on a 2.5 × 20 in strip of the third sheet, wrapped in green, and zip-tie it over the swap zone. Test this on the first sign, since it hasn't been tried.
- **Spare strip:** The run includes a "Join us today" strip per sign, 4.2 sq in, which never goes out of date.
- **Both sides:** Adds 105 sq in of vinyl, and the 5-yard rolls still cover it.

### Trail markers, 3 × 6 in blaze and 14 × 4 in arrows (make 6 and 4): $66.69 plus shared items

- **Substrate:** 1 blank cuts into 4 arrow plates (stacked 14 × 16 in) and 6 blaze plates (from the leftover 18 × 8 in and 4 × 16 in areas). Wrap each plate with green, or wrap the blank before sawing if the saw leaves a clean edge.
- **Vinyl:** yellow 7.3 sq in per blaze, 43.8 total; pale 5.0 sq in per Footbridge plate and 4.4 per Old courts plate, 18.8 total
- **Hardware:** two 4 × 4 × 8 ft posts cut to 6 ft, 2 bags of concrete, 2 deck screws per plate. Arrows mount at their plain end, like a fingerpost, so they reach out from the post.

### Shared across all signs: $66.68

Green wrap, yellow and white vinyl, transfer tape, 2 squeegees, and alcohol. Weeding tools ($37.99 if the cutter's owner has none) aren't in the total. Volunteers supply masking tape, saw, drill, zip ties, and a post-hole digger.

## Vinyl needed on the roll

Roll length comes from nesting every piece in the run, then adding a 25% recut allowance plus 12 in for a test cut and leader.

| Color | Measured letter area | Nested length, 12 in cutter | With waste | Nested length, 24 in cutter | With waste | Buy |
|---|---|---|---|---|---|---|
| Yellow 021 | 114 sq in | 28 in | 47 in | 14 in | 30 in | 12 in × 5 yd (180 in) |
| White 010 | 99 sq in | 41 in | 63 in | 23 in | 41 in | 12 in × 5 yd (180 in) |
| Forest Green 613 wrap | about 90 in of roll, hand applied | not cut | about 3 yd | not cut | about 3 yd | 24 in × 5 yd |

## 12-inch or 24-inch cutter

The shopping list doesn't change. A 24-inch machine can run a 12-inch roll, and the wrap needs a 24-inch roll either way. What changes is the cutting.

| | 12 in cutter | 24 in cutter |
|---|---|---|
| Files | `cut-untested/gang-12in/` | `cut-untested/gang-24in/` |
| Widest cut used | 11.5 in | 23 in |
| Long lines | Run sideways along the feed, up to 14.2 in | Run straight across |
| Must feed reliably for | At least 41 in in one run, or split the file | At least 23 in |
| If it only takes a 12 × 12 in mat | Won't work for the long lines; needs a 24 in mat or roll feed | n/a |
| Lining up | Every line is placed by hand from `piece-placement.csv` | Same, or cut a whole color layer at once for easier alignment, using more vinyl |

## Cutter-day plan

Plan on **about 5 hours with two people**. These are my estimates, since nothing has been timed on this machine. Share the day with the WCA signs, but keep the two groups' purchases and receipts separate.

**Before the day**

- [ ] Send the cutter's owner the questions below, then confirm the file format and cut width.
- [ ] Have materials in hand a week ahead, including swatches.
- [ ] Get the board's approval for wording and logo, and WRA's OK. Don't cut placeholder names.
- [ ] Update the date line, then re-run `build_signs.py`. To change any label or copy, edit the top of that script.
- [ ] Wrap and trim the blanks in green the day before, so that isn't competing for cutter time (about 1 hour).
- [ ] Print `piece-placement.csv`, or print the proof at any size, for layout.

**On the day**

| Order | Step | Rough time |
|---|---|---|
| 1 | Cut `test-cut-first.svg` in yellow scrap. Measure the 2 in square. Check that the thin serifs on "Woodmont Park" survive weeding. | 20 min |
| 2 | Cut all yellow: the big letters and simple blazes are the easiest | 20 min |
| 3 | Cut all white, including date strips | 25 min |
| 4 | Weed everything, starting with white, which is harder to see | 75 min |
| 5 | Apply transfer tape, then place the trailhead sign | 40 min |
| 6 | Place yard signs and date strips | 45 min |
| 7 | Place the plates, then pack up leftovers and label them by color | 30 min |

Let the signs rest indoors for a day before they go out. Install posts on a separate workday, after calling 811 and marking approved spots.

**If the thin serifs fail the test cut:** slow the cutter and try a fresh blade. If they still lift, reset the Playfair lines in Outfit, which takes a one-line change in the script. The smallest strokes are about 0.07 in in the WRA line and under 0.05 in on a few Playfair serifs.

## Questions for the cutter's owner

1. What's the cutter's make and model, and how wide can it cut?
2. Does it take rolls? How long a run can it hold in line?
3. Which software does it use, and which file does it want? We can convert the files if SVG won't open at the right size.
4. Which outdoor vinyl and transfer tape do you already have, in which colors? Would you rather use a brand you know?
5. Can you buy sign blanks or dark green stock through a supplier?
6. Do you have a weeding tool, squeegee, and spare blade?
7. Which day works, and how much time can you give? Could it be shared with the WCA signs?
8. Would you want to be repaid for materials you supply? Please keep receipts either way.

## Before cutting: files and status

- `designs/`: full-size SVG and preview PNG for each sign, plus `all-signs-proof.png`. These are proofs, not cut files.
- `cut-untested/`: one outlined file per vinyl color per sign. Every file is marked untested. Text is outlines, and the trail line is a filled shape.
- `cut-untested/workday-yard__date-line__pale.svg`: the swappable date line. The date shown (Sat, Nov 14, 9–11 AM) is only an example.
- The two crosses in two-color files are for lining up the second color. Peel them off afterward.
- **Placeholders needing board approval:** the blaze logo, "Woodmont Park Trails", "Footbridge", and "Old courts".
