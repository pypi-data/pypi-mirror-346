"""YAML serialization and deserialization for blockkit."""

from datetime import datetime
from typing import Any, Dict, List, Type, Union
from uuid import UUID

import ruamel.yaml
from ruamel.yaml import YAML

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import SerializationError
from corelab_blockkit.list import BlockList
from corelab_blockkit.registry import registry

# Create a YAML instance with safe loading/dumping
yaml = YAML(typ="safe")
yaml.default_flow_style = False


def serialize_to_yaml(
    obj: Union[BaseBlock, BlockList, List[BaseBlock]], 
    **kwargs: Any
) -> str:
    """Serialize a block, block list, or list of blocks to YAML.

    Args:
        obj: The object to serialize
        **kwargs: Additional arguments to pass to YAML.dump

    Returns:
        The YAML string

    Raises:
        SerializationError: If serialization fails
    """
    try:
        # Convert to a dictionary first
        if isinstance(obj, BaseBlock):
            data = obj.model_dump()
        elif isinstance(obj, BlockList):
            data = obj.model_dump()
        elif isinstance(obj, list) and all(isinstance(item, BaseBlock) for item in obj):
            data = {"blocks": [block.model_dump() for block in obj]}
        else:
            raise SerializationError(f"Unsupported object type: {type(obj)}")

        # Convert UUIDs to strings
        _convert_uuids_to_strings(data)

        # Dump to YAML
        import io
        stream = io.StringIO()
        yaml.dump(data, stream, **kwargs)
        return stream.getvalue()

    except Exception as e:
        raise SerializationError(f"Failed to serialize to YAML: {e}") from e


def deserialize_from_yaml(
    yaml_str: str, 
    target_type: Type[Union[BaseBlock, BlockList]] = BlockList
) -> Union[BaseBlock, BlockList]:
    """Deserialize a YAML string to a block or block list.

    Args:
        yaml_str: The YAML string to deserialize
        target_type: The type to deserialize to (BaseBlock or BlockList)

    Returns:
        The deserialized object

    Raises:
        SerializationError: If deserialization fails
    """
    try:
        import io
        stream = io.StringIO(yaml_str)
        data = yaml.load(stream)

        if target_type == BlockList:
            # Deserialize a block list
            if not isinstance(data, dict) or "blocks" not in data:
                raise SerializationError("Invalid YAML format for BlockList")

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
                raise SerializationError("Invalid YAML format for BaseBlock")

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
        raise SerializationError(f"Failed to deserialize from YAML: {e}") from e


def _convert_uuids_to_strings(data: Any) -> None:
    """Recursively convert UUIDs and datetimes to strings in a data structure.

    Args:
        data: The data structure to convert
    """
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if isinstance(value, UUID):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                _convert_uuids_to_strings(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, UUID):
                data[i] = str(item)
            elif isinstance(item, datetime):
                data[i] = item.isoformat()
            elif isinstance(item, (dict, list)):
                _convert_uuids_to_strings(item)
