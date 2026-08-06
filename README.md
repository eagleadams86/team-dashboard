# Team Dashboard

Four weekly flow metrics for a delivery team, from nothing but a list of completed and started
dates. A web port of the "Team Dashboard v5" Excel workbook, minus the 20-second recalculation.

**Live:** https://eagleadams86.github.io/team-dashboard/

Paste your work items, get four charts:

| Dimension | Question it answers | What's plotted |
|---|---|---|
| **Quality** — how well | How much defect debt do we carry? | Unplanned work as a share of everything completed, per week |
| **Responsiveness** — how fast | How long from starting to finishing? | Average cycle time per week |
| **Productivity** — how much | What pace do we deliver at? | Items completed per week |
| **Predictability** — how repeatable | Is our completion pace consistent? | Net flow — items completed minus items started, per week |

Each chart carries a dashed linear trend line, the same as the workbook's.

## Getting your data in

The **Your Data** tab takes three columns pasted straight from Excel, Jira or a CSV:

```
Completed Date   Start Date   Type
2015-01-21       2015-01-14
2015-01-26       2015-01-14   Defect
2015-01-26       2015-01-21   Unplanned
```

- Only **Completed Date** is required. Start Date is needed for cycle time and net flow;
  Type is needed for the Quality chart.
- Tabs and commas both work, and a header row is skipped automatically.
- Dates can be ISO (`2015-01-21`), numeric (`21/01/2015`), month-name (`21 Jan 2015`) or raw
  Excel serial numbers. Where `03/04/2015` is genuinely ambiguous, the app auto-detects
  day-first vs month-first from the rest of your data — or you can force it.
- Rows with an unreadable completion date are skipped and listed back to you; a bad start
  date keeps the row but drops the date.

There's no inline row editing — to fix something, correct it at the source and paste again.

## Settings

Everything the four charts depend on, defaulted to the workbook's own values:

- **Team name** — appears in the page title
- **Unplanned work type** — the exact text in your Type column that means "unplanned"
  (`Defect` by default). Anything blank, or not matching, counts as planned work.
- **Same-day cycle time** — what an item that starts and finishes on one day is worth
  (`0.5` days)
- **Legend labels** and the **word for cycle time** (Cycle time / Time in Process / TiP /
  In process time)
- **Work type filter list** — the Display → Value pairs behind the dashboard's filter

The workbook's aging thresholds, WIP/age warning percentages and cycle-time percentile aren't
here: they only feed the *WIP and Age* and *More Charts* sheets, which this app doesn't carry.

## How the numbers are worked out

`derive()` in [index.html](index.html) is the only place any figure is computed, and it's a
faithful port of the workbook's formula chain — each block cites the sheet and column it
reproduces. The parts worth knowing:

- **Weeks start on Sunday.** Week keys are `YEAR-WW` using Excel's default `WEEKNUM`, where the
  week containing 1 January is week 1. Reimplemented rather than approximated, because
  JavaScript has no equivalent.
- **The date window trims the axis, not the data.** "Show data for most recent 3 months" moves
  where the chart starts; every item still counts toward the weeks that remain. That's the
  workbook's behaviour and it's deliberate.
- **Cycle time** is `completed − started`, floored at 0, with same-day items taking the
  configured value.
- **A week with no unplanned work scores 0%**, not blank; a week with no completions has an
  average cycle time of 0.

One deliberate departure from the workbook: it colours the net-flow bars blue and orange. This
app uses the theme's accent for positive and `--serious` for negative — not the red/green pair,
because the coaching goal is "keep around zero", so neither sign is good or bad.

## Running it

Single page, no build step, no accounts, no network calls. Open `index.html` directly, or
serve the folder:

```bash
python3 -m http.server 8013
```

Your data lives in `localStorage` and never leaves the browser.

## Tests

`tests.html` pins the pure functions by loading the real `index.html` in a hidden iframe — no
copies to drift. It must be served over `http://localhost`, not opened as a file.

The expectations aren't invented: they're the cached formula results from the workbook itself
for its own 141-item sample. If the suite is green, this app reproduces Excel — down to
`Throughput!D2 = 7`, `Cycle Time!Q2 = 10.2857…`, `Work in Progress!W2 = −5`, and the
19.92% average defect rate in the Quality chart title.

## Files

| File | |
|---|---|
| `index.html` | The whole app — inline CSS and JS |
| `chart.min.js` | Chart.js 4.4.1, vendored (no CDN) |
| `theme.css` | Copy of the palette from [claude-theme-pack](https://github.com/eagleadams86/claude-theme-pack); also inlined into `index.html` so it works over `file://` |
| `tests.html` | Pure-function tests |

Four themes — Midnight (default), Dark, Light, Sepia — from the shared theme pack. Palette
changes belong in the pack, not here.
