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

## ARTs (2026-08-20) — the first schema bump since working days

`state.arts` is a list of `{id, name}` and each team carries an `artId` or null. **SCHEMA 4 → 5,
with `sanitizeArts` and the widened `sanitizeTeams` in the same commit** — the rule at the top of
this file, honoured. Modelled exactly like the sibling app's, down to the field names, because
the two are read side by side; the divergences below are deliberate.

- **An ART is a LABEL, never a level of maths.** Every figure is worked out per team by
  `derive()` and All Teams adds them up. The moment an ART carries a figure of its own there are
  two places a team's throughput can be computed and they can disagree. Keep it a filter and a
  sort.
- **`teamsInArt` and `groupTeamsByArt` are pure** — they take the list rather than reading
  `state` — so a share payload can be grouped before it is adopted and tests can pin both. They
  live in section 4 with the rest of the domain code, **not** beside `sanitizeArts`: the
  `window.TD` export runs at the end of section 4, and `const ART_NONE` declared in section 5 is
  a temporal-dead-zone error that takes the whole app down. It did, once, during the build.
- **Grouping is a SORT, not a filter**: `groupTeamsByArt` returns every team. Within a group they
  keep the order they were added in, so a list somebody knows by eye never silently reshuffles.
- **A dangling `artId` is cleared in `hydrateState`, not guarded at every read.** It happens for
  real — an older build drops `arts` while keeping the teams it hydrated. A hostile `artId` is
  **dropped rather than replaced** with a fresh id: an invented one points at no ART anyway, and
  "on no train" is a real answer where a made-up id is not.
- **Nothing is written until there is something to write.** No `arts` key and no `artId` until
  they exist, so a browser that never uses the feature serialises byte-identically to before and
  its first save after this build lands doesn't rewrite the whole synced document — the same rule
  the per-row created date follows. Pinned.
- **`SHARE_PAYLOAD_V` was NOT bumped.** An older cached build drops `arts` and shows ungrouped
  teams, which is graceful degradation rather than a wrong number; bumping would make every link
  from this build unreadable to that one. A link carries **only the trains its own teams are on**
  — sharing one team must never publish the names of every train Charles supports, and an ART
  name is the one field in a payload that names something outside the team.
- **`view.artFilter`, not `state.settings.artFilter`** — the one deliberate divergence from the
  sibling, which keeps it in settings. TD already moved `activeTeamId` into `view` on the
  reasoning that scoping the laptop should not yank the phone; the same argument applies, and it
  keeps the filter off the schema entirely. Validated in `currentArtScope()`, which falls back to
  every team: a scope that shows too much is visible, one that shows too little is not.
- **One `scopePhrase`, used in all four places the scope is said** (heading, summary row, window
  note, empty state), so they cannot drift. "No ART" is right on a picker, where it is one option
  beside the train names, and wrong in a sentence — "All teams on No ART" reads as a train
  somebody called No ART. The heading takes a Title Case variant, like every heading here.
- **A train with no teams yet gets its own empty state.** It is one click to reach (add a train,
  close the dialog) and neither of the other two messages fits: there is no filter to blame and
  nothing to paste, because the train has no teams rather than no data.
- The team-name column has a `min-width` so the ART picker beside it cannot truncate
  "Team Kingfisher" to "Team Ki" on a phone; the row simply outgrows the dialog and
  `.table-scroll` does its job.
- **The demo puts two teams on one train and leaves one on none.** A train per team makes
  grouping look pointless; all three on one leaves the No ART option absent. Pinned, including
  that scoping to the train visibly moves a figure — a picker that changes nothing on the one
  dataset anybody is shown is a feature nobody will find.
- A fixture with a literal `</script>` in it closed the script block in tests.html and the whole
  suite silently stopped running. Hostile-id fixtures use `'"><script>'`, the form the existing
  team-id tests already use.

## Copy and CSV on Every Table of Figures (2026-08-20)

Ported from the sibling, which grew it first; the two apps are read side by side and a table
should come off either the same way. Until this landed the only ways figures left the app were
the whole-dataset JSON backup and a share link, neither of which helps anybody putting the All
Teams comparison into a Monday status mail.

- **Read off the RENDERED table, never rebuilt from state.** Both tables are already the product
  of choices the reader made — filter, window, grouping, ART scope, sort column — and a second
  code path building "the same" rows would have to reproduce every one of them and would drift
  from the screen the first time one changed. What you export is what you are looking at, by
  construction. Don't "optimise" this into a state-driven builder.
- **`cellText` strips furniture**: `[aria-hidden="true"]` and `.sr-only` as the general rule,
  plus `.tile-help` and `.team-art`. The last is the named case — the ART under a team's name is
  a grouping the screen shows, not a figure in that cell, and the sibling strips its own
  `.artname` for the same reason.
- **`tableToRows` pads to the widest row.** A colspan empty state would otherwise emit a
  one-column row in a nine-column file: valid CSV, and every spreadsheet reads the rest of that
  row under the wrong headings.
- **The formula guard is a security boundary, not a formatting nicety.** `=`, `+`, `@` and a
  dash-not-followed-by-a-digit get a leading apostrophe. A team name is the one free-text field
  this app stores and a share link is how somebody else's text reaches this browser, so a CSV is
  simply the one place the escaping is not HTML. A **negative number is deliberately left alone**
  — net flow is negative half the time and quoting it would break the arithmetic.
- **Tabs for the clipboard, commas for the file.** A pasted CSV lands as one column and needs
  Text to Columns; a file must be a CSV to open as a spreadsheet. `cellText` collapses all
  whitespace, which is what makes a tab safe as a delimiter with no quoting.
- **The BOM is spelled `'\uFEFF'`, as an escape.** I first wrote it as a literal character and
  it survived — but it is invisible in an editor and in a diff, which is exactly why the sibling
  spells it out. Without it Excel on Windows opens a UTF-8 CSV as Latin-1. Note `Blob.text()`
  strips a leading BOM on decode, so a test asserting on the decoded string will always say it
  is missing; check `arrayBuffer()` for `EF BB BF`.
- **`toCsv` and `toTsv` are function DECLARATIONS**, not the sibling's arrow consts. Its test
  hooks sit at the end of that file; this app's `window.TD` export runs in section 4, thousands
  of lines above, and reading a `const` before its declaration took the whole app down once here
  — the same TDZ trap `ART_NONE` sprang.
- **The buttons stay on in a shared view.** Everything else a shared view strips is stripped
  because it would WRITE; this writes nothing and can only hand back figures already on the
  recipient's screen.
- **`slugify` guards the filename**, the other place free text lands somewhere it can be
  interpreted — a train name with a slash would propose a path.
- The Settings and Teams-dialog tables deliberately have no buttons: configuration, not figures.

## The Teams Dialog Follows the Sibling's (2026-08-20)

Reordering landed the same afternoon, in both apps at once:

- **Teams and ARTs reorder with ↑ / ↓.** Both lists are *read* in order — teams down the
  header picker and the All Teams table, ARTs as the order their groups come in — so the
  order you added things in is rarely the order you want a year later. Reordering permutes an
  array that was always there, so **no new field and no schema bump**.
- **`.icon-btn` split**: the base hover is now NEUTRAL and `.danger` is what turns it red,
  the same split `.btn` / `.btn.danger` already uses. The class used to mean "delete" because
  deleting was the only thing it did; the arrows are not destructive and must not light up as
  though they were. The × buttons carry `.danger` now.
- **Ends are disabled rather than hidden**: a button that vanishes at the top of a list makes
  the row jump and moves the delete under the pointer.
- **`moveInList` restores focus after `renderAll()`**, or moving something with the keyboard
  loses your place entirely — the row is rebuilt, so the focused button no longer exists. If
  it lands disabled, focus goes to its opposite number on the same row. The test that pins
  this **opens the dialog through `manageBtn`**: a button inside a closed `<dialog>` is
  `display: none` and cannot take focus, so the assertion passes vacuously without it.
- A team moves within its own ART group in the picker, not to the top of the list, because
  `groupTeamsByArt` sorts by train first. That is the same rule the All Teams table follows
  and it is pinned.


Charles asked for this window to match Sprint Predictability's **Teams, ARTs & PIs**, which is
the right call: the two apps share their chrome and the sibling is the design lead for it. What
that means concretely, and what a later edit must not tidy back:

- **`#manageDialog` is 1100px**, matched to the sibling's — which took it from Money Map's own
  wide dialog, so the three apps' working windows are one width. The app default of 560 is right
  for Back up and the help sheet, which are a few lines each, and wrong for a table of teams: at
  560 a row's name box, picker, count and delete were shouldered into each other.
- **No `thead` on either table.** There is nothing a heading would add — a count says
  "217 items", a picker shows the train it is set to, and a name box is a name box. Each control
  keeps its own `aria-label`, which a visible heading was never going to give it.
- **A section per thing you manage**, headed by its name with its own `+ Add` button at the
  right-hand end of the header row, a 12px muted note under the heading, then the table. Both
  Add buttons live in those headers, not under their tables.
- **The ARTs section is flat, not folded.** It was behind a `<details>` on the reasoning that
  most people support one train; the sibling shows its three sections flat, the two dialogs are
  read side by side, and a section somebody has to open is a section they have to find first.
- **Row padding is the sibling's 10px 12px, but the two outside edges are zeroed.** That
  difference is content, not taste: its rows hold plain text, where a 12px inset reads as a
  margin; these hold a bordered input box, and the inset would put that box out of line with the
  section heading directly above it.
- The heading stays `h2` at 16px rather than the sibling's `h3` at 17px, because every other
  dialog in THIS app is `h2` and one odd one out would be worse than a pixel of difference.
- Pinned in tests.html — the width, the absent theads, the two section headers, both Add buttons
  being in them, and the counts carrying their nouns. All of it is the kind of thing a later edit
  tidies back with the best of intentions.

## All Teams, and the Shared Control Strip (2026-08-20)

A second top-level view beside the Dashboard: every team as one row, over one shared window.
Rules it must keep:

- **`deriveTeams()` computes NOTHING.** Every figure in the table comes out of the same
  `derive()` the dashboard reads, once per team, so a row and that team's own page can never
  disagree — which matters more here than anywhere, because the table is what gets acted on
  before anyone looks at the detail.
- **The train is DERIVED over the concatenated rows, never summed.** Totals could be added up;
  percentiles cannot. The 85th percentile of eight teams is not the average of their eight
  percentiles, and a summary row built that way would be quietly wrong in its most-read column.
  A consequence to keep in the help text: pooling *items* weights the figure by how much each
  team delivers, so the train can read 7 while a small slow team reads 23. Both true. The tile
  is for promising unassigned work; the column is for finding who needs help.
- **`derive()` takes an `asOf` override, and it may only ever move a date LATER.** An earlier one
  would hide data rather than align it, and no caller should be able to ask for that by accident.
  `deriveTeams` derives the train first and imposes its `endDate` on every team, because without
  one shared date "the last 3 months" is a different three months per row.
- **`dataEnd` is read off the UNFILTERED `rows`, not off `items`.** Freshness is a property of
  the export; filter to defects and a healthy team's last defect might be a month old, which is a
  fact about its quality and would send someone chasing a perfectly current export. It is also
  taken before `asOf` can move anything.
- **The empty return carries `dataEnd` and `inProgressCount`.** It was moved below the date scan
  to be able to: a team with five items open and nothing finished is a finding, and a row of
  dashes claiming it has no work in progress would hide it. Don't move it back above.
- **The control strip is SHARED between the two views** (`#viewControls`, lifted out of
  `panel-dashboard` into `<main>`), because all three controls mean the same thing to both and a
  second copy would be two controls over one piece of state. Two consequences that bit during the
  build: the three handlers must call `renderViews()`, not `renderDashboard()` — the first
  version left the strip working on one tab and inert on the other — and `#windowNote` is written
  only by whichever view `activeTab` says is on screen.
- **`renderAllTeams()` returns immediately unless it is the view on screen.** Every row is a full
  `derive()`, forecast and all, so running it behind a hidden panel would multiply the most
  expensive thing the app does by the number of teams on every keystroke anywhere else.
  `selectTab` re-renders on the way in.
- The tab is hidden below two teams, the same threshold as the picker, and `selectTab` refuses to
  land on a hidden tab — a saved position outlives the team that was deleted, or arrives with a
  one-team share link. It DOES appear in a shared view, which is the point: an RTE can send a
  whole train's roll-up as one link.
- Sort state lives in `view` (`teamSort`, `teamSortDir`) — per device, no schema. Numeric columns
  run worst-first on the first press; **Data to runs the other way**, because its interesting end
  is the oldest export. **Nulls sort last in both directions**, or a team with no data wins the
  top of "shortest cycle time". Which way a column runs on a first press travels on the header
  button as `data-desc` rather than being re-derived in the handler.
- **The demo's Wagtail carries `stale: 9`**, shifting its whole history back nine days. Its own
  dashboard is untouched (every window hangs off the latest date in the data, so the picture moves
  with it); on All Teams it is the team with nine silent days dragging its rate down. Without a
  team like it the Data to column is a row of matching dates that looks like it does nothing —
  which is exactly what the demo rule exists to prevent.
- **One chart, and the reasoning behind that.** A line PER TEAM would need a categorical palette
  the theme pack does not have — only `--accent` and `--serious`, which every chart here uses as
  its two-series pair — and inventing colours locally is the drift the pack exists to stop. That
  ruled out the expensive version, and for a while it wrongly ruled out the cheap one too: the
  train's own AGGREGATE line needs exactly one colour, and the accent already is it. So All Teams
  carries the train's throughput over time and nothing per-team. A per-team chart still goes
  through `tokens.json` and the contrast gate first.
- **`drawTrainThroughput` is deliberately identical to the dashboard's throughput chart** — same
  type, colour, trend line and partial-period tooltip footer. It is the same measure, and a
  second styling for it would only invite the question of what is different about it.
- **The chart is held in its own `trainChart`, NOT in the shared `charts` registry.** That object
  is the dashboard's, and `renderDashboard` destroys every entry in it whenever the SELECTED TEAM
  has nothing plottable — which has no bearing on the train, and would have wiped this chart out
  from under somebody looking at a perfectly healthy roll-up. Pinned by a test that selects an
  empty team while standing on All Teams.

## The Work Item Age Chart (2026-08-20)

The fourth card in Health, and the only chart in the app whose points are ITEMS rather than
periods: every item still in flight, plotted at the age it has reached, in a column for its work
type. What must not regress:

- **It must never contradict the two tiles it sits beside.** `ageing.count` is the same set the
  work in progress tile counts and `ageing.agedCount` the same set the aged work tile counts,
  from the same dates and the same threshold; `ageing.median` and `ageing.p85` are the *same
  figures* the headline cycle time tile states, not a second calculation of them. All six are
  pinned in tests.html against `summary`, because a dashboard telling a stand-up two different
  things about one board would be wrong in the place nobody checks.
- **Aged means older THAN the threshold, never equal to it** (`r.age > agedDays`), matching the
  `<` in `agedCounts`. Get it wrong and the chart reports an item aged a day before the tile does.
- **Ages go through `spanDays`**, so the working-days setting reaches them exactly as it reaches
  the threshold they are drawn against — a chart whose dots and whose line disagreed about what a
  day is would be unreadable. And they are read as of `endDate`, like work in progress and aged
  work, never from `Date.now()`.
- **The three reference lines are labelled where they are drawn, by the `refLabels` plugin, not
  in a legend.** Five legend entries wrapped to two rows and took a sixth of a 300px card, and
  they cost a lookup as well as the space. Only the two dot styles keep legend entries — a shape
  does need a key. The labels are right-aligned because columns are ordered busiest-first, which
  makes the right-hand edge the reliably quiet corner.
- **Each label sits in an OPAQUE CHIP, and that is load-bearing, not decoration.** The first
  version drew bare text floated above its line. It read perfectly on the demo and badly on
  Charles's real board, reported the same day, in two ways at once: the dashes ran straight
  through the words, and where two lines land a day apart — an ageing threshold of 14 against an
  85th percentile of 13 is an ordinary board — the nudge stacked both labels into one smudge of
  text and dashes. The chip is painted in `--surface`, so it interrupts its own line and
  separates one label from the next, and it is centred ON the line rather than floated above it,
  which is what makes the interruption read as a name rather than as a gap. Its cost is that it
  can cover a dot; that is why it is as narrow as the text allows, and why the right-hand edge is
  kept quiet. Don't go back to bare text.
- The plugin nudges a label clear of the one above rather than dropping it — silently losing one
  is worse than moving it, and the chip's colour still says which line it belongs to.
- **The wording beside each line is built in `derive()`** (`ageing.lines`), with the rest of the
  app's figures-in-a-sentence; the chart layer adds only the colour and the dash, which are the
  one part of a line that is a drawing decision. Those labels drop a trailing `.0` where `num1`
  would keep it: a tile wants figures lining up on the decimal point, a chart label wants every
  character it can give back to the chart under the chip.
- **Columns are work types, and that is a compromise the README states.** The canonical chart puts
  workflow STAGE on the x axis, which needs the status-history export blocked time and flow
  efficiency are both waiting on. `AGE_UNTYPED` and `AGE_OTHER` are pushed to the right-hand end
  regardless of count — neither is a work type, and keeping both there is what preserves the quiet
  corner above. `AGE_MAX_COLUMNS` counts REAL types only, so an untyped item can never push a real
  one off the chart.
- **Dot positions are computed in `derive()`, not improvised by the renderer**, so the spread is a
  pinned property of the data. Sorted by age within a column, spread across `±AGE_SPREAD`, and a
  column of one sits dead centre on its own tick.
- **The dots carry no ticket key and never will** — this app stores none. The tooltip gives the
  work type and the start date instead, which is what finds the item again in the export. Any
  future change here must not smuggle identifying text onto the chart; the storage rule at the
  top of this file is the reason.
- Aged dots are told apart by SHAPE as well as colour (a `--serious` triangle against accent
  circles), the same rule the defect and cycle time charts follow, and the same non-RAG pair.
  Nothing is coloured "bad": the threshold is one the reader set.
- Health went from three charts to four, so the defect rate card lost its `solo` class. The class
  and its CSS stay — the next odd group would otherwise rediscover the problem.

## The Monte Carlo Forecast (2026-08-20)

The fourth chart group, and the only one that looks forward. It resamples this team's own
recorded throughput ten thousand times and reports how often each outcome came up. What must
not regress:

- **It deals from `wholeThroughput`, and nothing else.** That is the same set the
  completed-per-period and steady delivery tiles read, so the three can never disagree about
  which periods they describe. Dealing the part period in would deal a bad week that never
  happened; dealing individual DAYS instead would quietly assume each day is independent of the
  ones around it and report a narrower spread than the team ever showed. Whole periods keep the
  shared variation — a freeze, an incident, a holiday week — that is the honest part of the
  answer.
- **The two confidences run OPPOSITE WAYS, and this is the easiest thing in the app to break.**
  A date is safer the later it is (85% confidence → the 85th percentile); a count is safer the
  lower it is (85% confidence → the *15th*). `daysAtConfidence` and `countAtConfidence` exist so
  that no caller ever passes a percentile, and everything on screen is labelled by confidence
  for the same reason. Pinned from both ends in tests.html — including against the trials
  themselves, not just against the percentile function that produced them.
- **Seeded with a constant (`FORECAST_SEED`), never `Math.random()`.** A forecast that moved a
  day between renders would read as the app being unsure of itself, could not be pinned by a
  test, and could not be talked through twice. The uncertainty is stated by the spread on the
  chart. `seededRandom` was lifted out of the demo section into the maths section when this
  landed — it now has two callers and both pass a constant.
- **`forecastItems` and `forecastDate` live in `view`, NOT in `state`.** What you are asking the
  forecast is a position on this device, like `activeTeamId`. That keeps them out of the synced
  document entirely: **no SCHEMA bump, no whitelist entry, no place in a share payload** — a
  link's recipient gets the defaults and asks their own question, which was verified against a
  real share link (the visitor can change the question and localStorage stays empty). Both are
  validated in `derive()` at their point of use, like `bucket` and `filterDisplay`; a value that
  is not a positive number falls back to the default rather than being clamped up to 1, because
  a cleared or negative box is nonsense input rather than a small request.
- **The eight-whole-period floor is a refusal, not a warning.** Below it both cards hide their
  chart and name the control that fixes it. With four observations the shape of the answer is a
  fact about which four periods you hold. Reachable from the demo by grouping it by month over
  the default 3-month window, which is why that case has a test.
- **Answers are stated in DAYS though the sample is dealt in periods.** The period that crosses
  the finish line is interpolated into — ten items reached three items into a week that
  delivered five is three fifths of that week. Without it a weekly team answers "2 weeks" to
  nearly every question and the chart is four bars wide; the first build did exactly that, and
  its 50% and 85% answers were the same date. `periodsToDays` rounds UP, because a promise that
  rounds down is the wrong kind of wrong.
- **The shading is one hue in four steps, by STRENGTH and not by darkness.** `tint()` mixes
  toward each theme's own surface, so the faded end is near-black on Midnight and near-white on
  Light — "darker is safer" would be backwards in half the themes. Never RAG: the app states
  figures rather than judging them, a 50% answer is not "bad", and a red/green ramp is
  unreadable to the person most likely to be handed a forecast in a room. The answer rows carry
  the same four fills as swatches, which is what saves the shading from needing a legend.
- Adding the target date meant adding `input[type="date"]` to the app's own base input rule —
  without it the box kept the UA's 2px border and zero padding and sat 10px shorter than the
  number box beside it. Golf Handicap's rule already listed it. **Not theme drift**: the pack
  owns the two date-specific rules (the 16px touch floor and turning the native appearance off),
  the control's box is each app's own.

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
  is mirrored in the other, including the cross-`applink`. That link lives in the
  **footer** since 2026-08-20 (it sat in the header beside the title before), where
  it replaced the plain-text cross-link on the `.privacy-links` line — one crossing
  per page, not two. The footer is a flex row: the notes wrapped in `.footnotes`,
  the link after them with `margin: 0 19px 0 auto` so it sits at the right edge
  bottom-aligned with the last note (the 19px mirrors the notes' indent) and wraps
  onto its own line, still right-aligned, on a narrow window. `.brand` carries the
  `margin-right: auto` that pushes the header controls right.
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

## Fields, Dialogs and Scroll Boxes (2026-08-20)

- **Every modal opens through `openModal(dlg)`, never `showModal()` directly.**
  `showModal()` runs the spec's dialog focusing steps — the `autofocus` element, or failing
  that the FIRST FOCUSABLE one — and there is no `autofocus` anywhere in the file, so which
  dialogs raised a phone's keyboard was decided entirely by which happened to open with a
  text box — Teams & boards did, because its markup opens on a
  team-name box; Back up, Share, Tidy up and Help did not. The keyboard then covers half the dialog before it has been read. On a
  COARSE pointer `openModal` moves focus off the field and onto the dialog itself.
  - **Focus still goes INTO the dialog** — that part is not optional, or a keyboard or
    screen-reader user is stranded outside a thing covering the page. The CONTAINER is what
    the ARIA practices offer for this case: every dialog here carries `aria-labelledby`, so
    it announces itself, and Tab reaches the first field. `tabIndex` is set at open rather
    than in the markup — a dialog is a focus target only for that moment.
  - **`(pointer: coarse)`, NOT a width breakpoint.** The keyboard is a fact about touch, not
    width: a desktop window dragged narrow keeps its click-and-type, a wide tablet is spared.
  - **`raisesKeyboard(el)` is pure and pinned** over `{tagName, type}`, so the type list is a
    test rather than a rediscovery. It is a no-op when the browser landed on a button, a
    picker or a disclosure, which is what leaves those dialogs exactly as they were.
  - A dialog that genuinely wants the keyboard needs no special case: call `openModal` and
    then focus the field yourself afterwards, which simply wins.
  Ported from Money Map, and mirrored across the app family the same afternoon.
- **A box you land on has its contents SELECTED**, so typing replaces the value
  rather than running on to the end of it — one delegated `focusin` listener
  (`SELECT_ON_FOCUS`), which bubbles where `focus` does not, so it covers every
  field including the ones built a moment before a dialog is shown, with nothing
  to remember when adding one. Ported from Money Map 2026-08-20 and now in every
  app in the family. Four things it must keep doing:
  - **The type list is a WHITELIST.** A date, a checkbox, a range and a file
    picker have no text for `select()` to take, and a type nobody has thought
    about is left alone rather than silently swept in.
  - **A TEXTAREA is never touched** — the `INPUT` check does it. A box you write
    several lines into should not be one keystroke from gone, and unlike a
    mistyped figure there is nothing on screen to retype it from.
  - **`data-keep-caret` is the by-hand opt-out for a single-line PROSE field**,
    which the TEXTAREA rule cannot catch. Nothing here carries it — a team name and a
    work-item label are values, not prose — but it is wired so the next one has it.
  - **The one-shot `mouseup` guard is load-bearing, and only for a POINTER-driven
    focus.** A click focuses on mousedown and then places the caret on mouseup,
    which collapses the selection made a moment earlier: without it the feature
    works from the keyboard and looks broken with a mouse, which is how everybody
    would meet it. A `{once:true}` listener left hanging after a Tab would sit
    there and eat the caret placement of a later, deliberate click — hence
    `focusFromPointer`, set on a capturing `pointerdown`. Clicking a second time
    places the caret normally (the field is focused by then, so no focusin
    fires), and that is the way back in for editing rather than replacing.
  It does not fight `openModal`: on a touch screen focus goes to the dialog, so
  nothing is selected until you tap a field.
- **A horizontal scroll box must carry `position: relative`.** `overflow-x: auto` is the
  whole design for `.table-scroll` — content too wide for a phone scrolls inside its card and the
  page stays the width of the screen. On iOS that only half worked: WebKit clipped it on
  screen but still counted its full width in the DOCUMENT's scrollable area, so the page
  itself became horizontally scrollable into a band of nothing. Measured on iOS 27 at a
  402px viewport: `documentElement.scrollWidth` 906 against a 402px body. `position:
  relative` is what fixes it and nothing weaker does — a stacking context alone
  (`isolation: isolate`) leaves it at 906, and so does spelling out `overflow-y`;
  `contain: paint` works but takes the containing block for fixed descendants with it.
  Chrome and Firefox were always right here, so it is only ever visible on a phone.
- **Date fields are `appearance: none`, and that lives in `theme.css`, not here.** WebKit
  ignores an author `box-sizing` on a natively drawn control, so `width: 100%` on a date
  input meant the column PLUS its padding and border and the box hung over its neighbour.
  See rule 11 in the theme pack's CLAUDE.md; don't re-fix it locally.
