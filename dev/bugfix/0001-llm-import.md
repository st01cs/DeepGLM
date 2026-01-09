# Bug Fix Specification: LLM Import Error

## Bug Summary

**Error**: `ModuleNotFoundError: No module named 'langchain_deepseek'`

**Root Cause**: Using `init_chat_model()` with model name `"deepseek-ai/DeepSeek-V3.2"` causes LangChain to attempt importing the non-existent `langchain-deepseek` package, instead of using OpenAI-compatible API mode.

**User Intent**: Use OpenAI-compatible API (e.g., DeepSeek via `OPENAI_BASE_URL`) without requiring provider-specific packages.

## Technical Analysis

### Current Implementation (Broken)

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model=os.environ.get("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2"),
)
```

**Problem**: `init_chat_model()` tries to be smart by detecting provider from model name prefix. When it sees `"deepseek-ai/*"`, it attempts to import `langchain-deepseek`, which doesn't exist.

### User Requirements

From 5 rounds of in-depth interview:

1. **Solution Approach**: Use "底层 API 调用" (bottom-level API calls)
2. **Package Choice**: `langchain-openai` with `ChatOpenAI` class
3. **Configuration**: Only `.env` file, no CLI args
4. **Priority**: Quick fix over elegant architecture
5. **Backward Compatibility**: No requirements
6. **Environment Variables**: Rename `MODEL_NAME` to `OPENAI_MODEL`
7. **Model Format**: Full path like `"deepseek-ai/DeepSeek-V3.2"`
8. **Parameters**: Minimal set (only model, api_key, base_url)
9. **Dependencies**: No changes to `pyproject.toml`
10. **Default Values**: Both `OPENAI_MODEL` and `OPENAI_BASE_URL` must be set
11. **Testing**: No automated tests required
12. **Documentation**: Code-only fix, no doc updates

## Fix Strategy

### Approach: Direct ChatOpenAI Instantiation

Replace `init_chat_model()` with direct `ChatOpenAI` class instantiation:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=os.environ["OPENAI_MODEL"],
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)
```

**Benefits**:
- Bypasses provider detection logic
- Works with any OpenAI-compatible API
- No provider-specific package dependencies
- Simple and direct

## Implementation Plan

### Code Changes

#### 1. Import Statement (Line 6)

**Before**:
```python
from langchain.chat_models import init_chat_model
```

**After**:
```python
from langchain_openai import ChatOpenAI
```

#### 2. Model Initialization (Lines 34-37)

**Before**:
```python
# 1. Initialize model (reads OPENAI_API_KEY, OPENAI_BASE_URL from env)
model = init_chat_model(
    model=os.environ.get("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2"),
)
```

**After**:
```python
# 1. Initialize model
model = ChatOpenAI(
    model=os.environ["OPENAI_MODEL"],
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)
```

#### 3. Required Environment Variables Validation (Lines 14-22)

**Before**:
```python
# Validate required environment variables
required_vars = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]
```

**After**:
```python
# Validate required environment variables
required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "TAVILY_API_KEY"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]
```

### Environment Variable Changes

#### .env.example

**Before**:
```bash
# Model Provider (OpenAI-compatible API)
OPENAI_API_KEY="sk-your-api-key-here"
OPENAI_BASE_URL="https://api.deepseek.com"
MODEL_NAME="deepseek-chat"
```

**After**:
```bash
# Model Provider (OpenAI-compatible API)
OPENAI_API_KEY="sk-your-api-key-here"
OPENAI_BASE_URL="https://api.deepseek.com"
OPENAI_MODEL="deepseek-ai/DeepSeek-V3.2"
```

**Key Changes**:
- `MODEL_NAME` → `OPENAI_MODEL`
- Default value changed to full path format
- Both `OPENAI_BASE_URL` and `OPENAI_MODEL` are now required

## Detailed Code Changes

### main.py (Complete Modified Section)

```python
import os
import sys
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI  # Changed: import
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Validate required environment variables
    required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "TAVILY_API_KEY"]  # Changed: added OPENAI_BASE_URL and OPENAI_MODEL
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(
            f"Error: Missing required environment variables: {', '.join(missing_vars)}"
        )
        print("Please set them in your .env file or environment.")
        sys.exit(1)

    # Get user query from command line argument
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        print('Usage: python main.py "your research question"')
        print(
            'Example: python main.py "What are the latest developments in quantum computing?"'
        )
        sys.exit(1)

    # 1. Initialize model  # Changed: direct ChatOpenAI instantiation
    model = ChatOpenAI(
        model=os.environ["OPENAI_MODEL"],
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"],
    )

    # 2. Initialize tools
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    def internet_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
    ):
        """Run a web search using Tavily."""
        return tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )

    # 3. System prompt
    research_instructions = """You are an expert researcher. Your job is to write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## Internet Search Usage

Use the internet_search tool ONLY when:
- The user explicitly asks you to search for information
- The user asks questions that require current or external information
- The user requests fact-checking or verification

Do NOT search autonomously. If the user's question can be answered from your training data, answer directly without searching.

## Response Guidelines

- Provide clear, concise, well-structured responses
- Focus on the most relevant information
- No need to cite sources explicitly in your response
- Prioritize accuracy and clarity over comprehensiveness
"""

    # 4. Create agent
    agent = create_deep_agent(
        model=model, tools=[internet_search], system_prompt=research_instructions
    )

    # 5. Execute
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": user_query}]})

        # 6. Output
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Dependencies

### pyproject.toml

**No changes required.**

**Rationale**: `langchain-openai` is already a transitive dependency of `deepagents>=0.3.4`. The `ChatOpenAI` class is available without explicitly adding it to `pyproject.toml`.

To verify, check:
```bash
.venv/bin/python -c "from langchain_openai import ChatOpenAI; print('OK')"
```

If this fails, add to `pyproject.toml`:
```toml
dependencies = [
    "deepagents>=0.3.4",
    "tavily-python>=0.7.17",
    "python-dotenv>=1.0.0",
    "langchain-openai>=0.1.0",  # Only if needed
]
```

## Testing Strategy

### Manual Verification

Since no automated tests are required, manual verification steps:

1. **Update .env file**:
   ```bash
   cp .env.example .env
   # Edit .env with actual API keys
   ```

2. **Verify imports**:
   ```bash
   .venv/bin/python -c "from langchain_openai import ChatOpenAI; print('Import OK')"
   ```

3. **Run with a simple query**:
   ```bash
   python main.py "Explain what is Python"
   ```

4. **Verify error handling**:
   ```bash
   # Temporarily remove OPENAI_BASE_URL from .env
   python main.py "test"
   # Should show: "Error: Missing required environment variables: OPENAI_BASE_URL"
   ```

## Error Behavior

### Before Fix

```
ImportError: Could not import langchain-deepseek python package.
Please install it with `pip install langchain-deepseek`
```

### After Fix

**If OPENAI_BASE_URL or OPENAI_MODEL is missing**:
```
Error: Missing required environment variables: OPENAI_BASE_URL, OPENAI_MODEL
Please set them in your .env file or environment.
```

**If API key is invalid**:
```
Error during execution: Authentication error
```

**If everything is correct**:
```
[Normal agent response]
```

## Migration Guide for Users

### Step 1: Update .env file

Rename or add environment variable:

**Old**:
```bash
MODEL_NAME="deepseek-chat"
```

**New**:
```bash
OPENAI_MODEL="deepseek-ai/DeepSeek-V3.2"
OPENAI_BASE_URL="https://api.deepseek.com"
```

### Step 2: Ensure all required variables are set

Required variables:
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL` ← **New requirement**
- `OPENAI_MODEL` ← **Renamed from MODEL_NAME**
- `TAVILY_API_KEY`

### Step 3: Verify configuration

```bash
python main.py "test query"
```

## Common Configurations

### DeepSeek
```bash
OPENAI_API_KEY="sk-xxx"
OPENAI_BASE_URL="https://api.deepseek.com"
OPENAI_MODEL="deepseek-ai/DeepSeek-V3.2"
```

### OpenAI (GPT-4)
```bash
OPENAI_API_KEY="sk-xxx"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_MODEL="gpt-4o"
```

### Together AI
```bash
OPENAI_API_KEY="xxx"
OPENAI_BASE_URL="https://api.together.xyz/v1"
OPENAI_MODEL="meta-llama/Llama-3-70b-chat-hf"
```

## Rationale & Design Decisions

### Why ChatOpenAI instead of init_chat_model?

1. **Provider Detection**: `init_chat_model` tries to detect provider from model name, causing import errors
2. **Explicit Configuration**: `ChatOpenAI` requires explicit `base_url`, avoiding ambiguity
3. **Simplicity**: Direct class instantiation is easier to understand and debug
4. **Compatibility**: Works with any OpenAI-compatible API without provider-specific packages

### Why rename MODEL_NAME to OPENAI_MODEL?

1. **Clarity**: Name explicitly indicates it's for OpenAI-compatible API
2. **Consistency**: Matches other `OPENAI_*` environment variables
3. **User Intent**: Aligns with user's choice of "底层 API 调用" approach

### Why require OPENAI_BASE_URL?

1. **Explicit Configuration**: Forces users to be explicit about API endpoint
2. **Error Prevention**: Prevents accidentally calling wrong API
3. **OpenAI Compatibility**: OpenAI-compatible APIs require custom `base_url`

### Minimal parameter set?

1. **User Preference**: Interview confirmed "最小参数" approach
2. **Simplicity**: Avoids unnecessary complexity
3. **Sufficient**: `model`, `api_key`, `base_url` are sufficient for basic usage

## Potential Issues & Mitigations

### Issue 1: langchain_openai not available

**Symptom**: `ModuleNotFoundError: No module named 'langchain_openai'`

**Solution**:
```bash
uv sync
# or
.venv/bin/python -m pip install langchain-openai
```

### Issue 2: Incorrect model name format

**Symptom**: API returns "model not found" error

**Solution**: Verify model name matches provider's expected format
- DeepSeek: Use full path like `"deepseek-ai/DeepSeek-V3.2"`
- OpenAI: Use short name like `"gpt-4o"`

### Issue 3: Base URL missing trailing path

**Symptom**: 404 or authentication errors

**Solution**: Ensure `base_url` includes full path
- Correct: `"https://api.deepseek.com"` or `"https://api.deepseek.com/v1"`
- Check provider documentation for correct format

## Future Improvements (Out of Scope)

Based on interview responses, these are explicitly out of scope:

- ❌ Automatic provider detection
- ❌ Support for multiple providers in same codebase
- ❌ Configuration validation beyond required variables
- ❌ Default values for model or base_url
- ❌ Advanced parameters (temperature, max_tokens, etc.)
- ❌ Automated tests
- ❌ Documentation updates (README.md)
- ❌ Backward compatibility with `MODEL_NAME`

## Summary

**Change**: 3 lines of code in `main.py`, 1 variable rename in `.env.example`

**Impact**: Fixes import error, enables any OpenAI-compatible API

**Risk**: Low - direct replacement, no architectural changes

**Effort**: Minimal - < 5 minutes to implement

**Testing**: Manual verification sufficient per user requirements

---

**Bug Fix Version**: 1.0
**Date**: 2025-01-09
**Status**: Ready for Implementation
**Interview Rounds**: 5 (25 questions total)
