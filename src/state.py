
from typing import TypedDict, Any


class LessonState(TypedDict, total=False):
    topic: str
    learner_profile: str
    lesson: str
    evaluation: dict[str, Any]
    retry_count: int
    rejection_log: list[dict[str, Any]]
    status: str
    improvement_memory: list[str]
