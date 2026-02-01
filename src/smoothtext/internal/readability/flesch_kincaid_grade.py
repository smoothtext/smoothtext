#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _flesch_kincaid_grade_base(
    c1: float,
    c2: float,
    c3: float,
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text=text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    if not sentences:
        return 0.0

    num_sentences: int = len(sentences)
    num_words: int = sum(len(sentence) for sentence in sentences)
    num_syllables: int = sum(
        syllabifier.count(word) for sentence in sentences for word in sentence
    )

    return (c1 * (num_words / num_sentences)) + (c2 * (num_syllables / num_words)) - c3


def _flesch_kincaid_grade(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _flesch_kincaid_grade_base(0.39, 11.8, 15.59, text, tokenizer, syllabifier)


def _flesch_kincaid_grade_simplified(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _flesch_kincaid_grade_base(0.4, 12.0, 16.0, text, tokenizer, syllabifier)
