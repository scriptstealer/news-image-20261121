# The World Today: 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/scriptstealer/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/scriptstealer/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun bounty entry: one image summing up the world news of
**Saturday 21 November 2026** — drawn procedurally with Pillow, no network,
fully deterministic.

`main.py` (Python 3.13, standard library + PIL) writes the newspaper front
page to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`):

- Lead: Iran strikes U.S. bases in Bahrain
- Russian missile hits Kryvyi Rih, Ukraine
- Mexico captures FBI most-wanted cartel boss "Chapo Isidro"
- COP31 climate talks run past their deadline in Antalya
- AI sell-off hits Wall Street — worst week since Covid
- Magnitude 6.8 quake shakes the Banda Sea off Timor-Leste
- In brief: Bolsonaro in intensive care; France marches over the cost of
  living; France beat Argentina 45–17 to reach the rugby final

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs are byte-identical. Font loading is defensive: the program tries a
list of system font paths and falls back to Pillow's built-in font if none
exists, so a missing font can never crash it.

Referral code: `6rdgs9pm`
