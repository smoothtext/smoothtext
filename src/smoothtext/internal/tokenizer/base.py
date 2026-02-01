#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from abc import ABC, abstractmethod


class TokenizerBase(ABC):
    @abstractmethod
    def sentencize(self, text: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def tokenize(
        self,
        text: str,
        sentencize: bool,
        words: bool,
        remove_punct: bool,
        include_tags: bool,
    ) -> (
        list[str]
        | list[tuple[str, str]]
        | list[list[str]]
        | list[list[tuple[str, str]]]
    ):
        raise NotImplementedError
