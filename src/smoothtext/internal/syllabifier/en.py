#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from typing import Literal

import pyphen

from .base import SyllabifierBase


class SyllabifierEn(SyllabifierBase):
    def __init__(self, dialect: Literal["GB", "US"]) -> None:
        self._pyphen = pyphen.Pyphen(lang=f"en_{dialect}")


class SyllabifierEnGB(SyllabifierEn):
    def __init__(self) -> None:
        super().__init__("GB")

    def syllabify(self, word: str) -> list[str]:
        if not word:
            return []

        return self._pyphen.inserted(word, " ").split(" ")

    def count(self, word: str) -> int:
        return len(self.syllabify(word))


class SyllabifierEnUS(SyllabifierEn):
    def __init__(self) -> None:
        super().__init__("US")

        try:
            import cmudict

            self._cmu = cmudict.dict()
        except ImportError:
            self._cmu = {}

    def syllabify(self, word: str) -> list[str]:
        if not word:
            return []

        return self._pyphen.inserted(word, " ").split(" ")

    def count(self, word: str) -> int:
        if not word:
            return 0

        if word.lower() in self._cmu:
            return len([p for p in self._cmu[word.lower()][0] if p[-1].isdigit()])

        return len(self.syllabify(word))
