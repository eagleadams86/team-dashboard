# Team Dashboard ("Flow Metrics" on screen)

Kanban/flow metrics from pasted Jira exports — throughput, cycle time, lead time,
net flow, aged WIP — per team. One file, `index.html`, no build step. Deployed via
GitHub Pages: https://eagleadams86.github.io/team-dashboard/
(The on-screen name is **Flow Metrics**; every identifier still says team-dashboard.)

Charles pastes data from his **work Jira** into this app. That fact drives the two
non-negotiable rule sets below. The sibling app is Sprint Velocity
(`~/claude-sprint-velocity`) — its CLAUDE.md is the fuller reference for the
conventions the two apps share (chrome, themes, share links, testing); this
file records what is specific to this repo and what must never regress.

## Pinning the Tabs and the View Controls (2026-09-03) — no schema change

Charles: *"let a user pin this whole section to the top, similar to how we did it
with money map."* The section is the tab row AND the control strip, so they are
held in one band, `.pinbar`, and stuck as one. Money Map pins its two toolbars
separately because its year strip belongs to one tab and unpins on its own on a
phone; here the two rows are shown and hidden together, so one band with one
measured offset is the whole of it. Everything else is its shape: `data-pin` on
`<html>` set by the head script before first paint, `--pin-top` measured from the
header's real rectangle, `td-pin` in localStorage, off by default.

**Four things this app had to work out that Money Map did not.**

- **The band is a FLEX COLUMN, and that is load-bearing.** The rows' own bottom
  margins are what space this section, and a plain block would let the last one
  collapse straight out through the bottom of the band — so pinned, the page
  would scroll through an 18px window under the controls. In a flex container
  margins never collapse, so the same 18px stays inside the box that paints it.
  **Nothing moves when you pin**, which the suite asserts by measuring the
  panel's top and the document height both ways.
- **THE WELCOME CARD WAS IN THE MIDDLE.** It sat between the tab strip and the
  control strip in the markup, so the two could not be wrapped without wrapping
  it too — and a sticky band would then have pinned the welcome card to the top.
  It moved below the controls. Nothing reads its position: it takes the whole
  page when it is up (`data-welcome`), and everything around it is hidden.
- **A phone pins the tab row and nothing else**, and `display: contents` is what
  makes that work. A sticky box can only stick INSIDE its parent's box: left as a
  band, `.tabrow` scrolled away the moment the band's bottom passed the top of
  the window — 536px down a phone screen. With `contents` the band generates no
  box and the row's containing block is `<main>` again. Applied at that width
  whether or not the pin is on, so the box tree is the same either way and the
  toggle stays free of reflow. The numbers are measured, not guessed: the band is
  170px at 1265 and **537 at 375, against a header of 173** — 709 of an 812px
  screen.
- **`display: contents` also breaks the measurement, and that is the bug to
  remember.** Such an element is still `position: sticky` to the cascade and its
  rectangle is 0×0, so `stuckPin()` happily picked the band and wrote a
  `--pin-clear` that cleared nothing. It asks for both now.

`measurePinTop()` runs from `selectTab()` and `renderEmptyState()` as well as
from the ResizeObserver: the band's height changes when the control strip goes on
Your Data and when the welcome card takes the page, and **an observer is
delivered with the next rendering step, which a background window does not
have.**

23 checks in `pinning the tabs and the view controls`. **The suite's frame is 1px
wide, so the phone rule is the only one that ever matches in it** — the test
resizes `#app` to 1265, measures, resizes to 375, measures, and puts it back.
That is the only way a media query is tested by firing rather than by grepping.
It also scrolls the frame to the top first: groups above it leave the frame
scrolled, and the real press is a hit test, which answers null for a button
above the viewport.

**The tabs became one scrolling row on a phone the same day** (asked for after
Sprint Predictability's, and for the pin's sake). Three tabs and the button come
to about 370px, which is just past a 375 screen once `.shell`'s padding is off,
so the row wrapped and the pinned band carried 116px where 42 would do. `nowrap`
plus `overflow-x: auto` at the SAME 720px as the pin rule, so the phone has one
breakpoint rather than two a pixel apart. It is harmless where they fit — a
nowrap row only scrolls when there is something to scroll.
- **The pin button is NOT in the scroller.** That is the second reason `.tabrow`
  exists as a wrapper; inside `.tabs` it would scroll away with them.
- **selectTab() nudges the chosen tab into view**, only when it is actually off
  an end, by RECTANGLE and not `offsetLeft` (whose offsetParent is the page), and
  **never `scrollIntoView`** — that is free to scroll the PAGE to satisfy the
  vertical axis. Money Map's arithmetic, and Sprint Predictability's.
- **The suite asserts ONE LINE, not "it overflows".** Whether the row overflows
  depends on how many tabs are on offer, and All Teams is away below two teams —
  which is the state that frame is in by the time it gets there. It measures the
  row against a TAB rather than against a literal, since the row also carries the
  pin's 20px band and a scrollbar.

**Sprint Predictability has both of these now**, and it shares this app's chrome.

## WIP vs Month Got Its Own ⓘ (2026-09-03) — no schema change

Charles asked what the column meant. That is the finding, not the request: the
note existed, and the arrangement meant to lead him to it could not be followed.

- **The cross-reference was unfollowable.** `teamColumns` gave dots only to the
  two columns unique to this table, on the rule that every other column is a
  dashboard tile laid on its side and the tile carries the note. True — except
  that tile is labelled **"WIP vs throughput"** and the column is **"WIP vs
  month"**. Same figure, two names, and nothing on screen says so. **A
  cross-reference that depends on a reader guessing two labels are the same
  thing is not a route.** The obvious alternative — renaming one of them so they
  match — was left alone: Charles reads both, and it is his call.
- **The window is named for THIS heading**, `teamWipRatio` → *WIP vs Month*,
  following `teamTrend` and `teamDataEnd`. Opening the tile's *Work in Progress*
  window from here would have told a reader who came about the ratio that the
  window is not for them — the naming half of one-dot-one-explanation.
- **It earns its place with a fact the tile's note cannot state**: the
  denominator is a month counted back from the newest date in that team's own
  data, **not the window on screen**, which makes this the one column here that
  does not move when the window does.

**IT COST THE TABLE ITS FIT, and that is the part to remember.** A dot is 40px —
2px of button padding, a 10px margin, a 16px circle, a 12px margin — and this
table had NOTHING spare: ten columns came to exactly the width of an ordinary
1265px window, so the third circle took it 38px over and into the sideways
scroll the original two-dot decision was written to avoid.

**Letting the headings alone wrap buys it back.** `table.data td` is `nowrap` and
so is every other heading in the app — a figure broken over two lines is worse
than a wide column — and `#allTeamsTable thead` is now the one exception, scoped
by id so the Loaded Data table's headings are untouched. The header row goes from
36px to 56px and the table fits again with room over. **Both halves are pinned in
the suite**, because either alone puts it back in a scroll: the dot count, and
the computed `white-space` plus a stripped-source check that the rule still names
the table by id.

## Stepping Between Charts in Full Screen (2026-09-03) — no schema change

Charles: *"when a chart is in full screen mode, add left and right arrows near the
'leave fullscreen' button that allows the user to rotate through the charts on that
screen, while remaining in fullscreen."* Two things decide how this is built.

- **The arrows live in the OVERLAY, not in the card.** A step moves one card out of
  `#chartMaxi` and another in; a button inside the card is detached under the pointer
  mid-press, and a detached button takes the keyboard's focus to `<body>` with it — press
  Next once and there is nothing left to press. In the overlay they never move, so the
  arrow you are on stays the arrow you are on for a whole walk. This is the same class of
  trap as the `.chart-max` icon rewrite (`[[real-press-not-btn-click]]` in memory), reached from the
  other side.
- **"That screen" is the SUB-TAB**, `card.closest('[role="tabpanel"]')` — so from Cycle
  Time the walk reaches the other Flow charts and never the Health ones. Stepping right
  must land somewhere the reader could have got to by scrolling. The All Teams panel is a
  list of one, so it gets no arrows at all rather than a loop back onto itself.
- **The walk is re-read on every press and on every render, never captured on the way
  up.** The header stays live up here on purpose; change team and lead time can go. That
  is why `dressStepBtns()` hangs off `syncMaxiButtons()` as well as off open and close.
- **The card returns to its own seat before the next one leaves its own**, so the grid
  never holds two `.chart-slot`s and the order the next walk is read from is the real one.
  Nothing else the overlay owns is touched by a step — not the scroll position, not the
  inert shell, not the measured `--maxi-top`: it is the same window with a different chart
  in it.
- **The arrow keys do the same**, except inside a control — the team and theme pickers are
  in the header and stay usable while a chart is up, and Left in a `<select>` is the
  select's.
- **`.maxi-nav` is positioned from a sum that includes the card's 1px BORDER**
  (20 + 1 + 13 down; + 26 + 6 across), because an absolutely positioned box is offset from
  its containing block's *padding* box — `.chart-max`'s own `top: 13px` therefore lands a
  border-width further in. Left out, the three buttons are a pixel out of line, which is
  what the first draft did. Same lesson as `[[inset-grows-from-padding-box]]` in memory.
- **The heading's clearance is on `#chartMaxi.has-nav`**, so a screen with nothing to walk
  carries no reserved space beside its chart's name.

- **The arrow-key handler skips ARIA ROLES, not just form controls.** Money Map
  found it on 2026-09-03: its Net Worth card carries an "as of" radio pair INSIDE
  the card, so it is still reachable while that card fills the window, and Right
  both moved the month and stepped the chart. A `<button role="radio">` is not an
  `<input>`. The guard names radiogroup, tablist, listbox, menu, menubar, slider,
  spinbutton, grid and tree, and the same list is in all four apps — nothing here
  puts such a control inside a chart card TODAY, which is exactly why it would be
  missed the day something does.

27 checks in `walking the charts on that screen without coming back down`.

**Ported the same day**, so a change belongs in all four: **Lottery Portfolio** (no tabs —
it walks the whole page, minus folded sections), **Sprint Predictability** and **Money
Map** (both walk `#views`, which their renders rewrite wholesale, so the walk is always the
tab the reader is on). **Money Map's arrows sit in the heading BAND**, not floating over
the card's corner, because that corner is its fold control — the same divergence its ⤢
already had, and the reason it is the only one of the four whose step BUTTONS have to hand the
focus back by themselves after a step. The KEYS are a different case and every app has it:
opening puts the focus on the card's own ⤢, and a key step carries that button back into the
inert page — so `maxiStep()` moves a focus that is gone, or outside the overlay, onto the new
card's ⤢ (2026-09-04; see "Fixes From the 2026-09-03 Audit" at the end of this file).
**Golf Handicap and the starter draw one chart each**, so there is
nothing to walk; both record that, and where to take the walk from if a second arrives.

## A Settings Window Is a Stack, Not a Column (2026-09-02) — no schema change

Charles, of the Settings window: *"this window is big and a bit hard to read. can you add
section separators or something?"* It held **six unrelated settings under two headings** —
everything from the ageing thresholds to the outlier block sat under *Labels & Work Types*,
which named none of it — so the window read as one undifferentiated column of 13px prose.

- **Six sections now, each in its own `<section class="manage-sec">`:** Labels & Work Types,
  Aged Work, Features, Working Days, Unusually Long Items, Work Type Filter List. The list is
  pinned in the suite as a whole, so a setting added here has to say which section it belongs
  to or add one.
- **`.manage-sec` is one rule and some spacing** — `border-top: 1px solid var(--border-strong)`
  and nothing else. No new colour, no fill, no shadow (pack rule 14), and `.manage-head` is
  untouched. `--border-strong` rather than `--border` because at `--border` the line is barely
  visible on midnight, which is the whole thing that was asked for.
- **The spacing moved off the heading rows.** Each was an inline `margin-top` — 16px, 18px,
  20px, four different values across two dialogs by 2026-09-02. A section is now one element
  to move and the gap above a heading cannot drift per dialog again.
- **The first section takes the spacing and not the rule** (`:first-of-type`), because above it
  is the window's own heading or the sentence describing the whole window, and a line under
  either reads as the end of a section rather than the start of one.
- **The Features hint came out of the grid the same day** (reported an hour later): five
  lines of prose in the second cell beside a one-line field, which is the one thing this
  dialog's own rule says not to do — the reading order went across the window instead of down
  it, and the box sat stranded in the middle of its section. It now runs full width beneath
  the field, like every other section's explanation, and the field takes the whole row because
  it is the only cell in its grid. **The suite pins the rule for the whole window**: no `.hint`
  inside a `.grid`.
- **Its `.manage-note` was taken out in that change and put straight back by Charles.** The
  sentence repeats the label under it, but every other section opens with one, and being the
  only heading with nothing under it was the more visible oddity — consistency of the shape
  beats economy of the sentence. Pinned too: no section is left as a bare heading.
- **The note about a blank Type moved into the section holding the box it points at.** It says
  "the defect text above" and had drifted to the foot of the outlier block, four sections below
  that box. Pinned, because the end of the window is where an appended note lands.
- **Teams, ARTs & Stages took the same treatment in the same change**, and so did Sprint
  Predictability's *Targets* and Golf Handicap's *League Handicap*. Neither sibling window
  would have earned the complaint on its own — they are short — but the four are the same
  screen wearing four names, and a divider in two of them is drift rather than design. See the
  shared settings-window furniture note in Sprint Predictability's CLAUDE.md.

## A Heading May Teach the Vocabulary (2026-09-01) — no schema change, DECIDED WITH CHARLES

**This reverses "there is no adopt-this-heading button", and it is the reversal the
*Workflow Stages* section asked to be made deliberately.** The rule's stated reason was
"no status name is ever stored", and that stopped being true on 2026-09-01 when the
vocabulary shipped. What survived the change is the real question — *what evidence
admits a word into storage?* — and the answer for a heading turns out to be a different
kind of evidence from the repetition gate, not a weaker one.

**Three rules, all three required.** A wrapped heading offers its status to the
vocabulary only when:

1. the heading carries the `Days in` / `Time in` wrapper — the export declaring, in its
   own words, that the column below it is a number of days in a status;
2. **every filled cell under it is a plain day count** (`cleanStageDays`), so there is
   no prose in that column to be the thing that got stored; and
3. the remainder passes `cleanStatusLabel` — the same whitelist every adopted status
   goes through: 40 characters, six words, no punctuation a status does not have.

- **Rule 2 is the safety argument and it is worth stating why it is strong.** The
  repetition gate exists because a status VALUE can be prose — a summary column
  mistaken for a status column — and it works by measuring a property of a column of
  values. A single header cell has no repetition to measure, so that gate cannot be
  applied here at all. What CAN be applied is the column underneath: prose does not sit
  under a column of numbers. One unreadable cell refuses the whole heading.
- **An EMPTY column passes rule 2 vacuously, and that is deliberate.** The case this
  feature exists for is a status nobody is sitting in — `Days in CERT` with nothing in
  it — which is exactly why the word appears in no cell and cannot be learned any other
  way. An empty column cannot hold prose either. Pinned, because it looks like an
  oversight and is the point.
- **`STAGE_OPEN_ENDED` is excluded**, so `Done never reaches your list` is not reversed
  through the back door. Those are the statuses whose day count is not a duration; the
  app already refuses them from values and warns when a stage claims their column.
- **Headings are adopted LAST, after every row**, so a status somebody is actually
  sitting in takes a slot before one only a heading knows about. If the list fills at
  `STATUS_MAX`, the one still in use is the one kept.
- **`statusesNew` is now the slice up to the heading pass, and `headingStatuses` is the
  rest.** Two sentences in the report, never naming the same word twice, because the
  reader's next move differs: a status off a cell is already grouping the age chart; a
  status off a heading does nothing until it is ticked into a stage.
- **The report says what it can SEE.** The obvious sentence — "nothing is sitting in
  these" — is a claim about a board this app cannot check on an export with no Status
  column. It says instead that the word reached it through a heading and through no
  cell it read. Third time this trap has come up in one feature; see the note on the
  Time in Stage card.
- **`stageHeadingLabel` is the case-preserving twin of `stageHeadingBare`.** Matching
  wants the normalised form because case is noise between exports; the vocabulary wants
  the spelling the export used, because the reader has to recognise the word in a list.
  Where the raw stripper cannot cut (a heading like `Days-in-Code Review`, which
  normalises fine but does not match the raw pattern) it returns '' and the heading
  teaches nothing — one status to type, never a wrong one.

## A Status on a Row That Did Not Load (2026-09-01) — no schema change

The third report in the same chain, and the door still shut after the first two:
Charles had a `Days in Ready for Work` column and no way to match it, because
"Ready for Work" was not in his status list to tick. Everything sitting in that
status is untouched backlog — raised, never started, no dates — and those rows are
dropped by the `undated` return **before** the status block runs. 559 rows of his
paste went that way.

- **Two questions had been answered by one block.** WHICH STATUSES EXIST is a claim
  about the reader's workflow; the unmatched-status count and the bad-cell tally are
  claims about the rows that LOADED. The block sits below the `undated` return for the
  second reason — counting dropped backlog rows once made the report read "400 items
  had a status no stage answers to" against a perfect set-up — and that reasoning is
  untouched and still load-bearing. What moved is only the learning.
- **`learnStatus` takes the word and NOTHING else.** No id on the row (there is no
  row), no unmatched tally, no refusal counted. The refusal counters stay claims about
  loaded rows, which is what they say on screen.
- **The guard is unchanged, and that is the safety argument.** The value comes from the
  same column, which has already passed leg 2's repetition gate over every row in the
  paste, and every word still goes through `cleanStatusLabel`. A dropped row is not a
  weaker source — it is the same column, one row further down. Read through
  `cols.statusUsable` like every other reader of that column, so a prose-like column is
  not half-read on the way past either.
- **Still in-flight only.** Every row reaching that return has an empty completion date,
  so `Done` does not arrive by this door.
- **The tick is offered on the same terms the main path offers it**, so a stage already
  aliased `Ready for Work` does not have to be re-ticked because the only rows carrying
  that status were ones the app could not measure.
- **The other half of the report — a status with nothing in it anywhere — was put to
  Charles the same day and he took it.** See *A Heading May Teach the Vocabulary* below.

## A Ticked Status Claims Its Column (2026-09-01) — no schema change, DECIDED WITH CHARLES

The second half of the section below, and it only showed up once the first half was
shipped and Charles pasted his export again: the report still said no stage claimed
any of eighteen day-count columns. **His stages were grouped by TICKING statuses,
and ticks write `stage.statuses` (ids) while the heading matcher read `stage.match`
(typed text).** The age chart grouped perfectly, the alias box was empty, and the two
halves of the feature could not see each other.

**This was put to Charles as a decision rather than fixed in passing**, because the
*Workflow Stages* section says this area is one to decide deliberately and write
down. He chose it. The alternatives offered were leaving aliases as the only heading
matcher (he types his statuses once) and auto-filling the alias box on tick (the
label stored twice, and an untick with no obvious meaning).

- **`stageColumnsFor(header, stages, statuses)` now also matches a heading against the
  LABELS of the statuses ticked into each stage.** The vocabulary is threaded from
  `parsePastedRows` through `detectColumns`; all three call sites already passed
  `state.statuses`.
- **NOTHING NEW IS STORED, and that is the entire permission for this.** The label is
  already in `state.statuses` — it got there through the repetition gate and
  `cleanStatusLabel`, the argument that replaced "no status name is ever stored" — so
  comparing a heading against it is the same act as comparing it against a typed
  alias: the heading is compared and discarded with the rest of the paste.
  **This is NOT the "adopt this heading" button**, which stays absent and stays
  forbidden: that one would write a column heading INTO storage. The direction is the
  whole distinction.
- **A ticked status is matched EXACTLY, on the same terms a typed alias is.** It
  inherits the rule rather than a friendlier version of it: `Days in Waiting on
  Development Env` is still not development time, and a ticked `Done` still trips the
  open-interval warning.
- **Typed aliases win, and the two passes are WHOLE-LIST rather than interleaved per
  stage** — every alias is read into the map before any tick. A reader who typed
  something was being specific; a tick losing to it needs no report, because
  `sanitizeStages` already makes one status belong to exactly one stage.
- **The vocabulary a parse starts from, never the one it leaves behind.** `readAs`
  gets `statusList`, the copy taken before adoption, so a status this paste is
  adopting for the first time cannot claim a heading in the same paste. The tick that
  joins it to a stage is the reader's act and comes after they have seen it arrive.
  Pinned — the alternative is a paste that invents its own rule mid-parse.
- **Three pieces of copy said "only a typed alias can match a heading" and are now
  amended, not deleted**: the stages dialog's last paragraph, the note over
  `stageForStatusId`, and the header comment on the stage feature. What is still true
  is the narrower claim, and it is worth keeping: a status this app has never been
  SHOWN is not in the list to be ticked, so a typed name remains the only way to match
  a heading naming a status that has never appeared in a Status column, or an old
  spelling the board has since renamed. That is what the box is for now, and the
  dialog says so.
- **The Time in Stage card's empty state was making the report's old mistake**, one
  card along: "your export says where each item IS, but not how long it has been
  there" is a claim about a file the card cannot see, and on this export it was
  wrong — eighteen columns of durations sat in it. It now says what is missing, not
  why, and points at the parse report, which is the one place that counts them.

## A Real Export Wraps Its Status Names, and the Report Lied About It (2026-09-01) — no schema change

Reported by Charles with a 1,781-row Time in Status export: twelve day-count columns,
stages set up, and *Time in stage* empty. Two separate faults, one visible and one
not, and the invisible one is the more instructive.

- **The match now reads a wrapper off the HEADING: `Days in`, `Day in`, `Time in`,
  `Time spent in`, anchored at the front, on the normalised form.** Nothing else is
  stripped. A real export heads its columns `Days in Code Review`; the aliases box
  asks for a status and says so; `code review` never met `days in code review`, so
  every duration in the file was dropped. The whole heading is still tried FIRST, so
  an alias typed out in full — the workaround, and what the README told people to do
  until today — keeps working, and so does a board with a status genuinely called
  that.
- **This is NOT the substring rule, which stays turned down.** What is left after the
  phrase comes off must still equal an alias in full: `Days in Waiting on Testing Env`
  strips to `waiting on testing env`, which an alias of `Testing` still does not match.
  The anchor is what makes that true, and `Cycle days in Testing` is pinned as
  untouched for the same reason. **`Days Blocked` has no "in" and so cannot be reached
  by this at all** — the Flagged overlay must never become a stage, and this must not
  become the change that quietly let it in.
- **The cost the fix takes on, and pays for on screen: a bare `Done` alias can now
  reach `Days in Done`.** Only an alias typed out in full could before. That column is
  an open interval — it runs to the moment the export was taken and grows on every
  re-run — so the parse report now names the column, names the stage it feeds, and
  says to take the status off unless it was meant. `STAGE_OPEN_ENDED` holds the rest
  (`closed`, `resolved`, `cancelled`, `rejected`, `abandoned`). **The column is still
  CLAIMED**: refusing a column a stage asked for would be the app deciding what
  somebody's workflow means, which is the thing the alias design exists to avoid. Warn,
  do not overrule. The flag is read off the BARE form however the column was claimed,
  so the long-form alias is caught on the same terms.
- **THE REPORT USED A PROXY FOR A QUESTION IT HAD NO ANSWER TO, and that is the bug
  worth remembering.** It chose between "none of your headings matched" and "no day
  counts in this paste" by asking whether a Status column had been found. On this
  export it printed the second: a *reassurance*, stated as a fact about somebody's
  data, on a paste with twelve day-count columns in it. A wrong number is what this
  report exists to prevent, and a wrong reassurance is the same failure with the
  number left out. The two branches are now one: the fact both cases share is stated
  first, and only the sentence after it varies — on `columns.stageDurationCols`, which
  counts columns whose heading SAYS it holds days and which no stage claimed.
- **`stageDurationCols` is a heading test, deliberately not a shape test on the
  values.** A column of plain numbers is also story points, an estimate and a comment
  tally; a report that nagged about alias spellings every time somebody pasted an
  estimate column is a report people stop reading. A heading carrying the wrapper is
  the export saying in its own words what the column holds, and that is evidence. It
  is a count for the report and is never read into anything.
- **Still no heading is ever echoed.** The report names columns by position and stages
  by the reader's own name, exactly as before; the `Days in Code Review` in the new
  sentence is a fixed example in the source, not a cell out of the paste. The
  serialise-and-grep assertion covers the wrapped shape now too.
- The dialog copy says *type the status, not the whole heading*, and says why: the bare
  status is the only spelling that also matches a plain export's **Status** column, so
  the long form gets you durations, no grouping, and no way to see why.

## A Filter Row May Name Several Work Types (2026-09-01) — no schema change

Asked for by Charles, who had already typed `Stories and Tasks → Story, Task` into
the list and wanted to know whether that was the right shape before it was built.
It was, and the reason is that **this app already had the convention twice**:
`featureTypes` and the stage aliases are both comma-separated lists of work-type
labels typed into one box. A third spelling of "several labels in one field" —
a multi-select, a chip editor, a checkbox list of the types found in the paste —
would have been one more thing to learn for a board that already knows this one.

**NO SCHEMA BUMP AND NO MIGRATION, and that is not a happy accident.** `value`
is the string it always was; only what reads it changed. A saved copy, a backup
file and a share link all still carry exactly what they carried, and — because
the family's five stateful apps HALT on data newer than the code — a reader on a
cached build is not locked out of their own dashboard by a settings nicety. The
worst an old build does with `Story, Task` is match nothing.

- **`filterTypes(value)` is the one rule about what a filter keeps**, and it
  returns `null` for "no filter" rather than an empty array, so a caller cannot
  read "everything" as "nothing matches". `derive()` reads it; so does
  `currentFilterValue()`, which decides whether the empty-state wording claims a
  filter is on. **Those two must never disagree** and briefly did while the
  wording had its own `=== 'all'` test: `All, Bug` removed nothing and still said
  it had. Any third reader asks `filterTypes` too.
- **"All" ANYWHERE in a list means no filter**, not a match on a type called
  "all". A list that already contains everything is everything. This is wider
  than the old rule (the whole value had to read `All`) and deliberately so.
- **MATCHING IS EXACT, PER ENTRY, and this is the half of the feature that needs
  the tests.** A list makes "starts with" the natural assumption, and a
  contains-match would have `Task` silently collecting `Sub-task`. On a
  dashboard an over-full view is worse than an empty one: empty is visibly wrong
  and gets fixed, slightly-too-full is invisible and gets reported to a stand-up
  as a fact. Two thirds of the new assertions are about what a grouped row
  LEAVES BEHIND, not what it collects.
- **The boundary got STRICTER, not looser.** The Value box needed room for eight
  labels (`FILTER_VALUE_MAX = FILTER_TYPES_MAX * 42`, stated as the arithmetic so
  raising one cannot silently truncate the other), and a flat 336-character cap
  would have let one 336-character sentence through where 120 used to sit —
  in a field that **travels in a share link**, so it is attacker-controlled text.
  So `normalizeSettings` stopped capping and started REBUILDING: `cleanFilterValue`
  holds every entry to `cleanWorkType` (dropped whole, never truncated), caps the
  count, and re-joins. It keeps the spelling it was given — it tidies a value, it
  never restyles one — and it runs only where a document arrives from outside,
  never on a keystroke, because rewriting a half-typed value under the cursor is
  the one thing a tidy-up must not do.

### Two things about the table, asked for in the same breath

- **The list reorders.** `moveFilter` rather than the `moveInList` beside
  `rowActs`, because that one finds its row BY ID and a filter row has none and
  wants none: it is a display name, a value and a position, and nothing outside
  the list points at a particular row. The cost is the focus restore, which has
  to look up the button at the row's NEW INDEX. Keep it — without it, moving a
  row with the keyboard rebuilds every button in the table and drops focus back
  at the top of the dialog after every single press.
- **The `All` row is greyed.** Its two boxes have always been `readonly` and have
  always looked editable: they took the caret, took a click, and swallowed every
  keystroke. **`readonly`, NOT `disabled`** — a disabled input is skipped by the
  keyboard and goes unannounced in several screen readers, so the row that
  explains what "no filter" means would stop existing for the reader who most
  needs it read out. There is an assertion saying exactly that, so nobody
  "simplifies" it to `disabled` later. The colours are two tokens the pack
  already has (`--text-muted` on `--surface-alt`, 4.73:1 at worst across the four
  themes) — no new palette value, per the a11y-without-drift rule.
- **`.rowacts .spacer`, and it is not cosmetic.** This is the only table in the
  app where SOME rows have a delete and one does not — the teams table drops
  every delete at once, when a single team is left — and right-aligning two
  buttons against three put the `All` row's ↑ directly under its neighbours' ↓.
  An empty box the width of the missing button, not a disabled one, because a
  button nobody may press is still a stop on the way through with the keyboard.
  Pinned by MEASURING the two arrows' left edges, not by looking for a `<span>`:
  a spacer of the wrong width is still a spacer. Verified to bite — removing it
  fails that assertion by exactly 36px, the button plus its gap.
- **Order is the one thing the `All` row can still change.** Its arrows are live
  and its delete is still hidden. What makes a row read-only is its NAME, not its
  position, and a reader who wants Defects at the top of a five-row picker is not
  touching anything.
- **THE ROW GREW FROM ONE BUTTON TO THREE, AND 72 PIXELS CAME OUT OF THE TEXT
  COLUMNS.** On a phone the Display box read "Stories an" and the Value box
  "Story, Ta" — truncated controls, which is exactly what the no-orphaned-fields
  rule exists to stop, and invisible at desktop width where the feature was built.
  Fixed the way the Teams table already fixes it: a floor on both text columns
  (150px / 170px, the wider one for the box that may hold a list) plus
  `.table-scroll`, so the table outgrows the dialog and scrolls in its own box.
  **Any future column added to a settings table has to be checked at 375px**,
  because the failure is silent at the width it was written at.
- **A row nobody has typed into yet is named by its POSITION.** The three buttons
  take their `aria-label` from `f.display || 'work type row N'`. The delete used
  to read the display name straight, so a fresh row's delete announced as
  "Remove " — an unnamed control, and the shape of thing an axe run with a
  placeholder in the box will happily green-light.

## Chart text is on the ramp, and in the app's face (2026-08-30) — no schema change

**`applyChartTextDefaults()` sets four Chart.js defaults before every
construction: `color`, `borderColor`, `font.family` and `font.size = fsPx('xs')`.**
Sprint Predictability's block, ported the same day the family's tooltips were
swept — these two apps share their chrome, so a chart in one and a chart in the
other have to be the same text beside each other.

This app already passed `font: { size: fsPx('xs') }` to every axis and title it
NAMES. What that left behind were the two it does not name — **the tooltip and
the legend**, at Chart.js's built-in 12px — and every one of them in Chart.js's
built-in Helvetica rather than the face the page is set in.

- **Set BEFORE the construction.** Chart.js copies the defaults into the chart at
  that moment and never looks at them again, which is why the call sits at the
  top of `renderChart` — and why `chartTrainThroughput`, the one chart built
  outside `renderChart`, calls it for itself. The suite pins that second call
  site by name, because it is the one that would quietly keep whatever the last
  chart happened to leave set.
- The explicit `font: { size: fsPx('xs') }` on the axes is the same value and is
  left in place.

## Only Numbers, Dates and Guarded Labels Are Ever Saved (2026-08-12/13, amended 2026-08-20/21, and REVERSED IN PART 2026-09-01 — see The Status Is Stored Now)

- **⌕ Find / ⌘K is Money Map's window, ported (2026-08-23)** — `searchApp(st, query)` is PURE over the state it is handed; two-character minimum, `SEARCH_CAP` of 80 with the overflow COUNTED so the cap is never silent, and the count span (`role="status"`) is the live region rather than the results list. **It adds no field and stores nothing**: a team name, an ART name, a stage name, a stage alias, a status label, a ≤40-char work type and a key-shaped issue key are the only words this app keeps at all, so Find can only ever reach what the whitelists already let in — do not "improve" it by matching anything that is not already stored. An item hit carries the INDEX into its own team's list — `rows` OR `features`, and `unit` says which (2026-09-01) — because that is what `openItemDialog` takes and it reads whichever list the Count switch is on; `goToSearchHit` sets the team AND throws the switch to `unit` before it renders. The item snippet reads the COMPLETION date only — the sort reads whichever date the row has, but an in-progress row shown as its start date reads as one that finished that day. `renderSearchResults` fences a shared view down to team and ART hits, since the data tab and the stages window are not there. `SEARCH_VIEW_LABEL` must name every visible tab plus `stage`; tests assert both directions, and the header-order sweep pins where the button sits. Mirrored into Sprint Predictability and Golf Handicap in the same pass — a change to one belongs in all three — and the Task Dashboard has one too, which makes six windows in five apps plus the starter.
- **THE WINDOW ITSELF IS PINNED, PROPERTY BY PROPERTY, AND THE SAME BLOCK IS IN ALL SIX APPS VERBATIM (2026-08-23).** 700px on 18px of padding — the Back Up & Restore window's size, the family's other fixed-width window — with the heading, the intro line, the box, the hit and its three lines, and the "Nothing matches" line all declared inside the `#searchDialog` block rather than borrowed from whatever quiet-text class the app happens to have. That borrowing is what made one window into six: 360px and 420px wide, a 320px box inside a 360px dialog, a hittab at `--fs-sm` here and `--fs-xs` there, `.04em` typed out beside `--ls-label`, and four different colours on the same sentence. A change to any of it belongs in all six. Two details worth keeping: `#searchDialog > p` is the DIRECT child only (the results list's message is a `<p>` too, and an id in that selector would out-rank `.searchresults .hint` and hand it the intro line's colour), and the block deliberately declares NO dialog chrome — backdrop, shadow, a field's touch-height floor, and the max-height Money Map divides by its own zoom all belong to the app's `dialog` rule and are shared with every other window it opens.
- **The header buttons wear a glyph in front of the word** (2026-08-21) — plain text characters, NOT emoji and not an icon font: one more file to fetch is the last thing a header painted this early needs, and a text glyph inherits the theme's colour for free, so it can never become the thing that carries a meaning by hue. Each is `aria-hidden` — the word beside it is already the whole label. The glyphs are Money Map's own where the same button exists there (`⇩` Back up, `↗` Share, `⚙` settings), so one action looks the same in every app, and `☰` is the list/manage one the three list-managing apps share. Added to Sprint Predictability, Flow Metrics, Golf Handicap and PAPTrack in the same commit.
- **A row is three ISO dates, one short work-type label, one issue key, one
  status id and a set of NUMBERS keyed by stage id.
  A ROW STILL HOLDS NO WORD** — the status is an id into `state.statuses`, which
  is where the words live; see The Status Is Stored Now.
  What follows was written before 2026-09-01 and is left standing because the
  clause above is the only part of it that moved.
  Nothing else. There are no free-text or comment fields anywhere in this app —
  don't add one.** A team carries a name, an optional `artId`, an optional
  project id — added 2026-08-20 and guarded by the same shape as the front of a
  key — and, since 2026-08-22, two optional NUMBERS it sets rather than measures:
  a work-in-progress limit and a cycle time target. `state.settings` gained a
  third number and a THREE-VALUE ENUM on 2026-08-24 (`outlierMode`,
  `outlierDays`) — the enum is pinned to a literal list in `normalizeSettings`,
  which is what keeps it a switch rather than a place to put a word.
  See the project id section below. `state.stages` carries names

  and aliases the reader typed, plus the status ids it groups; `state.statuses`
  carries the status labels read off an export. **Nothing on a ROW is ever a
  word, and that survived 2026-09-01 intact** — see The Status Is Stored Now,
  then the workflow stages section, which is the longest one in this file for a
  reason.
- **The issue key was added on 2026-08-20 at Charles's explicit request**, and it
  reverses the "no ticket keys, ever" line this file used to carry. It is worth
  knowing why it was allowed where a summary field never would be: a key is
  **structurally checkable**. `cleanIssueKey` tests it against `ISSUE_KEY_RE`
  (`^[A-Za-z][A-Za-z0-9]{0,9}-[0-9]{1,6}$`) and drops anything that fails, so
  the field cannot hold a sentence, markup, a formula or a name — there is no
  input that both passes and carries prose. That is a stronger boundary than
  `cleanWorkType`'s 40-char cap, not a weaker one, and it is the reason the
  request could be honoured without loosening the app's stance.
  **A second identifier is NOT precedent.** The next field somebody wants will
  probably be a summary or a status, and neither has a shape — the test to apply
  is "can a regex tell this from a sentence?", not "is a key stored, so why not
  this?".
  **A status was in fact the next thing wanted (2026-08-21), and it did NOT get
  in on this reasoning** — it could not, because it fails that test outright.
  What got in then was a stage the reader names in a dialog and a number of days.
  **It got in on 2026-09-01 on a DIFFERENT argument entirely** — a property of
  the COLUMN rather than of the value — and that argument is written out under
  The Status Is Stored Now. The sentence above still stands as written: the
  regex test remains the test for a per-row VALUE, and a status still fails it.
  Do not read the status's admission as loosening it.
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
  **`refOf()` was deliberately left alone when the key arrived (2026-08-20).**
  The temptation is obvious — the key is stored now, so why not name the problem
  row with it — but the reason the echo was cut was that the *line* is untrusted,
  and that has not changed: `refOf` reads whatever cells a possibly-mismapped
  column map points at. Adding the key there means reading a cell the parser has
  already decided is suspect. A test pins the current behaviour; if it is ever
  wanted, put `cleanIssueKey(at(cells, cols.key))` in and change that test
  deliberately rather than by accident.
- **Whitelists at every boundary**: `sanitizeTeams()` and `hydrateRows()` rebuild
  teams/rows from known keys. `hydrateRows()` also applies the paste boundary's
  date-ordering rules (started ≤ completed, created ≤ start) so a hand-edited
  copy can't smuggle a backwards span in as a 0-day cycle time; `normalizeSettings()` returns only
  `Object.keys(DEFAULT_SETTINGS)`; `loadView()` reads only `DEFAULT_VIEW`'s keys.
  A stray key on a hand-edited backup or share link must never ride along
  into the saved copy. **A new stored field must be added to the right
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
  genuinely newer copy. Sync's removal collapsed what the two DO — `save()` is
  now `persist()` plus the viewOnly guard — and the distinction is kept anyway:
  persist() means "write the shape down", save() means "the user changed
  something", and collapsing them would lose the only marker of which is which.)
- Settings labels, team names, ART names, stage names and status labels are
  short and capped; rows carry **two identifiers and no other** — the issue key,
  shape-checked, and a status id pointing into `state.statuses` — and no titles,
  summaries or names of people.
  `privacy.html` promises exactly that, keep it true and update its effective
  date in the same commit as any storage change (it went to 2026-08-20 with the
  key, to 2026-08-21 with stages, to 2026-08-27 with the feature ageing
  threshold and to 2026-09-01 with the status vocabulary).

- **Which tab you were on IS remembered, for the two number views only.** `view.activeTab`, restored at boot. It used to be deliberately not saved — the old comment said "a reload should open on the dashboard" — which was out of step with both siblings (Sprint Predictability keeps `settings.view`, Money Map keeps `ui.activeTab`) and with the fact that All Teams is where somebody with several teams works. Changed 2026-08-21 after it was reported as annoying. Settings and Your Data are NOT remembered, on purpose. No new guard was needed: `selectTab` already refuses a hidden or unknown tab and falls back to the dashboard, which is exactly the All-Teams-disappears-below-two-teams case.
- **The All Teams Throughput trend column is a sparkline plus a signed figure, and both halves are load-bearing.** The SVG is `aria-hidden` and the figure beside it is the text equivalent — that is not only for screen readers: `cellText()` strips anything hidden from assistive technology as decoration, so without a VISIBLE figure the CSV export would have an empty column. It reuses `linearTrend`, the same fit the chart above draws, so the two can never disagree; if it ever grows its own regression, that is the bug. The trace is normalised to its own range (shape, not magnitude — Per week is the magnitude) and drawn in `currentColor` so one CSS rule themes it. **No red-for-falling**: nothing in this account's palette sits on the red-green axis, and rising throughput is not unambiguously good anyway. Sorting is ascending-first, like Data to and for the same reason — the interesting end is the most negative. **The header names the metric** — it shipped as a bare "Trend" and that was not enough beside eight other columns that each name theirs. **Deliberately not a line-per-team chart**: this view is written for eight teams, the theme pack's categorical ramp stops at five, and eight lines on one card is a spaghetti chart.

## Both of a Team's Lists, Everywhere (2026-08-25) — no schema change

Found by a review of the whole repo the day the forecast landed. All three are the same shape and
none of them is about the forecast: **the feature layer added a SECOND list to a team, and four
places went on reading only `rows`.** A feature is a row — same record, same wire letters, same
`hydrateRow` — so anything that walks a team's records has to walk both, and the test to apply to
anything near this is *"would this be wrong if half the data were in `features`?"*.

- **The Clear button took the list you were NOT looking at.** The Your Data card shows one of the
  two — the heading says which, the add button says which, the export filename says which — and
  the red button beside them read "Clear This Team's Data" and emptied `rows` regardless. So a
  reader looking at twenty features pressed it, was asked about a hundred and ninety ITEMS that
  were not on screen, agreed, and afterwards had the same twenty features in front of them and no
  work items anywhere. **This is the item dialog's own rule** — *"the dialog decides its list once
  on the way in and reads it again on save"* — arriving on a button instead of a form, and worse
  there, because nothing was open to re-read: the confirm quoted a count off the invisible list.
  Both the label and the handler follow `featureUnit()` now, and clearing the features says the
  work items are left alone, the same promise the single-feature delete makes. The pluralisation
  was fixed in passing; it said "Delete all 1 items" before.
- **A FEATURE'S STAGE DATA WAS NEVER PRUNED, ANYWHERE.** The Add a Feature form offers the stage
  picker and a day box per stage — `buildManualRow` writes `stage` and `stages` without asking
  whether it is a feature — so a feature can hold both fields, and three separate places dropped
  them on the floor:
  - `hydrateState` pruned dangling ids on `t.rows` only, so **`openItemDialog`'s stated invariant
    was false for the record it was opening**: *"an id on `r.stages` can only be a stage that
    exists"*. The dialog builds its boxes from `state.stages` and reads them back as the whole
    truth, so the orphan figure was silently dropped on the next edit and otherwise sat in
    localStorage for ever.
  - The stage delete cleared `rows` only — and its confirm counted `rows` only, which is the
    contradiction the `w`-versus-`g` fix already has a paragraph about. `renderStageRows`'s count
    column had the same gap, and the two must agree or the count above the confirm disagrees with
    the confirm.
  - `buildSharePayload`'s `usedStages` walked `rows` only, so a stage named by a feature alone was
    left out of the link — and the recipient's `hydrateState` then pruned the figure as a dangling
    id. A sender's number that arrives as nothing.

  Nothing on screen ever DREW the orphan (`renderStageTime` joins against `state.stages`), which
  is exactly why it needed a test rather than an eye.
- **The team delete never mentioned the features it destroyed.** A team holding twenty features
  and no work items was taken under a bare "Delete X?" — the most destructive control in the app
  asking the mildest question it has, about a list it did not name. Both halves are stated now,
  each only when there is one, so an ordinary team's confirm reads exactly as it always did.
- **Eighteen assertions, and they were PROVEN TO FAIL FIRST** — all four fixes reverted, the suite
  run, eighteen reds each naming its own fault. The Clear-button group is the only one that touches
  `view.unit`, so it puts it back and asserts the restore: `td-view` outlives a run, and a suite
  left in the feature view would fail the next one for a reason that is not about the app.

### What was checked and is NOT wrong

Recorded so the next sweep does not re-derive it. **Clean up old data is items-only on purpose** —
the README says so in as many words — and was left alone; whether an old feature should go with
its items is a question for Charles, not a bug to fix quietly. `countCreated`/`countKeys`/
`countStageDays` read `rows` only, and that is harmless: `countFeatureLinks` counts the features
themselves, so the losing-a-field prompt still fires on a file whose only created dates are on
features. The "(empty)" a team with features and no items reads as in the picker, the share list
and the cleanup list is the same class of thing and is left standing.

## The Forecast Scenario (2026-08-25) — no schema change

Phase 5, the last of the five. `view.scenario` — seven knobs, all numbers and small integers, all
device-local. No `SCHEMA` bump; it DOES travel in a share link (see below).

- **THE NO-OP PROMISE IS KEPT BY DISPATCH, NOT BY ALIGNED STREAMS, and the plan for this was
  wrong.** The design said a defaulted scenario would return an array deep-equal to the unscoped
  sampler's, on the strength of every knob drawing unconditionally so the stream stayed aligned.
  That cannot hold: the scoped samplers draw MORE per trial than the originals — a growth draw per
  trial, a confidence draw per period — so the stream is a different length whatever the knobs say.
  `scenarioIsDefault` switches the caller back to the ORIGINAL sampler instead, which is a
  stronger guarantee and a simpler one: today's answers are the same code, not approximately the
  same numbers. A test asserts BOTH halves — that the scoped version is not stream-identical, and
  that it gives the same answer anyway.
- **Inside the scoped samplers the unconditional-draw rule still holds**, for the reason it always
  did: turning knob A on must not move the answer knob B was giving. Every knob draws every trial,
  even where its range collapses to 1 — never inside an `if`. Add a knob and you add its draw for
  every trial.
- **Clarity WIDENS, and draws ONCE PER FEATURE.** Per-feature draws model independent vagueness
  and partly cancel on the sum; a single per-trial multiplier models one correlated shock, never
  cancels, and overstates the spread badly. The ranges are a COMPRESSED cone of uncertainty
  (max 0.7–3.0, not the textbook 0.25–4) because the sizes being multiplied already carry the
  board's own spread — this is a RESIDUAL knob, not an estimation cone from nothing — and because
  a 4x upper bound trips the spread guard every time, which would ship a control whose only output
  is a refusal. The asymmetry is intentional: software uncertainty is one-tailed.
- **NO TEAM-CONFIDENCE STEP GOES MEANINGFULLY ABOVE 1** (max 1.05). A reorganisation making a team
  faster is the most-abused claim in this domain and this app must not supply the arithmetic.
  Pinned as an invariant over the whole list, so a new step cannot quietly break it.
- **Scope growth and extra features would DOUBLE-COUNT if named badly.** "+20%" and "+20%" reads
  like +40% and is +44%. They are relabelled to be genuinely orthogonal — growth WITHIN counted
  features versus features not counted — and `scenarioScopeRange` prints the product as one line
  regardless, so the double-count cannot survive as a reading error.
- **Scope SHRINK is refused** (`growthLo` clamps at 0). It is not a risk anybody plans for and it
  would be a way to forecast your way to a date.
- **Clamp an out-of-range NUMBER, default a non-number.** Resetting an over-range `parallel` to
  the default would silently turn "everything at once" into "one at a time" — the opposite answer.
  The split `forecastItems` already draws, applied to every integer knob.
- **A typed pace REPLACES history and disables team confidence.** A blend is traceable to neither
  source; multiplying a guess by a guess compounds two people's pessimism. The eight-period floor
  stays the DEFAULT outcome rather than the only one — that is the whole point of the control. The
  card states the weakness rather than fudging it: a typed range has no quiet weeks and no spikes,
  so it spreads LESS than real periods do.
- **A typed FEATURE SIZE replaces the measured one, and only where a measurement exists**
  (2026-08-27). `view.planSizeOn` + `typedFeatureSizeRange()`; both are needed, so a ticked box
  with no number leaves the measurement standing — the same two-part test `scenarioPaceOn` makes,
  and for the same reason. **Off by default and deliberately NOT three-state like the pace tick:**
  a default that followed the data would swap a measurement for a guess on somebody else's board
  without their saying so. The tick is on screen only with data on the feature lens; planning has
  no tick because it has no measurement, and the item lens has neither. The **join-rate floor goes
  null with it** — that guard protects a measured distribution and there is none left. It raises an
  assumption (so it is counted, listed and reachable by Reset) ONLY when `replacedSizes` is passed,
  which is what tells the data path from planning. **Anything that reports the basis must check
  `f.sizesTyped` first**: the basis tile, the figures row, the `how` sentence and the schedule all
  claimed a measurement over a synthesised list until they did. Kept under the `planSize` key
  prefix on purpose — renaming would drop every stored value at `loadView`'s whitelist.
  - **IN PLANNING THE SIZE ROW RIDES WITH THE PACE TICK** and there is no size tick at all. With no
    history an unticked pace is no forecast, so a size box standing beside one is a number with
    nowhere to go — the orphaned-control fault, third time. With data the two are independent and
    must stay so. The planning hint names the TICK when the tick is off, rather than sending the
    reader to a box that is not on screen.
  - **Reset CLEARS `planSizeLo`/`planSizeHi` as well as `planSizeOn`**, and `scReset.disabled` reads
    the two numbers, not only the tick. It shipped keeping them for one day and was reported the
    same day: nothing gates those boxes in planning, so a kept size goes on forecasting under a
    button that says it cleared everything.
- **PARALLELISM CHANGES EACH FEATURE'S DATE AND NOT THE LAST ONE**, and the test asserts EXACT
  equality of the all-done 85th across 1, 3, 6 and 10 in parallel. Throughput is dealt per period
  whatever it is spent on, so under any work-conserving schedule the makespan is identical.
  **SPILLOVER IS WHAT MAKES THAT TRUE** — a feature needing less than its equal share hands the
  remainder back inside the same period; without it the team idles and the invariance breaks. Do
  not add a per-feature maximum rate: it would break the invariance and need a parameter nobody
  can supply.
  - **The card must keep saying it does not charge for splitting attention.** Little's Law ties
    cycle time to WIP and real throughput FALLS as more is started at once. This holds it constant,
    so parallelism looks free here and is not. That sentence is the honesty of the whole control.
  - **Per-feature percentiles are taken INDEPENDENTLY**, never by selecting the trials where the
    whole set landed at the 85th — that is a conditional distribution and gives artificially narrow
    spreads. The consequence is on the card: the dates are MARGINALS and are not jointly
    achievable; only the last row also means "everything by then".
  - **One flat `Float64Array` with strided indexing**, not an array of arrays — the naive version
    allocates 2,000 small arrays per render and GC-pauses on every change. Percentiles go through a
    reused scratch buffer and the typed array's own numeric sort, NOT `percentileOf` (which slices
    and sorts with a comparator per call). `FORECAST_SCHEDULE_TRIALS` is 2,000 rather than 10,000:
    these are dates printed to the day and the standard error of an 85th from 2,000 draws is under
    half a day. Don't "improve" it back for symmetry.
- **THE SPREAD GUARD REFUSES AT 2.5x, AND THE FIRST NUMBER WAS 3 ON A FALSE PREMISE.** The plan
  said "three is about where three stacked knobs land". Measured on the demo's own data at 4,000
  trials, that is simply untrue — a forecast SUMS feature sizes and WALKS many periods, and both
  concentrate the result:

  | | ratio |
  |---|---|
  | plain, ten features | 1.30 |
  | + scope growth 0–150% | 1.55 |
  | + clarity "barely understood" | 1.37 |
  | + brand new team | 1.29 |
  | all three at once | **1.65** |
  | all three, on ONE feature | **2.95** |

  At 3 the guard was unreachable — a control whose only output is never firing. 2.5 catches the
  last row, clears every realistic multi-feature scenario, and is nowhere near the 1.30 an
  unadjusted forecast gives. **If the clarity or confidence ranges are ever retuned, RE-MEASURE
  rather than reasoning about it** — the reasoning was what got it wrong the first time.
  `widestScenarioKnob` names which knob to turn back first: a proxy (widest range as a fraction of
  its own low end) rather than the exact answer, which would re-run the forecast once per knob at
  ~5 extra runs and is affordable if the proxy proves not good enough.
- **`beyondReach` is re-checked AFTER the scenario**, since a scope multiplier can push a
  reachable backlog past the walk's limit and the old check ran on the unmultiplied count.
- **A non-default scenario changes the answer's LABEL, not just a note beside it.** "85% of
  adjusted runs" on the tile, the fold's summary saying how many settings are on, and the
  assumptions listed in words UNDER THE TILES — never in the ⓘ, the standard the forecast hint
  already set. Somebody who screenshots one tile has to still be told.
- **`scReset` is essential, not a nicety.** These persist to localStorage with the rest of the
  view, so without one way to clear them all somebody opens the app tomorrow and reads yesterday's
  scenario as today's forecast.
- **`change`, never `input`, on every knob.** Each one re-runs ten thousand simulations; an
  `input` handler would forecast 1, 12 and 120 on the way to typing 1200. One delegated listener
  over the block rather than one per control — a per-control list is a list somebody adds a control
  without joining.
- **THE FORECAST TRAVELS IN A SHARE LINK, and this reverses a documented decision.**
  `forecastItems` and `forecastDate` were deliberately kept out, on the reasoning that a recipient
  asks their own question. That held while the answer depended only on the question; it stops
  holding once a SCENARIO can change what the numbers mean, because a link is how a forecast
  reaches a planning room and two people reading different numbers off one link is worse than
  useless. Every field is a number, an integer or a date string, so the storage policy is
  untouched. `SHARE_PAYLOAD_V` NOT bumped — an older build drops the block and draws the plain
  forecast. **The SCOPE deliberately does not travel**: it names teams by id, and a link carries
  only the teams it was asked to.
- **`derive()` TAKES A QUESTION, NOT THE APP'S STATE, and that literal object bit once.** The view
  object handed to `derive()` in `renderDashboard` is built by hand, so a field added to `view` and
  not added there silently never arrives. `countFrom` did exactly that for a day: it worked on a
  pooled scope, which goes through `deriveTeams` and its own object, and did nothing on a single
  team. **If you add a view field the forecast reads, add it in BOTH places.**
## Features Age Against Their Own Threshold (2026-08-27) — SCHEMA 12 → 13

`settings.featureAgedDays`, and it **ships EMPTY**. The Aged work card in the feature view was
counting features against the item threshold — a fortnight is a coaching convention about work
items and does not survive the change of unit, so read against features it flagged boards that
were behaving normally.

- **Null means "not set" and must SURVIVE as null, never as 0.** It is in `NULLABLE_SETTINGS`
  beside `outlierDays`, and `normalizeSettings` keeps only a number > 0. There is no number this
  app is entitled to assume about somebody else's features, so with nothing set there is no aged
  figure, no aged chart and no threshold line — not a figure computed against zero. Every reader
  of an aged feature figure has to pass null through rather than defaulting it.
- **SCHEMA 12 → 13 in the same commit as the whitelist entry**, per the rule at the top: an older
  build would strip the key on load and push the stripped copy back. Settings ride into a share
  link whole, so the threshold travels; `SHARE_PAYLOAD_V` unchanged.
- **The demo sets 30 days at Load-sample time (`DEMO_FEATURE_AGED`)** — a number for those two
  boards, not a default the app holds — so the feature view tells the same story about the same
  teams the item view does, and the load-sample confirm names it.
- `privacy.html`'s storage list already covered it ("the thresholds"); its effective date moved
  to 2026-08-27 with this change.

## The Unit Switch Is on Two Tabs (2026-08-27) — no schema change

Reported by Charles standing on "Loaded Features" with no way out of it: the Count switch lived
only in `#viewControls`, `selectTab` hides that strip off the two number tabs
(`NUMBER_TABS`), and `renderDataTable` follows `featureUnit()` — so Your Data showed one of a
team's two lists with no control to change which. Naming the list in the heading, which is what
the app did about this before, says which one you got; it does not offer the other.

- **`#unitFieldData` is the SAME control, not a second one.** Same label word, same two option
  values, same `view.unit`, same handler (`['unitSel','unitSelData'].forEach`), and
  `renderUnitControl` sets BOTH boxes from `featureUnit()` on every render. There is no path
  where one reads Features and the other Work items — tested both directions, because a copy
  that only follows goes stale the first time somebody uses the original.
- **The rest of the strip deliberately did NOT follow it there.** The work type filter, the date
  window and Group by all narrow a population and mean nothing to a raw list. The unit is the
  one control in that strip that chooses WHICH population — its own comment in the markup says
  so — and a tab showing a population is a tab it belongs on. If anyone later proposes showing
  the whole strip on Your Data, this is why not.
- **It sits on its own line above the table, not in the heading row.** A field is a label line
  over a control line; dropped among the one-line buttons it would sit out of line with all of
  them, which is the orphaned-field complaint this app has had twice.
- **`#unitFieldData { max-width: 160px }`, and 160 is not a number chosen here** — it is what
  `.controls .field`'s `min-width` resolves to, so the same control is the same size on both
  tabs. Every select in this app is `width: 100%`; uncapped it drew a 1200px box for two words.
- **It cannot lock behind you.** `renderEmptyState` gates `#loadedCard` on the team's WORK ITEMS
  (`activeRows()`), not on the list being shown, so switching to a team's empty feature list
  keeps the card, the "No features loaded yet." note AND the switch. Pinned by test.
- Hidden in print alongside `#viewControls .field`, for the same reason those are.

## Forecast Placement — Kept Under Dashboard (2026-08-27) — no schema change

Charles asked whether the forecast should be its own top-level tab. **It stays a section of the
Dashboard tab**, and the reason is the strip above it: `months`, `bucket`, `filterValue`, the
custom From/To pair and the Count switch ALL feed the forecast — see the view object
`renderDashboard` hands `deriveTeams` and `derive`. A forecast here is a resample of the history
in whatever window that strip is set to. Sitting beside Flow, Delivery and Health is what tells
a reader that widening from 3 months to 12 moves the forecast too; promoted, it would be a
top-level tab silently governed by a control last touched on a different one — the fault this
file already records against Settings when Settings left the strip. Planning mode already does
the promotion where it is warranted: `renderDashboard` hides the other three and forces
`selectChartTab('forecast')`.

**The counter-case is real and worth re-reading before anyone changes this.** Forecast is ~305
lines of markup against Flow's 61, Delivery's 32 and Health's 103 — more than the other three
combined — and it is the only one you TYPE into. If a second forecasting surface ever lands,
promote them together; one section outgrowing its siblings is not on its own a reason.

Two defects that placement had were fixed the same day:

- **The tablist is named `aria-label="Dashboard sections"`, not "Chart groups".** Forecast is not
  a chart group — its charts are the working and the tables are the output — so a screen reader
  announcing "chart groups, 4 of 4, Forecast" was mislabelling the one tab the phrase did not
  fit. **The code still says `chartTab` / `CHART_GROUPS` / `selectChartTab` on purpose**:
  `view.chartTab` is saved state and travels in a share link, so renaming it would strand every
  reader's saved section on the next load to fix a word only this file reads.
- **`#fcScopeNote` says when the forecast is not this team.** The Dashboard tab makes one
  implicit promise — everything on it is the team in the header picker — and "Whose pace" is the
  only control that breaks it. The scope was already NAMED in four places (the hint, both chart
  titles, the figures table), which is a weaker claim: somebody who has just been reading Flow
  takes "dealt from the Payments Train pooled" as extra detail about the team they are on. The
  new line names what is DIFFERENT, and names the control that did it. It is `#fcStale`'s
  sibling and deliberately a SECOND element rather than more sentences in it — who first, then
  over what; they are separate claims with separate causes, and the pair fires together often
  because pooling is what exposes a short export in the first place. **Two exemptions, both
  tested:** silent in planning mode (there are no tiles or other sections to contrast with), and
  silent when the pool is one team that is already the picked one (same rows, same derive — a
  divergence note there would be a false alarm on a card whose whole job is to be believed).

## The Three Forecast Extras (2026-08-25) — no schema change

Asked for straight after phase 5 shipped, having been left out of it. All three are additions
rather than corrections.

- **`requiredPaceFor` bisects a MULTIPLIER on the team's own samples, never substitutes a flat
  rate.** A team that delivers 2, 9, 4, 7 does not become a team that delivers 5.5 every period
  because it speeds up, and a required rate worked out against a flat average would be a promise
  about a team nobody has. Monotone (scaling every sample up can only finish sooner), so bisection
  is valid — a test pins that more scope needs a faster pace.
  - **A multiplier under one is HEADROOM, not an instruction.** Printing "0.75x your pace" reads
    as advice to slow down. Both readings are stated as a multiple of THE PACE THAT WOULD DO IT,
    so "you have 5x what you need" and "you need 2.4x what you have" are the same sentence
    pointing opposite ways, and a reader moving between them never has to reverse anything.
  - **Unreachable is its own answer**, not "19.97x", which would read like a plan.
  - **The pace is in WORK ITEMS even on a feature forecast** — nobody speeds up by completing
    features faster. `sizes` is the argument that switches the walk to the feature model while
    leaving the reported rate in items.
- **A BISECTION IS THE MOST EXPENSIVE THING IN THIS APP, and shipping it naively cost 3x.**
  Measured on the demo the first version put a single-team feature forecast at 336ms and
  `renderAllTeams` at 849ms, because it is a whole forecast run once per iteration and All Teams
  runs one derive per team plus the train. Three things fixed it, to 133ms and 260ms — the second
  figure being FASTER than before this change:
  - `FORECAST_SOLVE_TRIALS` 2000 → **1200** and `FORECAST_SOLVE_ITERS` 24 → **18**. Eighteen
    halvings of 0.1–20 still resolve the multiplier to about seven millionths, five decimal places
    past what the tile prints.
  - **`view.forecastMode: 'off'`** skips the bisection where nothing reads it. The All Teams table
    has NO forecast column and its train chart is throughput only, so every simulation there was
    work nobody could see. A test pins that the flag drops the bisection and **nothing else** —
    the forecast itself is byte-identical either way.
  - The pre-scan in `deriveTeams` (coverage end + stale list) is skipped under the same flag: it
    exists only for the forecast, and it was a whole extra derive per team.
- **The +12 weeks preset counts from where the WALK starts**, not from today and not from the
  data's end — once counting-from is in play those are three different dates, and a preset one day
  out from the forecast it sets is worse than no preset. `lastForecastCountFrom` is remembered at
  render because the button fires long afterwards and cannot re-derive it. **The app has no PI
  calendar and does not pretend to**: the button is labelled by the span, the way the window picker
  labels the same one.
- **The figures table exists because the CSV writer reads TABLES off the page.** The percentile
  answers are styled divs beside a histogram, which is right on screen and cannot be exported, so
  this restates them in the one shape that can leave — the rule every export here follows: what you
  take away is what you were looking at. **It carries the assumptions in the same file**, because a
  percentile that arrives in a spreadsheet without the scenario that produced it is a number nobody
  can check, and a fortnight later nobody can remember either.
- **Nothing is left of the three.** Every variable Charles enumerated was built in phases 1–5;
  these were the additions noted as outstanding, and they are done.

## Forecasting Features by Decomposition (2026-08-25) — no schema change

Phase 4. Nothing stored; two new pure samplers, one assembler, three new floors.

- **DO NOT RESAMPLE FEATURE COMPLETIONS, and the reason is measured rather than asserted.** A
  team finishing one or two features a month gives a weekly series like
  `[0,0,1,0,0,0,1,0,0,0,0,1]` — twelve periods clears `FORECAST_MIN_PERIODS`, something completed
  clears the all-zero check, and the existing guards let it straight through. Against a dense
  series chosen to have the SAME median, the sparse one answers 11 periods at 50% and 24 at 95%
  (a 2.2x spread) where the dense one answers 12 and 13.3 (1.1x). Both say "about twelve
  periods"; only one of them knows it, and the difference is the zero fraction rather than
  delivery. A first draft of this comment said "a step function with three or four distinct
  answers" — that was WRONG (the sparse series produces 31 distinct answers) and the test caught
  it. The claim is about the SPREAD, not the granularity.
- **`featureNonZeroPeriods` + `FEATURE_MIN_NONZERO` (5)** is the floor the existing ones do not
  give. Direct feature throughput is kept as a named fallback rather than deleted, because it
  captures something decomposition cannot see: a feature that took three weeks after its last item
  closed, for integration or sign-off.
- **ONE INTEGRATED TRIAL, NEVER TWO MULTIPLIED FORECASTS.** The classic error in this kind of
  tool is to forecast the halves separately and multiply the 85th percentiles — "the 85th
  percentile feature is 20 items" times "20 items takes N weeks" — which compounds two tail
  values and lands far past the real 85th. `forecastFeaturePeriods` draws a size PER FEATURE per
  trial, sums them, and walks that target once, so the trial distribution carries both sources of
  variance jointly. **A test pins the integrated 85th as strictly below the multiplied one**; if
  anyone ever "simplifies" this into two calls, that test is what stops them.
- **One draw per feature, not one per trial.** A single multiplier applied to all of them would
  model every feature on the board being the same size as every other, which is the one thing the
  size distribution exists to disprove.
- **`forecastFeaturesIn` is a WALK, not a division.** A budget that runs out part-way through a
  feature has delivered the ones before it; dividing a total by an average size would count the
  half-built one and throw away exactly the variance this exists to report. Pinned with a
  hand-checkable fixture (steady pace, one size).
- **Three floors, and the ORDER of the checks is load-bearing.** `thin-join` is tested BEFORE
  `few-sizes` because a thin join is WHY the size count is low: reporting the symptom would send
  the reader hunting for finished features when the column they need is missing. `FEATURE_MIN_SIZES`
  is 5 — deliberately lower than the 8 periods a throughput sample needs, because the other half
  of the model still carries the full item history, so the total evidence behind an answer is
  higher than either floor alone.
- **`featureForecastOf` returns the SAME SHAPE `derive()` does for an item forecast** — same keys,
  same rows, same histograms — so `renderForecast` draws either without knowing which. It is pure
  and takes everything as arguments, because the two halves come from two different lists and no
  single `derive()` call holds both. `derive()` now returns `sampleSet` (the samples themselves,
  not just the count) for exactly this.
- **The feature forecast is ASSEMBLED IN `renderDashboard`**, where both lists are in hand, and it
  applies the same coverage trim the pooled forecast does — a team three periods behind
  contributes three periods of zero to the ITEM throughput too.
- **`#dashNoFeatures` is a fourth empty face, and it exists because the other three are each
  WRONG for it.** A team with items and no features was being told "No Data Yet — head to Your
  Data and paste your work items", with 48 of them already loaded. That is the same failure the
  stage-time card has a comment about: a message that sends somebody to fix a set-up that is
  right. Tested FIRST, before the other three.
- **Both halves are named on the tile** ("Built from 17 finished features, sized at a median of 9
  items each, paced by 14 whole weeks of item throughput") and the model is stated in the hint
  every time, including the limitation it does not correct for: **decomposition assumes a feature
  is done when its items are done**, so integration, sign-off and a demo are not in the numbers.
  Measuring and correcting that is a later change; stating it is this one.
- **Still to come (phase 5):** the scenario knobs — scope growth, feature clarity, team
  confidence, estimated throughput where there is no history, features in parallel and the
  per-feature delivery schedule, periods unavailable — plus the assumptions list, the
  uninformative-spread guard, required throughput and the forecast CSV. The plan is in
  `~/.claude/plans/`.

## Forecasting More Than One Team (2026-08-25) — no schema change

Phase 3. `view.forecastScope` and `view.countFrom`, both device-local — no `SCHEMA` bump and no
share-payload entry, matching `forecastItems` and `forecastDate`, which have always lived there.

- **POOL THE ROWS, NEVER SUM THE TEAMS' DISTRIBUTIONS.** The series is additive (counting over a
  disjoint union is a sum) but the DISTRIBUTION is not. One draw takes a calendar PERIOD and asks
  what the whole train delivered in it, so the covariance between teams — a freeze, an incident,
  planning week, a shared holiday — is carried for free. Summing independent per-team draws sets
  that term to zero and produces a **narrower** spread than reality, which understates risk. That
  is the one direction this app must never be wrong in. If it is ever proposed as a performance
  optimisation, this paragraph is the reason not to; there is a comment saying so at the call
  site and a test pinning the additive half so nobody mistakes it for licence.
- **THE SHARED DATE IS A FAIRNESS RULE THAT BECOMES A LIE IN A FORECAST.** `deriveTeams` imposes
  one `asOf` on every team, which is right for a comparison and wrong for a resample: a team three
  weeks behind contributes three periods of ZERO, and those are not observations of a slow team,
  they are the absence of data — `derive()` cannot tell the difference, because throughput is a
  count over rows that are not there. **Worse than the level it drops is the spread it adds**:
  those periods are systematically low rather than randomly low, so they fatten the slow tail
  exactly where the 85th and 95th are read.
  - `deriveTeams` computes `coverageEnd` (the earliest `dataEnd` among teams that HAVE rows —
    teams with none are excluded, or one empty team would refuse every forecast on the train) and
    re-derives the train with `forecastCoverageEnd` set.
  - **Only the FORECAST's window moves.** `asOf` stays the newest date for everything else, or
    the All Teams table stops being a fair comparison. The trim is a slice on the already-computed
    `wholeThroughput`, not a second window.
  - `reason: 'stale-team'` is its OWN refusal, fired only when the trim is what caused the
    shortfall. Folding it into `few-periods` would name the wrong fix: one is answered by the
    grouping and window controls in front of the reader, the other by re-exporting a team or
    narrowing the scope.
  - Nothing happens for a single team, and `lostPeriods`/`coverageEnd` are 0/null there — which
    is every forecast this app drew before now, pinned as unchanged.
- **`countFrom` — the anchor an export flatters the plan by.** Every figure here is read as of
  the newest date in the data and the forecast always followed; on a nine-day-stale export that
  puts every forecast date nine days early, and nobody delivers those days retrospectively. The
  DEFAULT DOES NOT CHANGE — it would make the forecast disagree with every tile beside it — but
  the control appears when the data ends before today, with the gap named. `max`, never a swap, so
  a future-dated export cannot pull the anchor earlier than the data ends. `todayLocalISO()`, not
  UTC: "today" is a claim about the reader's calendar, and a UTC today is tomorrow far enough
  east. The trials are untouched; only the date they land on moves, and a test pins that the day
  COUNT is identical and the DATE differs by exactly the staleness.
- **`FC_SCOPE_ALL` is a `~` sentinel like `ART_NONE`**, for the same reason. `currentForecastScope()`
  validates at the point of use and falls back to the team on screen — the one scope always
  available — because a forecast showing too little is visible where one showing too much is not.
  Hidden below two teams, the picker's own threshold.
- **The scope's own derive happens in `renderDashboard`, not in `derive()`.** Everything else on
  that screen is the team in the picker; only the forecast widens. `renderForecast` takes the
  scope and the stale list as arguments rather than reaching for state, so what it says about
  whose pace it dealt from cannot drift from what was dealt.
- **`deriveTeams` derives each team ONCE for the pre-scan** (coverage end and the stale list) and
  again for its row against the shared view. A first draft did it three times; that is a third of
  the most expensive thing this app does thrown away.

## The Feature View (2026-08-25) — no schema change

Phase 2. `view.unit` is `'items' | 'features'` and a `<select>` in the control strip. It stores
nothing new — which unit you are reading is a position on this device, like the team you have
picked — so no `SCHEMA` bump and no share-payload entry.

- **THERE IS NO SECOND SET OF MATHS, and that is the whole design.** `derive()` takes a list of
  records and works out flow over it; it does not know and must not care what they are. Switching
  the unit is switching WHICH LIST goes in (`unitRowsOf`, `deriveTeams`'s `listOf`). Nothing was
  threaded through the metrics engine, so the two readings cannot drift — there is only one
  reading. A test derives the same list both ways and pins every figure identical.
- **What DOES have to follow is the wording.** A chart headed "Items Completed per Week" over a
  list of features is a lie nobody double-checks. `derive()` works the unit's name out once
  (`unit`/`Unit`/`Units`/`unitOne`/`unitMany`, returned on the result) and every title, axis,
  tile foot and forecast row reads it. **Never spell "item" out in a label again** — that is how
  the two get out of step.
- **`view.unit` is read through `featureUnit()`, never directly.** A saved view outlives the data
  it described: delete every feature, or open a share link from a sender who had them, and a
  stored `'features'` would leave the dashboard counting an empty list and reporting that the team
  had stopped delivering — which looks exactly like a finding. Features only while there are some,
  and the fallback is items rather than an empty screen. Same reason an unrecognised value means
  items: falling back the other way would be a dashboard silently counting features while every
  reader assumed items.
- **THREE THINGS DELIBERATELY DO NOT CARRY OVER, and the reasoning is the same for all three: a
  figure that is merely less useful may stay, and one that would be actively FALSE must not.**
  - **`wipLimit` and `sleDays` are nulled in the feature view.** Both are promises a team made
    about its BOARD. Three features in flight against a limit of six reads "inside it" — a
    reassurance about a promise nobody made — and a 54-day feature against a 10-day target reads
    "not met", a failure nobody signed up to. Null is "not set" everywhere in this app and not set
    is the truth here. A second limit and target FOR features is a real thing somebody might want
    and is deliberately not built: two more stored fields answering a question nobody has asked.
  - **The defect rate card and tile go.** A defect is a kind of work item, so the defect type
    matches nothing in a list of features and the chart would plot a flat zero across every
    period — a claim of perfect quality on a board that may have plenty of bugs. The tile reads a
    dash, not 0.00%: the figure is not zero, it does not exist.
  - **The progress table's counts are the WHOLE feature, not the window.** Every other figure on
    that screen is windowed; a progress figure that moved when somebody changed the date picker
    would be unreadable. The title names no window, on purpose.
- **`featureBreakdown(features, items)` is the ONE new piece of maths, and it is deliberately
  OUTSIDE `derive()`.** It is the only figure needing both of a team's lists at once. Giving
  `derive()` a second list so it could compute one card would make every caller and every existing
  test pass an argument they have no use for. When the forecast needs the join it can have its own
  way in.
  - **`sizes` counts COMPLETED features only**, and only children that finished at or before the
    feature did. An in-flight feature is still growing; a child that finished after was reparented
    or added later. Same reasoning cycle time uses.
  - **A finished feature with no visible children is LEFT OUT, never recorded as zero.** Its items
    are outside the window, on another board, or not in the paste — a zero would pull every
    measure of size down for a reason that is about the export.
  - **`joined` and `sizes` answer different questions and the counts differ.** An item that
    finished after its feature closed is still JOINED to it (the export's coverage) while not
    counting toward what that feature took (delivery). A test states this directly, because
    getting them the same is the obvious "tidy-up".
- **The `solo` class is TOGGLED now, not static.** Flow holds three cards in the item view and
  four in the feature view, so which card is the odd one out changes with the switch. `solo`
  narrows the third card to one column and centres it; with four there is no third.
- **Features can be TYPED IN, and that was not optional.** CLAUDE.md's own rule — every chart has
  a door that is not a Jira paste — would otherwise have been broken by the two new cards on the
  day they shipped. `buildManualRow` gained an `isFeature` flag relaxing exactly two rules and no
  others: a key is REQUIRED (items name it by key) and a created date alone is enough. The item
  rule is untouched and pinned as untouched. The work item form gained a **Part of feature** box
  on the same reasoning.
  - **The dialog decides its list once on the way in and reads it again on save.** A form opened
    from a list of features and writing into the items would be the worst kind of wrong —
    silently correct-looking.
  - **Deleting a feature leaves its items alone.** They are work that was really done, and taking
    them with it would be the most destructive thing in the app hiding behind the smallest button.
    Their parent key then points at nothing, which the size card reports rather than repairs.
- **The Your Data tab does NOT carry the unit switch** — the strip is for the two number views,
  and a work-type filter or a date window means nothing to a raw list. So the HEADING names the
  list instead ("Loaded Features"), and the export filename follows: a download called
  `work-items.csv` holding features would be wrong on somebody's disk long after the screen that
  produced it is gone.
- **No new demo data was needed** and that is not a hole in the sample-data rule: the demo's two
  keyed teams already carry features from Phase 1, so every surface here is reachable from Load
  sample data, and Team Bare Export is the team with none.

## The Feature Layer (2026-08-25) — SCHEMA 11 → 12

Asked for by Charles as the foundation of feature-level forecasting: read Jira's **Parent key**,
drop **Parent summary**, and keep features apart from work items so item-level metrics cannot
move. Phase 1 of five; the forecasting itself is not built yet.

- **`r.parentKey` (`p` on the wire) is the SECOND shape-checked identifier, and it went in on the
  issue key's own reasoning, not as precedent creep.** It is guarded by `cleanIssueKey` —
  literally the same function, the same `ISSUE_KEY_RE`, at the same two doors — because it is the
  same shape of value. The admission test is unchanged and was applied again: *can a regex tell
  this from a sentence?* It can. **`Parent summary` fails that test outright and is never read**,
  which is the same answer a status got.
- **`t.features` is a SEPARATE LIST, never a flag on `rows`, and that is the load-bearing
  decision.** Every item-level figure is computed over `rows`, so a feature that is not in `rows`
  cannot reach one — no audit of a dozen call sites, no trusting that audit for ever. A test
  derives the same export twice, with the layer on and with the feature rows removed by hand, and
  pins **eleven series byte-identical**. If extraction ever leaks, that is where it shows.
- **A feature IS a row.** Same record, same wire letters, same `hydrateRow`, same allowlist.
  `hydrateRows` and `hydrateFeatures` differ **only in their filter**, which is the whole
  difference between the two: an item needs a completion or a start, a feature needs a **key and
  any date**. Don't grow a second record shape; the one place they may diverge is that filter.
- **The relaxed filter is not a nicety.** An item with only a created date is untouched backlog
  and says nothing about flow. A feature in that state is the PIPELINE — the thing a forecast is
  about — and dropping it would leave the app able to forecast only work already under way.
  Pinned from both sides, including that `parsePastedRows` does not count it as `undated`.
- **A KEYLESS FEATURE IS NOT A FEATURE.** Items name their feature by key; one with no key can
  never be joined to anything. Counted as `featuresNoKey` and reported under its own heading
  rather than folded into `undated`, because the two say different things to the reader: one
  means "your export has backlog in it", which is normal, and the other means "your feature rows
  arrived without the column that makes them features", which has a fix.
- **`PROSE_HEADING` is the hardening this layer OWED the storage policy, and it closed a real
  hole rather than a theoretical one.** No heading pattern ever matched `Parent summary` — but
  `detectColumns` also finds the work-type column from the VALUES when no heading claims it
  (`distinct <= 20`, `dateRate < 0.6`, rejected only when every value is distinct), and a 200-row
  export covering eight features has exactly **eight distinct parent summaries**, which passes
  both tests. It was kept out only by the real Type column usually having fewer distinct values
  still, with `cleanWorkType`'s 40-character cap as the last catch — and a short summary
  ("Login redesign", fourteen characters) clears that cap. **This change made it far likelier by
  inviting people to paste the very export that carries the column.** So a heading matching
  `/summary|description|comment|notes?\b|title|reason|justification/` is now excluded from
  **every** role, in both passes, with no fallback: a role that can only be filled by a prose
  column goes unfilled. The test runs it **both ways** — the same forty rows, one word changed in
  one heading — and asserts the column is taken without the guard and refused with it. A guard
  nobody has watched fail is a guard nobody knows works.
  **Stage columns are deliberately NOT filtered by it**: a stage column is only ever a heading
  that exactly equals an alias the reader typed by hand, which is a deliberate act rather than a
  guess, and its values must survive `cleanStageDays` to be stored at all. This list exists to
  stop the app GUESSING its way into prose, and stages never guess.
- **`HEADER_PATTERNS.parent` is ANCHORED and has NO headerless fallback** — the third anchored
  pattern, and the only role with no shape-based fallback at all. Every other role can be found
  from its values; a parent key looks EXACTLY like an issue key, so two unheaded key columns
  cannot be told apart. Guessing would reparent every item in the file, silently, and **a wrong
  parent is worse than no parent**: it invents a feature breakdown nobody's board has. No
  heading, no parent.
- **`featureTypes` is a LIST, it ships as `['Feature']`, and empty is still off.** The word was
  added 2026-09-03 at Charles's request, reversing the empty default. It is not the Spikes-and-
  Stories mistake repeated: `Feature` is what Jira's own hierarchy calls the level above a Story,
  and unlike a filter row a feature type matching nothing diverts no rows, moves no figure and
  shows nothing. **Do not make an empty list mean "give me the defaults back"** the way
  `s.filters` does — clearing the box is the documented way to switch the whole layer off, and
  every guard in the feature code is written against it. Each entry goes through `cleanWorkType`
  (dropped whole, never truncated), the list is capped at `FEATURE_TYPES_MAX` and de-duplicated on
  the matched form. It has its own listener rather than a row in `SETTING_INPUTS`, because that
  map is for scalars.
- **`mergeFeatures` de-duplicates on APPEND where rows deliberately do not.** Two pasted rows
  describing the same work item are two rows — the app has never had a way to know otherwise.
  A feature IS its key, so the same key twice would count one feature as two everywhere it is
  joined and no reader could see why their numbers had doubled. Incoming wins: it is the newer
  export.
- **Features are only written when feature types are set up.** With none, `res.features` is empty
  by construction, so an unconditional replace would let an ordinary paste silently delete a
  feature list built with the setting on. Both paste paths guard on it.
- **A features-only paste is a real thing to do.** Both paste paths test BOTH routings before
  deciding nothing was loaded; testing only the item routing reported such a paste as loaded and
  wrote nothing.
- **The multi-team split routes features through `routeRowsToTeams` too** — a feature's key
  carries its project at the front exactly as an item's does, so the same pure function does it
  and a feature can never land in a team its children did not. Only the `assigned` half is used:
  an unclaimed feature key is the same finding as an unclaimed item key, already named in the
  report by the id it belongs to.
- **`SHARE_PAYLOAD_V` was NOT bumped**, matching ARTs, keys, stages and the two targets. Features
  DO travel — they are what the shared charts are drawn from — and are **windowed with the same
  cutoff the rows are**, or a link trimmed to three months would carry every feature the team ever
  had against three months of items. **`tdAdopt`'s losing-a-field prompt WAS extended to them**,
  on the re-typeability test: a column of parent keys pasted per item comes back only by finding
  the export again.
- **The demo's two keyed teams break their work down and Team Bare Export does not**, which is the
  third face again. Items are dealt to features in **contiguous runs** whose lengths cycle through
  the profile's `featureQuotas` — deterministic, never from `rnd()`, the fourth field to follow
  that rule after the issue key counter, the stage split and the status cycle. **An earlier draft
  let a feature be revisited later and gave every one of them a seven-month span**, which is both
  wrong about how features work and useless to forecast from. How MANY features that produces
  falls out of the quotas and the team's own throughput rather than being stated, so nothing has
  to be kept in step by hand. The work-in-progress items are broken into runs of three so each
  team has **two or three OPEN features** rather than one — an unfinished feature is what a
  feature forecast is about, and one is not a demonstration. Feature rows are emitted in the same
  paste as their children, as a real export would, and each one's dates are built FROM its
  children: earliest created, earliest start, and a completion **only when every child is done**.
- **Still to come (phases 2–5):** the Items/Features unit toggle, multi-team and ART forecasting,
  feature forecasting by decomposition, and the scenario knobs. The plan is in
  `~/.claude/plans/`. Two things Phase 4 will want that Phase 1 does not provide: an
  **unstarted** feature in the demo (there are none — the demo generates no untouched backlog at
  all), and a reason to widen `FORECAST_MIN_PERIODS` thinking, since feature completions are
  sparse enough to pass the 8-period floor as a step function.

## Ignoring Major Outliers (2026-08-24) — SCHEMA 10 → 11

Asked for by Charles: a way to stop one enormous item wrecking the figures across
the app. Two decisions were taken before any code, and both are load-bearing.

**1. It is a rule, not a per-item tick box.** `settings.outlierMode` is
`'off' | 'auto' | 'days'` and `settings.outlierDays` is the typed cutoff. Nothing
is stored per row, so there is no new wire letter and no hydrate whitelist entry —
only `normalizeSettings`, which coerces both (settings ride into a SHARE LINK, so
both arrive attacker-controlled). The rule collapses to ONE stateable number,
which is why the screen can say *"ignoring 4 items over 87 days"* — a claim a
reader can check against the scatter and argue with, where a hand-curated list of
exclusions is a judgement nobody else can see.

**2. It removes a DURATION, never a DELIVERY.** An ignored item still counts as
delivered, started, raised, in progress and (if a defect) unplanned. Only its
cycle time, lead time and stage times leave the pool. Throughput, net flow, the
CFD, WIP, aged work, the defect rate and both forecasts are pinned byte-identical
by a test with nine equality assertions. **You cannot fix an average by claiming
the team shipped one fewer item.** This is also what made the change small: the
app already had a "this item has no cycle time" path (`cycleTimeOf` returns null
for an item with no start date) and every consumer already handled it.

### Three things that must not regress

- **Aged work and the Work Item Age chart are out of scope, permanently.** They
  measure work in flight, which has no cycle time to be an outlier of. An item
  open for 300 days is the finding; a setting that quietly stopped counting it
  would be the one genuinely harmful thing here. `ageLines` filters the `outlier`
  key out of the scatter's lines it borrows — and note that leaving it in did not
  merely look wrong, it took the whole dashboard down, because the age chart looks
  each line's key up in a style table and an unknown key is `undefined.colour`.
- **`summary.sleMet` deliberately refuses to see the setting.** It is computed
  over `windowCyclesAll` — every finished item, ignored ones included. A target is
  a promise about real work and the items that broke it are exactly what an
  outlier rule takes out; read over the fenced pool, a team's 85% ≤ target flipped
  from "not met" to "met" the moment the setting went on, which would make a
  switch in Settings the cheapest way to pass a service level. The tile's foot
  carries `sleJudgedIncludesIgnored` so "7.0 … target 10.0 — not met" reads as a
  statement about two populations rather than as a bug.
- **The fence is PER TEAM on All Teams, never shared.** Do not "fix" this into a
  shared parameter the way `asOf` is shared. A shared date is a fairness rule; a
  shared fence is the opposite — a platform team at sixty days and a support team
  at three do not have the same idea of unusual, and the estate's pooled fence is
  wide enough to catch neither. It also keeps a team's figures identical on the
  table and on its own dashboard. A test pins all of it.

### The rule itself

`outlierCutoffOf(values, mode, typedDays)` — Q3 + **3** × IQR, not the textbook
1.5. Cycle times are strongly right-skewed and this app's headline figure is the
85th percentile, which *lives* in the tail; a 1.5 fence eats a legitimate tail and
quietly reshapes the number teams forecast with. Twelve-item floor on `auto` only
— a typed fence is not derived from the data, so a small sample cannot make it
wrong. Scoped to the **window**, like every other figure (see the stage-times
comment for the card that had to learn this).

### What it says, and where

`outlierPhrase` / `outlierNote` / `outlierFoot` — one wording, three punctuations.
The window note, the four duration cards' titles and the cycle/lead/percentile
tile feet. Silent when the fence caught nothing. On the scatter the ignored dots
are **still drawn**, as hollow rings under a dotted line at the cutoff, and they
stay clickable to copy a key — the one chart whose job is showing the spread must
not hide the spread. Shape, not colour alone, per the family rule.

**No Loaded Data column**, and that was a deliberate reversal during the build:
that table lists stored rows with no window or filter in view, so marking a row
there would state a window-relative fact on a screen with no window. The scatter
is the identification surface, and it already names and copies.

### One thing fixed in passing

The debounced settings listener called `renderDashboard()`, so a setting changed
while standing on All Teams left that tab stale until you switched away and back.
Now `renderViews()`. Pre-existing; it affected `agedDays` too.

## Six Gaps Closed (2026-08-22) — SCHEMA 9 → 10


Asked for as a set, after a review that listed what the app was missing. Five features and one
piece of plumbing. The two that touch storage are first; the rest change no saved field.

### The Limit and the Target — SCHEMA 9 → 10

`t.wipLimit` and `t.sleDays` on each team: how much work it means to have open at once, and how
long it means an item to take. Both optional, both `null` by default, guarded by `cleanWipLimit`
and `cleanSleDays` at both boundaries (the input handler and `sanitizeTeams`) like every other
stored field. `SCHEMA` and the whitelist moved in the same commit, as the rule at the top says.

- **PER TEAM, NOT IN SETTINGS, and that is the whole decision.** Every setting here is shared by
  every team and can be, because each describes how a FIGURE IS WORKED OUT — what a defect is,
  what a same-day item is worth. These two describe a team's own board: a limit of eight means
  something different to a team of three and a team of twelve, and a promise is made by the
  people who keep it. Do not "tidy" them into the Settings tab.
- **NOT SET IS THE DEFAULT AND MUST STAY SO.** A limit the app picked would draw a line across
  somebody's chart claiming they had agreed to it. Every reader treats null as "draw nothing, say
  nothing" — never as a zero, and never as false: `summary.overWipLimit` and `summary.sleMet` are
  **null** when there is nothing to read against, because `false` would say a team is inside a
  limit it never agreed to.
- **They reach `derive()` on the VIEW object**, the way `asOf` and the forecast's two questions
  do, and are validated there at their point of use. `derive` takes a team's rows, not a team;
  handing it the team object would let it reach for anything else on there.
- **Strictly over, never equal** — a limit of eight allows eight. Same reading `agedCounts`
  already takes of the ageing threshold, and pinned.
- **The target is compared with the PERCENTILE, not the average.** A target is a promise about
  the next item, which is the one question an average cannot answer.
- **NOTHING TURNS A COLOUR.** The verdict is a sentence on the tile; the bars over a limit are
  the colour of the bars under it. The app states figures rather than grading them, the palette
  has nothing on the red-green axis to grade with, and a bar that changed colour would be the app
  calling a period a failure. The limit line and the target line take `--series-5` and a dash of
  their own — the ageing threshold's colour, because all three are **lines the reader drew**, as
  against the median and percentile lines, which are things their data did.
- **They TRAVEL in a share link where the project id does not**, and the two are not
  inconsistent: a project id routes a paste the recipient cannot make, and these are drawn on the
  charts the link exists to show. `SHARE_PAYLOAD_V` was NOT bumped, matching ARTs, keys and
  stages — an older build drops both and draws no lines, which is graceful degradation.
- **`tdAdopt`'s losing-a-field prompt was NOT extended to them**, on the re-typeability test that
  kept ARTs and the project id out of it: two numbers typed in a dialog in seconds.
- The boxes live on the team's row in Teams & Stages with their meaning in FRONT of them
  ("WIP ≤", "85% ≤"), because that table deliberately has no header row. The `<label>` is both
  the visible prefix and the accessible name, and the `aria-label` **starts with the words on
  screen** (WCAG 2.5.3) and adds only which row it belongs to.
- The demo's two keyed teams carry **the same limit and the same target** and only one keeps
  either; Team Bare Export carries neither. Identical figures on two boards is the point — a
  limit per team would show two lines and teach nothing.

### The Cumulative Flow Diagram — no schema change

Three cumulative counts read at the same eval points work in progress is read at, stacked:
finished, in progress, raised-and-not-started. Third card in **Delivery**, `solo` like the lead
time card in Flow.

- **`cfd.inProgress` IS `wip`, and a test pins the two as equal.** They are worked out different
  ways — a subtraction of two cumulative counts against `openCounts` walking the items — so if
  they ever disagree, one of them is wrong. That equality is also what makes the band readable as
  work in progress rather than as "work opened inside the window".
- **THE BASELINE IS WHAT MAKES IT READABLE.** Everything delivered before the window opens is
  subtracted from all three curves. Without it, nine months of history under a three-month window
  puts 130 items in the bottom band and leaves the two that matter as a sliver. Subtracting one
  constant from all three cannot move a band's THICKNESS — a band is a difference — so nothing
  else changes. Counted from strictly before the first bucket, not from the first eval point,
  which would swallow the opening bucket's completions.
- **Two fallbacks keep the bands off negative**, and each is also the honest reading: an item
  completed with no start date enters both counts on the day it closed (never observably in
  progress), and an item with no created date joins at its start. Without them a paste missing
  either column draws a band below zero, which Chart.js will happily stack.
- **The backlog band is absent without created dates, never flat at zero** — a flat zero is a
  claim that there is no backlog where the truth is that the export cannot see one. Same stance
  the lead time chart takes on the same column.
- **THE TOP BAND IS SURVIVORSHIP, AND THE HELP SAYS SO SINCE 2026-09-01.** Charles asked how a
  work item view can show 21 items raised-but-not-started in a week when the parser drops any row
  with neither date (`featurePipeline`, the one exemption, is features only). It can, because
  *not started* is read as of the WEEK being plotted: an item raised in week 26 and picked up in
  week 31 sits in the top band for the five weeks between, and it is in the paste at all because
  it has a start date. So the band draws the wait DELIVERED work really had, never the backlog as
  it stands — and it closes to nothing at the right edge, since every stored item started on or
  before `endDate`. A right edge that does NOT close means a typed `customTo` cutting the axis
  before some starts.
- **Which means the chart changes shape behind the reader**, and that is the half a note could
  easily keep quiet about. Next month's export brings the items that have started since, and they
  thicken a band over weeks already drawn — the same week, read twice, honestly reporting two
  different numbers. The understatement is worst nearest the present. Both halves are in the
  `cfd` help entry and both are pinned in `tests.html`: a note that keeps one and loses the other
  leaves the same question half answered.
- Three colours from the pack's ramp — `--series-1`, `--series-3`, `--series-5`, the widest
  separation five tokens allow. **The app's first three-series chart**; everything else needed
  two, which is why the pair at the top of `drawCharts` is a pair. Colour is not the only cue: the
  bands are in a fixed order bottom to top and the chart carries a legend.

### A Window Between Two Dates — no schema change

`months: 'custom'` plus `view.customFrom` / `view.customTo`, and `customWindow()` — pure and
exported — deciding what counts as a usable pair. In `view`, so no schema bump and no place in a
share payload.

- **The END IS CLAMPED to the data, and the clamp comes AFTER the shared date.** That ordering is
  the trick: a team whose export stops mid-window is still read as of the date every other team
  is read as of (what `asOf` is for), while nothing is ever read as of a date past the typed end
  or past the data. Get it the other way round and All Teams stops aligning.
- **An incomplete or backwards pair means NO custom window, not an error** — it is the state a
  reader passes through on the way to typing the second date. The note under the strip says what
  it is waiting for rather than leaving two filled boxes looking ignored.
- **Choosing Custom prefills the boxes with the window already on screen**, so the picture does
  not change at the moment of switching. Only when both are empty: a pair typed earlier is theirs.
- **`derive()` gained an empty-axis return.** A typed window is the only one that can leave
  `weekStarts` empty — every rolling window ends where the data does and floors at the first
  completion — and everything below that line indexes `weekStarts[0]`. It returns the same shape
  the no-completions case does.
- **`inProgressCount` and `windowItemCount` are now read AS OF the window's end** (`wip`'s last
  value) rather than "not completed yet". Identical for every rolling window; the typed window is
  where they part company, and "how many are open today" stated inside a window about last
  January is a figure from outside it.

### Printing — no schema change

Two halves, and the split is the thing to keep: **layout** in an `@media print` block, **colour**
in `beforePrint`.

- **The print block names no colour at all**, and a test asserts it. Browsers do not print
  backgrounds, so the page comes out on paper's own white; asking for `print-color-adjust` would
  spend somebody's toner on a surface colour.
- **Midnight and Dark switch to the pack's Light palette for the duration of the print**, in JS,
  because charts are CANVASES: they re-read the CSS variables only when they are drawn, so a
  print-only palette in a stylesheet would leave every chart in the theme it was last rendered
  in. Nothing is saved, so the swap cannot outlive the print. Light and Sepia are left alone.
- `closeMaxi()` first: a chart filling the window is a fixed overlay with the page inert behind
  it, and would print as one chart and a blank page.
- The grid is deliberately NOT forced to one column — the print layout's width is only known
  after the stylesheet applies, and every canvas would need re-rendering at a size nothing had
  measured. A canvas is an image drawn at device resolution; it downscales cleanly.
- `#printHead` is the print-only line naming the team (or the train) and the window, because the
  header's picker and the tab strip both go. It does NOT repeat the app name the header keeps.

### The Dashboard Tab Is Hidden Until Something Has Data — no schema change

Asked for straight after the six above. It was the last control in
`renderEmptyState()` still offering something with nothing behind it: a first run showed a
Dashboard tab whose entire content was a card explaining that there was no data yet.

- **ANY team, not the active one**, and that is the load-bearing half. Keyed on the active team
  the tab would appear and disappear as somebody moved through the picker — a control moving
  under the pointer — and `#dashEmpty`, which is written for exactly "this team is empty and
  another one is not", would become unreachable.
- **NEVER in a shared view.** `tab-data` and `tab-settings` are both hidden there, so hiding this
  one too would leave a tab strip with nothing in it. Verified against a real link whose team
  carried no rows: one tab, and the card that explains itself.
- **`selectTab`'s fallback moved with it.** It was `'dashboard'` unconditionally, which stopped
  being safe the moment the dashboard could be hidden; it is now Your Data in that case — the one
  tab that can do something about there being no data, which is the same reasoning boot uses.
- **Boot's predicate moved too**, from the ACTIVE team's rows to any team's. It used to send
  somebody whose other teams were full to Your Data because the one they happened to be on was
  empty.
- **The demo offer on `#dashEmpty` goes when any team has rows** (`#dashDemo`, hidden as a unit
  with the sentence explaining it). With the tab gone on a first run, the only way to reach that
  card is from a working app, where a button that quietly adds three teams is the same mis-click
  the one beside *Load pasted rows* is already taken away to prevent.

### Settings Moved Into the Header — no schema change

Asked for the same day as the tab rule above, and it is the other half of the same thought: the
tab strip is for ways of READING your numbers, and Settings is a thing you GO to. Teams, backups
and sharing were already buttons; this is the fourth of that kind, not a third view.

- **`TABS` is three now**, and nothing else had to move: `selectTab` already refuses a name that
  is not in the list, so a browser that saved `activeTab: 'settings'` before the change falls back
  on the next load. Pinned as a case, because it is not hypothetical.
- **Laid out as the Teams window's twin** — one section per thing you set, headed by its name,
  the Add button at the right-hand end of that heading row, one Done. Same 1100px, and it needs
  it: `.grid.two` is auto-fit at 260px a track, so at the 560px base all five fields stack into a
  column six deep.
- **The window's own note sits under its h2**, not under the closing row. A sentence below Done
  is a sentence after the way out.
- **Reset and Done share the closing row**, destructive left, way out right. Reset is deliberately
  NOT up beside "+ Add a type", where a mis-click costs every label somebody has set.
- **`renderSettingsForm()` runs on the way IN**, not just at boot: every field in that window is
  also written by Reset and by a restore, and a window opening on a value the app no longer holds
  is the worst kind of wrong — one nothing on screen contradicts.
- **The glyph is ⚙ and the button is LAST in the row.** The comment above the header buttons had
  already named ⚙ as the family's settings mark before this app had one — it is Money Map's.
- **It goes in a shared view**, with the other three writing controls.
- The `#tab-settings { margin-left: auto }` rule went with the tab. Nothing else in that strip
  wants pushing right.

### Installing It — no schema change

`manifest.webmanifest`, three PNG icons and an apple-touch-icon, all drawn by `make_favicon.py`
from the same mark, all on `sw.js`'s SHELL list.

- **`manifest-src 'self'` has to be spelled out in the CSP.** Under `default-src 'none'` a
  manifest is covered by no other directive, so the fetch is refused and "Install app" silently
  stops appearing. It admits a static JSON file on this origin and nothing else.
- **`scope` is `./`, never `/`.** Every app in the family is served from ONE origin, and a scope
  of `/` would capture Sprint Predictability and Money Map into this app's window.
- The install files are cached because an INSTALLED copy is the one most likely to be opened with
  no network at all — a launcher re-reads the manifest and its icons to draw the window. All of
  them are already public in this repo, so the origin-wide-cache rule is unchanged by them.
- `<meta name="theme-color">` holds Midnight as a literal (it must be right before any script
  runs) and `paintThemeColor()` rewrites it from the pack's own `--bg` on every theme change.
- The maskable icon is full bleed with square corners; the safe zone is a disc of radius 25.6 in
  the 64 viewport and the mark's furthest point is 23.8 from centre. Widen a bar or drop its base
  and re-check that number — it is written down in `make_favicon.py`.

## The Status Is Stored Now (2026-09-01) — SCHEMA 13 → 14

**This section REVERSES the safety argument the section below it is built on, at Charles's
explicit request.** That section — and this file's storage policy, and `privacy.html`, and the
README — all said the same thing: no status name is ever stored. They were rewritten in this
commit rather than left contradicting the code. Read this before that one; that one is now the
history of how the field got in, and this is the rule.

`state.statuses` is a list of `{id, label}`, capped at `STATUS_MAX` (40). A row carries `r.status`
(`u` on the wire) — **an id into that list, never a word**. A stage gains `st.statuses`, the ids
it groups. `st.match` — the typed aliases — **stays**, and is not vestigial: see below.

### The four legs, and which two carry the weight

The old argument could not be repaired, only replaced: a status has no shape a regex can check,
so a cap in its place would be the theatre this file already warned about. What holds instead:

1. **THE APP NEVER GUESSES A STATUS COLUMN.** `HEADER_PATTERNS.status` is anchored, with no
   headerless fallback — both already true before this change. `PROSE_HEADING` still excludes a
   prose heading from every role.
2. **A STATUS COLUMN REPEATS AND PROSE DOES NOT.** A workflow is ~10 statuses across a whole
   export; a summary column has ~one distinct value per row. `statusColumnUsable` tests it at
   the paste boundary, **all-or-nothing, before anything is stored** — the same class of test
   `detectColumns` already used for the headerless work-type detector. This is a property of the
   COLUMN, which is exactly what the value could not supply.
3. **A ROW STORES AN ID.** The words live once, in a capped list the reader can see and delete in
   the stages window. Blast radius of a mistake: one visible entry, not 400 cells.
4. **Shape hygiene per label** (`cleanStatusLabel`): ≤40 chars, ≤6 words, a character whitelist,
   dropped whole. **SECONDARY, AND THE TESTS SAY SO** — one assertion pins that a short summary
   ("Login redesign") CLEARS every shape test, precisely so nobody cites leg 4 as the boundary.

**Legs 1 and 2 are the argument. If either is ever weakened, the feature is no longer safe and
this section is void.** In particular: never add a headerless fallback for the status role, and
never make the repetition gate per-cell instead of per-column — half-reading a prose column is
the worst of both answers.

**NOT PRECEDENT FOR A SUMMARY FIELD, and the reason is leg 2 rather than any cap.** A summary
column fails the repetition test by construction — that is what makes it a summary. The test to
apply to the next request is *"does this column repeat the way a closed vocabulary does?"*, not
*"a status is stored, so why not this?"*.

### What the change bought, and it is not only the storage

- **THE STAGE IS DERIVED, NOT FROZEN.** `stageOf(row, stages)` is the ONE place a row's stage is
  answered: a row with a status resolves through the stage's ticked list **at read time**; a row
  without one falls back to the stored `r.stage`. So re-ticking a status **re-buckets rows pasted
  weeks ago**, where the old design could only ever affect the next export. Nothing reads
  `r.stage` directly any more except `stageOf` and the boundary code — keep it that way.
  The legacy fallback is NOT a migration step and must not become one: rewriting old rows would
  mean inventing a status label this app never saw.
- **The age chart has three rungs, still a switch and still no picker**: stage → status → work
  type. The status rung is the one that matters in practice — a board that pastes an export gets
  the canonical axis with no set-up at all. Work type is NOT legacy; it is what a board with no
  Status column still gets, and Team Bare Export still draws it.
- **`st.match` still does one job nothing else can**: a Time in Status export names its statuses
  in its column HEADINGS, which are not values in any column and so never reach the vocabulary.
  Aliases also **auto-tick** a matching status into their stage as it is adopted
  (`res.statusTicks` → `adoptStatuses`), which is the upgrade path — a reader who set stages up
  before this build gets their next paste grouped with nothing re-typed. The demo exercises
  exactly that path, which is why `demoStages` still ships aliases and empty tick lists.
- **The "adopt this heading" button that was refused for a year now exists**, as the tick list.
  It is allowed because the objection has gone, not because it was overruled: the objection was
  that one click would copy work-system text into permanent storage, and there is no such copy —
  ticking moves an id between two lists the app already holds.

### Things that did NOT change, and the pull to change them is real

- **In-flight only.** Every export says Done against most of the file. The vocabulary would be
  "more complete" with Done in it; completeness is not a reason to store anything. Pinned.
- **`refOf()` is untouched.** A row reaches the problem list because its columns look wrong, so
  its cells are the ones that cannot be trusted. The paste report DOES name statuses it KEPT —
  those passed legs 2 and 4 and are stored data — and never a cell it REFUSED. That distinction
  is the whole of it.
- **No free-text input anywhere.** The item form's status control is a `<select>` over the stored
  vocabulary. If it ever becomes a text box, leg 2 has been bypassed and the argument is void.
- **The transition-log export shape is still refused**, and the reason survives: it is not one
  column of repeated labels to measure, so leg 2 has nothing to bite on.
- **`SHARE_PAYLOAD_V` NOT bumped**, matching every field before it. Statuses DO travel — the
  recipient's age chart is drawn from them — windowed to what the link's own rows use, and a
  stage travels if it groups one of them (or the recipient prunes the tick as a dangling id and
  the sender's grouping arrives as none). The ALIASES still do not travel.

### The boundary work, all in this commit

`sanitizeStatuses` (leg 4 at the other door, cap, dedupe on `normalizeAlias`, `ID_OK`,
`PROTO_KEY`); `sanitizeStages` gains `statuses` with **first stage wins a contested status**, the
same answer a contested alias gets; `hydrateRow` gains `status`; `serializeRows` emits `u`
omit-when-empty; `hydrateState` prunes dangling status ids **on rows AND features** and prunes a
stage's tick list. It USED to drop a status nothing points at, except one a stage had ticked —
**REVERSED 2026-09-01, see Six Fixes From the 2026-09-01 Audit**: two doors now admit a status
nothing points at by construction, and the prune erased them on the next reload.
`countStageDays` counts `r.status` too, so `tdAdopt`'s losing-a-field prompt covers it (a per-item
status column is not re-typeable — the same test that sent stage times in and kept ARTs out).
Delete-all takes `state.statuses`. **A THIRD REFERENCE FROM A RECORD TO A STAGE NOW EXISTS**
(`g`, legacy `w`, and a ticked status) — `renderStageRows`'s count column and the stage-delete
confirm both go through `stageOf`, which is the `w`-versus-`g` bug's own lesson applied ahead of
time rather than after.


## Workflow Stages (2026-08-21) — SCHEMA 7 → 8

> **SUPERSEDED IN PART ON 2026-09-01.** The first bullet's argument — "no status name is ever
> stored" — was reversed deliberately; read **The Status Is Stored Now** above before acting on
> anything here. It is left standing rather than rewritten because everything else in it is
> still live (the alias rules, the two export shapes, the column guards, the day counts, the
> honesty rules on the figures) and because the argument it makes is why the replacement had to
> be a different KIND of argument rather than a weaker version of this one.

`state.stages` is a list of `{id, name, match[], statuses[]}` and each row carries an optional
`stages` object of day counts keyed by stage id (`g` on the wire). It is what blocked time, flow
efficiency and a stage-by-stage age chart have always been waiting on — and it is the first
field in this app whose source is a **Jira status**, which is the field every rule at the top of
this file was written to keep out. **Read this whole section before changing anything near it.**

- **THE SAFETY ARGUMENT IS NOT A GUARD ON THE VALUE. It is that no status name is ever
  stored.** A status has no shape a regex can check — "Fix the login bug on prod" is
  twenty-five characters of letters and spaces, which is every shape a status label has — so
  the test that let the issue key and the project id in (*can a regex tell this from a
  sentence?*) fails here, and a shape guard would be theatre. What is stored instead is a
  stage **the reader named in a dialog**, which is the same class of data as a team name or an
  ART name, plus **numbers**. The status name out of the export lives for the length of one
  parse: it is matched against the aliases the reader typed, turned into a day count, and
  discarded with the rest of the pasted text. `tests.html` asserts this directly — it
  stringifies the parsed rows and greps for the column headings.
- **A day count can also be TYPED, since 2026-08-22** — a box per stage on the work item form. It
  takes nothing away from the argument above: what is refused here is a status *name*, and a box
  takes a number. See *Days in Each Stage, Typed In*.
- **That is why matching is by ALIASES YOU TYPE and there is no "adopt this heading" button.**
  (AMENDED 2026-09-01, twice, and the second one REVERSES this bullet. First: a status TICKED
  into a stage matches a heading too, which is not this button — a tick compares a heading
  against a label already in storage. Then: a wrapped heading whose column holds nothing but
  day counts DOES teach the vocabulary its status. Taken deliberately, with Charles, on the
  grounds this bullet itself set out. See *A Ticked Status Claims Its Column* and *A Heading
  May Teach the Vocabulary*.)
  It is the obvious convenience and it is deliberately absent: one click that copies
  work-system text into permanent storage is exactly the thing this design exists to avoid.
  The project id's "create the team from the report" button is not precedent — a project id has
  a shape, and this does not. If it is ever wanted it is a decision to take deliberately and
  write down here, not a convenience to add in passing.
- **Only the days-per-status export shape is supported, and the other one must never be.**
  One row per issue, one column per status, every per-item cell a number: the free text is
  confined to a single header row. The transition-log shape — one row per transition with a
  status name in a cell on every row — puts untrusted text on every item row, which is the
  shape this design refuses.
- **Matching is EXACT on the normalised form, never a substring.** A substring rule looks
  kinder and is worse: an alias of `Testing` would silently swallow a "Waiting on Testing Env"
  column and add somebody's environment queue to their test time — a wrong number nobody can
  see. `normalizeAlias` collapses case and punctuation, so `In-Progress` and `In Progress` are
  one status; that is the only latitude there is.
  **AMENDED 2026-09-01, twice** — see *A Real Export Wraps Its Status Names* and *A Ticked Status
  Claims Its Column* above. A ticked status matches on exactly these terms too. A HEADING now has a
  `Days in` / `Time in` phrase read off the front before the comparison, because that is how a
  real export names these columns; what is left still has to equal an alias in full, so the
  Waiting-on-Testing-Env case above is unchanged and still pinned. Exact is exact; the wrapper
  is not part of the status.
- **Two columns may feed ONE stage and are added together** (the point of aliases — a workflow
  with "Ready for Code Review" and "Code Review" is one Review stage). **Two stages claiming one
  alias is the opposite**: a contradiction the app must not resolve silently, so the first in the
  list keeps it and `duplicateStageAliases` puts the clash on screen as it is typed, exactly as
  two teams sharing a project id already are.
- **Stage columns are found by HEADING ONLY — no headerless fallback, deliberately.** Every
  other role can be found from the values, because a date looks like a date and a key looks
  like a key. A column of day counts looks like a column of day counts whatever stage it
  belongs to, so guessing would mean assigning somebody's review time to their test stage on
  the strength of column order. A date, type or key role also **wins a contested column
  outright**, and the stage that wanted it goes into `columns.stageClash` so the report can say
  so — otherwise a stage aliased `Created` simply reports nothing and nobody can see why.
- **A duration column may not take a date role, and it takes TWO guards to stop it (2026-08-24).**
  A real Jira-changelog export names its columns `Days in Backlog`, `Days in Ready for Work`,
  `Days in In Progress`, `Days in SIT`, `Days in Done`, `Days Blocked` — and the date patterns
  here are loose on purpose, because a date column can be called almost anything. So
  `/in.?progress/` matches `Days in In Progress` and `/done/` matches `Days in Done`: for one
  export the ONLY thing keeping the completion date off a column of day counts was `Resolved`
  happening to sit earlier in the row. The failure is silent — a day count is not a date, so
  every row comes out unfinished and the throughput reads zero with nothing on screen saying
  why. `detectColumns` now runs each heading-matched role in **two passes**:
  1. **fussy** — the stage columns are hidden (`stageSkip`), and a *date* role additionally
     declines any column that has values and whose values are not dates (`datey`);
  2. **the old matcher, untouched** — every heading a candidate again.

  Both halves are load-bearing and neither covers the other. The stage skip cannot protect
  `Days in Done`, because that column must be **aliased to nothing** (see below) and so is
  invisible to it; the value test cannot protect a stage column that is legitimately empty in
  this particular export. And the second pass is what keeps the guard a *preference* rather
  than a rule: a `Resolved` column full of dates this app cannot parse still lands in the
  completed role and still reports its unreadable cells, instead of vanishing into "no
  completion column" and taking the diagnostic with it. `datey` passes an entirely EMPTY
  column deliberately — an export of nothing but work in flight has an empty `Resolved`, and
  that is still the completion date.
- **Two columns of a changelog export must NOT be aliased to a stage, and both look like they
  should be.** (Since 2026-09-01 `Days in Done` is reachable by a bare `Done` alias and the
  report warns when a stage claims it; `Days Blocked` still cannot be reached except by its own
  full spelling. See the amendment above.) `Days in Done` is an open interval that runs to the moment the export was taken,
  so it grows on every re-run — alias it and the biggest stage on the chart is one that means
  "how long ago did this finish". `Days Blocked` is the **Flagged** flag, which runs
  *concurrently* with whatever status the item is sitting in — on a real row the four real
  stages already summed to the item's entire age, and adding blocked time took the total 15%
  past it. Neither is a stage; the first is not a duration at all and the second is an overlay.
- **The report names columns BY POSITION and stages by the reader's own name — never the
  heading out of the export.** This report has never echoed a pasted cell and a heading is a
  pasted cell. Somebody matching up a column reads the heading off the export they still have
  open. Showing unmapped headings in the mapping dialog was considered and left out; it is the
  narrowest possible widening of that rule, and it is still a widening.
- **Zero is a REAL value and is kept.** An item that passed through a stage inside a day
  genuinely spent no measurable time there, and dropping those would quietly lift every median.
  An EMPTY cell is different — no data for that stage — and `parsePastedRows` tells the two
  apart by looking at the raw text, exactly as it does for the dates.
- **The card reports a share of the time MEASURED, never a share of cycle time.** They are not
  the same number and only one is honest: a status export counts calendar days in every status
  it was asked about, including ones outside the started-to-finished span, so a share of cycle
  time can exceed 100% for perfectly ordinary data. A wrong number with an explanation attached
  is still a wrong number.
- **These are CALENDAR days whatever the working-days setting says, and the card title says so
  in its own words.** That setting governs the three durations this app works out itself, from
  dates it holds; these are worked out by Jira from a status history this app never sees, and
  there is no honest way to re-measure a single total Monday-to-Friday. Re-labelling them would
  be the one thing worse than not converting them. This is the one deliberate exception to
  "don't let the two measures diverge", and it is safe only because it is stated on the card.
- **`stageTimesOf` is pure and NAMELESS** — it returns figures keyed by stage id and never
  touches `state.stages`, so the one place a stage's name is decided stays the dialog it was
  typed into. The renderer joins the two, **in the reader's own stage order**: a workflow has a
  direction, and sorting the table by size would throw away the one thing a reader already
  knows how to scan.
- **The whitelists, in the same commit as the SCHEMA bump, as always**: `sanitizeStages` (ids
  through `ID_OK`, names at 120, aliases at 60 each and 24 of them, duplicates collapsed),
  `hydrateStageDays` (ids through `ID_OK`, values through `cleanStageDays`), and `hydrateState`
  pruning day counts whose stage no longer exists — the dangling-`artId` treatment, once at the
  boundary rather than guarded at every read. A row left with none loses the object entirely, so
  it goes back to serialising as it did before the feature.
- **The day counts object has NO PROTOTYPE.** `Object.create(null)` in both the parse and the
  hydrate. `ID_OK` happily matches `__proto__`, and this is the first field in the app whose
  keys come from outside; with no prototype there is nothing for that to reach. Pinned.
- **`g` is omitted when empty**, so a team that never pastes a status export serialises
  byte-identically to before — the rule `k`, `i` and `projectId` already follow, and what keeps
  the first save after this build from rewriting the whole stored document. Likewise no
  `stages` key on the document until a stage exists.
- **`SHARE_PAYLOAD_V` was NOT bumped**, matching ARTs and keys. A link carries the day counts
  and **only the stages its own rows spent time in** — the ARTs rule, for the ARTs reason: a
  stage name describes the reader's workflow, and sharing one team should not publish the shape
  of a workflow that team has nothing to do with. **The ALIASES deliberately do not travel**:
  they are matching rules for a paste box the recipient does not have, and they are the one
  field in this app typed to mirror a work system's own words. An older cached build drops both
  and shows the app as it was — graceful degradation.
- **`tdAdopt`'s losing-a-field prompt WAS extended to stage times**, where it was not extended
  to ARTs or the project id. The test is re-typeability: a train's name and a project id are one
  word typed in a dialog, and a per-item column of day counts is not — it comes back only by
  finding the export again. Same test, opposite answer, and that is the line to apply next time.
- **The manage dialog is now "Teams, ARTs & Stages" and the header button is "Teams & Stages"**
  — three sections against the sibling's three (Teams, ARTs & PIs). The two windows share a
  SHAPE — one section per thing you manage, each headed by its name with its own Add button —
  not a list of sections; the sibling has no stage times and this app has no PIs.
  **The button rename (2026-08-21) is the sibling's rule being followed, not a divergence from
  it**: SV's button has always read "Teams & PIs", naming its own distinctive section rather
  than hiding it behind the first one, and this app's plain "Teams" was the drift. It was
  reported the day stages shipped, by Charles, who could not find the feature — a section
  nobody knows is there is a section nobody opens. Every in-app sentence that points at the
  window was renamed with it. Pinned, because "Teams" is the tidier-looking label and exactly
  what a later edit would shorten it back to.
- **The demo sets the stages up BEFORE it parses**, because a stage column is only ever found
  by an alias that already exists. Team Healthy Flow spends most of its time building, **Team
  Long Tail spends more of its time queueing than building** — the finding the whole feature
  exists to produce, and the reason the demo lands on Team Long Tail — and Team Bare Export
  carries none, so the card's empty face is reachable. Review is fed by two of Team Long Tail's
  columns. The demo's split is **deterministic and never drawn from `rnd()`**, exactly like the
  issue key counter: a draw consumed here would silently move Team Long Tail's tail and Team
  Healthy Flow's aged count. It is written in **tenths of a day**,
  because whole days on a four-day board report that every item spent zero time in review.
- What this unblocks and what it does not: blocked time and flow efficiency now have their
  export, but both still need a per-stage **waiting or working** flag, which is a decision about
  meaning rather than a parse. Neither is built. The work item age chart's stage axis WAS
  built — off the current stage rather than off these durations; see the section above it.

## Two Defaults Trimmed, and a Delete That Did Not Look Like One (2026-08-21)

- **`sameDayValue` is 0.5**, reversing a default of 1 and the reasoning that came with it ("an item
  opened and closed inside one day still occupied someone for that day"). A whole day is the same
  figure as an item that genuinely took a full day, so the two cannot be told apart in any
  percentile or average — on a board that closes a lot of small work that pulls the distribution UP,
  not down. Half a day is the most an app working in whole dates can honestly say about a span its
  dates cannot resolve.
- **The default filter list is two rows**, trimmed from five: `All` and `Defects → Bug`. The three
  that went — Spikes, Stories, Tasks — were guesses at somebody else's board, and on a team whose
  types read Feature, Chore and Incident they were three filters matching nothing, which reads as
  broken data rather than as a setting nobody set. `Defects → Bug` stays because it PAIRS with
  `unplannedType`: the same word and the same match, so the strip and the defect rate agree out of
  the box. A test pins that pairing, not just the list.
- **BOTH ARE SAFE FOR THE SAME REASON, and it is the reason a default can be moved here at all**:
  `normalizeSettings` fills gaps rather than overwriting, so they reach only a first run and "Reset
  settings to defaults" and no existing dashboard's figures move. There is a test saying so
  directly beside each new value — that property is the whole licence.
- **A TEST THAT SAVES CAN PLANT THE TRAP IT LATER WALKS INTO** (2026-08-22). `plant()` starts
  every group from known DATA (`td-state`); it does NOT touch the VIEW (`td-view`) — which tab,
  which window, the custom From/To pair — and every `saveView()` writes there. The custom-window
  group ends on a deliberate half-pair (a From, no To) to check the "Both dates are needed" note,
  and then opened by assuming both boxes were empty, which is the precondition the app's prefill
  guards on ("a pair typed earlier is theirs and is not overwritten"). So it passed on a browser
  that had never run the suite and failed from the second run onwards, on identical code —
  three red tests that looked like an app bug and were not. **CI can never catch this**: it is a
  fresh profile every run, so it only ever sees run 1. The group sets its own precondition through
  the app's own change handlers now, and restores it at the end with an assertion on the restore,
  so a broken reset fails loudly instead of going quiet until somebody runs the suite twice.
  Anything new that depends on a view value does the same.
- **WATCH FOR TESTS THAT READ A DEFAULT INSTEAD OF SETTING ONE.** Two scatter tests moved with
  `sameDayValue`, and one of them was a PAIR meant to show that changing the setting moves a dot —
  it had quietly stopped showing anything the moment its contrast value became the new default. A
  contrast test has to contrast with something the default is not, and a test about something else
  should pin the settings it does not care about.
- **`.icon-btn.danger` on the work type filter's delete.** The base hover is neutral and `.danger`
  is what turns it red — the same split `.btn` and `.btn.danger` use — and that row was the one
  place the class had been left off, so the only destructive control on the Settings tab was also
  the only one that gave no warning as the pointer arrived. Pinned as an INVARIANT over the page
  rather than as a check on that button: every icon button that deletes carries it, and every one
  that merely MOVES something does not, because reordering is not destructive and must not light up
  as though it were.

## Two Alignment Rules the Grid and the Table Were Missing (2026-08-21)

Both reported by Charles looking at the app, and both are the same shape: something stated for one
half of a pair and never for the other.

- **A CARD WITH NO CHART NOW MATCHES THE ONE BESIDE IT.** It carried `align-self: start` on the
  reasoning that it "has no reason to stand as tall as the chart beside it" — true of the card and
  false of the ROW: one card ending 200px above its neighbour is a ragged step across the grid, and
  the empty half reads as something that failed to draw. Stretch is the grid's own default, so the
  fix is removing that rule; what replaces it makes the leftover height not be DEAD space — the
  card becomes a flex column and the note grows into what is left with its text centred. **Alone on
  its row it is unchanged**, which is what was asked for and what the `.wide` stage-time card and
  everything below the 940px breakpoint rely on. Pinned in a 1240px frame, because the whole
  assertion is about having a neighbour — measuring it in a one-column layout measures nothing.
- **`td.num` IS RIGHT-ALIGNED NOW.** `th.num` always was, so every numeric column in Loaded Data
  ran its figures down the left of a heading sitting on the right. It is the same failure the All
  Teams table's own comment states in the other direction ("a heading sitting over the left edge of
  a column of right-aligned figures reads as belonging to the column before it") — it had simply
  never been said about the cells. The test asserts the cell and its heading AGREE rather than
  asserting a value, so a future re-alignment has to move both.

## Typing an Item In (2026-08-21) — no schema change

Asked for by Charles: "should we add an easy way to type data manually? not everyone is going to
be using Jira or know how to get the report out of it." The app was paste-only, which assumed both
a Jira and the knowledge to export from it.

- **IT CLOSES A SECOND GAP THE REQUEST DID NOT NAME.** There was no way to correct or delete ONE
  row: a typo meant re-pasting the export or clearing the team, and the Loaded Data card said so in
  as many words ("read-only — to correct a row, fix it in your source and paste again"). That is no
  answer when the source is somebody's own memory, and it is why this landed as an editable table
  rather than only an add form.
- **A DIALOG, NOT INPUTS IN THE TABLE.** That table sorts and is rebuilt on nearly every render, so
  a half-typed cell would be taken away by the next re-render along with the caret — the lesson
  this app has already learnt twice (the settings redraw debounce, and why `wireForecast` redraws
  only its own result region). It is also read straight off the page by the CSV writer, and an
  `<input>` has no textContent for `cellText`. Both reasons sit above the markup.
- **`buildManualRow` is PURE and returns the same shape `parsePastedRows` does**, through the same
  guards — a typed row and a pasted row have to be the same thing once saved.
- **It REFUSES a bad ordering where the paste drops the date.** Deliberate, and the reason is the
  door rather than the rule: a paste is hundreds of rows arriving from a system nobody here
  controls, so dropping one date and reporting it is the only workable answer; a form is one row
  with the person who typed it looking straight at it. Both behaviours are pinned side by side, so
  neither gets "made consistent" with the other.
- **Dates are `type="date"`, and that is half the point.** A picker has no d/m/y to guess at, so
  the ambiguous-order problem that produced a 59-day cycle time the same afternoon cannot arise
  for a typed row.
- **The stage picker follows the parser's rule** — a stage says where an item IS, so it is offered
  and stored only for work in flight, and an id nothing answers to is dropped.
- **Day counts got a control on 2026-08-22 — see the next section.** They had none until then, and
  were carried through an edit by `keepStages` instead. That path still exists and is still right
  for the case it now covers: no stages set up means no boxes drawn, and a field with no input is a
  field the next save silently drops — the trap the sibling app records under `capacityScale`.
- **The Item cell now shows the WORK TYPE where there is no key**, where it showed a dash. It is a
  control now, and a control with no name is one nobody can find or announce; it is also the same
  fallback `dotName()` uses, so an item is called the same thing wherever the app must call it
  something. The SORT is unchanged — `issueSortKey` still reads the key, so a keyless row is still
  an absence and still goes last. Two existing tests moved with it, deliberately.
- **The first-run door is on the PASTE CARD, not only on Loaded Data**, because that card is hidden
  until rows exist — so the reader this was built for met a paste box explaining a Jira export and
  nothing else. It hides once this team has rows, the same reasoning the demo button beside it
  follows: the Loaded Data card then carries "+ Add item" where you would look for it.
- **THE WHOLE ROW opens the editor**, not only the name in it (asked for the same day).
  `data-item` sits on the row AND on the button inside it holding the same index, so the one
  delegated listener's `closest()` finds the button when the name is pressed and the row
  otherwise — the same number either way, no double-open, and no `stopPropagation` to remember.
  The button stays because a `<tr>` cannot take focus: it is what a keyboard and a screen reader
  reach, and the row is the pointer's larger target. **A click with a text selection in hand is
  ignored** — this table has Copy and CSV buttons precisely because people drag figures out of it,
  and a drag ends in a click.
- **A DATE IN THE FUTURE IS REFUSED, not warned about, and the severity is why.** Every window in
  this app hangs off the LATEST date in the data rather than off today, so one item finished in
  2027 drags the whole dashboard forward a year and empties every chart on it — a mistyped year is
  the easiest typo on a date field and its consequence is a screen that looks broken for a reason
  nothing on it explains. All three date fields are checked. **`todayLocalISO()`, never UTC**: the
  rows are UTC dates, but "in the future" is a claim about the reader's own calendar, and a UTC
  comparison refuses this morning's item for anyone far enough east. The paste path deliberately
  does NOT gain this check — it reports rather than refuses, which is its whole stance.
- **The row's index is carried on the button, not its position on screen.** The table sorts, so
  what is drawn is a permutation of the array being written back to; a Map is built once per render
  rather than an `indexOf` per row.

## The Target and the Ageing Threshold Are Not Duplicates (2026-08-22) — wording only

Reported by Charles, looking at `85% ≤ 10 d` in Teams & Stages beside *count an in-progress item
as aged after 10 days* in Settings: **"are these duplicate settings?"** They never were, and no
figure changed here — but nothing on screen said which was which, and the demo happens to show 10
for both, so the question was the app's fault rather than the reader's.

- **The distinction is WHICH WORK EACH ONE READS**, and every explanation added says that first.
  `sleDays` is compared with the 85th percentile cycle time of **finished** items
  (`percentileOf(windowCycles, CYCLE_PERCENTILE) <= sleDays`); `settings.agedDays` is compared
  with the current age of items **still open** (`r.age > agedDays`). Nothing that has completed is
  ever counted by the second, and nothing unfinished by the first.
- **THE THRESHOLD NORMALLY SITS BELOW THE TARGET, and that is the part that changes what somebody
  types.** An item open as long as the whole promise has already missed it, so a threshold equal to
  the target turns the one leading indicator on the dashboard into a lagging one. The copy says
  this in the two places a number is entered and argues it in the Aged Work note.
- **Said in FOUR places, from both ends**: the Teams dialog note (where the target is typed), a
  hint under the Settings box (where the threshold is typed), the `agedWork` help, and a pointer
  back from the `cycleTimePercentile` help. A reader who is confused is looking at one of them, not
  at whichever one we decided to put it under.
- **No live "your 85th percentile is X, try Y" suggestion, deliberately.** The threshold is global
  and the target is per team, so there is no single percentile to suggest from — and a number the
  app proposed would be the app drawing a line somebody had not agreed to, which is the rule
  `wipLimit`/`sleDays` already follow.
- **They cannot be merged, and nobody should try.** Two populations, two scopes (per team vs
  shared), two defaults (null vs 14). The reason they LOOK alike is that both are a count of days
  next to a comparison operator, which is a presentation coincidence.
- Pinned in tests.html: all four passages, including the "lower" guidance, so a tidy-up cannot take
  the explanation out and leave the boxes.

## Days in Each Stage, Typed In (2026-08-22) — no schema change

Reported by Charles: *"flow metrics doesn't appears to have a way to manually key time in status
data. ensure every chart has a way to populate its data without pasting from jira."* He was right:
of everything on a row, the per-stage day counts were the only field with no door but a paste,
which made **Time in Stage the only card in the app a reader without a Jira report could not
fill** — in an app whose second door exists precisely because not everybody has one.

It stores no new field, so `SCHEMA` did not move. What changed is that `state.stages` now drives a
box per stage on the Add/Edit Work Item form, and `buildManualRow` reads them.

- **THE SAFETY ARGUMENT IS UNTOUCHED, and that is what made this a small change rather than a
  reopening of the stages debate.** What the stages section refuses is *status names* — text out of
  a work system, with no shape a regex can check. This adds no text at all: the stage was already
  named by the reader in a dialog, and what the boxes take is **numbers**. The line the earlier
  comment drew ("no honest way to type five of them per row") was about ergonomics, not safety, and
  five boxes is what the Teams & Stages dialog next door already asks for.
- **EMPTY IS NOT ZERO, and this is the one thing that would be easy to "tidy" and must not be.** An
  empty box means *no figure for that stage* and the stage is left off the row entirely; a typed
  `0` is a real measurement of an item that crossed a stage inside a day. Writing zeros into
  untouched boxes would lower every median on the card by counting stages nobody measured. This is
  the same distinction `parsePastedRows` draws off the raw cell text, and the values are read off
  the form **as strings** for exactly that reason — `valueAsNumber` collapses an empty box and a
  typed 0 into the same answer. Pinned in tests.html both ways round.
- **REFUSED, never dropped — and the ceiling is refused where a paste has it CLAMPED.**
  `cleanStageDays` quietly pins a pasted 9999 to ten years, which is right for hundreds of rows
  arriving with nobody watching and wrong for one row with somebody looking straight at it. Same
  split the date ordering already takes between the two doors, and pinned side by side for the same
  reason: neither should get "made consistent" with the other.
- **The boxes are the whole truth when they are drawn.** Clearing one REMOVES that figure — an edit
  that could not take a wrong number back out would be worse than no edit. `keepStages` therefore
  only applies when there are no stages at all, and the two paths are `if`/`else if` rather than
  both running.
- **In the reader's own stage order**, matching the card. Same reasoning as `renderStageTime`: a
  workflow has a direction, and the form and the table it feeds should scan the same way.
- **`Object.create(null)`**, as in the parse and the hydrate — the keys come off the page. Stage
  ids cannot be `__proto__` anyway (`sanitizeStages` refuses it), which is belt and braces, not a
  reason to skip either.
- **Every empty state that named only the paste now names both doors.** That was the other half of
  the request — a manual path nobody is told about is not a path. The Time in Stage card's three
  faces, the lead time note, the cycle scatter's empty face, the lead time tile's help text, the
  empty stages table, the All Teams empty face and the first-run dashboard card all changed. If a
  new empty state tells somebody to go and paste something, it is wrong.
- **Nothing else was missing.** The audit that came with this: cycle time, the scatter, lead time,
  throughput, net flow, the CFD, WIP, aged work, item age, defect rate and both forecasts read only
  `created`/`started`/`completed`/`type`, each of which the form has always had; the item age chart
  groups by `stage`, which has had a picker since 2026-08-21; the train chart reads teams and ARTs,
  both typed in dialogs. Stage day counts were the single gap.

## Three Reports From One Paste (2026-08-21) — no schema change

Charles pasted four hand-typed rows, got "Nothing to load — paste some rows first" under rows he
was looking at, and asked why. Three separate things came out of it.

- **A SINGLE SPACE IS NOW A SEPARATOR, BUT ONLY AS A FALLBACK.** `splitCells` takes a tab, a
  comma, then two-or-more spaces, and one space is deliberately not a separator: a work type is
  "Tech Debt" and a date is "21 Jan 2015". That is still true. What changed is the case where the
  rule leaves EVERY line as one cell — no columns at all, every row dropped as undated, nothing
  loaded. `parsePastedRows` now reads the paste through `readAs()` twice: the loose split is tried
  only when the ordinary one found neither a completion nor a start column, and kept only if it
  finds one. **That guard is the whole design** — it can never reach a paste that works today (a
  lone column of "21 Jan 2015" dates already found its date column, so the fallback never runs)
  and can only improve on one that was going to fail outright. Pinned from both sides.
- **"Nothing to load — paste some rows first" was being said over four pasted rows.** Two
  different failures shared one sentence. `nothingLoadedHtml()` now tells them apart on
  `res.lineCount`, and is shared by both paste surfaces — the rule `parseProblemsHtml` and
  `columnsReadHtml` already follow, because two reports drifting apart on what went wrong is the
  failure this app spends the most words preventing.
- **AN UNEVIDENCED DATE ORDER NOW SAYS IT GUESSED, and this is the dangerous one.** Every date in
  that paste read either way round, so `detectDateOrder` had nothing to go on and returned its
  day-first tie-break: 1/1/26 → 1/3/26 became a 59-day cycle time where an American reader meant
  two. The order has always been stated in the report; what it never said was that it was a
  guess. `dateEvidence()` was split out of `detectDateOrder` to count the ambiguous cells as well
  as the decisive ones — the second number is worth as much as the first — and `orderGuessed`
  fires only on Auto-detect with no decisive date and at least one ambiguous one. A reader who
  chose an order is not guessing, and a paste of ISO dates has nothing to guess about.

## Delete All Data Takes the ARTs and Stages (2026-08-21)

Reported in the same breath: "arts and stages aren't deleting when I hit delete all data". They
were not in the reset at all, so a reader who had set up four stages and a train found both still
there under a toast reading "Everything deleted — starting fresh", with the dialog having said
nothing about either.

- **The line is DATA vs SETTINGS.** A stage carries the status names typed off an export and an
  ART is a grouping of teams; `settings` is the labels, thresholds and work-type filters the
  dialog explicitly promises to keep. Both halves are pinned, so neither can drift.
- **The dialog now lists what it will take**, ARTs and stages included, built from what is
  actually there. A delete that destroys something it never mentioned is the part that made this
  a bug rather than a preference.
- **`view.artFilter` is cleared with them**, rather than left for `currentArtScope()` to correct
  on read: leaving a stale id in the saved view means the next thing to read it has to know that.
- **The sibling does NOT have this bug** — Sprint Predictability clears through `blankState()`,
  which wipes every collection by construction. This app rebuilt `state.teams` by hand, which is
  exactly how a collection gets forgotten. Checked, not assumed.

## Charts Draw in the Pack's Series Ramp, Not the Accent (2026-08-21)

`--series-1` and `--series-5` for the two data colours, where every chart used `--accent` and
`--serious`. Reported by Charles: "why do the charts in SV have colours in the sepia theme but
TD's don't? they are all just kinda black and gray."

- **`--accent` IS NOT A CHART COLOUR.** It is the app's emphasis colour, and in two themes out of
  four the palette makes it the INK — Sepia's `--accent` is `#3a3020`, which is also its
  `--text-primary`, and Dark's is `#eef0f5`, which is also its. So a throughput line was drawn in
  the body-text colour. It reads fine on Midnight (indigo) and Light (blue), which is why it went
  unnoticed for so long: the two themes it is wrong on are the two nobody was developing in.
- **The grammar did not change, only the source.** One colour for the measure, a second for the
  other thing on the chart, and every rule about which goes where is exactly as it was — net flow
  below zero, defects raised, the 85th percentile, aged dots and the ageing threshold line all
  still take the second colour; aged BARS still deliberately do not.
- **Why 1 and 5, not 1 and 2.** The comments through `drawCharts` have always described the pair
  as blue and orange ("blue above zero, orange below"). `--series-1` and `--series-5` are the blue
  and the rust in all four themes, so this is the first build where the colours match what the
  code already said they were.
- **Annotation stayed muted.** `trendDataset` and the median/85th reference lines keep
  `--text-muted` / `--text-secondary`. They are drawn OVER the data, and colouring them puts them
  in competition with the thing they exist to be read against. Pinned.
- **The All Teams sparkline moved with them**, for the same reason it reuses `linearTrend`: it
  plots throughput, so it is drawn in throughput's colour. On Sepia and Dark `--accent` made it
  one more piece of the table's text.
- **This is adoption, not drift.** The ramp is the pack's (added 2026-08-21, gated harder than the
  status tokens, picked off the blue-yellow axis so no two collapse under red-green deficiency)
  and this app already links the stylesheet — the colours were sitting in it unused. **Flow
  Metrics' per-team lines were the open item in that adoption and remain closed for their own
  reason**: eight teams, a ramp that stops at five, and a spaghetti chart either way.
- Pinned across all four themes by the assertion that names the bug — a data series is never
  `--text-primary` — plus a source check, and a rule check on `.spark`.

## A Tile Row Never Strands a Tile (2026-08-23) — family-wide

**A `.tiles.group` row fills ONE line when the line has room for every tile, and splits into
EQUAL rows when it does not.** Money Map hit this first — six net-worth tiles came out five
across with the sixth alone underneath — and every app in the family with a variable-count tile
row now answers it the same way. Here it was Flow's five tiles at four across: four figures and
then one, reading as an afterthought rather than as the fifth answer.

- **The COUNT comes from `:has(> :nth-child(N):last-child)`** — "exactly N children". The panels
  differ by design: five tiles on Flow, four on Delivery, three on Health and Forecast.
- **The WIDTH comes from a CONTAINER query, never the viewport.** `:has(> .tiles.group)` makes
  the chart panel the named container `tiles`, so the row is measured as it actually sits, card
  padding already off. Where no container is found the row keeps the plain auto-fit line.
- **The thresholds are the 200px minimum tile and the 12px gap multiplied out**: 2→412, 3→624,
  4→836, 5→1048, 6→1260, 7→1472, 8→1684. Narrowest first, so the widest rule that matches wins.
  tests.html reads those two numbers back out of the CSS and checks every threshold against
  them, so raising the minimum tile fails the suite rather than quietly making a row too tight.
- **Only counts that leave rows differing by at most one tile are offered, and never a row
  holding a single tile.** Five go 5, or 3 + 2, or one per line — never 2 + 2 + 1. Seven go 7 or
  4 + 3. Where the only alternative would strand one tile the row drops to a single column.
- **A short last row is STRETCHED to finish the line**, never left with a hole at the end of it:
  `lcm(columns, last row)` tracks, the full rows' tiles spanning `lcm/columns` and the last
  row's `lcm/last row`, so Flow's 3 + 2 is six tracks at span 2 and span 3. Golf Handicap's
  hand-counted grid, generalised to every count. The stretch is undone at the width where the
  tiles all fit on one line, and on BOTH selectors — `:nth-child` out-ranks a bare `> *` and
  would otherwise carry its span into the wider layout.
- **THE FOUR DASHBOARD TILES ARE THE DELIBERATE EXCEPTION AND STAY ONE.** `.tiles` without
  `.group` is always exactly four, one per dimension; spelled-out columns and its two media
  queries are already gap-free at every width, and a test asserts nothing counts children on
  plain `.tiles`. Sprint Predictability has the same block against its own `.tiles`, with a
  160px floor — the counts there vary, which is the whole difference.

## One Surface for the Whole Page (2026-08-21) — a divergence from the sibling

`.tile` moved from `--surface-alt` to `--surface`, the ground the chart cards and the tables are
already on. Reported by Charles looking at Sepia, where the two are a tan and a cream and the four
headline tiles read as a band of something else sitting above the charts rather than as the
summary of them.

- **NO PALETTE CHANGE, and that is the point.** This swaps which existing pack token an element
  reads; it does not invent, tune or override a colour, so `~/claude-theme-pack` is untouched and
  no contrast gate is involved. That is the same move the a11y contrast fixes take — reuse a
  token, never add one — and it is the reason this did not need deciding with Charles as a
  palette question.
- **Pinned in ALL FOUR THEMES, and pinned as a relationship rather than a value.** The test asserts
  `.tile`, `.chart-card` and `.card` share a background and that all three still differ from the
  page behind them; it never names a hex, because those belong to the pack. A palette edit lands
  in every theme at once, which is why one theme would not have been enough.
- **The 4px left edge went to 6px in the same change, and it is the same change.** The tile used
  to be told apart from the card beside it by its FILL; it is told apart by that edge now, so the
  edge has to carry it — 4px is the right weight for a marker on a tile that is already a
  different colour, and on a row of tiles that are not it reads as a slightly heavy border.
  **Don't go past 6**: beyond that it stops being an edge and starts being a column, and it eats
  into the 14px of padding the label is set against. Pinned as a RELATIONSHIP (heavier than the
  other three borders), never at 6px — the number is a judgement and may be tuned again.
- **`.tile-help:hover` moved the other way**, `--surface` → `--surface-alt`. Every surface that
  button now sits on is `--surface` — a tile, a chart card's name row, an All Teams heading — so
  the old fill was a visible hover on a tile and no fill at all on a chart card. The one place the
  two backgrounds differing was doing any work, and it was doing it backwards. **This hover is
  now the family's** (2026-08-23): Money Map reached for `--focus-border` instead, which says
  "focused" to anybody reading the two states side by side, and this one won the sweep.
- **THE INFO DOT AND THE HELP WINDOW ARE FAMILY-WIDE BLOCKS, DECLARED PROPERTY BY PROPERTY, AND
  THE SAME IN EVERY APP THAT HAS ONE (2026-08-23).** A change to either belongs in all of them.
  - The dot is a 16px outlined circled **"i"** — `.tile-help`, `min-height: 0`, `margin-left: 7px`,
    and a 24px tap target from an unpainted `::after` so the line's height never moves. Golf
    Handicap and the NY calculator drew a "?" in a filled 18px pill until that date; "i" won
    because "?" is the glyph a browser already puts on its own help cursor and in a form's
    validation bubble, and it asks a question where this thing answers one.
  - The window is sized by its TEXT: `#helpBody` capped at a 66-character measure and
    `#helpDialog` at `width: fit-content`, so the window takes the measure as its width — 666px
    with 624px of text, the same figure in every app. Both rules or neither. **This app's half of
    the drift was the type**: the help ran at `--fs-xs` (13px, the size of its chrome and its
    table headings) across the full 560px, about 80 characters a line, while Money Map capped its
    text at 66 characters and Sprint Predictability at 46. The block pins `--fs-sm` — and,
    since a second pass on 2026-08-23, the heading (`--fs-md`/600), the prose colour
    (`--text-secondary`), the paragraph margins, `#helpBody strong` and the window's own
    `padding: 20px` as well. Four things were still riding on inheritance across the family:
    an unset heading weight defaults to bold, an unset paragraph colour lands on
    `--text-primary`, browser paragraph spacing is 1em rather than 10px, and each app's
    dialog padding decided the window's width. Nothing here moved except the padding, which
    was already 20px, so this app came out unchanged on screen.
  - **A HELP BODY IS AN ARRAY OF PARAGRAPHS, NOT A STRING** (2026-08-23), and a paragraph is an
    array of runs: a plain string, or `b('…')` for bold. `renderHelpBody` walks it with
    `createElement` and `textContent`, so **none of it is ever parsed as markup** — which is what
    lets a note here quote a reader's own stage name safely, and is the same rule `pre-line` used
    to be protecting. Money Map carries the identical pair; the other five apps write their help
    as HTML literals and are right to.
    Every entry was one block of 230 to 1,900 characters before this. Bold carries the thing
    being defined or the load-bearing claim, **at most one per paragraph**, and `tests.html` pins
    that: every entry is more than one paragraph, every entry bolds something, and no entry has
    more bold runs than paragraphs.
  - **`#helpBody { white-space: pre-line; }` IS GONE, and `#helpBody` is a `<div>`.** The rule
    existed because the help was one string: a blank line was its only paragraph break, and at
    `normal` a note written as three paragraphs arrived as one wall of text. The breaks are
    structural now, so `pre-line` would only turn every wrapped line in the SOURCE into a break
    on screen. A `<p>` cannot hold paragraphs, hence the `<div>`.
  - **Two ALL-CAPS emphases in the Aged Work note became bold**, and the tests that pinned them
    had to follow — a caps match proved the emphasis was there, and a `<strong>` is what proves
    it now.
  - **`tests.html` deliberately does not cross-check dots against entries, unlike the sibling
    suites.** This app passes the key as a variable — `helpBtn(helpKey, label)`,
    `helpBtn(c.help, c.label)` — so a scan for quoted keys finds one of twenty-one and would go
    green on nothing. What is pinned instead is the guard that makes a wrong key harmless:
    `helpBtn` returns `''` when the table has no entry, so a bad key draws no dot at all.
- **THIS IS A DELIBERATE DIVERGENCE FROM SPRINT PREDICTABILITY**, which shares this tile and keeps
  `--bg-card-alt`. It is not drift and it should not be "fixed" by mirroring without thinking: the
  sibling has a `.tile.hero`, which stands out from its neighbours *by being the card surface*.
  Make every SV tile the card surface and the hero has nothing left to be. This app has no hero
  tile, so the same change costs it nothing. Recorded in both READMEs as the second noted
  exception to the shared-chrome rule, beside the tile column counts.

## The Boot Hold, and All Four Tabs (2026-08-21) — no schema change

Both halves of one report from Charles: a refresh flickered badly, and a refresh on Your Data or
Settings landed somewhere else.

- **`html[data-booting] .shell { visibility: hidden }`, set in the `<head>` script beside the
  theme and lifted by `bootDone()`.** The cause is structural rather than slow: this is 560KB of
  markup a browser paints AS IT PARSES, with the script that fills it at the foot, so ~100ms of
  empty skeleton assembled and then popped. Worse on the other tabs — `#panel-dashboard` is the
  one visible in the markup, so a boot landing anywhere else painted the dashboard in full and
  swapped it out.
- **`visibility`, NEVER `display`.** A hidden box still has a size; a `display:none` one does not,
  and Chart.js measures its canvas the moment it draws. Under `display:none` every chart would
  boot at 0×0 and need re-drawing rather than resizing. Pinned, because `display:none` is the
  obvious "tidier" edit and it would break silently — the charts would look fine after the first
  resize.
- **The header is deliberately NOT held.** Everything in that row already carries its final width
  in the markup (`#teamSel` has a `—` placeholder and a 140px floor for exactly this reason), so
  it is correct before the script runs, and hiding it would move the flicker rather than remove it.
- **THE BACKSTOP IS PART OF THE FEATURE.** The reveal is also on a `setTimeout` set in the head
  script itself, before anything that can throw — a boot that dies would otherwise leave a blank
  page for ever. Two seconds: far past a normal boot (~150ms), far short of giving up. Every exit
  calls `bootDone()` anyway — the ordinary branch after `selectTab`, `openSharedView`'s `finally`
  (it is async, and both the teams and the error card count as something to show), and
  `haltForNewerData`, which throws and so would never reach either.
- **All four tabs are remembered now**, not the two number views. The old reasoning — Settings and
  Your Data are "places you go to do a thing and then leave" — is true of the trip and false of the
  refresh: reloading to check something is not leaving, and being thrown to the dashboard mid-edit
  of a work-type filter costs finding your way back to the row you were typing in. No new guard
  was needed; `selectTab` already refuses a hidden or unknown tab.

## Six Bugs Found by Reading (2026-08-21) — no schema change

A read-through of the whole file after the trend column landed. Nothing here needed a stored
field, and all six were the same shape: a figure or a sentence that described something other
than what it was next to.

- **Time in stage read every row the team held, not the window.** `stageTimesOf(items)` where
  every other figure on that screen is built from the bucket walk — so one month, three months
  and all data gave identical medians under a note that had just said which three months were
  being shown, and the comment on the returned field asserted the opposite of what the code did.
  It now takes `windowItems.concat(items.filter(r => !r.completed))`: what finished inside the
  window, plus what is open now. **The open half has to be added rather than walked to** — an
  open item has no completion and so no bucket — and it belongs in scope because it is in scope
  everywhere else on that screen. The card's empty face gained the window as a possible cause,
  or a team whose stage times all sit outside the picker is told to change the work-type filter.
- **The window note stated `itemCount`, which is deliberately not windowed.** "14 weeks · 190
  items" about a window holding 67. `itemCount` is right as it stands and pinned as such — the
  window trims weeks, not rows — so the fix is the sentence: `windowItemCount` is a second field
  and `itemsInWindow()` writes "67 of 190 items", dropping the "of" form when the window covers
  the lot. **One helper for both notes**, the dashboard's and All Teams', because they are the
  same sentence about a different scope.
- **`unmatchedStatus` counted rows the parser then threw away.** The in-flight-only rule exists
  so a file full of "Done" cannot make that count read 800; it did not reach the rows dropped
  further down the loop, and an untouched backlog item — a status, no dates at all — is dropped
  by the `undated` return. So an ordinary export made the note say "400 items had a status no
  stage answers to" and sent the reader to check spellings that were right. **The whole stage
  block moved below the three `return`s**, bad-cell tally included: "left out" is a claim about a
  row that was kept.
- **The trend column exported as text.** It wrote U+2212 MINUS and a "±" for a flat run, both of
  which a spreadsheet refuses as numbers — in the one column whose entire point is its sign, in
  tables the README describes as arithmetic you can do. Now ASCII, with an explicit `+` on a rise
  and a plain `0.0` when flat. **`FORMULA_LEAD` was rewritten to match**: the test is now "is the
  whole cell a number?" (`PLAIN_NUMBER`) rather than "does the character after the sign look
  numeric", which lets `+4.3` through and newly catches `-3abc`, `-1+1` and `+A1` — stricter in
  both directions, and the DDE payloads are still defused because none of them is a number.
- **Every All Teams column named a `help` key and the header render never read one.** Dead since
  the view was built, and two of the notes behind it — the throughput trend and Data to —
  describe columns that exist ONLY in that table, so they could not be opened anywhere. Wired up
  **for those two and deliberately not for the other seven**: those are dashboard tiles laid on
  their side and the tile already carries the note, and nine circles at 28px apiece measured the
  table over the width of an ordinary window and into a sideways scroll it had always fitted
  inside (1373px against 1265). The ⓘ is a SIBLING of the sort button inside a `.th-head` flex
  wrapper — a button inside a button is invalid, and `display: flex` on a `<th>` stops it
  generating a table-cell box and unpicks the column alignment. The sort arrow's selector needed
  `:not(.tile-help)` or it landed on both buttons.
- **"five items aged past the threshold" — it was six.** Team Long Tail's `wip` list gained an
  item, the README was corrected and the Load-sample dialog was not. Counted from the profile
  now (`DEMO_AGED`) rather than written out, against `DEFAULT_SETTINGS.agedDays` with the
  threshold named in the same sentence — the live setting would be wrong in working-days mode,
  where these ages are calendar days. A test asserts the dialog's own text against the derived
  figure.

## Four More Found by Reading (2026-08-21) — no schema change

A second read-through, after the stage axis landed. Same shape as the six above: three of the
four are something on screen describing what was true before the last change rather than what
is true now.

- **Deleting a stage left the "sitting in it" pointers behind.** A row references a stage two
  ways — `g`, the days it spent there, and `w`, the stage it is in RIGHT NOW — and the delete
  handler only knew about the first. Two consequences, and the second is the one that made it a
  bug rather than an untidiness. The confirm counted `g` alone, so on **the ordinary-export case
  this app was built for** — a Status column and no durations anywhere — the row's own count
  column said "4 items" and the confirm directly under it said nothing was going. And the `w`
  pointers survived into `persist()`, so localStorage held a pointer at a deleted stage until
  something reloaded the page and `hydrateState` pruned it. **The ART delete a section above has
  always nulled its dangling `artId` on the spot**; this is the same call, and the fix is to make
  both halves of the stage delete do what that one does. Pinned by a group of its own, driving
  the real button with a stubbed `confirm` and reading the message back.
- **The work item age ⓘ still said "Columns are work types."** It has been the stage axis since
  the Status column landed the same day, and the demo's own default team draws it that way — so
  the first note a reader opens off the first board they are shown described the chart in front
  of them incorrectly. The README's *Columns Are Workflow Stages — or Work Types* had been
  written and the ⓘ had not. It now says both readings, in the README's own order, and says why
  there is no picker.
- **`#helpBody` had no `white-space` rule, so a note written as paragraphs arrived as one
  block.** The body is written with `textContent` — never markup, which is what lets a note
  quote a reader's own label safely — so its only paragraph break is a newline, and at `normal`
  a blank line collapses to a space. The throughput trend note is three paragraphs and read as a
  wall. `pre-line` honours the breaks and still collapses ordinary wrapping whitespace, so
  nothing else moved; the age note above now uses it too.
- **Two `Math.min/max.apply(null, …)` calls over a team's own items.** `minOf`/`maxOf` exist a
  few hundred lines above them, with a comment explaining why the forecast does not spread ten
  thousand trials across a call's arguments — and past an engine limit (65,536 in WebKit) that
  is not slow, it throws. The two here walk a list whose length is the reader's export rather
  than a constant this app picks, which is the weaker case for the same rule. Both now go
  through the helpers, and the comment on them says why every min/max over a list does.

Also tidied: the `.skip` CSS block had picked up a blank line between every line of it, and is
now byte-identical to the sibling apps' copy again; and the comment over `let activeTab` still
read "not saved — a reload should open on the dashboard", which stopped being true when
`view.activeTab` landed.

## The Current Stage (2026-08-21) — SCHEMA 8 → 9

> **SUPERSEDED IN PART ON 2026-09-01.** The `w` this section added is now the LEGACY half of
> the field: a row that carries a status resolves its stage through `stageOf` at read time and
> writes no `w` at all. The in-flight-only rule, the anchored heading and the axis-switch-not-a-
> picker decision all survive unchanged and are still governed here. See **The Status Is Stored
> Now** above.

`r.stage` on each row (`w` on the wire), read from an ordinary **Status** column. It exists
because Charles's own export has statuses and no durations, which is the ordinary Jira case —
the day counts above need a marketplace add-on, and this needs nothing. It reuses the stage
machinery whole: same stages, same aliases, same argument.

- **The untrusted text is now in a CELL ON EVERY ROW rather than in one header**, which makes
  the storage claim matter more, not less. The status is matched against the aliases the reader
  typed, the STAGE ID is stored, and the word is discarded with the paste. A cell matching
  nothing stores nothing — it is not kept as a label, shortened to fit, or echoed on screen.
- **The SAME aliases serve both halves**, deliberately. A stage listing "Ready for Code Review"
  and "Code Review" reads a time-in-status export's HEADINGS and a plain export's CELLS off one
  setup, so a board that later gains durations needs nothing re-typed.
- **Only read for work still IN FLIGHT.** Every export says "Done" or "Closed" against
  everything it has ever finished, which is most of the file: reading those would file the whole
  history under a stage nobody has, store a useless id on every completed row, and make the
  unmatched-status count read "800 items" on a healthy set-up. A finished item's current status
  says nothing about flow, and the one figure this field feeds looks only at work in progress.
  Pinned both ways.
- **`HEADER_PATTERNS.status` is ANCHORED**, the second anchored pattern after the key and for
  the same reason: "Status Category", "Status Category Changed" and "Status changed date" are
  all real Jira headings a loose `/status/` would swallow, and the last is a DATE. Only `Status`
  or `Current status` counts. **There is no headerless fallback** — a status column looks
  exactly like a work-type column from the values alone.
- **The column is claimed even when no stage will match a value in it**, and that is a fix as
  much as a feature: a Status column is a short repeated label, which is precisely what the
  work-type detector hunts for, and "Ready for Code Review" is inside `cleanWorkType`'s 40-char
  cap. Before this role existed a headerless-type export could file its statuses as work types.
- **THE WORK ITEM AGE CHART NOW GROUPS BY STAGE**, which ends the compromise the README has
  carried since that chart was built. It **switches rather than offering a picker**: a picker
  is a control set once and never touched, and nothing is lost without one — the work-type
  reading is a filter away, and scoping the strip to Bugs makes this chart answer "where do
  defects get stuck", which is strictly more than the type axis ever said. Falls back to work
  type when no item in flight carries a stage, so a team like Team Bare Export is unchanged.
- **Stage columns keep the READER's order, where type columns rank busiest-first.** A workflow
  has a direction and that order is the one thing the reader already knows how to scan. Only
  stages holding something in flight get a column: an empty one is a gap in the axis that costs
  width and reads as a chart that failed to draw. `AGE_NO_STAGE` and `AGE_OTHER_STAGES` are
  pushed right like their type counterparts, which is what keeps the right-hand edge the quiet
  corner the reference-line labels are drawn in.
- **The tick carries the count — "Review (4)"** — because "how many are sitting in each stage"
  is the other half of what this axis was asked for, and putting it on the tick answers it
  without a second card. NOT done on the type axis, where the columns are already ordered by
  size and the number would restate the ordering. `ageing.columnNames` carries the bare labels
  so nothing has to parse a count back out of a string.
- **`derive()` gained a fourth argument, `stages`**, and it is the one piece of naming that
  function takes — for the one figure that puts names on an axis. Optional: a caller passing
  three arguments gets the work-type columns, which is every test written before stages existed
  and is why this landed without test churn. `stageTimesOf` stays nameless; do not "tidy" the
  two into one convention.
- **The Time in Stage card knows the status-only case and says so.** A team with current stages
  and no durations gets a message saying its stages ARE working and pointing at the age chart —
  not "you have no stage data", which would send somebody to check a set-up that is right.
- **The demo's Team Long Tail carries one status no stage lists** — "Compliance Review",
  straight off Charles's own workflow — holding its second-oldest item, so the "No stage" column
  and the unmatched-status note are both reachable AND both worth acting on. Its in-flight
  statuses are matched POSITIONALLY to the `wip` ages, so three of the four oldest sit in Test
  and the bottleneck is a column you can point at. `statusOf` never draws from `rnd()`, like
  every other demo field added since the issue key.

## The Project Id and the Multi-Team Paste (2026-08-20) — SCHEMA 6 → 7

`t.projectId` on each team, `projectId` on the wire (no short name — a team is not a row, and
its fields are already spelled out). One export covering a whole train, split by the letters at
the front of each issue key: DAE-1552 goes to whichever team is set to DAE. It is the first
thing the key made possible that is not a label on a chart.

- **The guard is the SAME SHAPE as the front of `ISSUE_KEY_RE`**, deliberately, in
  `cleanProjectId` — and it is built that way because a value that could never begin a key is a
  routing rule that could never fire; there would be no honest way to tell somebody why their
  rows went nowhere. Both boundaries again (the input handler and `sanitizeTeams`), drop-whole
  again, folded to upper case again. The reasoning that let the issue key in covers this too: a
  regex can tell it from a sentence. **Still not precedent for a third field.**
- **A LABEL and an address, never a level of maths** — the ART rule, third time. Nothing counts,
  groups, filters or sorts by the project id. `routeRowsToTeams` is the one place a row's team is
  decided, and it is pure: it takes the team list, so the dialog can show the plan before
  anything is written and the tests can pin both.
- **Nothing is guessed at.** Three separate buckets — `unclaimed` (no team answers to the id),
  `ambiguous` (two do), `noKey` (no key to read) — because the three have three different fixes.
  Nothing is ever routed to the first team or to the active one: a row in the wrong team's
  throughput is a wrong number nobody can see, where a homeless row is a message on screen.
  **A clash is refused, not resolved.** Which team a project belongs to is the one question the
  app cannot answer, and picking one would silently move somebody's throughput.
- **The whole paste goes through `parsePastedRows` ONCE.** One export has one column layout;
  detecting columns per team would let the same file be read two different ways.
- **Check before load.** `runMulti('check')` writes nothing and says so; the replace names every
  team it would overwrite and what each loses. This is the one surface that can destroy data on
  boards nobody is looking at, which the team-at-a-time box cannot.
- **The box is cleared only when there is nothing left to do with it** — with an unclaimed id
  still listed the next step is "create the team, split again", and clearing would have thrown
  away the paste that step needs. And the clear happens AFTER `showMultiNote`, which reads the
  box to tell "nothing pasted" from "nothing loaded"; clearing first made a successful load
  report that nothing had been pasted at all. Both bit during the build.
- **Creating a team from the report is offered, never done.** A paste is not a reason to invent
  teams in somebody's dashboard, and an export with a stray project in it is ordinary. Pressing
  it creates the team with the id already set and re-runs the CHECK — agreeing to a team is not
  agreeing to replace three others.
- **A single-team paste fills in a team's id for it**, but only when the team has none, only
  when the keys are UNANIMOUS (`soleProjectId`, floor of 3), and never into a clash. Typing an id
  per team is exactly the setup step that would otherwise stand between a first paste and this
  feature working. A majority is a question, not a fact; and adopting into a clash would break a
  split that works today to fill in a field nobody asked for.
- **`SHARE_PAYLOAD_V` was NOT bumped and the id does NOT travel** — the first field to be left
  out of a link deliberately rather than by version. A viewer has no paste box, so it would
  route nothing; and every key in the payload already carries its project at the front. The
  payload's team whitelist is explicit, so this is what happens by default — pinned anyway.
- **`tdAdopt`'s losing-a-field prompt was NOT extended to it.** That prompt exists for a column
  pasted per item that cannot be got back; a project id is one word re-typed in a dialog, the
  same reasoning that keeps ARTs out of it.
- `parseProblemsHtml` and `columnsReadHtml` were split out of `showParseNote` so both paste
  surfaces explain one export the same way. Two reports drifting apart on what a column was read
  as is the failure this app has always spent the most words preventing.
- The demo's two keyed teams carry the ids their keys are built from and Team Bare Export
  carries none, so both faces are reachable from Load sample data — and the demo is itself a
  multi-team export that splits back into the teams it came from, which a test pins.
- `table.manage input.projid` has to sit AFTER the 320px `input[type="text"]` cap it shares its
  specificity with, or it loses. `text-transform: uppercase` shows what is actually stored as it
  is typed; the placeholder is exempted, or "e.g. DAE" shouts.

## The Issue Key (2026-08-20) — SCHEMA 5 → 6

`r.key` on each row, `i` on the wire. Asked for so the scatter plots can name the item behind a
dot: "which of these needs reviewing" is unanswerable when every dot is called Story.

- **The guard is a SHAPE, not a cap** — `ISSUE_KEY_RE` in `cleanIssueKey`, applied at both
  boundaries (`parsePastedRows` and `hydrateRows`) exactly as `cleanWorkType` is. A value that
  fails is dropped WHOLE. This is the point of the whole feature: the cell that arrives here
  when somebody's column map is off is a ticket summary, and seventeen characters of a summary
  is still a summary. **Never relax this to a length cap**, and never "just trim it to fit".
- **`i` is omitted when empty**, so a team that has never pasted a key serialises
  byte-identically to before — the rule the created date and `artId` already follow, and what
  keeps the first save after this build from rewriting the whole stored document.
- **`SHARE_PAYLOAD_V` was NOT bumped**, matching ARTs. Keys DO travel in a link, deliberately:
  they name the dots, and a link that dropped them would show the recipient a different picture
  from the sender's. An older cached build drops the field and names dots by type — graceful
  degradation. The share dialog and `privacy.html` both say keys travel; keep that true.
- **Detection is deliberately narrow at BOTH ends.** `HEADER_PATTERNS.key` is the only anchored
  pattern in that table (`^\s*(issue\s*)?key\s*$`), because a loose `/key/` eats "Issue id",
  "Parent key" and "Key changed date" — all real Jira headings, all pinned by tests. The
  headerless fallback asks `keyRate >= 0.8` on `columnStats`, i.e. it asks the same question
  `cleanIssueKey` will ask, so a column it picks is a column whose cells will actually store.
  A date can never score, and neither can a summary — which is what tells the key column from
  the all-distinct column beside it.
- **The key is a LABEL, never a level of maths** — the same rule ARTs follow. Nothing counts,
  groups or filters by it. `dotName()` is the one place a dot's name is decided, shared by both
  scatters so they can never drift; `issueSortKey()` is the one place the Item column's order is
  decided (zero-pads the number so DAE-10 doesn't land between DAE-1 and DAE-9).
- **Two demo teams carry keys and Team Bare Export deliberately carries none**, so both faces are
  reachable from Load sample data — named dots, and the type-named fallback. The generator's key
  counter must never draw from `rnd()`: the sequence is seeded and every pinned demo figure
  depends on it.

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
  its first save after this build lands doesn't rewrite the whole stored document — the same rule
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
  "Team Healthy Flow" to "Team He" on a phone; the row simply outgrows the dialog and
  `.table-scroll` does its job.
- **The demo puts two teams on one train and leaves one on none.** A train per team makes
  grouping look pointless; all three on one leaves the No ART option absent. Pinned, including
  that scoping to the train visibly moves a figure — a picker that changes nothing on the one
  dataset anybody is shown is a feature nobody will find.
- A fixture with a literal `</script>` in it closed the script block in tests.html and the whole
  suite silently stopped running. Hostile-id fixtures use `'"><script>'`, the form the existing
  team-id tests already use.

## Both Tables Sort, in Three States (2026-08-20)

The Loaded Data list sorts the way All Teams does. `dataColumns()` mirrors `teamColumns()`:
`get` returns the value a sort COMPARES — the underlying date or number, never the rendered text,
so "in progress" and "—" sort as the absences they are rather than alphabetically among real
values.

- **`nextSort()` is shared by both tables, and it is THREE states**: the column its own way, then
  reversed, then off. Both tables have a default order that was chosen and is worth getting back
  to — All Teams opens in the picker's order, Loaded Data with the items still in play at the top
  — and with a two-state toggle those were reachable exactly once, on the first render, with a
  reload the only way back. Don't reduce it to two.
- **Nulls sort LAST in both directions**, the same rule as All Teams: an item in progress has no
  completion date and no cycle time, and letting it win the top of "shortest cycle time" is the
  one result nobody could read past.
- **The period column sorts by the completion date behind it**, never by its own label: "Aug 2026"
  and "Sep 2026" sort backwards as text, and a week key only happens to sort right because it is
  written year-first.
- Sort state lives in `view` (`dataSort`, `dataSortDir`) — per device, no schema — and the export
  reads the rendered page, so **the sort travels into a CSV**. The arrow on a sorted heading is a
  CSS `::after`, so it does NOT: pinned, because a stray ↓ in a header cell is exactly the kind of
  thing that would reach a spreadsheet unnoticed.
- **A test-isolation lesson worth keeping.** These DOM groups share this origin's saved `view`
  with whatever was last pressed in the app, so a table can arrive already sorted and an assertion
  about the default order passes or fails on luck. Both groups now cycle any live column back to
  off before asserting — which is only possible BECAUSE of the third press. The All Teams group
  had the same latent fragility and had simply been getting away with it.

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
- **The formula guard is a security boundary, not a formatting nicety.** A cell opening with
  one of OWASP's six leads — `=` `+` `-` `@` TAB CR — gets a leading apostrophe unless the
  WHOLE cell is a number (`PLAIN_NUMBER`). The tab and the carriage return are in the set
  because a reader that strips the leading whitespace then finds the formula underneath;
  neither can begin a number, so they cost the carve-out nothing. A team name is the one
  free-text field this app stores and a share link is how somebody else's text reaches this
  browser, so a CSV is simply the one place the escaping is not HTML. A **number is
  deliberately left alone** — net flow is negative half the time and quoting it would break
  the arithmetic.
  **These two lines are the family's one CSV rule.** As of 2026-08-27 the identical
  `FORMULA_LEAD` / `PLAIN_NUMBER` pair is in all seven exporters — here, Golf Handicap,
  PAPTrack, Sprint Predictability, the starter and both lottery pages — and a change to it
  belongs in all of them. Money Map is the one deliberate exception: it builds its rows from
  state, so it can pass an `isText` flag and guard only the cells it knows are text.
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

## The Teams Dialog Follows the Sibling's (2026-08-20, third section 2026-08-21)

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
  for Back up, which is a few lines, and wrong for a table of teams: at 560 a row's name box,
  picker, count and delete were shouldered into each other. **The help window no longer takes
  that default at all** — since 2026-08-23 it is sized by its own text (see below), which comes
  out at 666px.
- **A HELP TITLE OR BODY MAY BE A FUNCTION, and three of them are** (2026-08-27, found by
  sweeping every help window in the family). Everything else on this page reads its unit
  noun out of derive()'s `Unit`/`Units` block — that block exists so nobody spells "item"
  out — but `METRIC_HELP` is a module-level literal, so its titles were the one set of
  words on screen that could not follow the Count switch. With it on Features, three
  windows opened headed **Item** beside a tile reading **Feature**: `cycleScatter`,
  `itemAge` and `forecastHowMany`. The dots' own aria-labels had been following the
  switch the whole time; only the window they opened did not.
  `helpUnit()` / `helpUnits()` sit beside `featureUnit()` and are resolved when the
  window OPENS, and the click handler calls a `title`/`body` that is a function — the
  arrangement Sprint Predictability already uses for a metric's `target` line.
  Three things worth keeping. It reads **`featureUnit()`, not `view.unit`**, because that
  is this app's single answer to "which list are we reading" and already guards a dozen
  readers: a stored `'features'` with no features left has to read as items here too, or
  the window names a list the page is not showing. **`forecastHowMany`'s BODY moved as
  well**, and it is the only one that had to — its last paragraph makes a counting claim
  ("it counts items, not points or value"), which in the other unit is a wrong statement
  about the figure rather than merely a wrong noun. And **`featureSize`, `featureProgress`
  and `schedule` still hard-code a noun on purpose**: those three are about FEATURES
  whichever list is being counted, and a test pins that they are the only ones left doing
  it, so a new entry spelling a unit into its title fails.
  **Known and deliberately not done:** `cycleScatter`'s and `itemAge`'s BODIES still say
  "item" throughout (~7 and ~12 times). Much of that prose is genuinely item-specific —
  issue keys, work types, workflow stages — so substituting a noun through it would make
  claims that are not true of features. That is a content rewrite, not a naming fix.
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
- **The demo's Team Bare Export carries `stale: 9`**, shifting its whole history back nine days.
  Its own dashboard is untouched (every window hangs off the latest date in the data, so the
  picture moves with it); on All Teams it is the team with nine silent days dragging its rate
  down. Without a team like it the Data to column is a row of matching dates that looks like it
  does nothing — which is exactly what the demo rule exists to prevent.
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

## The Planning-Increment Window (2026-08-20)

`months: 'pi'` is the one window value that is not a number of months. `PI_WEEKS = 12` — six
two-week sprints, matching the sibling's `SPRINTS_PER_PI = 6` and its 14-day cadence — and the
span is `addDays(endDate, -(PI_WEEKS * 7 - 1))`, i.e. 84 days flat.

- **Not expressed in months.** Rounding 12 weeks through months would land it a few days out of
  step with the sprints it is made of, which defeats the point of the option existing.
- **`Number('pi')` is NaN**, so `derive`'s start-date line has to branch on it before the
  arithmetic — that branch is the whole feature and the only place the value is special.
- The option sits between *1 month* and *3 months* because the picker is ordered by SPAN, not by
  the unit each label happens to use.
- **A 12-week window drawn as weeks carries 13 bars**, essentially always: the ends fall mid-week
  and `bucketStart` rounds down. That is how every other window here behaves, and it is why the
  option's label and the window note use different units — the label is calendar, the note is
  buckets on the axis. Don't "fix" it by snapping this one window to bucket boundaries; the others
  would then disagree with it.
- It reaches All Teams for free, because `deriveTeams` passes the view straight through.

## Click a Dot, Copy Its Key (2026-08-21)

Asked for by Charles, and the natural end of what the issue key was stored for: the tooltip
names the item furthest up the column, and the next thing anybody does with that name is paste
it into Jira.

- **ONE handler shared by both scatters** (`onDotClick` / `onDotHover`, declared once and
  assigned by `dotsCopyKeys`), like `dotName` and for the same reason: the two charts are read
  as a pair, and a copy that worked on one and not the other is a bug nobody could describe.
  Declared at module level rather than built per render so the two carry the *identical*
  function — which is what lets a test assert it, and the cheapest guard there is on the pair
  drifting. Pinned, along with both charts actually carrying it: a renderer that forgot to
  attach the handler is a regression no pure test can see.
- **A dot with no key says so and copies nothing.** `dotName` falls back to the work type for a
  paste with no Key column — useful as a label, useless on a clipboard, and silently putting
  "Story" there would be worse than doing nothing. The no-key branch toasts synchronously,
  which is why it is the one the suite asserts on; the success branch awaits `copyText`.
- **The cursor is the whole affordance** — a canvas gives no other hint that anything under it
  can be pressed — so it turns to a pointer ONLY over a dot that will actually copy. The
  tooltip's last line says "Click to copy DAE-1234", and only when there is a key.
- **ONE copy line per tooltip, naming the dot the click will really take.** Reported by Charles
  the day this shipped: items that finished on the same day in the same number of days land on
  ONE pixel, Chart.js hands the hover to every one of them, and the tooltip drew six identical
  sentences each offering a different key — when a click can only ever take the first. The
  tooltip now keeps the first item only (`onlyTopDot`, installed by `dotsCopyKeys` so both
  scatters get it), which is the same element, in the same order, that `onDotClick` copies. How
  many are underneath is NOT dropped: `stackDots` writes a `stack` count onto every dot of both
  scatters in `derive`, and `dotTipFooter` says "6 items sit on this dot" above the copy line.
  Counted on exact x/y equality, which is the same test Chart.js applies to decide two dots are
  equally near the pointer — so the number stated is the number of items really under it. Do NOT
  put the copy line back on `afterLabel`: per-item is exactly what made it lie. The age chart
  spreads its dots, so nothing there ever stacks; it is stamped anyway so the shared tooltip
  never has to ask which chart it is on.
- **Reference lines cannot be hit**: `pointHitRadius: 0`, and their points carry no key anyway.
  `dotUnder` returns null for a dataset with no `data`, which is pinned.
- **Alive in a shared view**, on exactly the reasoning the table export buttons carry: it writes
  nothing and reads only what is already drawn on the recipient's screen.
- **Charts whose points are PERIODS must never get this.** There is nothing to put on a
  clipboard, and a pointer cursor over a bar would promise one. Pinned.
- **Keyboard and screen-reader users are not served by this and cannot be** — a canvas has no
  focusable points. The route to the same keys is the Loaded Data table, which every chart's
  `aria-label` already points at and which has its own Copy button. Say that in the README
  rather than pretending the chart is reachable; do NOT "fix" it by making the canvas focusable,
  which would put one tab stop in front of a hundred invisible dots.
- `copyText()` was already there for the table exports — clipboard API first, `execCommand`
  behind it, and an honest toast when both refuse. Nothing new was written for the copying
  itself.

## One Chart, Filling the Window (2026-08-21)

Asked for by Charles: a button on each chart to see it full screen, fitted to the window,
**"with the menu still visible"**. That last phrase decided the whole implementation and is the
thing to read before changing any of it.

- **It is NOT `requestFullscreen()` and NOT a modal `<dialog>`**, because both take the menu
  away: the Fullscreen API drops the browser's own chrome as well as the page's, and a modal
  dialog is promoted to the top layer, which paints over the sticky header and makes it inert.
  What is here is an ordinary fixed overlay (`#chartMaxi`) at **z-index 15 against the header's
  20**, starting at `--maxi-top` — the header's own measured height. Both numbers are pinned in
  tests.html, because the obvious "tidy-up" for this feature is to reach for one of the two APIs
  that would silently undo it. The header staying live is not decoration: changing team while a
  chart fills the window and watching it redraw is the thing the feature is for.
- **The CARD IS MOVED into the overlay, not copied.** `renderChart()` finds its canvas by id and
  a theme change destroys and rebuilds every chart in the app, so a second canvas up there would
  leave every redraw painting the copy left behind on the page — the maximised chart would go
  stale without anything looking wrong. A hidden `.chart-slot` holds the card's place in the grid
  so it goes back exactly where it came from, index and all. Pinned, including that the Chart.js
  instance is the same object afterwards.
- **The button hangs off the CARD, not off `.chart-name`.** That row's `innerHTML` is rewritten
  on every render (`setTitle`), so a button inside it would be destroyed and rebuilt on every
  keystroke that redraws a chart; both heading lines carry a matching `padding-right` instead. It
  is built once at boot for every `.chart-card` that contains a `.chart-wrap` — which is what
  keeps `#cardStageTime` out of it without naming it: a table has nothing a bigger box would show
  more of.
- **`syncMaxiButtons()` runs at the end of every render that can change what is drawable** —
  both exits of `renderDashboard()`, including the nothing-to-plot branch that destroys every
  chart, and both exits of `drawTrainThroughput()`. It does two jobs: take the button away from a
  card with no chart under it, and **bring the window down if the chart that was filling it has
  gone**. The header is live up there, so changing team is the ordinary way to reach that; without
  this the overlay would hold a destroyed canvas over a dashboard showing an empty state.
- **Nothing about it is stored.** Which chart is up is not in `view`, not in `state` and not in a
  share payload — no `SCHEMA` bump, no whitelist entry. It is a position on a screen for as long
  as you are looking at it, like a scroll position. It is **alive in a shared view** on the same
  reasoning the dot-copy handler is: it writes nothing and reads only what is already drawn.
- **Three ways out** — the same button (it toggles, and swaps to an arrows-in icon), Escape, and
  a click on the backdrop, which is the app's rule for every dialog. That last one is why the
  overlay keeps a 20px margin round the card rather than filling the window edge to edge: with no
  outside there is nothing for a click-outside to land on. Escape defers to an open `<dialog>` —
  the ⓘ pressed on a maximised chart is exactly that case — and that is pinned.
- **The ground is `--bg`, not a translucent scrim.** A dialog-style `rgba(0,0,0,.55)` over that
  20px margin left a ghosted band of the chart underneath showing through at the bottom edge,
  right where the eye goes to read an x axis.
- **`--maxi-top` is measured by a `ResizeObserver` on the header, not on window resize.** That
  row wraps to two or three lines on a phone, and it does so for reasons that are not a window
  resize — picking a team with a longer name is enough. The observer runs only while something is
  maximised.
- **`.shell` is marked `inert` while it is open**, so Tab runs round the header and the overlay
  and never wanders into the page underneath. The overlay and the dialogs live OUTSIDE `.shell`
  for that reason — anything inside would go inert with it. `role="dialog"` without
  `aria-modal`, because the header really is still live and `aria-modal="true"` would tell a
  screen reader the opposite.
- **The demo needed no new data**, and that is not a hole in the sample-data rule: the button is
  on every chart the demo already draws, and the one state worth seeing — a card with no chart
  under it and so no button — is Team Bare Export's lead time, which the demo already carries.

## The Cycle Time Scatter (2026-08-20)

One dot per finished item, beside the cycle time line — the same measure at two resolutions, and
they sit side by side so that is visible.

- **Built from the BUCKETS, not from `items`**, so the scatter and the line describe the same set
  by construction: an item completed outside the plotted window is in neither. Pinned against the
  throughput total.
- **`x` is a DAY INDEX from the first bucket, not a date.** Chart.js needs a time adapter for a
  date axis and this app vendors none. The ticks are forced back onto the bucket starts and
  labelled with the same words the line chart uses, so the two x axes read identically — which is
  what lets a reader match a spike on one to the dots that caused it. Same forced-tick trick as
  the work item age chart.
- **The x axis is padded 10% past the last day**, and that is not cosmetic. The age chart can pin
  its labels to the right-hand edge because its columns are ordered busiest-first and the last is
  reliably emptiest; a TIME axis offers no such corner, and the median line runs straight through
  the densest band of dots. The margin gives the label chips somewhere to sit that is not on top
  of the data.
- **One colour, and no shape for "slow".** The age chart marks items past the ageing THRESHOLD,
  which is a line the reader drew. There is no equivalent here: 15% of items sit above the 85th
  percentile by definition, not by failing, and colouring them would be the app judging a figure
  rather than stating it.
- **Fill is the accent at ALPHA, not a `tint()`.** That is the overplotting fix — `tint()` returns
  an opaque colour, so stacked dots would hide each other, where translucent ones darken. Jittering
  a date to separate them would be a lie about when something finished.
- **The two reference lines are the same two the age chart draws**, from the same pooled
  percentiles, in the same words, drawn by the same `refLabels` plugin. The ageing threshold is
  deliberately absent: it is a rule about work in progress, and nothing on this chart is.
  `ageMedian` / `ageP85` / `ageShort` were hoisted above both blocks so the two cannot drift — and
  because reading them from the age section below was a temporal-dead-zone error.
- Flow went to three charts, so **lead time took the `solo` class** — the odd card keeps a single
  column's width and sits centred. That class had been carried unused since Health went to four;
  this is the group its comment predicted.

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
- **Columns are workflow STAGE when the items in flight carry one, and work type otherwise.**
  The stage axis is the canonical version and landed 2026-08-21 — see the current stage section,
  which carries the reasoning for the switch, the ordering and the counts on the ticks. The work
  type axis is not legacy: it is what a board with no status column still gets, and it is what
  the whole ranking-and-folding machinery below was written for. `AGE_UNTYPED` and `AGE_OTHER` are pushed to the right-hand end
  regardless of count — neither is a work type, and keeping both there is what preserves the quiet
  corner above. `AGE_MAX_COLUMNS` counts REAL types only, so an untyped item can never push a real
  one off the chart.
- **Dot positions are computed in `derive()`, not improvised by the renderer**, so the spread is a
  pinned property of the data. Sorted by age within a column, spread across `±AGE_SPREAD`, and a
  column of one sits dead centre on its own tick.
- **A dot is named by `dotName()`** — its issue key where the paste had one, and its work type
  and start date where it didn't. This line read "no ticket key and never will" until the key
  arrived (2026-08-20) and reversed it: naming the dots is the reason the field was asked for.
  What did NOT change is the rule underneath it. A key is the ONE identifier this app stores,
  and no future change may put any other identifying text on the chart — the storage rule at
  the top of this file is why. The fallback is not a stopgap either: work type plus start date
  is what finds the item again in an export with no key column.
- Aged dots are told apart by SHAPE as well as colour (a `--serious` triangle against accent
  circles), the same rule the defect and cycle time charts follow, and the same non-RAG pair.
  Nothing is coloured "bad": the threshold is one the reader set.
- Health went from three charts to four, so the defect rate card lost its `solo` class. The class
  and its CSS stay — the next odd group would otherwise rediscover the problem.

## The Monte Carlo Forecast (2026-08-20)

The fourth section of the Dashboard tab, and the only one that looks forward. It resamples this team's own
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
  forecast is a position on this device, like `activeTeamId`. That keeps them out of the stored
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
- **The base field rule's TYPE LIST is the theme pack's own** (2026-08-22). `select,
  textarea, input[type=text|number|date|month|search|tel|url|email|password]` — the same
  list the pack enumerates in its coarse-pointer rule. It has to stay a whitelist (a
  checkbox handed a surface, a border and padding stops being a checkbox), but a whitelist
  grown by hand is a field that arrives silently UNSTYLED, wearing the browser's own box
  beside fields wearing the theme's. Nothing fails and nothing logs. It has happened twice
  in this family in opposite directions: this app was missing `date`, Golf Handicap was
  missing `search`. Borrowing the pack's list is what stops it being a fresh discovery each
  time, since it answers the same question ("is this a thing you type into?") in the one
  place that should. **Adding a type to one means adding it to the other.**
  `input[type=search]` also takes `appearance: none`, like the pack's date fields, because
  the native inset shape ignores the border and radius — that removes Chromium's native ×
  too, so a search box with no other way to clear itself should offer one.
  **Sprint Predictability is the design lead**; Money Map and Golf Handicap carry the
  identical list. PAPTrack and the dashboard style fields by CONTAINER (`.field input`) and
  by class (`.ctl`) instead — element selectors, which have no equivalent gap — and the
  lottery pages style their few fields per component. Those three are deliberately NOT
  converted; don't "finish the job" by giving them a type list.
  The date case is this app's own instance of it: adding the forecast's target date meant
  adding `input[type="date"]` to this rule, because without it the box kept the UA's 2px
  border and zero padding and sat 10px shorter than the number box beside it. **Not theme
  drift**: the pack owns the two date-specific rules (the 16px touch floor and turning the
  native appearance off), the control's box is each app's own.

## Security (shared origin)

- All of `eagleadams86.github.io` is ONE browser origin: any page on any of the
  account's Pages sites can touch this app's localStorage. So: **no third-party
  scripts ever** (`chart.min.js` is vendored — don't hand-edit it), and a CSP on
  every page.
- **This app's CSP now names NO external origin at all** (2026-08-20, with sync).
  `default-src 'none'` is the real rule rather than a formality, and
  `connect-src 'none'` is spelled out rather than left to the default because it
  is the directive that would carry work data off the device. Adding any origin
  here is a decision about where Jira figures may go — ask whether it is needed
  at all first, and expect `tests.html` to fail until the pin is changed
  deliberately.

## Sync Was REMOVED (2026-08-20) — Don't Put It Back Without Asking

Google sign-in + one Firestore doc per user (project `teamdashboard-6723f`) was removed at
Charles's request, in the same PR that let the app store issue keys. The two go together: the
app now holds identifiers out of a work system, and the answer to "where does that live" is
"one browser, and nowhere else".

- **It was removed, not disabled.** The module, `#syncBtn`, the which-copy dialog,
  `firestore.rules`, `hasData()`, `cloudPush`/`cloudFlush`/`tdSignedIn` and every Google
  address in the CSP went together. Setting a config to `null` would have left the code, the
  origins and the CSP in place — which is not the same claim.
- **The pins are in `tests.html`, group "sync is gone — and cannot come back by accident".**
  A CSP naming no host, `connect-src 'none'`, no module script, no `import(`, a word-list
  tripwire over the app's *code* (comments are stripped, because the removal note deliberately
  names Firebase so a grep lands somewhere useful), and a live boot proving the leftover keys
  are deleted. If you are reinstating sync, those tests are the specification of what you are
  undoing — change them deliberately, in the same commit.
- **`clearSyncLeftovers()` deletes `td-sync-uid` and `td-updated` on every load.**
  `td-sync-uid` is a Google account id, the only personally identifying thing this app ever
  wrote down; leaving it after removing the feature would be keeping an identifier for nothing.
- **`tdAdopt()` survives sync** — restore-from-backup is its caller now, plus the test
  harness's `plant()`. Two things changed with it: it no longer stores a newer document
  verbatim before halting (that made sense only when the incoming copy was genuinely the
  newest in existence), and its "you are about to lose your created dates / issue keys" prompt
  is worded for a FILE rather than for another device. The restore handler now honours its
  `false` return — before, a declined adopt still toasted "Backup restored".
- **What was lost with it, and would have to be rebuilt**: the Google Identity Services
  workaround for corporate networks that block `<project>.firebaseapp.com` **per hostname**
  (measured, real, and not something a fresh implementation would think of), the
  never-guess-by-timestamp reconciliation, the empty-copy-never-wins rule, and the
  `serverAt` server-clock ordering. It is all in one commit in `git log`.
- **The Firestore data was deleted too, 2026-08-20**, by hand in the console — removing a
  client deletes nothing server-side, so this was a separate deliberate step. The
  `teamdashboard` collection is empty, and `privacy.html` states that rather than promising
  deletion on request.
- **Charles's account was the ONLY one that ever signed in**, confirmed from the Firebase
  Authentication list on 2026-08-20. So no third party's data was ever in that database, and
  the deletion cost nobody anything — which is why `privacy.html` no longer carries a
  deletion-request route: it would be offering a service to an empty set. Worth knowing
  before reading the older docs, which talked about fellow Scrum Masters signing in; they
  could have, and never did.
- The project `teamdashboard-6723f` and Charles's own Auth row still exist. Deleting the
  project outright is a further step nobody has taken; it would also kill the API key
  GitHub's secret scanner flags on this repo.

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
    prefix, or it wipes a sibling's. (The SHELL list also carries the manifest
    and the four install icons since 2026-08-22 — still all public files in this
    repo, which is the rule.)
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
  `worker-src → child-src → script-src` fallback chain — which, when this was
  written, would have inherited script-src's gstatic and accounts.google.com
  hosts. Those went with sync (2026-08-20); the directive stays spelled out so
  no origin ever added to script-src can reach the worker by fallback.
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
- **tests.html busts its own cache, on the frames AND on the source fetches
  (2026-08-22), and that is not tidiness.** `const BUST = '?t=' + Date.now()` goes
  on every hidden `iframe.src` (six when this was written, twelve now) and through `bustFetch()` on every read of a
  file this repo ships. The frame cache and the HTTP cache are different caches
  and they can disagree: in the lottery repo the same harness reported
  **all-green against a page three features out of date**, because the
  source-level tests were reading the file off the server while the frames ran a
  copy the browser had cached. Nothing errored; the new code was simply never
  run. A suite that can pass against a build which exists nowhere is worse than
  no suite — it turns "untested" into "verified". **If a test passes when you
  expected it to fail, check the frame's `contentWindow` has the function you
  just wrote before believing anything.** The `api.github.com` call is
  deliberately left un-busted: somebody else's endpoint, not a file we ship.
- **A second consecutive local run of the suite fails three date tests, and it is
  the harness, not the app (found 2026-08-22, NOT yet fixed).** The suite plants
  data and leaves `td-view` behind, so the next run boots the app with a
  `customFrom` already saved — and the three "the date strip is prefilled with
  the ends of the data" tests then see the restored window instead of the
  default one. CI never sees it because it starts from a clean profile.
  `localStorage.removeItem('td-view')` before a run, or expect three red rows
  that mean nothing. Same family as the ambient-state trap in Money Map.
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
  `color-scheme` per theme and `--chrome-h`. **There were per-theme `--shadow`
  values too, and they went on 2026-08-23** with every other elevation shadow in
  the family — four apps had invented one, none of them a pack token, for
  something nobody could see once a modal backdrop sat over it. Pack hard rule 14,
  enforced by its `check_consumers.py`. The `box-shadow: inset` on the
  current-row marker is not a shadow and stays: it is a border drawn where a real
  `border` would move the cell.
- **THE SAMPLE DATA IS THE DEMO, and a feature isn't finished until it reaches
  it.** `loadSample()` (section 9c) is what someone sent a share link explores and
  what the app is shown with, so every feature must be visible from it. Adding one
  means adding the data that demonstrates it, a line in the roster comment above
  `loadSample()`, a row in the README's demo table, and an assertion in the demo
  group of tests.html — that group exists because these are ordinary-looking
  figures a later edit would tidy without noticing. The same rule runs in Sprint
  Velocity; it was added to both on 2026-08-19 after Charles loaded a sample and
  couldn't find the feature it was meant to show.
  - **Each demo team is NAMED FOR THE ONE THING IT SHOWS** — Team Healthy Flow,
    Team Long Tail, Team Bare Export — so the picker reads as a contents page and
    a reader who lands on a board already knows which finding it is meant to
    teach. Sprint Velocity's demo is named the same way. A new demo team gets a
    name of the same kind; renaming one back to a bird or a place would leave the
    demo teaching nothing until you had read all of its numbers.
  - Every figure in `DEMO_TEAMS` is load-bearing: **Team Long Tail's tail is the
    app's central argument** (p85 ≈ 23 days against a median of 5 — tidy that away
    and nothing on screen justifies reading p85 rather than the average); Team
    Bare Export has **no created dates**, which is the only way the lead-time
    chart's own
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

## Fields, Dialogs and Scroll Boxes (2026-08-20, layout rule added 2026-08-22)

### No Field In a ROW Is Ever Two Lines Tall — `.forecast-ask` (2026-08-25)

The same complaint as the dialog rule below, arriving in a horizontal strip instead. Reported by
Charles the day the +12 weeks preset shipped: the button was put UNDER the date box, so that one
cell was **96px against its neighbours' 64px** — and the row is aligned on its bottom edge, so its
label and its box sat **32px above** the three beside them.

- **THE RULE: a field in one of these rows is ONE label line and ONE control line.** A control
  that needs a second button puts it BESIDE the box (`.fc-date-row`), never under it. If a setting
  needs more than that, it does not belong in the row — which is exactly the dialogs' rule, said
  about a strip.
- **The row is FLEX, not `auto-fit` grid, and the grid version had a second fault nobody had
  noticed.** `repeat(auto-fit, minmax(180px, 1fr))` makes as many equal columns as FIT, not as many
  as there are fields: at 1233px that is six columns of 192px for four fields — four narrow boxes
  and two columns of dead space at the right-hand end. `flex: 1 1 <basis>` shares the whole line
  between however many fields are on it. The one field carrying a second control asks for a bigger
  basis (`#fcDateField`, 320px) so both fit, and `min-width: 0` on the input is what keeps them on
  one line — without it the date box refuses to shrink and the button wraps underneath, which is
  the exact fault this exists to prevent.
- **A DATE BOX IS 2px TALLER THAN EVERY OTHER CONTROL, and that was pre-existing and app-wide.**
  The shared field rule gives every control `min-height: calc(1.5em + 16px)` — 40px — and a select
  and a number box land there; Chrome's date editor has a 26px inner content box rather than 24px,
  so `input[type=date]` renders 42. In a bottom-aligned row that pushes its label 2px out of line.
  The main control strip had it too, on the custom From/To boxes. Fixed with `height` **scoped to
  the two side-by-side rows** — the shared `min-height` carries an iOS guard that cannot be tested
  from here (an empty date box collapses to its padding because the pack turns the native
  appearance off), and pinning the height satisfies that guard exactly rather than replacing it.
  The item dialog's date fields are left alone: each is alone in its own grid cell. **The control's
  box is this app's own** — the pack owns only the appearance and the 16px touch floor — so this is
  not theme drift.
- **The sweep is the guard.** `tests.html` walks the row at nine widths, groups the fields by the
  line they landed on, and fails on any group whose labels, controls or heights disagree — plus a
  direct check that the button is beside the box and that the date box matches the number box
  **as a comparison rather than at 40px**, so the day the field height changes the test moves with
  it. It counts what it reached and refuses a sweep that found nothing, the trap this suite has
  been caught by before. **Proven to fail before it was committed**: making `.fc-date-row` a block
  again turns 18 checks red and names the fault.
- **The ambient-state trap caught me on the way through.** Measuring the layout by hand left
  `months: 'custom'` in `td-view`, and the next suite run threw at check 669 on an undefined CFD
  chart — a custom window with no dates leaves nothing plottable. It reads as a code failure and is
  not. `localStorage.removeItem('td-view')` before a local run, as the Working Rules say.

### No Field Is Ever Stranded on a Short Row — `.grid.two.pairs`

Charles has reported dead space in a dialog more times than anything else, across two apps
(`[[no-orphaned-form-fields]]` in memory records three reports in one day on Money Map, the third
caused by the fix for the second). On 2026-08-22 it arrived here twice in one change: a long hint
inflated its grid row and left a void beside the two fields next to it, and an odd number of
workflow stages left the last day-count box alone in half a fieldset.

**Fix it in the layout. A field-by-field fix has never once held** — the next innocent addition
strands a different field, and whoever adds it has no reason to know there was ever a rule.

- **`.grid.two` is `auto-fit`, which does NOT solve this.** It collapses a track only when the
  whole grid has nothing to put in it — that saves the one-field grid (the multi-team paste's date
  picker) and does nothing for *n* fields into a column count that does not divide *n*.
- **`.grid.two.pairs` fixes the count at two, which is what makes the arithmetic decidable in CSS
  alone**: `> :last-child:nth-child(odd) { grid-column: 1 / -1 }`. An odd number of fields means
  the last one starts a row by itself, so it spans. No opt-in flag, no JS measuring pass, nothing
  for the next person to remember. Two columns is also right on its own merits where the labels are
  sentences — a sentence in a 260px auto-fit track wraps to three lines.
- **IF A SETTING NEEDS MORE THAN A LABEL, IT GOES OUTSIDE THE GRID.** A multi-line hint inside a
  bottom-aligned grid cell inflates its whole row; that is what happened to the ageing threshold.
  It now sits under the grid, paired two-up with its own explanation — which also avoids the
  opposite fault of a box for a two-digit number stretched across 1100px. The working-days
  checkbox has always followed this rule; it is now the general one.
- **The regression test walks every `.grid.two` in every dialog at seven widths** and fails on any
  row whose last cell stops short of the grid's right edge. Two things about it matter:
  - **Rows are found by LEFT resetting, never by grouping on `top`.** The grid is
    `align-items: end`, so two cells on one row routinely have different tops — grouping by top
    splits a full row into two short ones and reports failures where the layout is fine. This cost
    a false alarm while it was being written.
  - **It counts the grids it reached and asserts it saw at least five**, because a sweep that found
    nothing passes every "no bad rows" assertion it makes — the trap `[[negative-assertions-pass-on-empty]]`
    records. The fixture plants an ODD number of stages for the same reason: an even count passes
    without the span rule doing anything.
  - Proven to fail with the rule removed before being committed, rather than assumed to work.


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
- **`package.json` is a Dependabot manifest, not a build step.** It installs nothing, declares nothing but the vendored `chart.min.js`, is `private: true` with no scripts, and CI passes `--omit=dev` so npm never downloads it. **Dependabot cannot re-vendor a file**, so a version-bump PR would raise the manifest while the app kept serving the old bytes — `tests.html` pins the manifest's pin to the version string inside the bundle, which makes a manifest-only bump fail and turns the PR into the right instruction: update the file too, in all four repos that carry it (lottery, team-dashboard, financial-plan, sprint-velocity). Never add a `scripts` block, and never let the pin become a `^` range — a range cannot be checked against a file.

## The Privacy Page Carries the Family Footer (2026-08-21)

Every public page in this account carries the same three things at the foot: the privacy
policy, the repo under the label **How it works**, and the authorship line. The APP's footer
has had all three for a while. `privacy.html` had **none** of them until now — and it is a
public page reached by a link in that very footer, so anybody who followed it landed on a
document with no way back to the thing it documents and no statement of who wrote it. The
lottery site's privacy page had grown the footer first and was the only one; the other four
were brought into line together rather than one at a time, because a convention held by one
page out of five is not a convention.

- **No privacy link in it**, unlike the app's own footer — you are standing on that page. That
  absence is asserted, not just omitted: the test checks there is no `href="privacy.html"`.
- **The authorship line is the app's own, verbatim**, which means the two-link form here: *independent personal project* points at **NOTICE**
  (who owns it) and *MIT licensed* points at **LICENSE** (the terms). Getting those two the
  wrong way round is the mistake the app's own footer comment records.
- `.foot` and `.foot a` are copied from the lottery page's stylesheet unchanged, so all five
  read identically. Muted, inheriting the link colour — provenance at the foot of a document
  rather than something to click on the way in.
- **Pinned in `tests.html`**, so the next page added to this repo cannot quietly ship without
  it.
- **It is a real `<footer>`, and the policy is in a real `<main>`** (2026-08-21, a day after
  the footer itself). A styled `<p>` is not a landmark, and a page whose only landmark is
  contentinfo is worse than one with none — the actual policy would sit in no landmark at all.
  So both went in together.
  - **`</main>` closes BEFORE the `<footer>`, and that ordering is the whole thing.** A
    `<footer>` nested inside `main`, `article` or `section` is **not** contentinfo — it is a
    plain footer for that section. So `.wrap` stays an ordinary `<div>` rather than becoming
    the `<main>`, which would have swallowed the footer and left the page with no contentinfo
    at all while looking correct in the source. A test asserts the ORDER, not just the tags.
  - The back link stays outside `<main>` — it is navigation, not the document.
  - **The tests strip HTML comments and match the footer by its class**, because the notes
    beside both elements name them in prose and one of those notes lives in the `<style>`
    block, which an HTML-comment strip does not reach. Without both, a page that had lost the
    element and kept the comment explaining it would still pass. That is not hypothetical —
    it is how the first version of this test failed.
  - **The strip is a LOOP, not a single `.replace()`** (2026-08-21, `stripHtmlComments`).
    One pass over a multi-character delimiter can leave a NEW opener behind that the pass has
    already gone past, so a single pass is only as good as the input is well-formed — CodeQL's
    `js/incomplete-multi-character-sanitization` flagged exactly this line, and it was open on
    five of the nine public repos at once. Nothing here renders what it strips, so there was
    no vulnerability; the reason to fix it is that a helper that can be fooled about what is
    commented out is one that can miss a live off-origin script, which is what these suites
    exist to catch. Same helper, same wording, in every sibling repo's suite.
  - `.foot` sets `margin`, not `margin-top`, so the rule no longer depends on which element
    carries it: a `<p>` brought a UA bottom margin with it and a `<footer>` does not.

- **`<main>` opens ABOVE the tab strip (2026-08-21), not around the panel alone.** Two things
  were wrong with the old placement: the tabs were in no landmark (axe-core's `region` rule),
  and the skip link jumped straight past them — a keyboard user who took "Skip to content"
  had the whole tab row behind them and could only reach it by shift-tabbing back. The tabs
  and the panel they drive are one widget, so the landmark goes round both, and `#shareBar`
  comes inside with them because it describes what is on screen. `role="tabpanel"` still goes
  on the inner div and NEVER on `<main>`: putting a role on an element is its role, and it
  would silently replace the landmark. Every page here now passes axe-core at WCAG 2.1 A/AA
  plus best-practice, in all four themes, with data loaded, on every tab and with every
  header dialog open.

- **The privacy page's back link lives in a `<nav>` (2026-08-21).** It stays OUTSIDE `<main>`
  — it is navigation, not the document — but "outside main" is not the same as "outside every
  landmark", which is where it sat: axe-core's `region` rule found it on all six privacy pages
  at once. The `<nav>` carries an `aria-label` naming where it goes back to.
- **Decorative glyphs on buttons are `aria-hidden` everywhere, not just in the header.** The
  header row got the treatment on 2026-08-21 and the rest of the app did not, so a screen
  reader still read "downwards black arrow, Export JSON" in every dialog. Around 50 buttons
  across the family were wrapped in the same pass. The sync button was the exception that
  proved it: its label was rewritten with `textContent` as the state changed, so a span there
  would have been blown away — it carried an `aria-label` re-stated in every branch of
  `updateUI()` instead. Both went with sync's removal (2026-08-20); the pattern is recorded
  here for the next state-changing button.

## Six Fixes From the 2026-09-01 Audit

A bug audit of the three work apps on 2026-09-01 (three auditors, each finding
reproduced headless before it was reported) found six in Flow Metrics that the
suite did not cover. Each has a test now, proven to fail first by reverting the fix.

- **hydrateState keeps every status that passed the door (fix 1).** The `liveStatuses` prune dropped any status no row, feature or stage pointed at, and
  `loadState` wrote the pruned copy straight back. Written when the only door into the vocabulary
  was a row that loaded, so an unreferenced status could only be a leftover. `164b437` (a status
  off a row dropped as undated — no row is stored, so nothing CAN point at it) and `62cfb93` (a
  status off an empty `Days in …` heading — a status nobody is in) both produce exactly that, and
  the report named words that were gone by the next reload. The list is bounded by `STATUS_MAX`
  at the door and delete-all takes it; a dangling POINTER is still pruned, which is a different
  thing. The test that pinned the old rule was rewritten, not deleted.

- **The work item age chart is read as of `endDate` (fix 2).** `inFlight` in derive() filtered `r.started && !r.completed` — open TODAY — while `endDate` had
  already been clamped to a typed window's `to` and the chart's title named that date. Under a
  January window an item finished in March was missing and one started in February was drawn at
  age zero; `summary.agedNow` (read correctly, off `wip`) said one aged item and
  `ageing.agedCount` said none. In flight on a date is `started <= endDate && (!completed ||
  completed > endDate)`. `items` is not window-filtered, so the fix is the filter alone.

- **A bare integer is not evidence of a date column (fix 3).** `columnStats` counted every cell `parseDate` accepted, and `parseDate` reads a 4–6 digit
  integer as a spreadsheet serial, so a column of five-digit Jira ids had `dateRate` 1.0 and the
  free-date ranking took `Issue id` as the completion date whenever the export had no Resolved
  column. `dateRate` now excludes `SERIAL_ONLY` cells and `serialRate` counts them apart;
  `datey` (the heading-matched roles' content check) accepts either, so a *Resolved* column of
  serials still lands. A column found by content alone must hold something that could only be a
  date.

- **Find walks both lists and the hit says which (fix 4).** `searchApp` walked `t.rows` only — the SIXTH rows-only walker, see the two-lists note — so a
  feature could not be found, and `goToSearchHit` handed the index to `openItemDialog`, which
  reads whichever list `featureUnit()` says: an item found with the switch on Features opened the
  feature at the same index, with Save ready to overwrite it. A hit now carries `unit`
  ('items'|'features'), goToSearchHit sets `view.unit` from it before `renderAll()`, and a
  feature's snippet leads with "feature". The question to keep asking near a team: would this be
  wrong if half the data were in `features`?

- **The paste is cut into records, not lines (fix 5).** `parsePastedRows` split on `\r?\n` before any quote handling, so a quoted cell holding a
  newline — Excel writes a multi-line Description exactly so, in both CSV and tab form — cut the
  row in two: the tail became a row of its own and every column after the break moved one cell
  left, so the key was lost and the start date was read as the completion date, silently.
  `splitRecords(text)` scans with splitCsvLine's own rule (a quote opens a cell only at the start
  of one; `""` is a literal; a newline inside an open cell continues the record) and returns each
  record with the PHYSICAL line it starts on, which `lineNo` now reads from `lineOf` — the report
  points at the export, and a record above may span lines. **A quote that never closes is not a
  quote**: if the scan ends inside a cell the paste is cut on plain newlines, exactly as before,
  so one stray `"` in a hand-typed paste cannot swallow everything after it.

- **The week holding 1 January is week 1 of the NEW year (fix 6).** `weekNumber` counted from the Sunday on or before Jan 1 of the year of the day it was handed,
  and `weekKey` read the year off that day too — and every caller hands the week's Sunday, so the
  straddling week was `2025-53` and the next `2026-02`: week 01 never appeared, and the same week
  had two keys depending on which day asked (`weekKey(1 Jan)` already said `2026-01`). Both now
  read the year off the week's SATURDAY, so a key is a pure function of the week. The pinned
  `'2024-53'` in two tests became `'2025-01'`; the fortnight key beside it (`'2024-52'`, a week
  that does not straddle) did not move. Keys are computed, never stored, so nothing migrates.

## Fixes From the 2026-09-03 Audit

A second bug audit of the three work apps on 2026-09-03 (again three auditors, each finding
reproduced headless before it was reported) — this time aimed at the day-old full-screen
stepping, the pin and the phone tab row, and then a general pass. Each fix has a test, proven
red against the unfixed page before the fix went in; the commit quotes the red row.

- **A key step in full screen lands the focus on the new card's ⤢ (fix 1, family-wide).** `openMaxi()` puts the
  keyboard on the card's own ⤢, and `maxiStep()` carried that card — button and all — back
  into the inert page under the overlay, so the browser dropped the focus on `<body>`: the next
  arrow still worked (the handler listens on the document) but Tab started again from the top of
  the page. The rule, in one sentence: *a step lands focus on the arrow that pressed it, or on the
  new card's ⤢, never on the page underneath.* The overlay's own arrows never move, so a step
  BUTTON that has the keyboard keeps it (the suite already asserted that); only a focus that is
  gone, or outside `#chartMaxi`, is moved — with `preventScroll`, because the page under the
  overlay must not be dragged about. The same shape went into Sprint Predictability and Money Map
  the same day. The Money Map sentence in "Stepping Between Charts in Full Screen" above was about
  its buttons, and now says so.

- **The phone tab scroller leaves the focus ring room on every side (fix 2, family-wide).** `overflow-x: auto`
  makes `.tabs` a scrollport on BOTH axes, and a scrollport clips at its padding edge — so the
  ring (2px, offset 2px: 4px outside the tab) lost its top and the outer edges of the first and
  last tabs; only the bottom had its 4px of padding. Now `padding: 4px` with `margin: -4px -4px 0`
  — the room is given and then given straight back to the layout, so the tabs, the row's height
  (which `measurePinTop()` reads for `--pin-clear`) and the page's height are all what they were.
  Proved by measuring at 375 and 1280, pinned and unpinned, before and after: only the `.tabs`
  box itself changed. The bottom margin stays 0 because that 4px was already in the row. Money
  Map's `.yearrail` had this pattern first. Four checks in the pin group measure it rather than
  grepping for it.

- **The tile names the fold by its heading, and the cards name the same route (fix 3).** With the typed-pace tick
  defaulted on and its boxes empty — sample data, Team Long Tail, a three-month window grouped
  by fortnight — the tiles said *waiting for a pace below* while "Adjust for what you know" sat
  SHUT, and the chart cards under them said *group by a shorter period, or widen the date
  window*: two remedies for one state, and the tile's pointed at nothing on screen. The tile now
  reads *waiting for a pace under "Adjust for what you know" below* — the heading is visible
  whichever way the fold is, so the sentence is true either way, which is why it does not say
  "folded": the fold is pressed without a render and a tile claiming it was shut would go stale
  on the press. `waitingForPace` is one boolean shared with `excuse()`, which appends the same
  route to the few-periods, stale-team and no-throughput sentences; on a plan, which has no
  window to widen, the card names the typed pace alone (it used to offer to widen a window over
  no data at all). The fold is never opened FOR the reader. The README paragraph that said the
  tick "arrives checked so the boxes are open" now says enabled, not shown.

- **A Find hit that leaves the view brings a maximised chart down first (fix 4).** ⌘K opens over a
  maximised chart on purpose — Find is a window like the help window, and a chart is not a
  `dialog[open]` — but `goToSearchHit` did `renderAll()` + `selectTab()` under the overlay and
  never `closeMaxi()`: the item editor opened over the full-screen chart, and two Escapes later
  the chart came down onto Your Data with its ⤢ — the button `closeMaxi` hands the keyboard to —
  in a hidden panel, so the focus fell to `<body>`. Now a hit whose view is not `activeTab`
  closes the chart BEFORE the render, the way `beforePrint()` does; a team hit on the same view
  leaves it up (the header's picker by another route, and the picker stays live up here on
  purpose), and a stage hit is a dialog over it like the help window. After `selectTab`, a focus
  that is on nothing the reader can see — `<body>`, or an element with no client rects — goes
  onto the hit's own tab, so the editor has something real to return to when it closes.

- **The delete-all sentence is one list, in English (fix 5).** `plural(n, 'status')` said *7
  statuss*, and the extras were joined with `' and '` between every pair — *along with 1 ART and
  4 workflow stages and 7 statuss*. The README had been promising *1 ART, 4 workflow stages and 7
  statuses* all along. That dialog's local `plural` now takes an optional spelt-out plural (none
  of the other four `plural`s in the file does; each is one line and local, and this stays local
  for the same reason), and the list is commas between with *and* before the last. No list helper
  exists in the file to share — every other `join(', ')` is a plain comma list. Three checks in
  "the delete-all sentence lists what goes, in English".

### Round Two, 2026-09-04

The leftovers of the same audit that Charles chose to fix the next day. Same routine: a test
first, red against the unfixed page, and the commit quotes the row.

- **A team is stale when it is a whole period behind, not a day (fix 6).** `staleTeams` in
  `deriveTeams` listed every team with `dataEnd < endDate`, and the sample data has one a single
  day behind (Team Long Tail ends the day before Team Healthy Flow) — so the Delivery ART
  forecast, and the feature forecast across all three teams, told the reader to re-export a team
  the forecast had lost nothing from. Lost nothing because the samples are WHOLE periods: a gap
  shorter than one falls inside the part-period they never count. The rule is now the
  forecast's own — `periods >= 1` — and `coverageEnd` is cut from the same list (null when no
  team is stale), so the two cannot disagree; the earliest end is always a stale team's end
  whenever there is one, so nothing that was ever trimmed trims differently now. The All Teams
  "Data to" column is untouched: it reports the date, which is still true. Four checks in the
  pure stale group and five on the sample data, through the scope picker's own change event.

- **A typed item key that is not a key is refused, not dropped (fix 7).** `buildManualRow` put
  the Item box through `cleanIssueKey`, which returns `''` for anything not the shape of a Jira
  key — so `bad key here` saved a row with no key and no word about it, while the same box on a
  FEATURE was refused out loud. The form now refuses a non-empty key that fails `ISSUE_KEY_RE`,
  in the feature sentence's voice (*"That isn't the shape of a Jira key — DAE-1552. Leave it
  blank or fix it."*); a blank key is still allowed, the field is optional, and `hrn-12` still
  lands as `HRN-12`. The paste path is untouched — it drops the cell and reports the line, which
  is the right rule for hundreds of rows arriving unwatched. The one pure check that pinned the
  old drop was rewritten, not deleted. The parent-key box still drops silently; it was not in the
  finding and is left for a decision of its own.
