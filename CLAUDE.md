# Team Dashboard ("Flow Metrics" on screen)

Kanban/flow metrics from pasted Jira exports — throughput, cycle time, lead time,
net flow, aged WIP — per team. One file, `index.html`, no build step. Deployed via
GitHub Pages: https://eagleadams86.github.io/team-dashboard/
(The on-screen name is **Flow Metrics**; every identifier still says team-dashboard.)

Charles pastes data from his **work Jira** into this app. That fact drives the two
non-negotiable rule sets below. The sibling app is Sprint Velocity
(`~/claude-sprint-velocity`) — its CLAUDE.md is the fuller reference for the
conventions the two apps share (chrome, themes, sync, share links, testing); this
file records what is specific to this repo and what must never regress.

## Only Numbers and Dates Are Ever Saved (2026-08-12/13)

- **A row is three ISO dates plus one short work-type label. Nothing else. There
  are no free-text or comment fields anywhere in this app — don't add one.**
- `cleanWorkType()` pins the type to a ≤40-char label at BOTH boundaries — the
  paste (`parsePastedRows`) and every read-back (`hydrateRows`). A longer cell (a
  ticket summary in the wrong column) is **dropped whole, never truncated** — 40
  chars of a summary is still work-system text.
- The pasted text itself is parsed on the spot and never stored; `pasteBox` is
  cleared on a replace-load.
- **On-screen text follows the same rule as storage.** Problem rows in the paste
  report are echoed via `refOf()` as only the type and the three dates (each cell
  through `cleanWorkType`), never the raw pasted line — a ticket key (DAE-1023)
  appearing in the help text was reported by Charles and fixed 2026-08-13. Any
  new diagnostic or preview must not repeat raw pasted cells; point at the source
  export with a line number instead.
- **Whitelists at every boundary**: `sanitizeTeams()` and `hydrateRows()` rebuild
  teams/rows from known keys. `hydrateRows()` also applies the paste boundary's
  date-ordering rules (started ≤ completed, created ≤ start) so a hand-edited
  copy can't smuggle a backwards span in as a 0-day cycle time; `normalizeSettings()` returns only
  `Object.keys(DEFAULT_SETTINGS)`; `loadView()` reads only `DEFAULT_VIEW`'s keys.
  A stray key on a hand-edited backup or cloud document must never ride along
  into the saved/synced copies. **A new stored field must be added to the right
  whitelist or it will be deliberately stripped** — tests.html pins this.
- **`SCHEMA` is what makes those whitelists safe against OLDER code, and it is
  now read as well as written.** Stripping an unknown key is right for a hostile
  payload and wrong for a copy written by a NEWER build — and it bites harder
  here than at the sibling app, because `loadState()` writes the hydrated copy
  straight back: an older tab opening a newer document loses the unknown fields
  **on load alone**, no edit needed, and the next save pushes that loss to every
  other device. So four boundaries compare `schema` now:
  - **Boot** — a top-level check under `const SCHEMA`, before any listener is
    attached, calling `haltForNewerData()`: a card over the page, no render, and
    a `throw` that skips the rest of the script block. Skipped in a shared view,
    which reads and writes nothing of this device's own.
  - **`tdAdopt()`** — the live path, for a document arriving mid-session. It
    stores the newer copy **verbatim** first (it is the newest there is, and the
    fresh build reads localStorage next load), then halts.
  - **Restore** — refuses the file with a toast and does NOT halt, because
    nothing has arrived yet and what's on screen is still good. It must stay
    ahead of the `tdAdopt()` call, which would otherwise halt on it.
  - **Share links** carry `SHARE_PAYLOAD_V`, deliberately separate from `SCHEMA`
    (a viewer needs no data schema). It lives on `window.TDShare`, not
    `TDState` — `TDState` is assembled a thousand lines earlier, and reading the
    `const` before its declaration is a TDZ error that takes the app down.
  The halt reuses `viewOnly` (hence `let viewOnly`, not `const`) rather than
  inventing a second flag, so every existing write path is already guarded.
  **Bump `SCHEMA` in the same commit that adds a stored field, and widen the
  whitelist in that same commit.** All of it is pinned in tests.html, the boot
  path by booting a second copy of the app against a planted future document.
- **Working days (2026-08-19) is ONE setting driving THREE durations** — cycle
  time, lead time and the ageing threshold — and the wording on every chart,
  tile, axis and column that states one. Don't let them diverge: a screen mixing
  the two measures is unreadable. `spanDays()` is the only place the choice is
  made, and `derive()` returns `workingDays`/`dayNoun` alongside the numbers so a
  label can never disagree with the figure above it. **Holidays are deliberately
  absent** — per-country, per-year, and free text in an app that stores none —
  and the setting's own hint says so rather than half-implementing it. It took
  `SCHEMA` 3 → 4. A share link carries `settings` whole, so the setting travels;
  a viewer still on an older cached build strips it and reads calendar days,
  which is accepted rather than bumping `SHARE_PAYLOAD_V` — that would make every
  link from this build unreadable to that one, including for the majority who
  never turn the setting on.
- `loadState()` writes a repaired copy back with **`persist()`, deliberately NOT
  `save()`** — a shape repair must not stamp this device's copy newest and race a
  genuinely newer cloud document. (`save()` = persist + timestamp + cloud push;
  reserve it for real edits.)
- Settings labels and team names are short and capped (120); rows carry no ids,
  keys, titles or names of people — `privacy.html` promises this, keep it true
  and update its effective date in the same commit as any storage change.

## Security (shared origin)

- All of `eagleadams86.github.io` is ONE browser origin: any page on any of the
  account's Pages sites can touch this app's localStorage and Firebase session.
  So: **no third-party scripts ever** (`chart.min.js` is vendored — don't
  hand-edit it), a CSP on every page, and any new external endpoint goes into
  the CSP's connect-src after asking whether it's needed at all.
- This app signs in via **Google Identity Services, not Firebase's popup** (the
  flow was proven here first, then ported to Sprint Velocity) — its CSP differs
  from its siblings' accordingly; don't "unify" it blindly.
- Sync: one Firestore doc per user, project `teamdashboard-6723f`; rules confine
  each account to its own data. `FIREBASE_CONFIG` is public client config, not a
  secret — GitHub's leak alerts on it are closed won't-fix; never rotate.

## Offline (`sw.js`)

- **There IS a service worker, and it was refused for a long time.** The three
  objections were right to be made; two turned out to be answerable by design
  rather than by abstention, and the third is what the whole thing is built
  around. Recorded because the next person to touch this needs the reasoning:
  - *"A resident process on the shared origin."* Bounded. A worker's scope
    cannot exceed its own directory without the `Service-Worker-Allowed` header,
    and GitHub Pages cannot send headers — so this one structurally cannot see
    Sprint Velocity or financial-plan. Locally, where the app is served from the
    root, it does control `tests.html`; the allowlist is what makes that
    harmless, not the scope.
  - *"Caches are ORIGIN-wide, not per app."* True, and it does not go away — any
    page on the origin can read this cache, and the sibling workers share the
    store. The answer is the rule in `sw.js`: **only files already public in
    this repo are ever cached** (`./`, `chart.min.js`, `theme.css`,
    `privacy.html`, `favicon.ico`). Nothing in there is anything an attacker
    could not read straight off GitHub, and the data stays in localStorage,
    which every page on the origin could already reach. It cuts the other way
    too — `activate` must only ever delete caches with this app's `td-shell-`
    prefix, or it wipes a sibling's.
  - *"A caching bug serves stale code to an app whose data shape moves."* Still
    the real risk. **The worker is network-first for everything**: you can only
    be served cached code on a visit where the network did not answer. The
    braces to that belt is `SCHEMA` / `haltForNewerData()` above — a saved copy
    from a newer build is refused rather than run through hydrateState(), which
    would strip the fields that build added.
- **The page's CSP does not apply to the worker.** It takes its policy from its
  own script's HTTP response headers, and Pages cannot set headers, so `sw.js`
  runs with **no CSP at all**, permanently installed. Hence: tiny, no `eval`, no
  `importScripts`, no dynamic import, no cross-origin URL anywhere in it — and
  hence `worker-src 'self'` spelled out in the page CSP rather than left to the
  `worker-src → child-src → script-src` fallback chain, which would inherit
  script-src's gstatic and accounts.google.com hosts.
- **`sw-kill.js` is the escape hatch, and it exists BEFORE it is needed.** A bad
  page is fixed by pushing a new one; a bad worker is resident and can keep
  serving itself. `cp sw-kill.js sw.js`, commit, push — every installed copy
  then clears this app's caches, unregisters itself and reloads its windows.
- **Two traps, both of which fail silently:** `cache.addAll` is all-or-nothing
  (one 404 rejects the whole precache, install fails, and there is no offline at
  all while the app looks perfectly healthy online); and **`install` fires once
  per script version**, so if the cache is later evicted nothing rebuilds it and
  offline decays to "whatever the last online visit happened to request". Hence
  `topUp()`, fetching entries one by one, pinged by the page on every load via a
  `shell-check` message — the repair must be able to run without a new worker
  version to hang it on.
- **`shellKey()` matches on the PATH, not the URL**, because the markup asks for
  `favicon.ico?v=1`: keyed on the full URL, the precached favicon would never be
  the entry that answers. `index.html` folds onto `./` for the same reason.
- Registration is guarded three ways, all load-bearing: **not in a frame** (or a
  `tests.html` run would install a worker and then test whatever it had cached),
  **not under `window.tdViewOnly`** — which covers both a shared view and a page
  stopped by `haltForNewerData()`, since the halt's `throw` cannot reach a
  separate script block — and **on `load`**.
- **Testing it locally will mislead you.** The browser holds its own copy of
  `sw.js`, and a byte-identical script fires no `install`, so edits appear to do
  nothing and an emptied cache appears not to refill. `await reg.update()`
  before judging any of it. Related: a suite run against a registered dev worker
  is testing the cache, not the disk — unregister it on localhost before
  trusting a green run.
- The scope is `./`, never absolute: on the local server the app is at the root,
  not under `/team-dashboard/`, and an absolute scope is simply invalid there.

## Working Rules

- **tests.html** (same-origin iframe over `http://localhost`, refuses to run
  anywhere else — that guard is load-bearing, don't remove it) must say "All N
  tests passed" whenever the parser, boundaries, or metrics change; CI
  (`.github/workflows/tests.yml`) runs it headless on every push on port 8013.
  When a rule in this file changes, change the matching test in the same commit.
- The header/chrome is shared with Sprint Velocity — a chrome change in one repo
  is mirrored in the other, including the cross-`applink`.
- Theme: `theme.css` is a copy from `~/claude-theme-pack` (the source of truth
  for ALL apps) — never diverge it locally; palette changes go through the
  pack's `tokens.json` + contrast gate. **All three pages LINK it.** Until
  2026-08-18 `index.html` instead carried a verbatim inline copy of all 74
  tokens so it would also work over `file://`, while `privacy.html` and
  `tests.html` linked the file — the palette twice, in two mechanisms, with the
  inline copy winning. Nothing had drifted, but a pack change would have
  silently done nothing to the app while updating its own privacy page: drift
  with a delay fuse. The cost of linking is that `index.html` no longer stands
  alone — `theme.css` has to sit beside it, and opening the HTML off disk
  without it gives an unstyled page. Don't re-inline to "restore" `file://`.
  What stays in the app's own `<style>`, after the link so it still wins:
  `color-scheme` per theme, the per-theme `--shadow` values and `--chrome-h`.
  **The pack has no `--shadow` token at all**, so those are additions, not
  overrides.
- **THE SAMPLE DATA IS THE DEMO, and a feature isn't finished until it reaches
  it.** `loadSample()` (section 9c) is what someone sent a share link explores and
  what the app is shown with, so every feature must be visible from it. Adding one
  means adding the data that demonstrates it, a line in the roster comment above
  `loadSample()`, a row in the README's demo table, and an assertion in the demo
  group of tests.html — that group exists because these are ordinary-looking
  figures a later edit would tidy without noticing. The same rule runs in Sprint
  Velocity; it was added to both on 2026-08-19 after Charles loaded a sample and
  couldn't find the feature it was meant to show.
  - Every figure in `DEMO_TEAMS` is load-bearing: **Heron's tail is the app's
    central argument** (p85 ≈ 23 days against a median of 5 — tidy that away and
    nothing on screen justifies reading p85 rather than the average); Wagtail has
    **no created dates**, which is the only way the lead-time chart's own
    explanation is reachable; the span stays around nine months so Clean up old
    data and the 6/9/12-month windows all have answers.
  - **The dates cover the WHOLE WEEK, weekends included**, which is the only
    thing that makes the working-days setting reachable from the demo: generate
    completions on weekdays only and the toggle changes nothing on the one
    dataset anybody is ever shown.
  - Dates are counted from `Date.now()`, so the demo is live whenever it is
    opened. The generator is **seeded** (`seededRandom`) — never swap it for
    `Math.random()`, or the dataset reshuffles on every device and no test can
    pin it. A type bag's LENGTH doesn't move the sequence, only which type each
    draw lands on, so the mix can be retuned without moving a single date.
  - It is built as **paste text run through `parsePastedRows()`**, not
    hand-assembled row objects — the demo comes in through the same boundary a
    real export does and cannot produce a shape the parser would never make.
- **`tdAdopt()` asks before dropping Created dates, and a hidden iframe's
  `confirm()` auto-dismisses to "keep them" — which makes the adopt DECLINE.**
  tests.html therefore plants state through its own `plant()` helper, which stubs
  `confirm`, and resets to an empty app at the top of `run()`. Without that, any
  browser whose app happened to hold created dates (anyone who has pressed Load
  sample data on localhost) failed share-payload tests that have nothing to do
  with created dates. Don't call `win.tdAdopt` directly from a test.
- **README.md is the index** — keep it current with any meaningful change.
- Commit subjects are plain English a non-developer can read. The in-app
  "Recent changes" box that listed them verbatim was removed 2026-08-18,
  across the whole app family; the habit stands.
- After changes: browser-test locally (preview server, port 8013), run
  tests.html, commit, push, verify the Pages deploy and CI, spot-check live —
  then stop the preview server.
