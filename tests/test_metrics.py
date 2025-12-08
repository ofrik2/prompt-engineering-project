from prompt_lab.dataset.generator import generate_dummy_tasks
from prompt_lab.evaluator.metrics import compute_accuracy
from prompt_lab.methods.baseline import BaselineResult


def test_compute_accuracy_all_correct():
    tasks = generate_dummy_tasks()

    # Build predictions that exactly match the ground truth for each task
    predictions = [
        BaselineResult(
            task_id=t.id,
            prompt_length="short",
            prompt_text="",
            predicted_answer=t.ground_truth,
        )
        for t in tasks
    ]

    result = compute_accuracy(tasks, predictions)

    assert result.total == len(predictions)
    assert result.correct == len(predictions)
    assert result.accuracy == 1.0


def test_compute_accuracy_half_correct():
    tasks = generate_dummy_tasks()

    # Make predictions for each task, but only some of them correct
    predictions = []

    for i, t in enumerate(tasks):
        if i % 2 == 0:
            # even index -> correct
            pred = t.ground_truth
        else:
            # odd index -> wrong on purpose
            pred = "WRONG_ANSWER"

        predictions.append(
            BaselineResult(
                task_id=t.id,
                prompt_length="short",
                prompt_text="",
                predicted_answer=pred,
            )
        )

    result = compute_accuracy(tasks, predictions)

    assert result.total == len(predictions)
    # For 3 tasks, about half correct -> 2 correct if indices 0 and 2
    assert result.correct == 2
    assert abs(result.accuracy - (2 / 3)) < 1e-6
