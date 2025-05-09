"""Quote block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, Optional

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock


class QuoteBlock(BaseBlock):
    """A block containing a quotation.

    Attributes:
        text: The quoted text
        source: Optional source of the quote (author, book, etc.)
        citation: Optional formal citation
    """

    KIND: ClassVar[str] = "quote"

    def __init__(
        self,
        *,
        text: str,
        source: Optional[str] = None,
        citation: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a quote block.

        Args:
            text: The quoted text
            source: Optional source of the quote (author, book, etc.)
            citation: Optional formal citation
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "text": text,
        }

        if source is not None:
            payload["source"] = source

        if citation is not None:
            payload["citation"] = citation

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def text(self) -> str:
        """Get the quoted text.

        Returns:
            The quoted text
        """
        return self.payload.get("text", "")

    @property
    def source(self) -> Optional[str]:
        """Get the quote source.

        Returns:
            The quote source, or None if not set
        """
        return self.payload.get("source")

    @property
    def citation(self) -> Optional[str]:
        """Get the formal citation.

        Returns:
            The formal citation, or None if not set
        """
        return self.payload.get("citation")
