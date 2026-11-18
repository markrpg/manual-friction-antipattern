# Prompt

Paste this into any coding agent (Claude Code, Codex, Cursor, Copilot, Windsurf) at the start of UI work:

```text
Use the Manual Friction Antipattern skill for this work. It's already installed
(~/.claude/skills/manual-friction, ~/.codex/skills/manual-friction) or can be
read at https://raw.githubusercontent.com/markrpg/manual-friction-antipattern/main/SKILL.md —
follow it:

1. Before designing or building, write the journey card: the result, a
   newcomer's starting state, and the steps only the person can supply.
2. While building, turn every decision the product can infer into a default,
   and refuse the banned patterns.
3. Before calling the change done, walk the journey in the running app as a
   newcomer. Write the scorecard and the leader-board row before you report
   anything. Report the friction ratio, the score, each event, and any budget
   failures. If you can't run the app, say the check is pending and what you
   need from me.
```

To score an existing flow instead:

```text
Using https://raw.githubusercontent.com/markrpg/manual-friction-antipattern/main/SKILL.md,
score the journey from <start> to <result> in this app. Write the necessary
steps first, then walk it as a newcomer and report the ratio, score, events
and the fixes ordered by points removed.
```
