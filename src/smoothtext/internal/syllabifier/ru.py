#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

import pyphen

from .base import SyllabifierBase


class SyllabifierRu(SyllabifierBase):
    def __init__(self) -> None:
        self._pyphen = pyphen.Pyphen(lang="ru_RU")

    def syllabify(self, word: str) -> list[str]:
        if not word:
            return []

        return self._pyphen.inserted(word, " ").split(" ")

    def count(self, word: str) -> int:
        return len(self.syllabify(word))
