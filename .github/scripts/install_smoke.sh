#!/usr/bin/env bash
# Install smoke test: prove the catalog actually installs with the real
# Claude Code tooling, not just that the files look right.
#
#   1. `claude plugin validate . --strict`  — the loader's own manifest check
#   2. `marketplace add ./`                 — register this repo as a marketplace
#   3. for each LOCAL plugin: `install` it, then `details` it and assert it
#      exposes at least one component (i.e. the SKILL.md was recognized, not
#      just copied).
#
# Runs against an isolated HOME so it never touches a real ~/.claude.
# Needs no auth: plugin management is auth-free. `claude` must be on PATH.
#
#   Usage: .github/scripts/install_smoke.sh [repo_root]
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

ISO="$(mktemp -d "${RUNNER_TEMP:-/tmp}/iso-claude.XXXXXX")"
export HOME="$ISO"
trap 'rm -rf "$ISO"' EXIT

MP=".claude-plugin/marketplace.json"
MKT="$(python3 -c "import json;print(json.load(open('$MP'))['name'])")"
PLUGINS=()
while IFS= read -r line; do
  [ -n "$line" ] && PLUGINS+=("$line")
done < <(python3 -c "
import json
for p in json.load(open('$MP')).get('plugins', []):
    if isinstance(p.get('source'), str):  # local skill; remote ones live elsewhere
        print(p['name'])
")

# Gate on plain validate (real defects only). --strict additionally nags on
# unrecognized fields, which is the one place validate can false-positive on a
# harmless PR, so it runs as an advisory warning, not a blocker.
echo "::group::claude plugin validate . (gate)"
claude plugin validate .
echo "::endgroup::"

echo "::group::claude plugin validate . --strict (advisory)"
claude plugin validate . --strict \
  || echo "::warning::strict validation found issues (advisory, not blocking)"
echo "::endgroup::"

echo "::group::marketplace add"
claude plugin marketplace add ./
echo "marketplace='$MKT'  local plugins: ${PLUGINS[*]:-<none>}"
echo "::endgroup::"

if [ "${#PLUGINS[@]}" -eq 0 ]; then
  echo "no local plugins to install"; exit 0
fi

fail=0
for p in "${PLUGINS[@]}"; do
  echo "::group::install $p"
  if ! claude plugin install "$p@$MKT" --scope user; then
    echo "::error::install failed for $p@$MKT"
    fail=1; echo "::endgroup::"; continue
  fi
  details="$(claude plugin details "$p@$MKT" 2>&1 || true)"
  echo "$details"
  # Component inventory prints e.g. "Skills (1)". Require a nonzero count.
  if ! printf '%s\n' "$details" | grep -qE '\([1-9][0-9]*\)'; then
    echo "::error::$p installed but exposes no components (SKILL.md not recognized?)"
    fail=1
  fi
  echo "::endgroup::"
done

if [ "$fail" -ne 0 ]; then
  echo "install smoke test FAILED"
  exit 1
fi
echo "install smoke test OK — ${#PLUGINS[@]} plugin(s) installed and recognized"
