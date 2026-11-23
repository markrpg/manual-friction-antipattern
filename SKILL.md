---
name: manual-friction
description: >
  Prevents and measures manual friction: work a person does that the product
  already had enough information to do itself. Catches accounts set up again
  per project, restart-to-apply, detours to Settings, generic errors, dead or
  unexplained disabled buttons, one-option pickers, redundant confirms,
  Refresh buttons, internal IDs, lost drafts, implementation-led controls,
  wordy labels, overexposed features, production debug tools, and fragmented
  navigation or disconnected journeys. Use before building or changing any
  user-facing screen or flow, including small fixes and adding an option,
  setting or model, plus onboarding, forms, errors and approval prompts; when
  reviewing a design, screenshot or UI diff; and when verifying a UI change
  in the running app. Also use when someone calls a flow clunky, fiddly,
  confusing, a slog, too many clicks, or "this should just work", asks for a
  UX review or flow audit, or says "manual friction", "friction score",
  "antidesign" or /manual-friction.
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
- Is it a control? What decision does it let the person make? If the only answer is which internal path the app takes (open the saved copy, resume the prepared task, review the stored draft), the app takes that path itself.

The reach table (sign-in covers the account across every project, folder access covers that folder, deleting covers one action, and so on) is in [references/measure.md](references/measure.md#reach-of-an-approval).

## Part 1: Journey first

Before any screen, component or endpoint, write the journey card. Copy [templates/journey-card.md](templates/journey-card.md):

- **Result**: the outcome the person cares about ("first task running").
- **Starting state**: a newcomer's. Installed app, accounts already connected that could be reused, an item the product hasn't seen, no workarounds learned.
- **Necessary steps**: numbered, each tagged with its kind from the list above. This is the denominator. Write it before you look at any existing UI, or the UI will tell you what's "necessary".
- **Approvals**: each with its reach and when it must be asked again.
- **Target**: friction ratio ≤ 1.5, score ≤ 5, no Way forward or Progress events.

### Place the change in the app

For changes that affect routes, feature ownership or handoffs, read the product's UX notes if they exist. Check them against the routes and related screens in use. Record in the card where people start, which existing area owns the capability, where each path leads, and what must carry across. Review the screens together before designing any one of them. Give changed handoffs step IDs so reviewers and planners can refer to the same place.

Extend an existing view or open the shared action in context when it fits. A new destination needs a distinct user goal, a discoverable entry, and an exit that leaves the person ready for what they came to do. Use the app's existing navigation and interaction conventions. Different entry points can use the same action and state; keep useful shortcuts, direct links and standalone management. See [references/ux-coherence.md](references/ux-coherence.md) for the shared UX contract and a worked example.

Then **score the plan before you build it**: walk the design you intend on paper, count the stages between intent and result, the controls the person has to work and the decisions the screen shows, and record that as the planned score in the card. A plan that is already over budget is over budget before anyone writes a line.

Then plan the build against the card. Any step the plan needs that isn't on the card is friction you are about to build. Remove it, turn it into a default, or show which of the five kinds it belongs to.

When defining a product area or reviewing the app as a whole, write down the critical journeys that aren't documented yet. Start with first launch to first result, resuming work, applying a result, or connecting another account and using it in an existing project.

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

### Controls follow what the person is doing

AI-built interfaces often give every internal state or operation its own button, screen or flow. Each one makes sense alone. Together they turn one intention into several decisions, and the person has to work out where the app put their work before they can carry on with it.

Start with what the person is trying to do and where they will naturally go to do it. Restore state and do the housekeeping there. Add a separate control only when it gives the person a genuinely different choice.

For every button, link or screen you add, ask: **what decision does this let the person make?** If the answer is "which internal path to take", the app makes it.

Example: a person comes back to Qwobolt's Hub to keep writing. The app had stored their work as a prepared task, so it offered *Review saved conversation*, with the conversation already on screen. The fix restores the text and choices into the chat box. They edit and press Continue, and any review the work requires appears before an agent starts.

### Show what the task needs

Agents build screens that mirror the implementation. Every capability they wrote gets a visible control, and every concept they handled (provider IDs, retries, runtime states, test endpoints) reaches the screen. Each addition looks thorough; together they make a screen the person has to read before they can use it. Three faults, each counted:

| Fault | What the agent produces | What to build | Counted as |
|---|---|---|---|
| Wordiness | Long headings, sentence-length button labels, helper text that restates the heading, status repeated in prose | Short familiar labels, a verb and a noun for an action; a line of help only when it carries a source, a count, a time, a cause, a consequence or the next action | Attention (2) per screen that has to be read before acting |
| Exposure | A button, toggle or panel for every capability, all at the same weight | The common task up front; infrequent and expert controls one disclosure away, beside the work they change | Attention (2) per infrequent control on a main journey screen |
| Leakage | Debug panels, test buttons, raw JSON, state names like `IDLE_READY`, diagnostics on everyday screens | Developer tools in a diagnostic layer that production users never reach | Attention (2) each; reachable without an environment or permission check, the change fails |

Behind all three sits a habit of proving that something was implemented. For each element, ask what the person loses if it goes. If the only loss is evidence that a feature exists, it goes.

**Keep the state the person relies on.** Cutting exposure removes controls and words. State stays: the current selection, whether it's connected, progress, errors, and whether the last action worked. Before you remove any status line or indicator, name where the person sees that state afterwards. If the answer is nowhere, it stays, in fewer words. In the example below, "Connected" survives the cut.

The agent's version of a model picker:

> **AI Model Configuration and Runtime Management**
> Configure your active AI provider, manage connection parameters, inspect current operational status and execute model verification operations.
> Currently Selected AI Model Provider: OpenAI — GPT-6 — Connected and Operational
> [Apply Model Configuration] [Test Provider Connection] [Show Runtime Diagnostics] [Refresh Provider Status]
> Last configuration validation completed successfully. Runtime status: IDLE_READY.

The task's version:

> **Model** · GPT-6 · [Change]
> Connected

Every capability survives. A change applies when it's made, the connection is checked on its own (live state), and diagnostics sit in the diagnostic layer.

**Three layers.**

- *Primary*: everyday tasks, the settings that express intent, results, errors with a next action.
- *Advanced*: infrequent configuration, expert settings, detailed status, one disclosure away from the task it changes.
- *Diagnostic*: debug views, test actions, raw payloads, traces and instrumentation. Reachable only in a development build or by a signed-in support role, checked where the action runs (the server or the main process). A control hidden with CSS or a client-side flag can still be called, so leakage is a security defect as well as clutter.

**Simplify by the score.** A shorter screen helps only when the journey gets cheaper. Removing the label that explains an unfamiliar control adds an Attention event; hiding state the person needs before they trust the result adds one; trading a visible button for an extra click raises the ratio. Rescore and keep whichever version scores lower.

**Reassess after every feature.** A session that adds a feature tends to append its controls and leave the rest of the screen alone, so a clean screen degrades release by release. After adding anything visible, review the whole screen it lands on: which layer the new control belongs in, whether an existing control now duplicates it, whether the primary action still stands out. When a change touches a screen, count its visible controls and words before you edit it and again after, and record both in the scorecard (`screens`: `controls_before`, `words_before`, `controls`, `words`). A rise in either with no drop in the score is a regression to look at; the counts are signals, and a lower count with a higher score is worse.

Control budgets, which can be counted on a design before anyone uses it:

| Count | Budget | Each one over |
|---|---|---|
| Inferable decisions shown in a main journey | 0 | Time (1) on the same screen; Search (3) if it lives in Settings |
| Visible controls in a settings section by default | ≤ 5, intent-level; the rest behind Advanced | Attention (2) per section |
| Primary actions per screen | Exactly one stands out | Attention (2) |
| Stages between intent and result | One per necessary step | Time (1); Place (5) if it leaves the current view |
| Confirmations on undoable actions | 0 | Time (1) each |
| Controls whose only decision is an internal path (saved copy, prepared task, stored draft, staging step) | 0 | Attention (2) each; Place (5) if it opens another view |
| Infrequent or expert controls on a main journey screen | 0; one disclosure away | Attention (2) each |
| Developer or test tooling reachable by a production user | 0 | Attention (2) each; fails the change when nothing checks the environment or permission where the action runs |

An approval is necessary only when all of these hold: it's asked once inside its reach; it's asked where the risk is, inside the flow that needs it; it says what it allows, for how long and what happens if declined; the draft is kept whichever way the person answers; declining leaves a way forward. Each failure scores; see [references/measure.md](references/measure.md#when-approval-is-friction).

The agent build habits that produce friction, each with its replacement, are in [references/patterns.md](references/patterns.md#build-habits). Read that table before building a new flow. The habits feel like good engineering from inside one feature: a control for every setting, a button for every internal state, a sentence to explain each control, a debug panel left in, a new screen per stage, a confirmation "to be safe", the new action placed next to the code that runs it, a safety check repeated at every level, "restart to apply" because live loading is harder, tests on fixtures as the proof.

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
14. A button, screen or flow that exists only because of how the app stores or runs the work ("Review saved conversation", "Resume prepared task", "Open draft"), when the work could be restored where the person already is.
15. Copy that restates what the screen already shows, or a button label that reads as a sentence.
16. Developer or test tooling in a production flow (debug panels, test buttons, raw payloads, internal state names), or tooling hidden only by CSS or a client-side flag.
17. Infrequent or expert controls at the same weight as the screen's primary action.

On a code diff, run the static scan in [references/patterns.md](references/patterns.md#static-scan). Its hits are leads; confirm each by reading the code.

## Part 4: Scoring review

For a design, mock, screenshot or diff:

1. Take the journey card (write it if missing).
2. Walk the planned path through the related screens, as the newcomer. Check who owns the action, where someone would look first, and where each handoff leaves them.
3. Classify every friction event with the table below, plus the control budgets above.
4. Write the events to a scorecard and run the scorer. The scorecard is the deliverable, not the report.

Where you can, have the review done by an agent that didn't build the change, given the journey card and the screens involved, without coaching on where to click. Ask the reviewer to find the action and follow it through to the result.

A design that passes review can still score in the broken band once used. Review catches the screen-visible kinds early and cheaply; it passes nothing on its own.

## Part 5: Installed-app walk

This part decides whether a user-visible change passes. Procedure in [references/measure.md](references/measure.md#scoring-a-journey); in short:

1. Build and install, or launch, the app as a person would get it. Use a clean starting state: a new item outside existing ones, a connected account that could be reused, no learned workarounds.
2. Drive it with the automation you have (computer use, browser tools, Playwright, the platform's UI test runner). Start a timer at launch.
3. Record every step, including wrong turns and waits. Deliberately try the wrong turns a newcomer would take: the nested or overlapping item, the missing connection, the error path, the restart.
4. For changed handoffs, try the affected entries and check where success, Back, Cancel and recoverable failure leave you. Check the draft, selected item and other state the next action needs. At each interruption, record whether typed text was kept or lost. Walk distinct paths from their own starting states. For a missing or broken handoff, attach evidence from after the action to its step ID and put the fix in the project’s planning queue.
5. Test each step with the two questions, group friction steps into events, weight them, run the scorer.

**Write two files before you report anything**, so the work survives the session:

- `scorecard.json` — the events, the steps, the ratio, the score, the two supporting numbers, and the visible controls and words on each screen of the journey, before and after for any screen the change touched. Use [templates/scorecard.json](templates/scorecard.json). Every event carries `id`, `cause`, `loss` and `fix`; every step that is friction names its event id. Attach the evidence to the events themselves (`screen` or `behaviour`, and where it was seen) rather than leaving it in a report nobody can re-check.
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
- **Budget for a main journey:** no `way_forward` or `progress` events; no `search` event for the journey's main action; `place` events only where an approval is needed and the person returns to the same draft; ratio ≤ 1.5; score ≤ 5. Any `way_forward` or `progress` event fails the journey whatever the total, and so does any event marked `"ungated_diagnostic": true` (developer or test tooling a production user can reach and call).
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
| `attention` | Live state instead of Refresh; plain words instead of IDs; platform shortcuts; short labels; infrequent controls one disclosure away; developer tooling moved to the diagnostic layer behind a real check |
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
