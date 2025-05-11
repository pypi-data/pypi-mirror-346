"""Custom exception classes for LitePrompt – wrapping PromptPoet's core exceptions."""

from prompt_poet.pp_exceptions import (
    TruncationError as _PromptPoetTruncationError,
)


class LitePromptError(Exception):
    """Base exception for all LitePrompt errors."""


class LiteTruncationError(_PromptPoetTruncationError, LitePromptError):
    """Raised when truncation fails to meet the token limit (from PromptPoet)."""
