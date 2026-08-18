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
- **README.md is the index** — keep it current with any meaningful change.
- Commit subjects are plain English a non-developer can read. The in-app
  "Recent changes" box that listed them verbatim was removed 2026-08-18,
  across the whole app family; the habit stands.
- After changes: browser-test locally (preview server, port 8013), run
  tests.html, commit, push, verify the Pages deploy and CI, spot-check live —
  then stop the preview server.
