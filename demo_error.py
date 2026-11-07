
import src.graph as graph_module
from src.generator import generate_lesson as real_generate_lesson

attempt_counter = 0


def demo_generator(topic, learner_profile, feedback):
    global attempt_counter
    attempt_counter += 1

    lesson = real_generate_lesson(
        topic=topic,
        learner_profile=learner_profile,
        feedback=feedback
    )

    if attempt_counter == 1:
        print("\nDEMO: Injecting a deliberate technical error into Attempt 1.")

        lesson += """
## Additional Statement

RAG does not retrieve information from external documents.
It only uses the language model's internal knowledge.
"""
    else:
        print("\nDEMO: Regenerating the lesson using evaluation feedback.")

    return lesson


# Temporarily replace the lesson generator for this demo
graph_module.generate_lesson = demo_generator

initial_state = {
    "topic": "Introduction to RAG",
    "learner_profile": (
        "A 12th-grade graduate in India with limited English vocabulary, "
        "learning this topic from zero."
    ),
    "retry_count": 0,
    "rejection_log": [],
    "status": "STARTED"
}

# Run the complete lesson-generation workflow
final_state = graph_module.lesson_graph.invoke(initial_state)

print("\n========== DEMO RESULT ==========")
print("Final status:", final_state["status"])
print("Attempts used:", final_state["retry_count"])
print("Rejection log:", final_state["rejection_log"])

print("\nFinal lesson:\n")
print(final_state["lesson"])
