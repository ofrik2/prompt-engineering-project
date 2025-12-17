"""
Configuration loading utilities.

This module knows how to:
- locate the default config file (config/default.yaml)
- parse it
- expose it as simple Python dataclasses

It also supports environment overrides so the project can be used as a CLI tool
without editing YAML files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import os
import yaml

from prompt_lab.methods.fewshot import FewShotExample


# ---------- Data classes ----------

@dataclass
class ModelConfig:
    provider: str
    model_name: str
    temperature: float
    max_tokens: int


@dataclass
class ExperimentConfig:
    name: str
    methods: List[str]
    dataset: str          # "dummy" or "file"
    dataset_path: str     # used when dataset == "file"
    output_dir: str


@dataclass
class AppConfig:
    model: ModelConfig
    experiment: ExperimentConfig
    fewshot_examples: List[FewShotExample]


# ---------- Loader functions ----------

def get_project_root() -> Path:
    """
    Return the project root directory (the folder that contains `src/` and `config/`).

    This assumes this file lives under: src/prompt_lab/config/loader.py
    """
    # loader.py -> config -> prompt_lab -> src -> PROJECT_ROOT
    return Path(__file__).resolve().parents[3]


def get_default_config_path() -> Path:
    """Return the config path.

    Priority:
      1) PROMPT_LAB_CONFIG env var (absolute or relative to project root)
      2) <project_root>/config/default.yaml
    """
    env_path = os.getenv("PROMPT_LAB_CONFIG")
    if env_path:
        p = Path(env_path)
        if not p.is_absolute():
            p = get_project_root() / p
        return p
    return get_project_root() / "config" / "default.yaml"


def load_config(path: Path | None = None) -> AppConfig:
    """
    Load configuration from a YAML file.

    If `path` is None, use config/default.yaml (or PROMPT_LAB_CONFIG override).
    """
    if path is None:
        path = get_default_config_path()

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # ----- model -----
    model_raw = raw.get("model", {})
    model_cfg = ModelConfig(
        provider=str(model_raw.get("provider", "")),
        model_name=str(model_raw.get("model_name", "")),
        temperature=float(model_raw.get("temperature", 0.0)),
        max_tokens=int(model_raw.get("max_tokens", 0)),
    )

    # ----- experiment -----
    experiment_raw = raw.get("experiment", {})
    experiment_cfg = ExperimentConfig(
        name=str(experiment_raw.get("name", "")),
        methods=list(experiment_raw.get("methods", [])),
        dataset=str(experiment_raw.get("dataset", "")),
        dataset_path=str(experiment_raw.get("dataset_path", "")),
        output_dir=str(experiment_raw.get("output_dir", "results")),
    )

    # ----- env overrides (optional) -----
    # These allow running the package from CLI without editing YAML.
    provider_override = os.getenv("PROMPT_LAB_PROVIDER")
    if provider_override:
        model_cfg.provider = provider_override

    dataset_path_override = os.getenv("PROMPT_LAB_DATASET_PATH")
    if dataset_path_override:
        # Force "file" dataset when user supplies a path override
        experiment_cfg.dataset = "file"
        experiment_cfg.dataset_path = dataset_path_override

    output_dir_override = os.getenv("PROMPT_LAB_OUTPUT_DIR")
    if output_dir_override:
        experiment_cfg.output_dir = output_dir_override

    # ----- few-shot examples (optional) -----
    fewshot_raw = raw.get("fewshot_examples", [])
    fewshot_examples: List[FewShotExample] = []
    for ex in fewshot_raw:
        fewshot_examples.append(
            FewShotExample(
                input_text=str(ex["input"]),
                output_text=str(ex["output"]),
            )
        )

    return AppConfig(
        model=model_cfg,
        experiment=experiment_cfg,
        fewshot_examples=fewshot_examples,
    )
