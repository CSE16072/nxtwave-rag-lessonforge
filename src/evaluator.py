from typing import Literal

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GOOGLE_API_KEY, MODEL_NAME, check_config
from src.prompts import EVALUATION_PROMPT


# Each criterion must receive either PASS or FAIL
class CriterionResult(BaseModel):
    status: Literal["PASS", "FAIL"] = Field(
        description="The result must be exactly PASS or FAIL."
    )

    reason: str = Field(
        description="Explain why the lesson passed or failed this criterion."
    )

    suggestion: str = Field(
        description="Give a specific improvement if the criterion failed."
    )


# Structure of the complete evaluation
class LessonEvaluation(BaseModel):
    technical_accuracy: CriterionResult

    beginner_friendly: CriterionResult

    practical_example: CriterionResult

    jargon_control: CriterionResult

    key_coverage: CriterionResult

    teaching_flow: CriterionResult


def evaluate_lesson(topic, learner_profile, lesson):
    """
    Evaluate a generated lesson using six strict criteria.
    """

    # Check whether the API key is configured
    check_config()

    # Create the Gemini model connection
    model = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )

    # Ask Gemini to return structured evaluation results
    evaluator = model.with_structured_output(LessonEvaluation)

    # Fill the evaluation prompt
    prompt = EVALUATION_PROMPT.format(
        topic=topic,
        learner_profile=learner_profile,
        lesson=lesson,
    )

    # Get the structured evaluation
    evaluation = evaluator.invoke(prompt)

    # Convert the Pydantic result into a Python dictionary
    result = evaluation.model_dump()

    # Check whether every criterion passed
    all_passed = all(
        criterion["status"] == "PASS"
        for criterion in result.values()
    )

    # Add the final pass/fail result
    result["passed"] = all_passed

    return result


if __name__ == "__main__":

    # Generate a lesson first
    from src.generator import generate_lesson

    topic = "Introduction to RAG"

    learner_profile = (
        "A 12th-grade graduate in India who has limited English "
        "vocabulary and is learning from zero."
    )

    lesson = generate_lesson(
        topic=topic,
        learner_profile=learner_profile,
    )

    # Evaluate the generated lesson
    evaluation = evaluate_lesson(
        topic=topic,
        learner_profile=learner_profile,
        lesson=lesson,
    )

    # Display the evaluation results
    print("\n--- LESSON EVALUATION ---\n")

    for criterion, details in evaluation.items():

        if criterion == "passed":
            continue

        print(f"\n{criterion.upper()}")
        print(f"Status: {details['status']}")
        print(f"Reason: {details['reason']}")
        print(f"Suggestion: {details['suggestion']}")

    print("\n--- FINAL RESULT ---")

    if evaluation["passed"]:
        print("PASS: The lesson meets all evaluation criteria.")
    else:
        print("FAIL: The lesson needs improvement.")
