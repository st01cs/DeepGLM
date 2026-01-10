"""Configuration management for DeepGLM Android Automation Agent.

This module loads and validates environment variables from a .env file,
providing typed access to configuration throughout the application.
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application configuration settings.

    This class provides type-safe access to environment variables
    and validates that required variables are present.

    Attributes:
        OPENAI_API_KEY: API key for OpenAI-compatible LLM service
        OPENAI_BASE_URL: Base URL for the API endpoint
        OPENAI_MODEL: Model identifier to use
        VISION_MODEL: Optional vision model for screen analysis
        TAVILY_API_KEY: API key for Tavily search service
        ADB_PATH: Path to adb executable (defaults to 'adb')
    """

    def __init__(self) -> None:
        """Initialize settings and validate required environment variables."""
        # Required variables
        self.OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
        self.OPENAI_BASE_URL: str = os.environ.get("OPENAI_BASE_URL", "")
        self.OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "")
        self.TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "")

        # Optional variables
        self.VISION_MODEL: str | None = os.environ.get("VISION_MODEL")
        self.ADB_PATH: str = os.environ.get("ADB_PATH", "adb")

        # Validate required variables
        required_vars = {
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
            "OPENAI_BASE_URL": self.OPENAI_BASE_URL,
            "OPENAI_MODEL": self.OPENAI_MODEL,
            "TAVILY_API_KEY": self.TAVILY_API_KEY,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            print(
                f"Error: Missing required environment variables: {', '.join(missing_vars)}"
            )
            print("Please set them in your .env file or environment.")
            sys.exit(1)


# Singleton instance
settings = Settings()
