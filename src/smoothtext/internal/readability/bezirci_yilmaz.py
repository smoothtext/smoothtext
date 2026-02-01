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


def _bezirci_yilmaz(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_words: int = sum(len(sentence) for sentence in sentences)
    num_syllables: int = 0
    syllable_frequencies: dict[int, int] = {3: 0, 4: 0, 5: 0, 6: 0}
    for sentence in sentences:
        for word in sentence:
            word_syllable_count: int = syllabifier.count(word=word)
            num_syllables += word_syllable_count

            if 3 <= word_syllable_count:
                if word_syllable_count > 6:
                    word_syllable_count = 6

                syllable_frequencies[word_syllable_count] += 1

    if not num_sentences:
        return 0.0

    score: float = 0.0
    score += (float(syllable_frequencies[3]) / float(num_sentences)) * 0.84
    score += (float(syllable_frequencies[4]) / float(num_sentences)) * 1.5
    score += (float(syllable_frequencies[5]) / float(num_sentences)) * 3.5
    score += (float(syllable_frequencies[6]) / float(num_sentences)) * 26.25

    return math.sqrt((num_words / num_sentences) * score)
