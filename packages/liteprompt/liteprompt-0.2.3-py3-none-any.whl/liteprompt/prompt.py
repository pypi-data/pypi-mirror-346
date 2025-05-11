from prompt_poet.prompt import Prompt as BasePrompt
from prompt_poet.prompt import PromptPart as BasePromptPart
from dataclasses import dataclass, field
from prompt_poet.prompt import TruncationBlock as BaseTruncationBlock
from typing import Optional, Any
from prompt_poet.template import Template
import yaml


class LiteTemplate(Template):
    """Custom template class inheriting from Template."""

    pass


@dataclass
class LitePromptPart(BasePromptPart):
    """Extended PromptPart with tool_calls and related attributes."""

    tool_calls: Optional[Any] = None
    function_call: Optional[Any] = None
    tool_call_id: Optional[str] = None

    _original_fields: Optional[dict] = field(default=None, repr=False)

    def to_dict(self):
        """Convert the PromptPart to a dictionary, excluding 'id'."""
        d = self._original_fields.copy() if self._original_fields else {}
        d.pop("id", None)
        return d


@dataclass
class LiteTruncationBlock(BaseTruncationBlock):
    """Extended TruncationBlock with optional metadata."""

    metadata: Optional[dict] = None


class LitePrompt(BasePrompt):
    """A custom extension of the Prompt class with injected behavior."""

    def __init__(self, *args, **kwargs):
        if kwargs.get("raw_template") and "template_path" not in kwargs:
            kwargs["template_path"] = ""
        super().__init__(*args, **kwargs)

    def messages(self):
        """Override the messages property to use the LitePromptPart to_dict."""
        return [part.to_dict() for part in self._parts]

    def _render_parts(self):
        """Override the render_parts method to handle LitePromptPart."""
        self._rendered_template = self._template.render_template(self._template_data)
        loaded_yaml = yaml.safe_load(self._rendered_template)

        self._parts = []
        for yaml_part in loaded_yaml:
            part = LitePromptPart(**yaml_part)
            part._original_fields = yaml_part
            self._validate_template_replacements(part)
            self._cleanup_content(part)
            self._parts.append(part)

    def _cleanup_content(self, part):
        """Override the content cleanup to handle whitespace and special characters."""
        if isinstance(part.content, str):
            cleaned = part.content.strip().replace(self._space_marker, " ")
            part.content = self._unescape_special_characters(cleaned)
