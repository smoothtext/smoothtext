#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

import unicodedata

from .base import SyllabifierBase


class SyllabifierTr(SyllabifierBase):
    def syllabify(self, word: str) -> list[str]:
        s: list[str] = []

        if not word:
            return s

        word_: str = self._a(word)
        if len(word_) != len(word):
            raise ValueError(f"Normalization failed for word: {word}")

        p: int = len(word_)
        i: int = p - 1
        while i >= 0:
            c = word_[i]

            if self._v(c):
                if i == 0:
                    s.append(word[0:p])
                    p = 0

                c: str = word_[i - 1]
                if self._c(c):
                    i -= 1

                s.append(word[i:p])
                p = i

            i -= 1

        if p != 0:
            s.append(word[0:p])

        s.reverse()
        return s

    def count(self, word: str) -> int:
        return len(self.syllabify(word))

    def _a(self, word: str) -> str:
        word = word.replace("ı", "i").replace("İ", "I")

        return "".join(
            c
            for c in unicodedata.normalize("NFD", word)
            if unicodedata.category(c) != "Mn"
        )

    def _v(self, c: str) -> bool:
        return c in "aeiouAEIOU"

    def _c(self, c: str) -> bool:
        return c in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTUVWXYZ"
