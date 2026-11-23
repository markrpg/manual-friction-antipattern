#!/usr/bin/env python3
"""Score a manual-friction scorecard.

Usage: friction_score.py SCORECARD.json [--json]
Exit codes: 0 within budget, 1 over budget, 2 bad input.
"""
import argparse
import json
import sys

LOSSES = ["time", "attention", "search", "place", "progress", "way_forward"]
DEFAULT_WEIGHTS = {"time": 1, "attention": 2, "search": 3, "place": 5, "progress": 8, "way_forward": 10}
MAX_RATIO = 1.5
MAX_SCORE = 5


def band(score):
    if score <= 5:
        return "normal"
    if score <= 15:
        return "noticeable"
    return "broken"


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def score_card(card):
    weights = {**DEFAULT_WEIGHTS, **card.get("weights", {})}
    if set(weights) != set(LOSSES):
        fail(f"weights must use exactly these classes: {', '.join(LOSSES)}")
    ordered = [weights[k] for k in LOSSES]
    if any(a >= b for a, b in zip(ordered, ordered[1:])):
        fail("weights must keep the order time < attention < search < place < progress < way_forward")

    events = card.get("events", [])
    ids = set()
    for e in events:
        if e.get("loss") not in weights:
            fail(f"event {e.get('id', '?')}: loss must be one of {', '.join(LOSSES)}")
        if "id" in e:
            if e["id"] in ids:
                fail(f"duplicate event id {e['id']}")
            ids.add(e["id"])

    warnings = []
    steps = card.get("steps")
    for i, s in enumerate(steps or [], 1):
        ev = s.get("event")
        if ev and ev not in ids:
            warnings.append(f"step {i} refers to unknown event {ev}")
        if s.get("necessary") and ev:
            warnings.append(f"step {i} is marked necessary but carries event {ev}")

    necessary = card.get("necessary_steps", [])
    taken = card.get("steps_taken", len(steps) if steps is not None else None)
    ratio = round(taken / len(necessary), 2) if taken and necessary else None
    if steps is not None and necessary:
        marked = sum(1 for s in steps if s.get("necessary"))
        if marked != len(necessary):
            warnings.append(f"{marked} steps marked necessary, {len(necessary)} listed in necessary_steps")

    total = sum(weights[e["loss"]] for e in events)
    main = card.get("main_journey", True)

    failures = []
    for e in events:
        label = f"{e.get('id', '?')} ({e.get('cause', e['loss'])})"
        if e.get("ungated_diagnostic"):
            failures.append(f"developer or test tooling a production user can reach: {label}")
        if e["loss"] in ("way_forward", "progress"):
            failures.append(f"{e['loss']} event: {label}")
        elif main and e["loss"] == "search" and e.get("main_action"):
            failures.append(f"search event on the main action: {label}")
        elif main and e["loss"] == "place" and not (e.get("approval_needed") and e.get("draft_kept")):
            failures.append(f"place event without a needed approval and a kept draft: {label}")
    if main and ratio is not None and ratio > MAX_RATIO:
        failures.append(f"friction ratio {ratio} > {MAX_RATIO}")
    if main and total > MAX_SCORE:
        failures.append(f"friction score {total} > {MAX_SCORE}")

    survival = card.get("draft_survival")
    lost = [d for d in survival or [] if not d.get("kept", True)]
    progress_events = sum(1 for e in events if e["loss"] == "progress")
    if len(lost) > progress_events:
        warnings.append(f"{len(lost)} lost drafts but {progress_events} progress events; each lost draft is a progress event")

    screens = card.get("screens")
    for sc in screens or []:
        for key in ("controls", "words", "controls_before", "words_before"):
            if key in sc and (not isinstance(sc[key], int) or sc[key] < 0):
                fail(f"screen {sc.get('name', '?')}: {key} must be a whole number")

    by_class = {k: sum(weights[k] for e in events if e["loss"] == k) for k in LOSSES}
    return {
        "journey": card.get("journey"),
        "result": card.get("result"),
        "build": card.get("build"),
        "mode": card.get("mode"),
        "main_journey": main,
        "steps_taken": taken,
        "necessary_steps": len(necessary),
        "ratio": ratio,
        "score": total,
        "band": band(total),
        "by_class": by_class,
        "events": [{**e, "weight": weights[e["loss"]]} for e in events],
        "time_to_first_result_s": card.get("time_to_first_result_s"),
        "draft_survival": survival,
        "screens": screens,
        "pass": not failures,
        "failures": failures,
        "warnings": warnings,
    }


def markdown(r):
    na = "not recorded"
    out = [f"## {r['journey'] or 'Journey'}", ""]
    if r["result"]:
        out.append(f"Result: {r['result']}  ")
    if r["build"]:
        out.append(f"Build: {r['build']}  ")
    if r["mode"]:
        out.append(f"Mode: {r['mode']}  ")
    ratio = f"{r['ratio']} ({r['steps_taken']} ÷ {r['necessary_steps']})" if r["ratio"] is not None else na
    t = r["time_to_first_result_s"]
    ds = r["draft_survival"]
    drafts = (f"{sum(1 for d in ds if d.get('kept', True))} kept, "
              f"{sum(1 for d in ds if not d.get('kept', True))} lost") if ds else na
    out += [
        f"Friction ratio: {ratio}  ",
        f"Friction score: {r['score']} ({r['band']})  ",
        f"Time to first result: {f'{t} s' if t is not None else na}  ",
        f"Draft survival: {drafts}",
        "",
        "| Event | Cause | Loss | Weight | Fix |",
        "|---|---|---|---|---|",
    ]
    for e in sorted(r["events"], key=lambda e: -e["weight"]):
        out.append(f"| {e.get('id', '')} | {e.get('cause', '')} | {e['loss']} | {e['weight']} | {e.get('fix', '')} |")
    out.append(f"| | **Total** | | **{r['score']}** | |")
    out.append("")
    if r["screens"]:
        def cell(sc, key):
            after, before = sc.get(key), sc.get(key + "_before")
            if after is None:
                return "—"
            if before is None:
                return str(after)
            return f"{before} → {after} ({after - before:+d})"
        out += ["| Screen | Visible controls | Words |", "|---|---|---|"]
        for sc in r["screens"]:
            out.append(f"| {sc.get('name', '')} | {cell(sc, 'controls')} | {cell(sc, 'words')} |")
        out.append("")
    if r["pass"]:
        out.append("**Within budget.**" if r["main_journey"] else "**No way_forward or progress events.**")
    else:
        out.append("**Over budget:**")
        out += [f"- {f}" for f in r["failures"]]
    if r["warnings"]:
        out += ["", "Warnings:"] + [f"- {w}" for w in r["warnings"]]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Score a manual-friction scorecard.")
    ap.add_argument("scorecard")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = ap.parse_args()
    try:
        with open(args.scorecard, encoding="utf-8") as f:
            card = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))
    r = score_card(card)
    print(json.dumps(r, indent=2, ensure_ascii=False) if args.json else markdown(r))
    sys.exit(0 if r["pass"] else 1)


if __name__ == "__main__":
    main()
