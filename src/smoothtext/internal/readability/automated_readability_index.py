#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/


from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _automated_readability_index(
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text=text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_words: int = sum(len(sentence) for sentence in sentences)
    num_characters: int = sum(len(word) for sentence in sentences for word in sentence)

    return (
        (4.71 * (num_characters / num_words))
        + (0.5 * (num_words / num_sentences))
        - 21.43
    )
