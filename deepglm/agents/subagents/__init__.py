"""Subagents module for DeepGLM Android Automation Agent."""

from deepglm.agents.subagents.android_operator import (  # noqa: F401
    android_operator_subagent,
    get_android_operator_subagent,
)

__all__ = ["android_operator_subagent", "get_android_operator_subagent"]
