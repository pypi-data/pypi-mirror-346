"""Registry for block types in the blockkit package."""

import importlib.metadata
import logging
from typing import Dict, List, Type

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import RegistryError

logger = logging.getLogger(__name__)


class BlockTypeRegistry:
    """Registry for block types.

    This registry allows for registering block types and discovering them
    through entry points.
    """

    def __init__(self) -> None:
        """Initialize the registry."""
        self._types: Dict[str, Type[BaseBlock]] = {}

    def register(self, block_class: Type[BaseBlock]) -> None:
        """Register a block type.

        Args:
            block_class: The block class to register

        Raises:
            RegistryError: If the block type is already registered
        """
        kind = block_class.KIND
        if not kind:
            raise RegistryError(
                f"Block class {block_class.__name__} has no KIND defined"
            )

        if kind in self._types:
            raise RegistryError(f"Block type '{kind}' is already registered")

        self._types[kind] = block_class
        logger.debug(f"Registered block type: {kind}")

    def get(self, kind: str) -> Type[BaseBlock]:
        """Get a block type by kind.

        Args:
            kind: The kind of block to get

        Returns:
            The block class

        Raises:
            RegistryError: If the block type is not registered
        """
        if kind not in self._types:
            raise RegistryError(f"Block type '{kind}' is not registered")

        return self._types[kind]

    def list_types(self) -> List[str]:
        """List all registered block types.

        Returns:
            A list of block type kinds
        """
        return list(self._types.keys())

    def load_entry_points(self) -> None:
        """Load block types from entry points.

        This method discovers and loads block types from the 'blockkit.blocks'
        entry point group.
        """
        try:
            for entry_point in importlib.metadata.entry_points(group="blockkit.blocks"):
                try:
                    block_class = entry_point.load()
                    self.register(block_class)
                    logger.info(
                        f"Loaded block type from entry point: {entry_point.name}"
                    )
                except Exception as e:
                    logger.error(f"Failed to load entry point {entry_point.name}: {e}")
        except Exception as e:
            logger.error(f"Failed to load entry points: {e}")


# Singleton instance of the registry
registry = BlockTypeRegistry()
