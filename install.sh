#!/usr/bin/env bash
# Link this checkout into every agent's skills folder on this machine.
# A link keeps the installed skill identical to the checkout: a git pull or a
# local edit takes effect in both, with no second copy to drift.
# Re-runnable. Only ever replaces a link of ours that points somewhere old;
# an existing real installation is left alone and reported.
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$src/SKILL.md" ]; then
  echo "Run this from the manual-friction-antipattern checkout." >&2
  exit 1
fi

dest="${1:-}"
if [ -n "$dest" ]; then
  # install.sh /path/to/skills  (for Codex: ~/.codex/skills)
  targets=("$dest/manual-friction")
else
  targets=()
  for base in "$HOME/.claude" "$HOME/.codex" "$HOME/.cursor" "$HOME/.windsurf" "$HOME/.config/opencode"; do
    [ -d "$base" ] && targets+=("$base/skills/manual-friction")
  done
fi

if [ "${#targets[@]}" -eq 0 ]; then
  echo "No agent folder found. Pass a skills folder instead:" >&2
  echo "  ./install.sh ~/.codex/skills" >&2
  exit 1
fi

for link in "${targets[@]}"; do
  read -r -a skill_dirs <<< "$(ls -d "$link" 2>/dev/null || true)"
  if [ -L "$link" ]; then
    if [ "$(readlink "$link")" = "$src" ]; then
      echo "Already linked: $link"
      continue
    fi
    echo "Removing old link: $link -> $(readlink "$link")"
    rm "$link"
  elif [ -e "$link" ]; then
    echo "Left alone (existing installation): $link"
    continue
  fi

  skills_dir="$(dirname "$link")"
  mkdir -p "$skills_dir"
  if ls "$link" >/dev/null 2>&1; then
    continue
  fi
  ln -s "$src" "$link"
  echo "Linked: $link -> $src"
done

echo
echo "New sessions will load the skill. The scorer stays in the same folder:"
echo "  python3 $src/scripts/friction_score.py scorecard.json"
