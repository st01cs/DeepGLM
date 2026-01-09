# DeepGLM Research Agent - Technical Specification

## Project Overview

**DeepGLM** is a streamlined research and knowledge work assistant built as a single-agent CLI tool. It focuses on simplicity, directness, and extensibility while providing powerful internet search capabilities powered by open-source LLMs.

## Core Philosophy

- **Simplicity First**: Minimal abstractions, direct implementations
- **Explicit Control**: User-initiated search triggers, no autonomous decisions
- **Transparent Failures**: Clear error messages without complex retry logic
- **Extensibility**: Easy to add new tools via code
- **No Constraints**: Unlimited execution, no filtering, no caching, no timeout limits

## Architecture

### Type: Monolithic Single-Agent
- Single agent handling all tasks
- Tool-based extensibility
- No sub-agents or routing complexity
- Direct tool invocation

### Memory Strategy
- **Short-term**: Session-based conversation context only
- **No long-term memory** persistence
- **No knowledge graph** or knowledge base construction
- Stateless between runs

### Model
- **Primary**: DeepSeek (or compatible open-source models)
- **Fallback**: Can be configured via environment variables
- **Reasoning Mode**: Fast inference (no chain-of-thought overhead)
- **Provider**: Configurable via LangChain `init_chat_model()`

## Tool Ecosystem

### Core Tool: Internet Search

**Implementation**: Tavily Client

**Parameters** (System defaults, not user-configurable):
```python
max_results: int = 5
topic: Literal["general", "news", "finance"] = "general"
include_raw_content: bool = False
search_depth: str = "basic"  # Shallow search
```

**Triggering**: Explicit user invocation only
- Agent does NOT autonomously decide to search
- User must explicitly request information that requires search
- Prompt engineering to reinforce explicit trigger behavior

**Search Strategy**:
- Single source: Tavily internet search only
- No multi-source fusion (simplified from initial concept)
- Direct result concatenation
- No result caching
- No deduplication or post-processing

### Tool Extension Mechanism

**Approach**: Direct code addition

```python
# Pattern for adding new tools
def new_tool(param: type, ...) -> ReturnType:
    """Tool description for agent"""
    # Implementation
    return result

# Register in agent creation
agent = create_deep_agent(
    model=model,
    tools=[internet_search, new_tool],  # Add here
    system_prompt=system_prompt
)
```

**Future Considerations**:
- Plugin system if tool count > 5
- Configuration-based registration for dynamic loading
- Keep it simple until proven necessary

### Tool Candidates (Future)
- Python code execution (if calculation needs emerge)
- File system operations (if local file access needed)
- Additional search sources (academic, code, news)

## User Interface & Experience

### Interaction Mode
- **Type**: Single-turn conversation
- No multi-turn context maintenance
- No interactive clarification from agent
- No interruptibility during execution

### Input/Output
- **Input**: Command-line arguments or stdin
- **Output**: Non-streaming (complete response at once)
- **Format**: Plain text (no Markdown, no rich formatting)
- **Citations**: None (search sources not explicitly referenced)

### Deployment
- **Form**: Command-line tool
- **Execution**: Direct Python script execution
- **Distribution**: Standard Python package (via pyproject.toml)

### Error Handling
- **Strategy**: Transparent failure
- **Message Style**: User-friendly error descriptions
- **Behavior**: Report errors and halt execution
- No retry logic
- No graceful degradation
- No fallback mechanisms

## System Prompt Design

### Core Identity
```
You are an expert researcher. Your job is to write a polished report.

You have access to an internet search tool as your primary means of gathering information.
```

### Tool Behavior Guidelines
```
## Internet Search Usage

Use the internet_search tool ONLY when:
- The user explicitly asks you to search for information
- The user asks questions that require current or external information
- The user requests fact-checking or verification

Do NOT search autonomously. If the user's question can be answered from your training data, answer directly without searching.
```

### Response Guidelines
```
- Provide clear, concise, well-structured responses
- Focus on the most relevant information
- No need to cite sources explicitly in your response
- Prioritize accuracy and clarity over comprehensiveness
```

## Configuration Management

### Method: Environment Variables

**Required Variables**:
```bash
# Model Provider (OpenAI-compatible API)
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com  # or custom endpoint

# Search
TAVILY_API_KEY=tvly-xxx

# Optional: LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_xxx
LANGCHAIN_PROJECT=deepglm-research
```

**Model Configuration**:
```python
model = init_chat_model(model="deepseek-chat")  # or "gpt-4o", etc.
```

### No Configuration Files
- No YAML/TOML config files
- No command-line argument parsing
- All configuration via environment variables only

## Observability & Monitoring

### LangSmith Integration

**Purpose**: Execution tracing for debugging and understanding agent behavior

**Configuration**:
```python
# Automatic tracing when env vars are set
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "lsv2_xxx"
os.environ["LANGCHAIN_PROJECT"] = "deepglm-research"
```

**What Gets Traced**:
- All LLM calls
- Tool invocations
- Agent reasoning steps
- Final outputs

**What Does NOT Get Traced**:
- Search results content (to reduce noise)
- Intermediate computations
- User PII (if present)

### No Logging
- No file-based logging
- No log levels
- No structured logging
- Rely on LangSmith for debugging needs

### No Metrics/Monitoring
- No cost tracking
- No usage statistics
- No performance metrics
- No alerting

## Constraints & Boundaries

### Cost Control: None
- Unlimited token usage
- Unlimited search calls
- No budget limits
- No usage quotas

### Content Filtering: None
- No content safety filters
- No quality assessment
- No source reliability checks
- User responsible for content evaluation

### Time Limits: None
- No global timeout
- No tool-level timeout
- No execution time limits
- Tasks run to completion or failure

### Caching: None
- No search result caching
- No response caching
- No session or persistent cache
- Every search is real-time

## Implementation Structure

### Project Layout
```
deepglm/
├── main.py                 # Entry point
├── pyproject.toml          # Dependencies
├── .env.example            # Environment template
├── README.md               # Usage documentation
└── dev/
    ├── plan/
    │   └── 0000-start.md  # This specification
    └── refs/
        └── deepagents.md   # DeepAgents reference
```

### Dependencies
```
deepagents>=0.3.4    # Agent framework
tavily-python>=0.7.17  # Search API
langchain>=0.3        # LLM integration
python-dotenv>=1.0.0  # Environment variable loading
```

### Code Structure (main.py)
```python
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # 1. Initialize model (reads OPENAI_API_KEY, OPENAI_BASE_URL from env)
    model = init_chat_model(model="deepseek-chat")

    # 2. Initialize tools
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    def internet_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
    ):
        """Run a web search"""
        return tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )

    # 3. System prompt
    research_instructions = """You are an expert researcher..."""

    # 4. Create agent
    agent = create_deep_agent(
        model=model,
        tools=[internet_search],
        system_prompt=research_instructions
    )

    # 5. Execute
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "..."}]}
    )

    # 6. Output
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
```

## Usage Examples

### Basic Research Query
```bash
# Search required
python main.py "What are the latest developments in quantum computing?"

# No search needed
python main.py "Explain the concept of machine learning."
```

### Different Search Topics
```bash
# General (default)
python main.py "Search for information about renewable energy trends"

# News
python main.py "What are today's major technology headlines?"

# Finance
python main.py "What's the current stock market trend?"
```

### Tool Extension Example
```python
# Adding a calculator tool
def calculator(expression: str) -> float:
    """Evaluate a mathematical expression"""
    return eval(expression)

agent = create_deep_agent(
    model=model,
    tools=[internet_search, calculator],
    system_prompt=research_instructions
)
```

## Design Rationale

### Why Monolithic Architecture?
- **Simplicity**: No routing logic, no sub-agent coordination
- **Performance**: No inter-agent communication overhead
- **Debuggability**: Single execution flow, easier to trace
- **Adequate**: Research tasks don't require complex orchestration

### Why Explicit Search Triggering?
- **Cost Control**: Prevents unnecessary API calls
- **Predictability**: User knows when searches happen
- **Transparency**: Clear separation between knowledge and retrieval
- **Privacy**: User controls what information is looked up

### Why No Caching?
- **Freshness**: Research often needs current information
- **Simplicity**: No cache invalidation logic
- **Cost**: Caching complexity outweighs benefits for this use case
- **Scale**: Not enough volume to make caching worthwhile

### Why Plain Text Output?
- **Universality**: Works everywhere, no rendering needed
- **Simplicity**: No formatting or template logic
- **Flexibility**: User can pipe/redirect output as needed
- **Adequacy**: Research reports don't need rich formatting

### Why LangSmith but No Logging?
- **Tracing > Logging**: LangSmith provides richer debugging info
- **Structured Data**: Easier to analyze than text logs
- **No Noise**: Don't clutter filesystem with log files
- **Integrated**: Single observability platform

## Future Evolution Paths

### Phase 1: Current (MVP)
- Single search tool
- Basic research queries
- Command-line interface
- LangSmith tracing

### Phase 2: Tool Expansion (If Needed)
- Add calculation tool (Python code execution)
- Add file operations (read/write local files)
- Add additional search sources (academic, code)
- Improve tool error handling

### Phase 3: Rich Interaction (If Needed)
- Multi-turn conversations
- Streaming output
- Markdown formatting
- Source citations

### Phase 4: Advanced Features (If Needed)
- Long-term memory (vector store)
- Knowledge base construction
- Sub-agent delegation
- Custom tools via plugins

**Key Principle**: Only add complexity when proven necessary by actual use cases.

## Non-Goals

### Explicitly Out of Scope
- ❌ Multi-agent systems
- ❌ Long-term memory/knowledge persistence
- ❌ Complex UI (web, mobile)
- ❌ Real-time streaming
- ❌ Rich formatting (Markdown, HTML, PDF)
- ❌ Source citation management
- ❌ Advanced search (semantic, hybrid)
- ❌ Content filtering or safety checks
- ❌ Cost optimization (caching, batching)
- ❌ Enterprise features (auth, multi-tenancy)
- ❌ Production deployment (Docker, cloud)

## Success Criteria

### Functional Requirements
- ✅ Can answer questions from training data without search
- ✅ Can search internet when explicitly requested
- ✅ Returns coherent, well-structured research reports
- ✅ Handles errors gracefully with clear messages
- ✅ Easy to add new tools via code

### Non-Functional Requirements
- ✅ Simple to understand and modify
- ✅ Fast response times (no unnecessary tool calls)
- ✅ Transparent behavior (visible via LangSmith)
- ✅ Works with open-source models (DeepSeek)
- ✅ Minimal dependencies

### User Experience
- ✅ Clear command-line interface
- ✅ Predictable behavior
- ✅ No hidden costs or surprises
- ✅ Easy debugging (via LangSmith)

## Open Questions & Decisions Required

1. **Model Specific**: Which specific DeepSeek model? (deepseek-chat, deepseek-coder, etc.)
2. **Input Method**: Command-line argument vs. stdin vs. interactive prompt?
3. **Topic Default**: Should `topic` default to "general" or be inferred from query?
4. **Result Limitation**: Is 5 results always appropriate, or should it vary?
5. **Search Quality**: Any post-processing needed on Tavily results?

## Implementation Priority

### P0 (Must Have)
- Basic agent with Tavily search
- Environment variable configuration (.env loading)
- LangSmith tracing
- Error handling

### P1 (Should Have)
- Clear system prompt
- Documentation (README)
- Usage examples
- .env.example

### P2 (Nice to Have)
- Additional tools (if needed)
- Input validation
- Better error messages
- Performance tuning

### P3 (Future)
- Multi-turn conversation
- Streaming output
- Tool extension framework
- Advanced search features

---

**Specification Version**: 1.0
**Last Updated**: 2025-01-09
**Status**: Ready for Implementation
