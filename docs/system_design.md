
# RAG LessonForge — System Design

## 1. Overview

RAG LessonForge is an AI-powered lesson generation system that creates beginner-friendly educational content and evaluates its quality before accepting it.

The target learners are Indian students who have completed Class 12 and have limited English proficiency.

The system generates a lesson, evaluates it using a structured rubric, and retries generation when the lesson does not meet the required quality standards.

## 2. System Architecture

The application uses the following components:

- Python: Main application logic
- LangChain: Integration with the Gemini language model
- Gemini: Lesson generation and evaluation
- LangGraph: Workflow orchestration
- Pydantic: Structured evaluation output
- SQLite: Persistent storage of evaluation failures
- Pytest: Automated testing

## 3. Workflow

The application follows this sequence:

1. Receive the lesson topic and learner profile.
2. Retrieve relevant repeated failures from SQLite memory.
3. Generate a lesson using Gemini.
4. Evaluate the lesson against six quality criteria.
5. If all criteria pass, accept the lesson.
6. If any criterion fails, record the rejection details.
7. Use feedback to generate an improved lesson.
8. Repeat until the lesson passes or the maximum of three attempts is reached.
9. Save the final lesson and evaluation report.

## 4. LangGraph Workflow

The graph contains two main nodes.

### Generate Node

The generate node:

- Reads the topic and learner profile.
- Collects feedback from previous rejected attempts.
- Retrieves recurring failures from persistent memory.
- Calls the lesson generator.
- Updates the attempt count.

### Evaluate Node

The evaluate node:

- Calls the evaluator.
- Checks all six evaluation criteria.
- Stores failed criteria in SQLite.
- Updates the evaluation status.
- Adds failure reasons and correction suggestions to the rejection log.

### Conditional Routing

After evaluation:

- PASS routes to the end of the workflow.
- FAIL routes back to generation if attempts remain.
- FAIL after the maximum attempts routes to the end.

## 5. Evaluation Criteria

Each lesson is checked for:

1. Technical accuracy
2. Beginner-friendly language
3. Practical example
4. Jargon control
5. Key coverage
6. Teaching flow

A lesson passes only when all six criteria pass.

## 6. Persistent Memory

SQLite stores failed evaluation results, including:

- Topic
- Failed criterion
- Failure reason
- Suggested correction
- Timestamp

The system retrieves repeated failures and includes them as guidance during future lesson generation.

This provides persistent feedback across application runs.

## 7. Retry Strategy

The system allows a maximum of three generation attempts.

The rejection log preserves the history of failed attempts. The system does not overwrite previous rejection details.

If the lesson passes, the final status is PASS. If all attempts fail, the final status is FAIL.

## 8. Output Management

The output manager saves:

- Lesson content in Markdown
- Evaluation details in JSON
- Overall status
- Number of attempts
- Rejection history

Files are saved in the `outputs` directory.

## 9. Testing

Pytest is used to test:

- Memory table creation
- Saving failed evaluations
- Detecting repeated failures
- Retry behavior
- Maximum-attempt behavior

Run the tests using:

```powershell
pytest -v
```

## 10. Limitations

- Lesson generation and evaluation depend on the Gemini API.
- The evaluator is an AI model and may make incorrect judgments.
- Persistent memory stores evaluation failures but does not automatically rewrite the rubric.
- The current workflow focuses on a single lesson topic per execution.
