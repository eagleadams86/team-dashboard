# Flow Metrics

Kanban flow metrics for as many delivery teams as you like, from nothing but a list of
completed and started dates. Single page, no build step, nothing to install.

**Live:** https://eagleadams86.github.io/team-dashboard/

The app is called **Flow Metrics** on screen. The repo, the Pages path and the
`app: 'team-dashboard'` marker inside a backup file all still say *team-dashboard* — renaming
any of those would break existing links and backups, so the rename is deliberately a
display-only one.

There are two ways to read the numbers: the **Dashboard**, which is one team in detail, and
**[All Teams](#all-teams-which-one-needs-you)**, which is every team side by side over one shared
window. Both are driven by the same work type filter, date window and grouping.

On the Dashboard the charts are grouped into four tabs — **by what the data means**, so the
measures that move together are read together:

| Group | Question it answers | What's plotted |
|---|---|---|
| **Flow** — how long work takes | How long does an item take, and how reliably? | Cycle time (average and 85th percentile); **every finished item, as a dot**; lead time |
| **Delivery** — how much comes out | What pace do we deliver at, and is it steady? | Items completed per period; net flow (completed minus started); **[raised, started, finished](#raised-started-finished-the-cumulative-flow-diagram)** — the cumulative flow diagram |
| **Health** — the state of the board | How loaded is the board, and how stale? | Work in progress; aged work; **[work item age](#work-item-age-what-to-do-this-morning)**, by workflow stage where your export says one; defect rate — defects resolved and defects raised; **[time in stage](#where-the-time-goes-time-in-stage)**, where the wait actually goes |
| **Forecast** — what that implies | When will this batch be done, and how much by a date? | Two distributions from ten thousand simulated runs, one per question |

The first three describe what already happened. **Forecast** is the only one that looks
forward, and it is the reason for collecting any of the rest — see
[Forecasting](#forecasting-what-the-pace-youve-had-implies) below.

Charts sit two to a row at any window wide enough for the pair. **Delivery holds three**, so its
last one — the cumulative flow diagram — is alone on its row: it keeps a single column's width and
sits **centred** rather than stretching the full width. The one card that isn't a chart, **time in
stage**, does span both columns, because a five-column table in half a row scrolls sideways on an
ordinary laptop. A chart drawn twice as wide as the ones above it reads as the more important one,
which it isn't, and its bars stop being comparable with theirs at a glance. On a narrow window
every chart is full width, so there is nothing to centre.

Any one of them can be **[filled to the window](#one-chart-filling-the-window)** with the ⤢ in
its corner, with the header still there above it.

**Choose how much history to show** — 1 month, **12 weeks (a PI)**, 3, 6, 9 or 12 months, All, or
**[Custom dates](#a-window-between-two-dates-you-type)**.
Every option but the PI is a number of calendar months; a planning increment is six two-week
sprints, so it is 84 days flat rather than three months rounded — a few days out of step with the
sprints it is made of would defeat the point of having it. It sits between *1 month* and *3
months* in the list, because that list is ordered by how much history it shows rather than by the
unit each option is written in.

One thing to expect: a 12-week window drawn as weeks usually carries **13 bars**, not 12. The
window is exactly 12 weeks of calendar, but its ends fall mid-week, so the first and last bars are
partial — which is true of every other window here too, and why the note above the charts says how
much of the last period it covers.

**Group by week, 2 weeks or month.** The control sits beside the date window on the dashboard.
Weekly is the default and the finest grain; monthly smooths out the lumpiness that makes a
single week hard to read. The grouping also drives the last column of the Your Data table, so
the table and the charts always name the same period.

Charts draw their data in the shared theme pack's **categorical colours** — `--series-1`, a blue,
for the measure, and `--series-5`, a rust, for the second series where a chart has one. They used
to draw in the app's accent, which is fine on Midnight and Light and wrong on the other two: on
Sepia and Dark the palette makes the accent the *body-text ink*, so a throughput line came out the
same colour as the writing around it and the dashboard read as black and grey. Trend and reference
lines stay muted grey on purpose — they are annotation over the data, not data.

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
- **Health** — the ratio of work in progress to a month's throughput, the age of the **oldest
  item still in progress**, and the defect rate.
- **Forecast** — the 85%-confident answer to each of its two questions, and the number of whole
  periods both were dealt from.

Net flow and the defect rate sit with their charts rather than in the headline row because both
are readings on the period just gone, and neither says what to pick up this morning. Net flow in
particular says which *way* work in progress is moving, where the headline tile says where it
stands — and a net figure of +2 reads the same from 12 started and 10 completed as from 2 and 0,
which is why the pair of counts sits beside it.

The headline four stay visible whichever group is open. The tiles are deliberately neutral: this
app has no targets, so no tile is ever coloured "good" or "bad". There being exactly four in the
headline row, they go four-across on a wide window and pair into a 2x2 on a narrower one — never
three and a stray fourth; the group rows vary in count and are laid out by `auto-fit` instead.

A tile is drawn on **the same surface as a chart card and a table** — one ground for everything
on the page, with a border and a left edge to lift it off the background, exactly as a card has.
It used to sit a shade apart, which in Sepia read as a tan band above cream charts and sorted the
dashboard into two tones that meant nothing. That edge went from 4px to **6px** in the same
change, and for the same reason: the tile used to be told apart by its fill, and now it is told
apart by the edge, so the edge has to be able to carry it.

### Typing Items In by Hand

Not everyone has a Jira, or knows how to get a report out of one. **Add an item** sits beside the
paste box on a first run, and **+ Add item** on the Loaded Data card once you have rows: one short
form — started, completed, work type, and optionally a created date, an item name, the stage it
is sitting in, and **how many days it spent in each of your stages**.

**Everything on the dashboard can be filled in from that form.** There is no chart, tile or table
here that needs an export — the stage day counts were the last thing that did, until 2026-08-22.

It also closes a gap the paste box never could: **press any row in Loaded Data to edit it, or
delete it.** Before this the card said "read-only — to correct a row, fix it in your source and
paste again", which is no answer at all when the source is your own memory.

Two things worth knowing:

- **The dates are date pickers, so there is nothing to guess at.** The ambiguous
  day-first/month-first question a pasted `1/3/26` raises does not arise here at all.
- **Press anywhere on a row** in Loaded Data to open it, not just its name — though a click that
  ends a text selection is ignored, so dragging a figure out to copy it still works.
- **An empty stage box is not a zero.** Leave a stage blank and that item simply says nothing about
  it; type `0` and you are saying it crossed that stage inside a day. The medians on the Time in
  Stage table only count the boxes you actually filled in, which is what keeps them honest.
- **A date in the future is refused**, in any of the three fields, and the message says why: every
  window on the dashboard is measured back from the newest date in your data, so one item dated
  next year would empty every chart on it.
- **A typed row and a pasted row are the same thing once saved.** Both cross the same guards — the
  work type capped and dropped whole if it is really a sentence, the item name kept only if it is
  the shape of an issue key. The one difference is that the form **refuses** a bad ordering rather
  than dropping the offending date: a paste is hundreds of rows from a system nobody here
  controls, and a form is one row with you looking straight at it.

### How Many Items the Window Covers

The window note under the date range reads **"14 weeks · 67 of 190 items (9 in progress)"** when
the picker is hiding history, and just "190 items" when it is not. Both numbers are worth having:
the first is what every figure on the screen is computed from, and the second is what the team
holds. Narrowing the window trims *weeks*, not rows — nothing is deleted — so without the pair the
note stated a count nearly three times what the charts under it were drawn from, directly beneath
the sentence naming the three months being shown.

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

**The forecast skips it too**, and for the strongest version of the same reason: it deals whole
periods out again at random, and a period that has not finished happening is a bad week that
never occurred. Dealing one in would teach the model a slump the team never had. It uses exactly
the set the completed-per-period tile does, so the two can never disagree about which periods
they describe.

The line is drawn at "is this a count per period?", not at "is this important". It does mean two
tiles in the same row can be counted over different sets of periods — steady delivery over whole
ones, net flow beside it over all of them — which is why each tile states the count it used.

Each chart card heads with **what it is** — CYCLE TIME, THROUGHPUT, AGED WORK — and carries the
detail on a second line beneath: which grouping, which series, the window average. The name is
identifiable at a glance across a room in a stand-up; the sentence under it answers "plotted
how?". The **ⓘ button** sits on the name and opens a plain-English note on what the figure means
and which direction is good.

## A Window Between Two Dates You Type

Every option in the window picker but one is counted back from the newest date in your data:
*the last three months*, *the last 12 weeks*. **Custom dates** is the one that isn't. Choose it
and two date boxes appear beside the picker; the figures are then read between exactly those two
dates.

It exists for the thing a rolling window structurally cannot do: **compare two fixed periods**.
Last quarter against the quarter before it. The three months either side of a reorganisation. The
period a change was supposed to help, read on its own terms rather than as part of a span that
keeps moving as more data arrives.

A few details worth knowing, each of which is there for a reason:

- **Choosing it doesn't change the picture.** The boxes are filled in with the window you were
  already looking at — the last three months of your data — so you start by editing a window
  rather than building one from nothing. A control that emptied the charts the instant you chose
  it would read as broken.
- **The end is clamped to your data.** Type a *To* of next month and the figures are still read
  as of the last date your export actually reaches. Everything in this app is read as of the
  newest date in the data rather than as of today, deliberately — work in progress and aged work
  are both read at the window's end, so an end date past the export would age every open item for
  free against data that stopped weeks ago.
- **Both dates are needed, and *From* must come before *To*.** Half a pair is the state you pass
  through on the way to typing the second date, so it means "no custom window" rather than an
  error — the note under the strip says so while it waits, instead of leaving two boxes that hold
  dates and appear to be ignored.
- **Neither box will take a date in the future**, the same rule every other date field here
  follows.
- **It reaches All Teams too**, and there it does the aligning the shared date exists for by
  construction: every team is read between the same two dates, however much or little data each
  of them has inside them.
- A window your data doesn't reach plots nothing, and says which dates it found nothing between
  rather than blaming the work type filter.

Which dates you're looking at is a position on *this* device, like the team you have picked: it
is not part of your data, so it stays out of backups and share links.

## One of a Pair

This app shares its look and behaviour with
[Sprint Predictability](https://eagleadams86.github.io/sprint-velocity/), its sibling: the same
sticky header, button tabs (with arrow-key navigation), summary tiles, ⓘ help dialogs,
read-only share links, theme picker and footer. **Each app's footer carries a button link to
the other**, at the right-hand end of the row that holds the **Privacy policy** and **How it
works** links. If a chrome rule changes in one app, it should change in the other too — with two
noted exceptions. **How many tile columns there are**: this app's headline row always has exactly
four tiles and so states its column counts outright, while the sibling's tile groups vary in
size and are still laid out by `auto-fit` — as this app's own per-group tile rows are. And **what
a tile is drawn on**: this app puts tiles on the same surface as its cards (see above), where the
sibling keeps them a shade apart so that its one *hero* tile can stand out from the rest by being
the card surface. It has a tile this app does not; the difference follows from that.

## Grouping Teams into ARTs

If you support teams across more than one Agile Release Train, you can group them. The
**Teams & Stages** dialog has an **Agile Release Trains** section: add one, then set each team's ART from
the picker in its own row of the table above. A team can be on one train or on none — being on
none is perfectly normal, and nothing forces you to use the feature at all.

**An ART is a label, never a level of maths.** Every figure in this app is worked out per team
and the All Teams view adds them up; grouping changes what you are looking at and never a single
number. What it does change:

- **All Teams gains a train picker** — *All trains*, each train by name, and *No ART* if any team
  is un-grouped. Everything below it follows: the four tiles, every row, and the summary row at
  the foot of the table, which reads **All teams on Payments ART** when you scope to one.
- The picker **says how many teams it is hiding**, the same way every other exclusion in this app
  says what it left out. A figure should never move for a reason that isn't on the page.
- With no filter, the table **groups by train** so a train's teams sit together, and each team
  carries its ART under its name. **The header team picker groups the same way**, so a list you
  know by eye reads the same in both places.

ARTs reorder with **↑** and **↓** like teams do, and that order is the order their groups appear
in — both in the header picker and down the All Teams table.

Deleting an ART is the cheapest delete in the app: it takes no team and no work item with it —
the teams that were on it simply go back to having none. The confirmation says so.

**Share links carry only the trains their own teams are actually on**, so sharing one team never
publishes the names of every train you support. Share a team that is on no train and the link
has no ART names in it at all.

## All Teams: Which One Needs You

The dashboard answers *how is this team doing?*. **All Teams** answers *which of my teams needs
me?* — which, before it existed, meant visiting eight teams in the picker and holding their
numbers in your head.

A chart of the whole train's throughput over time, then one row per team, one column per question
people actually scan for:

| Column | The question |
|---|---|
| **Completed** / **Per week** | Who is delivering, and at what pace? |
| **Throughput trend** | Which team is *changing*? |
| **85th cycle time** | Who is slow, and who is unpredictable? |
| **In progress** / **WIP vs month** | Who is overloaded? |
| **Aged** | Who has work going stale? |
| **Defect rate** | Who has a quality problem? |
| **Data to** | …and whose figures are worth trusting at all |

**Throughput trend** and **Data to** carry an ⓘ of their own, because they are the two columns
that exist only here — every other column is a dashboard tile laid on its side, and the tile
carries the note. Nine circles across one header row costs 250px of a table already tight for
width, which is the whole reason it is two and not nine.

**Throughput trend** deserves its own paragraph, because it answers something none of the other
columns can.
Every other figure here is a snapshot, so a team halfway down a decline reads exactly like a team
that was always that slow — and the chart above hides it, because one team's slide is another's
gain. The sparkline is that team's throughput across the window on screen, drawn from the same
fitted line the chart uses, with the signed figure beside it showing what the line rises or falls
by end to end. Sort by it to put the steepest fallers on top.

The signed figure is a **plain number** — `-1.1`, `+4.3`, `0.0` — so the column survives the trip
into a spreadsheet as something you can sort and average. It is written with an ordinary hyphen
rather than a typographic minus for exactly that reason: these tables are read off the rendered
page, so what is on screen is what lands in the CSV, and the one column whose whole point is its
sign is the last one that should arrive as text.

The trace is **scale-free** — normalised to its own range — so what it shows is the *shape*. Two
teams with identical traces can be delivering at very different rates; Per week beside it is the
magnitude. And check **Data to** before reading a fall as a slowdown: a team whose export
stopped three weeks ago has a trace that falls away for exactly the same reason it has a stale
date, which is a reporting problem rather than a delivery one. (The demo shows this on purpose —
Team Bare Export has both the steepest fall and the oldest export.)

A reload puts you back on **whichever tab you were last using** — all four of them. A remembered
tab that is no longer on offer (All Teams disappears below two teams) falls back to the dashboard,
as does anything unrecognisable in a hand-edited copy.

The page also **holds still while it loads**. This app is one 560KB HTML file that the browser
paints as it parses, with the script that fills it at the foot — so for about a tenth of a second
you used to watch an empty skeleton assemble and then everything pop in at once, and a reload on
Your Data painted the whole dashboard first and then swapped it out. The header shows
straight away, because everything in that row carries its final width in the markup; the rest
appears once, complete, on the tab you left it on. If the script ever fails outright the page
reveals itself anyway after two seconds, so a broken load is a visibly broken page rather than a
blank one.

There is deliberately **no line-per-team chart**. This view is written for somebody with eight
teams, the shared theme pack's categorical ramp stops at five, and eight lines on one card is a
spaghetti chart even where the colours exist. A column sits beside the numbers it explains and
scales to any number of teams.

**Press a column heading to sort by it.** Every numeric column runs worst-first on the first
press — most aged, longest cycle time — because the reason anyone presses a heading is to find
the outlier, not to admire the ordering. *Data to* runs the other way, since the interesting end
there is the oldest export. Press again to reverse, and **a third time to turn the sort off** and
get the default order back. A team with no figure in a column always sorts last, whichever way it
is running: a team with no data has not got the shortest cycle time in the train.

**Press a team's name to open its dashboard.** That is the move the whole view sets up — the
table says who needs looking at, and this is looking at them. The team you currently have
selected is marked in the table, so you can always find your way back to where you were.

If your teams are [grouped into ARTs](#grouping-teams-into-arts), a **train picker** appears
above the tiles and everything on the page follows it — including the summary row, which becomes
that train's own figures rather than the whole estate's with some rows hidden.

The tab appears once you have a **second team**, the same rule the team picker follows: with one
team there is no comparison to make.

### The Train's Throughput Over Time

The four tiles say where the train **is**; the chart under them says where it has **been** — items
completed per period across every team in scope, with the same dashed trend line every other chart
carries. It follows the train picker, the work type filter, the date window and the grouping, like
everything else on the page.

It plots **one series and one colour on purpose**. A line per team would need a palette of
distinguishable colours that the shared theme pack doesn't have, and inventing one here would put
this app's charts out of step with its siblings. The aggregate needs only the accent — and it
answers the question the tiles can't: *is the whole train's delivery steady?* Which team moved is
the table underneath.

One thing to watch: a dip can be **one team stopping** rather than the train slowing down. Check
the **Data to** column before concluding anything — a team whose export is stale looks exactly like
a team that stopped delivering.

### One Shared Date, and Why It Matters

Every row is read **over the same window and as of the same date** — the newest date any team
has. Without that, "the last 3 months" would mean a different three months in every row, and a
team that stopped exporting in June would show a healthy June quarter next to everyone else's
September one.

That is also why **Data to** earns a column. A team three weeks behind everyone else has three
weeks of zero throughput dragging its rate down and three weeks of extra ageing on everything it
has open — and none of that is visible in the numbers themselves. Team Bare Export in the demo
is nine days behind for exactly this reason: it reads slower on this page than on its own
dashboard, and the date column is the only thing that explains why. **Before drawing any
conclusion about a team, check its export is current.**

Freshness is a property of the export, not of a work type: filter to defects and *Data to* still
shows when the team last sent anything, not when it last had a bug. A healthy team with no recent
defects is not a stale team.

### The Bottom Row Is Derived, Not Added Up

The four tiles and the **All teams** row describe the whole train. Totals — items completed, work
in progress, aged work — really are the sum of the rows above them. The **85th percentile is
not**: the 85th percentile of eight teams is not the average of their eight percentiles, and a
summary row built that way would be quietly wrong in its most-read column. It is worked out over
every item any team completed, exactly as if the teams were one team.

That has a consequence worth knowing. Because it pools *items* rather than *teams*, the train
figure is weighted by how much each team delivers — so a large fast team holds it down while a
small team with a long tail sits well above it. On the demo the train reads 7 days while Team
Long Tail reads 23. Both are true. **Read the tile for a promise about work you haven't assigned
yet; read the column to find who needs help.** The tile cannot tell you a team is struggling,
and it isn't meant to.

### Teams With Nothing to Say

A team still gets a row when it has no figures — that is a finding, not an omission — but it says
what it can rather than showing a line of dashes. A team that has **started work and finished
none** in the window shows its work in progress and its export date, because "this team has
stopped finishing things" is precisely what someone scanning this table is looking for. A team
with no work items at all shows dashes throughout.

## Teams

Each team keeps its own list of work items; the picker in the header chooses which one the
dashboard is showing. Teams can be [grouped into ARTs](#grouping-teams-into-arts), in which case
the picker groups them the same way. Add, rename, reorder and delete teams from the **Teams & Stages**
button beside that picker — a name is edited in place, **↑** and **↓** move a team up or down,
and **×** deletes it. Each row also holds a **project id** — the letters at the front of that
team's issue keys, `DAE` for `DAE-1552` — which is what lets [one export covering several
teams](#pasting-several-teams-at-once) be pasted in one go and split between them. It is
optional, it changes no figure, and a team without one simply takes nothing from a split.

Each row also holds the two figures the team **sets** rather than measures: **WIP ≤**, how much
work it means to have open at once, and **85% ≤**, how long it means an item to take. Both are
covered under [your own limit and your own target](#your-own-limit-and-your-own-target) below.

The
order matters: it is the order teams appear in that picker and down
the All Teams table. That window also holds your [Agile Release Trains](#grouping-teams-into-arts)
and your [workflow stages](#where-the-time-goes-time-in-stage), and is
laid out to match the sibling app's **Teams, ARTs & PIs** — same width, a section per thing you
manage, each with its own *+ Add* button at the right-hand end of its heading. The third section
differs between the two apps, and that is the point: they share a shape, not a list of sections. Settings are
shared by every team — one place to say what a "defect" is.

The picker only appears once there are **two or more** teams: with one team it is not a
choice. It is part of a wider rule — nothing shows until there is something behind it, so a
first run is the [welcome card](#the-first-thing-you-see) and nothing else. The **Loaded data** card,
the **Clean up old data** card and the **Append to existing** / **Clear this team's data**
buttons all appear the moment rows exist (`renderEmptyState()`).

**The Dashboard tab follows the same rule**: it isn't there until something has data, and a
browser with nothing in it opens on Your Data. It was the last thing here still offering a page
of nothing — a tab whose entire content was a card saying there was no data yet. It asks about
**all** your teams rather than the one you're looking at, which is what keeps it from appearing
and disappearing as you move through the picker, and what leaves an empty team beside a full one
still able to say so. In a **shared view** it is never hidden: Your Data is taken away there and
the header's buttons with it, so hiding this one as well would leave a tab strip with nothing
in it.

Which team you're looking at is a position on *this* device and deliberately isn't part of
your data: it stays out of backups and share links for the same reason the theme does.

## The First Thing You See

With nothing recorded anywhere there are no tabs, no view controls and no panels — just one
card in the middle of the page:

> **Welcome to Flow Metrics**
>
> A flow clinic for your delivery teams: give it your work items — a completed date, a start
> date and a type — and it works out throughput, cycle and lead time, work in progress, and
> the age of everything still open…
>
> **Start Fresh** · **Load Sample Data** · **Restore a Backup**

**Start Fresh** opens *Your Data*, where you paste a report out of Jira or add work items one
at a time. **Load Sample Data** loads [the demo](#the-demo--trying-it-without-pasting-anything).
**Restore a Backup** opens the same [*Back Up & Restore*](#back-up--restore) window the ⇩
button does.

It writes nothing. There is nothing to create here — the figures come from a paste or from
typed items — so *Start Fresh* just puts the card away for this sitting and opens the tab that
takes both. Reload with still nothing entered and the card comes back, which is the truth
about where you are.

Before this the app opened straight onto the Your Data tab and its paste box, which answers
"how do I fill this in" to somebody who hasn't yet been told what the thing is. Every app in
the family now opens on this same card, in the same words and the same order — what the app
is, where the figures go, the three ways in, then a line for each button. The second paragraph
is the privacy claim the footer also makes, and the two must never disagree: this app has no
sync and no account, so it says so outright.

## The Demo — Trying It Without Pasting Anything

**Load sample data** isn't filler to fill the screen: it's this app's demo, and the rule is
that **every feature has to be reachable from it**. Three teams, about nine months of
made-up work items ending today, and one of the three deliberately short of a column.

The button is on the [welcome card](#the-first-thing-you-see) a first run opens on, and again
beside *Load pasted rows* on the Your Data tab you reach from it — and, since the Dashboard tab
is [hidden until something has data](#teams), those are the two places it can be met. Pressing it switches you to the dashboard. It
disappears once anything holds data, and so does the copy of it on the empty-dashboard card,
which from a working app would be a mis-click that quietly adds three teams.

It lands on **Team Long Tail**, because Team Healthy Flow's board is the prettier one and says
less — the reason this app reads the 85th percentile rather than the average is only visible
on a team that has a tail.

Each team is **named for the one thing it's there to show**, so the picker reads as a contents
page rather than a list of names you'd have to open one by one:

| Team | What it's there to show |
|---|---|
| **Team Healthy Flow** | The healthy board. Carries issue keys (`KFR-…`), as Team Long Tail does (`HRN-…`), so the charts have something to name their dots with — and the matching project id, so a multi-team paste has somewhere to route them. Short cycle times (p85 ≈ 6 days against a median of 4), four items in flight, none aged, a defect rate around 11%. Its export carries **stage times too**, and they read the healthy way round: about 62% of its measured time is spent building. It sets a **WIP limit of 6 and a 10-day target** and is comfortably inside both. The baseline the other two read against. |
| **Team Long Tail** | The board the metrics exist to catch. A long tail, so **p85 lands around 23 days against a median of 5** — the app's whole argument for reading p85 rather than the average, on one screen. Nine items in flight, **six of them past the 14-day ageing threshold** and its oldest well above its own 85% line on the work item age chart, and a defect rate about two and a half times Team Healthy Flow's. Its [stage times](#where-the-time-goes-time-in-stage) then say *why*: **more of its time goes on waiting to be reviewed and tested than on building it**, which no cycle time figure can tell you. Its export has both a *Ready for Code Review* and a *Code Review* column, so it also shows two statuses adding into one stage. It sets **the same limit of 6 and the same 10-day target Team Healthy Flow does** and keeps neither — which is the point of the pair carrying identical figures. |
| **Team Bare Export** | A newer team: four months of history, **no created dates, no issue keys, no Status column and no stage times at all**, so the lead-time chart's "add a Created column" face is reachable, the parse report's "no issue key in this paste" note is too, the charts' type-named tooltips have a team that shows them, and the date window has a team it visibly runs past. Its export also **stops nine days before the other two**, which is what gives the All Teams view's *Data to* column something to show — it reads slower there than on its own dashboard, and the date is the only thing that says why. It sets **no limit and no target**, which is how every browser starts and the only way the no-line, no-verdict face of those two is reachable. Also proves each team's data stands on its own. |

Team Healthy Flow and Team Long Tail also arrive with the **project ids their own keys are
built from** (`KFR` and `HRN`), so [pasting several teams at once](#pasting-several-teams-at-once)
works straight off the demo rather than only after three ids are typed in — and Team Bare
Export, with no keys, is the team the split's *takes nothing* line is about.

The demo also arrives with **four workflow stages set up** — Build, Review, Test and Deploy —
because a status is only ever read when a stage already lists it, so the demo has
to set them up before it pastes, exactly as you would. Team Healthy Flow and Team Long Tail
carry the columns and Team Bare Export carries none, so both faces of the
[Time in stage](#where-the-time-goes-time-in-stage) card are reachable, and both axes of the
work item age chart are too. Deploy is deliberately a
stage almost nothing sits in: a table where every row is a big number teaches nobody where to
look.

Team Healthy Flow and Team Long Tail also carry a **Status column**, so their age charts group
by stage. Team Long Tail's is the one to look at: three of its four oldest items sit in
**Test**, which names the
bottleneck in a way no cycle time figure can. One of its items is in *Compliance Review* — a
status the demo's stages deliberately **don't** list — so it lands in the **No stage** column
and the parse report says one item's status matched nothing. That is the demo showing you a real
part of a workflow you haven't set up yet, which is exactly what it will do on your own board.

The demo also puts **Team Healthy Flow and Team Long Tail on one train (Delivery ART) and
leaves Team Bare Export on none** — the smallest arrangement where every part of
[ARTs](#grouping-teams-into-arts) does something. The picker gets *All trains*, *Delivery ART*
and *No ART*; both groups have somebody in them; and scoping to the train visibly changes the
figures at the foot of the table. A train per
team would make grouping look pointless, and putting all three on one would leave *No ART* absent.

On **All Teams** the three read as a train with one obvious problem: Team Long Tail's 85th
percentile is three or four times the other two, it holds most of the aged work, and its defect
rate is the highest — while Team Bare Export's *Data to* column quietly explains why its
delivery rate looks worse there than on its own page.

The **work item age** chart reads differently on each of the three, which is what makes it worth
looking at from the demo: Team Healthy Flow has nothing past the threshold and every dot below
its own 85% line; Team Long Tail's oldest item has been in flight longer than its own 85th
percentile by a wide margin, which is the whole argument for drawing that line; and all three
carry enough work types in flight for the columns to say something.

All three teams have enough weekly history to **forecast** on the default 3-month window — Team
Bare Export, at four months, is the one that decides that — and Team Long Tail's spread is wide
enough that its 50%, 85% and 95% answers are days apart rather than all the same date, which is
the whole argument for reading a distribution instead of a single number. Switching **Group by**
to Month on that same window drops below the eight-period floor, so the forecast's "not enough
history" card is reachable from the demo too.

Every team carries all four work types, so the **work type filter** does something whichever
team you're on. The dates cover the **whole week**, not just weekdays, which is what makes the
**working days** setting reachable from the demo: turning it on visibly shortens Team Long
Tail's tail and drops two items out of its aged count. The span is long enough that **Clean up
old data** has real answers — a 3-month cutoff would drop items from all three teams, a 12-month
one from none — and that the 6, 9 and 12-month **date windows** each change the picture.

**The dates are counted from the day you load it**, so the demo is live whenever it's opened
rather than stale from the day it was written, and the work in progress is genuinely in
progress. The randomness is **seeded**: the same numbers every time, on every device, so it
can be pinned by a test and talked through twice.

Two things it deliberately doesn't demo: **bad rows and the parse report**. Those are
responses to input rather than properties of a dataset — you meet them the moment you paste
anything of your own — and baking permanent errors into the demo would leave every first run
showing a red note.

It asks before it loads and adds alongside anything you already have, with one exception:
the empty `My team` the app creates on a first run is dropped, but only if it's untouched —
still the only team, still empty, still under that name. To get rid of the demo afterwards,
use **Teams & Stages** to delete the three, or *Start again* in the Back up dialog.

The demo group in `tests.html` pins every finding in that table. **Adding a feature means
adding the data that demonstrates it, a row in this table, and a test** — a feature the demo
can't reach is a feature nobody you share this with will find.

## Getting Your Data In

The **Your Data** tab takes a paste from Jira, a CSV or any other export and loads it into the
team currently selected in the header. One export covering *several* teams goes in through
[**Paste several teams…**](#pasting-several-teams-at-once) instead, which splits it by the
project id at the front of each issue key. Paste the export as it comes — a Jira export looks
like this and works unchanged:

```
Key        Created     In Progress   Resolved    Issue Type
DAE-1064   4/02/2026   4/27/2026     5/11/2026   Story
DAE-1058   4/09/2026   4/28/2026                 Story
DAE-1491   7/28/2026   8/5/2026                  Story
```

The **Created** column is optional and unlocks lead time. Without it everything else works
exactly as before, and that chart says so on its face rather than disappearing.

A **Status** column is read too, once you have set up the
[workflow stages](#where-the-time-goes-time-in-stage) that name your statuses: each in-flight
item is filed under the stage it's sitting in, which is what puts stage on the work item age
chart's axis. Extra columns holding a **number of days per status** are read on the same
set-up. A column whose heading — or a cell whose value — matches nothing you've set up is
simply ignored, and always was.

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

**Only dates, a short type label and the issue key are ever saved.** The paste is read for
those on the spot and everything else is discarded — summaries, statuses, assignees, comments
and the rest of the export are never stored. Two guards do that work, and they are different
on purpose:

- The **work type** is held to a short category label ("Story", "Bug", "Tech Debt"). A cell
  longer than a label — a summary that landed in the wrong column, say — is dropped whole
  rather than truncated, so no fragment of a work system's text reaches the saved copy.
- The **issue key** is checked against the *shape* of a key rather than its length: up to ten
  letters or digits, a dash, up to six digits, and nothing else. `DAE-1552` passes;
  `Customer data export breaks on accented names` does not, and neither does anything
  carrying a space, a quote, an angle bracket or a second dash. There is no input that both
  passes this check and carries prose — which is exactly why a key could be stored where a
  summary field never will be.

Both guards run again whenever a saved copy, cloud document, backup or share link is read
back in. There are deliberately no free-text or comment fields anywhere in the app.

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
the work type and the three dates, never the whole pasted line. Not even the issue key, which
the app *does* store: a row reaches this list precisely because its columns look wrong, so the
cell the key would be read from is the one cell that cannot be trusted to hold a key. The line
also carries a summary, and that belongs on screen no more than in storage;
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

## Pasting Several Teams at Once

A real Jira export is usually a whole train, not one board. Splitting it by hand — filter, copy,
switch team, paste, repeat — is the chore that stops a dashboard being kept current, so
**Paste several teams…** on the Your Data tab takes the whole export in one go and routes each
row to the team it belongs to.

**The routing is the project id at the front of each issue key.** Each team is one Jira project,
so `DAE-1552` belongs to whichever team is set to `DAE`. You set that id once per team, in the
**Teams & Stages** window — or let the app fill it in for you: when a team with no id yet is given a
single-team paste whose keys are *unanimously* one project, that project becomes its id and the
paste report says so. Unanimity is the bar, not a majority: a paste that is 90% one project is a
question, not a fact.

The whole export is parsed **once**, as one export, so every team is read with the same column
map and the same date convention — detecting the columns per team would let one file be read two
different ways.

Three buttons, and the first of them writes nothing:

- **Check this paste** shows the plan — which teams the export splits into, how many items each
  would take, and how many each holds now. Nothing is loaded.
- **Split into teams** replaces the items in each team the paste names. A team the paste does
  *not* name is left exactly as it is. Where that would overwrite existing items it asks first,
  naming each team and what it stands to lose.
- **Append to each team** adds to what is already there instead.

**Anything the app cannot place is named, never guessed at** — a row in the wrong team's
throughput is a wrong number nobody can see, while a homeless row is a message on screen. There
are three ways a row can fail to land, and they have three different fixes:

| What the report says | What it means | The fix |
|---|---|---|
| *N project ids no team claims* | Rows for a project nothing answers to | One press creates a team for it, named after the id and with the id already set — or give the id to a team you already have |
| *N project ids are on more than one team* | Two teams share an id, so nothing can decide | Change one of them in **Teams & Stages** |
| *N items had no readable issue key* | Nothing to route by | Add a `Key` column to the export |

When something is still unplaced, the paste **stays in the box** — create the team, press
**Check this paste** again, and those rows are included. A paste with no key column at all is
refused with that reason rather than reported as a split into nothing.

The project id is a **label and an address, never a level of maths** — the same rule ARTs and
issue keys follow. Nothing counts, groups, filters or sorts by it. It also never travels in a
share link: someone reading a link has no paste box, and every key in the payload carries its
project at the front anyway.

## Settings

**A window off the header**, behind the ⚙ button at the right-hand end — beside Teams & Stages,
Back up and Share, and laid out the same way. It was the fourth tab until 22 Aug 2026, which put
a page you visit twice a year in a strip whose other entries are ways of *reading* your numbers.
Settings is a thing you go and set, like teams and backups, and all three of those were already
buttons.

Because it opens over the dashboard rather than replacing it, a change lands on the charts behind
it — rename the defect word and the chart titles follow while the window is still open.

Everything the charts depend on, shared by all your teams:

- **Defect work type** — the exact text in your Type column that means "defect"
  (`Bug` by default). Anything blank, or not matching, counts as ordinary planned work.
- **Aged after (days)** — how long an item can sit in progress before the Aged work chart
  counts it (`14` by default; worth keeping under a month).
- **Count working days only (Monday to Friday)** — off by default. On, cycle time, lead time
  and the ageing threshold skip weekends: an item started on a Friday and finished on the
  Monday takes one day, not three. It is one switch for all three, because a screen mixing the
  two measures would be unreadable, and every chart and column that states a duration re-labels
  itself to say which days it means. **Public holidays are not known to the app** and still
  count as working days — a holiday list would be per-country and per-year, and this app
  deliberately stores no text of that kind. Throughput, net flow, work in progress and the
  defect rate are counts rather than durations, so they don't move.
- **Same-day cycle time** — what an item that starts and finishes on one day is worth
  (`1` day: it still occupied someone for that day)
- **Word for defects on charts** (`Defect` by default — singular, because it reads as
  "Defect rate") and the **word for cycle time** (Cycle Time / Time in Process / TiP /
  In Process Time)
- **Work type filter list** — the Display → Value pairs behind the dashboard's filter. Out of the
  box just two: `All`, which is the locked no-filter row, and `Defects → Bug`, which is paired
  with the defect type above so the filter and the defect rate agree without being told to.
  **Add the types your own board uses** with *Add a type* — the parse report names the work types
  it found in your paste, so you can copy them straight across. It used to ship Spikes, Stories and
  Tasks as well; they were guesses at somebody else's board, and on a team whose types read
  Feature, Chore and Incident they were three filters matching nothing, which reads as broken data
  rather than as a setting nobody has set

Nothing else is here on purpose: a setting that changes nothing is worse than a missing one.

## Your Own Limit and Your Own Target

Two figures a team **sets** rather than measures, both optional and both **empty out of the box**:

- **WIP ≤** — how much work this team means to have open at once.
- **85% ≤** — how long it means an item to take: the promise the 85th percentile is read against.

They live in **Teams & Stages**, on the team's own row, and **not** in the Settings window
beside it — which is the one design decision here worth stating. Every setting in this app is shared by every team, and
can be, because each describes how a *figure is worked out*: what counts as a defect, what a
same-day item is worth. These two describe a team's own board. A limit of eight means something
different to a team of three and a team of twelve, and a promise is made by the people who have
to keep it.

What they do:

- The **limit** is drawn flat across the work in progress chart, and the *Work in progress* tile
  says whether today is inside it and by how much: *limit 6 — over by 3*.
- The **target** is drawn on both scatter charts — every finished item, and work item age — and
  the *85th percentile* tile says *target 10.0 — met* or *not met*. It is compared with the
  percentile rather than with the average deliberately: a target is a promise about the next
  item, which is the one question an average cannot answer. On the age chart it means something
  slightly different and equally useful — an item still open above that line has already blown
  the promise, and knowing that this morning beats reading it next month.

**Neither changes a single figure.** They are what the figures are compared *to*, which is why
leaving both blank costs nothing: the app states the numbers and does not judge them, exactly as
it did before these existed. That is also why nothing is set by default — a limit the app picked
would draw a line across your chart claiming you had agreed to it.

**Nothing turns a colour.** The verdict is a sentence on the tile, and the bars over a limit are
the same colour as the bars under it. This app states figures rather than grading them, its
palette has nothing on the red-green axis to grade with, and a period over a limit is something
to look at rather than a failure to mark.

Both **travel in a share link**, so the person you send it to sees the same lines you do. Both are
**per team**, so the All Teams table — which compares teams against each other rather than against
their own promises — deliberately doesn't carry them.

### The Target Is Not the Ageing Threshold

These two read almost the same on screen — **85% ≤ 10 d** on a team's row, and **count an
in-progress item as aged after 10 days** in Settings — and they answer different questions:

| | **85% ≤ N d** (per team) | **Aged after N** (Settings, shared) |
|---|---|---|
| Looks at | Work that has **finished** | Work that has **not** |
| Asks | Did 85% of what we delivered get through in N days? | How long can something sit open before we want to see it? |
| Default | Not set | 14 |

**The threshold usually wants to be the lower of the two, and that is the part worth acting on.**
If your promise is ten days, an item that has already been open ten days has *missed* it — being
told so is a post-mortem, not a warning. Flag it at six and it is still something you can swarm on,
split, or unblock. Aged work is the one chart here that can tell you about a miss before it
happens, and the threshold is what decides whether it does.

Picking the lower number off your own data beats guessing: if your median cycle time is 4 days and
your 85th percentile is 10, then anything sitting at 6 or 7 is already unusual for you.

Going the other way is a real choice too. On a board carrying a lot of genuinely long work, a tight
threshold flags everything and the chart becomes noise you stop reading — raising it above the
target turns it into an escalation list rather than a nudge list. And setting them equal is
coherent if what you want is the literal reading, *show me anything already past what we promised*.
It just tells you about work you can no longer save.

One structural note: the target is **per team** and the threshold is **shared by every team**, so
with more than one team they cannot all match anyway. A promise is made by the people who keep it;
the threshold is closer to a house convention.

## What Isn't Here, and Why

**Blocked time** — how long an item couldn't move because something was in its way. A plain
Jira export doesn't carry it: "Flagged" is a state, not a duration, and reconstructing the
duration needs the issue's status history. Half of what that needed
[now exists](#where-the-time-goes-time-in-stage): a Time in Status export is read — or the days
are typed in — and they land against stages you named. What's still missing is a way to say **which of your stages is
blocked time** rather than working time — which is a decision about meaning, not a parse, and
it hasn't been built. Set up a stage for your blocked statuses and the table will at least show
you how much of the wait they account for.

**Flow efficiency** — what share of an item's total wait was actually spent working. This app
carried an approximation of it for a while: `cycle time ÷ lead time`, i.e. the share of the
raised-to-delivered span that the item was in progress. It was removed, because that only
measures the queue *before* work starts. On a team that picks work up the day it's raised — as
the team this was built for does, its start date set by automation on the Ready → In Progress
transition — the figure pins at ~95% and never moves, while the waiting that actually matters
happens *inside* the in-progress span: in review, blocked, waiting on an environment.
[Time in stage](#where-the-time-goes-time-in-stage) now shows that waiting directly — it is
exactly what Team Long Tail's row in the demo is for — but turning it back into a single efficiency
percentage needs each stage marked as **working or waiting**, and that flag doesn't exist. The
table is arguably the better answer anyway: it says *where* the wait is, where a percentage only
says how much. Half a metric that always reads 95% is worse than no metric at all.

**Value delivered** and **story readiness** need data that doesn't exist in a flow export at
all — business outcomes, and how often a story was rewritten after being picked up. Neither is
derivable from dates.

**A forecast weighted by item size**, and one that starts from what is already in progress.
Both are real refinements and both are deliberately out for now. Sizing would need a field this
app doesn't store and would reintroduce the estimating the forecast exists to avoid; crediting
work already under way would need a rule for how far along an in-progress item is, which is the
same status-history problem blocked time has. Counting whole items from a standing start is the
conservative reading of both, and a wide spread is the honest signal that items on this board
are not comparable.

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
  read it. It is dropped on load rather than left riding along in every backup for ever.

### Created Dates and Older Versions of the App

Rows gained an optional created date (`k` on the wire, backup `version: 3`, `schema: 3` in the
saved state; the working-days setting later took both markers to `4`, ARTs to `5`,
the issue key to `6`, the per-team project id to `7`, workflow stages to `8`, the per-row
current stage to `9` and the per-team [limit and target](#your-own-limit-and-your-own-target)
to `10`). A row without one is left exactly as it was — no `k` key is written —
so a team that has never pasted a created date saves byte-identically to before. **The issue key
(`i` on the wire) follows exactly the same rule**: absent unless there is one, so a team whose
export has no key column saves byte-identically to before that field existed, and the first save
after upgrading doesn't rewrite the whole stored document. **The project id follows it too** — a team
without one writes no `projectId` key at all, so a browser that never splits a paste stores
exactly what it stored before the feature existed.

**Stage times follow the same rule**: no `g` key on a row until there are day counts to put
in it, and no `stages` list on the document until you set one up, so a browser that never uses
the feature saves exactly what it saved before it existed. **So do the limit and the target**: a
team that has set neither writes neither key, and both are re-typed in seconds if an older build
ever drops them — which is why they are not on the list of fields the app stops and asks about.

The limit and the target **do travel in a share link**, unlike the project id: they are drawn on
the charts a link exists to show, and a link without them would give the reader a different
picture from the sender's. An older cached build simply drops both and draws the charts without
the lines.

**Created dates, issue keys and stage times are never dropped silently.** A backup saved by a build older
than the one that added a field simply has none of it in the file. It restores without
complaint, and the column is gone — and since [sync was
removed](#cross-device-sync-was-removed-2026-08-20) there is no second copy anywhere to get it
back from. So a restore that would lose them **asks first**, in one prompt covering all three
fields, and Cancel means nothing is restored at all rather than "restored, minus a column".
ARTs and project ids are deliberately *not* in that prompt: a train's name and a project id are
one word re-typed in a dialog, where a column of day counts pasted per item is not.
The boot version check doesn't cover this: that fires on a copy from a *newer* build, and this
one is older.

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
  configured value — **half a day out of the box**, so an item opened and closed inside one day
  stays distinguishable from one that genuinely took a full day. Change it in Settings; a browser
  that already has a value keeps it. **Lead time** is `completed − created` by exactly the same rules — the
  whole wait, including the time an item sat in the backlog before anyone picked it up. Lead
  time is therefore always the longer of the two, and the gap between them is queue.
- **Days are calendar days unless you turn working days on.** Flow metrics measure the wait the
  customer actually had, and the customer's weekend isn't free — so calendar days are the
  default and Monday-to-Friday is the deliberate choice. Working days are counted with a weekday
  ordinal rather than by walking a span a day at a time, so a two-year lead time costs the same
  as a two-day cycle time; the ordinal steps by one on each weekday and stands still over a
  weekend, so the difference between two of them *is* the working days between the dates. A span
  that falls entirely inside a weekend is zero working days and takes the same-day value, which
  is the same statement that setting always makes. The ageing threshold moves with it: 14
  working days is nearly three calendar weeks, so items age later and the Aged work count drops.
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

## Raised, Started, Finished: the Cumulative Flow Diagram

The third card in **Delivery**, and the only chart here that shows work arriving and work leaving
in the same picture. Everything the team holds is stacked at the end of each period, in three
bands:

| Band | What it is |
|---|---|
| **Finished** (bottom) | Delivered by that date |
| **In progress** (middle) | Started and not finished — the same figure the work in progress chart plots |
| **Raised, not started** (top) | Raised and still waiting to be picked up |

**Read the bands, not the lines.** The middle band's *thickness* is work in progress, so a band
that widens from left to right is work piling up faster than it leaves — whatever the throughput
tile says, and visible weeks before the cycle time chart catches up with it. The bottom band's
*slope* is delivery: flat means nothing finished that period. Two edges running parallel is a team
in balance, which is the shape to want; it is also the shape that says a forecast can be trusted.

Three details, each of which is a decision rather than an accident:

- **The finished band starts at zero on the left edge.** What the team delivered *before* the
  window isn't stacked underneath it — with nine months of history under a three-month window,
  that would put 130 items in the bottom band and leave the two bands that matter as a sliver at
  the top of the card. Nothing else moves for it: a band is the gap between two curves, so
  subtracting the same figure from all three leaves every thickness exactly as it was. The
  in-progress band is still a real count of open work, not just of work opened inside the window.
- **The top band needs a Created column**, and is left off entirely without one rather than drawn
  as a flat zero claiming there is no backlog — the same stance the lead time chart takes on the
  same column. Team Bare Export in the demo is the two-band version.
- **An item with no start date** was never observably in progress, so it goes straight into the
  finished band on the day it closed rather than being given a spell in the middle one.

The middle band is worked out a different way from the work in progress chart beside it — a
subtraction of two cumulative counts, against a walk over the items — and a test pins the two as
equal. If they ever disagree, one of them is wrong.

## Every Finished Item: the Spread, Not the Average

Beside the cycle time chart sits the same measure at a different resolution: **one dot per
finished item**, at the time it took, over the week it finished. The line chart averages within
each period — which is exactly what hides the one item that took five months.

This is the only view in the app where a **single item is a thing you can point at**. A dot far
above the rest is a conversation, and the week it sits over tells you which one to have.

The two lines across it are this team's own finished work: half of it came in under the lower one,
85% under the upper one. They are the **same two lines the [work item age](#work-item-age-what-to-do-this-morning)
chart draws**, in the same words, so the pair reads together — this shows where finished work
landed, that shows where open work has got to.

**What you are looking for is the spread, not the average.** A tight band means the next item is
predictable. A long tail means it is a lottery however good the typical case looks — and it is
exactly what makes the [forecast](#forecasting-what-the-pace-youve-had-implies) wide. On the
demo, Team Healthy Flow's dots sit in a band under 14 days while Team Long Tail's run to 48: the
same argument the 85th percentile tile makes, in a picture.

Dots are drawn translucent, so several items finishing on one day at the same speed show as a
darker mark rather than as one. The alternative — nudging dots sideways to separate them — would
be a lie about when something finished.

An item that finished with **no start date** has no cycle time, so it gets no dot rather than one
at zero. If nothing in the window has a start date the card says so instead of drawing an empty
grid.

## Where the Time Goes: Time in Stage

Cycle time says an item took eleven days. It cannot say that seven of them were spent waiting
for someone to review it. **Time in stage** does, and it is the one card on the dashboard that
is a table rather than a chart — five stages is five numbers, and a bar chart of five numbers
says less than the numbers do.

It reads **the window and the filter**, like everything else on the screen: what finished inside
the dates you picked, plus what is open now. The card's own title says how many items that is, and
it is the same figure the window note above states. (It shipped reading every row the team held,
which made it the one card that did not move when the picker did — one month, three months and all
data gave the same medians under a note that had just said which three months were being shown.)

### Two Exports, One Set-Up

Stages read **two different kinds of export**, and you set them up once for both:

| What your export has | What you get |
|---|---|
| **A Status column** (where each item is now) — an ordinary Jira export | The work item age chart grouped by **stage**: what is sitting in each part of the workflow, and how long it has been there |
| **A Time in Status export** (a column per status, holding days) — usually a marketplace add-on | The **Time in Stage** table below: how long work typically waits in each stage |
| **Neither** — you type the days in yourself | The same **Time in Stage** table. Every stage you set up gets a box on the work item form |

Most people have the first and not the second. That is fine — the first is the one that answers
*where is the work stuck*, and it needs nothing installed. And if you have neither, the third row
is not a consolation prize: the table reads typed figures and pasted ones identically, because they
are the same figures once saved.

### You Name the Stages. Your Export's Status Names Are Never Stored

This is the part worth reading even if you skip the rest.

A **stage** is a part of your workflow you want to measure the wait in — *Build*, *Review*,
*Test*. You create and name them under **Teams & Stages** in the header, and against each one you type
the **Jira statuses that feed it**, separated by commas. Several statuses can feed one stage:
a workflow with both *Ready for Code Review* and *Code Review* is one Review stage as far as
the flow is concerned. Those same statuses are matched against a **Status column's values** and
against a **Time in Status export's headings**, so one set-up serves both — and a board that
later gains durations needs nothing re-typed.

Paste an export with a **Status** column and each in-flight item is filed under the stage its
status matches. Paste a **Time in Status** export — one row per issue, one column per status,
each cell a number of days — and the days land in the stage each status is matched to, several
columns adding together where several statuses feed one stage.

**Or type the days in.** Once a stage exists it gets a box on the Add/Edit Work Item form, so a
board kept by hand — or a couple of figures read off a Jira screen without exporting anything —
fills this table exactly as an export does. Leave a box empty for a stage you have no figure for;
that is different from typing `0`, which says the item crossed it inside a day. The days are
**calendar** days either way, which is what a Time in Status export counts and what the card says
on its face — the working-days setting governs the three durations this app measures itself, and
cannot honestly be applied to a single total someone else worked out.

**The status names — in your headings and in your Status column's cells — are matched while the
paste is being read, and then thrown away with the rest of it.** What is saved is the stage name *you* chose and a
number. Every other field this app stores is guarded by asking whether a regex can tell it
from a sentence — a key can, a project id can. **A status cannot**: "Fix the login bug on
prod" is twenty-five characters of letters and spaces, which is every shape a status label
has. So the safety here is not a guard on the value; it is that the value is never stored.

That is also why **there is no button that picks the status names up out of your export**, even
though the app has just read them and it would save you the typing. One click that copies
work-system text into permanent storage is the thing this design exists to avoid.

Matching ignores capitals and punctuation — `In-Progress` and `In Progress` are the same
status — but it is **exact, never a partial match**. An alias of `Testing` will not quietly
swallow a *Waiting on Testing Env* column and add somebody's environment queue to your test
time. If two stages list the same status, the app says so as you type rather than picking one.

**Deleting a stage takes its figures with it, and the confirm counts them both ways** — the
time items spent in it, and the items sitting in it right now, which on an ordinary Status-only
export is all there is. No work item is deleted, and re-pasting the same export brings the
figures back.

### Reading the Table

| Column | What it says |
|---|---|
| **Items** | How many items have a figure for *that* stage — not how many have stage data at all. |
| **Median days** | The typical wait in that stage. |
| **85th percentile** | The one to plan against, exactly as it is for cycle time — and a real duration some item actually took, never an interpolation. |
| **Share of measured time** | That stage's days as a share of **all** the stage time measured. |

**The share is of measured time, not of cycle time**, and the difference matters. A status
export counts calendar days in every status you asked about, including ones that sit outside
the started-to-finished span this app calls cycle time — so a share of cycle time could come
out above 100% on perfectly ordinary data. A share of what was measured is self-consistent
whatever your export covers.

**These are calendar days whatever the working-days setting says**, and the card title says so
in its own words. That setting governs the three durations the app works out itself, from dates
it holds. These are worked out by Jira, from a status history the app never sees, and there is
no honest way to re-measure a single total Monday to Friday.

Stages appear **in the order you arranged them in**, not biggest first: a workflow has a
direction, and that order is the one thing you already know how to scan. Only stages that
actually carry figures get a row. The table copies and downloads like [every other table of
figures](#taking-a-table-off-the-page).

### One More Thing the Status Column Fixes

A Status column is a short repeated label — which is exactly what the app's work-type detector
hunts for, and *Ready for Code Review* is short enough to pass as a work type. Before the app
knew what a Status column was, an export without clear headings could quietly file its statuses
as work types. Naming the column takes it out of that guess, whether or not any stage matches
what's in it.

Only work **still in flight** gets a stage. Every export says *Done* against everything it has
ever closed, and a finished item's current status says nothing about flow — so those are
skipped rather than filed under a stage you don't have.

### What the Parse Report Tells You

After a paste it says which column it read as the current status and how many items were filed
under a stage, and it names which columns were read as which stage — **by position and by your
stage name**, never by the heading or the cell out of your export, because this report has never
echoed a pasted cell.

**Columns are separated by a tab, a comma, or two or more spaces.** A single space is not a
separator in general — a work type is *Tech Debt* and a date is *21 Jan 2015*, and both contain
one — but a paste that yields no columns at all is retried on single spaces and kept if that finds
a column of dates. So `1/1/26 1/1/26 Story` typed out by hand works, while a lone column of
*21 Jan 2015* dates still reads as one column.

If nothing loads, the note says which of the two happened: an empty box gets "paste some rows
first", and a box with rows in it that produced nothing says so and names the likely cause,
rather than telling you to paste rows you are looking at.

**An ambiguous date order announces itself.** With Auto-detect on, the order is read off the data
— `21/01/2015` can only be day-first. When *nothing* in the paste settles it, as in a set of dates
that are all 12 or under, the app falls back to day first **and says that it guessed**, with the
picker to change. The difference is not cosmetic: `1/1/26` to `1/3/26` is two days read one way
and fifty-nine the other.

If items had a status **no stage answers to**, it says how many. It does not say what they were:
that is work-system text, and the count is what tells you your aliases are wrong rather than one
row being odd. It counts only rows that were actually **loaded** — an untouched backlog item has a
status and no dates at all, so it is dropped before it gets here, and counting those made the note
read "400 items had a status no stage answers to" on a set-up whose spellings were perfect. If nothing matched, it says so and points you at the Teams
window. If a stage's alias named a column the dashboard already needs — aliasing `Created`, say
— the date wins and the report tells you which stage lost, rather than leaving you with a stage
that silently reports nothing.

Cells it cannot read as a plain number of days are counted per column and left out. The app
reads `3` and `3.5`; an export written as `3d 4h` or `12:30` needs asking for in days.

## Work Item Age: What to Do This Morning

Every other chart on the Health tab is a count. **Work item age** is the one that names things:
each item still in progress plotted at the age it has reached so far, in a column for its work
type.

It is the chart to run a stand-up off. The aged work chart beside it says *how many* were stale
at the end of each period; this one says *which ones are stale now, and by how much*.

### The Three Lines Are the Point

A dot on its own says an item is 23 days old, which means nothing without something to compare
it against. So three lines cross the chart:

| Line | What it is |
|---|---|
| **half took under N** | The median of this team's own finished work |
| **85% took under N** | The 85th percentile — the same figure the headline tile states |
| **aged after N** | The ageing threshold from Settings |

The middle one is the one that matters. An item above it has **already taken longer than 85% of
everything this team has ever delivered** — it is not merely old, it is outside the range of
work that finishes normally, and it is very unlikely to be the exception. That is a much stronger
thing to say in a stand-up than "this looks like it's been there a while", and it comes from the
team's own history rather than from anyone's opinion.

The lines are labelled where they are drawn rather than in a legend: a legend entry costs
vertical space out of a 300px card, and it costs a lookup — matching a dash pattern at the top of
the card to a line in the middle of it. Only the two dot shapes get a legend, because a shape does
need a key.

Each label sits in a small opaque panel, centred on its own line. That is what keeps the dashes
from running through the words, and what separates two labels when the lines are close together —
an ageing threshold of 14 against an 85th percentile of 13 is an ordinary board, and without the
panels those two labels landed on top of each other.

### Columns Are Workflow Stages — or Work Types

**If your export has a Status column, the columns are the stages you set up.** That is the
canonical version of this chart, and the question people actually walk up to a board with:
*what is sitting in each part of the workflow, and how long has it been there?* A cycle time
figure can tell you work is slow. This tells you it is slow **in test**.

Stages appear in **the order you arranged them**, left to right, so the axis reads the way your
workflow does — not busiest-first, because a workflow has a direction and that order is the one
thing you already know how to scan. Only stages holding something in flight get a column; an
empty one is a gap in the axis rather than information. Each tick carries its count —
**Review (4)** — so the chart also answers "how many are sitting there".

Items whose status matches none of your stages land in a **No stage** column at the right-hand
end. That is worth looking at rather than ignoring: it usually means a real part of your
workflow you haven't set up yet.

**Without a Status column the columns are work types**, exactly as they always were, and that
is not a legacy fallback — a board where the defects age and the stories don't is a completely
different problem from one where everything ages, and one glance separates them. Those columns
are ordered by how many items are in them, busiest first, and a board with more issue types
than fit folds its tail into one **Other types** column.

There is deliberately **no picker** to switch between the two. It would be a control you set
once and never touched, and nothing is lost without it: the work-type reading is a filter away.
Scope the strip to **Defects** and this chart answers *where do defects get stuck* — which is
strictly more than the work-type axis ever said.

Items within a column are spread across it and sorted by age, so two items the same age never
land on the same pixel.

### Click a Dot to Copy Its Key

Point at a dot and the tooltip names it. **Press it and its issue key goes on your clipboard**,
ready to paste into Jira — which is the next thing anybody does with a name read off this chart.
A toast confirms which key was copied. The pointer only turns to a hand over a dot that has a
key, so the affordance never promises something that would do nothing.

A dot with **no** key says so rather than copying something else. Without a Key column the
tooltip falls back to the work type, which is a useful label and useless on a clipboard — quietly
copying `Story` would be worse than doing nothing.

Where several items finished on the same day in the same number of days, their dots land on one
pixel. The tooltip describes **the one a press would copy** — the item it names at the top — and
says how many are underneath it: *"6 items sit on this dot"*, then *"Click to copy DAE-1306, the
one named above"*. The others are not reachable by pressing a dot they are hidden under; the
[Loaded Data table](#sorting-the-loaded-data-table) lists every one of them.

It works the same on **both** scatters — this one and [every finished
item](#every-finished-item-the-spread-not-the-average) — from one piece of code, so the pair
can never behave differently. It works in a [shared link](#sharing-a-read-only-link) too: it
writes nothing and reads only what is already drawn on the recipient's screen.

If you are working by keyboard or with a screen reader, the same keys are in the **Loaded data**
table on the Your Data tab, which has its own **Copy** button — that table is where every
chart's text description already points.

### What a Dot Is Called

Point at a dot and it names the item: its **issue key**, if your paste had a Key column. That is
the whole reason the key is stored — "which of these needs looking at" is unanswerable when
every dot on the chart is called Story, and a key is something you can paste straight into Jira.
Or [press the dot](#click-a-dot-to-copy-its-key) and it goes on your clipboard without the
retyping.

If your export has no key column, a dot falls back to its **work type and start date**, which
finds the item in the export you pasted in seconds. Both charts name dots the same way, from one
piece of code, so the pair can never disagree about what an item is called.

The key is the *only* thing out of your work system the app keeps — no summary, no status, no
assignee — and it is checked against [the shape of a key](#getting-your-data-in) rather than
trimmed to fit, so a mismapped column stores nothing at all rather than storing part of a
sentence. The Your Data tab lists every item with its key, unfinished ones at the top.

### Reading It

- **Nothing above the threshold line** — the board is healthy, and the aged work tile reads 0.
  Team Healthy Flow in the demo looks like this.
- **A few dots high above everything else** — the usual picture, and the useful one: those are
  the items to talk about, in that order, starting with the highest.
- **Everything drifting upward together** — not an ageing problem but a work-in-progress problem.
  Check the WIP vs throughput tile; the answer is usually to start less, not to push harder.
- **One column ageing and the others not** — a queue specific to that kind of work. Defects
  waiting on a reproduction, spikes nobody has time for.

Ages follow the **working days** setting exactly as the ageing threshold does, because a chart
whose dots and whose line disagreed about what a day is would be unreadable. And like work in
progress and aged work, ages are read **as of the newest date in your data**, not today — so a
paste of last quarter's export reports that quarter rather than ageing everything by the months
since.

## Forecasting: What the Pace You've Had Implies

Every other figure here describes what already happened. The **Forecast** tab is the one that
looks forward, and it does it without asking you to estimate anything at all.

It takes the throughput this team actually recorded — the completions in each whole period —
deals those periods out again at random **ten thousand times**, and reports how often each
outcome came up. That is a Monte Carlo forecast, and the only input it needs is the thing you
have already pasted: dates. No story points, no sizing, no velocity, nothing anybody has to
guess at in a room.

It answers two questions, from the same set of deals:

| Question | You type | You get |
|---|---|---|
| **Time to finish** | a number of items | the date that many will be done by, at 50%, 85% and 95% confidence |
| **Items by a date** | a target date | how many will be finished by then, at the same three confidences |

Both boxes sit inside the tab rather than in the control strip at the top of the dashboard,
because they change nothing outside this group. Everything in the strip *does* reach them: the
team, the work type filter, the date window and the grouping all decide which periods get dealt.

### Read the Confidence, Not the Percentile

The two questions take their answers from **opposite ends of the distribution**, which is the
one thing about this feature that is easy to get backwards:

- A **date** is a safer promise the **later** it is. 95% confidence buys you a later date.
- A **count** is a safer promise the **lower** it is. 95% confidence buys you a smaller number.

So being more careful moves one answer up and the other down. Nothing on screen is labelled by
percentile for that reason — every row says "85% confident", and every count says "at least",
so you never have to hold the flip in your head. A team asked for twelve items might see *85%
confident: 8 October* and, on the card beside it, *85% confident: at least 47 items by 15
December*. Both are the cautious reading.

Which row to use is a judgement about consequences, not about statistics. 50% is a coin toss —
fine for a private guess at what a sprint might hold. 85% is the one worth saying out loud, and
the same 85 the cycle time tile reads, for the same reason: high enough to be a promise worth
making, low enough that one freak run doesn't set it. 95% is what you quote when being late is
expensive.

### The Spread Is the Real Output

The chart under each answer is the distribution the three rows are read off, shaded by
confidence — the stronger the colour, the safer a promise at that point. It is worth more than
any single row. A narrow, tall distribution means the team's pace is steady and the date is
close to a fact. A wide, flat one means the date is a guess whichever row you pick, and the fix
for that is steadier delivery rather than a later promise. Two teams with the same median can
have completely different pictures here, which is exactly the conversation the tab exists to
start.

The shading runs one way on one chart and the other way on the other, because the safe end of
each is at a different edge — but the colour means the same thing on both, and the rows repeat
it in words for anyone who would rather not read colour at all.

### What It Assumes, and When It Refuses

**It assumes the next few periods look like the ones on screen.** That is stated on the tab
itself, every time, rather than hidden in a help note — and it is why the date window is part
of the forecast rather than just part of the charts. Narrowing to 3 months is how you ask "what
if we carry on at our recent pace?"; opening it to 12 asks the same question of a longer, and
possibly less relevant, history. A window stretching back past a reorganisation forecasts a team
that no longer exists.

**Below eight whole periods it refuses outright.** Both cards say so and name the control that
fixes it — group by a shorter period, or widen the window. With a handful of observations the
shape of the answer is a fact about which four periods you happen to hold rather than about the
team, and reporting a confidence there would be inventing one. Grouping by month over a 3-month
window is the usual way to meet this, and grouping by week is the usual way out of it.

**The same data and the same question always give the same answer.** The random number generator
is seeded with a constant, so a forecast never moves a day between renders — switch the filter
and switch it back and the figure is where you left it. The uncertainty is stated by the spread
on the chart, which is where it belongs; a number that also jittered would read as the app being
unsure of itself.

### Two Details Worth Knowing

**Answers are given to the day**, even though the sample is dealt in whole periods. When a run
crosses the finish line part-way through a period, that period is counted as the fraction of it
that was needed — reaching the tenth item three items into a week that delivered five counts as
three fifths of a week. Without that, a weekly team would answer "2 weeks" to almost every
question anyone asked, and the chart would be four bars wide.

**It counts items, not points or value.** So it is only as good as your items being roughly
comparable in size — which, on a board whose cycle times cluster, they usually are, and if they
are not, that shows up as a wide spread rather than as a wrong answer quietly given.

## One Chart, Filling the Window

Every chart card has a **⤢** button in its top-right corner. Press it and that chart fills the
window — the same chart, the same figures, drawn at four or five times the size, which is the
difference between "there is a spike around week 29" and being able to read which week it is.
Press it again, press **Esc**, or click the margin around the card to come back. Everything
else on the page stays exactly where you left it, including which tab and which chart group you
were on.

**The menu stays put.** The header — the team picker, the theme, Teams & Stages, Back up and
Share — is still there above the chart and still works, so you can flick a chart between two
teams without leaving it. That is why this isn't the browser's own full-screen mode: that one
takes the header, the tabs and the address bar with it, and you would have to come back out to
change anything.

A few details:

- **The button only appears when there is a chart under it.** Lead time on a team with no
  created dates shows its explanation instead, and there is nothing to enlarge — so no button.
- **If the chart goes away while it is filling the window, the window comes back down.**
  Switching to a team that can't draw that chart is the way you would meet this.
- Charts still do everything they do at ordinary size. The ⓘ still opens, tooltips still follow
  the pointer, and on the two scatters [pressing a dot still copies its
  key](#click-a-dot-to-copy-its-key).
- The **Time in stage** card has no button, because it is a table rather than a chart — the
  **Copy** button beside it is the thing worth having there.
- It works in a [shared link](#sharing-a-read-only-link) too. Like everything else on a chart it
  writes nothing: which chart is enlarged isn't saved anywhere, so a reload brings back the
  dashboard as it was.
- On a phone it is worth more, not less: the header takes two or three rows and the chart gets
  everything under it, which is roughly twice the height a card gives it.

## Taking a Table off the Page

All three tables of figures — **All Teams**, the **Loaded Data** list on Your Data, and
**[Time in stage](#where-the-time-goes-time-in-stage)** on the Health tab — carry
**Copy** and **⬇ CSV** in their heading.

| Button | What it does |
|---|---|
| **Copy** | Puts the table on the clipboard tab-separated, which pastes as a real grid into an email, a slide or a spreadsheet |
| **⬇ CSV** | Downloads a file, for keeping or for opening in Excel |

Two buttons because there are two jobs and each is bad at the other's: a pasted CSV lands as one
column of text and has to be run through *Text to Columns*, and a file has to be a CSV to open as
a spreadsheet at all.

**What you export is what you are looking at.** The tables are read off the rendered page rather
than rebuilt from stored data, so every choice you have already made applies — the work type
filter, the date window, the grouping, which ART is in scope, which column the table is sorted
by — and the file cannot quietly disagree with the screen it came from. Display furniture is
dropped: the ⓘ buttons, screen-reader-only text, and the ART printed under a team's name, none
of which are values in a cell.

The filename says where it came from and when — `flow-metrics-all-teams-2026-08-20.csv`, or
`flow-metrics-all-teams-payments-art-2026-08-20.csv` when you have scoped to one train, so two
exports taken a minute apart don't land in Downloads under the same name.

**The buttons stay on in a shared view**, unlike every other control there. Everything else a
shared view strips is stripped because it would *write*; this writes nothing and can only hand
back figures already on the recipient's screen. Sending a link is how a colleague gets these
numbers — letting them paste the table into their own notes is the point of it.

One detail worth knowing: a spreadsheet treats a cell opening with `=`, `+` or `@` as a
**formula**, so a team called `=1+1` would be executable the moment the file is opened. Those
cells get a leading apostrophe, which Excel, Numbers and Sheets all read as "this is text". A
genuine negative number is left alone — net flow is negative for half the weeks on a busy board,
and quoting it would break the arithmetic you exported a CSV to do.

The two tables in the **Settings** and **Teams & Stages** windows have no export buttons: they are
configuration — a Display→Value mapping, and a list of names — rather than figures anybody puts
in a status email.

### Sorting the Loaded Data Table

The item list sorts the same way the [All Teams](#all-teams-which-one-needs-you) table does:
press a heading to sort by it, press again to reverse, and **a third time to turn it off**.

It opens — and returns to — **items still in play at the top, then newest first**, which is the
order that answers "what is open right now?" without asking for anything. Pressing a heading asks
for a different order rather than replacing that default with whatever was last pressed.

Each column runs the useful way on its first press: dates newest-first, cycle time longest-first.
**Item** is the one exception and runs A to Z, because a list of keys has no most-interesting
end — you scan it for one you already have in mind. It groups by project and then runs in
issue-number order, so `DAE-10` comes after `DAE-9` rather than between `DAE-1` and it.
**Absences always sort last**, whichever direction the column is running — an item still in
progress has no completion date and no cycle time, so it has no place in an ordering by either,
and letting it win the top would be the one result nobody could read past.

The period column sorts **chronologically**, by the completion date behind it rather than by its
own label — "Aug 2026" and "Sep 2026" sort backwards as text.

Because [export](#taking-a-table-off-the-page) reads the rendered page, **the sort travels with
it**: sort by cycle time, press ⬇ CSV, and the file arrives in that order.

## Printing It

**Ctrl-P / ⌘-P prints the view you're looking at**, and the page is laid out for paper rather
than photographed off the screen. What goes is everything a piece of paper cannot use: the tab
strip, the three pickers, the header's buttons, the ⓘ circles, the maximise buttons and the
export buttons. What stays is the figures, the charts, and — the one that matters — **the note
saying which dates they cover**, plus a line naming the team or the train. A figure on paper
without its window is worthless, and the header's team picker is one of the things that has just
gone.

**A dark theme prints as a light one.** Browsers don't print page backgrounds, so Midnight and
Dark would otherwise come off the printer as pale grey text on white paper, with charts drawn in
colours picked to sit on black. The page switches itself to the **Light** theme for the duration
of the print and back afterwards — no colour is invented for paper, and nothing is saved, so the
swap can't outlive the print. Light and Sepia are left exactly as they are; both are already ink
on a pale ground.

Charts print because a canvas is an image, drawn at device resolution, so it scales down cleanly
onto the page. A chart filling the window is brought back down first — printed as it stands, it
would be one chart on page one and a blank page two.

For figures somebody needs to *use* rather than read, the
[Copy and ⬇ CSV buttons](#taking-a-table-off-the-page) are still the better route.

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
a copy you keep, independent of this browser. It is the only copy of your data that exists
anywhere else, and the only way back from a cleared browser.

**Restoring replaces everything.** You're shown what the file holds against what's already
here — *"Restore 2 teams and 3 items from this file? This replaces the 1 team and 0 items in
this browser"* — and nothing changes until you confirm. Restoring on another device is how you
move your data between devices.

A restored file goes through exactly the same sanitising as a share link (`hydrateState`), so a
hand-edited backup can't introduce anything a link couldn't.
Before that, `isBackup()` checks the file is plainly one of ours: `hydrateState` is deliberately
forgiving and will turn `{}` into a valid empty dashboard, which is right for a damaged saved
copy and catastrophic for the wrong file picked out of a Downloads folder. Choosing a file that
isn't a backup is refused outright and leaves your data alone.

**If one device is behind** — every saved copy carries the data format the app that wrote it
understood. A copy written by a *newer* version than the one you're running won't be opened:
you get a card saying so, nothing is changed or deleted, and reloading picks up the current
version. That matters most on a device that's been offline for a while, where the browser can
still be running an older cached copy of the app while another device has moved on. A backup
file from a newer version is refused the same way — without stopping the app you're using —
and a share link from one tells the reader the link is fine and their copy is behind.

**Two things are deliberately not in the file:** your theme, and which team you were looking
at. Both are positions on this device rather than data.

### Starting Again

Folded away at the foot of the same dialog, under **Start again**, is **Delete all data** —
the whole-board version of Clean up old data. It's behind a fold on purpose: the one
irreversible action in the app shouldn't sit a mis-click away from Download backup.

Pressing it opens a confirmation of its own that **lists exactly what is going** — "This deletes
2 teams and 3 items, along with 1 ART and 4 workflow stages" — and offers the same JSON download
as a last chance to keep any of it. The ARTs and the stages go with the teams: a stage carries
status names you typed off an export and an ART is a grouping of teams, so both are data. **Your
settings are kept**, which is the line the delete draws — the labels, the thresholds, the work
type filters and your theme are configuration, and the dialog says so. There is no "…and every device you own" line any more: since sync was removed there is
exactly one copy, and it is the one in this browser.

**Your settings and your theme survive.** Starting fresh isn't asking to lose the type
labels, filters and ageing threshold you spent time tuning — those are configuration, not
data. What's left is exactly what a brand-new browser gets: one empty team to paste into.

## Sharing a Read-Only Link

The **Share** button in the header builds a link that shows someone the teams you pick,
read-only — no sign-in, no way to change anything, and (ported from the sibling app) the
data travels **inside the link itself**: everything after the `#` never leaves the browser,
so the figures reach the recipient without GitHub Pages or anyone else seeing them. The payload is a trimmed copy — the chosen teams plus the shared settings, because
those drive every number on the charts.

It carries the same fields the app stores, **issue keys included**. That is deliberate: the keys
are what names the items on the charts, and a link that dropped them would show the recipient a
different picture from the one you are looking at. Nothing else out of your work system goes —
no summaries, no statuses, no names — and a key in a link has passed the same shape check as a
key in storage, so a link cannot carry anything in that field the app would not have saved. The
dialog says so above the link. A recipient still on an older cached build simply sees dots named
by work type, as they were before keys existed.

**A team's [limit and target](#your-own-limit-and-your-own-target) travel with it**, so the
lines on the charts and the verdicts on the tiles read the same for the recipient as for you.
The project id deliberately does not — it routes a paste the recipient has no way to make.

**Stage times travel too, and so do the stage names they belong to** — they are what the figures
*are*, and a link carrying counts without names would arrive showing nothing. Only the stages
the shared items actually spent time in go, on the same reasoning that sends only the trains
those teams are on: a stage name describes your workflow, and sharing one team should not
publish the shape of a workflow that team has nothing to do with. **The list of Jira statuses
you typed does not travel at all** — it is a matching rule for a paste box the recipient does
not have, and it is the one field in the app typed to mirror a work system's own words.

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

The recipient sees a standing "Read-only view" bar, the dashboard only (no Your Data tab, and
none of the header buttons that write — Teams & Stages, Back up, Share or Settings), and a link
back to their own data. Nothing they do is saved, and nothing
already in their browser is touched — `save()`, `persist()` and `saveView()` are all
no-ops in a shared view, and no service worker is installed. A link that arrives truncated (mail
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

## Installing It

Chrome's **Install page as app**, Safari's **Add to Dock** and iOS's **Add to Home Screen** all
turn Flow Metrics into a real app window with its own icon, rather than a browser tab or a
shortcut with a blank square next to it. That takes a `manifest.webmanifest` and PNG icons —
neither the inline SVG icon nor `favicon.ico` is any use to any of them — and both are in the
repo, drawn by `make_favicon.py` from the same mark the favicon uses.

Installing is a **window, not a sandbox**: an installed app shares the browser's storage, so
nothing about it changes what any page on this origin can already reach. The manifest's scope is
its own directory, which matters more than it looks here — every one of these apps is served from
the same origin, and a scope of `/` would capture Sprint Predictability and Money Map into this
app's window.

The offline cache below came first, which is the wrong way round: an installed copy is the one
most likely to be opened with no network at all, so the manifest and its icons are cached with
the rest of the shell.

## Working Offline

The app keeps a copy of itself on your device, so it opens with no network at all — on a
train, on hotel wifi, or when the work VPN is being difficult. Your teams and work items
were always local, so once the page loads **everything** works: pasting, the charts, cleanup,
export, share links, backup and restore. There is no longer any part of the app that needs the
network — sync was the one exception, and it is gone.

What's kept is only the app's own public files — the page, the stylesheet, the chart
library, the icons and the install manifest, the same files anyone can read on GitHub. **Nothing of yours is ever
put there**, which matters more than it sounds: every one of these apps shares a single
browser origin, so that cache is not private to this app.

The network is always tried **first**, and the stored copy is used only when it genuinely
doesn't answer (or takes more than five seconds). So you can't be left running an old
version while you're online — and if a device does end up behind, the version check
described under [Back Up & Restore](#back-up--restore) stops it misreading anything.

`sw-kill.js` sits in the repo unused, as an escape hatch: copying it over `sw.js` and
pushing makes every installed copy uninstall itself and go back to being an ordinary
online-only page.

## Cross-Device Sync Was Removed (2026-08-20)

This app used to offer optional Google sign-in, which mirrored your teams to a Firestore
database in a Firebase project owned by the author. **It is gone.** Not disabled behind a
`null` config — removed: the module, the sign-in button, the reconciliation dialog, the
`firestore.rules` file and every Google address in the Content-Security-Policy went in one
commit.

**Why.** This app holds figures taken from a work Jira. Sync meant a copy of them sat in a
personal Firebase project, which is a place work data has no particular business being — and
the feature was carrying a fair amount of complexity for it: a hostname-blocking workaround, a
reconciliation dialog, an empty-copy-never-wins rule, a server-clock ordering scheme and a
whole class of failure ("looks fine, has not pushed for weeks") that had to be surfaced in the
UI because it could not be prevented. Removing it deleted all of that at once.

**What replaces it.** **Back up** downloads a JSON file; **Restore** reads one back. That is
how you move data between devices now, and it has the property sync never had: you can see
exactly what moved, and it goes nowhere you did not put it.

**What the removal is worth checking against.** The claim is not "the Firebase code is gone" —
it is that the page cannot reach the network at all. The CSP at the top of `index.html` names
**no external origin**, and spells out `connect-src 'none'` rather than leaving it to the
default, because that is the directive that would carry work data off the device. `tests.html`
pins both, plus a word-list tripwire over the app's code so a paste-back of the old module
fails loudly rather than shipping.

**Leftovers are deleted, not merely unread.** `clearSyncLeftovers()` runs on every load and
removes `td-sync-uid` and `td-updated`. The first of those is a Google account id — the only
personally identifying thing this app ever wrote down — and keeping it after removing the
feature that needed it would be keeping an identifier for no reason. Pinned by a test that
plants both keys, boots the app and checks they are gone.

**The data written before the removal was deleted too**, on the same day — removing the
client deletes nothing server-side, so the Firestore collection was emptied by hand in the
console. `privacy.html` says so rather than promising to do it on request.

**If it is ever wanted back**, `git log` has the whole module in one commit, including the
Google Identity Services workaround for corporate networks that block
`<project>.firebaseapp.com` per hostname — which was real, was measured, and would be needed
again. Putting it back means putting the CSP origins back too, and the tests above will say
so.

## Running It

Single page, no build step, no accounts required. Serve the folder:

```bash
python3 -m http.server 8013
```

`index.html` no longer stands alone: the palette is linked as `theme.css` rather than
inlined, and the charts need the vendored `chart.min.js` — without it the page's script
stops at startup. Copying all three files (`index.html`, `theme.css`, `chart.min.js`) to a
folder and opening `index.html` over `file://` still works; a server is simplest, and the
tests need one anyway.

Your data lives in `localStorage` and does not leave the browser.
[`privacy.html`](privacy.html) is the privacy policy — keep it and its effective date current
if what the app stores, or where it sends it, ever changes. The footer links to it, and to
this README on GitHub as **How it works**, for anyone wanting more than the in-app ⓘ dialogs.

A Content-Security-Policy `<meta>` at the top of `index.html` **names no external origin at
all**. Since sync was removed there is nothing for it to allow: no CDN, no Google, no
analytics. `default-src 'none'` is therefore the real rule rather than a formality, and each
directive below it is an exception it has to earn — including `connect-src 'none'`, spelled
out rather than left to the default because it is the one directive that would carry work data
off the device, and `worker-src 'self'` for `sw.js`, spelled out rather than resolved through
the fallback chain.

**Adding any origin there is a decision about where work data may go, not a technical
detail** — and it fails only in production while working fine on localhost, so it will not
announce itself. `tests.html` fails if the policy names a single host.

## Tests

![tests](https://github.com/eagleadams86/team-dashboard/actions/workflows/tests.yml/badge.svg)

`tests.html` pins the pure functions by loading the real `index.html` in a hidden iframe — no
copies to drift. It must be served over `http://localhost`, not opened as a file. The iframe is
marked `data-td-tests`; that was how the sync module knew to stay off inside the harness, and
the attribute is kept — it is the harness's only way to say "this is a test frame", and the
next thing that must not run in one will want it.

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

Beyond the metrics it covers `detectColumns()` (a leading key column read as the key, the dates
either way round, header names beating position, a free-text summary mistaken for neither the
type nor the key, and the real Jira headings a loose pattern would swallow — *Issue id*,
*Parent key*, *Key changed date*), the issue-key guard from both directions (every rejection
listed one by one, including a summary, markup and a spreadsheet formula),
work-in-progress handling — including the net-flow miscount stated as a test, and a WIP row
whose *empty completed cell comes first*, which a line-trim once shifted into a completed row —
the week straddling New Year (whose cycle times once vanished from the chart and tile), quoted
CSV fields, the share-link codec round trip on both wire formats, that [sync really is
gone](#cross-device-sync-was-removed-2026-08-20) (a CSP naming no host at all, a word-list
tripwire over the app's code, and the leftover keys actually being deleted at boot), and the
outside-copy boundary: `sanitizeTeams()` (ids arriving in a share link end up in `data-` attributes and
`<option value>`, so anything not `[A-Za-z0-9_-]{1,64}` is replaced, names are capped, types
coerced to strings), `normalizeSettings()`
(including the `defectType` → `unplannedType` carry-over, and junk filter entries or a junk
same-day value being coerced rather than trusted), `hasData()`, the predicate the
"empty never beats data" rule rests on, and `isBackup()`, the guard that stops the wrong JSON
file being restored over real data.

**Workflow stages get the longest guard group in the suite**, in both their halves — because they are the one field
whose source is a Jira status and the safety does not come from a check on the value. Both
halves are pinned: the *guards* (a day count is a plain number — `3d 4h`, `12:30`, a negative
and a six-digit value all refused; an alias is capped and dropped whole past it; a hostile or
dangling stage id never reaches a stored day count, and the day-count object has no prototype
for a `__proto__` key to reach) and the *route* (matching is exact rather than substring, the
stage *name* is not an alias, two columns feeding one stage are added, two stages claiming one
status is reported rather than resolved, and a status nobody has listed is simply not read —
so a paste can never add the rule that reads it). The claim underneath the whole design is
asserted directly: the parsed rows are stringified and checked to contain **no status name at
all**, on hand-written fixtures and again on the demo's own data.

**Click-to-copy** is pinned on the part that can go quietly wrong: a dot with no key saying so
rather than copying its work type, a reference line yielding nothing, and — the one no pure test
can see — both scatters actually carrying the handler, as the *same* function, while a chart
whose points are periods carries none.

The **current stage** gets its own group, since that is where the untrusted text sits in a cell
on every row rather than in one heading: the anchored heading against the real Jira columns a
loose pattern would eat (*Status Category*, *Status changed date*), a Status column not being
mistaken for the work type, a finished item taking no stage however its status reads, a
dangling or unsafe stage pointer being dropped, and the age chart switching axes — stage
columns in the reader's order with counts on the ticks, work type ranked busiest-first when no
item in flight carries a stage.

Two promises get pinned end to end rather than function by function:
`buildSharePayload()` — a share link holds **only the chosen teams** plus the shared settings,
and nothing else (no theme, no view state) — and `migrate()`, the v1 upgrade,
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

**Why there is a `package.json` in a repo with no build step.** It is not a package and it
installs nothing — it exists so Dependabot has a manifest to scan. Its only entry is the
Chart.js that is *vendored* as `chart.min.js` beside the app, pinned exactly, and CI passes
`--omit=dev` so npm never downloads it. Dependabot cannot re-vendor a file, so a version-bump
PR would otherwise raise the manifest while the app went on serving the old bytes; a test pins
the two to the same version, which makes a manifest-only bump fail and turns the PR into the
right instruction — update the file too, in all four repos that carry it.

## Files

| File | |
|---|---|
| `index.html` | The whole app — inline CSS and JS |
| `chart.min.js` | Chart.js 4.4.1, vendored (no CDN) |
| `theme.css` | Copy of the palette from [claude-theme-pack](https://github.com/eagleadams86/claude-theme-pack); **linked** by `index.html`, `privacy.html` and `tests.html` — since 2026-08-18 it is not also inlined, so the palette lives in one place and a pack change reaches the app |
| `sw.js` | Service worker: keeps the app's own public files on your device so it opens offline |
| `sw-kill.js` | The escape hatch — copy it over `sw.js` and push to uninstall every installed worker |
| `tests.html` | Pure-function tests |
| `privacy.html` | Privacy policy — what the app stores and where it does (and doesn't) go |
| `.github/workflows/tests.yml` | Runs `tests.html` headless on every push |
| `favicon.ico` | Tab icon — the fallback a browser fetches from the site root on its own |
| `manifest.webmanifest` | What makes the app [installable](#installing-it) — its name, its window and its icons |
| `icon-192.png`, `icon-512.png` | The install icons a launcher draws the app with |
| `icon-512-maskable.png` | The same mark full bleed, for launchers that crop an icon to their own outline |
| `apple-touch-icon.png` | Safari's own preference, square and opaque — Apple applies its own corners |
| `make_favicon.py` | Draws `favicon.ico` and all four PNGs above, all from the same mark as the inline SVG icon in `index.html` |

The icon is three weeks of flow side by side, on the midnight tile the whole app family
wears; the header shows the same mark. `make_favicon.py` (Pillow) keeps `favicon.ico` and
the page's inline SVG the same picture, rather than leaving a binary nobody can review in a
diff. Re-run it with `python3 make_favicon.py`, then bump the `?v=` on every `favicon.ico`
reference — browsers hold on to an icon for a long time. The install PNGs are versioned by
`sw.js`'s `CACHE` constant instead; bump that too.

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
links, four themes and a test suite. It had cross-device sync too, until that was removed on
2026-08-20 — see [above](#cross-device-sync-was-removed-2026-08-20).

## Ownership and Licence

Flow Metrics is an independent personal project by Charles Adams — built on personally owned
hardware, with a personally paid-for Claude subscription, in a personal GitHub account. No
employer equipment, funding or code went into it, and since 2026-08-20 it has no server or
database behind it either: your data stays in your own browser.

It holds no employer information beyond issue keys, and that is a property of the design
rather than a promise: there is no free-text field anywhere in the app, and the storage
whitelist admits only numbers, dates, short fixed labels and the shape-checked key. Text you
paste in is parsed in the browser and thrown away — summaries, statuses and comments are never
stored, transmitted or committed, and nothing is ever committed to this repository. Adding a
stored field means adding it to that whitelist, or it is deliberately stripped.

Share it freely: it is [MIT licensed](LICENSE), so anyone — including a company you work
for — may use, modify and redistribute it. Running it inside an organisation conveys no
ownership of it; permission comes from that licence, granted by the author as copyright
holder. [NOTICE](NOTICE) records this in full.

## The Landmarks (2026-08-21)

`<main>` opens **above** the tab strip, not below it. It used to wrap the tab panel alone,
which had two consequences: the tabs sat in no landmark at all (axe-core's `region` rule),
and — the reason worth acting on — **the skip link jumped past them**, so a keyboard user who
took "Skip to content" had the entire tab row behind them, reachable only by shift-tabbing
back. The tabs and the panel they drive are one widget, so the landmark goes round both. The
share bar comes inside with them: it describes what is on screen, so it is content rather
than furniture.

`role="tabpanel"` still goes on the inner div and never on `<main>` — putting a role ON an
element IS its role, so it would silently replace the landmark. That older note stands
unchanged.

Every page in this repo passes axe-core at WCAG 2.1 A and AA plus its best-practice rules, in
all four themes, with data loaded and on every tab.
