#!/usr/bin/env bash
# Local skill helper — returns the path to a skill's SKILL.md
# Usage: source ./skill.sh <skill-name>
#        cat $(./skill.sh ai-agents) | pbcopy   # copy to clipboard

declare -A SKILLS=(
  [manim]="skills/manim/SKILL.md"
)

if [[ $# -eq 0 ]]; then
  echo "Usage: ./skill.sh <skill-name>"
  echo ""
  echo "Available skills:"
  for key in "${!SKILLS[@]}"; do
    echo "  $key  ->  ${SKILLS[$key]}"
  done
else
  if [[ -n "${SKILLS[$1]}" ]]; then
    echo "${SKILLS[$1]}"
  else
    echo "Error: skill '$1' not found." >&2
    echo "Available: ${!SKILLS[@]}" >&2
    exit 1
  fi
fi
