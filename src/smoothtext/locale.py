#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from __future__ import annotations
import re

from .language import Language
from .language_variant import LanguageVariant
from .internal.constants.language import LanguageConstants
from .internal.constants.language_variant import LanguageVariantConstants


class Locale:
    """
    A class representing a specific language and region combination.

    Attributes:
        language (Language): The parent language of the current locale.
        language_variant (LanguageVariant): The specific language variant of the current locale.

    Example:
        ```python
        from smoothtext import Locale, Language, LanguageVariant

        # Initialization
        loc1 = Locale("en-US")

        # Accessing properties
        print(loc1.language)         # Language.English
        print(loc1.language_variant) # LanguageVariant.English_US
        ```
    """

    def _assign(self, locale: LocaleLike) -> None:
        if isinstance(locale, Locale):
            self._language_variant = locale.language_variant
            return

        if isinstance(locale, Language):
            self._language_variant = locale.default_variant
            return

        if isinstance(locale, LanguageVariant):
            self._language_variant = locale
            return

        if isinstance(locale, str):
            parsed = self._parse(locale)
            if parsed is not None:
                self._language_variant = parsed
                return

        raise ValueError(f"[SmoothText.Locale] Invalid locale string: {locale}.")

    def __init__(self, locale: LocaleLike) -> None:
        """
        Initializes a new Locale instance.

        Args:
            locale (LocaleLike): The locale identifier. Can be a string,
                a `Language` member, a `LanguageVariant` member, or another `Locale` instance.

        Raises:
            ValueError: If the provided `locale` cannot be parsed or recognized.
        """
        self._language_variant = None
        self._assign(locale)

    @property
    def language(self) -> Language:
        """
        The parent language of the current locale.

        Returns:
            Language: The language associated with this locale.

        Example:
            ```python
            >>> loc = Locale("en-US")
            >>> loc.language
            <Language.English: 'English'>
            ```
        """
        return self._language_variant.language

    @language.setter
    def language(self, value: LocaleLike) -> None:
        """
        Sets the language of the locale.

        Args:
            value (LocaleLike): The new language identifier.

        Raises:
            ValueError: If the provided value is invalid.

        Example:
            ```python
            >>> loc = Locale("en-US")
            >>> loc.language
            <Language.English: 'English'>
            >>> loc.language = "de"
            >>> loc.language
            <Language.German: 'German'>
            >>> loc.language_variant
            <LanguageVariant.German_DE: 'German (Germany)'>
            ```
        """
        self._assign(value)

    @property
    def language_variant(self) -> LanguageVariant:
        """
        The specific language variant of the current locale.

        Returns:
            LanguageVariant: The regional/dialect variant.

        Example:
            ```python
            >>> loc = Locale("en-US")
            >>> loc.language_variant
            <LanguageVariant.English_US: 'English (United States)'>
            ```
        """
        return self._language_variant

    @language_variant.setter
    def language_variant(self, value: LocaleLike) -> None:
        """
        Sets the language variant of the locale.

        Args:
            value (LocaleLike): The new language variant identifier.

        Raises:
            ValueError: If the provided value is invalid.

        Example:
            ```python
            >>> loc = Locale("en-US")
            >>> loc.language_variant
            <LanguageVariant.English_US: 'English (United States)'>
            >>> loc.language_variant = "tr-GB"
            >>> loc.language_variant
            <LanguageVariant.Turkish_TR: 'Turkish (Turkey)'>
            >>> loc.language
            <Language.Turkish: 'Turkish'>
            ```
        """
        self._assign(value)

    def to_dict(self) -> dict[str, str]:
        """
        Returns a dictionary representation of the locale.

        Returns:
            dict[str, str]: A dictionary containing the language and variant.

        Example:
            ```python
            >>> loc = Locale("en-US")
            >>> loc.to_dict()
            {'language': 'English', 'language_variant': 'English (United States)'}
            ```
        """
        return {
            "language": self.language.name,
            "language_variant": self.language_variant.name,
        }

    @staticmethod
    def _parse(locale: str) -> LanguageVariant | None:
        locale = locale.replace("_", "-").lower().strip()

        for lang, vals in LanguageConstants.items():
            for val in vals:
                if locale == val.lower():
                    return lang.default_variant

        for variant, vals in LanguageVariantConstants.items():
            for val in vals:
                if locale == val.lower() or locale == variant.tag.lower():
                    return variant

        return None

    @staticmethod
    def parse(locale: LocaleLike) -> Locale | None:
        """
        Attempts to parse a locale identifier into a Locale instance.

        Unlike the constructor, this method returns `None` instead of raising
        an exception if parsing fails.

        Args:
            locale (LocaleLike): The locale identifier to parse.

        Returns:
            Locale | None: A `Locale` instance if successful, `None` otherwise.

        Example:
            ```python
            >>> Locale.parse("en-GB")
            <Locale: English (United Kingdom)>
            >>> Locale.parse("invalid")
            None
            ```
        """
        if isinstance(locale, Locale):
            return locale

        if isinstance(locale, Language) or isinstance(locale, LanguageVariant):
            return Locale(locale)

        if isinstance(locale, str):
            try:
                return Locale(locale)
            except ValueError:
                return None

        return None

    @staticmethod
    def parse_multiple(
        locales: LocaleLike | list[LocaleLike],
        uniquify: bool = True,
        strict: bool = False,
    ) -> list[Locale]:
        """
        Parses locale identifiers from lists or a single string containing multiple identifiers separated by common delimiters (space, comma, etc.).

        Args:
            locales (LocaleLike | list[LocaleLike]): One or more locale identifiers.
            uniquify (bool): Whether to remove duplicate locales from the result.
                Defaults to True.
            strict (bool): If True, raises a ValueError if any identifier is invalid.
                If False, invalid identifiers are simply skipped. Defaults to False.

        Returns:
            list[Locale]: A list of successfully parsed `Locale` instances.

        Raises:
            ValueError: If `strict` is True and an invalid locale is encountered.

        Example:
            ```python
            >>> Locale.parse_multiple("en-US, tr; de")
            [<Locale: en-US>, <Locale: tr-TR>, <Locale: de-DE>]
            ```
        """
        if not locales or locales is None:
            return []

        if isinstance(locales, str):
            locales = [
                locale.strip().lower() for locale in re.split(r"[ ,;:]+", locales)
            ]

        if not isinstance(locales, list):
            locales = [locales]

        parsed: list[Locale] = []
        for locale in locales:
            res = Locale.parse(locale)
            if res is None:
                if strict:
                    raise ValueError(
                        f"[SmoothText.Locale] Invalid locale string: {locale}."
                    )

                continue

            if uniquify and res in parsed:
                continue

            parsed.append(res)

        return parsed

    def __eq__(self, other: LocaleLike) -> bool:
        try:
            return self.language_variant == Locale(other).language_variant
        except ValueError:
            return False

    def __hash__(self) -> int:
        return hash(self.language_variant)


LocaleLike = Language | LanguageVariant | Locale | str
"""Type alias for objects that can be converted into a `Locale`."""
