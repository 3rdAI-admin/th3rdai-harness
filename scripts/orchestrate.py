#!/usr/bin/env python3
"""Native orchestrator CLI (dry-run coordinator).

Wraps the sequencer and eval hook. `route` assembles per-step context bundles and
writes dry-run run records; `eval` pairs a case with its rubric and scaffolds a
PENDING result + run record. No model/network calls and no dependencies — the
opt-in `--execute` mode is specified for Phase 04.

Run from the repo root:
    python3 scripts/orchestrate.py route iteration
    python3 scripts/orchestrate.py eval evals/cases/planning/basic-feature-plan.md
"""
import argparse
import sys
from pathlib import Path

# Put the repo root on sys.path so `scripts.orchestrator` imports regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.orchestrator import evalhook, sequencer  # noqa: E402


def _cmd_route(args) -> int:
    results = sequencer.dry_run(args.name, runs_dir=args.runs_dir)
    for bundle, _record, path in results:
        print(bundle.render())
        print(f"  -> run record: {path}\n")
    print(f"{len(results)} dry-run step record(s) written under {args.runs_dir}/")
    return 0


def _cmd_eval(args) -> int:
    out = evalhook.run_eval(
        args.case, rubric=args.rubric,
        results_dir=args.results_dir, runs_dir=args.runs_dir,
    )
    print("Eval scaffolded (PENDING — Evaluator to complete):")
    print(f"  case        : {args.case}")
    print(f"  rubric      : {out['rubric']}")
    print(f"  criteria    : {len(out['criteria'])}")
    print(f"  result stub : {out['result']}")
    print(f"  run record  : {out['run_record']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orchestrate",
        description="Native orchestrator — dry-run coordinator (no model/network calls).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    route = sub.add_parser(
        "route", help="Sequence a lifecycle route into per-step context bundles (dry-run)."
    )
    route.add_argument("name", help="route name from configs/routing.yaml")
    route.add_argument(
        "--dry-run", action="store_true",
        help="explicit dry-run; the only mode in this phase (pairs with --execute in Phase 04)",
    )
    route.add_argument("--runs-dir", default="runs", help="directory for run records (default: runs)")
    route.set_defaults(func=_cmd_route)

    ev = sub.add_parser(
        "eval", help="Pair an eval case with its rubric and scaffold a PENDING result."
    )
    ev.add_argument("case", help="path to an evals/cases/*/*.md file")
    ev.add_argument("--rubric", default=None,
                    help="override rubric path (else resolved from the case's ## Rubric reference)")
    ev.add_argument("--results-dir", default="evals/results")
    ev.add_argument("--runs-dir", default="runs")
    ev.set_defaults(func=_cmd_eval)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (sequencer.SequencerError, evalhook.EvalHookError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
