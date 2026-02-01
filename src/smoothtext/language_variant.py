#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .language import Language


class LanguageVariant(Enum):
    """
    An enumeration of supported language variants (dialects) in SmoothText.

    Attributes:
        English_GB (LanguageVariant): English as used in the United Kingdom.
        English_US (LanguageVariant): English as used in the United States.
        German_DE (LanguageVariant): German as used in Germany.
        Turkish_TR (LanguageVariant): Turkish as used in Turkey.

    Example:
        ```python
        from smoothtext import LanguageVariant

        # Accessing the BCP 47 tag
        print(LanguageVariant.English_US.tag)  # 'en-us'

        # Getting the parent language
        print(LanguageVariant.English_US.language)  # Language.English
        ```
    """

    English_GB = "English (United Kingdom)"
    """British English."""

    English_US = "English (United States)"
    """American English."""

    German_DE = "German (Germany)"
    """German (Germany)."""

    Russian_RU = "Russian (Russia)"
    """Russian (Russia)."""

    Turkish_TR = "Turkish (Turkey)"
    """Turkish (Turkey)."""

    @property
    def _constants(self) -> tuple[str, str]:
        from .internal.constants.language_variant import LanguageVariantConstants

        return LanguageVariantConstants[self]

    @property
    def language(self) -> Language:
        """
        The parent Language for this variant.

        Returns:
            Language: The language this variant belongs to.

        Raises:
            RuntimeError: If the variant is not associated with any language.

        Example:
            ```python
            >>> LanguageVariant.German_DE.language
            <Language.German: 'German'>
            ```
        """
        from .language import Language

        for lang in Language:
            if self in lang.variants:
                return lang

        # This should never happen, but just in case.
        raise RuntimeError(
            f"[SmoothText.LanguageVariant] {self} does not have a parent language."
        )

    @property
    def tag(self) -> str:
        """
        The BCP 47 language tag for this variant.

        Returns:
            str: The language tag (e.g., 'en-gb').

        Example:
            ```python
            >>> LanguageVariant.Turkish_TR.tag
            'tr-tr'
            ```
        """
        return f"{self.language.alpha2}-{self._constants[0]}"

    def __eq__(self, other: Language | LanguageVariant | str) -> bool:
        from .language import Language

        if isinstance(other, Language):
            return self.language == other

        if isinstance(other, LanguageVariant):
            return self.value == other.value

        if isinstance(other, str):
            other = other.lower()
            return self.value.lower() == other or self.tag.lower() == other

        return False

    def __hash__(self) -> int:
        return hash(self.value)
