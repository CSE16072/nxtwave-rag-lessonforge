# RAG LessonForge

## Overview

RAG LessonForge is a self-evaluating AI lesson generation system designed for Indian students who have completed Class 12 and have limited English proficiency.

The system generates beginner-friendly lessons, evaluates them against a strict quality rubric, and regenerates them when they fail evaluation.

This project demonstrates AI-based content generation, structured evaluation, workflow orchestration, feedback-driven retries, and persistent memory.

## Problem Statement

AI-generated educational content can be too technical, incomplete, or difficult for beginners to understand.

RAG LessonForge aims to improve generated lessons through an automated evaluation and feedback loop.

## Key Features

- Beginner-friendly lesson generation
- AI-based lesson evaluation
- Six strict quality criteria
- PASS/FAIL evaluation
- Maximum of three generation attempts (one initial attempt and up to two retries).
- Rejection log with failure reasons and correction suggestions
- Persistent evaluation memory using SQLite
- Recurring failure detection
- Markdown and JSON output reports
- Automated tests using Pytest

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Gemini | Lesson generation and evaluation |
| LangChain | Language model integration |
| LangGraph | Workflow orchestration |
| Pydantic | Structured evaluation results |
| SQLite | Persistent evaluation memory |
| Pytest | Automated testing |
| python-dotenv | Environment variable management |

## Project Structure

```text
nxtwave-rag-lessonforge/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── state.py
│   ├── prompts.py
│   ├── generator.py
│   ├── evaluator.py
│   ├── memory.py
│   ├── graph.py
│   └── output_manager.py
├── tests/
│   ├── test_memory.py
│   └── test_graph.py
├── docs/
│   ├── system_design.md
│   ├── evaluation_rubric.md
│   └── demo_script.md
├── outputs/
├── main.py
├── test_gemini.py
├── demo_error.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Evaluation Rubric

Each generated lesson is evaluated against six criteria:

1. Technical accuracy
2. Beginner-friendly language
3. Practical example
4. Jargon control
5. Key coverage
6. Teaching flow

The lesson passes only when all six criteria pass.

If any criterion fails, the lesson is rejected and regenerated using evaluation feedback.

## Workflow

1. Receive the topic and learner profile.
2. Retrieve recurring failures from SQLite memory.
3. Generate a lesson using Gemini.
4. Evaluate the lesson against the rubric.
5. Accept the lesson if all criteria pass.
6. Otherwise, record the rejection details.
7. Regenerate using feedback.
8. Stop after a maximum of three attempts.
9. Save the lesson and evaluation report.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/CSE16072/nxtwave-rag-lessonforge.git
cd nxtwave-rag-lessonforge
```

### 2. Create a Virtual Environment

For Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root and add:

```text
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own Gemini API key.

Do not commit the `.env` file or expose your API key publicly.

## Run the Application

With the virtual environment activated:

```powershell
python main.py
```

The application generates and evaluates a lesson on the configured topic.

## Run Tests

Run the automated test suite:

```powershell
pytest -v
```

The tests cover persistent memory and graph retry behavior.

## Output

The application saves generated results in the `outputs/` directory.

The outputs include:

- Markdown lesson
- JSON evaluation report
- Final PASS/FAIL status
- Attempt count
- Evaluation results
- Rejection log

## Documentation

Additional project documentation is available in the `docs/` directory:

- `system_design.md` — System architecture and workflow
- `evaluation_rubric.md` — Evaluation criteria and retry policy
- `demo_script.md` — Project demonstration script

## Limitations

- The application depends on Gemini API availability.
- AI-based evaluation may not always be perfect.
- The current system focuses on generating one lesson topic per execution.
- Persistent memory uses past failures as guidance; it does not automatically modify the evaluation rubric.
- The assessment focuses on generating and evaluating a beginner-friendly lesson about RAG, rather than building a separate RAG retrieval pipeline.
- Future improvements could include grounding generated lessons in curated educational reference material.

## Future Improvements

- Add support for multiple educational topics.
- Introduce configurable learner profiles.
- Add a user interface for lesson generation.
- Track evaluation performance across multiple topics.
- Improve grounding with curated educational reference material.

## Author

Developed as part of the NxtWave Associate Gen AI Curriculum Engineer assignment.
