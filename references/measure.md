# Manual Friction: the measure

Full definitions behind `SKILL.md`. Examples come from Qwobolt, the agent workbench where the measure was first applied. The rules are general.

## Definition

Manual friction is work a person does that the product already had enough information to do itself.

*Work* covers any step: a click, a shortcut, a choice, typing, going somewhere to find something, waiting for a restart, or working out what went wrong. *Enough information* means what the product knew at that moment: accounts already signed in, folders already chosen, settings already made, the only option available, the cause of its own error.

## What only the person has

These steps are the reason the product exists. They are necessary and never counted as friction.

| Kind | Meaning | Examples |
|---|---|---|
| Intent | What they want done | The task text; which folder to work in |
| Choice | A pick between two or more valid options that the product can't rank with confidence | Which provider or model, when more than one is ready; which of several checks to run |
| Approval | Accepting a risk only they can accept | Giving a folder access; spending; deleting; bringing in untrusted content |
| Secret | Something the product must never guess | An API key or password |
| Physical action | Something off the screen | Approving a sign-in on a phone; plugging in a device |

A choice with one option is not a choice. A choice the product can make with confidence, which the person can change later, is a default. An approval the person already gave for the same risk is not a new approval.

## Reach of an approval

Every approval covers an area: the things the risk belongs to. Asking once for that area is necessary. Asking again for something inside it is friction.

| Approval | Its reach | Ask again when |
|---|---|---|
| Sign in to a provider or account | The account, across every project | The account changes or the sign-in expires |
| Access to a folder | That folder | A different folder is chosen |
| Run a project check script | That script as it is now | The script's contents change |
| Spending | The budget set | The budget would be exceeded |
| Deleting or overwriting | That one action | Every time |
| Untrusted import | That one import | Every time |
| Storing a secret | That secret | It is replaced or cleared |

Checks the product runs for its own sake, such as whether an installed agent is compatible, belong to the product. When they pass, the person sees nothing. When they fail, the person gets the cause and the next action.

To store an approval at its reach, key it by the reach: account ID for sign-in, folder path for access, content hash for a script, budget ID for spend. Deletes and imports are never stored.

## The test for each step

1. Does only the person have this? Intent, a real choice, an approval, a secret or a physical action.
2. Is this the first time it is asked inside its reach?

Yes to both: necessary. Anything else: friction.

## What gets counted

**Step.** One click, one shortcut, one typed entry, one decision, or one wait the person has to sit through. Typing a whole task description is one step. Quitting and reopening the app are two.

**Journey.** A path from a starting point to a result the person cares about. Qwobolt's main journeys:

- Launch → add a folder → first task running
- Reopen a task after the app restarts
- Apply a finished task's changes to the project
- Connect a second provider and use it in an existing project

**Starting state.** Score each journey as a newcomer would meet it: the installed app, a provider already signed in, a new folder outside every existing project, no workarounds learned. A person who knows the tricks hides friction, because they skip the wrong turns.

**Event.** One piece of friction with one cause. Two events are counted separately when they could be fixed separately. Going to Settings (a detour) and pressing "Use in this project" (asked again) are two events: putting the button in the composer removes the detour and keeps the second request, while reusing the signed-in provider removes both.

## Friction ratio

```
friction ratio = steps taken ÷ necessary steps
```

1.0 means the person did only what only they could do. 2.0 means half their steps were the product's work. It treats every step the same, so a redundant click and a restart count alike; the score handles that.

## Friction score

```
friction score = Σ weight of each friction event
```

Ordered by loss; each class costs more than the one above, and the last two can end the journey.

| Loss | What happens to the person | Signals | Weight |
|---|---|---|---|
| Time | One extra action on the screen they're already on | Confirming something that can be undone; picking the only option; retyping a value the screen already shows | 1 |
| Attention | They must notice or work something out before carrying on | A Refresh or Check button needed to see current state; a missing platform shortcut; internal IDs to decode; wording that needs translating | 2 |
| Search | The action exists, somewhere they wouldn't look | A main action reachable only through search, a command palette, a shortcut or another page; setup asked for again in a place they must already know about | 3 |
| Place | They leave what they were doing to fix a missing piece, then find their way back | Composer → Settings → back; a setup screen reached from an error | 5 |
| Progress | Work or state they had is gone and must be rebuilt | Quit and reopen; "starts after restart"; a lost draft; a reset form; lost scroll position in a long review | 8 |
| Way forward | They can't carry on without outside help | A generic error; a greyed-out button with no reason; a button that does nothing; an error pointing at the wrong cause | 10 |

The weights set the order of cost. Tune the values once several journeys have been scored; keep the order.

## Bands and budget

| Score | Band | Meaning |
|---|---|---|
| 0–5 | Normal | A few extra clicks; nobody remarks on them |
| 6–15 | Noticeable | People learn workarounds and pass them on |
| 16+ | Broken | People need help, or stop |

Budget for a main journey:

- No Way forward or Progress events.
- No Search events for the journey's main action.
- Place events only where an approval is needed, and the person returns to the same draft.
- Friction ratio ≤ 1.5.
- Friction score ≤ 5.

Any Way forward or Progress event fails a journey, main or not, whatever the total.

## Two supporting numbers

**Time to first result.** Seconds from launching the app to the result running, from the newcomer starting state. Easy to track release to release, and it catches slow steps the ratio misses, such as a long wait for a check.

**Draft survival.** After every detour, error, retry and restart: is what the person typed still there? Record kept or lost for each interruption. Each loss is a Progress event.

## When approval is friction

An approval is necessary when all of these hold:

1. It is asked once inside its reach.
2. It is asked where the risk is, inside the flow that needs it.
3. It says what it allows, for how long, and what happens if declined.
4. The person's draft is kept whichever way they answer.

And declining leaves a way forward. Each failed condition turns the approval, or part of it, into friction:

| Failure | Counted as | Weight |
|---|---|---|
| Asked again inside its reach | Search, or Time if on the same screen | 3 / 1 |
| Asked on a different page from the flow | Place | 5 |
| No explanation, or internal terms | Attention | 2 |
| Answering loses the draft | Progress | 8 |
| Declining gives no way forward | Way forward | 10 |

## Control friction

Exposed controls and split-up flows are friction too: decisions and stages the product could have handled. Unlike most behaviour-only friction, they can be counted on a design before anyone uses the app.

| Count | Budget | Each one over counts as |
|---|---|---|
| Inferable decisions shown: choices the product could make with a default the person can change later | 0 in a main journey | Time (1) on the same screen; Search (3) if it lives in Settings |
| Visible controls in a settings section by default | ≤ 5 high-level intent controls; the rest behind Advanced | Attention (2) per section over |
| Primary actions per screen | Exactly one stands out | Attention (2) when none does, or several share equal weight |
| Stages between intent and result | One per necessary step | Time (1) per extra stage; Place (5) if it leaves the current view |
| Confirmations on actions that can be undone | 0: act, show what happened, offer Undo | Time (1) each |
| Controls whose only decision is an internal path: a separate button, screen or flow for a saved copy, a prepared task, a stored draft or a staging step | 0: restore the work where the person goes next | Attention (2) each; Place (5) if it opens another view |

**Implementation-led controls.** The review question for any extra control is what decision it lets the person make. If the answer is only which internal path the app takes, the person is being asked to learn how the app is built, and the app should take the path itself.

**Ask or act.** The product asks before acting only when it is unsure of the person's intent or the stakes are high. Otherwise it acts, shows what it did, and offers Undo. Actions appear beside the work they apply to, and detail stays behind a disclosure until someone opens it.

## Screen or behaviour

Some friction can be seen on a screen or a design board. The rest only shows when someone uses the running app. This decides how each kind is caught.

| Visible on a screen (caught in review) | Only in behaviour (caught by walking the installed app) |
|---|---|
| Add or open action missing from the view that lists the items | Something just added needs a restart to work |
| Greyed-out button with no reason | Draft lost after a detour or error |
| Error state with no cause or next action | Signed-in account set up again for each project |
| "Restart to apply" with no Restart now button | Error code falls through to a generic message |
| Refresh or Check as the only way to see state | Button that does nothing |
| Confirmation led by internal IDs | Platform shortcut missing in native windows |
| Picker with one option | |

Of the 33 points in the small-repo run, 5 were visible on a screen. The other 28 only showed in behaviour. A design can pass review and still score in the broken band.

## Scoring a journey

1. Pick the journey and its result.
2. Write the necessary steps first, before touching the app. This is the denominator.
3. Set the newcomer starting state.
4. Walk it as a newcomer. Record every step, including wrong turns and waits. Start a timer at launch.
5. Test each step with the two questions.
6. Group friction steps into events by cause, splitting where the fixes would differ.
7. Weight each event with the loss table, and the approval table for approvals.
8. Record the ratio, score, time to first result and draft survival.
9. Compare with the budget. Any Way forward or Progress event fails the journey, whatever the total.
10. Rescore after fixes from the same starting state.

## Limits

- It measures effort. A journey can score 0 and still do the wrong thing.
- The weights rank costs; the gaps between them are estimates.
- Step counts depend on how finely steps are cut. Keep one way of cutting across a project so scores compare.
- A newcomer and a regular meet different friction. This measure scores the newcomer.
- Necessary approvals still cost time. They stay out of the score because removing them would remove a protection.
