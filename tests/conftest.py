"""Pytest configuration and fixtures for DeepGLM tests."""

import os
import sys
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(autouse=True)
def setup_test_env(project_root: Path) -> Generator[None, None, None]:
    """Set up test environment variables before all tests."""
    # Set test environment variables
    os.environ["OPENAI_API_KEY"] = "test_key"
    os.environ["OPENAI_BASE_URL"] = "http://localhost:8000"
    os.environ["OPENAI_MODEL"] = "test_model"
    os.environ["TAVILY_API_KEY"] = "test_tavily_key"

    yield

    # Clean up environment variables after tests
    for key in ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "TAVILY_API_KEY"]:
        os.environ.pop(key, None)


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def add_project_to_path(project_root: Path) -> Generator[None, None, None]:
    """Add project root to Python path for testing."""
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    yield
    if str(project_root) in sys.path:
        sys.path.remove(str(project_root))
