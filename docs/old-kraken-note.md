# DK1 old Kraken mark — sourcing note (issue #13)

## Answer

Usable old mark found and vendored: `previews/logos/kraken-old.svg`.

- Source URL: https://commons.wikimedia.org/wiki/File:K-logo-wikipedia.svg
- Direct file: https://upload.wikimedia.org/wikipedia/commons/4/42/K-logo-wikipedia.svg
- Uploaded 26 Jan 2021 by UncleXYZ from Kraken's press page
  (`https://www.kraken.com/press/kraken-images`); author listed as
  Kraken Financial.
- Format: SVG, nominal 512 × 87, viewBox `0 0 150.5 25.6`, 3 KB,
  transparent background (no bg rect), 7 paths (tentacle icon + kraken
  wordmark), single flat fill `#5841D8`.
- License: Commons `PD-textlogo` (public domain — below threshold of
  originality). Trademark still belongs to Kraken; fine for the
  ex-Kraken founder-bio use. No attribution legally required; credit
  "Kraken Financial via Wikimedia Commons" stays in this note.

## Why it fits

- Flat lilac `#5841D8` vs current `previews/logos/kraken.png` (downscaled
  480 × 170 from the 1144 × 404 2024 lockup), whose opaque pixels meter as
  dark-purple `(24,0,72)` with magenta shading `(216,72,223)` — the
  cartoonish gradient the ticket wants to move away from.
- Same creature + wordmark lineage, pre-2024 flat treatment: reads clean
  at chip size, matches the "old lilac mark" decision locked in map #12.

## Alternatives checked

- `File:Kraken-logo-light-background.png` (1144 × 404, 27 Sep 2024, CC BY-SA
  4.0) — this IS the current cartoonish lockup; rejected as the thing we
  are replacing. https://commons.wikimedia.org/wiki/File:Kraken-logo-light-background.png
- `File:Kraken_bitcoin_exchange_logo.png` (en.wikipedia, 421 × 48, 2016,
  PD) — even older dark-slate raster wordmark, palette PNG, small; worse
  than the 2021 SVG in every way.
  https://en.wikipedia.org/wiki/File:Kraken_bitcoin_exchange_logo.png
- Simple Icons (3460 icons, `develop` branch data): no Kraken-exchange slug
  exists — only GitKraken (different company). Nothing to vendor there.
- Kraken press kit (`https://www.kraken.com/press/kraken-images`): no direct
  logo download — "contact press@kraken.com". The 2021 SVG's stated source
  is that same press page, so this is the press artwork, vendored.

## Suggested swap (not done here — research branch only)

`index.html` proof block currently uses `previews/logos/kraken.png`
(60 × 21 display). Swap src to `previews/logos/kraken-old.svg`, keep
`class="wlogo"` + `width:auto` per the wordmark rule, confirm
`scripts/ui_gates.py` stays green.
