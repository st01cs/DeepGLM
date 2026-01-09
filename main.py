import os
import sys
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Validate required environment variables
    required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "TAVILY_API_KEY"]
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

    # 1. Initialize model
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
