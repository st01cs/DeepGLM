"""Custom exceptions for DeepGLM."""


class DeepGLMError(Exception):
    """Base exception for all DeepGLM errors."""


class ConfigurationError(DeepGLMError):
    """Base class for configuration-related errors."""


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing."""


class InvalidConfigError(ConfigurationError):
    """Raised when configuration values are invalid."""


class AgentError(DeepGLMError):
    """Base class for agent-related errors."""


class AgentCreationError(AgentError):
    """Raised when agent creation fails."""


class AgentExecutionError(AgentError):
    """Raised when agent execution fails."""


class ToolError(DeepGLMError):
    """Base class for tool-related errors."""


class ToolExecutionError(ToolError):
    """Raised when tool execution fails."""


class ToolNotFoundError(ToolError):
    """Raised when a requested tool is not found."""
