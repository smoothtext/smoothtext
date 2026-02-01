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
    from .language_variant import LanguageVariant


class Language(Enum):
    """
    An enumeration of supported languages in SmoothText.

    Attributes:
        English (Language): The English language.
        German (Language): The German language.
        Turkish (Language): The Turkish language.

    Example:
        ```python
        from smoothtext import Language, LanguageVariant

        # Accessing metadata
        print(Language.English.alpha2)  # 'en'

        # Comparison with strings
        print(Language.Turkish == "tr")  # True

        # Comparison with variants
        print(Language.English == LanguageVariant.English_US)  # True
        ```
    """

    English = "English"
    """The English language."""

    German = "German"
    """The German language."""

    Russian = "Russian"
    """The Russian language."""

    Turkish = "Turkish"
    """The Turkish language."""

    @property
    def _constants(self) -> tuple[str, str, str]:
        from .internal.constants.language import LanguageConstants

        return LanguageConstants[self]

    @property
    def alpha2(self) -> str:
        """
        The ISO 639-1 (alpha-2) code of the language.

        Returns:
            str: The two-letter language code.

        Example:
            ```python
            >>> Language.German.alpha2
            'de'
            ```
        """
        return self._constants[0]

    @property
    def alpha3(self) -> str:
        """
        The ISO 639-3 (alpha-3) code of the language.

        Returns:
            str: The three-letter language code.

        Example:
            ```python
            >>> Language.Turkish.alpha3
            'tur'
            ```
        """
        return self._constants[1]

    @property
    def default_variant(self) -> LanguageVariant:
        """
        The default LanguageVariant for this language.

        Returns:
            LanguageVariant: The primary variant associated with the language.

        Raises:
            RuntimeError: If the language does not have a default variant configured.

        Example:
            ```python
            >>> Language.English.default_variant
            <LanguageVariant.English_US: 'English (United States)'>
            ```
        """
        from .language_variant import LanguageVariant

        if self == Language.English:
            return LanguageVariant.English_US

        if self == Language.German:
            return LanguageVariant.German_DE

        if self == Language.Russian:
            return LanguageVariant.Russian_RU

        if self == Language.Turkish:
            return LanguageVariant.Turkish_TR

        # This should never happen, but just in case.
        raise RuntimeError(
            f"[SmoothText.Language] {self} does not have a default variant."
        )

    @property
    def variants(self) -> list[LanguageVariant]:
        """
        A list of all supported LanguageVariants for this language.

        Returns:
            list[LanguageVariant]: All variants associated with the language.

        Raises:
            RuntimeError: If the language does not have any variants configured.

        Example:
            ```python
            >>> Language.English.variants
            [<LanguageVariant.English_GB: ...>, <LanguageVariant.English_US: ...>]
            ```
        """
        from .language_variant import LanguageVariant

        if self == Language.English:
            return [LanguageVariant.English_GB, LanguageVariant.English_US]

        if self == Language.German:
            return [LanguageVariant.German_DE]

        if self == Language.Russian:
            return [LanguageVariant.Russian_RU]

        if self == Language.Turkish:
            return [LanguageVariant.Turkish_TR]

        # This should never happen, but just in case.
        raise RuntimeError(f"[SmoothText.Language] {self} does not have any variants.")

    def __eq__(self, other: Language | LanguageVariant | str) -> bool:
        if isinstance(other, Language):
            return self.value == other.value

        if isinstance(other, LanguageVariant):
            return self in other.variants

        if isinstance(other, str):
            other = other.lower()
            return self.value.lower() == other or self.alpha2.lower() == other

        return False

    def __hash__(self) -> int:
        return hash(self.value)
