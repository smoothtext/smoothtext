#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from abc import ABC, abstractmethod


class SyllabifierBase(ABC):
    @abstractmethod
    def syllabify(self, word: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def count(self, word: str) -> int:
        raise NotImplementedError
