#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/


from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _matskovskiy(
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences: list[list[tuple[str, str]]] = tokenizer.tokenize(
        text=text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_words: int = 0
    num_complex_words: int = 0

    for sentence in sentences:
        num_words += len(sentence)
        for word in sentence:
            if syllabifier.count(word) >= 3:
                num_complex_words += 1

    return (
        (0.62 * (float(num_words) / float(num_sentences)))
        + (0.123 * (float(num_complex_words) / float(num_words)))
        + 0.051
    )
