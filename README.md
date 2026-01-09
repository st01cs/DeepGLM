# DeepGLM Android Automation Agent

An intelligent Android device automation agent built with LangChain DeepAgents. DeepGLM focuses on goal-oriented task execution where you specify objectives and the agent decomposes and executes them using ADB commands.

## Project Status

**Current Phase: Phase 1 - Core Structure Setup 🚧**

The project is currently in Phase 1 of development, establishing a layered architecture foundation. Android automation features are planned for Phase 2-5.

**What Works Now:**
- ✅ Clean modular code structure
- ✅ Internet search via Tavily
- ✅ Configuration management
- ✅ Placeholder ADB tools (not yet implemented)

**Coming Soon:**
- 🔨 Phase 2: Actual ADB functionality implementation
- 🔨 Phase 3: Subagent integration
- 🔨 Phase 4: Vision model for screen analysis
- 🔨 Phase 5: File system operations

## Features

### Current (Phase 1)
- **Layered Architecture**: Clean separation of config, tools, and agents
- **Internet Search**: Powered by Tavily API for research
- **Type-Safe Configuration**: Environment-based config with validation
- **Extensible Design**: Easy to add new tools and agents

### Planned (Phase 2-5)
- **ADB Integration**: Control Android devices via ADB commands
- **Goal-Oriented Automation**: Specify objectives, agent handles execution
- **Visual Screen Analysis**: Understand screen content with vision models
- **App Management**: Launch, monitor, and control Android apps
- **UI Operations**: Tap, swipe, input, and navigate interfaces

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DeepGLM
```

2. Install dependencies using uv:
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# Required: Model Provider (OpenAI-compatible API)
OPENAI_API_KEY="sk-your-api-key-here"
OPENAI_BASE_URL="https://api.deepseek.com"
OPENAI_MODEL="deepseek-ai/DeepSeek-V3.2"

# Required: Search
TAVILY_API_KEY="tvly-your-tavily-api-key-here"

# Optional: Vision Model (for Phase 4)
# VISION_MODEL="gpt-4o"

# Optional: ADB Path (for Phase 2)
# ADB_PATH="/usr/local/bin/adb"

# Optional: LangSmith Tracing
# LANGCHAIN_TRACING_V2="true"
# LANGCHAIN_API_KEY="lsv2-your-langsmith-api-key-here"
# LANGCHAIN_PROJECT="deepglm-android"
```

### Getting API Keys

- **DeepSeek**: Get your API key from [https://platform.deepseek.com](https://platform.deepseek.com)
- **Tavily**: Get your API key from [https://tavily.com](https://tavily.com)
- **LangSmith**: Get your API key from [https://smith.langchain.com](https://smith.langchain.com)

## Usage

### Basic Usage (Current - Phase 1)

Currently, DeepGLM can research topics and answer questions using internet search:

```bash
python main.py "What are the latest developments in quantum computing?"
```

### Examples

**Research Android automation:**
```bash
python main.py "Research best practices for Android UI automation with ADB"
```

**General knowledge:**
```bash
python main.py "Explain how Android's input system works"
```

**Finance-specific search:**
```bash
python main.py "What's the current trend in mobile app development?"
```

### Planned Usage (Phase 2-5)

Once ADB tools are implemented, you'll be able to:

```bash
# Open an app and perform actions
python main.py "Open YouTube and search for cat videos"

# Navigate through settings
python main.py "Enable dark mode in system settings"

# Multi-step automation
python main.py "Open Gmail, compose a new email to test@example.com with subject 'Test'"
```

## Architecture Overview

### Directory Structure

```
DeepGLM/
├── config/              # Configuration layer
│   ├── settings.py      # Environment loading & validation
│   └── prompts.py       # System prompts for agents
├── tools/               # Tools layer
│   ├── adb.py          # ADB command wrappers (placeholders)
│   ├── internet.py     # Tavily search integration
│   └── vision.py       # Screen analysis (reserved)
├── agents/              # Agent layer
│   ├── main_agent.py   # Primary Android automation agent
│   └── subagents/      # Subagent configurations
│       └── android_operator.py  # Android UI specialist
├── middleware/          # Middleware layer (reserved)
│   └── filesystem.py   # File operations (future)
├── main.py             # Entry point
├── pyproject.toml      # Dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

### Design Principles

- **Layered Architecture**: Clear separation between config, tools, and agents
- **Type Safety**: Type hints throughout for better IDE support
- **Explicit Over Implicit**: Clear, direct implementations over magic
- **Phased Development**: Incremental feature addition based on need
- **Zero Breaking Changes**: Backward compatibility maintained during refactors

## Development

### Phase 1: Core Structure (Current)
✅ Completed:
- Directory structure with __init__.py files
- Configuration management (config/settings.py)
- System prompts (config/prompts.py)
- Placeholder ADB tools (tools/adb.py)
- Internet search tool (tools/internet.py)
- Vision module placeholder (tools/vision.py)
- Agent factory (agents/main_agent.py)
- Subagent specification (agents/subagents/android_operator.py)
- Refactored main.py
- Updated documentation

### Phase 2: Android Tools Implementation (Next)
- Implement actual ADB command execution
- Device info functions (get_devices, get_device_info, get_battery_level)
- Input events (tap, swipe, input_text, press_key)
- Screen capture
- App management (list_packages, launch_app, force_stop_app, install_app, uninstall_app)
- Error handling and device status checks

### Phase 3: Agent Integration
- Integrate SubAgentMiddleware
- Design comprehensive system prompts
- Create specialized subagents
- Test end-to-end automation workflows

### Phase 4: Vision Analysis
- Setup vision model integration
- Implement capture_and_analyze function
- Create visual analysis workflows
- Test screen understanding capabilities

### Phase 5: File System Operations
- Design file system middleware architecture
- Implement basic file operations
- Add sandbox restrictions

## Dependencies

Current dependencies (pyproject.toml):

- `deepagents>=0.3.4` - Agent framework with LangGraph
- `langchain-openai` - OpenAI-compatible LLM integration
- `langchain-core` - Core LangChain components
- `tavily-python>=0.7.17` - Search API
- `python-dotenv>=1.0.0` - Environment variable loading

## Troubleshooting

### Missing Environment Variables

If you see an error about missing environment variables:

```bash
# Check if .env exists
ls -la .env

# Verify required variables are set
grep OPENAI_API_KEY .env
grep TAVILY_API_KEY .env
```

### Import Errors

If you encounter import errors:

```bash
# Ensure you're in the project root
cd /path/to/DeepGLM

# Install dependencies
uv sync

# Verify Python path
python -c "import sys; print(sys.path)"
```

### Model Connection Issues

If you're using DeepSeek, verify:
- `OPENAI_API_KEY` is correct
- `OPENAI_BASE_URL` is set to `https://api.deepseek.com`
- `OPENAI_MODEL` is set to a valid model name

## Roadmap

See [dev/plan/0002-code-structure.md](dev/plan/0002-code-structure.md) for detailed implementation plans and phase specifications.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**Development Guidelines:**
1. Follow the phased development approach
2. Maintain type hints and docstrings
3. Keep backward compatibility
4. Test before committing
5. Update documentation as needed

## License

[Your License Here]
