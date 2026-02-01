#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

try:
    import spacy
except ImportError:
    pass

from .base import TokenizerBase
from ..backend.installer import _backend_model
from ...backend import Backend
from ...locale import Locale


class TokenizerSpaCy(TokenizerBase):
    def __init__(self, locale: Locale) -> None:
        model: str | None = _backend_model(Backend.SpaCy, locale)
        if model is None:
            raise RuntimeError(
                f"Failed to load SpaCy model for locale {locale.language.name} ({locale.language_variant.name})"
            )

        self._processor = spacy.load(model)

    def sentencize(self, text: str) -> list[str]:
        return [sentence.text for sentence in self._processor(text).sents]

    def tokenize(
        self,
        text: str,
        sentencize: bool,
        words: bool,
        remove_punct: bool,
        include_tags: bool,
    ) -> (
        list[str]
        | list[tuple[str, str]]
        | list[list[str]]
        | list[list[tuple[str, str]]]
    ):
        doc = self._processor(text)

        if words:
            if sentencize:
                return [
                    [
                        self._t(token, include_tags)
                        for token in sentence
                        if not remove_punct or not token.is_punct
                    ]
                    for sentence in doc.sents
                ]
            else:
                return [
                    self._t(token, include_tags)
                    for token in doc
                    if not remove_punct or not token.is_punct
                ]

        if sentencize:
            return [self._m(sentence, remove_punct) for sentence in doc.sents]
        else:
            return self._m(doc, remove_punct)

    def _m(self, tokens: list, remove_punct: bool) -> list[str]:
        t: list[str] = []
        n: int = len(tokens)
        b: str = ""
        for i, token in enumerate(tokens):
            if not remove_punct or not token.is_punct:
                b += token.text

            if not token.whitespace_ and i + 1 < n:
                if not tokens[i + 1].is_punct:
                    continue

            if b:
                t.append(b)
                b = ""

        return t

    def _t(self, token, include_tags: bool) -> str | tuple[str, str]:
        if include_tags:
            return token.text, token.pos_

        return token.text
