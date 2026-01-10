"""Configuration module for DeepGLM Android Automation Agent."""

from deepglm.config.prompts import (  # noqa: F401
    ANDROID_OPERATOR_PROMPT,
    CODE_REVIEWER_PROMPT,
    DOCUMENTATION_WRITER_PROMPT,
    MAIN_AGENT_PROMPT,
    RESEARCH_ANALYST_PROMPT,
)
from deepglm.config.settings import settings  # noqa: F401

__all__ = [
    "settings",
    "MAIN_AGENT_PROMPT",
    "ANDROID_OPERATOR_PROMPT",
    "RESEARCH_ANALYST_PROMPT",
    "CODE_REVIEWER_PROMPT",
    "DOCUMENTATION_WRITER_PROMPT",
]
