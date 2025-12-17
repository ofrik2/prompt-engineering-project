from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _find_project_root() -> Path:
    """
    Try to locate the repository root.

    We look upwards from this file until we find:
      - config/default.yaml
      - src/
    This works for a cloned repo and editable installs.
    """
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "config" / "default.yaml").exists() and (p / "src").exists():
            return p
    # Fallback: current working directory
    return Path.cwd()


def _set_override_env(
    config: str | None,
    provider: str | None,
    dataset_path: str | None,
    output_dir: str | None,
) -> None:
    if config:
        os.environ["PROMPT_LAB_CONFIG"] = config
    if provider:
        os.environ["PROMPT_LAB_PROVIDER"] = provider
    if dataset_path:
        os.environ["PROMPT_LAB_DATASET_PATH"] = dataset_path
    if output_dir:
        os.environ["PROMPT_LAB_OUTPUT_DIR"] = output_dir


def _run_script(project_root: Path, script_rel_path: str) -> int:
    script_path = project_root / script_rel_path
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}", file=sys.stderr)
        return 2
    cmd = [sys.executable, str(script_path)]
    return subprocess.call(cmd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="prompt-lab",
        description="Prompt Engineering project runner",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common_flags(p: argparse.ArgumentParser) -> None:
        p.add_argument("--config", help="Path to YAML config (defaults to config/default.yaml)")
        p.add_argument("--provider", choices=["dummy", "azure"], help="Override model.provider")
        p.add_argument("--dataset-path", help="Override experiment.dataset_path (forces dataset=file)")
        p.add_argument("--output-dir", help="Override experiment.output_dir")

    p_full = sub.add_parser("full", help="Run full pipeline: experiments + analysis + HTML report")
    add_common_flags(p_full)

    p_run_all = sub.add_parser("run-all", help="Run all experiments and write raw predictions")
    add_common_flags(p_run_all)

    p_baseline = sub.add_parser("baseline", help="Run baseline experiment only")
    add_common_flags(p_baseline)

    p_cot = sub.add_parser("cot", help="Run chain-of-thought experiment only")
    add_common_flags(p_cot)

    p_few = sub.add_parser("fewshot", help="Run few-shot experiment only")
    add_common_flags(p_few)

    p_analyze = sub.add_parser("analyze", help="Run analysis scripts without rerunning LLM calls")
    add_common_flags(p_analyze)

    p_report = sub.add_parser("report", help="Generate HTML report only")
    add_common_flags(p_report)

    args = parser.parse_args(argv)
    project_root = _find_project_root()

    # Normalize relative config path to repo root (so users can pass "config/default.yaml")
    config_path = args.config
    if config_path:
        cp = Path(config_path)
        if not cp.is_absolute():
            config_path = str((project_root / cp).resolve())

    dataset_path = args.dataset_path
    if dataset_path:
        dp = Path(dataset_path)
        if not dp.is_absolute():
            dataset_path = str((Path.cwd() / dp).resolve())

    output_dir = args.output_dir
    if output_dir:
        od = Path(output_dir)
        if not od.is_absolute():
            output_dir = str((Path.cwd() / od).resolve())

    _set_override_env(config_path, args.provider, dataset_path, output_dir)

    if args.command == "full":
        return _run_script(project_root, "src/run_full_pipeline.py")
    if args.command == "run-all":
        return _run_script(project_root, "src/run_all_experiments.py")
    if args.command == "baseline":
        return _run_script(project_root, "src/run_baseline_experiment.py")
    if args.command == "cot":
        return _run_script(project_root, "src/run_cot_experiment.py")
    if args.command == "fewshot":
        return _run_script(project_root, "src/run_fewshot_experiment.py")
    if args.command == "analyze":
        # Same analysis sequence as the pipeline (minus the experiment runs)
        for rel in [
            "src/analysis/analyze_prompt_variation.py",
            "src/analysis/compare_methods_per_task.py",
            "src/analysis/analyze_cot_overthinking.py",
            "src/analysis/analyze_fewshot_effect.py",
        ]:
            rc = _run_script(project_root, rel)
            if rc != 0:
                return rc
        return 0
    if args.command == "report":
        return _run_script(project_root, "src/analysis/generate_html_report.py")

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
