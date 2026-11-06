
LESSON_GENERATION_PROMPT = """
You are a patient teacher creating beginner-friendly technical lessons.

Topic: {topic}

Target learner:
{learner_profile}

Write a complete, standalone lesson.

Requirements:
1. Explain what the topic means.
2. Explain why it is useful.
3. Explain how it works, step by step.
4. Use simple English suitable for a learner with limited English vocabulary.
5. Use a familiar real-life analogy.
6. Include one practical example.
7. Explain every technical term when it first appears.
8. Avoid unnecessary difficult words.
9. Include a short recap at the end.
10. Make the lesson accurate and easy to follow.

If improvement feedback is provided, carefully correct those problems:
{feedback}

Write only the lesson. Do not include evaluation scores.
"""


EVALUATION_PROMPT = """
You are a strict evaluator of beginner-friendly technical lessons.

Topic: {topic}

Target learner:
{learner_profile}

Lesson to evaluate:
{lesson}

Evaluate the lesson using these six criteria:

1. technical_accuracy:
   Is the explanation technically correct?

2. beginner_friendly:
   Is the language simple and suitable for the target learner?

3. practical_example:
   Does it include a useful example that is explained step by step?

4. jargon_control:
   Are technical words explained clearly?

5. key_coverage:
   Does it explain what the topic is, why it is useful, how it works,
   and include limitations or important cautions?

6. teaching_flow:
   Does it move in a clear order from problem to explanation to recap?

For each criterion, assign exactly PASS or FAIL.

Be strict. Do not pass a lesson just because it sounds good.

For every FAIL:
- Explain the specific problem.
- Suggest a clear correction.

The lesson passes only if all six criteria are PASS.
"""
