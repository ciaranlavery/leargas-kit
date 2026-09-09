# AGENTS.md — learned operating rules (2026-09-09, enforced by `scripts/ui_gates.py`)

## Parallel work (learned from LK3/LK4 shared-checkout collision)

- One ticket = one git worktree + one branch (`bb/<slug>`). Never run two
  writers in the same checkout. A merge commit must show whose hunks survived.
- `main` only ever receives reviewed merges. No direct commits for UI/copy.

## Demo pages (`demo-*.html`) — themed product, not landing clones

- NEVER use landing green/cream (`#1c7448`, `#16603b`, `#faf7f0`, `#e9e1d2`,
  classes `lk-topbar`/`lk-cta`/`lk-foot`/`lk-note`) inside demos.
- NO top banner on demos. Wayfinding is the footer home link only — a banner
  photographs into every screenshot and unbalances the dashboard top.
- Demos end at one `.bookbar` band + ONE quiet footer (home link in accent +
  mock line, flex `space-between`, baseline-aligned). No stacked triple
  footers, no green CTA button inside a themed dashboard.
- No `→` on intro links (timeline `→` inside FAQ prose is fine).

## Landing (`index.html`) — carousel showcase, one intentional contrast

- Demos showcase = MANUAL carousel on cream (arrows + dots, no autoplay):
  the viewed slide ping-pongs dark↔light (1.8s holds, 1.5s morphs) via a
  JS-timed `.lit` flip (`armSlide`), NEVER a looping CSS animation — loop
  wraps snap mid-view, and JS restarts flash. Resets touch ONLY the current
  slide; frozen end-themes glide out cleanly on manual nav. A 900ms
  `snapGuard` recovers if `transitionend` is ever missed. Track glide (.8s)
  matches the morph pace. Captions sit BELOW shots as a static bar (title
  only), never overlaid on dashboard elements. Standfirst is one line; no
  autoplay claims, no "closest match" steering.
- Each slide ping-pongs dark↔light while viewed (morphs alternate direction
  via flip-flop target). Stills (`previews/<name>.png` + `<name>-light.png`,
  both 1920px, banner-free, band-free).
  Regenerate headless (viewport 1920×1080, `color_scheme` dark/light) when
  dashboards change — never ship blurry 960px.
- Numbers live ONLY on How-it-works steps. Why-cards carry no badges; Grows
  itself is one closing line inside How-it-works, not a third card section.
  FAQ cards centered (`margin-inline:auto`) like price. Price card stands off
  its title, like standfirst rhythm.
- Trust band = `Built for …` + sample line only. No big stat metrics.
- Works-with strip lives at the TOP of the page (directly under the topbar),
  slim and translucent: chips at 62% opacity, full on hover. Infinite logo
  marquee (CSS `mq` keyframes, two identical `.mq-half` groups for a seamless
  -50% loop, edge fade mask, pause on hover, wraps statically under
  reduced-motion). Real marks vendored locally in `previews/logos/` (never
  hotlink); brands without a Simple Icons slug get a same-green monogram
  tile, never a fake logo. Escape hatch below the marquee:
  "Don't see yours? Ask — if it exports, we can use it."
- Proof block (`#proof`, above pricing) = founder monogram + pilot-stage
  honesty, never testimonials. Mock stays mock.
- Tinted bands: green final CTA only. No other `band` sections. Sections
  share one rhythm (`section.block` padding, no per-section snowflakes).
## Trust & honesty (non-negotiable — user-verified 2026-09-09)

- NEVER fabricate testimonials, client names, £/hrs-saved figures, founder
  photos, or logos. Pilot-stage MUST read as pilot-stage: the proof block
  says plainly there are no client logos yet and every number is labelled
  sample. When real photo/numbers land, they replace the monogram + pilot
  copy — until then the gate below fails any invented proof on sight
  (Sarah/Mick/Aoife and kin are permanently banned strings).
- Compatibility claims stay input-level ("built from … e.g. …; if it exports,
  it probably packs") — never claim certified integrations.
- Booking CTAs live in exactly three places, all reading word-for-word
  `Book the free 30-min chat` → `https://calendly.com/leargas/30min`: the hero
  button, one `.bookbar` band per demo (theme `--accent` button, NO `→`), and
  the green final band (whole band clickable), plus ONE low-key text link in
  the proof block. Nowhere else — no topbar, pricing, sticky, widget, or
  popup code.
- Works-with marks: real artwork vendored in `previews/logos/` (Simple Icons
  where a slug exists; Wikimedia Commons press SVGs otherwise, e.g. SumUp,
  Lightspeed; transparent PNG downscaled for Zettle). ALWAYS full brand
  colors at full opacity — instant recognition beats decoration; no
  grayscale, no translucency. Brands with no obtainable mark get a same-green
  monogram tile, never a fake logo.

## Gate

Run `python3 scripts/ui_gates.py` before every merge to `main`. Green required.
If a rule fires and the design genuinely needs an exception, update this file
first — the exception is a decision, not a silent override.
