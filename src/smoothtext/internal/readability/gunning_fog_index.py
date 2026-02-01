#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/


from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase


def _gunning_fog_index(
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences: list[list[tuple[str, str]]] = tokenizer.tokenize(
        text=text, sentencize=True, words=True, remove_punct=True, include_tags=True
    )

    num_sentences: int = len(sentences)
    num_words: int = 0
    num_complex_words: int = 0

    for sentence in sentences:
        num_words += len(sentence)
        for word, upos in sentence:
            if upos == "PROPN":
                continue

            if syllabifier.count(word) >= 3:
                num_complex_words += 1

    return 0.4 * ((num_words / num_sentences) + 100 * (num_complex_words / num_words))
