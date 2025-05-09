"""Text block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, Optional, Union

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.enums import TextFormat


class TextBlock(BaseBlock):
    """A block containing formatted text.

    Attributes:
        text: The text content, which may include Markdown formatting
        format: The format of the text (e.g., "markdown", "plain")
    """

    KIND: ClassVar[str] = "text"

    def __init__(
        self,
        *,
        text: str,
        format: Union[TextFormat, str] = TextFormat.MARKDOWN,
        **kwargs: Any,
    ) -> None:
        """Initialize a text block.

        Args:
            text: The text content
            format: The format of the text (default: TextFormat.MARKDOWN)
            **kwargs: Additional arguments to pass to BaseBlock
        """
        # Convert format to string if it's an enum
        format_value = format.value if isinstance(format, TextFormat) else format

        payload = {
            "text": text,
            "format": format_value,
        }
        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def text(self) -> str:
        """Get the text content.

        Returns:
            The text content
        """
        return self.payload.get("text", "")

    @property
    def format(self) -> TextFormat:
        """Get the text format.

        Returns:
            The text format as a TextFormat enum
        """
        format_str = self.payload.get("format", "markdown")
        try:
            return TextFormat(format_str)
        except ValueError:
            # If the format string doesn't match any enum value, return MARKDOWN
            return TextFormat.MARKDOWN
