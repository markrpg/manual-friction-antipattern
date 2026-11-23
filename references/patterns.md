# Patterns, build habits and static scan

## Build habits

The root cause: most software in training data is dashboards full of actions, settings pages with every toggle visible, multi-step wizards and forms that ask for everything up front. Asked to "build a UI for X", a model reaches for the middle of that, and prompts add to it ("add a settings page for the AI" asks for a control surface). An AI product can infer intent, keep context and pick defaults, yet generated interfaces still treat it as a backend the person steers with forms and buttons.

The way agents build adds more. Each habit below looks sound inside one feature. Check your plan against the table before building.

| Habit | Friction it produces | Qwobolt instance | Do instead |
|---|---|---|---|
| A control for every setting, all visible | Time, Attention | Project checks: pick a candidate and save, even when only one was found | Apply the single or best candidate; show it as a fact with Change beside it |
| Work split into separate screens and stages | Place, Time | Provider set up in Settings, away from the composer that needs it | One stage per necessary step; missing setup opens inline in the flow |
| Confirmation before low-risk actions | Time | Continue draft asks for a second confirmation | Act, show what happened, offer Undo |
| Each feature built and tested alone; nobody walks the whole path | Progress, Way forward | Adding a project worked; opening it in the running app did not | Walk the journey end to end in the installed app before calling it done |
| New actions go beside the code that runs them | Search | Open folder sits on a Projects page the grid never links to | Put the action on the view that lists the items, and wherever the person would look first |
| Safety checks copied to every level | Search, Time | Provider sign-in repeated for each project | Store each approval at its reach; ask again only when the reach changes |
| Every internal state or operation gets its own button, screen or flow | Attention, Place | The Hub offers Review saved conversation for a conversation already on screen, because the work was stored as a prepared task | Restore the work where the person goes next; add a control only for a genuinely different choice |
| Every implemented feature gets a visible control, to show it was built | Attention | Model card with Apply, Test connection, Show diagnostics and Refresh side by side | The common task up front; the rest one disclosure away; checks run on their own |
| Implementation vocabulary reaches the screen | Attention | Runtime status `IDLE_READY` under the model picker | The person's words; internals behind Details or in the diagnostic layer |
| Explaining each control in a sentence to look clear | Attention | A heading followed by a paragraph that restates it | Short labels; help only when it carries a source, count, time, cause, consequence or next action |
| Debug and test tooling left in, or hidden with CSS | Attention, plus a security defect | Test provider connection and raw JSON on the settings screen | A diagnostic layer reachable only in a development build or by a support role, checked where the action runs |
| Each session appends its controls and leaves the screen as it was | Attention, Search | A screen that grows one panel per feature | After adding anything visible, review the whole screen; track controls and words per screen |
| Internal state shown as it is | Attention | Stop session lists attempt, runtime and generation IDs | Lead with what the person recognises (task name, folder); IDs behind Details |
| Error codes added without messages | Way forward | `working_copy_overlaps` becomes provider troubleshooting | Add the message, cause and next action in the same change as the code |
| Waiting on the app's state handed to the person | Attention | Models appear only after Check connection | Run the check on open and on change; show progress while it runs |
| "Restart to apply" chosen because live loading is harder | Progress | New projects and tool plugins | Load live; if impossible, Restart now with full state and draft restore |
| Proof from tests on test data | All behaviour-only kinds | Fixture tests passed; the installed app needed a restart | Tests guard logic; the installed-app walk proves the change |
| Small native helpers skip platform basics | Attention | Folder picker without Go to Folder | Use the platform's standard panel and its shortcuts; test them |

## Banned patterns with detection

| # | Pattern | Class | Where it shows | How to catch it |
|---|---|---|---|---|
| 1 | Add/open action missing from the view that lists items | Search (3) | Screen | Review each list view: can a newcomer add or open from here? |
| 2 | Disabled control with no visible reason | Way forward (10) | Screen | Scan 5; every disabled state needs adjacent text naming what's missing |
| 3 | Error with no cause or next action, or the wrong cause | Way forward (10) | Screen + behaviour | Scan 2 and 3; trigger each error path during the walk |
| 4 | "Restart to apply" / starts after restart | Progress (8) | Screen + behaviour | Scan 1; add a thing during the walk and use it without restarting |
| 5 | Refresh/Check as the only way to see state | Attention (2) | Screen | Scan 6 |
| 6 | Internal IDs in user-facing text | Attention (2) | Screen | Scan 7 |
| 7 | Picker that can show one option | Time (1) | Screen | Scan 9; check what renders when the list has one item |
| 8 | Confirmation on an undoable action | Time (1) | Screen | Scan 4 |
| 9 | Control with no handler, a no-op, or "coming soon" | Way forward (10) | Behaviour | Scan 8; press every control on the journey |
| 10 | Flow sends the person to Settings to finish | Place (5) | Behaviour | Scan 10 |
| 11 | Completed setup asked again per project/workspace/item | Search (3) | Behaviour | Scan 11; walk the second-project journey with an account already connected |
| 12 | Draft lost on detour, error, decline or restart | Progress (8) | Behaviour | Scan 12; type, interrupt, return, check |
| 13 | Platform shortcut missing in a native window | Attention (2) | Behaviour | Try Go to Folder (⇧⌘G), paste, drag and drop in every native panel |
| 14 | Form asks for something the product already knows, or before it's needed | Time (1) / Search (3) | Screen | Scan 13; for every field, ask what happens if it is left out and the product fills it in |
| 15 | Confirmation the person has to scroll to see | Attention (2) | Screen + behaviour | Scan 14; check the viewport after each action at the default scroll position |
| 16 | Manual retry ("Try again") where the product could retry itself | Attention (2) | Screen + behaviour | Scan 1; a retry the product runs alone is not a control |
| 17 | Control whose only decision is an internal path (Review saved…, Resume prepared…, Open draft…) | Attention (2); Place (5) if it opens another view | Screen | Scan 15; for each control ask what decision it lets the person make |
| 18 | Copy that restates what the screen shows; button labels that read as sentences | Attention (2) per screen | Screen | Scan 18; read each line of help and ask what it tells someone already looking at the screen |
| 19 | Developer or test tooling in a production flow, or hidden only by CSS or a client-side flag | Attention (2) each; ungated, the change fails | Screen + code | Scans 16 and 17; for each hit, find the check where the action runs |
| 20 | Infrequent or expert controls at the same weight as the primary action | Attention (2) each | Screen | Count the controls visible by default on each main journey screen; ask how often each is used |

## Static scan

Run from the repository root on the files a change touches (add `-g` globs to narrow, or pipe `git diff --name-only` into `rg --files-from`). Every hit is a lead: read the code and decide whether a person meets it on a journey. Patterns are written for `rg` (ripgrep); swap to `grep -rEin` if it's missing.

```bash
# 1. Restart to apply (Progress)
rg -n -i "restart (to|required|needed|the app)|after (a |the )?restart|relaunch|takes effect (after|on next)|reopen the app|requires? (a )?restart"

# 2. Generic error copy (Way forward)
rg -n -i "something went wrong|an? (unknown|unexpected) error|unknown error|please try again|error occurred|oops"

# 3. Error codes without messages (Way forward): list codes emitted, then codes mapped to copy, and diff
rg -o -N -i "(code|kind|reason|error_type)\s*[:=]\s*['\"][a-z0-9_.-]+['\"]" | sort -u
rg -n -i "switch\s*\(.*(code|kind|reason)|case ['\"][a-z0-9_]+['\"]|(default|_)\s*(:|=>)"

# 4. Confirmations (Time; check whether the action can be undone)
rg -n -i "are you sure|window\.confirm|\bconfirm\(|ConfirmDialog|AlertDialog|NSAlert|\.alert\(|showConfirm"

# 5. Disabled controls (Way forward if no visible reason nearby)
rg -n "disabled(=|:|\s*\{)|\.disabled\(|isEnabled\s*=\s*false|setEnabled\(false\)" -A2

# 6. Refresh / Check buttons (Attention)
rg -n -i "['\">](refresh|reload|check (connection|status|again)|sync now|re-?scan)['\"<]"

# 7. Internal IDs in UI text (Attention)
rg -n -i "(attempt|runtime|generation|session|request|trace|run|job)[_ ]?id\b" -g '*.{tsx,jsx,vue,svelte,swift,kt,html,xib,storyboard}'

# 8. No-op or unfinished handlers (Way forward)
rg -n -i "on(Click|Press|Tap|Select)\s*=\s*\{\s*\(\)\s*=>\s*\{\s*\}\s*\}|action:\s*\{\s*\}|coming soon|not implemented|TODO.*(handler|wire|hook up|implement)"

# 9. Pickers (Time when one option): check the single-item case
rg -n "<select|<Select|Picker\(|RadioGroup|SegmentedControl|Dropdown|NSPopUpButton"

# 10. Sending the person to Settings (Place) — hits outside settings code
rg -n -i "go to settings|open settings|in settings|navigate\(['\"]/?settings|openSettings|showSettings" -g '!**/settings/**'

# 11. Setup asked again per item (Search)
rg -n -i "use in this project|for this (project|workspace)|enable for (this|project)|per[- ](project|workspace)|connect to this"

# 12. Drafts held only in component state (Progress): list composers and text areas, then check persistence
rg -n "<textarea|<TextArea|TextEditor\(|contentEditable|multiline" 
rg -n -i "localStorage|sessionStorage|persist|draft|autosave|UserDefaults|@AppStorage|@SceneStorage"
```

For 12, every multi-line input on a main journey should appear in the second list too, keyed to its context (project, task, thread). If it doesn't, assume the draft is lost and confirm in the walk.

```bash
# 13. Fields asking for what the product already knows (Time / Search)
rg -n "placeholder=|<label|name=\"[a-z_]+\"" -g '*.{tsx,jsx,html,vue,svelte,swift,kt}'
# then for each field ask: what breaks if the product fills this in? Nothing → cut it.

# 14. Feedback the person must scroll to see (Attention) — behaviour, not regex.
# Take the viewport at the default scroll position after each action and note
# whether the result is visible without scrolling.

# 15. Controls named after how the app stores or runs the work (Attention / Place)
rg -n -i "['\">](review|resume|open|restore|load|view|continue) (the )?(saved|prepared|pending|stored|staged|cached|queued|draft)|prepared task|saved (conversation|session|state)|staging"
# for each hit ask: what decision does this let the person make? Only which
# internal path to take → restore the work where they already are and remove it.

# 16. Developer and test tooling in UI code (Attention; ungated fails the change)
rg -n -i "debug|diagnostic|devtools|dev tools|test (connection|provider|endpoint|mode)|raw (json|payload|response)|JSON\.stringify\([^)]*,\s*null,\s*2\)|<pre[ >]" -g '*.{tsx,jsx,vue,svelte,html,swift,kt}'

# 17. How that tooling is hidden: a client-side check alone leaves the action callable
rg -n "NODE_ENV|import\.meta\.env\.DEV|isDev|__DEV__|DEBUG|display:\s*none|hidden=\{" -g '*.{tsx,jsx,vue,svelte,ts,js}'
# for every scan 16 hit, find the environment or permission check where the
# action itself runs (server route, IPC handler, main process). None → fail.

# 18. Wordiness: button labels of three words or more, and state constants shown as text
rg -o -N --no-filename "<button[^>]*>[^<{]+</button>" -g '*.{tsx,jsx,vue,svelte,html}' | sed 's/<[^>]*>//g' | awk 'NF>=3'
rg -n "['\"][A-Z]{2,}(_[A-Z]{2,})+['\"]" -g '*.{tsx,jsx,vue,svelte,html,swift,kt}'
```

For 18, also read every paragraph under a heading on a main journey screen. Keep it only if it carries a source, a count, a time, a cause, a consequence or the next action.

**Two writers.** A setting is usually written in more than one place: the screen, the handler that applies it, and sometimes a config, a default or a per-item copy. Most "the button does nothing" bugs are these two disagreeing. For every control you touch, trace once from the control to the state the flow actually reads, and confirm the scan 8 hit (a no-op handler) is gone from that path. Where the product keeps per-item copies of a setting, prefer the account-level or project-level value with the per-item one as an override.

For settings sprawl, count default-visible controls per section:

```bash
rg -c "<(Switch|Toggle|Checkbox|Input|Select|Slider|RadioGroup)\b|Toggle\(|Picker\(|TextField\(" path/to/settings
```

More than five in a section means some belong behind Advanced or should become defaults.
