#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from typing import Literal

from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _wiener_sachtextformel_base(
    version: Literal[1, 2, 3, 4],
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
    num_words: int = 0
    num_long_words: int = 0
    num_mono_syllable_words: int = 0
    num_multi_syllable_words: int = 0

    for sentence in sentences:
        num_words += len(sentence)

        for word in sentence:
            word = word.lower()
            if 6 <= len(word):
                num_long_words += 1

            word_syllable_count: int = syllabifier.count(word)
            if word_syllable_count == 1:
                num_mono_syllable_words += 1
            elif word_syllable_count >= 3:
                num_multi_syllable_words += 1

    SL: float = num_words / num_sentences
    IW: float = num_long_words / num_words * 100.0
    ES: float = num_mono_syllable_words / num_words * 100.0
    MS: float = num_multi_syllable_words / num_words * 100.0

    if 1 == version:
        return 0.1935 * MS + 0.1672 * SL + 0.1297 * IW - 0.0327 * ES - 0.875

    if 2 == version:
        return 0.2007 * MS + 0.1682 * SL + 0.1373 * IW - 2.779

    if 3 == version:
        return 0.2963 * MS + 0.1905 * SL - 1.1144

    if 4 == version:
        return 0.2744 * MS + 0.2656 * SL - 1.693

    return 0.0


def _wiener_sachtextformel(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _wiener_sachtextformel_4(text, tokenizer, syllabifier)


def _wiener_sachtextformel_1(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _wiener_sachtextformel_base(1, text, tokenizer, syllabifier)


def _wiener_sachtextformel_2(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _wiener_sachtextformel_base(2, text, tokenizer, syllabifier)


def _wiener_sachtextformel_3(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _wiener_sachtextformel_base(3, text, tokenizer, syllabifier)


def _wiener_sachtextformel_4(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    return _wiener_sachtextformel_base(4, text, tokenizer, syllabifier)
