#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

import math

from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _smog_index(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_polysyllabic_words: int = 0

    for sentence in sentences:
        for word in sentence:
            if syllabifier.count(word) >= 3:
                num_polysyllabic_words += 1

    if num_polysyllabic_words == 0:
        return 0.0

    return 1.0430 * math.sqrt(num_polysyllabic_words * (30 / num_sentences)) + 3.1291
