# news20-front-page-entry3

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/freezzard/news20-front-page-entry3/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/freezzard/news20-front-page-entry3/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A classic newspaper front page for Friday 20 November 2026, drawn entirely in code. Thirty-five verified stories from that one day: three illustrated hero cards (the missile barrage on Kyiv's river bridges, Cyclone Akvan's landfall in Odisha, the AI sell-off across Asia's markets), ten more illustrated cards, the day in numbers, a region tally bar, a dot-pinned world map, twenty-two one-line briefs, and a date-check footer that names what was left out as other days' news. The Python program in this repo (render.py, scenes.py, draw.py, data.py) draws the page at 2048x2048 and exports the 1024x1024 entry.png; main.ts copies those bytes to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=2k68scpr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
