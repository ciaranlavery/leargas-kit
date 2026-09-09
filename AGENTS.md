# AGENTS.md — learned operating rules (2026-09-09, enforced by `scripts/ui_gates.py`)

## Parallel work (learned from LK3/LK4 shared-checkout collision)

- One ticket = one git worktree + one branch (`bb/<slug>`). Never run two
  writers in the same checkout. A merge commit must show whose hunks survived.
- `main` only ever receives reviewed merges. No direct commits for UI/copy.

## Demo pages (`demo-*.html`) — themed product, not landing clones

- NEVER use landing green/cream (`#1c7448`, `#16603b`, `#faf7f0`, `#e9e1d2`,
  classes `lk-topbar`/`lk-cta`/`lk-foot`/`lk-note`) inside demos. Demo chrome
  is `.demo-top` on demo vars (`--surface-2`, `--line`, `--muted`, accent link).
- One booking band per demo (`.bookbar`, theme `--accent` button, NO `→` on
  the button) + ONE quiet footer (home link in accent + mock line). No stacked
  triple footers, no green CTA button inside a themed dashboard.
- No `→` on booking-button/intro links (timeline `→` inside FAQ prose is fine).

## Landing (`index.html`) — carousel showcase, one intentional contrast

- Demos showcase = autoplay carousel on cream (one slide visible, dots +
  arrows, 4.5s advance, pauses on hover/focus/hidden tab, reduced-motion
  shows static slides). NEVER a static auto-fit screenshot grid — it orphans
  the 4th card (3+1) at common widths and lets captions run off-screen; the
  viewport clips overflow instead. Dark shots sit inside bordered cards.
- Each slide crossfades dark→light stills (`previews/<name>.png` +
  `<name>-light.png`, both 1920px, staggered `thememorph` cycle, frozen under
  reduced-motion). Regenerate stills headless (viewport 1920×1080,
  `color_scheme` dark/light) when dashboards change — never ship blurry 960px.
- Numbers live ONLY on How-it-works steps. Why-cards carry no badges; Grows
  is a plain text strip. FAQ cards centered (`margin-inline:auto`) like price.
- Trust band = `Built for …` + sample line only. No big stat metrics.
- Tinted bands: green final CTA only. No other `band` sections. Number
  markers (`feat .n`, `step .n`) one size. Sections share one rhythm
  (`section.block` padding, no per-section snowflakes).
- CTA budget: topbar, hero, pricing, final, sticky + `#book` widget/fallbacks
  only. No mid-section `Book a 30-min chat` button rows.
- No pilot-feedback/proof section without real named data. Mock stays mock.

## Gate

Run `python3 scripts/ui_gates.py` before every merge to `main`. Green required.
If a rule fires and the design genuinely needs an exception, update this file
first — the exception is a decision, not a silent override.
