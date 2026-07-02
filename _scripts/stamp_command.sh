#!/usr/bin/env bash
set -euo pipefail

stamp_path="$1"
shift

"$@"
mkdir -p "$(dirname "${stamp_path}")"
{
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  date -u '+completed_at: %Y-%m-%dT%H:%M:%SZ'
} > "${stamp_path}"
