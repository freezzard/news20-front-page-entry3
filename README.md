# Friday 20 November 2026 — The World in One Day

A one-page newspaper front page that sums up Friday 20 November 2026
in 35 dated stories: three large hero stories, ten medium stories, and
22 one-line briefs, with a world map, a six-number strip, and a region
tally. The page is drawn in code with Pillow, saved as `entry.png`
(1024 by 1024, under 1 MiB), and copied to the output directory by
`main.ts`.

## What is on the page

- **Masthead.** The date in giant serif type: Friday 20 November 2026.
  A kicker line above it states the scope: 35 stories, 7 regions.
- **Sub-headline.** One line naming the four biggest stories of the day.
- **Number strip.** Six big figures from the day: 3 bridges hit in Kyiv,
  300,000+ people evacuated before Cyclone Akvan, -6.2% for Taiwan's
  index, 100,000 youth visas a year in the UK-EU deal, 2.3% Japan CPI,
  and 118 runs by Phillips against India.
- **Region tally.** A bar that counts the 35 stories by region: Europe 10,
  Asia 9, Middle East 3, Africa 1, Americas 9, Oceania 2, Global 1.
- **Hero cards (3).** Kyiv bridges, Cyclone Akvan, Asia's market sell-off.
  Each card carries a painted scene, a kicker, a headline, a two-sentence
  deck, a source line, and a status chip where one applies.
- **Medium cards (10).** UK-EU reset, COP31 final day, Hormuz oil, the US
  Senate war-powers vote, Jakarta-Beijing talks, the Hague genocide
  ruling, Gaza truce line, Wellington cricket, GTA VI launch-day totals,
  and Japan inflation. Each has a small painted scene and the same
  headline, deck, and source pattern as the hero cards.
- **Date check.** A box stating the dating rule: every story on the page
  happened, or was first reported, on Friday 20 November 2026, in any
  time zone. Figures marked ESTIMATE, CLAIM, or ONGOING are not settled.
- **World map.** Numbered pins 1 to 13 mark the hero and medium stories;
  small dots mark the 22 briefs. Pins in crowded Europe are nudged so
  each number stays readable.
- **Briefs (22).** One line each, in two columns, numbered 14 to 35, each
  with its city, its fact, and its source. A long line is trimmed with
  an ellipsis so it never wraps to a second line.
- **Footer.** Source list and a note that pictures and map are drawn
  in code.

## The three hero stories

1. Russian missiles hit three Kyiv bridges — the Darnytskyi, Pivdennyi,
   and Podilsko-Voskresenskyi bridges — killing three and wounding 15.
2. Cyclone Akvan comes ashore near Gopalpur in eastern India after more
   than 300,000 people were moved to shelters; no deaths reported.
3. An AI sell-off sinks Asia's stock markets: Taiwan falls 6.2% in its
   worst week since 1991, Seoul loses 5.2%, Tokyo 5.1%.

## Layout grid, top to bottom

The page is 1024 by 1024 with a 24-pixel margin on each side, leaving
976 pixels of content width. The sections stack in this order:

1. Kicker line and rule, then the giant serif masthead date.
2. One-line italic sub-headline naming the four biggest stories.
3. Six-number strip: six cells, each with a large red figure above a
   small label, separated by hairline rules.
4. Region tally bar: seven colored segments sized by story count, with
   a narrow segment minimum so every label stays readable.
5. Three hero cards in one row, each 246 pixels tall with a painted
   scene 108 pixels tall on top.
6. Ten medium cards in two rows of five, each 132 pixels tall with a
   painted scene 46 pixels tall on top.
7. Date-check box, 46 pixels tall, spanning the full content width.
8. Bottom band: the world map on the left (306 wide) and the 22 briefs
   on the right in two columns of 11.
9. Footer attribution line, centered, in small grey type.

The renderer tracks a running vertical position through these sections
and reports an overflow when the bottom would pass the page edge.

## Files in this repository

- `data.py` — all 35 stories, the six-number strip, the region order and
  paints, the masthead and footer lines, and the date-check wording.
- `draw.py` — fonts, text wrapping and measuring, palette, chips, badges,
  card frames, skies, waves, and building rows.
- `scenes.py` — the 13 painted scenes, one per hero and medium card,
  drawn with plain shapes and no text inside any scene. Each scene is
  painted on a fixed virtual canvas and resized into its picture box,
  so no shape can spill onto the card's text.
- `render.py` — the layout engine: masthead, strip, tally, cards, map,
  briefs, footer. It measures every text block before drawing and
  reports any overflow instead of clipping it.
- `main.ts` — the entrypoint. It copies `entry.png` into the output
  directory byte for byte and verifies size, PNG signature, dimensions,
  and hash.
- `entry.png` — the rendered page, 1024 by 1024.
- `LICENSE` — MIT.

## How to render the page

Python 3 with Pillow, from this directory:

```sh
python3 render.py
```

The script writes `entry.png` in place and prints its size, its SHA-256
hash, and the overflow count. A clean render reports zero overflows.
When the file would exceed the 1 MiB cap, the script requantizes it to
a palette PNG and reports the smaller size.

## How to run the entrypoint

Node 22, from this directory:

```sh
mkdir -p out && node main.ts
```

The program reads the output directory from the environment variable
named at the top of `main.ts` and falls back to `/output` when that
variable is unset. It copies `entry.png`, then checks that the copy
matches the source in size and SHA-256 hash, and prints one summary
line. Running it twice writes identical bytes both times.

## Verification checklist

- `python3 render.py` exits 0 and reports `overflow 0`.
- `entry.png` is 1024 by 1024 pixels and under 1,048,576 bytes.
- Every headline, deck, and brief fits inside its card or column.
- The region tally adds to 35.
- The map shows pins numbered 1 to 13 and dots for briefs 14 to 35.
- `node main.ts` copies the file and prints matching size and hash.

## Notes on the pictures

No photograph is used. Every picture on the page — the bridge attack at
dusk, the cyclone spiral over the coast, the falling market candles, the
two flags on a table, the climate hall, the tanker in the strait, the
senate dome, the two skylines, the court columns, the truce line, the
cricket pitch, the game city at sunset, and the rising Tokyo arrow — is
drawn from simple shapes in `scenes.py`. The world map is drawn from
hand-written continent outlines in `render.py`, projected flat with
longitude across and latitude down. The projection clips the far north
and the far south so the inhabited latitudes fill the map box.

## Sources

Reuters, AP, AFP, UN News, IMD, NASA, Sensor Tower, VGC, ICC, and the
newsrooms named on each card. Claims are attributed as reported; the
page does not present estimates or claims as settled fact.
