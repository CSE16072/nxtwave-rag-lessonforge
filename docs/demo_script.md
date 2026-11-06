
# RAG LessonForge — Demo Script

**Suggested duration:** 15–20 minutes

## 1. Introduction — 1 minute

Hello, my project is called RAG LessonForge.

It is a self-evaluating lesson generation system designed for students who have completed Class 12 and have limited English proficiency.

The goal is to generate lessons that are accurate, simple, practical, and easy to understand.

## 2. Problem Statement — 2 minutes

AI-generated educational content may sometimes be too technical, incomplete, or difficult for beginners.

A normal content generator produces an answer, but it does not necessarily check whether the answer is suitable for the learner.

RAG LessonForge addresses this by generating a lesson, evaluating it against a strict rubric, and regenerating it when necessary.

## 3. Project Architecture — 3 minutes

The project uses:

- Python for the application logic
- LangChain with Gemini for lesson generation and evaluation
- LangGraph to manage the generation and evaluation workflow
- Pydantic for structured evaluation results
- SQLite for persistent evaluation memory
- Pytest for automated testing

The main workflow is:

1. Start with the topic and learner profile.
2. Generate a lesson.
3. Evaluate the lesson against six criteria.
4. Accept the lesson if all criteria pass.
5. Otherwise, record the rejection and regenerate using feedback.
6. Stop after a maximum of three attempts.
7. Save the final lesson and evaluation report.

## 4. Demonstrate the Application — 4 minutes

Open the project in VS Code.

Show the main files:

- `main.py`
- `src/generator.py`
- `src/evaluator.py`
- `src/graph.py`
- `src/memory.py`
- `src/output_manager.py`

Explain that `main.py` starts the workflow.

The generator creates the lesson. The evaluator checks it. The graph controls retries. The memory module stores previous failures. The output manager saves the result.

Run the application:

```powershell
python main.py
```

Show the generated lesson and the evaluation status.

## 5. Demonstrate Self-Evaluation and Retries — 3 minutes

Explain the six criteria:

1. Technical accuracy
2. Beginner-friendly language
3. Practical example
4. Jargon control
5. Key coverage
6. Teaching flow

Show an example where a lesson fails one criterion.

Explain that the rejection log records the failed criterion, the reason, and the correction suggestion.

The next generation uses that feedback to improve the lesson.

If all criteria pass, the system accepts the lesson. If it still fails after three attempts, the system stops.

## 6. Persistent Memory — 2 minutes

Open `src/memory.py`.

Explain that failed evaluation results are stored in SQLite.

When similar issues occur repeatedly, the system retrieves those failures and uses them as additional guidance during later generations.

This helps the generator consider issues that appeared in previous runs.

## 7. Automated Testing — 2 minutes

Run:

```powershell
pytest -v
```

The project includes tests for:

- Creating the SQLite memory table
- Saving failed evaluations
- Detecting repeated failures
- Retrying after an evaluation failure
- Stopping after the maximum number of attempts

Show the passing test results.

## 8. Output Files — 1 minute

Open the `outputs` folder.

Show the generated Markdown lesson and JSON report.

Explain that the report includes the lesson, evaluation results, final status, attempt count, and rejection log.

## 9. Conclusion — 1 minute

RAG LessonForge combines AI-based lesson generation with structured evaluation and feedback-driven retries.

The project focuses on making generated educational content more suitable for beginner learners.

Thank you.
