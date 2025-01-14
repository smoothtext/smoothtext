#  SmoothText - https://smoothtext.tugrulgungor.me/
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from __future__ import annotations
from enum import Enum

_Constants: dict[any, tuple[str, str, str]] = {}


class Language(Enum):
    """
    Languages supported by SmoothText.

    Attributes:
        English: English language.
        Turkish: Turkish language.
    """

    English = 'English'
    Turkish = 'Turkish'

    def __str__(self) -> str:
        return self.value

    def alpha2(self) -> str:
        """
        Returns string representation of language.
        :return: String representation of language.
        """

        return _Constants[self][1]

    def alpha3(self) -> str:
        """
        Returns string representation of language.
        :return: String representation of language.
        """

        return _Constants[self][2]

    @staticmethod
    def values() -> list[Language]:
        """
        Returns list of supported languages.
        :return: List of supported languages.
        """

        return [Language.English, Language.Turkish]

    @staticmethod
    def parse(language: Language | str) -> Language:
        """
        Parses language string into supported languages.
        :param language: Language string to parse.
        :return: Language parsed into supported languages.
        :exception ValueError: If language is not supported.
        """

        if isinstance(language, Language):
            return language

        language = language.lower()

        for k, v in _Constants.items():
            for e in v:
                if e == language:
                    return k

        raise ValueError('Unknown language.')


_Constants[Language.English] = (Language.English.value.lower(), 'en', 'eng')
_Constants[Language.Turkish] = (Language.Turkish.value.lower(), 'tr', 'tur')
