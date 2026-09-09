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

## Landing (`index.html`) — one intentional contrast only

- Dark dashboard screenshots live on the dark `#demos` section
  (`.block.dark`). Never put dark shots on cream.
- Tinted bands: the dark demos section + green final CTA only. No other
  `band` sections. Number markers (`feat .n`, `step .n`) one size.
- CTA budget: topbar, hero, pricing, final, sticky + `#book` widget/fallbacks
  only. No mid-section `Book a 30-min chat` button rows.
- No pilot-feedback/proof section without real named data. Mock stays mock.

## Gate

Run `python3 scripts/ui_gates.py` before every merge to `main`. Green required.
If a rule fires and the design genuinely needs an exception, update this file
first — the exception is a decision, not a silent override.
