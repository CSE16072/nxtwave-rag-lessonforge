import src.memory as memory


def test_create_memory_table(tmp_path, monkeypatch):
    """
    Check whether the memory table is created.
    """

    # Use a temporary database for this test
    database_path = tmp_path / "test_memory.db"

    monkeypatch.setattr(
        memory,
        "DATABASE_NAME",
        str(database_path),
    )

    # Create the table
    memory.create_memory_table()

    # Check whether the database file exists
    assert database_path.exists()


def test_save_failed_evaluation(tmp_path, monkeypatch):
    """
    Check whether failed evaluation results are saved.
    """

    database_path = tmp_path / "test_memory.db"

    monkeypatch.setattr(
        memory,
        "DATABASE_NAME",
        str(database_path),
    )

    evaluation = {
        "technical_accuracy": {
            "status": "PASS",
            "reason": "The lesson is accurate.",
            "suggestion": "None.",
        },
        "key_coverage": {
            "status": "FAIL",
            "reason": "The lesson does not explain limitations.",
            "suggestion": "Add a section about RAG limitations.",
        },
        "passed": False,
    }

    # Save the failed evaluation
    memory.save_evaluation(
        topic="Introduction to RAG",
        evaluation=evaluation,
    )

    # Read saved failures
    failures = memory.get_all_failures()

    # Only the failed criterion should be saved
    assert len(failures) == 1

    assert failures[0][1] == "key_coverage"


def test_get_repeated_failures(tmp_path, monkeypatch):
    """
    Check whether repeated failures are identified.
    """

    database_path = tmp_path / "test_memory.db"

    monkeypatch.setattr(
        memory,
        "DATABASE_NAME",
        str(database_path),
    )

    evaluation = {
        "key_coverage": {
            "status": "FAIL",
            "reason": "The lesson does not explain limitations.",
            "suggestion": "Add a section about RAG limitations.",
        },
        "passed": False,
    }

    # Save the same failure twice
    memory.save_evaluation(
        topic="Introduction to RAG",
        evaluation=evaluation,
    )

    memory.save_evaluation(
        topic="Introduction to RAG",
        evaluation=evaluation,
    )

    # Look for criteria that failed at least twice
    repeated_failures = memory.get_repeated_failures(
        min_occurrences=2
    )

    assert len(repeated_failures) == 1

    assert repeated_failures[0]["criterion"] == "key_coverage"

    assert repeated_failures[0]["failure_count"] == 2