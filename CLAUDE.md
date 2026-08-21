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

## Only Numbers, Dates and Two Guarded Labels Are Ever Saved (2026-08-12/13, amended 2026-08-20/21)

- **A row is three ISO dates, one short work-type label, one issue key and a
  set of NUMBERS keyed by stage id.
  Nothing else. There are no free-text or comment fields anywhere in this app —
  don't add one.** A team carries a name, an optional `artId` and an optional
  project id — the last added 2026-08-20 and guarded by the same shape as the
  front of a key. See the project id section below. `state.stages` carries names
  and aliases the reader typed; **nothing on a row is ever a word** — see the
  workflow stages section, which is the longest one in this file for a reason.
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
  What got in was a stage the reader names in a dialog and a number of days. If
  that distinction is not clear, read the workflow stages section before
  touching anything near it.
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
- Settings labels, team names, ART names and stage names are short and capped
  (120); rows carry **one identifier and no other** — the issue key,
  shape-checked — and no titles, summaries, statuses or names of people.
  `privacy.html` promises exactly that, keep it true and update its effective
  date in the same commit as any storage change (it went to 2026-08-20 with the
  key and to 2026-08-21 with stages).

## Workflow Stages (2026-08-21) — SCHEMA 7 → 8

`state.stages` is a list of `{id, name, match[]}` and each row carries an optional `stages`
object of day counts keyed by stage id (`g` on the wire). It is what blocked time, flow
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
- **That is why matching is by ALIASES YOU TYPE and there is no "adopt this heading" button.**
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
  by an alias that already exists. Kingfisher spends most of its time building, **Heron spends
  more of its time queueing than building** — the finding the whole feature exists to produce,
  and the reason the demo lands on Heron — and Wagtail carries none, so the card's empty face is
  reachable. Review is fed by two of Heron's columns. The demo's split is **deterministic and
  never drawn from `rnd()`**, exactly like the issue key counter: a draw consumed here would
  silently move Heron's tail and Kingfisher's aged count. It is written in **tenths of a day**,
  because whole days on a four-day board report that every item spent zero time in review.
- What this unblocks and what it does not: blocked time and flow efficiency now have their
  export, but both still need a per-stage **waiting or working** flag, which is a decision about
  meaning rather than a parse. Neither is built. The work item age chart's stage axis WAS
  built — off the current stage rather than off these durations; see the section above it.

## The Current Stage (2026-08-21) — SCHEMA 8 → 9

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
  type when no item in flight carries a stage, so a team like Wagtail is unchanged.
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
- **The demo's Heron carries one status no stage lists** — "Compliance Review", straight off
  Charles's own workflow — holding its second-oldest item, so the "No stage" column and the
  unmatched-status note are both reachable AND both worth acting on. Its in-flight statuses are
  matched POSITIONALLY to the `wip` ages, so three of the four oldest sit in Test and the
  bottleneck is a column you can point at. `statusOf` never draws from `rnd()`, like every other
  demo field added since the issue key.

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
- The demo's two keyed teams carry the ids their keys are built from and Wagtail carries none,
  so both faces are reachable from Load sample data — and the demo is itself a multi-team export
  that splits back into the teams it came from, which a test pins.
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
- **Two demo teams carry keys and Wagtail deliberately carries none**, so both faces are
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
  "Team Kingfisher" to "Team Ki" on a phone; the row simply outgrows the dialog and
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
  under it and so no button — is Wagtail's lead time, which the demo already carries.

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
- Adding the target date meant adding `input[type="date"]` to the app's own base input rule —
  without it the box kept the UA's 2px border and zero padding and sat 10px shorter than the
  number box beside it. Golf Handicap's rule already listed it. **Not theme drift**: the pack
  owns the two date-specific rules (the 16px touch floor and turning the native appearance off),
  the control's box is each app's own.

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
