import src.graph as graph


def make_evaluation(passed):
    """
    Create a sample evaluation result for testing.
    """

    status = "PASS" if passed else "FAIL"

    evaluation = {
        "technical_accuracy": {
            "status": "PASS",
            "reason": "The lesson is technically accurate.",
            "suggestion": "None.",
        },
        "beginner_friendly": {
            "status": "PASS",
            "reason": "The language is simple.",
            "suggestion": "None.",
        },
        "practical_example": {
            "status": "PASS",
            "reason": "A useful example is included.",
            "suggestion": "None.",
        },
        "jargon_control": {
            "status": "PASS",
            "reason": "Technical terms are explained.",
            "suggestion": "None.",
        },
        "key_coverage": {
            "status": status,
            "reason": (
                "RAG limitations are missing."
                if not passed
                else "All important points are covered."
            ),
            "suggestion": (
                "Add a section about RAG limitations."
                if not passed
                else "None."
            ),
        },
        "teaching_flow": {
            "status": "PASS",
            "reason": "The lesson follows a clear order.",
            "suggestion": "None.",
        },
        "passed": passed,
    }

    return evaluation


def test_graph_retries_after_failure(monkeypatch):
    """
    Check that the graph retries after a failed evaluation.
    """

    generation_count = 0
    evaluation_count = 0

    def fake_generate_lesson(topic, learner_profile, feedback):
        nonlocal generation_count

        generation_count += 1

        return f"Generated lesson attempt {generation_count}"

    def fake_evaluate_lesson(topic, learner_profile, lesson):
        nonlocal evaluation_count

        evaluation_count += 1

        # First attempt fails, second attempt passes
        if evaluation_count == 1:
            return make_evaluation(False)

        return make_evaluation(True)

    # Replace real API calls with our test functions
    monkeypatch.setattr(
        graph,
        "generate_lesson",
        fake_generate_lesson,
    )

    monkeypatch.setattr(
        graph,
        "evaluate_lesson",
        fake_evaluate_lesson,
    )

    # Prevent tests from writing to the real memory database
    monkeypatch.setattr(
        graph,
        "save_evaluation",
        lambda topic, evaluation: None,
    )

    monkeypatch.setattr(
        graph,
        "get_repeated_failures",
        lambda: [],
    )

    initial_state = {
        "topic": "Introduction to RAG",
        "learner_profile": "A beginner learner.",
        "retry_count": 0,
        "rejection_log": [],
        "status": "STARTED",
    }

    result = graph.lesson_graph.invoke(initial_state)

    assert result["status"] == "PASS"
    assert result["retry_count"] == 2
    assert len(result["rejection_log"]) == 1

    assert generation_count == 2
    assert evaluation_count == 2


def test_graph_stops_after_max_attempts(monkeypatch):
    """
    Check that the graph stops after three failed attempts.
    """

    generation_count = 0

    def fake_generate_lesson(topic, learner_profile, feedback):
        nonlocal generation_count

        generation_count += 1

        return f"Generated lesson attempt {generation_count}"

    def fake_evaluate_lesson(topic, learner_profile, lesson):
        # Every attempt fails
        return make_evaluation(False)

    monkeypatch.setattr(
        graph,
        "generate_lesson",
        fake_generate_lesson,
    )

    monkeypatch.setattr(
        graph,
        "evaluate_lesson",
        fake_evaluate_lesson,
    )

    monkeypatch.setattr(
        graph,
        "save_evaluation",
        lambda topic, evaluation: None,
    )

    monkeypatch.setattr(
        graph,
        "get_repeated_failures",
        lambda: [],
    )

    initial_state = {
        "topic": "Introduction to RAG",
        "learner_profile": "A beginner learner.",
        "retry_count": 0,
        "rejection_log": [],
        "status": "STARTED",
    }

    result = graph.lesson_graph.invoke(initial_state)

    assert result["status"] == "FAIL"
    assert result["retry_count"] == graph.MAX_ATTEMPTS

    assert generation_count == graph.MAX_ATTEMPTS
    assert len(result["rejection_log"]) == graph.MAX_ATTEMPTS
