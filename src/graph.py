from langgraph.graph import StateGraph, START, END

from src.state import LessonState
from src.generator import generate_lesson
from src.evaluator import evaluate_lesson
from src.memory import save_evaluation, get_repeated_failures


MAX_ATTEMPTS = 3


def generate_node(state: LessonState):
    """
    Generate or regenerate a lesson using previous feedback.
    """

    # Get the current attempt number
    attempt = state.get("retry_count", 0) + 1

    # Collect feedback from previous failed attempts
    rejection_log = state.get("rejection_log", [])

    feedback_parts = []

    for rejection in rejection_log:

        for failure in rejection["failures"]:

            feedback_parts.append(
                f"{failure['criterion']}: "
                f"{failure['reason']}. "
                f"Correction: {failure['suggestion']}"
            )

    # Add knowledge from repeated failures in memory
    repeated_failures = get_repeated_failures()

    for failure in repeated_failures:

        feedback_parts.append(
            f"Repeated issue: {failure['criterion']} "
            f"failed {failure['failure_count']} times before. "
            f"Please address it carefully. "
            f"Suggestions: {failure['suggestions']}"
        )

    # Prepare feedback for the lesson generator
    if feedback_parts:
        feedback = "\n".join(feedback_parts)
    else:
        feedback = "No previous feedback."

    # Generate the lesson
    lesson = generate_lesson(
        topic=state["topic"],
        learner_profile=state["learner_profile"],
        feedback=feedback,
    )

    print(f"\nLesson generated. Attempt: {attempt}")

    return {
        "lesson": lesson,
        "retry_count": attempt,
    }


def evaluate_node(state: LessonState):
    """
    Evaluate the lesson and save any failures.
    """

    evaluation = evaluate_lesson(
        topic=state["topic"],
        learner_profile=state["learner_profile"],
        lesson=state["lesson"],
    )

    # Save failed criteria into persistent memory
    save_evaluation(
        topic=state["topic"],
        evaluation=evaluation,
    )

    # Check whether the lesson passed
    if evaluation["passed"]:

        print("\nEvaluation result: PASS")

        return {
            "evaluation": evaluation,
            "status": "PASS",
        }

    # Collect failed criteria
    failures = []

    for criterion, details in evaluation.items():

        if criterion == "passed":
            continue

        if details["status"] == "FAIL":

            failures.append(
                {
                    "criterion": criterion,
                    "reason": details["reason"],
                    "suggestion": details["suggestion"],
                }
            )

    # Create a rejection record
    rejection = {
        "attempt": state["retry_count"],
        "failures": failures,
    }

    # Add this rejection to the previous rejection log
    rejection_log = state.get("rejection_log", [])
    rejection_log = rejection_log + [rejection]

    print("\nEvaluation result: FAIL")
    print("Failed criteria:", len(failures))

    return {
        "evaluation": evaluation,
        "status": "FAIL",
        "rejection_log": rejection_log,
    }


def route_after_evaluation(state: LessonState):
    """
    Decide whether to finish or regenerate the lesson.
    """

    # Stop if the lesson passes
    if state.get("status") == "PASS":
        return "end"

    # Stop if the maximum number of attempts is reached
    if state.get("retry_count", 0) >= MAX_ATTEMPTS:
        return "end"

    # Otherwise, try generating the lesson again
    return "generate"


def build_graph():
    """
    Build the complete lesson generation workflow.
    """

    # Create the graph using our state structure
    workflow = StateGraph(LessonState)

    # Register the nodes
    workflow.add_node("generate", generate_node)
    workflow.add_node("evaluate", evaluate_node)

    # Define the workflow order
    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "evaluate")

    # Add the conditional decision
    workflow.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "generate": "generate",
            "end": END,
        },
    )

    # Compile the graph
    return workflow.compile()


# Create the compiled graph
lesson_graph = build_graph()


if __name__ == "__main__":

    # Initial information for the graph
    initial_state = {
        "topic": "Introduction to RAG",
        "learner_profile": (
            "A 12th-grade graduate in India who has limited English "
            "vocabulary and is learning from zero."
        ),
        "retry_count": 0,
        "rejection_log": [],
        "status": "STARTED",
    }

    # Run the complete workflow
    final_state = lesson_graph.invoke(initial_state)

    # Display the final result
    print("\n--- FINAL WORKFLOW RESULT ---")

    print("Status:", final_state["status"])
    print("Attempts:", final_state["retry_count"])

    print("\n--- FINAL LESSON ---")
    print(final_state["lesson"])

    print("\n--- REJECTION LOG ---")

    if final_state["rejection_log"]:

        for rejection in final_state["rejection_log"]:

            print(f"\nAttempt: {rejection['attempt']}")

            for failure in rejection["failures"]:

                print(f"Criterion: {failure['criterion']}")
                print(f"Reason: {failure['reason']}")
                print(f"Suggestion: {failure['suggestion']}")

    else:
        print("No rejected attempts.")
