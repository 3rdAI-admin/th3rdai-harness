#!/usr/bin/env bash
# worktree.sh — portable temporary-worktree isolation for harness builds.
#
# WHY: the Builder implements code and multi-file changes in an ISOLATED git
# worktree on a feature branch, never in the live/shared checkout. Two agents (or
# a build that fails validation) then cannot collide in one working tree, and the
# shared main tree stays clean. The branch outlives the worktree, so a human can
# review and merge it; cleanup removes only the temporary directory, never the work.
#
# USAGE
#   Source it (skills/agents):
#     source scripts/worktree.sh
#     wt="$(wt_create my-change)"   # stdout = the worktree path (nothing else)
#     cd "$wt"                      # ...implement + validate here...
#     wt_cleanup "$wt"             # remove the temp dir; the branch ref remains
#
#   Or as a CLI:
#     scripts/worktree.sh create <slug>     # prints the worktree path
#     scripts/worktree.sh cleanup <path>    # removes that worktree
#     scripts/worktree.sh list              # git worktree list
#
# PORTABILITY / GRACEFUL DEGRADATION
#   - bash 3.2 (stock macOS) compatible; no associative arrays, no mapfile.
#   - In a NON-git project (the harness is served into many kinds of repo),
#     wt_create prints the current repo root to stdout and a notice to stderr,
#     then returns 0 — the caller proceeds in place. Isolation is best-effort,
#     never a hard blocker for projects that cannot provide it.
#   - All human-facing text goes to stderr; stdout carries ONLY the path, so
#     `cd "$(wt_create ...)"` is safe.
#
# ENV
#   HARNESS_WT_BASE   where worktree directories are created
#                     (default: a sibling "<repo>-worktrees/" next to the repo).

# Guard against double-sourcing (idempotent function defs are fine, but skip the
# strict-mode toggle so sourcing never changes the caller's shell options).
if [ -z "${__WT_SOURCED:-}" ]; then
  __WT_SOURCED=1
fi

# --- internals -----------------------------------------------------------------

_wt_err() { printf '%s\n' "$*" >&2; }

_wt_abspath() {
  # Resolve a directory to its physical path (follows symlinks like /var -> /private/var
  # on macOS) so path comparisons are reliable. Falls back to the input unchanged.
  if [ -d "$1" ]; then (cd "$1" 2>/dev/null && pwd -P) || printf '%s' "$1"; else printf '%s' "$1"; fi
}

_wt_repo_root() {
  # Echo the git top-level, or empty + nonzero when not in a work tree.
  git rev-parse --show-toplevel 2>/dev/null
}

_wt_slugify() {
  # Lowercase; keep [a-z0-9-]; collapse the rest to '-'; trim; cap length.
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | tr -c 'a-z0-9-' '-' \
    | sed -e 's/-\{2,\}/-/g' -e 's/^-//' -e 's/-$//' \
    | cut -c1-40
}

# --- public API ----------------------------------------------------------------

# wt_create [slug] — create an isolated worktree on a new feature branch.
# Echoes the worktree path on stdout. In a non-git project, echoes the repo root
# (no isolation) and warns on stderr. Returns 0 on success or benign degradation,
# nonzero only on a real git failure the caller should surface.
wt_create() {
  local slug raw_slug root base ts branch path n
  raw_slug="${1:-build}"
  slug="$(_wt_slugify "$raw_slug")"
  [ -n "$slug" ] || slug="build"

  # `|| true`: under CLI strict mode (set -e) a failed capture must not abort before
  # the graceful-degradation check below runs.
  root="$(_wt_repo_root || true)"
  if [ -z "$root" ]; then
    _wt_err "worktree.sh: not a git repository — proceeding IN PLACE (no isolation)."
    pwd
    return 0
  fi

  ts="$(date +%Y%m%d-%H%M%S)"
  base="${HARNESS_WT_BASE:-$(dirname "$root")/$(basename "$root")-worktrees}"
  mkdir -p "$base" 2>/dev/null || {
    _wt_err "worktree.sh: cannot create worktree base $base — proceeding IN PLACE."
    printf '%s\n' "$root"
    return 0
  }

  branch="harness/wt-${slug}-${ts}"
  path="${base}/wt-${slug}-${ts}"
  # Collision-proof the names if two runs land in the same second.
  n=1
  while git show-ref --verify --quiet "refs/heads/${branch}" || [ -e "$path" ]; do
    branch="harness/wt-${slug}-${ts}-${n}"
    path="${base}/wt-${slug}-${ts}-${n}"
    n=$((n + 1))
  done

  if git worktree add -b "$branch" "$path" HEAD >&2; then
    _wt_err "worktree.sh: isolated work in $path (branch $branch, from $(git rev-parse --short HEAD))."
    _wt_err "worktree.sh: implement + validate there; a human reviews/merges the branch to main."
    printf '%s\n' "$path"
    return 0
  fi
  _wt_err "worktree.sh: 'git worktree add' failed — NOT proceeding in place (surface this)."
  return 1
}

# wt_cleanup <path> — remove a worktree created by wt_create. The branch ref and
# its commits persist (the work is NOT lost); only the temporary directory goes.
# Never run against the primary checkout.
wt_cleanup() {
  local path primary
  path="${1:-}"
  if [ -z "$path" ]; then
    _wt_err "worktree.sh: wt_cleanup needs a path"
    return 2
  fi
  # Resolve the primary worktree (first line of `git worktree list`) and compare by
  # PHYSICAL path — macOS mktemp yields /var/... while git reports /private/var/...,
  # so a raw string compare would miss the guard.
  primary="$(git worktree list --porcelain 2>/dev/null | sed -n 's/^worktree //p' | head -1)"
  if [ -n "$primary" ] && [ "$(_wt_abspath "$path")" = "$(_wt_abspath "$primary")" ]; then
    _wt_err "worktree.sh: refusing to remove the PRIMARY checkout ($path)"
    return 2
  fi
  if git worktree remove --force "$path" 2>/dev/null; then
    git worktree prune 2>/dev/null || true
    _wt_err "worktree.sh: removed $path (its branch ref remains for review/merge)."
    return 0
  fi
  _wt_err "worktree.sh: '$path' was not a removable worktree (already gone?) — pruning."
  git worktree prune 2>/dev/null || true
  return 0
}

wt_list() { git worktree list; }

wt_help() {
  sed -n '2,40p' "${BASH_SOURCE[0]:-$0}" | sed 's/^# \{0,1\}//'
}

# --- CLI dispatch (only when executed, not when sourced) -----------------------

# Only when executed by bash (not sourced, and not sourced into another shell such as
# zsh, where BASH_SOURCE is unset and the comparison would misfire).
if [ -n "${BASH_VERSION:-}" ] && [ "${BASH_SOURCE[0]}" = "$0" ]; then
  set -euo pipefail
  cmd="${1:-help}"
  shift || true
  case "$cmd" in
    create)  wt_create "$@" ;;
    cleanup) wt_cleanup "$@" ;;
    list)    wt_list ;;
    help|-h|--help) wt_help ;;
    *) _wt_err "worktree.sh: unknown command '$cmd' (create|cleanup|list|help)"; exit 2 ;;
  esac
fi
