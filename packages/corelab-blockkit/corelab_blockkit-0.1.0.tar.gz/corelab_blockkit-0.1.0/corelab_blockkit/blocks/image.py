"""Image block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, Optional

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock


class ImageBlock(BaseBlock):
    """A block containing an image.

    Attributes:
        url: The URL of the image
        alt_text: Alternative text for the image
        caption: Optional caption for the image
        width: Optional width of the image
        height: Optional height of the image
    """

    KIND: ClassVar[str] = "image"

    def __init__(
        self, 
        *,
        url: str,
        alt_text: str = "",
        caption: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize an image block.

        Args:
            url: The URL of the image
            alt_text: Alternative text for the image
            caption: Optional caption for the image
            width: Optional width of the image
            height: Optional height of the image
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "url": url,
            "alt_text": alt_text,
        }

        if caption is not None:
            payload["caption"] = caption

        if width is not None:
            payload["width"] = width

        if height is not None:
            payload["height"] = height

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def url(self) -> str:
        """Get the image URL.

        Returns:
            The image URL
        """
        return self.payload.get("url", "")

    @property
    def alt_text(self) -> str:
        """Get the alternative text.

        Returns:
            The alternative text
        """
        return self.payload.get("alt_text", "")

    @property
    def caption(self) -> Optional[str]:
        """Get the caption.

        Returns:
            The caption, or None if not set
        """
        return self.payload.get("caption")

    @property
    def width(self) -> Optional[int]:
        """Get the width.

        Returns:
            The width, or None if not set
        """
        return self.payload.get("width")

    @property
    def height(self) -> Optional[int]:
        """Get the height.

        Returns:
            The height, or None if not set
        """
        return self.payload.get("height")
