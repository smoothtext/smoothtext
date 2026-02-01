#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _flesch_reading_ease_base(
    c1: float,
    c2: float,
    c3: float,
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences = tokenizer.tokenize(
        text=text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_words: int = sum(len(sentence) for sentence in sentences)
    num_syllables: int = sum(
        syllabifier.count(word) for sentence in sentences for word in sentence
    )

    return c1 - (c2 * (num_words / num_sentences)) - (c3 * (num_syllables / num_words))


def _flesch_reading_ease(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _flesch_reading_ease_base(
        206.835,
        1.015,
        84.6,
        text,
        tokenizer,
        syllabifier,
    )
