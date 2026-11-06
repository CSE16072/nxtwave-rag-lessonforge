from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GOOGLE_API_KEY, MODEL_NAME, check_config
from src.prompts import LESSON_GENERATION_PROMPT


def generate_lesson(topic, learner_profile, feedback="No previous feedback."):
    """
    Generate a beginner-friendly lesson using Gemini.
    """

    # Check whether the API key is configured
    check_config()

    # Create the Gemini model connection
    model = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
    )

    # Fill the placeholders in our prompt
    prompt = LESSON_GENERATION_PROMPT.format(
        topic=topic,
        learner_profile=learner_profile,
        feedback=feedback,
    )

    # Send the prompt to Gemini
    response = model.invoke(prompt)

    # Get the response content
    content = response.content

    # Convert list-based response into plain text
    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])

        return "\n".join(text_parts)

    # Return content directly if it is already a string
    return content


if __name__ == "__main__":
    # Generate a lesson for our target learner
    lesson = generate_lesson(
        topic="Introduction to RAG",
        learner_profile=(
            "A 12th-grade graduate in India who has limited English "
            "vocabulary and is learning from zero."
        ),
    )

    # Display the generated lesson
    print("\n--- GENERATED LESSON ---\n")
    print(lesson)
