"""Metadata for blocks in the blockkit package."""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BlockMeta(BaseModel):
    """Metadata for a block.
    
    Attributes:
        created_at: When the block was created
        updated_at: When the block was last updated
        is_favorite: Whether the block is marked as favorite
        tags: Optional tags associated with the block
        extra: Additional metadata as key-value pairs
    """
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_favorite: bool = False # todo: Убрать! Это нужно не каждому приложению!!!
    tags: list[str] = Field(default_factory=list)
    extra: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = {
        "frozen": True,  # Make the model immutable (PEP 681)
    }


def toggle_favorite(meta: BlockMeta) -> BlockMeta:
    """Toggle the is_favorite flag on a BlockMeta instance.
    
    Args:
        meta: The BlockMeta instance to modify
        
    Returns:
        A new BlockMeta instance with the is_favorite flag toggled
    """
    return BlockMeta(
        created_at=meta.created_at,
        updated_at=datetime.now(),
        is_favorite=not meta.is_favorite,
        tags=meta.tags.copy(),
        extra=meta.extra.copy(),
    )