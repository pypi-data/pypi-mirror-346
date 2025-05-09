"""Block types for the blockkit package."""

# Import the base block
from corelab_blockkit.blocks.base import BaseBlock

# Import all block types
from corelab_blockkit.blocks.text import TextBlock
from corelab_blockkit.blocks.image import ImageBlock
from corelab_blockkit.blocks.video import VideoBlock
from corelab_blockkit.blocks.audio import AudioBlock
from corelab_blockkit.blocks.download import DownloadBlock
from corelab_blockkit.blocks.glossary import GlossaryBlock
from corelab_blockkit.blocks.quote import QuoteBlock
from corelab_blockkit.blocks.supplement import SupplementBlock

# Register all block types
from corelab_blockkit.registry import registry

# Clear the registry first to avoid duplicate registrations
registry._types = {}

registry.register(TextBlock)
registry.register(ImageBlock)
registry.register(VideoBlock)
registry.register(AudioBlock)
registry.register(DownloadBlock)
registry.register(GlossaryBlock)
registry.register(QuoteBlock)
registry.register(SupplementBlock)

__all__ = [
    "BaseBlock",
    "TextBlock",
    "ImageBlock",
    "VideoBlock",
    "AudioBlock",
    "DownloadBlock",
    "GlossaryBlock",
    "QuoteBlock",
    "SupplementBlock",
]
