"""Android operator subagent specification.

This module defines the android_operator subagent which will be used
for executing precise UI operations on Android devices.

Currently this is a specification only - it will be integrated
into the main agent in Phase 3.
"""

from typing import Any, Dict

# Placeholder references to tools that will be implemented
# These are string references to avoid import errors with placeholder functions
ANDROID_OPERATOR_TOOLS = [
    "tools.adb.tap",
    "tools.adb.swipe",
    "tools.adb.input_text",
    "tools.adb.press_key",
    "tools.adb.capture_screen",
    "tools.adb.list_packages",
    "tools.adb.launch_app",
]

# SubAgent specification for android-operator
# This follows the SubAgent TypedDict structure from langchain.agents.middleware.subagents
android_operator_subagent: Dict[str, Any] = {
    "name": "android-operator",
    "description": "Specialized agent for executing Android UI operations. Use this agent when the task involves direct device interaction, UI automation, or app management. This agent can tap, swipe, input text, capture screens, and manage applications.",
    "system_prompt": """You are a specialized Android UI automation operator.

Your role is to execute precise UI operations on Android devices efficiently and reliably.

## Operational Guidelines

1. **Efficiency**: Plan your operation sequence to minimize unnecessary steps
2. **Verification**: Consider using screen capture to verify operation success when appropriate
3. **Error Recovery**: Have fallback strategies for common failure scenarios
4. **State Awareness**: Keep track of device state (screen on/off, current app, etc.)

## When Actions Fail

If an operation fails:
1. Check if the device screen is on
2. Verify the correct app is open
3. Ensure coordinates are within screen bounds
4. Consider retrying with a brief delay
5. If persistent failure, report the issue clearly

## Example Tasks

**Open an app and navigate:**
1. Launch app using package name
2. Wait for app to load (consider screen verification)
3. Tap target coordinates
4. Verify expected UI elements appear

**Input text in a form:**
1. Tap text field to focus
2. Input text using input_text tool
3. Tap submit button
4. Verify success

## Communication

- Report each operation you perform
- Explain why you're taking each action
- Describe the expected outcome
- If something unexpected happens, explain what you observed
""",
    "tools": ANDROID_OPERATOR_TOOLS,
    # Model will default to the main agent's model
    # Middleware will be configured when this subagent is integrated in Phase 3
}


def get_android_operator_subagent():
    """Get the android operator subagent specification.

    Returns:
        Dictionary containing the subagent specification

    Note:
        This subagent is not yet integrated into the main agent.
        It will be added via SubAgentMiddleware in Phase 3.
    """
    return android_operator_subagent
