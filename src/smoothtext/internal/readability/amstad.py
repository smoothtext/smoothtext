#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .flesch_reading_ease import _flesch_reading_ease_base
from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _amstad(text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase) -> float:
    return _flesch_reading_ease_base(
        180.0,
        1.0,
        58.5,
        text,
        tokenizer,
        syllabifier,
    )
