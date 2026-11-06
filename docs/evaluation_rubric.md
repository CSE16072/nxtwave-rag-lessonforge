
# LessonForge Evaluation Rubric

## 1. Purpose

The evaluation rubric checks whether a generated lesson is accurate, beginner-friendly, practical, and suitable for Indian students who have completed Class 12 and have limited English proficiency.

The lesson is evaluated before it is accepted as the final output.

## 2. Evaluation Criteria

The evaluator uses six criteria.

### 2.1 Technical Accuracy

- The lesson must explain the topic correctly.
- It must avoid misleading or unsupported statements.
- Technical explanations must be consistent.

### 2.2 Beginner-Friendly Language

- The lesson must use simple and clear English.
- Sentences should be easy for a beginner to understand.
- The lesson should avoid unnecessary complexity.

### 2.3 Practical Example

- The lesson must include a practical example.
- The example should connect the topic to a familiar real-world situation.
- The example must help the learner understand the concept.

### 2.4 Jargon Control

- Technical terms must be explained in simple language.
- Unexplained jargon should be avoided.
- New concepts should be introduced gradually.

### 2.5 Key Coverage

The lesson must cover:

- What the topic means
- Why the topic is useful
- How it works
- Important limitations or cautions

### 2.6 Teaching Flow

- The lesson must follow a logical sequence.
- Concepts should progress from simple to more detailed.
- The lesson should include a recap or conclusion.

## 3. PASS / FAIL Rules

Each criterion receives one of two statuses:

- `PASS`: The lesson satisfies the criterion.
- `FAIL`: The lesson does not sufficiently satisfy the criterion.

The overall lesson passes only when all six criteria pass.

If even one criterion fails, the lesson is rejected and sent for regeneration.

## 4. Retry Policy

The system allows a maximum of three generation attempts.

1. Generate the lesson.
2. Evaluate it against all six criteria.
3. If it passes, accept the lesson.
4. If it fails, record the reasons and correction suggestions.
5. Regenerate using the evaluation feedback and relevant past failures.
6. Stop after three attempts, even if the lesson still fails.

The system does not continue regenerating indefinitely.

## 5. Rejection Log

When a lesson fails, the system records:

- Attempt number
- Failed criterion
- Reason for failure
- Suggested correction

This rejection log helps explain why a lesson was rejected and how the next attempt was improved.

## 6. Persistent Evaluation Memory

SQLite stores failed evaluation results.

The system can retrieve recurring failures and use them as additional guidance during lesson generation.

This supports improvement across multiple runs by reminding the generator about issues that have occurred repeatedly.

The stored failures do not automatically change the evaluation criteria. The evaluator continues to apply the defined rubric.

## 7. Final Output

The system saves:

- The final generated lesson
- The evaluation results
- The final PASS or FAIL status
- The number of attempts
- The rejection log

The output is saved in Markdown and JSON formats.
