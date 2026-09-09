# LK2 research: BB autonomous loop for this kit (issue #7, part of #5)

Question: how do we run this kit to done with minimal user touches using BB
(getbb.app) driving opencode — threads, git worktrees per ticket,
provider/subs, review gates without user-between-messages — in this repo?

TL;DR: one BB project on this repo, one manager thread per map, one worker
thread per ticket each in its own managed worktree (`bb/<slug>`), opencode
provider reusing the existing opencode login (no extra billing), permission
`auto` (fallback `full` in disposable worktrees) so approvals don't park on
the user, impl thread + reviewer thread per ticket, merge to `main` (Pages
deploys from `main` `/`). Static repo = no setup script needed.

## Sources (primary, checked 2026-09-09)

- BB site: https://getbb.app/ — threads in worktrees, drives opencode et al
  "via existing subs, no extra billing"; hero shows `bb/triage-sentry-spike`
  worktree with Full Access.
- BB repo README: https://github.com/get-bb/bb — every surface (app, CLI,
  HTTP API) drives bb; work runs in threads you follow live, steer, or hand
  off; telemetry opt-out `BB_TELEMETRY=false`.
- Package README `packages/bb-app/README.md` — `npx bb-app@latest` then
  `http://localhost:38886`; prereqs Node 22.19/24/26 + git + provider CLI
  authenticated; "bb will pick up your existing credentials", mix providers
  per task; `opencode` provider = install opencode + authenticate per
  opencode docs; CLI `bb`, SDK `BBSdk.threads.spawn/wait/output`; state under
  `~/.bb/`; opencode models come from opencode's own config (do NOT pin
  opencode models via BB `customModels`).
- Worktrees doc `docs/worktrees.md` — managed worktree = `git worktree add`
  + bookkeeping, own branch, at
  `~/.bb/plugins/environment-git-worktree/host-data/worktrees/<thread-id>/<repo>`;
  env picker **Worktree** or `bb thread spawn --project <id>
  --new-environment worktree --prompt ...`; `--base-branch` omit for smart
  default (origin default); `.worktreeinclude` (gitignore syntax) copies
  untracked files; `.bb-env-setup.sh` runs with `env bash` in new worktree
  pre-agent, 15-min timeout, non-zero fails provisioning; teardown
  `.bb-env-teardown.sh`; auto-remove on thread delete (archive = 5-min
  grace); branch survives worktree removal; failures surface in provisioning
  transcript.
- Config doc `docs/configuration.md` — `~/.bb/config.json` + `env.json`;
  `BB_SERVER_URL` defaults `http://127.0.0.1:38886`; branch prefix setting
  (`bb/` default); provider order/default per picker.
- Copes architecture deep-read: https://flaviocopes.com/bb-agentic-ide/ —
  thread = unit of work (project+provider+env+state+event log); manager
  threads are ordinary threads with spawn/wait/output tools
  (`bb thread spawn --parent-thread thr_manager`, `bb thread wait`, `bb thread
  output`); one thread per worktree; impl/review split; SQLite is source of
  truth; limits (daemon queue not durable, server central, providers differ,
  managers not magic).
- Local repo: `git remote` = `https://github.com/ciaranlavery/leargas-kit.git`
  (main); Pages = legacy build from `main` `/`, public, https enforced,
  live https://ciaranlavery.github.io/leargas-kit/; files `index.html`
  (287 lines, light landing, Calendly `https://calendly.com/leargas/30min`),
  `demo-leisure-club.html` (1122 lines, dark, Chart.js CDN x67 refs),
  other three `demo-*.html` (~90 long lines each, full dashboards with
  light/dark toggle via `localStorage leargas-theme`), `docs/` =
  `expansion-thesis.md` only, `previews/*.png`; no package.json/build,
  no CONTEXT.md. Tooling: `bb` CLI not installed, `opencode 1.18.29`
  present.
- Sibling tickets via `gh`: #2 mechanical gates (placeholders, links/tabs/
  toggles, 360px + light/dark, console-clean + local 200s), #3 copy DoD
  (annotated diff, owner approves), #4 pilot showing (blocked by #2+#3),
  #5 map (destination conversion-ready live kit; BB harness via existing
  subs; mock stays mock).

## Operating pattern

1. One BB project → this repo checkout. One manager thread per map (#5).
2. One worker thread per ticket, each **Worktree** environment, base
   `origin/main`. Branch naming: keep BB default `bb/<slug>-thr_<id>`
   (homepage demo: `bb/triage-sentry-spike`); e.g. `bb/lk3-copy`,
   `bb/lk4-verify`, `bb/lk5-finish`.
3. Manager spawns workers (`--parent-thread`), waits, reads output, routes
   reviewer findings back to worker. Workers never share a worktree.
4. Merge order: worker commits + pushes branch → PR → squash to `main`.
   Pages redeploys from `main` automatically. Never commit Pages output;
   there is none (static root).
5. No user-between-messages: workers run permission `auto` (provider-native
   review, no BB pause); use `full` only inside disposable worktrees.
   Reviewer is a separate thread with clean context, same project.

## opencode provider setup (existing subs, no extra billing)

- `npx bb-app@latest` (allow-scripts flag on npm ≥12 for
  better-sqlite3/node-pty/@parcel/watcher), open `localhost:38886`.
- Provider CLI already authenticated stays the credential: opencode login
  as today; BB picks it up. Per-thread provider/model picker chooses
  `acp-opencode`. Mix providers per task if ever needed.
- BB reads native skill roots incl. opencode
  (`~/.config/opencode/skills`, `.opencode/skills`, compat `.agents/`,
  `.claude/`); repo guidance goes in `.bb/AGENTS.md` (every provider) —
  this repo has none yet, recommend adding a 10-line one (static, mock
  stays mock, Pages from main, verify recipe).
- No `.bb-env-setup.sh` needed (no deps); no `.worktreeinclude` needed
  (no untracked secrets). Optional: tiny setup script asserting clean
  `git status` + `python3 -m http.server` smoke.

## Parallel-safe splits for LK3/LK4 (and #2/#3 now)

| Thread | Owns | Must not touch |
|---|---|---|
| landing/copy | `index.html` | demos |
| demo-leisure | `demo-leisure-club.html` | other pages |
| demo-trio | `demo-juice-bar.html`, `demo-restaurant.html`, `demo-social-group.html` | landing, leisure |
| assets/meta | `previews/`, `<head>` SEO/OG tags | body copy |
| reviewer | nothing (reads diffs, runs checks) | all writes |

Shared `<head>`/theme snippet: single owner per run (landing thread), others
rebase onto `main` after it lands. Copy DoD (#3) stays proposal-only until
owner approves — worker emits annotated diff, does not rewrite.

## Mechanical verify per thread (no build in this repo)

Each worker runs before reporting done (from its worktree root):

```bash
python3 -m http.server 8091 & sleep 1
for p in index.html demo-juice-bar.html demo-restaurant.html demo-social-group.html demo-leisure-club.html; do curl -s -o /dev/null -w "$p %{http_code}\n" http://localhost:8091/$p; done
grep -rn "\[phone\]\|\[email\]\|\[Your name\]\|TODO\|FIXME\|lorem" --include="*.html" . || true
node -e "const s=require('fs');['index.html','demo-juice-bar.html','demo-restaurant.html','demo-social-group.html','demo-leisure-club.html'].forEach(f=>{const h=s.readFileSync(f,'utf8');console.log(f,'calendly:'+(h.match(/calendly\.com\/leargas\/30min/g)||[]).length,'theme-toggle:'+/leargas-theme/.test(h))})"
```

Plus: click every tab/pill/CTA + theme toggle light/dark, 360px width no
horizontal scroll, console zero errors (manual or headless screenshot).
Leisure page needs Chart.js CDN reachable. Evidence (curl output + notes)
pasted into thread output so the reviewer can re-run.

## Init checklist (one session, ~15 min)

- [ ] `npx bb-app@latest`, add project → `/Users/optimusprime/leargas-kit`
      (or clone path on the BB host machine).
- [ ] Confirm provider `acp-opencode` listed (opencode on PATH,
      authenticated). Set default provider opencode.
- [ ] Add `.bb/AGENTS.md` (10 lines: static kit, mock stays mock, Pages
      main:/, verify recipe above, branch `bb/<slug>`).
- [ ] Manager thread prompt includes: ticket text, owned files table,
      verify recipe, "commit branch, open PR, report diff + evidence".
- [ ] Spawn order: #2 + #3 first (parallel-safe per table); #4 blocked
      (human showing, not parallelized); LK3/LK4 only after #7 lands this
      pattern.
- [ ] Reviewer thread per ticket: clean context, `git diff main...branch`,
      re-run verify, send actionable findings back, `bb thread wait` on fix.
- [ ] Merge: squash to `main`, confirm Pages build, archive threads
      (worktrees auto-removed, branches kept).

## Review gates without user-between-messages

Impl thread ↔ reviewer thread replaces the user: reviewer runs the verify
recipe + reads the diff, posts findings to the worker via `bb thread tell`
/ manager relay, worker fixes, reviewer re-checks, manager merges on green.
Automations plugin (`bb automation create --project <id> ...`) optional for
scheduled re-verify; not required for LK. Human gates remain only where the
ticket demands a human (#3 owner copy approval, #4 in-person showing).

## Limits / risks

- BB young: workflows evolving; pin what worked (this file) per run.
- Daemon progress queue is lossy on crash; thread history in SQLite is the
  truth — re-read `bb thread output/log` after reconnects.
- One server = one coordination domain; remote hosts raise trust surface
  (keep server on loopback/Tailscale, never raw public).
- Providers differ (resume/approvals/models); keep workers on opencode for
  this map unless a task needs otherwise.
- Parallel threads can't fix shared-architecture disputes — manager owns
  conflicts, landing-thread owns shared `<head>`.
- Mock stays mock: no real data plumbing, no backend, no paid campaigns
  (map #5 out-of-scope holds).
