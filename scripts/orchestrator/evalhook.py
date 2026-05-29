"""Eval hook: pair an eval case with its rubric and scaffold a PENDING result
stub + run record for the Evaluator to complete.

Prepares context only — it never scores or invokes a model. Rubric resolution
mirrors the gate in ``scripts/07-validate-harness.sh`` (the same
``evals/rubrics/<name>.md`` reference pattern), so the CLI and the validator
agree on what a case's rubric is.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from scripts.orchestrator import config, runlog

_RUBRIC_REF = re.compile(r"evals/rubrics/[A-Za-z0-9._-]+\.md")
_CRITERION_SPLIT = re.compile(r"\s+[—–-]\s+")  # em / en dash or hyphen, spaced


class EvalHookError(ValueError):
    """Raised when a rubric cannot be resolved for an eval case."""


def _resolve_path(rel_or_abs: str) -> Path:
    p = Path(rel_or_abs)
    return p if p.is_absolute() else config.repo_root() / p


def _section_text(md_text: str, heading: str) -> str:
    target = f"## {heading}".lower()
    out, capturing = [], False
    for line in md_text.splitlines():
        if line.strip().lower().startswith("## "):
            if capturing:
                break
            capturing = line.strip().lower() == target
            continue
        if capturing:
            out.append(line)
    return "\n".join(out)


def resolve_rubric(case_path: str, explicit: Optional[str] = None) -> str:
    """Repo-relative rubric path for a case.

    Order: explicit ``--rubric`` > the case's ``## Rubric`` section reference >
    a unique reference anywhere in the case. Fails loudly otherwise.
    """
    if explicit:
        if not _resolve_path(explicit).exists():
            raise EvalHookError(f"--rubric path does not exist: {explicit}")
        return explicit

    text = _resolve_path(case_path).read_text(encoding="utf-8")
    section_refs = list(dict.fromkeys(_RUBRIC_REF.findall(_section_text(text, "Rubric"))))
    if section_refs:
        return section_refs[0]

    all_refs = list(dict.fromkeys(_RUBRIC_REF.findall(text)))
    if not all_refs:
        raise EvalHookError(
            f"no rubric referenced in {case_path}; add a '## Rubric' section or pass --rubric"
        )
    if len(all_refs) > 1:
        raise EvalHookError(
            f"multiple rubrics referenced in {case_path} ({', '.join(all_refs)}); pass --rubric"
        )
    return all_refs[0]


def rubric_criteria(rubric_path: str) -> list:
    """Criterion names from a rubric's ``## Criteria`` bullet list.

    Handles both plain (``- Goal clarity``) and emphasized
    (``- **Name** — description``) bullet styles.
    """
    text = _resolve_path(rubric_path).read_text(encoding="utf-8")
    criteria = []
    for line in _section_text(text, "Criteria").splitlines():
        s = line.strip()
        if s.startswith("- "):
            head = _CRITERION_SPLIT.split(s[2:].strip(), maxsplit=1)[0]
            name = head.replace("**", "").strip()
            if name:
                criteria.append(name)
    return criteria


def _render_stub(case_rel, rubric_rel, run_record_rel, criteria, now) -> str:
    rows = "\n".join(f"| {c} | | |" for c in criteria) or "| (no criteria parsed) | | |"
    total = f"{len(criteria) * 5}" if criteria else "?"
    return f"""# Eval Result: {Path(case_rel).stem} vs {Path(rubric_rel).stem}

- Status: **PENDING** — scaffolded by the orchestrator eval hook; Evaluator to complete.
- Case: `{case_rel}`
- Rubric: `{rubric_rel}`
- Run record: `{run_record_rel}`
- Created: {now.strftime('%Y-%m-%dT%H:%M:%SZ')}

## Evaluation Setup
- Artifact under test: <fill in>
- Eval case: {case_rel}
- Rubric: {rubric_rel}
- Model profile: <fill in or n/a>
- Prompt version: <fill in or n/a>

## Scores

| Criterion | Score (1-5) | Justification (cite output) |
|-----------|-------------|-----------------------------|
{rows}

Total: <aggregate> / {total}

## Findings
- severity: <high|medium|low>
  observation: <what the output did or missed>
  rubric_link: <criterion>
  recommendation: <specific revision>

## Verdict
<acceptable | needs revision | reject> — per the rubric's Pass Threshold.
"""


def run_eval(case_path: str, rubric: Optional[str] = None,
             results_dir: str = "evals/results", runs_dir: str = "runs",
             now: Optional[datetime] = None) -> dict:
    """Scaffold a PENDING result stub + run record. Returns a summary dict."""
    now = now or datetime.now(timezone.utc)
    root = config.repo_root()

    case_rel = case_path
    rubric_rel = resolve_rubric(case_path, rubric)
    criteria = rubric_criteria(rubric_rel)

    run_id = runlog.new_run_id(f"eval-{Path(case_rel).stem}", now=now)
    result_rel = f"{results_dir}/{run_id}.md"
    run_record_rel = f"{runs_dir}/{run_id}.md"

    stub = _render_stub(case_rel, rubric_rel, run_record_rel, criteria, now)
    result_path = _resolve_path(result_rel)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(stub, encoding="utf-8")

    record = runlog.RunRecord(
        run_id=run_id,
        created_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        request=f"Eval scaffold: {case_rel} against {rubric_rel}",
        agent="evaluator",
        skill="skills/eval/eval.md",
        inputs=[case_rel, rubric_rel],
        outputs=[result_rel],
        tool_actions=["assembled case + rubric bundle (eval hook; no scoring)"],
        validation={"status": "skipped", "notes": "eval hook scaffolded result; Evaluator to score"},
        evaluation={"rubric": rubric_rel, "score": None, "notes": "PENDING; Evaluator to complete"},
        follow_up=[f"Evaluator: score {result_rel} against the rubric, then record evaluation.score"],
    )
    record_path = runlog.write(record, dir=runs_dir)

    return {
        "result": result_path,
        "run_record": record_path,
        "rubric": rubric_rel,
        "criteria": criteria,
        "record": record,
    }
