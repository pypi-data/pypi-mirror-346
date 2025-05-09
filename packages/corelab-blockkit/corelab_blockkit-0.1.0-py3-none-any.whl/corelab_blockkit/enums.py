"""Enums for the blockkit package."""

from enum import Enum, auto


class TextFormat(str, Enum):
    """Format of text content."""
    
    MARKDOWN = "markdown"
    PLAIN = "plain"
    HTML = "html"
    RST = "rst"  # reStructuredText


class AudioFormat(str, Enum):
    """Format of audio files."""
    
    MP3 = "mp3"
    OGG = "ogg"
    WAV = "wav"
    AAC = "aac"
    FLAC = "flac"


class VideoProvider(str, Enum):
    """Provider of video content."""
    
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    TWITCH = "twitch"
    DAILYMOTION = "dailymotion"
    CUSTOM = "custom"


class MimeType(str, Enum):
    """Common MIME types for files."""
    
    # Text
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"
    TEXT_CSS = "text/css"
    TEXT_JAVASCRIPT = "text/javascript"
    
    # Application
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_ZIP = "application/zip"
    APPLICATION_MSWORD = "application/msword"
    APPLICATION_EXCEL = "application/vnd.ms-excel"
    APPLICATION_POWERPOINT = "application/vnd.ms-powerpoint"
    
    # Image
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    IMAGE_SVG = "image/svg+xml"
    IMAGE_WEBP = "image/webp"
    
    # Audio
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    AUDIO_WAV = "audio/wav"
    AUDIO_WEBM = "audio/webm"
    
    # Video
    VIDEO_MP4 = "video/mp4"
    VIDEO_OGG = "video/ogg"
    VIDEO_WEBM = "video/webm"
    
    # Other
    BINARY = "application/octet-stream"