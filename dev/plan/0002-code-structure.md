# DeepGLM Code Structure Specification

## Current Focus: Phase 1 - Core Structure Setup

**Status:** 🚧 In Progress

**Objective:** Establish the layered architecture foundation with placeholder implementations, focusing on structure over functionality.

---

## Quick Reference: Phase 1 Goals

**What we're doing:** Building the scaffold, not the house

**Key Principles:**
- ✅ Structure over functionality
- ✅ Placeholders with clear intent
- ✅ Type hints everywhere
- ✅ Docstrings for everything
- ✅ Zero breaking changes to existing code

**What Phase 1 Delivers:**
1. Clean directory structure (config/, tools/, agents/, middleware/)
2. Configuration management via Settings class
3. Placeholder ADB tools (not implemented yet)
4. Refactored internet search tool
5. Agent factory function
6. Subagent specification (not integrated yet)
7. Updated documentation

**What Phase 1 Does NOT Deliver:**
- ❌ Actual ADB functionality (that's Phase 2)
- ❌ Working Android automation (that's Phase 2-3)
- ❌ Vision model integration (that's Phase 4)
- ❌ File system operations (that's Phase 5)

**Success Metric:** `python main.py "your query"` works exactly as before, but with cleaner code structure.

---

## Project Overview

**Project Name:** DeepGLM Android Automation Agent

**Core Purpose:** An intelligent automation agent specialized in Android device control via ADB commands.

**Key Characteristics:**

- Goal-oriented task execution (user specifies objectives, agent decomposes and executes)
- ADB-based Android device interaction (local single device)
- Layered architecture with flat directory layout
- Environment variable configuration via .env
- Session history in memory only (no persistence)
- File system operations reserved for future expansion
- No concurrent execution needed
- Simple CLI interface (keep current design)

---

## Architecture Design

### Directory Structure (Flat Layout)

```
DeepGLM/
├── .env                    # Environment variables
├── .env.example           # Environment template
├── .gitignore
├── pyproject.toml         # uv dependency management
├── uv.lock
├── README.md              # Project documentation
├── CLAUDE.md              # Claude-specific instructions
├── main.py                # Entry point
│
├── config/                # Configuration layer
│   ├── __init__.py
│   ├── settings.py        # Environment loading & validation
│   └── prompts.py         # System prompts for agents
│
├── tools/                 # Tools layer
│   ├── __init__.py
│   ├── adb.py            # ADB command wrappers
│   ├── internet.py       # Tavily search integration
│   └── vision.py         # Screen capture & analysis (reserved)
│
├── agents/               # Agent layer
│   ├── __init__.py
│   ├── main_agent.py    # Primary Android automation agent
│   └── subagents/       # Subagent configurations
│       ├── __init__.py
│       └── android_operator.py  # Android-specific subagent
│
└── middleware/           # Middleware layer (reserved)
    ├── __init__.py
    └── filesystem.py    # File system middleware (future)
```

---

## Component Specifications

### 1. Configuration Layer (`config/`)

#### `config/settings.py`
**Purpose:** Load and validate environment variables

**Responsibilities:**
- Load environment variables from .env
- Validate required variables
- Provide typed configuration access
- Handle missing variables with clear error messages

**Required Environment Variables:**
```python
OPENAI_API_KEY           # API key for LLM
OPENAI_BASE_URL          # Base URL for OpenAI-compatible API
OPENAI_MODEL             # Main model (e.g., "gpt-4o")
VISION_MODEL             # Vision model for screen analysis (optional)
TAVILY_API_KEY          # Tavily search API key
ADB_PATH                # Path to adb executable (optional, defaults to 'adb')
```

**Design Pattern:**
- Singleton configuration class
- Lazy loading
- Immutable after initialization

#### `config/prompts.py`
**Purpose:** Centralize all system prompts

**Contents:**
- Main agent system prompt (Android automation focus)
- Android operator subagent prompt
- Reserved prompts for future subagents

---

### 2. Tools Layer (`tools/`)

#### `tools/adb.py`
**Purpose:** ADB command wrappers for Android device control

**Required Functions:**

1. **Device Information**
   ```python
   def get_devices() -> List[DeviceInfo]
   def get_device_info(device_id: str) -> DeviceInfo
   def get_battery_level(device_id: str) -> int
   ```

2. **Input Events**
   ```python
   def tap(device_id: str, x: int, y: int) -> bool
   def swipe(device_id: str, x1: int, y1: int, x2: int, y2: int, duration_ms: int) -> bool
   def input_text(device_id: str, text: str) -> bool
   def press_key(device_id: str, key_code: str) -> bool
   ```

3. **Screen Capture**
   ```python
   def capture_screen(device_id: str, save_path: str) -> str
   ```

4. **App Management**
   ```python
   def list_packages(device_id: str) -> List[PackageInfo]
   def launch_app(device_id: str, package_name: str) -> bool
   def force_stop_app(device_id: str, package_name: str) -> bool
   def install_app(device_id: str, apk_path: str) -> bool
   def uninstall_app(device_id: str, package_name: str) -> bool
   ```

**Error Handling:**
- Check device online status before commands
- Provide friendly error messages
- Parse ADB output and extract relevant information
- Return boolean success indicators

**Design Notes:**
- All functions accept `device_id` parameter for future multi-device support
- Use subprocess to call ADB executable
- Validate ADB availability on initialization
- Log all ADB commands at INFO level

#### `tools/internet.py`
**Purpose:** Tavily search integration (existing)

**Status:** Keep existing implementation from main.py

#### `tools/vision.py` (Reserved)
**Purpose:** Screen capture and visual analysis

**Planned Functions:**
```python
def capture_and_analyze(
    device_id: str,
    analysis_prompt: str,
    save_path: Optional[str] = None
) -> AnalysisResult
```

**Notes:**
- Reserved for future implementation
- Will use dedicated vision model
- Integration point for visual understanding of Android screens

---

### 3. Agents Layer (`agents/`)

#### `agents/main_agent.py`
**Purpose:** Primary Android automation agent

**Responsibilities:**
- Create and configure the main agent using deepagents
- Integrate all tools (ADB, internet, vision)
- Configure middleware (SubAgentMiddleware)
- Handle user queries and orchestrate task execution

**Agent Configuration:**
```python
from deepagents import create_deep_agent
from langchain.agents.middleware.subagents import SubAgentMiddleware

# Main agent setup
model = ChatOpenAI(model=OPENAI_MODEL, ...)
tools = [tap, swipe, input_text, capture_screen, internet_search]

middleware = [
    SubAgentMiddleware(
        default_model=OPENAI_MODEL,
        default_tools=tools,
        subagents=[android_operator_subagent],
        general_purpose_agent=False  # Use specialized subagents only
    )
]

agent = create_deep_agent(
    model=model,
    tools=tools,
    middleware=middleware,
    system_prompt=ANDROID_AUTOMATION_PROMPT
)
```

**System Prompt Focus:**
- Goal-oriented task decomposition
- Android device operation expertise
- Visual analysis integration (when vision tools available)
- Step-by-step execution with verification
- Clear communication of actions taken

#### `agents/subagents/android_operator.py`
**Purpose:** Specialized subagent for Android UI operations

**SubAgent Specification:**
```python
android_operator_subagent = SubAgent(
    name="android-operator",
    description="Specialized agent for executing Android UI operations. Use this agent when the task involves direct device interaction, UI automation, or app management.",
    system_prompt=ANDROID_OPERATOR_PROMPT,
    tools=[tap, swipe, input_text, capture_screen, list_packages, launch_app],
    model=OPENAI_MODEL
)
```

**SubAgent Prompt Focus:**
- Efficient UI operation sequences
- State verification after actions
- Error recovery strategies
- Screen capture for validation when needed

**Usage Scenarios:**
- "Open Gmail and compose a new email"
- "Navigate to Settings and enable dark mode"
- "Clear recent apps from memory"

---

### 4. Middleware Layer (`middleware/`)

#### `middleware/filesystem.py` (Reserved)
**Purpose:** File system operations for future expansion

**Planned Capabilities:**
- Read/write files in current working directory
- File system exploration (list, search, glob)
- Integration with FilesystemMiddleware from deepagents

**Notes:**
- Reserved for future implementation
- Will use FilesystemMiddleware backend configuration
- Access limited to current working directory
- Sandbox policy enforcement

---

## State Management

### State Structure (LangGraph State)

```python
from typing import Annotated, TypedDict
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    device_id: str  # Connected Android device ID
    last_screenshot: Optional[str]  # Path to last screenshot
    operation_history: List[str]  # List of performed operations
```

**Notes:**
- Use LangGraph's StateGraph
- Messages automatically accumulated via `add_messages` reducer
- Device ID persisted for multi-step operations
- Operation history for verification and rollback (optional)

---

## Configuration Management

### Environment Variables (`.env`)

```bash
# OpenAI-compatible API Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Vision Model (Optional, for screen analysis)
VISION_MODEL=gpt-4o

# Tavily Search API
TAVILY_API_KEY=your_tavily_key_here

# ADB Configuration
ADB_PATH=adb  # Or full path if not in PATH

# Optional: LangSmith for tracing (not required)
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_langsmith_key
# LANGCHAIN_PROJECT=deepglm-android
```

### Configuration Loading Pattern

```python
# config/settings.py
import os
from dotenv import load_dotenv
from typing import Literal

class Settings:
    load_dotenv()

    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    OPENAI_BASE_URL: str = os.environ["OPENAI_BASE_URL"]
    OPENAI_MODEL: str = os.environ["OPENAI_MODEL"]
    VISION_MODEL: str | None = os.environ.get("VISION_MODEL")
    TAVILY_API_KEY: str = os.environ["TAVILY_API_KEY"]
    ADB_PATH: str = os.environ.get("ADB_PATH", "adb")

settings = Settings()
```

---

## Logging Strategy

### Log Levels
- **Default:** INFO
- **Components to log:**
  - All ADB commands executed
  - Tool invocations and results
  - Agent decision points
  - Errors with stack traces

### Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("deepglm")
```

---

## CLI Interface

### Current Design (Maintained)

```bash
# Single query execution
python main.py "your task description"

# Example
python main.py "Open YouTube and search for cat videos"
```

### Entry Point (`main.py`)

**Flow:**
1. Load and validate environment variables
2. Initialize LLM models (main + vision)
3. Initialize ADB connection and verify device
4. Create tools (ADB, internet, vision)
5. Configure middleware (SubAgentMiddleware)
6. Create main agent
7. Execute user query
8. Print result

**Error Handling:**
- Clear error messages for missing environment variables
- ADB device offline detection
- Graceful failure with actionable feedback

---

## Error Handling Strategy

### Principles
1. **Let Agent Handle:** Primary strategy - agent interprets errors and decides next action
2. **Friendly Messages:** All tools provide clear, actionable error messages
3. **No Automatic Retry:** Agent decides if retry is appropriate
4. **Device Status:** Pre-flight checks before operations

### Example Error Messages
```
"Device 'emulator-5554' is not online. Please check ADB connection."
"Failed to tap at coordinates (100, 200): Screen is locked"
"Package 'com.example.app' is not installed on device"
```

---

## Dependencies Management

### Tool: uv
**Reason:** Modern, fast Python package manager

### Core Dependencies (`pyproject.toml`)

```toml
[project]
name = "deepglm"
version = "0.1.0"
description = "Android Automation Agent with DeepGLM"
requires-python = ">=3.10"
dependencies = [
    "deepagents",
    "langchain-openai",
    "langchain-core",
    "python-dotenv",
    "tavily-python",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Testing Strategy

### Current Status: Not Implemented

**Rationale:** Keep focus on core functionality development

**Future Consideration:**
- Unit tests for ADB tool functions
- Integration tests for agent workflows
- Mock ADB responses for testing

---

## Documentation

### Required: README.md

**Sections:**
1. Project Overview
2. Features
3. Prerequisites (Python, ADB, Android device)
4. Installation (uv setup)
5. Configuration (.env setup)
6. Usage Examples
7. Troubleshooting
8. Roadmap

### Code Documentation
- Docstrings for all public functions
- Type hints for function signatures
- Inline comments for complex logic

---

## Version Control

### Git Configuration
- `.gitignore` for Python and sensitive files
- Ignore `.env` (use `.env.example` as template)
- Ignore `__pycache__`, `*.pyc`, `.venv`

### Commit Strategy
- Conventional commits (optional, not enforced)
- Clear commit messages
- No formal CI/CD

---

## Implementation Plan

## Phase 1: Core Structure (Current Focus)

### Objective
Build the foundational layered architecture with placeholder implementations. Focus on establishing the structure, not implementing actual functionality.

### Detailed Task List

#### 1. Directory Structure Setup
- [ ] Create `config/` directory with `__init__.py`
- [ ] Create `tools/` directory with `__init__.py`
- [ ] Create `agents/` directory with `__init__.py`
- [ ] Create `agents/subagents/` directory with `__init__.py`
- [ ] Create `middleware/` directory with `__init__.py` (reserved)

#### 2. Configuration Layer (`config/`)

**`config/settings.py`**
- [ ] Create Settings class
- [ ] Load environment variables using dotenv
- [ ] Validate required variables (OPENAI_API_KEY, OPENAI_BASE_URL, etc.)
- [ ] Provide typed access to configuration
- [ ] Handle missing variables with clear error messages
- [ ] Add type hints for all configuration properties

**`config/prompts.py`**
- [ ] Define MAIN_AGENT_PROMPT (placeholder for Android automation)
- [ ] Define ANDROID_OPERATOR_PROMPT (placeholder for subagent)
- [ ] Add docstrings explaining purpose of each prompt
- [ ] Reserve space for future prompts

#### 3. Tools Layer (`tools/`)

**`tools/adb.py`**
- [ ] Create file with module docstring
- [ ] Define placeholder functions with type hints:
  - `get_devices() -> List[str]`
  - `tap(device_id: str, x: int, y: int) -> bool`
  - `swipe(device_id: str, x1: int, y1: int, x2: int, y2: int, duration_ms: int) -> bool`
  - `input_text(device_id: str, text: str) -> bool`
  - `capture_screen(device_id: str, save_path: str) -> str`
  - `list_packages(device_id: str) -> List[str]`
  - `launch_app(device_id: str, package_name: str) -> bool`
- [ ] Each function should raise `NotImplementedError` with descriptive message
- [ ] Add detailed docstrings for each function explaining future implementation
- [ ] Define type aliases (DeviceInfo, PackageInfo, etc.)

**`tools/internet.py`**
- [ ] Extract existing Tavily search implementation from main.py
- [ ] Create `internet_search()` function
- [ ] Add type hints and docstring
- [ ] Keep existing functionality intact

**`tools/vision.py`** (Reserved)
- [ ] Create placeholder file with module docstring
- [ ] Add TODO comments for future implementation
- [ ] Define type aliases for AnalysisResult

#### 4. Agents Layer (`agents/`)

**`agents/main_agent.py`**
- [ ] Create `create_android_agent()` function
- [ ] Import required dependencies (deepagents, langchain)
- [ ] Load configuration from config.settings
- [ ] Load tools from tools module
- [ ] Return configured agent instance
- [ ] Add comprehensive docstring
- [ ] Keep main.py functionality working (refactor to use new structure)

**`agents/subagents/android_operator.py`**
- [ ] Define SubAgent specification dictionary
- [ ] Include: name, description, system_prompt, tools (references)
- [ ] Add type hints
- [ ] Add docstring explaining subagent purpose
- [ ] Export subagent specification

#### 5. Entry Point Refactor (`main.py`)

- [ ] Import from new modules (config, tools, agents)
- [ ] Remove inline tool definitions
- [ ] Use `create_android_agent()` from agents.main_agent
- [ ] Keep existing CLI interface unchanged
- [ ] Ensure backward compatibility (script should work as before)
- [ ] Add logging setup

#### 6. Documentation & Environment

**`.env.example`**
- [ ] Add ADB_PATH configuration
- [ ] Add VISION_MODEL configuration (optional, commented out)
- [ ] Keep existing configurations

**`README.md`**
- [ ] Update project description to emphasize Android automation
- [ ] Add new section: "Architecture Overview"
- [ ] Add diagram of directory structure
- [ ] Update "Features" to reflect Android focus
- [ ] Add "Project Status" section noting Phase 1 in progress
- [ ] Keep existing sections (Installation, Configuration, Usage)

**`.gitignore`**
- [ ] Ensure Python-specific ignores are present
- [ ] Add ignores for screenshots (if saved locally)

### Success Criteria for Phase 1

**Structural:**
- [ ] All directories created with proper `__init__.py` files
- [ ] All modules can be imported without errors
- [ ] Type hints present on all public functions
- [ ] Docstrings on all modules and public functions

**Functional:**
- [ ] `python main.py` works exactly as before
- [ ] No functionality lost during refactor
- [ ] Configuration loading works correctly
- [ ] Error messages for missing env vars are clear

**Code Quality:**
- [ ] No linting errors (use ruff or similar)
- [ ] No import errors
- [ ] Clear separation of concerns between layers
- [ ] Placeholder implementations clearly marked

---

## Future Phases (Not Started)

### Phase 2: Android Tools Implementation ⏸️
Implement actual ADB functionality in placeholder functions.

**Key Tasks:**
- Implement device info functions
- Implement input event functions (tap, swipe, input_text)
- Implement screen capture
- Implement app management functions
- Add error handling and logging
- Add device status checks

**Trigger:** Phase 1 complete and tested

### Phase 3: Agent Integration ⏸️
Integrate SubAgentMiddleware and design sophisticated prompts.

**Key Tasks:**
- Integrate SubAgentMiddleware into main agent
- Design comprehensive system prompts
- Create android_operator subagent
- Test end-to-end workflows
- Add error recovery strategies

**Trigger:** Phase 2 complete with working ADB tools

### Phase 4: Vision Analysis 🔮
Add visual screen understanding capabilities.

**Key Tasks:**
- Setup vision model integration
- Implement capture_and_analyze function
- Create visual analysis workflows
- Test screen understanding capabilities

**Trigger:** Phase 3 complete and baseline automation working

### Phase 5: File System Operations 🔒
Add file system middleware for local file operations.

**Key Tasks:**
- Design file system middleware architecture
- Implement basic file operations
- Add sandbox restrictions
- Integrate with agent tools

**Trigger:** Future requirement identified

---

## Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | Layered | Clear separation of concerns, easy to navigate |
| Directory Layout | Flat | Simple and direct, easy to find modules |
| Configuration | Environment Variables | Simple, secure, follows 12-factor app principles |
| State Management | LangGraph State | Type-safe, built-in reducers, LangChain ecosystem |
| Concurrency | None Needed | Simpler implementation, ADB is sequential |
| Session Persistence | Memory Only | Simplicity, restartable state not required |
| Error Handling | Agent-driven | Flexible, leverages LLM reasoning |
| Testing | Deferred | Focus on core functionality first |
| Documentation | README only | Sufficient for current scope |
| Dependencies | uv | Modern, fast, good lock file support |
| ADB Functions | Reserved | Architecture ready, implementation phased |
| File System | Reserved | Future expansion capability |
| Vision Model | Independent | Dedicated model for visual tasks |

---

## Future Extensions (Reserved)

1. **Multi-device Support**
   - Device selection logic
   - Parallel operations across devices

2. **Script Recording & Playback**
   - Record ADB command sequences
   - Parameterizable scripts

3. **Visual Testing Framework**
   - Screenshot comparison
   - UI element detection

4. **File Operations**
   - Read/write files on device
   - Pull/push files

5. **Advanced Automation**
   - Conditional logic based on screen state
   - Loop operations
   - Error recovery patterns

---

## Success Criteria

### Phase 1 Success Criteria (Current)

#### Structural Requirements

- [ ] **Directory Structure Complete**
  - All required directories created (`config/`, `tools/`, `agents/`, `agents/subagents/`, `middleware/`)
  - All `__init__.py` files in place
  - Proper package hierarchy established

- [ ] **Module Imports Work**
  - `from config import settings, prompts` works
  - `from tools import adb, internet, vision` works
  - `from agents import main_agent` works
  - `from agents.subagents import android_operator` works
  - No circular import errors

- [ ] **Type Safety**
  - All public functions have type hints
  - Type aliases defined for complex types (DeviceInfo, PackageInfo, etc.)
  - Configuration class has typed properties

- [ ] **Documentation**
  - All modules have docstrings
  - All public functions have docstrings
  - Placeholder functions clearly marked as "NotImplemented"

#### Functional Requirements

- [ ] **Backward Compatibility**
  - `python main.py "query"` works exactly as before
  - Internet search functionality unchanged
  - No features lost during refactor

- [ ] **Configuration Management**
  - Environment variables load correctly from .env
  - Missing variables produce clear error messages
  - Settings class provides typed access

- [ ] **Error Handling**
  - Clear error messages for missing configuration
  - Import errors handled gracefully
  - Placeholder functions raise NotImplementedError with helpful messages

#### Code Quality Requirements

- [ ] **Linting**
  - No ruff/pylint errors
  - Follows PEP 8 style guidelines
  - Consistent code formatting

- [ ] **Separation of Concerns**
  - Config layer only handles configuration
  - Tools layer only defines tools
  - Agents layer only creates agents
  - No cross-layer dependencies (one-way: config → tools → agents)

- [ ] **Placeholder Clarity**
  - ADB functions clearly marked as not implemented
  - Vision module marked as reserved
  - Filesystem middleware marked as future work

---

### Overall Project Success Criteria (Future)

#### Functional Requirements (Phases 2-5)

- [ ] Connect to local Android device via ADB
- [ ] Execute basic UI operations (tap, swipe, input)
- [ ] Capture and analyze screen content
- [ ] Manage apps (launch, stop, list)
- [ ] Perform goal-oriented task sequences
- [ ] Provide clear error messages

#### Quality Requirements (Phases 2-5)

- [ ] Clean code structure with clear separation
- [ ] Type hints for all public functions
- [ ] Comprehensive logging at INFO level
- [ ] Friendly error messages
- [ ] Documentation in README

#### Usability Requirements (Phases 2-5)

- [ ] Simple CLI interface
- [ ] Easy configuration via .env
- [ ] Clear setup instructions
- [ ] Actionable error feedback

---

*Last Updated: 2025-01-09*

*Version: 0.2.0 (Phase 1 Focus)*

*Changes from v0.1.0:*
- Added quick reference section for Phase 1
- Expanded Phase 1 task list with detailed checkboxes
- Clarified that Phase 1 focuses on structure, not functionality
- Marked future phases as "Not Started" with trigger conditions
- Separated Phase 1 success criteria from overall project criteria
- Emphasized backward compatibility as primary success metric
