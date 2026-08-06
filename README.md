# Team Dashboard

Four weekly flow metrics for as many delivery teams as you like, from nothing but a list of
completed and started dates. Single page, no build step, nothing to install.

**Live:** https://eagleadams86.github.io/team-dashboard/

Paste your work items, get four charts:

| Dimension | Question it answers | What's plotted |
|---|---|---|
| **Quality** — how well | How much bug debt do we carry? | Unplanned work as a share of everything completed, per week |
| **Responsiveness** — how fast | How long from starting to finishing? | Average cycle time per week |
| **Productivity** — how much | What pace do we deliver at? | Items completed per week |
| **Predictability** — how repeatable | Is our completion pace consistent? | Net flow — items completed minus items started, per week |

Each chart carries a dashed linear trend line.

## Teams

Each team keeps its own list of work items; the picker in the header chooses which one the
dashboard is showing. Add, rename and delete teams from the **Teams** card on the Your Data
tab. Settings are shared by every team — one place to say what "unplanned" means.

Which team you're looking at is a position on *this* device and deliberately isn't synced:
switching team on the laptop shouldn't yank the phone to the same team.

## Getting your data in

The **Your Data** tab takes a paste from Jira, a CSV or any other export and loads it into the
team currently selected in the header. Paste the export as it comes — a Jira export looks like this
and works unchanged:

```
Key        Resolved    In Progress   Issue Type
DAE-1064   5/11/2026   4/27/2026     Story
DAE-1058   5/15/2026                 Story
DAE-1491               8/5/2026      Story
```

**The columns are worked out from the data, not assumed by position.** Header names win when
they're there (`Resolved`/`Completed`, `In Progress`/`Start`, `Issue Type`); otherwise the app
finds the date columns by content and tells completion from start by **which date is later**,
so an export with the two the other way round still reads correctly. The work-type column is
told from the issue-key column by repetition — keys never repeat, types always do. Whatever it
settles on is **named back to you** after every paste, because a wrong guess here would
silently corrupt every number on the dashboard.

- Tabs and commas both work, and a header row is skipped automatically.
- Dates can be ISO (`2015-01-21`), numeric (`21/01/2015`), month-name (`21 Jan 2015`) or a raw
  day-count serial (`42043`). Where `03/04/2015` is genuinely ambiguous, the app auto-detects
  day-first vs month-first from the rest of your data — or you can force it.

**Work in progress belongs in the paste.** An item with a start date and no completion is not
an error — it's work you've begun, and it counts on the Predictability chart as work started.
Rows with *no* dates at all — untouched backlog — are ignored, and the count is reported so a
paste of 260 rows that becomes 170 items explains itself.

Genuinely unreadable dates are still errors and get listed back with their line numbers.

There's no inline row editing — to fix something, correct it at the source and paste again.

## Settings

Everything the four charts depend on, shared by all your teams:

- **Unplanned work type** — the exact text in your Type column that means "unplanned"
  (`Bug` by default). Anything blank, or not matching, counts as planned work.
- **Same-day cycle time** — what an item that starts and finishes on one day is worth
  (`0.5` days)
- **Legend labels** (`Stories` and `Bugs` by default) and the **word for cycle time**
  (Cycle time / Time in Process / TiP / In process time)
- **Work type filter list** — the Display → Value pairs behind the dashboard's filter, `All`
  and `Bugs → Bug` out of the box

Nothing else is here on purpose: a setting that changes nothing is worse than a missing one.

## How the numbers are worked out

`derive()` in [index.html](index.html) is the only place any figure is computed. The parts
worth knowing:

- **Weeks start on Sunday.** Week keys are `YEAR-WW`, where the week containing 1 January is
  week 1. Written out by hand, because JavaScript has no week-number function.
- **The date window trims the axis, not the data.** "Show data for most recent 3 months" moves
  where the chart starts; every item still counts toward the weeks that remain. That's
  deliberate.
- **Cycle time** is `completed − started`, floored at 0, with same-day items taking the
  configured value.
- **Unfinished items count as work started, and nothing else.** They move net flow but add
  nothing to throughput, the bug rate or the cycle-time average, all three of which key off
  a completion. Dropping them — which an earlier version did — made net flow read
  systematically too positive.
- **A week with no unplanned work scores 0%**, not blank; a week with no completions has an
  average cycle time of 0.

Net-flow bars use the theme's accent for positive and `--serious` for negative — deliberately
not the red/green pair, because the coaching goal is "keep around zero", so neither sign is
good or bad.

## Cross-device sync (Firebase, free tier — optional)

Signing in with Google is entirely optional and does one thing: puts the same teams on your
other devices. Without it the app is fully usable and fully local.

Sync is **enabled** in this deployment, backed by the `teamdashboard-6723f` Firebase project.
`FIREBASE_CONFIG`, at the top of the bottom `<script type="module">` block in `index.html`,
points at it; setting that constant back to `null` returns the app to local-only mode and
hides all sync UI.

To recreate the setup from scratch (e.g. in a fork):

1. At [console.firebase.google.com](https://console.firebase.google.com), create a project
   (Analytics not needed)
2. **Build → Authentication → Get started → Google** — enable the Google sign-in provider
3. **Authentication → Settings → Authorized domains** — add `eagleadams86.github.io`
4. **Build → Firestore Database → Create database** (production mode), then paste the contents
   of [`firestore.rules`](firestore.rules) into **Rules**
5. **Project settings → Your apps → Add app → Web** — copy the `firebaseConfig` object and
   paste it as the value of `FIREBASE_CONFIG`, **and** put its `authDomain` into the
   `frame-src` of the Content-Security-Policy `<meta>` at the top of `index.html` — the
   sign-in popup is blocked if those two disagree

The config object is not a secret; access is controlled by the rules, which restrict every
user to their own document. Each person who signs in gets their own private data — sharing
the app means sharing the URL, not the data. There is deliberately no shared-workspace model.

### About the `apiKey` in this file

GitHub secret scanning flags it as a "Google API Key — public leak". **That alert is expected
and has been closed as won't-fix** (the same alert exists, and is closed, on every one of these
Firebase apps).

A Firebase Web API key *identifies* the project; it doesn't *authorise* anything. Every Firebase
web app ships it in client JavaScript, because the browser has to have it. Rotating it would
change nothing, because the new one would be just as public.

What actually guards the data, checked on 2026-08-06:

| | |
|---|---|
| Firestore | Denies every unauthenticated read, on this app's path and all others |
| Anonymous sign-up | Disabled — `accounts:signUp` returns `ADMIN_ONLY_OPERATION` |
| Other Google APIs | None enabled in the project, so the key reaches nothing else |

The one forward-looking risk is that enabling some other API in the project later would widen
what an unrestricted key can reach. That's what the key restrictions below are for.

`firestore.rules` is a checked-in copy for the audit trail; the console is what's live. If the
rules ever change there, update the file to match.

**How sync behaves:** `localStorage` stays in charge and the cloud only mirrors it. The
**first** time a given Google account signs in on a browser, if both sides already hold data,
a dialog asks which copy to keep — deliberately not a timestamp guess, which cost real data in
the sibling app. Underneath that, **an empty copy never beats a copy with data in it**,
whichever is newer: without that rule, signing in on a fresh browser would push its emptiness,
stamped `now`, over the device that actually had the teams. The one empty team a fresh browser
creates doesn't count as data; teams you named do.

If sync stops working the button says **"⚠️ Not syncing"** and the note at the foot of the page
gives the cause and the remedy — a silent failure would leave the app claiming to sync while
nothing had left the browser for weeks. There's no retry button on purpose: Firestore retries
the transient causes itself, and the next successful save clears the state.

## Running it

Single page, no build step, no accounts required. Open `index.html` directly, or serve the
folder:

```bash
python3 -m http.server 8013
```

Your data lives in `localStorage`, and leaves the browser only if you sign in.
[`privacy.html`](privacy.html) is the privacy policy — keep it and its effective date current
if what the app stores, or where it sends it, ever changes.

A Content-Security-Policy `<meta>` at the top of `index.html` restricts the page to its own
scripts plus Firebase's CDN, and network access to the handful of Firebase endpoints sync
uses. **Any new external endpoint has to be added there too**, or it fails only in production.

One piece of expected console noise: Google's auth iframe fires a telemetry beacon at
`apis.google.com/js/gen_204` and the policy blocks it. Sign-in is unaffected — it's
fire-and-forget logging — and the block is what makes the privacy policy's "no analytics"
claim true, so don't allow it through.

## Tests

`tests.html` pins the pure functions by loading the real `index.html` in a hidden iframe — no
copies to drift. It must be served over `http://localhost`, not opened as a file.

Beyond the metrics it covers `detectColumns()` (a leading key column, the dates either way
round, header names beating position, a free-text summary not being mistaken for the type),
work-in-progress handling — including the net-flow bug stated as a test — and the sync
boundary: `sanitizeTeams()` (ids arriving from the cloud end up in `data-` attributes and
`<option value>`, so anything not `[A-Za-z0-9_-]{1,64}` is replaced), `normalizeSettings()`,
and `hasData()`, the predicate the "empty never beats data" rule rests on.

The expectations are pinned to a fixed 141-item sample, right down to the weekly throughput
series, `10.2857…` days average cycle time in week 1, `−5` net flow in week 1, and the 19.92%
average bug rate in the Quality chart title. Change the maths and the suite says so.

## Files

| File | |
|---|---|
| `index.html` | The whole app — inline CSS and JS |
| `chart.min.js` | Chart.js 4.4.1, vendored (no CDN) |
| `theme.css` | Copy of the palette from [claude-theme-pack](https://github.com/eagleadams86/claude-theme-pack); also inlined into `index.html` so it works over `file://` |
| `tests.html` | Pure-function tests |
| `privacy.html` | Privacy policy — exists because other people may sign in |
| `firestore.rules` | Checked-in copy of the deployed security rules |

Four themes — Midnight (default), Dark, Light, Sepia — from the shared theme pack. Palette
changes belong in the pack, not here.
