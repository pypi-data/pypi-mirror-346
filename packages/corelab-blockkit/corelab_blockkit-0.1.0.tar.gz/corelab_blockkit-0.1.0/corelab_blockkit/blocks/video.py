"""Video block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, Optional, Union

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.enums import VideoProvider


class VideoBlock(BaseBlock):
    """A block containing a video.

    Attributes:
        url: The URL of the video
        title: The title of the video
        description: Optional description of the video
        thumbnail_url: Optional URL of a thumbnail image
        duration: Optional duration of the video in seconds
        provider: Optional provider of the video (e.g., "youtube", "vimeo")
    """

    KIND: ClassVar[str] = "video"

    def __init__(
        self, 
        *,
        url: str,
        title: str,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        duration: Optional[int] = None,
        provider: Optional[Union[VideoProvider, str]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a video block.

        Args:
            url: The URL of the video
            title: The title of the video
            description: Optional description of the video
            thumbnail_url: Optional URL of a thumbnail image
            duration: Optional duration of the video in seconds
            provider: Optional provider of the video (e.g., VideoProvider.YOUTUBE, VideoProvider.VIMEO)
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "url": url,
            "title": title,
        }

        if description is not None:
            payload["description"] = description

        if thumbnail_url is not None:
            payload["thumbnail_url"] = thumbnail_url

        if duration is not None:
            payload["duration"] = duration

        if provider is not None:
            # Convert provider to string if it's an enum
            provider_value = provider.value if isinstance(provider, VideoProvider) else provider
            payload["provider"] = provider_value

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def url(self) -> str:
        """Get the video URL.

        Returns:
            The video URL
        """
        return self.payload.get("url", "")

    @property
    def title(self) -> str:
        """Get the video title.

        Returns:
            The video title
        """
        return self.payload.get("title", "")

    @property
    def description(self) -> Optional[str]:
        """Get the video description.

        Returns:
            The video description, or None if not set
        """
        return self.payload.get("description")

    @property
    def thumbnail_url(self) -> Optional[str]:
        """Get the thumbnail URL.

        Returns:
            The thumbnail URL, or None if not set
        """
        return self.payload.get("thumbnail_url")

    @property
    def duration(self) -> Optional[int]:
        """Get the video duration.

        Returns:
            The video duration in seconds, or None if not set
        """
        return self.payload.get("duration")

    @property
    def provider(self) -> Optional[VideoProvider]:
        """Get the video provider.

        Returns:
            The video provider as a VideoProvider enum, or None if not set
        """
        provider_str = self.payload.get("provider")
        if provider_str is None:
            return None

        try:
            return VideoProvider(provider_str)
        except ValueError:
            # If the provider string doesn't match any enum value, return None
            return None
