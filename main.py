from src.graph import lesson_graph
from src.output_manager import save_output


def main():
    """
    Run the complete RAG LessonForge application.
    """

    print("=" * 50)
    print("       RAG LESSONFORGE")
    print(" Self-Evaluating Lesson Generation System")
    print("=" * 50)

    # Define the lesson topic
    topic = "Introduction to RAG"

    # Define the target learner
    learner_profile = (
        "A 12th-grade graduate in India who has limited English "
        "vocabulary and is learning from zero."
    )

    # Prepare the initial workflow state
    initial_state = {
        "topic": topic,
        "learner_profile": learner_profile,
        "retry_count": 0,
        "rejection_log": [],
        "status": "STARTED",
    }

    print(f"\nTopic: {topic}")
    print("\nStarting lesson generation...")

    # Run the LangGraph workflow
    final_state = lesson_graph.invoke(initial_state)

    # Save the final lesson and evaluation report
    saved_files = save_output(final_state)

    # Display the final summary
    print("\n" + "=" * 50)
    print("             FINAL SUMMARY")
    print("=" * 50)

    print(f"Topic: {final_state['topic']}")
    print(f"Final Status: {final_state['status']}")
    print(f"Attempts: {final_state['retry_count']}")

    print("\nFiles created:")
    print(f"Markdown Report: {saved_files['markdown_path']}")
    print(f"JSON Report: {saved_files['json_path']}")

    print("\nRAG LessonForge completed successfully!")


if __name__ == "__main__":
    main()