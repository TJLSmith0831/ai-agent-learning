"""
NAMESPACE for LLM clients
"""

from enum import Enum


class LLMClient(str, Enum):
    """
    Namespace for LLM clients
    """

    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class DocumentationFormat(str, Enum):
    """
    Namespace for documentation formats
    """

    MARKDOWN: str = "markdown"
    RST: str = "rst"
    NUMPY: str = "numpy"
    GOOGLE: str = "google"
    SPHINX: str = "sphinx"
    PLAIN: str = "plain"
    EPYTEXT: str = "epytext"
