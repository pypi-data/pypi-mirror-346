"""Base block definition for the blockkit package."""

import re
from typing import Any, ClassVar, Dict, Optional, Type, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from corelab_blockkit.exceptions import BlockValidationError
from corelab_blockkit.meta import BlockMeta


T = TypeVar('T', bound='BaseBlock')


class BaseBlock(BaseModel):
    """Base class for all blocks.

    Attributes:
        id: Unique identifier for the block
        kind: Type of the block (e.g., "text", "image")
        meta: Metadata for the block
        payload: Content and configuration of the block
    """

    id: UUID = Field(default_factory=uuid4)
    kind: str
    meta: BlockMeta = Field(default_factory=BlockMeta)
    payload: Dict[str, Any] = Field(default_factory=dict)

    # Class variable to store the kind value for each block type
    KIND: ClassVar[str] = ""

    model_config = {
        "frozen": True,  # Make the model immutable (PEP 681)
    }

    @classmethod
    def model_validate(cls: Type[T], obj: Any) -> T:
        """Validate and create a model instance from a dictionary.

        This method extracts fields from the payload and passes them to the constructor.

        Args:
            obj: The dictionary to validate and create a model from

        Returns:
            An instance of the model
        """
        if not isinstance(obj, dict):
            raise ValueError(f"Expected dict, got {type(obj)}")

        # Extract the standard fields
        id_value = obj.get("id")
        meta_data = obj.get("meta", {})
        payload = obj.get("payload", {})

        # Convert id to UUID if it's a string
        if isinstance(id_value, str):
            try:
                id_value = UUID(id_value)
            except ValueError:
                raise ValueError(f"Invalid UUID: {id_value}")

        # Create a BlockMeta instance if meta_data is a dict
        if isinstance(meta_data, dict):
            meta = BlockMeta.model_validate(meta_data)
        else:
            meta = meta_data

        # Create a new instance with the extracted fields
        # Pass all the standard fields (id, meta) and the payload fields
        kwargs = {}
        if id_value is not None:
            kwargs["id"] = id_value
        if meta is not None:
            kwargs["meta"] = meta

        # For BaseBlock, we need to pass the kind and payload
        # For subclasses, the kind is set in the __init__ method
        # and payload fields are passed directly
        if cls is BaseBlock:
            kind = obj.get("kind")
            if kind is not None:
                kwargs["kind"] = kind
            if payload:
                kwargs["payload"] = payload
        else:
            # For subclasses, extract fields from payload
            # and pass them directly to the constructor
            kwargs.update(payload)

        return cls(**kwargs)

    @field_validator("kind")
    @classmethod
    def validate_kind(cls, value: str) -> str:
        """Validate that the kind field matches the expected pattern.

        Args:
            value: The kind value to validate

        Returns:
            The validated kind value

        Raises:
            BlockValidationError: If the kind value is invalid
        """
        if not re.match(r"^[a-z][a-z0-9_]*$", value):
            raise BlockValidationError(
                f"Invalid kind: {value}. Must start with a lowercase letter and "
                "contain only lowercase letters, numbers, and underscores."
            )
        return value

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Set the kind field automatically for subclasses.

        This ensures that each block type has a consistent kind value.
        """
        super().__init_subclass__(**kwargs)
        if not cls.KIND:
            # Convert CamelCase to snake_case for the kind field
            kind = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
            if kind.endswith("_block"):
                kind = kind[:-6]  # Remove "_block" suffix
            cls.KIND = kind
