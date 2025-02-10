#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

"""
Language support module for SmoothText.

This module provides language identification and parsing capabilities through the Language enum.
It supports ISO 639-1 (two-letter) and ISO 639-2 (three-letter) language codes, with optional
country variants using either hyphen or underscore separators (e.g., 'en-US' or 'en_US').

Examples:
    >>> lang = Language.parse("en-US")
    >>> print(lang)
    English (United States)
    >>> print(lang.family())
    English
"""

from __future__ import annotations
from enum import Enum

_Constants: dict[any, tuple[str, str, str]] = {}


class Language(Enum):
    """
    Enum representing languages supported by SmoothText.

    This enum provides language identification capabilities with support for both
    ISO 639-1 (two-letter) and ISO 639-2 (three-letter) language codes, with
    optional country variants. Languages are organized in families, where regional
    variants (e.g., English_US) belong to a parent language (e.g., English).

    Attributes:
        # Base Languages
        English: Generic English language support
        German: Generic German language support
        Turkish: Generic Turkish language support

        # English Variants
        English_GB: British English variant
        English_US: American English variant (default for 'en')

        # German Variants
        German_DE: German (Germany) variant (default for 'de')

        # Turkish Variants
        Turkish_TR: Turkish (Türkiye) variant (default for 'tr')

    Examples:
        >>> lang = Language.English_US
        >>> print(lang.alpha2())  # Returns 'en'
        >>> print(lang.family())  # Returns Language.English
    """

    # # # # # # # #
    # Attributes  #
    # # # # # # # #
    # Base Languages
    English = "English"
    German = "German"
    Turkish = "Turkish"

    # English Variants
    English_GB = "English (Great Britain)"
    English_US = "English (United States)"

    # German Variants
    German_DE = "German (Germany)"

    # Turkish Variants
    Turkish_TR = "Turkish (Türkiye)"

    def family(self) -> Language:
        """
        Get the family (base) language of the current language variant.

        The family language represents the base language without region/country specifics.
        Regional variants return their base language, while base languages return themselves.

        Returns:
            Language: Base language enum value

        Examples:
            >>> Language.English_US.family()  # Returns Language.English
            >>> Language.English.family()     # Returns Language.English
        """
        if self in [Language.English_GB, Language.English_US]:
            return Language.English

        if self in [Language.German_DE]:
            return Language.German

        if self in [Language.Turkish_TR]:
            return Language.Turkish

        return self

    def variants(self) -> list[Language]:
        """
        Get a list of all language variants for the current language.

        Returns:
            list[Language]: List of all language variants, including the current language

        Examples:
            >>> Language.English_GB.variants()
            [Language.English_GB, Language.English_US]
            >>> Language.English.variants()
            [Language.English_GB, Language.English_US]
        """
        if self.family() == Language.English:
            return [Language.English_GB, Language.English_US]

        if self.family() == Language.German:
            return [Language.German_DE]

        if self.family() == Language.Turkish:
            return [Language.Turkish_TR]

        return [self]

    # # # # # # # # # #
    # Stringification #
    # # # # # # # # # #
    def alpha2(self) -> str:
        """
        Get the ISO 639-1 two-letter code of the language.

        Returns:
            str: Two-letter language code (e.g., 'en' for English, 'tr' for Turkish)
        """
        return _Constants[self][1][:2]

    def alpha3(self) -> str:
        """
        Get the ISO 639-2 three-letter code of the language.

        Returns:
            str: Three-letter language code (e.g., 'eng' for English, 'tur' for Turkish)
        """
        return _Constants[self][2][:3]

    # # # # # # # # # # # # #
    # Readability Formulas  #
    # # # # # # # # # # # # #
    def readability_formulas(self) -> list["ReadabilityFormula"]:
        """
        Get a list of supported readability formulas for the current language.

        Different languages have different readability formulas that are specifically
        designed and validated for their linguistic characteristics.

        Returns:
            list[ReadabilityFormula]: List of readability formulas supported for this language

        Examples:
            >>> Language.English.readability_formulas()
            [ReadabilityFormula.Flesch_Reading_Ease,
             ReadabilityFormula.Flesch_Kincaid_Grade,
             ReadabilityFormula.Flesch_Kincaid_Grade_Simplified]
            >>> Language.Turkish.readability_formulas()
            [ReadabilityFormula.Atesman, ReadabilityFormula.Bezirci_Yilmaz]
        """
        from . import ReadabilityFormula

        if Language.English == self.family():
            return [
                ReadabilityFormula.Flesch_Reading_Ease,
                ReadabilityFormula.Flesch_Kincaid_Grade,
                ReadabilityFormula.Flesch_Kincaid_Grade_Simplified,
            ]

        if Language.German == self.family():
            return [
                ReadabilityFormula.Flesch_Reading_Ease,
                ReadabilityFormula.Wiener_Sachtextformel,
                ReadabilityFormula.Wiener_Sachtextformel_1,
                ReadabilityFormula.Wiener_Sachtextformel_2,
                ReadabilityFormula.Wiener_Sachtextformel_3,
                ReadabilityFormula.Wiener_Sachtextformel_4,
            ]

        if Language.Turkish == self.family():
            return [
                ReadabilityFormula.Atesman,
                ReadabilityFormula.Bezirci_Yilmaz,
            ]

    # # # # # # #
    # Operators #
    # # # # # # #
    def __hash__(self) -> int:
        """
        Get hash of the language enum value.
        Maintains hashability when used with custom __eq__.

        Returns:
            int: Hash value of the enum member
        """
        return hash(self.value)

    def __str__(self) -> str:
        """
        Get the full name of the language.

        Returns:
            str: Full name of the language (e.g., 'English', 'Turkish')
        """
        return self.value

    def __eq__(self, value: Language | str) -> bool:
        """
        Compare the current language with another language or string.

        Args:
            value: Language enum value or string to compare with

        Returns:
            bool: True if the languages are equal, False otherwise

        Examples:
            >>> Language.English == "en"
            True
            >>> Language.English == Language.Turkish
            False
        """
        if isinstance(value, Language):
            return self is value

        if isinstance(value, str):
            return self == Language.parse(value)

        return False

    # # # # # # # # # #
    # Static Methods  #
    # # # # # # # # # #
    @staticmethod
    def values() -> list[Language]:
        """
        Get a list of all supported languages.

        Returns:
            list[Language]: List containing all supported Language enum values
        """
        return [
            Language.English,
            Language.English_GB,
            Language.English_US,
            Language.German,
            Language.German_DE,
            Language.Turkish,
            Language.Turkish_TR,
        ]

    @staticmethod
    def parse(language: Language | str) -> Language | None:
        """
        Parse a language identifier into a Language enum value.

        Args:
            language: Language identifier to parse. Can be:
                     - Language enum value
                     - Full name (e.g., 'English')
                     - ISO 639-1 code (e.g., 'en')
                     - ISO 639-2 code (e.g., 'eng')

        Returns:
            Language: Corresponding Language enum value if valid
            None: If the input cannot be parsed into a supported language

        Examples:
            >>> Language.parse('en')
            Language.English
            >>> Language.parse('invalid')
            None
        """
        if isinstance(language, Language):
            return language

        if not isinstance(language, str):
            return None

        language = language.lower()

        if "_" in language:
            language = language.replace("_", "-")

        for k, v in _Constants.items():
            for e in v:
                if e == language:
                    if k == k.family():
                        return k.variants()[-1]

                    return k

        return None

    @staticmethod
    def parse_multiple(
        languages: Language | str | list[Language | str],
    ) -> list[Language]:
        """
        Parse multiple language identifiers into a list of Language enum values.
        Note: The order of returned languages is not guaranteed.

        Args:
            languages: One or more language identifiers. Can be:
                      - Single Language enum value
                      - Single language string
                      - List of Language enum values and/or strings
                      - Comma-separated string of language identifiers

        Returns:
            list[Language]: List of unique, valid Language enum values.
                           The order of languages in the list is not guaranteed.

        Examples:
            >>> # Order may vary in the results
            >>> Language.parse_multiple('en,tr')
            [Language.English_GB, Language.Turkish_TR]  # or [Language.Turkish_TR, Language.English_GB]
            >>> set(Language.parse_multiple(['en', 'invalid', 'tr']))  # Use set for order-independent comparison
            {Language.English_GB, Language.Turkish_TR}
        """
        if isinstance(languages, Language):
            return [languages]

        if isinstance(languages, str):
            languages = [s.strip() for s in languages.split(",")]

        return list({pl for l in languages if (pl := Language.parse(l)) is not None})


_Constants[Language.English] = (Language.English.value.lower(), "en", "eng")
_Constants[Language.English_GB] = (Language.English_GB.value.lower(), "en-gb", "eng-gb")
_Constants[Language.English_US] = (Language.English_US.value.lower(), "en-us", "eng-us")

_Constants[Language.German] = (Language.German.value.lower(), "de", "deu")
_Constants[Language.German_DE] = (Language.German_DE.value.lower(), "de-de", "deu-de")

_Constants[Language.Turkish] = (Language.Turkish.value.lower(), "tr", "tur")
_Constants[Language.Turkish_TR] = (Language.Turkish_TR.value.lower(), "tr-tr", "tur-tr")
