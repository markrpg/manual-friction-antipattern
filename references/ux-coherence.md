# UX coherence

Read this when a change affects routes, ownership or how someone carries work between views. For a local edit, use the existing view's conventions and check the changed behaviour in place.

## What to consult

| Source | What to look up | Where to verify it |
|---|---|---|
| Product model and interaction conventions (`PRODUCT_UX.md`) | What people come to do, what belongs to a project or account, and how shared actions behave | The vocabulary, controls and state in related views |
| Navigation map (`NAVIGATION.md`) | Hierarchy, routes, which area owns each capability, and which links lead there | Route definitions, menus, links and handlers |
| User journeys (`USER_JOURNEYS.md`) | Why someone starts in a given place, what each transition carries, and what result lets them continue | Running app and interaction tests for critical paths |

Use the product's existing files or a single document. A journey card is enough for a small app. Record the parts you need, link to the implementation, and update the notes or tests when a route or handoff changes. Generate route facts from code where the router supports it; a route list won't tell you what happens to a draft on the way back.

## Decide where the action belongs

Write the person's goal and necessary steps first. Inspect the views involved and find who already manages the action and writes the state. Compare extending that view or reusing its action in context with adding a destination. Write down the distinct task a new destination serves, where someone expects to find it, and what they can do next. Reuse navigation labels and behaviour people already know.

Give the capability one owner. A full management view can serve someone who plans to configure several accounts; the same connection form can open beside the model picker for someone midway through a task. Direct links, shortcuts and contextual entries can coexist when they lead to the same operation and explain the same outcomes.

## Walk the handoffs

Record the entry and destination, what the next action needs, and where success, Back, Cancel and a recoverable error leave someone. Check the draft, project, choice, focus or scroll position wherever losing it changes the next action. Compare the same action across its entry points. Check that outcomes and errors agree and that the state updates everywhere it is used.

**Example: connect a provider and use a model.** Provider management owns connections. From the composer, someone who wants another model opens its connection form, supplies the key or grants access there, and sees the new model become available on return. Their project and draft are still in place; the app leaves model choice to them unless they already made it. Cancel and Back return without changing their model. If a key is rejected, the form names the cause and lets them try a different key without making them rebuild the draft. Someone who opens provider management directly can connect the same account and continue managing providers. Neither path asks for access that was already granted within its reach.

Walk each path from its own starting state. Score any observed friction with the [existing loss classes](measure.md#friction-score). Verify the actual result as well: a low score can't make the wrong model run acceptable.

## Carry findings into planning

If the product keeps a journey register, give the steps stable IDs. For a critical handoff, record the screen, action, expected result, state that survives, and which source the next screen reads. Record exceptions beside the affected step with the expected recovery. Reuse step IDs when several journeys share an entrance or transition.

Capture the state after each changed handoff. Use a screenshot for visible problems and a state or interaction assertion when the failure is in what the next action reads. Try an unguided walk as the intended user as well; a script that already knows the route cannot test discovery. Record unchecked steps as pending, including when the app opens but the walker cannot reach the view.

Keep a short finding with its journey step, observed loss, evidence and fix. Link it from the issue or roadmap row that owns the fix, order work by the cost to the person, and rerun the affected path before closing the finding. Review related journeys together for a missing prerequisite, a path that ends before the useful result, and screens that disagree about the same state.
