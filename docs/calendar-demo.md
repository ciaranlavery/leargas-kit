# Calendar demo (LK6) — reuse `https://calendly.com/leargas/30min`

Decision: **reuse the existing Calendly link everywhere; no new demo account.**
Why: link is already live with no secrets (public scheduling URL, nothing in repo);
a second account splits notifications across two inboxes and risks missed bookings.
Code reads the URL from one place (`CALENDLY_URL` in `index.html`), so swapping later is a one-line change.

## Code hooks (already wired)

- `index.html`: `CALENDLY_URL` const → all `a[data-calendly]` hrefs set from it (8 anchors:
  topbar, hero, demos, why, pricing, book-head "new tab", inline fallback, book fallback).
- Inline widget: `.calendly-inline-widget[data-url]` (42rem) + `widget.css` / `widget.js`
  from `assets.calendly.com`; inner `.cal-fallback` shows when the widget is blocked,
  hidden by JS once the iframe renders. Outer `.book-fallback` link always present.
- Anchors: `#book` section on index; sticky CTA (`#stickyCta`, shown ≤56rem, hidden while
  `#book` is in view) and final CTA scroll to `#book`. Mobile 360px: widget `min-width:18rem`.
- Mock/real split: dashboards + Monday pack labelled SAMPLE / "Mock data throughout";
  `#book` copy states booking is a real slot with confirmation email.

## Owner checklist (HITL — ~10 min, Calendly account access required)

- [ ] Connect: Calendly → Calendar Connection → owner's Google/Outlook calendar;
      confirm event type `30min` length, buffers, and working hours cover rota-friendly times.
- [ ] Notifications: confirm owner gets new-booking email + calendar invite; test address first.
- [ ] Test booking proving date set: open site → `#book` → pick a real date/time →
      enter test name/email → confirm → assert: (1) Calendly confirmation page shows the
      date/time, (2) confirmation email arrives with the same date, (3) event with date
      appears on the connected calendar. Screenshot all three for LK5 evidence.
- [ ] Blocked-widget check: with an ad-blocker / JS off, assert the inline area shows the
      fallback link and it opens the same Calendly URL in a new tab.
- [ ] Revoke test: cancel the test event from Calendly (cancels calendar hold too);
      delete the test invitee record if GDPR-minimalism wanted. No test data stays live.
- [ ] To change the link later: edit `CALENDLY_URL` only — anchors, popup, and inline
      widget follow automatically. Do not hardcode a second URL.
