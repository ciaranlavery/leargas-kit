#!/usr/bin/env python3
"""UI consistency gates for the Leargas sales kit (see AGENTS.md).

Run before every merge to main:  python3 scripts/ui_gates.py
Exit 0 = green. Exit 1 = violation listed. No dependencies.
"""
import re
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

    # 2. Demo structure: one slim top bar, one booking band, one quiet footer.
    for d in DEMOS:
        t = text[d]
        check(f"demo-top:{d}", t.count('class="demo-top"') == 1,
              f"count={t.count('class=\"demo-top\"')}")
        check(f"bookbar-once:{d}", t.count('class="bookbar"') == 1,
              f"count={t.count('class=\"bookbar\"')}")
        check(f"home-link:{d}", "← Léargas home" in t, "accent home link present")
        check(f"mock-label:{d}", ("mock" in t.lower() or "sample" in t.lower()),
              "mock/sample labelled")

    # 3. No arrows on booking buttons/links (FAQ timeline prose in index exempt).
    for d in DEMOS:
        check(f"no-booking-arrow:{d}", "30-min chat →" not in t,
              "arrow-free" if "30-min chat →" not in t else "found → on booking copy")
    btn_arrows = [ln.strip()[:100] for ln in text[LANDING].splitlines()
                  if 'class="btn' in ln and "→" in ln]
    check("landing-btn-no-arrow", not btn_arrows, f"{len(btn_arrows)} btn lines with →" if btn_arrows else "buttons arrow-free")

    # 4. Landing structure.
    land = text[LANDING]
    check("no-proof-section", 'id="proof"' not in land and "Pilot feedback" not in land,
          "proof removed")
    check("no-mid-cta", "mid-cta" not in land, "no mid-section CTA rows")
    check("no-band", "block band" not in land, "no arbitrary tinted band")
    check("demos-dark", 'class="block dark" id="demos"' in land,
          "dark shots hosted on dark section")
    feat = re.search(r"\.feat \.n\{[^}]*width:([\d.]+rem)", land)
    step = re.search(r"\.step \.n\{[^}]*width:([\d.]+rem)", land)
    check("markers-one-size", bool(feat and step and feat.group(1) == step.group(1)),
          f"feat={feat.group(1) if feat else '?'} step={step.group(1) if step else '?'}")

    # 5. CTA budget (catches redundancy creep).
    for p in pages:
        n = text[p].count("calendly.com/leargas/30min")
        limit = 11 if p == LANDING else 4
        check(f"cta-budget:{p}", n <= limit, f"{n}/{limit} refs")

    # 6. Placeholders, previews.
    for p in pages:
        hits = [w for w in ("TODO", "FIXME", "lorem", "Lorem") if w in text[p]]
        check(f"no-placeholder:{p}", not hits, f"{hits}" if hits else "clean")
    for name in ("juice", "restaurant", "social", "leisure"):
        check(f"preview:{name}", (ROOT / "previews" / f"{name}.png").exists(), f"previews/{name}.png")

    print(f"\n{len(FAILS)} failures" if FAILS else "\nALL GATES GREEN")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
