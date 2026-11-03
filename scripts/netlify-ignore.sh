#!/usr/bin/env bash
# Netlify: exit 0 = skip deploy, exit 1 = deploy.
# Only skip commits created by our scheduled data sync.
set -u
sha="${COMMIT_REF:-HEAD}"
message="$(git show -s --format=%s "$sha" 2>/dev/null || true)"
if [[ "$message" == "chore: sync public LeetCode data" ]]; then
  echo "Skipping Netlify deployment for data-only sync. The frontend reads GitHub JSON directly."
  exit 0
fi
echo "Code/config update detected; run production deployment."
exit 1
