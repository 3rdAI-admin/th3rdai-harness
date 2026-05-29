"""Approval-gate helpers for the opt-in execution adapter (Phase 04).

This module backs the safety model described in
``plans/native-orchestrator/04-execution-adapter.md``: even under ``--execute``
the orchestrator must keep certain actions human-gated, and it must refuse to
let a step rewrite the harness's own contracts/configs/code without approval.

It reads the ``requires_approval`` phrases from ``configs/tools.yaml`` (via
``config.load_tools``) and exposes pure helpers plus one interactive confirm.

Standard library only; absolute imports rooted at the repo root.
"""
from __future__ import annotations

from scripts.orchestrator import config


class GateError(Exception):
    """Raised for approval-gate misuse (reserved; not required by callers)."""


# Repo-relative path prefixes the adapter must not write to without approval.
# These cover the harness's own contracts (agents/*), policy/config (configs/*),
# and the orchestrator's own code (scripts/orchestrator/*) — the spec's
# "no self-modification without approval" guard.
PROTECTED_PREFIXES = ("agents/", "configs/", "scripts/orchestrator/")


def _norm(text: str) -> str:
    """Lowercase and collapse internal whitespace runs to single spaces."""
    return " ".join(str(text).split()).lower()


def _approval_phrases(policies: dict) -> list[str]:
    """All ``requires_approval`` phrases across every policy, in order."""
    phrases: list[str] = []
    if not isinstance(policies, dict):
        return phrases
    for policy in policies.values():
        if not isinstance(policy, dict):
            continue
        for phrase in policy.get("requires_approval", []) or []:
            phrases.append(phrase)
    return phrases


def requires_approval(action: str, policies: dict | None = None) -> bool:
    """Whether a free-text ``action`` needs human approval per tools.yaml.

    Matching rule (conservative — err toward flagging): after lowercasing and
    collapsing internal whitespace, an action matches a ``requires_approval``
    phrase if the phrase is a substring of the action OR the action is a
    substring of the phrase. Either containment direction counts.

    When ``policies is None`` the policies are loaded from
    ``config.load_tools().get("tool_policies", {})``.
    """
    if policies is None:
        policies = config.load_tools().get("tool_policies", {})
    a = _norm(action)
    if not a:
        return False
    for phrase in _approval_phrases(policies):
        p = _norm(phrase)
        if not p:
            continue
        if p in a or a in p:
            return True
    return False


def gated_actions(actions: list[str], policies: dict | None = None) -> list[str]:
    """Subset of ``actions`` that require approval, order-preserving, de-duped.

    Policies are loaded once (when ``policies is None``) and reused across all
    actions for efficiency.
    """
    if policies is None:
        policies = config.load_tools().get("tool_policies", {})
    result: list[str] = []
    seen: set[str] = set()
    for action in actions:
        if action in seen:
            continue
        if requires_approval(action, policies):
            seen.add(action)
            result.append(action)
    return result


def confirm(
    actions: list[str],
    assume_yes: bool = False,
    prompt_fn=input,
    out=print,
) -> bool:
    """Confirm any gated actions before proceeding.

    - If no actions are gated, return True without ever invoking ``prompt_fn``.
    - If ``assume_yes`` is set, note the auto-approved gated actions via ``out``
      and return True.
    - Otherwise call ``prompt_fn`` exactly once with a message listing the gated
      actions; return True only if the reply (stripped, lowercased) is ``y`` or
      ``yes``; otherwise False.
    """
    gated = gated_actions(actions)
    if not gated:
        return True
    listed = ", ".join(gated)
    if assume_yes:
        out(f"Auto-approving gated action(s): {listed}")
        return True
    reply = prompt_fn(
        f"The following action(s) require approval: {listed}. Proceed? [y/N] "
    )
    return str(reply).strip().lower() in ("y", "yes")


def protected_writes(paths: list[str], prefixes=PROTECTED_PREFIXES) -> list[str]:
    """Repo-relative ``paths`` that fall under a protected prefix.

    A leading ``./`` is normalized away before matching. Order is preserved and
    each matching path is returned once. Backs the spec's "no self-modification
    without approval" guard for writes to ``agents/*``, ``configs/*``, or
    ``scripts/orchestrator/*``.
    """
    result: list[str] = []
    for path in paths:
        norm = str(path)
        if norm.startswith("./"):
            norm = norm[2:]
        if norm.startswith(tuple(prefixes)):
            result.append(path)
    return result
