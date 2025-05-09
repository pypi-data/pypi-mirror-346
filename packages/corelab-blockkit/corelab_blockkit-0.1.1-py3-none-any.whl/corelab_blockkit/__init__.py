"""corelab-blockkit - A library for building and managing content blocks.

corelab-blockkit is a CoreLab project that provides a standardized representation 
of course content as discrete "blocks" that can be serialized, rendered, and extended.
"""

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.enums import AudioFormat, MimeType, TextFormat, VideoProvider
from corelab_blockkit.list import BlockList
from corelab_blockkit.meta import BlockMeta, toggle_favorite
from corelab_blockkit.registry import registry

# Import all block types
from corelab_blockkit.blocks import *  # noqa

# Version information
__version__ = "0.1.1"
