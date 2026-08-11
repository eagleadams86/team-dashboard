# Flow Metrics

Kanban flow metrics for as many delivery teams as you like, from nothing but a list of
completed and started dates. Single page, no build step, nothing to install.

**Live:** https://eagleadams86.github.io/team-dashboard/

The app is called **Flow Metrics** on screen. The repo, the Pages path, the Firebase project
(`teamdashboard-6723f`) and the `app: 'team-dashboard'` marker inside a backup file all still
say *team-dashboard* — renaming any of those would break existing links, backups and sync,
so the rename is deliberately a display-only one.

Paste your work items and the charts are grouped into three tabs — **by what the data means**,
so the measures that move together are read together:

| Group | Question it answers | What's plotted |
|---|---|---|
| **Flow** — how long work takes | How long does an item take, and how much of that was waiting? | Cycle time; lead time; flow efficiency |
| **Delivery** — how much comes out | What pace do we deliver at, and is it steady? | Items completed per period; net flow (completed minus started) |
| **Health** — the state of the board | How much of what we finish is defect work? | Defect rate — defects resolved, and defects raised, against everything completed |

**Group by week, 2 weeks or month.** The control sits beside the date window on the dashboard.
Weekly is the default and the finest grain; monthly smooths out the lumpiness that makes a
single week hard to read. The grouping also drives the last column of the Your Data table, so
the table and the charts always name the same period.

Each chart carries a dashed linear trend line, and four **summary tiles** above the tabs state
the window-wide figures — average completed per week, average cycle time (pooled over the items
in the window, so an empty week can't drag it down), the defect rate, and total net flow. Those
four stay visible whichever group is open. The tiles are deliberately neutral: this app has no
targets, so no tile is ever coloured "good" or "bad". There being exactly four of them, they go
four-across on a wide window and pair into a 2x2 on a narrower one — never three and a stray
fourth.

The dashboard shows each chart's title and nothing else standing — the coaching question that
used to sit above every chart was removed deliberately, to get more chart on screen. That
framing lives one press away: the **ⓘ button** beside every tile and chart title opens a
plain-English note on what the figure means and which direction is good.

## One of a pair

This app shares its look and behaviour with
[Sprint Predictability](https://eagleadams86.github.io/sprint-velocity/), its sibling: the same
sticky header, button tabs (with arrow-key navigation), summary tiles, ⓘ help dialogs,
read-only share links, theme picker and footer. **Each app's header carries a link to the
other**, next to the title — one click either way, from anywhere on the page — and both
still cross-link at the foot of the page, where a **Recent
changes** box lists the last ten changes to this file, fetched from GitHub when
expanded. If a chrome rule changes in one app, it should change in the other too — with one
noted exception: how many tile columns there are. This app always has exactly four tiles and
so states its column counts outright, while the sibling's tile groups vary in size and are
still laid out by `auto-fit`.

## Teams

Each team keeps its own list of work items; the picker in the header chooses which one the
dashboard is showing. Add, rename and delete teams from the **Teams** button beside that
picker — a dialog, the same shape as the sibling app's Teams & PIs. Settings are shared by
every team — one place to say what "unplanned" means.

The picker only appears once there are **two or more** teams: with one team it is not a
choice. It is part of a wider rule — nothing shows until there is something behind it, so a
first run is the paste box and its instructions, and nothing else. The **Loaded data** card,
the **Clean up old data** card and the **Append to existing** / **Clear this team's data**
buttons all appear the moment rows exist (`renderEmptyState()`).

Which team you're looking at is a position on *this* device and deliberately isn't synced:
switching team on the laptop shouldn't yank the phone to the same team.

## Getting your data in

The **Your Data** tab takes a paste from Jira, a CSV or any other export and loads it into the
team currently selected in the header. Paste the export as it comes — a Jira export looks like this
and works unchanged:

```
Key        Created     In Progress   Resolved    Issue Type
DAE-1064   4/02/2026   4/27/2026     5/11/2026   Story
DAE-1058   4/09/2026   4/28/2026                 Story
DAE-1491   7/28/2026   8/5/2026                  Story
```

The **Created** column is optional and unlocks lead time and flow efficiency. Without it
everything else works exactly as before, and those two charts say so on their face rather than
disappearing.

**The columns are worked out from the data, not assumed by position.** Header names win when
they're there (`Resolved`/`Completed`, `In Progress`/`Start`, `Created`, `Issue Type`);
otherwise the app finds the date columns by content and ranks them by **which date is later**,
so an export with them in any order still reads correctly — created before started before
completed. The work-type column is
told from the issue-key column by repetition — keys never repeat, types always do. Whatever it
settles on is **named back to you** after every paste, because a wrong guess here would
silently corrupt every number on the dashboard.

- Tabs and commas both work, and a header row is skipped automatically. Quoted CSV fields are
  handled — `"Jan 21, 2015"` or `"Bug, urgent"` stays one cell, comma and all.
- Dates can be ISO (`2015-01-21`), numeric (`21/01/2015`), month-name (`21 Jan 2015`) or a raw
  day-count serial (`42043`). Where `03/04/2015` is genuinely ambiguous, the app auto-detects
  day-first vs month-first from the rest of your data — or you can force it.
- A **time on the end is fine** — `9/23/2025 10:21`, `23/Sep/25 4:12 PM`, `2025-09-23T10:21:00Z`.
  Jira and Excel export timestamps rather than bare dates, and every metric here works in whole
  days, so the clock is dropped. The date underneath still decides day-first vs month-first.

**Work in progress belongs in the paste.** An item with a start date and no completion is not
an error — it's work you've begun, and it counts on the net flow chart as work started.
Rows with *no* dates at all — untouched backlog — are ignored, and the count is reported so a
paste of 260 rows that becomes 170 items explains itself.

Genuinely unreadable dates are still errors and get listed back with their line numbers.

There's no inline row editing — to fix something, correct it at the source and paste again.

## Settings

Everything the charts depend on, shared by all your teams:

- **Defect work type** — the exact text in your Type column that means "defect"
  (`Bug` by default). Anything blank, or not matching, counts as ordinary planned work.
- **Same-day cycle time** — what an item that starts and finishes on one day is worth
  (`0.5` days)
- **Word for defects on charts** (`Bugs` by default) and the **word for cycle time**
  (Cycle time / Time in Process / TiP / In process time)
- **Work type filter list** — the Display → Value pairs behind the dashboard's filter, `All`
  and `Bugs → Bug` out of the box

Nothing else is here on purpose: a setting that changes nothing is worse than a missing one.

### Settings you've already saved keep winning

Defaults only fill in what isn't saved. A browser that has used the app before keeps whatever
was set there, so a changed default doesn't reach it — **the `Bug` defaults above show up on a
fresh browser, or after "Reset settings to defaults"**, not on a browser still holding the old
`Defect` values.

Two renames have happened in the stored data, and both are handled on load so nothing has to be
re-entered:

- The defect-work-type setting was saved as `defectType` and is now `unplannedType`. An old
  saved value is carried across, so a team that had set it to `Incident` still has `Incident`.
  (The key kept its name when the charts went back to calling this "defects": the *value* is
  your data, a share link carries it, and there is no version negotiation on a share link that
  would let an older build understand a renamed key.)
- A `plannedLabel` setting existed, with an input and a saved value, but nothing on screen ever
  read it. It is dropped on load rather than left riding along in every backup and synced copy.

### Created dates and older versions of the app

Rows gained an optional created date (`k` on the wire, backup `version: 3`, `schema: 3` in the
saved and synced state). A row without one is left exactly as it was — no `k` key is written —
so a team that has never pasted a created date saves byte-identically to before.

One thing to know if you use sync: **a browser still running an older build will strip created
dates from the synced copy.** It hydrates only the fields it knows about and pushes the rest
back without them. That build also drops the `schema` marker, so a document arriving without
one when this device holds created dates is detectably that case, and the app says so in a
toast rather than losing the data quietly. The fix is to reload Flow Metrics on the other
device. There's deliberately no automatic merge — that belongs in the sync conflict dialog,
which is its own piece of work.
- The first version stored one team's rows under `td-rows`, with the team name in `td-settings`.
  Those fold into a single team the first time a newer version loads, and the old keys go.

## How the numbers are worked out

`derive()` in [index.html](index.html) is the only place any figure is computed. The parts
worth knowing:

- **Weeks start on Sunday.** Week keys are `YEAR-WW`, where the week containing 1 January is
  week 1. Written out by hand, because JavaScript has no week-number function.
- **Fortnights are anchored to a fixed date** — the first Sunday of 1970 — not to whatever
  window is on screen. Which fortnight a date falls in is therefore a property of the calendar,
  and switching from 3 months to 12 doesn't slide every bar one week sideways. Months are
  plain calendar months.
- **The axis snaps outward to whole periods.** A 3-month window starting on the 5th, grouped
  by month, plots the whole of that month. The window note states the dates you asked for; the
  chart draws complete periods, because half a bar is worse than a slightly wider window.
- **A part-finished last period is plotted and labelled, not dropped.** The data usually stops
  mid-period, so the final bar is genuinely lower and always will be. Dropping it would hide
  the most recent data — the first thing anyone looks at — and would disagree with what Jira
  says the team finished this month. Instead the window note and the tooltip say how much of
  the period is covered ("Last month covers 5 of 31 days").
- **Throughput is conserved when you regroup; net flow is not.** Regrouping can't lose a
  completion, because the axis starts at the earliest completed period by definition. It can
  change the *started* tally, because a coarser period reaches further back — a month begins
  on the 1st where a week begins on a Sunday — and sweeps up starts the weekly axis never
  saw. Net flow moving when you change the grouping is the metric behaving correctly, not a
  bug.
- **The date window trims the axis, not the data.** "Show data for most recent 3 months" moves
  where the chart starts; every item still counts toward the weeks that remain. That's
  deliberate. The axis also never starts before the team's first completed period — a window
  longer than the data doesn't pad empty periods in front, which would read as real
  zero-throughput periods and dilute the tile averages for a young team.
- **Cycle time** is `completed − started`, floored at 0, with same-day items taking the
  configured value. **Lead time** is `completed − created` by exactly the same rules — the
  whole wait, including the time an item sat in the backlog before anyone picked it up. Lead
  time is therefore always the longer of the two, and the gap between them is queue.
- **Flow efficiency is pooled, and it is an approximation.** Per period it is
  `total cycle time ÷ total lead time` over the items completed in it — not the average of the
  per-item ratios, which lets one item raised and closed the same day report 100% and drown
  out a real one. It is *not* the textbook measure: a true flow efficiency needs the time an
  item spent in each individual status, so it can tell working from waiting *inside* the
  in-progress span. A plain Jira export doesn't carry that, so this counts everything between
  start and finish as working time and reads high when work sits blocked mid-flight. It still
  answers the question that matters most — how much of the total wait was queue.
- **A created date alone is not enough to keep a row.** An item raised and never picked up is
  backlog, not flow; counting it would make the intake series track grooming rather than work.
  The rule is unchanged: no completion and no start, no row.
- **Unfinished items count as work started, and nothing else.** They move net flow but add
  nothing to throughput, the bug rate or the cycle-time average, all three of which key off
  a completion. Dropping them — which an earlier version did — made net flow read
  systematically too positive.
- **A period with no defect work scores 0%**, not blank; a period with no completions has an
  average cycle time of 0.
- **A team whose items are all still in progress has nothing to chart yet, and the dashboard
  says exactly that** — "Nothing finished yet", not a complaint about the filter. The filter
  message only appears when a filter really is what's excluding everything.

Net-flow bars use the theme's accent for positive and `--serious` for negative — deliberately
not the red/green pair, because the coaching goal is "keep around zero", so neither sign is
good or bad.

## Cleaning up old data

Years of history make every paste, backup and share link heavier without telling you anything
new. **Your Data → Clean up old data → Remove old items** drops the items older than a cutoff
you choose:

- **How much to keep** — the last 3, 6 or 12 months, the last 2 or 3 years, or everything from
  a date you pick yourself.
- **Which teams** — any combination. Teams with nothing in them can't be picked.
- **Unfinished items** — off by default, and worth leaving off. An item with no completion date
  is still in progress however old its start date, and it still counts as work started on the
  net flow chart.

**The completed date decides.** An item that took a year to finish but finished inside the
window stays — the start date never drags it out.

**Relative options count back from the newest item in the data, not from today**, which is the
same anchor the dashboard's own date window uses. It matters: without it, loading last year's
export and picking "the last 12 months" would leave you one press from deleting all of it.
Whichever option you pick, the exact cutoff date is named before you commit.

Nothing happens until you press **Remove items**. Until then a running summary says how many
items would go and how many would stay, broken down per team when you've picked more than one,
and it calls out by name any team the cutoff would empty completely. The button stays disabled
while there's nothing to remove. There's no undo, so the dialog offers the same JSON download
as the Back up button — one press away from a deletion is exactly when a backup is worth having.

Removing items only removes items. The team itself survives, even if it ends up empty.

## Back up & restore

The **Back up** button in the header opens a dialog (the same shape as the sibling app's)
that writes one JSON file holding
every team, their work items and your shared settings — `team-dashboard-YYYY-MM-DD.json`. It's
a copy you keep, independent of this browser and of any Google account, and it's the only way
back from a cleared browser if you've never signed in.

**Restoring replaces everything.** You're shown what the file holds against what's already
here — *"Restore 2 teams and 3 items from this file? This replaces the 1 team and 0 items in
this browser"* — and nothing changes until you confirm. If you're signed in, the restored copy
is stamped as the newest and pushed, so it becomes what your other devices get.

A restored file goes through exactly the same sanitising as a copy arriving from the cloud
(`hydrateState`), so a hand-edited backup can't introduce anything a synced copy couldn't.
Before that, `isBackup()` checks the file is plainly one of ours: `hydrateState` is deliberately
forgiving and will turn `{}` into a valid empty dashboard, which is right for a damaged saved
copy and catastrophic for the wrong file picked out of a Downloads folder. Choosing a file that
isn't a backup is refused outright and leaves your data alone.

**Two things are deliberately not in the file:** your theme, and which team you were looking
at. Both are positions on this device rather than data — the same reason they don't sync.

## Sharing a read-only link

The **Share** button in the header builds a link that shows someone the teams you pick,
read-only — no sign-in, no way to change anything, and (ported from the sibling app) the
data travels **inside the link itself**: everything after the `#` never leaves the browser,
so the figures reach the recipient without GitHub Pages, Firebase or anyone else seeing
them. The payload is a trimmed copy — the chosen teams plus the shared settings, because
those drive every number on the charts — and never anything identifying.

The recipient sees a standing "Read-only view" bar, the dashboard only (no Your Data or
Settings tabs), and a link back to their own data. Nothing they do is saved, and nothing
already in their browser is touched — `save()`, `persist()` and `saveView()` are all
no-ops in a shared view, and sync never initialises. A link that arrives truncated (mail
apps do this) shows an error card rather than ever falling through to the viewer's own
data.

It's a **snapshot**: later edits don't appear in links already sent, and a sent link can't
be withdrawn — treat it like emailing a spreadsheet.

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
   paste it as the value of `FIREBASE_CONFIG`
6. **[console.cloud.google.com](https://console.cloud.google.com) → APIs & Services →
   Credentials** — open the OAuth 2.0 Client ID named *Web client (auto created by Google
   Service)*. Copy its Client ID into `GOOGLE_CLIENT_ID` in `index.html`, and under
   **Authorized JavaScript origins** add `https://eagleadams86.github.io` (and
   the exact localhost origin you serve from locally). Without the origin, Google rejects the
   token request with `origin_mismatch` and sign-in never starts.

   **Origins match exactly, port included.** `http://localhost` and `http://localhost:5000`
   are two different origins to Google, and neither covers `http://localhost:8080`. This
   project has `http://localhost`, `http://localhost:5000` and `https://eagleadams86.github.io`
   registered — serving locally on any other port means adding it here first.

### Why sign-in doesn't use Firebase's popup

Firebase's `signInWithPopup` opens the popup at `<project>.firebaseapp.com/__/auth/handler` and
only redirects on to Google from there. A proxy that blocks that first hop kills sign-in
outright — the popup dies with `ERR_TUNNEL_CONNECTION_FAILED` or the proxy's own block page,
and nothing in the app ever runs.

**The block is per hostname, not on `firebaseapp.com` as a whole**, which is worth stating
because the obvious conclusion is wrong. Measured on one corporate network on a single day:

| Hostname | Result |
|---|---|
| `teamdashboard-6723f.firebaseapp.com` | blocked |
| `paptrack-6c817.firebaseapp.com` | blocked |
| `sprintvelocity-141b7.firebaseapp.com` | **reachable** |

Same sign-in code, same SDK, three projects created within days of each other — and the two
blocked ones aren't even the newest. Whichever way a filter categorises a given hostname is
outside our control and can change, so "the other apps are fine" is not evidence that this one
will be, and a sibling app working today doesn't mean it will work next month.

So sign-in uses **Google Identity Services** instead: a popup straight to `accounts.google.com`
returns an OAuth access token, which Firebase exchanges for a session via
`signInWithCredential`. Same Google account, same Firestore data, same rules — only the doorway
changed, and `accounts.google.com` is a mainstream Google domain that isn't blocked in the same
way.

This is why `GOOGLE_CLIENT_ID` exists as a separate constant: it is *not* part of
`firebaseConfig` and can't be derived from it.

**Reachability, if sign-in fails on a restricted network.** The app needs
`accounts.google.com`, `www.gstatic.com`, `firestore.googleapis.com`,
`identitytoolkit.googleapis.com` and `securetoken.googleapis.com`. Opening each in a browser is
the quickest way to find which one a proxy is blocking. Note that an existing session keeps
refreshing against `securetoken.googleapis.com` alone, so an app can look fine for weeks on a
network where a *fresh* sign-in would fail — test in a private window.

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

The one forward-looking risk is that enabling some other API in this project later would widen
what the key can reach. The rule that follows: if a new Google API is ever turned on here,
restrict the key at the same time — Google Cloud console → **APIs & Services → Credentials →
the browser key → Application restrictions → HTTP referrers**, limited to
`eagleadams86.github.io`.

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
scripts plus Firebase's CDN and Google's sign-in client, and network access to the handful of
endpoints sync uses plus `api.github.com` (the Recent-changes box). **Any new external
endpoint has to be added there too**, or it fails only in production.

`accounts.google.com` appears in `script-src`, `connect-src` *and* `frame-src` because sign-in
goes through Google Identity Services — see [Why sign-in doesn't use Firebase's
popup](#why-sign-in-doesnt-use-firebases-popup) above.

Note for anyone comparing against the sibling apps: this one no longer allows `apis.google.com`
and no longer produces the `gen_204` telemetry noise those apps document, because the auth
iframe that fired it is gone.

`apis.google.com` stays out of `script-src` deliberately, and the sync module uses
`initializeAuth` rather than `getAuth` so the SDK never asks for it. `getAuth()` always wires in
`browserPopupRedirectResolver`, and on Safari, iOS and mobile browsers the SDK initialises that
resolver during startup — which loads `apis.google.com/js/api.js` to build the gapi iframe that
carries `signInWithPopup` and `signInWithRedirect` results back to the page. This app calls
neither, so nothing consumed it; the visible symptom was a CSP error in the console on phones
and in Safari, and nothing else. Token refresh, sign-out and the cross-tab session all run
elsewhere in the SDK and never touch the resolver. Dropping it costs
`signInWithPopup`/`signInWithRedirect`/phone sign-in, which now raise `auth/argument-error`; if
one is ever wanted, pass `browserPopupRedirectResolver` to that call rather than reverting to
`getAuth()`.

## Tests

![tests](https://github.com/eagleadams86/team-dashboard/actions/workflows/tests.yml/badge.svg)

`tests.html` pins the pure functions by loading the real `index.html` in a hidden iframe — no
copies to drift. It must be served over `http://localhost`, not opened as a file. The iframe is
marked `data-td-tests`, which the sync module checks so no sign-in session ever boots inside
the harness.

The suite also runs on every push:
[`.github/workflows/tests.yml`](.github/workflows/tests.yml) serves the folder, opens
`tests.html` in headless Chromium and fails the build if the summary goes red or the page
throws — so a suite that only ever ran when someone remembered to open it can't silently rot.

Beyond the metrics it covers `detectColumns()` (a leading key column, the dates either way
round, header names beating position, a free-text summary not being mistaken for the type),
work-in-progress handling — including the net-flow miscount stated as a test, and a WIP row
whose *empty completed cell comes first*, which a line-trim once shifted into a completed row —
the week straddling New Year (whose cycle times once vanished from the chart and tile), quoted
CSV fields, the share-link codec round trip on both wire formats, and the sync
boundary: `sanitizeTeams()` (ids arriving from the cloud end up in `data-` attributes and
`<option value>`, so anything not `[A-Za-z0-9_-]{1,64}` is replaced, names are capped, types
coerced to strings), `normalizeSettings()`
(including the `defectType` → `unplannedType` carry-over, and junk filter entries or a junk
same-day value being coerced rather than trusted), `hasData()`, the predicate the
"empty never beats data" rule rests on, and `isBackup()`, the guard that stops the wrong JSON
file being restored over real data.

Two promises get pinned end to end rather than function by function:
`buildSharePayload()` — a share link holds **only the chosen teams** plus the shared settings,
and nothing else (no theme, no sync uid, no view state) — and `migrate()`, the v1 upgrade,
exercised the way it really runs: the old `td-rows`/`td-settings` keys are planted, a second
hidden copy of the app boots, and the suite checks the single team it folds them into.

Cleanup gets the same treatment, since it's the one action with no undo: `cleanupDoomed()` is
pinned on both sides of the cutoff (the cutoff day itself is kept), on work in progress with
and without the box ticked, and on the case that would hurt most — an old start date with a
recent completion, which must stay. `cleanupAnchor()` is pinned to the newest date in the data
rather than today. One end-to-end check runs the whole reference sample past a 3-month cutoff
and asserts every item is either kept or removed, never both.

The expectations are pinned to a fixed 141-item sample, right down to the weekly throughput
series, `10.2857…` days average cycle time in week 1, `−5` net flow in week 1, and the 19.92%
average bug rate in the defect rate chart title. Change the maths and the suite says so.

## Files

| File | |
|---|---|
| `index.html` | The whole app — inline CSS and JS |
| `chart.min.js` | Chart.js 4.4.1, vendored (no CDN) |
| `theme.css` | Copy of the palette from [claude-theme-pack](https://github.com/eagleadams86/claude-theme-pack); also inlined into `index.html` so it works over `file://` |
| `tests.html` | Pure-function tests |
| `privacy.html` | Privacy policy — exists because other people may sign in |
| `firestore.rules` | Checked-in copy of the deployed security rules |
| `.github/workflows/tests.yml` | Runs `tests.html` headless on every push |
| `favicon.ico` | Tab icon |

Four themes — Midnight (default), Dark, Light, Sepia — from the shared theme pack. Palette
changes belong in the pack, not here. 
