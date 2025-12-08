from prompt_lab.config.loader import load_config, get_default_config_path


def main() -> None:
    cfg = load_config()
    print("Loaded config from:", get_default_config_path())
    print("--- Model ---")
    print("provider  :", cfg.model.provider)
    print("model_name:", cfg.model.model_name)
    print("temperature:", cfg.model.temperature)
    print("max_tokens:", cfg.model.max_tokens)
    print("--- Experiment ---")
    print("name      :", cfg.experiment.name)
    print("methods   :", cfg.experiment.methods)
    print("dataset   :", cfg.experiment.dataset)
    print("output_dir:", cfg.experiment.output_dir)


if __name__ == "__main__":
    main()
