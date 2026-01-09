# DeepGLM Research Agent

A streamlined research and knowledge work assistant built as a single-agent CLI tool. DeepGLM focuses on simplicity, directness, and extensibility while providing powerful internet search capabilities powered by open-source LLMs.

## Features

- **Monolithic Architecture**: Single agent with tool-based extensibility
- **Explicit Search Control**: Agent searches only when you explicitly request it
- **Open-Source Models**: Works with DeepSeek and other OpenAI-compatible APIs
- **LangSmith Integration**: Built-in execution tracing for debugging
- **Simple Configuration**: Environment-based configuration, no complex setup

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

Create a `.env` file in the project root with your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# Required: Model Provider (OpenAI-compatible API)
OPENAI_API_KEY="sk-your-api-key-here"
OPENAI_BASE_URL="https://api.deepseek.com"
MODEL_NAME="deepseek-chat"

# Required: Search
TAVILY_API_KEY="tvly-your-tavily-api-key-here"

# Optional: LangSmith Tracing
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="lsv2-your-langsmith-api-key-here"
LANGCHAIN_PROJECT="deepglm-research"
```

### Getting API Keys

- **DeepSeek**: Get your API key from [https://platform.deepseek.com](https://platform.deepseek.com)
- **Tavily**: Get your API key from [https://tavily.com](https://tavily.com)
- **LangSmith**: Get your API key from [https://smith.langchain.com](https://smith.langchain.com)

## Usage

### Basic Usage

Run DeepGLM with your research question as a command-line argument:

```bash
python main.py "What are the latest developments in quantum computing?"
```

### Examples

**Search for current information:**
```bash
python main.py "What are today's major technology headlines?"
```

**General knowledge questions (no search):**
```bash
python main.py "Explain the concept of machine learning"
```

**Finance-specific search:**
```bash
python main.py "What's the current stock market trend?"
```

**News search:**
```bash
python main.py "Search for recent developments in artificial intelligence"
```

### How It Works

1. **No Search Needed**: If your question can be answered from the model's training data, it responds directly without searching
2. **Explicit Search**: If you ask for current information, explicitly request search, or ask questions requiring external data, the agent uses the internet search tool
3. **Transparent Behavior**: All agent actions are traceable via LangSmith (if configured)

## Architecture

### Design Principles

- **Simplicity First**: Minimal abstractions, direct implementations
- **Explicit Control**: User-initiated search triggers, no autonomous decisions
- **Transparent Failures**: Clear error messages without complex retry logic
- **Extensibility**: Easy to add new tools via code
- **No Constraints**: Unlimited execution, no filtering, no caching

### Tool Extension

You can easily add new tools by defining functions and passing them to the agent:

```python
def calculator(expression: str) -> float:
    """Evaluate a mathematical expression"""
    return eval(expression)

agent = create_deep_agent(
    model=model,
    tools=[internet_search, calculator],
    system_prompt=research_instructions
)
```

## Development

### Project Structure

```
deepglm/
├── main.py              # Entry point
├── pyproject.toml       # Dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

### Dependencies

- `deepagents>=0.3.4` - Agent framework
- `tavily-python>=0.7.17` - Search API
- `python-dotenv>=1.0.0` - Environment variable loading

## Troubleshooting

### Missing Environment Variables

If you see an error about missing environment variables, ensure your `.env` file is properly configured:

```bash
# Check if .env exists
ls -la .env

# Verify required variables are set
grep OPENAI_API_KEY .env
grep TAVILY_API_KEY .env
```

### LangSmith Tracing Not Working

Ensure the following environment variables are set in your `.env`:

```bash
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="lsv2-your-key"
LANGCHAIN_PROJECT="deepglm-research"
```

### Model Connection Issues

If you're using DeepSeek, verify:
- `OPENAI_API_KEY` is correct
- `OPENAI_BASE_URL` is set to `https://api.deepseek.com`
- `MODEL_NAME` is set to `deepseek-chat`

## Limitations

- **Single-turn conversation**: No multi-turn context maintenance
- **No streaming**: Complete response returned at once
- **Plain text output**: No Markdown or rich formatting
- **No caching**: Every search is real-time
- **No content filtering**: User responsible for content evaluation

## Future Enhancements

Potential future improvements (only if needed):

- Phase 2: Tool expansion (code execution, file operations)
- Phase 3: Rich interaction (multi-turn, streaming, Markdown)
- Phase 4: Advanced features (long-term memory, knowledge base)

**Key Principle**: Complexity is only added when proven necessary by actual use cases.

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
