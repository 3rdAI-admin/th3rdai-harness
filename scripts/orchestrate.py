#!/usr/bin/env python3
"""Native orchestrator CLI.

Wraps the sequencer, eval hook, and execution driver. `route` assembles per-step
context bundles and writes dry-run run records by default; `route --execute` runs
each step through an adapter (opt-in, approval-gated). `eval` pairs a case with
its rubric and scaffolds a PENDING result + run record. The default path makes no
model/network calls and has no dependencies; execution is opt-in via `--execute`.

Run from the repo root:
    python3 scripts/orchestrate.py route iteration
    python3 scripts/orchestrate.py route release --execute --adapter cli --yes
    python3 scripts/orchestrate.py eval evals/cases/planning/basic-feature-plan.md
"""
import argparse
import sys
from pathlib import Path

# Put the repo root on sys.path so `scripts.orchestrator` imports regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.orchestrator import adapter as adapter_mod  # noqa: E402
from scripts.orchestrator import config, driver, evalhook, sequencer  # noqa: E402


def _safe_prompt(message: str) -> str:
    """Prompt that treats EOF (unattended stdin) as a decline, never a crash."""
    try:
        return input(message)
    except EOFError:
        return ""


def _load_execution_cfg() -> dict:
    if not (config.repo_root() / "configs" / "execution.yaml").exists():
        return {}
    doc = config.load_yaml("configs/execution.yaml") or {}
    return doc.get("execution", {}) or {}


def _build_adapter(args):
    choice = args.adapter or _load_execution_cfg().get("default_adapter", "noop")
    if choice == "noop":
        return adapter_mod.NoopAdapter()
    if choice == "cli":
        cli = _load_execution_cfg().get("cli", {}) or {}
        command = cli.get("command", []) or []
        if not command:
            raise adapter_mod.AdapterError(
                "--adapter cli needs a command in configs/execution.yaml "
                "(cli.command); configure one or use --adapter noop"
            )
        allowlist = cli.get("env_allowlist", []) or []
        return adapter_mod.CliAdapter(
            command,
            timeout=float(cli.get("timeout_seconds", 120)),
            env_allowlist=allowlist,
        )
    raise adapter_mod.AdapterError(f"unknown adapter '{choice}'")


def _cmd_route(args) -> int:
    if not args.execute:
        results = sequencer.dry_run(args.name, runs_dir=args.runs_dir)
        for bundle, _record, path in results:
            print(bundle.render())
            print(f"  -> run record: {path}\n")
        print(f"{len(results)} dry-run step record(s) written under {args.runs_dir}/")
        return 0

    adapter = _build_adapter(args)
    results = driver.execute_route(
        args.name, adapter, runs_dir=args.runs_dir,
        max_steps=args.max_steps, assume_yes=args.yes,
        autonomy_mode=args.autonomy, prompt_fn=_safe_prompt,
    )
    for step, result, _record, path in results:
        print(f"  step {step.order} {step.agent}: {result.status} -> {path}")
    print(f"executed/recorded {len(results)} step(s) with adapter '{adapter.name}'")
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
        "route", help="Sequence a lifecycle route into per-step context bundles."
    )
    route.add_argument("name", help="route name from configs/routing.yaml")
    route.add_argument(
        "--dry-run", action="store_true",
        help="explicit dry-run (the default); assembles bundles, invokes nothing",
    )
    route.add_argument(
        "--execute", action="store_true",
        help="opt-in: run each step through an adapter (approval-gated); default is dry-run",
    )
    route.add_argument(
        "--adapter", choices=["cli", "noop"], default=None,
        help="adapter for --execute (default: execution.yaml default_adapter, else noop)",
    )
    route.add_argument(
        "--max-steps", type=int, default=None,
        help="cap the number of steps executed (runaway guard)",
    )
    route.add_argument(
        "--yes", action="store_true",
        help="skip the per-step checkpoint; tools.yaml + protected-write gates still apply",
    )
    route.add_argument(
        "--autonomy",
        choices=["ask", "cautious", "full"],
        default=None,
        help="autonomy mode (ask=approve all, cautious=auto LOW/MEDIUM, full=auto all); overrides configs/autonomy.yaml",
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
    except (sequencer.SequencerError, evalhook.EvalHookError, adapter_mod.AdapterError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
