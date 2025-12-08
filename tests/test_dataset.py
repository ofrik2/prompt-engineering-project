from prompt_lab.dataset.generator import generate_dummy_tasks, build_prompt_variants


def test_generate_dummy_tasks_basic():
    tasks = generate_dummy_tasks()

    # We expect exactly 3 tasks for now
    assert len(tasks) == 3

    # Check that the IDs we defined exist
    ids = {t.id for t in tasks}
    assert "sentiment_1" in ids
    assert "math_1" in ids
    assert "logic_1" in ids


def test_build_prompt_variants_creates_three_lengths_per_task():
    tasks = generate_dummy_tasks()
    variants = build_prompt_variants(tasks)

    # For each task we create 3 variants: short, medium, long
    assert len(variants) == len(tasks) * 3

    lengths = {v.length for v in variants}
    assert lengths == {"short", "medium", "long"}
