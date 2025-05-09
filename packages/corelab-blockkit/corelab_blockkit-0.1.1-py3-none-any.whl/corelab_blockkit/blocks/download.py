"""Download block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, Optional, Union

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.enums import MimeType


class DownloadBlock(BaseBlock):
    """A block containing a downloadable file.

    Attributes:
        url: The URL of the file to download
        filename: The suggested filename for the download
        title: Optional title or description of the file
        size: Optional size of the file in bytes
        mime_type: Optional MIME type of the file
    """

    KIND: ClassVar[str] = "download"

    def __init__(
        self,
        *,
        url: str,
        filename: str,
        title: Optional[str] = None,
        size: Optional[int] = None,
        mime_type: Optional[Union[MimeType, str]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a download block.

        Args:
            url: The URL of the file to download
            filename: The suggested filename for the download
            title: Optional title or description of the file
            size: Optional size of the file in bytes
            mime_type: Optional MIME type of the file (e.g., MimeType.APPLICATION_PDF)
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "url": url,
            "filename": filename,
        }

        if title is not None:
            payload["title"] = title

        if size is not None:
            payload["size"] = size

        if mime_type is not None:
            # Convert mime_type to string if it's an enum
            mime_type_value = (
                mime_type.value if isinstance(mime_type, MimeType) else mime_type
            )
            payload["mime_type"] = mime_type_value

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def url(self) -> str:
        """Get the download URL.

        Returns:
            The download URL
        """
        return self.payload.get("url", "")

    @property
    def filename(self) -> str:
        """Get the suggested filename.

        Returns:
            The suggested filename
        """
        return self.payload.get("filename", "")

    @property
    def title(self) -> Optional[str]:
        """Get the file title.

        Returns:
            The file title, or None if not set
        """
        return self.payload.get("title")

    @property
    def size(self) -> Optional[int]:
        """Get the file size.

        Returns:
            The file size in bytes, or None if not set
        """
        return self.payload.get("size")

    @property
    def mime_type(self) -> Optional[MimeType]:
        """Get the MIME type.

        Returns:
            The MIME type as a MimeType enum, or None if not set
        """
        mime_type_str = self.payload.get("mime_type")
        if mime_type_str is None:
            return None

        try:
            return MimeType(mime_type_str)
        except ValueError:
            # If the mime_type string doesn't match any enum value, return None
            return None
