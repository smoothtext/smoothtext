#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _coleman_liau_index(
    text: str, tokenizer: TokenizerBase, syllabifier: SyllabifierBase
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_words: int = 0
    num_letters: int = 0

    for sentence in sentences:
        num_words += len(sentence)
        num_letters += sum(len(word) for word in sentence)

    L: float = (num_letters / num_words) * 100.0
    S: float = (num_sentences / num_words) * 100.0

    return 0.0588 * L - 0.296 * S - 15.8
