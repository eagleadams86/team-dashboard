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
| **Flow** — how long work takes | How long does an item take, and how reliably? | Cycle time (average and 85th percentile); lead time |
| **Delivery** — how much comes out | What pace do we deliver at, and is it steady? | Items completed per period; net flow (completed minus started) |
| **Health** — the state of the board | How loaded is the board, and how stale? | Work in progress; aged work; defect rate — defects resolved and defects raised |

Charts sit two to a row at any window wide enough for the pair. A group with an odd number of
them — Health, with three — leaves the last chart alone on its row: it keeps a single column's
width and sits **centred**, rather than stretching the full width. A chart drawn twice as wide as
the ones above it reads as the more important one, which it isn't, and its bars stop being
comparable with theirs at a glance. On a narrow window every chart is full width, so there is
nothing to centre.

**Group by week, 2 weeks or month.** The control sits beside the date window on the dashboard.
Weekly is the default and the finest grain; monthly smooths out the lumpiness that makes a
single week hard to read. The grouping also drives the last column of the Your Data table, so
the table and the charts always name the same period.

Each chart carries a dashed linear trend line, and four **summary tiles** above the tabs state
the window-wide figures — one for each dimension a kanban team can act on:

| Tile | Question it answers |
|---|---|
| **Completed per period** | What pace do we deliver at? (over whole periods only, see below) |
| **85th percentile cycle time** | What can I promise about the next item? (with the median beneath it) |
| **Work in progress** | How much is in flight right now? |
| **Aged work** | What has been in flight too long — i.e. what do I do today? |

Those are the four flow metrics a kanban team is normally coached on, and the last two are the
only figures here that describe the board as it *stands* rather than as it performed. Cycle time
reads as the **85th percentile rather than the average** deliberately: cycle times are skewed, so
the mean lands where most items beat it and a minority miss it badly — it is the one figure on
the page nobody can forecast with. The average is still a tile, beside the chart that plots both
lines.

Each group then adds a small tile row of its own, stating what its charts can't:

- **Flow** — average cycle time (pooled over the items in the window, so an empty week can't
  drag it down) and average lead time.
- **Delivery** — **steady delivery**, the band most whole periods land in (15th to 85th
  percentile of the per-period counts); total **net flow**; and **started vs completed**, the two
  counts net flow is the difference of.
- **Health** — the ratio of work in progress to a month's throughput, and the defect rate.

Net flow and the defect rate sit with their charts rather than in the headline row because both
are readings on the period just gone, and neither says what to pick up this morning. Net flow in
particular says which *way* work in progress is moving, where the headline tile says where it
stands — and a net figure of +2 reads the same from 12 started and 10 completed as from 2 and 0,
which is why the pair of counts sits beside it.

The headline four stay visible whichever group is open. The tiles are deliberately neutral: this
app has no targets, so no tile is ever coloured "good" or "bad". There being exactly four in the
headline row, they go four-across on a wide window and pair into a 2x2 on a narrower one — never
three and a stray fourth; the group rows vary in count and are laid out by `auto-fit` instead.

### Whole Periods, and Which Figures Use Them

Your data usually stops part-way through a period — the export runs to a Tuesday, the month it
lands in has three weeks left. That last bar is genuinely lower than a full period's and always
will be. The chart still plots it and the window note still says how much of the period it
covers ("Last week covers 4 of 7 days"), because dropping it would hide the most recent data,
which is the first thing anyone looks at.

**The two figures that describe what a typical period looks like skip it**: *completed per
period* and *steady delivery*. A period that hasn't finished happening is an incomplete
observation rather than a slow one, so averaging it in reports a pace the team never worked at,
and letting it set the band's low edge reports a floor they never delivered at. Both tiles name
the count they used ("over 13 whole weeks"), both read "—" when no period has finished yet, and
the ⓘ on each says so.

**Everything else counts it**, because nothing else is a per-period count:

- **Cycle time and lead time** average over *items*, not periods. An item that finished on the
  Tuesday took exactly as long as it took.
- **The defect rate** is the *pooled share* — defects completed over everything completed in the
  window, not the average of the per-period rates the chart plots. Averaging the rates weighed a
  quiet week's one-of-one the same as a busy week's four-of-ten, and counted a week in which
  nothing finished as a 0% that was never observed at all. A period that stops early still
  counts every completion it does have — a share is scale-free.
- **Net flow, started and completed** are *totals* of what happened in the window, not claims
  about a typical period.
- **Work in progress and aged work** are read at a point in time, and that point is already
  clamped to the end of your data (see below).

The line is drawn at "is this a count per period?", not at "is this important". It does mean two
tiles in the same row can be counted over different sets of periods — steady delivery over whole
ones, net flow beside it over all of them — which is why each tile states the count it used.

Each chart card heads with **what it is** — CYCLE TIME, THROUGHPUT, AGED WORK — and carries the
detail on a second line beneath: which grouping, which series, the window average. The name is
identifiable at a glance across a room in a stand-up; the sentence under it answers "plotted
how?". The **ⓘ button** sits on the name and opens a plain-English note on what the figure means
and which direction is good.

## One of a Pair

This app shares its look and behaviour with
[Sprint Predictability](https://eagleadams86.github.io/sprint-velocity/), its sibling: the same
sticky header, button tabs (with arrow-key navigation), summary tiles, ⓘ help dialogs,
read-only share links, theme picker and footer. **Each app's header carries a link to the
other**, next to the title — one click either way, from anywhere on the page — and both
still cross-link at the foot of the page, where a **How it works** link to that app's README
also sits. If a chrome rule changes in one app, it should change in the other too — with one
noted exception: how many tile columns there are. This app's headline row always has exactly
four tiles and so states its column counts outright, while the sibling's tile groups vary in
size and are still laid out by `auto-fit` — as this app's own per-group tile rows are.

## Teams

Each team keeps its own list of work items; the picker in the header chooses which one the
dashboard is showing. Add, rename and delete teams from the **Teams** button beside that
picker — a dialog, the same shape as the sibling app's Teams & PIs. Settings are shared by
every team — one place to say what a "defect" is.

The picker only appears once there are **two or more** teams: with one team it is not a
choice. It is part of a wider rule — nothing shows until there is something behind it, so a
first run is the paste box and its instructions, and nothing else. The **Loaded data** card,
the **Clean up old data** card and the **Append to existing** / **Clear this team's data**
buttons all appear the moment rows exist (`renderEmptyState()`).

Which team you're looking at is a position on *this* device and deliberately isn't synced:
switching team on the laptop shouldn't yank the phone to the same team.

## Getting Your Data In

The **Your Data** tab takes a paste from Jira, a CSV or any other export and loads it into the
team currently selected in the header. Paste the export as it comes — a Jira export looks like this
and works unchanged:

```
Key        Created     In Progress   Resolved    Issue Type
DAE-1064   4/02/2026   4/27/2026     5/11/2026   Story
DAE-1058   4/09/2026   4/28/2026                 Story
DAE-1491   7/28/2026   8/5/2026                  Story
```

The **Created** column is optional and unlocks lead time. Without it everything else works
exactly as before, and that chart says so on its face rather than disappearing.

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

**Only dates and a short type label are ever saved.** The paste is read for its dates and its
work type on the spot and then discarded — ticket keys, summaries and everything else in the
export are never stored. The work type itself is held to a short category label ("Story",
"Bug", "Tech Debt"): a cell longer than a label — a summary that landed in the wrong column,
say — is dropped whole rather than truncated, so no fragment of a work system's text can end
up in the saved or synced copy. The same guard runs again whenever a saved copy, cloud
document, backup or share link is read back in. There are deliberately no free-text or
comment fields anywhere in the app.

**The few labels you do type are capped at 120 characters where they're written**, not just
on the next load — team names, the defect and cycle-time words, and both columns of the work
type filter. `maxlength` stops ordinary typing past the cap but not a paste, and the object
you type into is the one that goes to `localStorage` and the cloud, so the cap is applied at
the keystroke as well as in `normalizeSettings()`. Typed numbers (the ageing threshold, the
same-day value) are clamped at zero the same way.

### What Happens to Bad Data

A bad *cell* costs you that field, not the whole row — with one exception, because every metric
keys off a completion date.

| What's wrong | What the row does |
|---|---|
| Completion date unreadable | **Row skipped** — nothing can be plotted without it |
| Completion date empty | Kept — it's work in progress |
| Start date unreadable | Kept, without a start date |
| Created date unreadable | Kept, without a created date |
| Start date later than the resolution | Kept, and the **start date dropped** |
| Ticket created after its work had started | Kept, and the **created date dropped** |
| No completion and no start | Dropped — untouched backlog says nothing about flow |
| A date that cannot exist (31 Feb, month 13) | Rejected rather than silently rolled over |

**Every problem row is listed back with its line number and only the cells the app reads** —
the work type and the three dates, never the whole pasted line. The line also carries the
ticket key and can carry a summary, and neither belongs on screen any more than in storage;
the line number is how you find the row in your export, which still has every identifying
detail — where it belongs. Long lists are capped, but the count above each list is always the
true total.

### The Three Dates Are Not Equally Trustworthy

`created ≤ started ≤ completed` is the one hard ordering these dates have, and **which end of it
breaks tells you something specific** — because in a normal Jira setup:

- **Created** is written by Jira and cannot be edited.
- **Resolved** is written by Jira and cannot be edited.
- **The start date** is set by automation when work moves to In Progress, but *can* be adjusted
  by hand afterwards.

So the start date is the only one of the three that can be wrong, and both ordering checks are
really checks on it.

**Start date later than the resolution.** Work cannot finish before it starts, so this is a bad
adjustment however it was meant. It has to be caught rather than tolerated: cycle time floors a
negative span at zero, so a row like this would otherwise contribute a **zero-day cycle time
that never happened** and drag the average down where nobody could see it. The start date is
dropped — the row still completed, so it still counts for throughput; it just no longer claims
to know when it started.

**Ticket created after its work had started.** Since Created can't be edited and the automation
stamps the start on the transition, `created ≤ started` holds by construction — so a violation
means someone moved the start date by hand, almost always to record that work truly began before
the ticket existed. That makes the adjusted date the *better* estimate of when work started, so
**cycle time keeps it in full**. Lead time doesn't: it measures the wait from a request to its
delivery, and here the work was already under way when the request was made, so there is no such
wait to measure. Keeping it would also produce a lead time shorter than the same row's cycle
time.

A handful of those is ordinary. A large share is either a mismapped column or a team that
routinely raises tickets after starting the work — different problems, both worth knowing, and
the app says so rather than calling it a few odd rows.

There's no inline row editing — to fix something, correct it at the source and paste again.

## Settings

Everything the charts depend on, shared by all your teams:

- **Defect work type** — the exact text in your Type column that means "defect"
  (`Bug` by default). Anything blank, or not matching, counts as ordinary planned work.
- **Aged after (days)** — how long an item can sit in progress before the Aged work chart
  counts it (`14` by default; worth keeping under a month).
- **Same-day cycle time** — what an item that starts and finishes on one day is worth
  (`1` day: it still occupied someone for that day)
- **Word for defects on charts** (`Defect` by default — singular, because it reads as
  "Defect rate") and the **word for cycle time** (Cycle Time / Time in Process / TiP /
  In Process Time)
- **Work type filter list** — the Display → Value pairs behind the dashboard's filter. Out of
  the box: `All`, `Defects → Bug`, `Spikes → Spike`, `Stories → Story`, `Tasks → Task`, so the
  filter is useful on the first paste rather than after a trip back here. Spikes especially —
  they are timeboxed investigations rather than delivered value, and taking them out of
  throughput changes the picture

Nothing else is here on purpose: a setting that changes nothing is worse than a missing one.

## What Isn't Here, and Why

**Blocked time** — how long an item couldn't move because something was in its way. A plain
Jira export doesn't carry it: "Flagged" is a state, not a duration, and reconstructing the
duration needs the issue's status history. To add it you'd need a **Time in Status** export —
one row per issue per status with entry and exit timestamps, or per-status day totals — plus a
mapping of which statuses count as blocked. That's a second paste surface and a status-category
setting, so it's deliberately out of scope rather than half-built.

**Flow efficiency** — what share of an item's total wait was actually spent working. This app
carried an approximation of it for a while: `cycle time ÷ lead time`, i.e. the share of the
raised-to-delivered span that the item was in progress. It was removed, because that only
measures the queue *before* work starts. On a team that picks work up the day it's raised — as
the team this was built for does, its start date set by automation on the Ready → In Progress
transition — the figure pins at ~95% and never moves, while the waiting that actually matters
happens *inside* the in-progress span: in review, blocked, waiting on an environment. Measuring
that needs the same **Time in Status** export as blocked time, plus a mapping of which statuses
count as working. Until then the 85th percentile and aged work are the honest way to see the
same problem. Half a metric that always reads 95% is worse than no metric at all.

**Value delivered** and **story readiness** need data that doesn't exist in a flow export at
all — business outcomes, and how often a story was rewritten after being picked up. Neither is
derivable from dates.

### Settings You've Already Saved Keep Winning

Defaults only fill in what isn't saved. A browser that has used the app before keeps whatever
was set there, so a changed default doesn't reach it — **the values above show up on a fresh
browser, or after "Reset settings to defaults"**, and nowhere else. That is why the defaults can
be changed freely: they are the starting point for a new browser, not a setting pushed onto an
existing one.

Two renames have happened in the stored data, and both are handled on load so nothing has to be
re-entered:

- The defect-work-type setting was saved as `defectType` and is now `unplannedType`. An old
  saved value is carried across, so a team that had set it to `Incident` still has `Incident`.
  (The key kept its name when the charts went back to calling this "defects": the *value* is
  your data, a share link carries it, and there is no version negotiation on a share link that
  would let an older build understand a renamed key.)
- A `plannedLabel` setting existed, with an input and a saved value, but nothing on screen ever
  read it. It is dropped on load rather than left riding along in every backup and synced copy.

### Created Dates and Older Versions of the App

Rows gained an optional created date (`k` on the wire, backup `version: 3`, `schema: 3` in the
saved and synced state). A row without one is left exactly as it was — no `k` key is written —
so a team that has never pasted a created date saves byte-identically to before.

**Created dates are never dropped silently.** If a synced copy arrives with none and this
device has some, the app asks before taking it — the same treatment as another device clearing
all its data — and cancelling keeps them *and* pushes them back up, so the other device gets
them too. Two ways that happens:

- a browser on an **older build**, which hydrates only the fields it knows and pushes the rest
  back without them (it also drops the `schema` marker, so this case is named in the prompt);
- a current build that has simply **never been given a Created column** — it pushes a perfectly
  valid copy that just has no created dates in it.

**Which copy is newer is decided by the Firestore server's clock, not by either device's.**
The synced document carries a `serverAt` server timestamp, and each device records the
`serverAt` of the version it currently holds and compares incoming writes against that.

It used to compare two devices' wall clocks — the pushing device wrote its own `Date.now()`
and the receiver compared that against its own last-edit stamp. Nothing reconciled the two, so
a laptop and a virtual desktop a few minutes apart could each conclude the other's newer change
was older; worse, the "loser" then pushed its staler copy over the newer one on its next
sign-in, so an edit could be lost on *both* devices. `updatedAt` is still written for any build
that predates this, and a device falls back to it until it has seen one server timestamp —
one push from each device is enough to leave the fallback behind for good.

The document also carries a `writerId`, so a device can recognise its own write coming back:
a server timestamp only resolves once the server has it, so your own push returns on the
listener as something that would otherwise look like news from elsewhere.
- The first version stored one team's rows under `td-rows`, with the team name in `td-settings`.
  Those fold into a single team the first time a newer version loads, and the old keys go.

## How the Numbers Are Worked Out

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
  the period is covered ("Last month covers 5 of 31 days"). It is excluded from the two
  per-period figures that would be distorted by it — the completed-per-period average and the
  steady delivery band — and counted everywhere else; see
  [Whole Periods](#whole-periods-and-which-figures-use-them) for why the line falls there.
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
  zero-throughput periods and dilute the tile averages for a young team. At the other end it
  runs to the **newest date in the data, completion or start**: a week in which things started
  but nothing finished yet is plotted with a true zero, so the started tally, net flow and the
  work-in-progress tile all see it — and "as of" on the tiles means the date it says.
- **Cycle time** is `completed − started`, floored at 0, with same-day items taking the
  configured value. **Lead time** is `completed − created` by exactly the same rules — the
  whole wait, including the time an item sat in the backlog before anyone picked it up. Lead
  time is therefore always the longer of the two, and the gap between them is queue.
- **The 85th percentile is the number to forecast with**, which is why it, rather than the
  average, is the cycle time figure in the headline row. 85% of the items completed finished
  within it, so it is a promise you can make about the next one. An average is not: on a
  right-skewed distribution — which delivery data always is — the mean sits well above the
  typical item and well below the slow tail, describing nothing. The gap between the two lines
  is how unpredictable the work is, and predictability is usually worth more to whoever is
  asking than raw speed.
- **Percentiles are nearest-rank, never interpolated.** The figure is always a duration some
  real item actually took, so "85% finished within 17 days" is a true statement about work you
  shipped. The window figure pools every item in the window rather than averaging the
  per-period percentiles, because a percentile of percentiles is not a percentile.
- **The same 85 governs the delivery band.** The steady-delivery tile reads the 15th and 85th
  percentiles of the per-period counts, mirrored around the middle so one convention serves
  both metrics: 85% of periods delivered at least the low figure, 85% at most the high one, and
  the middle 70% sat between them. It answers the half of the Delivery question an average
  can't — two teams averaging five a week are not the same team if one runs 4 to 6 and the
  other 0 to 15, and only the second needs explaining to whoever is asking for a date.
- **Started vs completed is the pair net flow hides.** A net figure of +2 reads identically
  whether it came from 12 started and 10 completed or from 2 and 0, and those are a team at
  pace and a team barely moving. Started counts every item with a start date whether or not it
  finished, so the pair also says how much of what was picked up in the window is still open.
- **A created date alone is not enough to keep a row.** An item raised and never picked up is
  backlog, not flow; counting it would make the intake series track grooming rather than work.
  The rule is unchanged: no completion and no start, no row.
- **Work in progress and aged work are states, not counts.** Every other metric counts events
  over a period; these two are read at a single moment — each period's last day — and
  reconstructed from the same start and completion dates as everything else, so you get a
  history rather than just today's number. That's also why they're drawn as bars: a line
  between two readings would imply a value in between, and there isn't one.
- **The reading point is clamped to the end of your data.** The last period usually runs past
  it, and letting the clock tick into the future would age every open item a few days for
  free. The clamp is also what makes the last bar of each series equal the tile above it.
- **Aged means older *than* the threshold.** An item exactly 14 days old is due today, not
  overdue.
- **The WIP-vs-throughput ratio** compares work in progress against a month's completions,
  however the charts are grouped. The coaching rule is to keep it under 0.5, nearer 0.25 for
  most teams — that lives in the ⓘ text and nowhere else. Nothing turns a colour when you
  cross it, because this app states figures rather than grading them, and a rule of thumb from
  a coaching email is not a target you set.
- **One caveat on aged work:** the clean-up tool's option to *also remove unfinished items*
  deletes long-running work in progress, which is exactly what this chart counts. History
  before a clean-up like that will read low. Removing completed items — the normal case —
  doesn't affect it, because those had already left the board.
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

## Cleaning Up Old Data

Years of history make every paste and backup heavier without telling you anything new.
**Your Data → Clean up old data → Remove old items** drops the items older than a cutoff you
choose. It is *not* the way to shorten a share link — the share dialog has its own history
window for that, and it deletes nothing:

- **How much to keep** — the last 3, 6 or 12 months, the last 2 or 3 years, or everything from
  a date you pick yourself.
- **Which teams** — any combination; **Select all** takes the lot, and the count above the
  list says where you are. Teams with nothing in them can't be picked.
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

## Back Up & Restore

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

### Starting Again

Folded away at the foot of the same dialog, under **Start again**, is **Delete all data** —
the whole-board version of Clean up old data. It's behind a fold on purpose: the one
irreversible action in the app shouldn't sit a mis-click away from Download backup.

Pressing it opens a confirmation of its own that says exactly how much is going ("This
deletes 2 teams and 3 items"), warns you when you're signed in that the copy in your Google
account goes too, and offers the same JSON download as a last chance to keep any of it.

**Your settings and your theme survive.** Starting fresh isn't asking to lose the type
labels, filters and ageing threshold you spent time tuning — those are configuration, not
data. What's left is exactly what a brand-new browser gets: one empty team to paste into.

## Sharing a Read-Only Link

The **Share** button in the header builds a link that shows someone the teams you pick,
read-only — no sign-in, no way to change anything, and (ported from the sibling app) the
data travels **inside the link itself**: everything after the `#` never leaves the browser,
so the figures reach the recipient without GitHub Pages, Firebase or anyone else seeing
them. The payload is a trimmed copy — the chosen teams plus the shared settings, because
those drive every number on the charts — and never anything identifying.

This dialog carries more than any other, so on a screen 760px or wider it opens **820px wide
with its two choices side by side**, matched in height, rather than stacked. That is the point of the extra width —
widening a single column only makes the lines longer. It takes the dialog from 764px tall to
621px, which is the difference between opening already scrolled on a laptop and not. Below that
it stacks and behaves as before, and no other dialog changes: the ⓘ help window is a paragraph
of prose, and a wider measure makes prose harder to read, not easier.

**How much history** decides how far back the link reaches, in the same words the clean-up
dialog uses: everything, the last 3, 6 or 12 months, the last 2 or 3 years, or everything from
a date you pick. Nothing is deleted — this only trims what rides in the URL, which is what
makes a long history shareable without having to delete it first. Months count back from the
newest item in the data (same anchor as the clean-up tool and the dashboard's own window), and
an **Unfinished items** box, off by default, decides whether items with no completion date go
along regardless of how old their start is. The line under the link reads `219 of 600 items —
from 18 Nov 2023` so the cost of a longer window is visible before you send it; a window that
would leave nothing at all says so.

The recipient sees a standing "Read-only view" bar, the dashboard only (no Your Data or
Settings tabs), and a link back to their own data. Nothing they do is saved, and nothing
already in their browser is touched — `save()`, `persist()` and `saveView()` are all
no-ops in a shared view, and sync never initialises. A link that arrives truncated (mail
apps do this) shows an error card rather than ever falling through to the viewer's own
data.

A trimmed link carries its cutoff as `from`, and the read-only bar says "Covers work from
18 Nov 2023 onward" — a windowed copy must never read as the team's whole history. The date
comes out of a link, so it's re-validated before it's shown, like everything else in there.
`from` is written only when a window was used, so an untrimmed link is byte-identical to the
ones the app built before, and a build that predates the field ignores it: the link still
opens, just without the line saying where the history starts.

It's a **snapshot**: later edits don't appear in links already sent, and a sent link can't
be withdrawn — treat it like emailing a spreadsheet.

## Cross-Device Sync (Firebase, Free Tier — Optional)

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

### Why Sign-In Doesn't Use Firebase's Popup

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

### About the `apiKey` in This File

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

Two rules in the push are load-bearing, both learned from a real outage in the sibling app.
**The cloud copy goes through JSON, exactly as the local save does** (`forCloud()`): `setDoc()`
walks the live object and Firestore rejects the *whole document* if it finds a single
`undefined` anywhere in it, where localStorage would simply drop that key — so a local copy
can look perfect while nothing reaches the cloud. This file's boundary rebuilds fresh literals
with concrete defaults and reaches no `undefined` today, and the tests pin that by *key*
(`x === undefined` passes whether the key exists or not); the round trip is there so the next
optional field can't quietly change it. And **`invalid-argument` does not mean "too big"** —
Firestore uses that one code for both an oversized document and a value it can't store, so the
"delete a team" advice appears only when Firestore's own message mentions size. A remedy that
destroys data must never be the guess.

## Running It

Single page, no build step, no accounts required. Serve the folder:

```bash
python3 -m http.server 8013
```

`index.html` no longer stands alone: the palette is linked as `theme.css` rather than
inlined, so opening the file off disk without `theme.css` beside it gives an unstyled page.
Copying both files to a folder and opening `index.html` over `file://` still works; a server
is simplest, and the tests need one anyway.

Your data lives in `localStorage`, and leaves the browser only if you sign in.
[`privacy.html`](privacy.html) is the privacy policy — keep it and its effective date current
if what the app stores, or where it sends it, ever changes. The footer links to it, and to
this README on GitHub as **How it works**, for anyone wanting more than the in-app ⓘ dialogs.

A Content-Security-Policy `<meta>` at the top of `index.html` restricts the page to its own
scripts plus Firebase's CDN and Google's sign-in client, and network access to the handful of
endpoints sync uses plus `api.github.com` (the Recent-changes box). **Any new external
endpoint has to be added there too**, or it fails only in production.

`accounts.google.com` appears in `script-src`, `connect-src` *and* `frame-src` because sign-in
goes through Google Identity Services — see [Why Sign-In Doesn't Use Firebase's Popup](#why-sign-in-doesnt-use-firebases-popup) above.

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

**It only runs on localhost, and enforces that itself.** `file://` is deliberately not treated
as local: it has no hostname, and the empty string used to sit in that allow-list on the
reasoning that the suite couldn't run there anyway — which sent it down the iframe branch, where
the frame silently fails to load and the page blamed the app. Opening it off disk now gets the
advice that fixes it.

 The suite is not read-only about
storage: it plants known state through `tdAdopt()`, and merely booting the app in the iframe
writes this origin's `td-*` keys. On localhost those keys are a scratch copy. But GitHub Pages
publishes every file in the repo, so `tests.html` is also live at
`/team-dashboard/tests.html` — where the same run would replace **real** saved teams with
two-item test data. A gate at the bottom of the script checks `location.hostname` against
`localhost` / `127.0.0.1` / `[::1]` and, anywhere else, refuses: it never creates the iframe,
explains why, and says how to run the suite properly. Nothing above that gate touches storage
on its own, so opening the published copy is now harmless.

(The alternative was keeping `tests.html` off the published site, via a Jekyll exclude or a
move into a subfolder. The guard was chosen instead because it is self-documenting and travels
with the file — a fork, a local copy, or a future host can't lose it.)

The suite also runs on every push:
[`.github/workflows/tests.yml`](.github/workflows/tests.yml) serves the folder, opens
`tests.html` in headless Chromium and fails the build if the summary goes red or the page
throws — so a suite that only ever ran when someone remembered to open it can't silently rot.
CI reaches it at `http://localhost:8013`, so the localhost gate lets it through; if that ever
changed, the run would time out waiting for a summary and fail loudly rather than skip.

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

The share window is pinned on all four of its promises: only rows inside it go into the link,
unfinished items stay unless the box is ticked, the app's own rows are **untouched** by
building a link, and a windowed link really does come out shorter than the whole-history one.

Cleanup gets the same treatment, since it's the one action with no undo: `outsideWindow()` is
pinned on both sides of the cutoff (the cutoff day itself is kept), on work in progress with
and without the box ticked, and on the case that would hurt most — an old start date with a
recent completion, which must stay. `historyAnchor()` is pinned to the newest date in the data
rather than today, and `windowCutoff()` on each shape of answer — including a half-typed custom
date, which must yield no cutoff rather than a guess. These three are shared with the share
dialog, so both dialogs sit on one set of tests. One end-to-end check runs the whole reference
sample past a 3-month cutoff and asserts every item is either kept or removed, never both.

The expectations are pinned to a fixed 141-item sample, right down to the weekly throughput
series, `10.2857…` days average cycle time in week 1, `−5` net flow in week 1, and the 19.92%
average bug rate in the defect rate chart title. Change the maths and the suite says so.

## Files

| File | |
|---|---|
| `index.html` | The whole app — inline CSS and JS |
| `chart.min.js` | Chart.js 4.4.1, vendored (no CDN) |
| `theme.css` | Copy of the palette from [claude-theme-pack](https://github.com/eagleadams86/claude-theme-pack); **linked** by `index.html`, `privacy.html` and `tests.html` — since 2026-08-18 it is not also inlined, so the palette lives in one place and a pack change reaches the app |
| `tests.html` | Pure-function tests |
| `privacy.html` | Privacy policy — exists because other people may sign in |
| `firestore.rules` | Checked-in copy of the deployed security rules |
| `.github/workflows/tests.yml` | Runs `tests.html` headless on every push |
| `favicon.ico` | Tab icon — the fallback a browser fetches from the site root on its own |
| `make_favicon.py` | Draws `favicon.ico` to match the inline SVG icon in `index.html` |

The icon is three weeks of flow side by side, on the midnight tile the whole app family
wears; the header shows the same mark. `make_favicon.py` (Pillow) keeps `favicon.ico` and
the page's inline SVG the same picture, rather than leaving a binary nobody can review in a
diff. Re-run it with `python3 make_favicon.py`, then bump the `?v=` on every `favicon.ico`
reference — browsers hold on to an icon for a long time.

Four themes — Midnight (default), Dark, Light, Sepia — from the shared theme pack. Palette
changes belong in the pack, not here. 

## Origins

The first version of this app was modelled on the **Team Dashboard v5** spreadsheet from
[Focused Objective](https://github.com/FocusedObjective/FocusedObjective.Resources), the
freely published collection of forecasting and flow-metrics tools by Troy Magennis. It is
worth a look in its own right, and so is the rest of that repo.

The metrics themselves belong to nobody: cycle time, lead time, throughput, net flow, work
in progress, aged work and the 85th percentile are standard Kanban measures that predate
the spreadsheet and are set out across the flow-metrics literature. What is here is an
independent reimplementation of them in HTML and JavaScript: the formulas, the layout and
every chart were built from scratch, and a handful of short field labels read the same only
because they name the same thing. It has since grown well past the original: any number of teams,
its own Flow / Delivery / Health grouping, a date window and period picker, read-only share
links, cross-device sync, four themes and a test suite.

## Ownership and Licence

Flow Metrics is an independent personal project by Charles Adams — built on personally owned
hardware, with a personally paid-for Claude subscription, in a personal GitHub account, and
syncing (when you turn it on) through a Firebase project he owns. No employer equipment,
funding or code went into it.

It holds no employer information either, and that is a property of the design rather than a
promise: there is no free-text field anywhere in the app, and the storage whitelist admits
only numbers, dates and short fixed labels. Text you paste in is parsed in the browser and
thrown away — ticket keys, summaries and comments are never stored, transmitted or
committed. Adding a stored field means adding it to that whitelist, or it is deliberately
stripped.

Share it freely: it is [MIT licensed](LICENSE), so anyone — including a company you work
for — may use, modify and redistribute it. Running it inside an organisation conveys no
ownership of it; permission comes from that licence, granted by the author as copyright
holder. [NOTICE](NOTICE) records this in full.
