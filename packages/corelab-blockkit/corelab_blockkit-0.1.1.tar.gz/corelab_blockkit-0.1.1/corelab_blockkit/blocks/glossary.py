"""Glossary block implementation for the blockkit package."""

from typing import Any, ClassVar, Dict, List, Optional

from pydantic import Field

from corelab_blockkit.blocks.base import BaseBlock


class GlossaryBlock(BaseBlock):
    """A block containing a glossary of terms and definitions.

    Attributes:
        terms: A list of term-definition pairs
        title: Optional title for the glossary
    """

    KIND: ClassVar[str] = "glossary"

    def __init__(
        self,
        *,
        terms: List[Dict[str, str]],
        title: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a glossary block.

        Args:
            terms: A list of term-definition pairs, each as a dict with 'term' and 'definition' keys
            title: Optional title for the glossary
            **kwargs: Additional arguments to pass to BaseBlock
        """
        # Validate that each term has the required keys
        for i, term_dict in enumerate(terms):
            if "term" not in term_dict:
                raise ValueError(f"Term at index {i} is missing the 'term' key")
            if "definition" not in term_dict:
                raise ValueError(f"Term at index {i} is missing the 'definition' key")

        payload = {
            "terms": terms,
        }

        if title is not None:
            payload["title"] = title

        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def terms(self) -> List[Dict[str, str]]:
        """Get the list of terms.

        Returns:
            The list of term-definition pairs
        """
        return self.payload.get("terms", [])

    @property
    def title(self) -> Optional[str]:
        """Get the glossary title.

        Returns:
            The glossary title, or None if not set
        """
        return self.payload.get("title")

    def get_term(self, term: str) -> Optional[str]:
        """Get the definition for a specific term.

        Args:
            term: The term to look up

        Returns:
            The definition, or None if the term is not found
        """
        for term_dict in self.terms:
            if term_dict.get("term") == term:
                return term_dict.get("definition")
        return None

    def get_terms(self) -> List[str]:
        """Get a list of all terms.

        Returns:
            A list of all terms in the glossary
        """
        return [term_dict.get("term", "") for term_dict in self.terms]
