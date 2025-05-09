"""JSON serialization and deserialization for blockkit."""

import json
from datetime import datetime
from typing import Any, Dict, List, Type, Union
from uuid import UUID

from pydantic import BaseModel

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import SerializationError
from corelab_blockkit.list import BlockList
from corelab_blockkit.registry import registry


class BlockJSONEncoder(json.JSONEncoder):
    """JSON encoder for blocks and related objects."""

    def default(self, obj: Any) -> Any:
        """Convert objects to JSON-serializable types.

        Args:
            obj: The object to convert

        Returns:
            A JSON-serializable representation of the object
        """
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)


def serialize_to_json(
    obj: Union[BaseBlock, BlockList, List[BaseBlock]], 
    **kwargs: Any
) -> str:
    """Serialize a block, block list, or list of blocks to JSON.

    Args:
        obj: The object to serialize
        **kwargs: Additional arguments to pass to json.dumps

    Returns:
        The JSON string

    Raises:
        SerializationError: If serialization fails
    """
    try:
        return json.dumps(obj, cls=BlockJSONEncoder, **kwargs)
    except Exception as e:
        raise SerializationError(f"Failed to serialize to JSON: {e}") from e


def deserialize_from_json(
    json_str: str, 
    target_type: Type[Union[BaseBlock, BlockList]] = BlockList
) -> Union[BaseBlock, BlockList]:
    """Deserialize a JSON string to a block or block list.

    Args:
        json_str: The JSON string to deserialize
        target_type: The type to deserialize to (BaseBlock or BlockList)

    Returns:
        The deserialized object

    Raises:
        SerializationError: If deserialization fails
    """
    try:
        data = json.loads(json_str)

        if target_type == BlockList:
            # Deserialize a block list
            if not isinstance(data, dict) or "blocks" not in data:
                raise SerializationError("Invalid JSON format for BlockList")

            blocks = []
            for block_data in data["blocks"]:
                if not isinstance(block_data, dict) or "kind" not in block_data:
                    raise SerializationError("Invalid block data: missing 'kind' field")

                kind = block_data["kind"]
                try:
                    block_class = registry.get(kind)
                    blocks.append(block_class.model_validate(block_data))
                except Exception as e:
                    raise SerializationError(f"Failed to deserialize block of kind '{kind}': {e}") from e

            return BlockList(blocks=blocks)

        elif issubclass(target_type, BaseBlock):
            # Deserialize a single block
            if not isinstance(data, dict) or "kind" not in data:
                raise SerializationError("Invalid JSON format for BaseBlock")

            kind = data["kind"]
            try:
                block_class = registry.get(kind)
                return block_class.model_validate(data)
            except Exception as e:
                raise SerializationError(f"Failed to deserialize block of kind '{kind}': {e}") from e

        else:
            raise SerializationError(f"Unsupported target type: {target_type}")

    except SerializationError:
        raise
    except Exception as e:
        raise SerializationError(f"Failed to deserialize from JSON: {e}") from e
