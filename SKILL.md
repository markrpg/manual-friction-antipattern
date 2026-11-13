---
name: manual-friction
description: >
  Prevents and measures manual friction: work a person does that the product
  already had enough information to do itself. Catches signed-in accounts set
  up again per project, restart-to-apply, detours to Settings from the flow
  that needs them, generic errors, greyed-out buttons with no reason, buttons
  that do nothing, pickers with one option, confirmations on undoable actions,
  Refresh/Check buttons, internal IDs in UI text and lost drafts. Use before
  designing or building any user-facing flow, screen, onboarding, settings
  page, form, error state or approval prompt; when reviewing a design,
  screenshot or UI diff; and when verifying a UI change in the running app.
  Also use whenever someone describes a flow as clunky, fiddly, long-winded,
  confusing, heavy, a slog, too many clicks, too many steps, too much
  hand-holding, babysitting, busywork, setup fatigue, "this should just work",
  or asks for a UX review, an audit of a flow, an onboarding pass, or a
  settings page. Also use when the user says "manual friction", "friction
  score", "score this journey", "friction audit", "antidesign" or invokes
  /manual-friction.
---

# Manual Friction

Manual friction is work a person does that the product already had enough information to do itself: a click, a choice, typing, a trip somewhere else to find something, a restart, or working out what went wrong. "Enough information" is what the product knew at that moment: accounts already signed in, folders already chosen, settings already made, the only option available, the cause of its own error.

Generated interfaces collect it by default. Training data is mostly dashboards, settings pages with every toggle visible, wizards and up-front forms, built for software that only did what it was told. Instructions alone don't hold against that prior, so this skill has two halves. Parts 1–3 steer what you design and build. Parts 4–5 score the result.

**The score decides.** Score twice: on the plan before you build, and in the running app before you call it done. Review alone never passes a change — in the calibration run ([examples/small-repo.md](examples/small-repo.md)) 28 of 33 points only showed up when someone used the running app.

**The numbers are the product of the audit.** A diagnosis without a comparable number is worthless after one release: nobody can tell whether a fix helped. The one file that must survive is the scorecard, and the one table that must grow is the leader board. Everything else — the report, the screenshots, the notes — is supporting.

| Mode | When | Parts |
|---|---|---|
| Build | Before and while designing or building a flow | 1 Journey first · 2 Defaults and disclosure · 3 Banned patterns |
| Review | A design, mock, screenshot or UI diff | 4 Scoring review |
| Walk | The change runs | 5 Installed-app walk |

If the skill is running somewhere that cannot read this whole file, work from this one line: *a person should never do work the product already had enough information to do itself; score the journey and keep the numbers.*

## The test for every step

Ask two questions of each step a person takes:

1. **Does only the person have this?** One of five kinds:
   - *Intent*: what they want done (the task text, which folder).
   - *Choice*: a pick between two or more valid options the product can't rank with confidence.
   - *Approval*: accepting a risk only they can accept (access, spend, delete, untrusted import).
   - *Secret*: something the product must never guess (a key, a password).
   - *Physical action*: something off the screen (approve on a phone, plug in a device).
2. **Is this the first time it's asked inside its reach?** Every approval covers an area. Asking again inside that area is friction.

Yes to both: necessary. Anything else: friction.

Three rules follow, and they settle most design arguments:

- A choice with one option is not a choice. Use it and say which.
- A choice the product can make with confidence, which the person can change later, is a default.
- An approval already given for the same risk is not a new approval.

**When you can't place a step, walk this tree** instead of guessing:

- Could the product have known this at that moment? No → necessary. Yes → keep going.
- Is it a choice? How many real options are there? One → not a choice; pick it. Several and the product can rank them → a default; pick the best and show it. Several and it can't → necessary.
- Is it an approval? What area does it cover? Already given for that area → not a new approval; ask again only when the area changes. Not given → where does the risk live? It belongs inside that flow, or the trip to it is Place (5).
- Is it a wait? Could the product be doing the work while the person reads the screen? Yes → it isn't a step for them.

The reach table (sign-in covers the account across every project, folder access covers that folder, deleting covers one action, and so on) is in [references/measure.md](references/measure.md#reach-of-an-approval).

## Part 1: Journey first

Before any screen, component or endpoint, write the journey card. Copy [templates/journey-card.md](templates/journey-card.md):

- **Result**: the outcome the person cares about ("first task running").
- **Starting state**: a newcomer's. Installed app, accounts already connected that could be reused, an item the product hasn't seen, no workarounds learned.
- **Necessary steps**: numbered, each tagged with its kind from the list above. This is the denominator. Write it before you look at any existing UI, or the UI will tell you what's "necessary".
- **Approvals**: each with its reach and when it must be asked again.
- **Target**: friction ratio ≤ 1.5, score ≤ 5, no Way forward or Progress events.

Then **score the plan before you build it**: walk the design you intend on paper, count the stages between intent and result, the controls the person has to work and the decisions the screen shows, and record that as the planned score in the card. A plan that is already over budget is over budget before anyone writes a line.

Then plan the build against the card. Any step the plan needs that isn't on the card is friction you are about to build. Remove it, turn it into a default, or show which of the five kinds it belongs to.

If the product's main journeys aren't written down yet, write them first. Most products have three to five: first launch to first result, resume after a restart, finish or apply the result, connect a second account/provider/device and use it where things already exist.

## Part 2: Defaults and disclosure

List every decision the flow touches. For each one, decide who holds it. If the product can infer it, it becomes a default: applied, shown as a fact, with a way to change it beside it.

Rules while building:

- **Reuse what's connected.** An account signed in once works in every project. Ask only when a compatibility or permission check fails, and ask inline.
- **Missing setup opens where it's needed**, inside the flow, as a sheet or inline panel. The person returns to the same draft.
- **Live state.** Status, models, connections and lists update on their own. A Refresh or Check button is never the only way to see current state. A retry the product could run itself is the same thing: retry on its own and show "Retrying".
- **Live loading.** Something just added or connected works in the running app. If a restart truly can't be avoided, offer Restart now, and restore the view and the draft afterwards.
- **Drafts survive** every detour, error, retry, decline and restart. Persist typed input keyed to its context; don't keep it only in component state.
- **Every error code has a message** that names the cause and the next action, written in the same change that adds the code. A specific code must never fall through to a generic message.
- **A disabled control says what it needs** ("Choose a folder first"), next to the control.
- **Platform basics** in native windows: Go to Folder, paste, standard shortcuts, drag and drop.
- **Plain language.** No internal IDs or codes in user-facing text; put them behind a details disclosure.
- **One place writes the setting.** Settings, forms and preferences are usually written in more than one place: the screen, the handler, sometimes a config or a default. Check that the control the person presses is the one that changes the state the flow reads, and that a control with no handler never ships (scan 8 in [references/patterns.md](references/patterns.md#static-scan)).

### Ask first, or act and offer Undo

One standing choice for every action. Don't mix them inside a flow.

| | Ask first | Act and offer Undo |
|---|---|---|
| When | Intent is unclear, or the stakes are high: delete, overwrite, spend, new access, untrusted import, secrets | Everything reversible |
| The person sees | What it allows, for how long, and what happens if declined | What just happened, with Undo |
| If they decline or undo | The draft is kept and a way forward stays open | Back to where they were |
| Counted as | Necessary, once inside its reach | Nothing |

A confirmation on something that can be undone is a Time event (1) each. A confirm that then leaves a dead button behind it is Way forward (10) — see banned pattern 8.

### Error recipe

Every error the person can meet has three parts in this order: **what happened** in their words, **why**, and **the next action** as a control on the error itself. Not "Something went wrong", not a code, not an instruction to go and find something. If the error can only be fixed by the product, the error is wrong: fix it instead.

Control budgets, which can be counted on a design before anyone uses it:

| Count | Budget | Each one over |
|---|---|---|
| Inferable decisions shown in a main journey | 0 | Time (1) on the same screen; Search (3) if it lives in Settings |
| Visible controls in a settings section by default | ≤ 5, intent-level; the rest behind Advanced | Attention (2) per section |
| Primary actions per screen | Exactly one stands out | Attention (2) |
| Stages between intent and result | One per necessary step | Time (1); Place (5) if it leaves the current view |
| Confirmations on undoable actions | 0 | Time (1) each |

An approval is necessary only when all of these hold: it's asked once inside its reach; it's asked where the risk is, inside the flow that needs it; it says what it allows, for how long and what happens if declined; the draft is kept whichever way the person answers; declining leaves a way forward. Each failure scores; see [references/measure.md](references/measure.md#when-approval-is-friction).

The agent build habits that produce friction, each with its replacement, are in [references/patterns.md](references/patterns.md#build-habits). Read that table before building a new flow. The habits feel like good engineering from inside one feature: a control for every setting, a new screen per stage, a confirmation "to be safe", the new action placed next to the code that runs it, a safety check repeated at every level, "restart to apply" because live loading is harder, tests on fixtures as the proof.

## Part 3: Banned patterns

Refuse these in any design or code you produce, and flag them in anything you review:

1. An add or open action missing from the view that lists the items.
2. A disabled control with no visible reason.
3. An error with no cause or next action, or one that points at the wrong cause.
4. "Restart to apply", above all with no Restart now button.
5. Refresh, Check or Try again as the only way to see state or make progress.
6. A confirmation led by internal IDs, or internal IDs in any user-facing text.
7. A picker, dropdown or radio group that can show a single option.
8. A confirm dialog on an undoable action that then leaves the button dead or the work undone.
9. A control with no handler, a no-op handler, or "coming soon".
10. A flow that sends the person to Settings to finish what they started.
11. Setup the person already completed, asked again for each project, workspace or item.
12. A form that asks for something the product already knows, or asks for it before it's needed.
13. Feedback the person has to scroll to see.

On a code diff, run the static scan in [references/patterns.md](references/patterns.md#static-scan). Its hits are leads; confirm each by reading the code.

## Part 4: Scoring review

For a design, mock, screenshot or diff:

1. Take the journey card (write it if missing).
2. Walk the planned path through the design on paper, as the newcomer. Include the likely wrong turns: where would a newcomer look first for the main action?
3. Classify every friction event with the table below, plus the control budgets above.
4. Write the events to a scorecard and run the scorer. The scorecard is the deliverable, not the report.

A design that passes review can still score in the broken band once used. Review catches the screen-visible kinds early and cheaply; it passes nothing on its own.

## Part 5: Installed-app walk

This part decides whether a user-visible change passes. Procedure in [references/measure.md](references/measure.md#scoring-a-journey); in short:

1. Build and install, or launch, the app as a person would get it. Use a clean starting state: a new item outside existing ones, a connected account that could be reused, no learned workarounds.
2. Drive it with the automation you have (computer use, browser tools, Playwright, the platform's UI test runner). Start a timer at launch.
3. Record every step, including wrong turns and waits. Deliberately try the wrong turns a newcomer would take: the nested or overlapping item, the missing connection, the error path, the restart.
4. At every interruption (detour, error, retry, decline, restart), check whether typed text is still there. Record kept or lost.
5. Test each step with the two questions, group friction steps into events, weight them, run the scorer.

**Write two files before you report anything**, so the work survives the session:

- `scorecard.json` — the events, the steps, the ratio, the score, the two supporting numbers. Use [templates/scorecard.json](templates/scorecard.json). Every event carries `id`, `cause`, `loss` and `fix`; every step that is friction names its event id. Attach the evidence to the events themselves (`screen` or `behaviour`, and where it was seen) rather than leaving it in a report nobody can re-check.
- A row in `friction-leaderboard.md`, in the product's own repo, one row per journey per build:

```markdown
| Date | Build | Journey | Steps ÷ necessary | Score | Band | Time to first result | Drafts |
```

Without those two files the audit didn't happen. A chat summary is not a scorecard.

After fixes, rescore from the same starting state and add the new row. The pair of rows is what says whether a fix helped.

If the walk can't run (no build, no access, the tool was denied), the friction check is **pending**. Say what blocks it and the smallest thing that would unblock it. Never report a pass from review or unit tests alone; fixture tests miss every behaviour-only kind.

## Scoring

**Events.** One event is one piece of friction with one cause. Count two events when they could be fixed separately. A detour to Settings (Place) and "Use in this project" there (asked again, Search) are two events: moving the button into the composer removes the detour but keeps the repeat; reusing the signed-in account removes both.

**Steps.** One click, shortcut, typed entry, decision or wait. A whole task description is one step. Quit and reopen are two. Keep one way of cutting steps across a project so scores compare.

| Loss | What happens to the person | Signals | Weight |
|---|---|---|---|
| `time` | One extra action on the screen they're on | Confirming something undoable; picking the only option; retyping a value the screen shows | 1 |
| `attention` | They must notice or work something out to carry on | Refresh/Check needed to see state; missing platform shortcut; internal IDs; wording that needs translating | 2 |
| `search` | The action exists somewhere they wouldn't look | Main action only via search, palette, shortcut or another page; setup asked again somewhere they must already know | 3 |
| `place` | They leave what they were doing, fix a missing piece, find their way back | Composer → Settings → back; a setup screen reached from an error | 5 |
| `progress` | Work or state they had is gone and must be rebuilt | Quit and reopen; "starts after restart"; lost draft; reset form; lost scroll position | 8 |
| `way_forward` | They can't continue without outside help | Generic error; greyed-out button with no reason; button that does nothing; error pointing at the wrong cause | 10 |

- **Friction ratio** = steps taken ÷ necessary steps. 1.0 means the person did only what only they could do.
- **Friction score** = sum of event weights. Bands: 0–5 normal, 6–15 noticeable (people learn workarounds and pass them on), 16+ broken (people need help, or stop).
- **Budget for a main journey:** no `way_forward` or `progress` events; no `search` event for the journey's main action; `place` events only where an approval is needed and the person returns to the same draft; ratio ≤ 1.5; score ≤ 5. Any `way_forward` or `progress` event fails the journey whatever the total.
- **Supporting numbers:** time to first result (seconds from launch), and draft survival (kept/lost per interruption; each loss is a `progress` event).

Run the scorer (Python 3, no dependencies; the path is relative to this skill's folder):

```bash
python3 scripts/friction_score.py scorecard.json        # markdown report
python3 scripts/friction_score.py scorecard.json --json # machine-readable
```

Exit code 0 means within budget, 1 over budget, 2 bad input. [examples/small-repo.json](examples/small-repo.json) scores 33, ratio 4.0, broken; use it to check you're cutting steps and events the same way.

## Fixing

Fix the heaviest events first. Standard fixes by class:

| Class | Fix |
|---|---|
| `way_forward` | A specific message naming the cause and the next action, with that action as a button; a disabled control states what it needs; a dead button works or goes |
| `progress` | Load live, without a restart; persist drafts per context; keep scroll and selection across navigation; if a restart is unavoidable, Restart now plus full state restore |
| `place` | Bring the missing setup into the flow as an inline sheet; return to the same draft |
| `search` | Put the add/open action on the view that lists the items; make the main action visible; reuse completed setup inside its reach |
| `attention` | Live state instead of Refresh; plain words instead of IDs; platform shortcuts |
| `time` | Defaults; auto-pick a single option; Undo instead of confirm |

Rescore from the same starting state after the fixes. Report how many points each fix removed.

## Report

When you score a journey, report:

- Journey, result, starting state, build or commit scored.
- Ratio, score, band, time to first result, draft survival (or "not recorded").
- The events table from the scorer.
- Verdict against the budget, with each failing rule.
- Fix-first list, ordered by points removed, with the points each one covers.
- Where the scorecard and the leader board row are.

## Limits

The measure counts effort; a journey can score 0 and still do the wrong thing. The weights set the order of cost and their gaps are estimates: tune them after several journeys, keeping the order (the scorer refuses weights that break it). It scores the newcomer; a regular who has learned the workarounds meets less friction on the same build. Necessary approvals still cost time and stay out of the score, because removing them would remove a protection.

Full definitions, the reach table, counting rules and the approval failure table: [references/measure.md](references/measure.md). Pattern catalogue, build habits and static scan: [references/patterns.md](references/patterns.md).
