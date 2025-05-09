"""Exceptions for the blockkit package."""

from typing import Any


class BlockkitError(Exception):
    """Base exception for all blockkit errors."""


class BlockTypeError(BlockkitError):
    """Raised when an invalid block type is used."""


class BlockValidationError(BlockkitError):
    """Raised when block validation fails."""


class BlockNotFoundError(BlockkitError):
    """Raised when a block is not found."""


class BlockDuplicateError(BlockkitError):
    """Raised when a block with the same ID already exists."""


class SerializationError(BlockkitError):
    """Raised when serialization or deserialization fails."""


class RegistryError(BlockkitError):
    """Raised when there's an error with the block type registry."""