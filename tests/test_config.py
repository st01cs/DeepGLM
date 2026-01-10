"""Test configuration loading and validation."""



def test_settings_instance():
    """Test that settings singleton exists."""
    from deepglm.config import settings
    assert settings is not None


def test_settings_has_required_attributes():
    """Test that settings has all required attributes."""
    from deepglm.config import settings

    required_attrs = [
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
        "OPENAI_MODEL",
        "TAVILY_API_KEY",
    ]
    for attr in required_attrs:
        assert hasattr(settings, attr), f"Settings missing {attr}"


def test_prompts_exist():
    """Test that prompts are defined."""
    from deepglm.config import prompts

    assert hasattr(prompts, "MAIN_AGENT_PROMPT")
    assert prompts.MAIN_AGENT_PROMPT != ""
    assert "Android automation" in prompts.MAIN_AGENT_PROMPT


def test_prompts_have_android_operator():
    """Test that Android operator prompts exist."""
    from deepglm.config import prompts

    assert hasattr(prompts, "ANDROID_OPERATOR_PROMPT")
    assert prompts.ANDROID_OPERATOR_PROMPT != ""
