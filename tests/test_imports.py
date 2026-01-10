"""Test that all deepglm modules can be imported correctly."""



def test_import_deepglm_package():
    """Test that the deepglm package can be imported."""
    import deepglm
    assert deepglm is not None


def test_import_deepglm_agents():
    """Test that deepglm.agents can be imported."""
    from deepglm import agents
    assert agents is not None


def test_import_main_agent():
    """Test that the main agent factory can be imported."""
    from deepglm.agents.main_agent import create_android_agent
    assert create_android_agent is not None


def test_import_config():
    """Test that config module can be imported."""
    from deepglm.config import prompts, settings
    assert prompts is not None
    assert settings is not None


def test_import_tools():
    """Test that tools can be imported."""
    from deepglm.tools import internet_search
    assert internet_search is not None


def test_import_exceptions():
    """Test that custom exceptions can be imported."""
    from deepglm.exceptions import (
        AgentError,
        ConfigurationError,
        DeepGLMError,
        MissingConfigError,
        ToolError,
    )
    assert DeepGLMError is not None
    assert ConfigurationError is not None
    assert MissingConfigError is not None
    assert AgentError is not None
    assert ToolError is not None


def test_public_api_exports():
    """Test that public API is properly exported."""
    import deepglm

    # Check that expected symbols are in __all__
    assert hasattr(deepglm, "__all__")
    expected_exports = ["create_android_agent", "prompts", "settings"]
    for export in expected_exports:
        assert export in deepglm.__all__, f"{export} not in __all__"
        assert hasattr(deepglm, export), f"{export} not exported from package"
