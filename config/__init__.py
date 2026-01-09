"""Configuration module for DeepGLM Android Automation Agent."""

from .settings import settings  # noqa: F401
from .prompts import (  # noqa: F401
    MAIN_AGENT_PROMPT,
    ANDROID_OPERATOR_PROMPT,
    RESEARCH_ANALYST_PROMPT,
    CODE_REVIEWER_PROMPT,
    DOCUMENTATION_WRITER_PROMPT,
)

__all__ = [
    "settings",
    "MAIN_AGENT_PROMPT",
    "ANDROID_OPERATOR_PROMPT",
    "RESEARCH_ANALYST_PROMPT",
    "CODE_REVIEWER_PROMPT",
    "DOCUMENTATION_WRITER_PROMPT",
]
