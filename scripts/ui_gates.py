#!/usr/bin/env python3
"""UI consistency gates for the Leargas sales kit (see AGENTS.md).

Run before every merge to main:  python3 scripts/ui_gates.py
Exit 0 = green. Exit 1 = violation listed. No dependencies.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMOS = ["demo-juice-bar.html", "demo-restaurant.html",
         "demo-social-group.html", "demo-leisure-club.html"]
LANDING = "index.html"
FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def main() -> int:
    pages = [LANDING, *DEMOS]
    text = {p: read(p) for p in pages}

    # 1. No landing green inside demos.
    banned = ["#1c7448", "#16603b", "#faf7f0", "#e9e1d2", "--lk-",
              "lk-topbar", "lk-cta", "lk-foot", "lk-note"]
    for d in DEMOS:
        hits = sorted({b for b in banned if b in text[d]})
        check(f"demo-chrome:{d}", not hits, f"banned remnants: {hits}" if hits else "no landing green")
        check(f"no-top-banner:{d}", 'demo-top' not in text[d] and 'demo-note' not in text[d],
              "banner-free top, footer carries wayfinding")

    # 2. Demo structure: one booking band + quiet footer, no other furniture.
    for d in DEMOS:
        t = text[d]
        check(f"bookbar-once:{d}", t.count('class="bookbar"') == 1,
              f"count={t.count('class=\"bookbar\"')}")
        check(f"home-link:{d}", "← Léargas home" in t, "accent home link present")
        check(f"mock-label:{d}", ("mock" in t.lower() or "sample" in t.lower()),
              "mock/sample labelled")

    # 3. Purged copy (FAQ timeline prose exempt).
    for d in DEMOS:
        check(f"no-booking-arrow:{d}", "30-min chat →" not in t,
              "arrow-free" if "30-min chat →" not in t else "found → on booking copy")

    # 4. Landing structure.
    land = text[LANDING]
    check("booking-ctas", land.count("https://calendly.com/leargas/30min") == 3
          and '<a class="btn" href="https://calendly.com/leargas/30min"' in land
          and '<a class="final" href="https://calendly.com/leargas/30min"' in land
          and "data-calendly" not in land
          and 'id="book"' not in land
          and "sticky-cta" not in land and "stickyCta" not in land
          and "widget.js" not in land,
          "hero button + proof text link + final band, nothing else")
    check("works-strip", all(k in land for k in (
        "Square", "Zettle", "SumUp", "Lightspeed", "Xero", "Open Banking",
        "Don't see yours?", "if it exports, we can use it"))
          and "probably packs" not in land
          and "@keyframes mq" in land
          and land.count('class="mq-half"') == 2
          and all((ROOT / "previews" / "logos" / f).exists() for f in (
              "square.svg", "xero.svg", "zettle.png", "sumup.svg", "lightspeed.svg"))
          and "filter:grayscale(1)" not in land
          and "opacity:.62" not in land
          and ".chip img.word{width:auto}" in land,
          "logo marquee + escape hatch, full-color marks vendored, wordmarks keep aspect")
    check("works-on-top", land.find('class="works"') < land.find('class="hero"'),
          "slim full-color band above the hero")
    check("one-voice", "Book a 30-min chat" not in land
          and land.count("Book the free 30-min chat") == 2,
          "every CTA reads exactly 'Book the free 30-min chat'")
    check("no-fit-phrase", "not a fit" not in land,
          "phrase purged")
    check("no-autoplay-copy", "slides on its own" not in land
          and "closest match" not in land,
          "manual carousel, no steering copy")
    check("no-proof-section", "Pilot feedback" not in land
          and "What a Monday changes" not in land,
          "no invented-testimonials section")
    check("honest-proof", all(k in land for k in (
        'id="proof"', "Who's behind it", "No client logos",
        "Founding partners", "labelled sample")),
          "founder + pilot-stage honesty, no fake clients")
    check("no-fabrication", all(n not in land + "".join(text[d] for d in DEMOS)
                                for n in ("Sarah", "Mick", "Aoife")),
          "no invented people anywhere")
    check("no-mid-cta", "mid-cta" not in land, "no mid-section CTA rows")
    check("no-band", "block band" not in land, "no arbitrary tinted band")
    check("no-trust-metrics", "class=\"metrics\"" not in land, "trust band is one line")
    check("no-static-grid", "demo-grid" not in land, "no orphan-prone screenshot grid")
    check("demos-carousel", all(k in land for k in (
        'id="demoCarousel"', 'id="demoTrack"', 'id="demoDots"',
        'id="carPrev"', 'id="carNext"')) and land.count('class="shot slide"') == 4,
          "manual carousel, 4 slides, dots + arrows")
    check("carousel-motion-safe", "armSlide" in land
          and "function tick" in land
          and "transition:opacity 1.5s" in land
          and "img.light.lit{opacity:1}" in land
          and "thememorph" not in land
          and "setInterval" not in land
          and "nextT" not in land
          and "snapGuard" in land
          and "prefers-reduced-motion: reduce" in land
          and "visibilitychange" in land,
          "manual advance, ping-pong morph, stuck-guard; static under reduced-motion")
    check("captions-below", ".shot-cap{display:flex" in land
          and "shot-cap b{font-size:1.0625rem" in land
          and all(s not in land for s in ("Sales by day, stock gaps", "Covers, promo profit",
                                          "Tickets, engagement", "Membership, courts")),
          "title-only static caption bar, nothing overlaid on shots")
    check("sample-pdf", (ROOT / "sample-monday-pack.pdf").exists()
          and 'href="sample-monday-pack.pdf" download' in land,
          "downloadable sample pack")
    check("theme-stills", land.count('class="light"') == 4,
          "one light layer per slide")
    check("markers-one-size", ".feat .n" not in land and ".step .n" in land,
          "numbers live only on How-it-works steps")
    check("sections-consolidated", "Grows with you" not in land
          and "compounds" in land,
          "Grows folded to one line, no third card grid")
    check("price-stands-off", "margin:2rem auto 0" in land,
          "price card spaced off its title")
    check("faq-centered", "details.faq" in land and "margin:0 auto .75rem" in land,
          "FAQ cards centered like price card")

    # 5. Booking linkage: hero button + final band on landing, one band per demo.
    for p in pages:
        if p == LANDING:
            continue
        check(f"demo-cta:{p}", text[p].count("calendly.com/leargas/30min") == 1
              and "Book a 30-min chat" not in text[p]
              and text[p].count("Book the free 30-min chat") == 1,
              "one band, one voice")
        check(f"no-fit-phrase:{p}", "not a fit" not in text[p],
              "phrase purged")

    # 6. Placeholders, previews.
    for p in pages:
        hits = [w for w in ("TODO", "FIXME", "lorem", "Lorem") if w in text[p]]
        check(f"no-placeholder:{p}", not hits, f"{hits}" if hits else "clean")
    for name in ("juice", "restaurant", "social", "leisure"):
        check(f"preview:{name}", (ROOT / "previews" / f"{name}.png").exists(), f"previews/{name}.png")
        check(f"preview-light:{name}", (ROOT / "previews" / f"{name}-light.png").exists(), f"previews/{name}-light.png")

    print(f"\n{len(FAILS)} failures" if FAILS else "\nALL GATES GREEN")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
