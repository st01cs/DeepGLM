"""DeepGLM Research Agent - A streamlined research and knowledge work assistant.

This package provides Android automation capabilities powered by deep agents
with support for internet research, device control, and task planning.
"""

import logging

# Import and re-export public API
from deepglm.agents.main_agent import create_android_agent
from deepglm.config import prompts, settings

# Configure package-level logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

__all__ = ["create_android_agent", "prompts", "settings", "logger"]

__version__ = "0.1.0"


