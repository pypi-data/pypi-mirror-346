"""Block list implementation for the blockkit package."""

from typing import Any, Dict, Iterator, List, Optional, TypeVar, cast
from uuid import UUID

from pydantic import BaseModel

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import BlockDuplicateError, BlockNotFoundError

T = TypeVar("T", bound=BaseBlock)


class BlockList(BaseModel):
    """A list of blocks with operations for manipulation.

    This class provides methods for adding, removing, moving, and finding blocks.
    It also provides methods for serialization and deserialization.
    """

    blocks: List[BaseBlock] = []

    model_config = {
        "frozen": True,  # Make the model immutable (PEP 681)
    }

    def __init__(self, blocks: Optional[List[BaseBlock]] = None) -> None:
        """Initialize a block list.

        Args:
            blocks: Optional list of blocks to initialize with
        """
        super().__init__(blocks=blocks or [])

        # Verify that all block IDs are unique
        id_set: Dict[UUID, bool] = {}
        for block in self.blocks:
            if block.id in id_set:
                raise BlockDuplicateError(f"Duplicate block ID: {block.id}")
            id_set[block.id] = True

    def add(self, block: BaseBlock, index: Optional[int] = None) -> "BlockList":
        """Add a block to the list.

        Args:
            block: The block to add
            index: Optional index to insert at (appends if None)

        Returns:
            A new BlockList with the block added

        Raises:
            BlockDuplicateError: If a block with the same ID already exists
            ValueError: If the index is out of range
        """
        # Check for duplicate ID
        if any(b.id == block.id for b in self.blocks):
            raise BlockDuplicateError(f"Block with ID {block.id} already exists")

        # Create a new list of blocks
        new_blocks = list(self.blocks)

        # Insert or append the block
        if index is not None:
            if index < 0 or index > len(new_blocks):
                raise ValueError(f"Index {index} out of range (0-{len(new_blocks)})")
            new_blocks.insert(index, block)
        else:
            new_blocks.append(block)

        return BlockList(blocks=new_blocks)

    def remove(self, block_id: UUID) -> "BlockList":
        """Remove a block from the list.

        Args:
            block_id: The ID of the block to remove

        Returns:
            A new BlockList with the block removed

        Raises:
            BlockNotFoundError: If the block is not found
        """
        for i, block in enumerate(self.blocks):
            if block.id == block_id:
                new_blocks = list(self.blocks)
                new_blocks.pop(i)
                return BlockList(blocks=new_blocks)

        raise BlockNotFoundError(f"Block with ID {block_id} not found")

    def move(self, block_id: UUID, new_index: int) -> "BlockList":
        """Move a block to a new position in the list.

        Args:
            block_id: The ID of the block to move
            new_index: The new index for the block

        Returns:
            A new BlockList with the block moved

        Raises:
            BlockNotFoundError: If the block is not found
            ValueError: If the new index is out of range
        """
        # Find the block
        block_index = None
        for i, block in enumerate(self.blocks):
            if block.id == block_id:
                block_index = i
                break

        if block_index is None:
            raise BlockNotFoundError(f"Block with ID {block_id} not found")

        # Check if the new index is valid
        if new_index < 0 or new_index >= len(self.blocks):
            raise ValueError(f"Index {new_index} out of range (0-{len(self.blocks) - 1})")

        # If the block is already at the desired index, return the same list
        if block_index == new_index:
            return self

        # Create a new list of blocks
        new_blocks = list(self.blocks)

        # Remove the block from its current position
        block = new_blocks.pop(block_index)

        # Insert the block at the new position
        new_blocks.insert(new_index, block)

        return BlockList(blocks=new_blocks)

    def find_by_id(self, block_id: UUID) -> BaseBlock:
        """Find a block by its ID.

        Args:
            block_id: The ID of the block to find

        Returns:
            The block with the specified ID

        Raises:
            BlockNotFoundError: If the block is not found
        """
        for block in self.blocks:
            if block.id == block_id:
                return block

        raise BlockNotFoundError(f"Block with ID {block_id} not found")

    def __iter__(self) -> Iterator[BaseBlock]:
        """Iterate over the blocks in the list.

        Returns:
            An iterator over the blocks
        """
        return iter(self.blocks)

    def __len__(self) -> int:
        """Get the number of blocks in the list.

        Returns:
            The number of blocks
        """
        return len(self.blocks)

    def __getitem__(self, index: int) -> BaseBlock:
        """Get a block by index.

        Args:
            index: The index of the block to get

        Returns:
            The block at the specified index
        """
        return self.blocks[index]

    def to_json(self, **kwargs: Any) -> str:
        """Serialize the block list to JSON.

        Args:
            **kwargs: Additional arguments to pass to json.dumps

        Returns:
            The JSON string
        """
        from corelab_blockkit.ser.json_codec import serialize_to_json
        return serialize_to_json(self, **kwargs)

    @classmethod
    def from_json(cls, json_str: str) -> "BlockList":
        """Deserialize a JSON string to a block list.

        Args:
            json_str: The JSON string to deserialize

        Returns:
            The deserialized block list
        """
        from corelab_blockkit.ser.json_codec import deserialize_from_json
        return deserialize_from_json(json_str, target_type=cls)

    def to_yaml(self, **kwargs: Any) -> str:
        """Serialize the block list to YAML.

        Args:
            **kwargs: Additional arguments to pass to YAML.dump

        Returns:
            The YAML string
        """
        from corelab_blockkit.ser.yaml_codec import serialize_to_yaml
        return serialize_to_yaml(self, **kwargs)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "BlockList":
        """Deserialize a YAML string to a block list.

        Args:
            yaml_str: The YAML string to deserialize

        Returns:
            The deserialized block list
        """
        from corelab_blockkit.ser.yaml_codec import deserialize_from_yaml
        return deserialize_from_yaml(yaml_str, target_type=cls)
