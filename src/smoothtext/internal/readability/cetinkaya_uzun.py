#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/


from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase
from ...resource_manager import ResourceManager


def _cetinkaya_uzun(
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text=text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    num_sentences: int = len(sentences)
    num_words: int = 0
    num_letters: int = 0

    for sentence in sentences:
        num_words += len(sentence)
        num_letters += sum(len(word) for word in sentence)

    AWL: float = num_letters / num_words
    ASL: float = num_words / num_sentences

    return 118.823 - (25.987 * AWL) - (0.971 * ASL)
