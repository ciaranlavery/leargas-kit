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
- One booking band per demo (`.bookbar`, theme `--accent` button, NO `→` on
  the button) + ONE quiet footer (home link in accent + mock line, flex
  `space-between`, baseline-aligned). No stacked triple footers, no green CTA
  button inside a themed dashboard.
- No `→` on booking-button/intro links (timeline `→` inside FAQ prose is fine).

## Landing (`index.html`) — carousel showcase, one intentional contrast

- Demos showcase = autoplay carousel on cream (one slide visible, dots +
  arrows, ~5.1s per viewing: 1.8s hold, one 1.5s morph, 1.8s hold). ONE morph
  per viewing, alternating: odd slides light→dark, even dark→light, so the
  entering slide always starts on the theme the last one ended on. The morph
  is a JS-timed `.lit` class flip (`armSlide`), NEVER a looping CSS animation
  — loop wraps snap mid-view, and JS restarts flash. Resets touch ONLY the
  entering slide while it is off-screen; frozen end-themes glide out cleanly.
  No hover/focus pause (pausing one clock without the other is what desynced
  them); hidden-tab return re-arms. A 900ms `snapGuard` recovers if
  `transitionend` is ever missed. Track glide (.8s) matches the morph pace.
  Captions sit BELOW shots as a static bar (title only), never overlaid on
  dashboard elements.
- Each slide morphs exactly once per 6s viewing (then the advance carries the
  ending theme into the next slide, which starts on it). Stills
  (`previews/<name>.png` + `<name>-light.png`, both 1920px, banner-free).
  Regenerate headless (viewport 1920×1080, `color_scheme` dark/light) when
  dashboards change — never ship blurry 960px.
- Numbers live ONLY on How-it-works steps. Why-cards carry no badges; Grows
  itself is one closing line inside How-it-works, not a third card section.
  FAQ cards centered (`margin-inline:auto`) like price. Price card stands off
  its title, like standfirst rhythm.
- Trust band = `Built for …` + sample line only. No big stat metrics.
- Tinted bands: green final CTA only. No other `band` sections. Sections
  share one rhythm (`section.block` padding, no per-section snowflakes).
- CTA budget: topbar, hero, pricing, final, sticky + `#book` widget/fallbacks
  only. No mid-section `Book a 30-min chat` button rows.
- No pilot-feedback/proof section without real named data. Mock stays mock.

## Gate

Run `python3 scripts/ui_gates.py` before every merge to `main`. Green required.
If a rule fires and the design genuinely needs an exception, update this file
first — the exception is a decision, not a silent override.
