#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

try:
    import stanza
    import torch
except ImportError:
    pass

from .base import TokenizerBase
from ..backend.installer import _backend_model
from ...backend import Backend
from ...locale import Locale
from ...language import Language


class TokenizerStanza(TokenizerBase):
    def __init__(self, locale: Locale):
        args = _backend_model(Backend.Stanza, locale)
        if args is None:
            raise RuntimeError(
                f"Failed to load stanza model for locale {locale.language.name} ({locale.language_variant.name})"
            )

        if torch.cuda.is_available():
            args["use_gpu"] = True

        processors: list[str] = ["mwt", "pos", "tokenize"]
        if locale.language == Language.Russian:
            processors.remove("mwt")

        self._pipeline = stanza.Pipeline(
            lang=locale.language.alpha2,
            processors=",".join(processors),
            download_method=stanza.DownloadMethod.REUSE_RESOURCES,
            **args,
        )

    def sentencize(self, text: str) -> list[str]:
        return [sentence.text for sentence in self._pipeline(text).sentences]

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
        doc = self._pipeline(text)

        if sentencize:
            return [
                [
                    self._t(token, include_tags)
                    for token in (sentence.words if words else sentence.tokens)
                    if self._p(token, remove_punct)
                ]
                for sentence in doc.sentences
            ]

        res: list[str] = []
        for sentence in doc.sentences:
            res.extend(
                [
                    self._t(token, include_tags)
                    for token in (sentence.words if words else sentence.tokens)
                    if self._p(token, remove_punct)
                ]
            )

        return res

    @staticmethod
    def _p(token, remove_punct: bool) -> bool:
        if not remove_punct:
            return True

        if not any(c.isalnum() for c in token.text):
            return False

        if hasattr(token, "upos"):
            return token.upos != "PUNCT"

        if hasattr(token, "words"):
            return any(word.upos != "PUNCT" for word in token.words)

        return False

    @staticmethod
    def _t(token, include_tags: bool) -> str | tuple[str, str]:
        if include_tags:
            return token.text, token.upos

        return token.text
