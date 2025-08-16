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
