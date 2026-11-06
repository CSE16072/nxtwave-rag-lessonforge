import json
from pathlib import Path
from datetime import datetime


# Define the output folder
OUTPUT_DIR = Path("outputs")


def save_output(state):
    """
    Save the final lesson, evaluation, and rejection log.
    """

    # Create the outputs folder if it does not exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create a unique filename using the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    markdown_path = OUTPUT_DIR / f"lesson_{timestamp}.md"
    json_path = OUTPUT_DIR / f"lesson_{timestamp}.json"

    # Get information from the final workflow state
    topic = state.get("topic", "Unknown Topic")
    lesson = state.get("lesson", "")
    status = state.get("status", "UNKNOWN")
    attempts = state.get("retry_count", 0)
    evaluation = state.get("evaluation", {})
    rejection_log = state.get("rejection_log", [])

    # Build the Markdown report
    markdown_content = f"""# RAG LessonForge Report

## Topic
{topic}

## Final Status
{status}

## Number of Attempts
{attempts}

## Generated Lesson

{lesson}

## Evaluation Results
"""

    # Add each evaluation criterion to the report
    for criterion, details in evaluation.items():

        if criterion == "passed":
            continue

        markdown_content += f"""
### {criterion.replace("_", " ").title()}

- **Status:** {details["status"]}
- **Reason:** {details["reason"]}
- **Suggestion:** {details["suggestion"]}
"""

    # Add the rejection history
    markdown_content += "\n## Rejection Log\n"

    if rejection_log:

        for rejection in rejection_log:

            markdown_content += (
                f"\n### Attempt {rejection['attempt']}\n"
            )

            for failure in rejection["failures"]:

                markdown_content += f"""
- **Criterion:** {failure["criterion"]}
- **Reason:** {failure["reason"]}
- **Suggestion:** {failure["suggestion"]}
"""

    else:
        markdown_content += "\nNo rejected attempts.\n"

    # Save the Markdown report
    markdown_path.write_text(
        markdown_content,
        encoding="utf-8",
    )

    # Build the JSON report
    json_content = {
        "topic": topic,
        "status": status,
        "attempts": attempts,
        "lesson": lesson,
        "evaluation": evaluation,
        "rejection_log": rejection_log,
    }

    # Save the JSON report
    json_path.write_text(
        json.dumps(
            json_content,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("\n--- OUTPUT FILES SAVED ---")
    print(f"Markdown: {markdown_path}")
    print(f"JSON: {json_path}")

    return {
        "markdown_path": str(markdown_path),
        "json_path": str(json_path),
    }


if __name__ == "__main__":

    # Simple test of the output folder
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Output folder is ready!")
    print(f"Folder location: {OUTPUT_DIR.resolve()}")