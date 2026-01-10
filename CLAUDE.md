The @dev/refs/langchain-llms.txt is a list of documents related to langchain/langgraph/deepagents. When you encounter these, be sure to consult the documentation before taking any action.

## Project Structure

As of Phase 0003, all application code is organized under the `deepglm` package:

```
deepglm/
├── __init__.py              # Public API exports
├── agents/                  # Agent creation and configuration
│   ├── __init__.py
│   ├── main_agent.py
│   └── subagents/
│       ├── __init__.py
│       └── android_operator.py
├── config/                  # Configuration management
│   ├── __init__.py
│   ├── prompts.py
│   └── settings.py
├── exceptions.py            # Custom exception hierarchy
├── middleware/              # Reserved for future middleware implementations
│   └── __init__.py
└── tools/                   # Tool implementations
    ├── __init__.py
    ├── adb.py
    ├── internet.py
    └── vision.py
```

## Public API

The main public API is exported from the `deepglm` package:

- `create_android_agent()`: Factory function to create the Android automation agent
- `prompts`: System prompts for the agent
- `settings`: Configuration settings singleton

Example usage:

```python
from deepglm import create_android_agent

agent = create_android_agent()
result = agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})
```
