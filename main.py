"""DeepGLM Android Automation Agent - Main Entry Point

This script provides a command-line interface for interacting with
the DeepGLM Android automation agent.

Usage:
    python main.py "your task description"

Example:
    python main.py "Research the latest Android automation techniques"
"""

import sys

from agents.main_agent import create_android_agent

# Import settings to trigger validation
import config.settings  # noqa: F401


def main():
    """Main entry point for the DeepGLM Android automation agent.

    This function:
    1. Validates configuration (via Settings class)
    2. Gets user query from command line arguments
    3. Creates the agent with configured tools
    4. Executes the query and prints results
    """
    # Get user query from command line argument
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        print('Usage: python main.py "your task description"')
        print(
            'Example: python main.py "What are the latest developments in quantum computing?"'
        )
        sys.exit(1)

    # Create agent using factory function
    # Note: Settings validation happens automatically during import
    agent = create_android_agent()

    # Execute user query
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": user_query}]})

        # Print the result
        print(result["messages"][-1].content)
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
