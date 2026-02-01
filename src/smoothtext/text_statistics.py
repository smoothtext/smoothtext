#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from dataclasses import dataclass


@dataclass
class TextStatistics:
    """
    Text statistics for SmoothText.

    Attributes:
        num_sentences (int): Number of sentences.
        num_words (int): Number of words.
        num_syllables (int): Number of syllables.
        syllable_frequencies (dict[int, int]): Frequency of syllables.
        word_frequencies (dict[str, int]): Frequency of words.
    """

    num_sentences: int
    num_words: int
    num_syllables: int
    syllable_frequencies: dict[int, int]
    word_frequencies: dict[str, int]

    def __init__(
        self,
        num_sentences: int = 0,
        num_words: int = 0,
        num_syllables: int = 0,
        syllable_frequencies: dict[int, int] = None,
        word_frequencies: dict[str, int] = None,
    ):
        self.num_sentences = num_sentences
        self.num_words = num_words
        self.num_syllables = num_syllables
        self.syllable_frequencies = syllable_frequencies or {}
        self.word_frequencies = word_frequencies or {}
