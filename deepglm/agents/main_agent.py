"""Main Android automation agent factory.

This module creates and configures the primary DeepGLM agent
with all tools and middleware.
"""

import logging

from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

from deepglm.config import prompts, settings
from deepglm.tools.internet import internet_search

logger = logging.getLogger(__name__)


def create_android_agent():
    """Create and configure the Android automation agent.

    This function sets up the main agent with:
    - Configured LLM model from settings
    - Available tools (currently only internet_search)
    - System prompt for Android automation
    - No middleware yet (will be added in Phase 3)

    Returns:
        Configured agent instance ready for invocation

    Note:
        As of Phase 1, this agent has limited functionality since
        ADB tools are placeholder implementations. The agent can
        perform web research but cannot yet control Android devices.

    Example:
        >>> agent = create_android_agent()
        >>> result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
        >>> print(result["messages"][-1].content)
    """
    logger.info("Creating Android automation agent")

    # Initialize model with configuration from settings
    logger.debug(f"Initializing model: {settings.OPENAI_MODEL}")
    model = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    # Collect available tools
    # Note: ADB tools are not included yet as they're placeholder implementations
    tools = [internet_search]
    logger.debug(f"Configured {len(tools)} tools")

    # Create the agent with system prompt and tools
    agent = create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=prompts.MAIN_AGENT_PROMPT,
    )

    logger.info("Android automation agent created successfully")
    return agent
