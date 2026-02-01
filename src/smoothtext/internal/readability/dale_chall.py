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


def _dale_chall(
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    sentences: list[list[str]] = tokenizer.tokenize(
        text=text, sentencize=True, words=False, remove_punct=True, include_tags=False
    )

    wordlist: list[str] = ResourceManager.get_dale_chall_wordlist()

    num_sentences: int = len(sentences)
    num_words: int = 0
    num_difficult_words: int = 0

    for sentence in sentences:
        num_words += len(sentence)

        for word in sentence:
            if word.lower() not in wordlist:
                num_difficult_words += 1

    return (
        0.1579 * ((num_difficult_words / num_words) * 100.0)
        + 0.0496 * (num_words / num_sentences)
        + 3.63
    )
