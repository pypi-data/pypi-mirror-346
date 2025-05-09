"""Supplement block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, List, Optional

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock


class SupplementBlock(BaseBlock):
    """A block containing supplementary information or resources.

    Attributes:
        title: The title of the supplement
        content: The main content of the supplement
        links: Optional list of related links
        tags: Optional list of tags for categorization
    """

    KIND: ClassVar[str] = "supplement"

    def __init__(
        self,
        *,
        title: str,
        content: str,
        links: Optional[List[Dict[str, str]]] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a supplement block.

        Args:
            title: The title of the supplement
            content: The main content of the supplement
            links: Optional list of related links, each as a dict with 'url' and 'title' keys
            tags: Optional list of tags for categorization
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "title": title,
            "content": content,
        }

        if links is not None:
            # Validate that each link has the required keys
            for i, link in enumerate(links):
                if "url" not in link:
                    raise ValueError(f"Link at index {i} is missing the 'url' key")
                if "title" not in link:
                    raise ValueError(f"Link at index {i} is missing the 'title' key")
            payload["links"] = links

        if tags is not None:
            payload["tags"] = tags

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def title(self) -> str:
        """Get the supplement title.

        Returns:
            The supplement title
        """
        return self.payload.get("title", "")

    @property
    def content(self) -> str:
        """Get the supplement content.

        Returns:
            The supplement content
        """
        return self.payload.get("content", "")

    @property
    def links(self) -> List[Dict[str, str]]:
        """Get the list of related links.

        Returns:
            The list of related links, or an empty list if not set
        """
        return self.payload.get("links", [])

    @property
    def tags(self) -> List[str]:
        """Get the list of tags.

        Returns:
            The list of tags, or an empty list if not set
        """
        return self.payload.get("tags", [])
