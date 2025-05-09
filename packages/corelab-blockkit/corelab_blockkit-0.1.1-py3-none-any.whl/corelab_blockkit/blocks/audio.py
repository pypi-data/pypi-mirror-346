"""Audio block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, Optional, Union

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.enums import AudioFormat


class AudioBlock(BaseBlock):
    """A block containing an audio file.

    Attributes:
        url: The URL of the audio file
        title: The title of the audio
        artist: Optional artist or creator of the audio
        duration: Optional duration of the audio in seconds
        format: Optional format of the audio file (e.g., "mp3", "ogg")
    """

    KIND: ClassVar[str] = "audio"

    def __init__(
        self,
        *,
        url: str,
        title: str,
        artist: Optional[str] = None,
        duration: Optional[int] = None,
        format: Optional[Union[AudioFormat, str]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize an audio block.

        Args:
            url: The URL of the audio file
            title: The title of the audio
            artist: Optional artist or creator of the audio
            duration: Optional duration of the audio in seconds
            format: Optional format of the audio file (e.g., AudioFormat.MP3, AudioFormat.OGG)
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "url": url,
            "title": title,
        }

        if artist is not None:
            payload["artist"] = artist

        if duration is not None:
            payload["duration"] = duration

        if format is not None:
            # Convert format to string if it's an enum
            format_value = format.value if isinstance(format, AudioFormat) else format
            payload["format"] = format_value

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def url(self) -> str:
        """Get the audio URL.

        Returns:
            The audio URL
        """
        return self.payload.get("url", "")

    @property
    def title(self) -> str:
        """Get the audio title.

        Returns:
            The audio title
        """
        return self.payload.get("title", "")

    @property
    def artist(self) -> Optional[str]:
        """Get the audio artist.

        Returns:
            The audio artist, or None if not set
        """
        return self.payload.get("artist")

    @property
    def duration(self) -> Optional[int]:
        """Get the audio duration.

        Returns:
            The audio duration in seconds, or None if not set
        """
        return self.payload.get("duration")

    @property
    def format(self) -> Optional[AudioFormat]:
        """Get the audio format.

        Returns:
            The audio format as an AudioFormat enum, or None if not set
        """
        format_str = self.payload.get("format")
        if format_str is None:
            return None

        try:
            return AudioFormat(format_str)
        except ValueError:
            # If the format string doesn't match any enum value, return None
            return None
