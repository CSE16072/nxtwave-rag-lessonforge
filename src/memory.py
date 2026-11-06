import sqlite3
from datetime import datetime, timezone


# Name of the database file
DATABASE_NAME = "lessonforge_memory.db"


def create_memory_table():
    """
    Create a table to store lesson evaluation failures.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            criterion TEXT NOT NULL,
            reason TEXT NOT NULL,
            suggestion TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_evaluation(topic, evaluation):
    """
    Save failed evaluation criteria into the database.
    """

    create_memory_table()

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    current_time = datetime.now(timezone.utc).isoformat()

    # Check each evaluation criterion
    for criterion, details in evaluation.items():

        # Skip the final overall result
        if criterion == "passed":
            continue

        # Save only failed criteria
        if details["status"] == "FAIL":

            cursor.execute(
                """
                INSERT INTO evaluation_memory
                (topic, criterion, reason, suggestion, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    topic,
                    criterion,
                    details["reason"],
                    details["suggestion"],
                    current_time,
                ),
            )

    connection.commit()
    connection.close()


def get_repeated_failures(min_occurrences=2):
    """
    Find criteria that failed repeatedly in previous evaluations.
    """

    create_memory_table()

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            criterion,
            COUNT(*) AS failure_count,
            GROUP_CONCAT(suggestion, ' | ') AS suggestions
        FROM evaluation_memory
        GROUP BY criterion
        HAVING COUNT(*) >= ?
        ORDER BY failure_count DESC
        """,
        (min_occurrences,),
    )

    rows = cursor.fetchall()

    connection.close()

    # Convert database rows into a list of dictionaries
    repeated_failures = []

    for row in rows:

        repeated_failures.append(
            {
                "criterion": row[0],
                "failure_count": row[1],
                "suggestions": row[2],
            }
        )

    return repeated_failures


def get_all_failures():
    """
    Retrieve all saved evaluation failures.
    """

    create_memory_table()

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT topic, criterion, reason, suggestion, created_at
        FROM evaluation_memory
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


if __name__ == "__main__":

    # Create the memory table
    create_memory_table()

    print("Memory database created successfully!")

    # Display previously saved failures
    failures = get_all_failures()

    print("\n--- SAVED EVALUATION FAILURES ---")

    if failures:

        for failure in failures:
            print(f"\nTopic: {failure[0]}")
            print(f"Criterion: {failure[1]}")
            print(f"Reason: {failure[2]}")
            print(f"Suggestion: {failure[3]}")
            print(f"Saved at: {failure[4]}")

    else:
        print("No evaluation failures have been saved yet.")
