#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

try:
    import nltk
except ImportError:
    pass

import string

from .base import TokenizerBase
from ...locale import Locale


class TokenizerNLTK(TokenizerBase):
    def __init__(self, locale: Locale) -> None:
        self._sentencizer = nltk.PunktTokenizer(locale.language.name.lower())
        self._tokenizer = nltk.NLTKWordTokenizer()
        self._language: str = locale.language.alpha3

    def sentencize(self, text: str) -> list[str]:
        return self._sentencizer.tokenize(text)

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
        sentences: list[str] = self.sentencize(text)
        tokens: list[list[str]] = []

        if words:
            for sentence in sentences:
                tokens.append(self._t(sentence, include_tags))
        else:
            for sentence in sentences:
                ss: list[tuple[int, int]] = list(
                    self._tokenizer.span_tokenize(sentence)
                )
                tt: list[str] = [sentence[s[0] : s[1]] for s in ss]

                m: list[str] = []
                b: str = ""
                p: int = -1

                for i, (start, end) in enumerate(ss):
                    t = tt[i]
                    if start == p and t not in string.punctuation:
                        b += t
                    else:
                        if b:
                            m.append(b)
                        b = t

                    p = end

                if b:
                    m.append(b)

                tokens.append(m)

        if remove_punct:
            if words and include_tags:
                for i, sentence in enumerate(tokens):
                    tokens[i] = [t for t in sentence if t[1] != "."]
            else:
                for i, sentence in enumerate(tokens):
                    tokens[i] = [t for t in sentence if any(c.isalnum() for c in t)]

            tokens = [t for t in tokens if t]

        if sentencize:
            return tokens

        res: list[str] = []
        for sentence in tokens:
            res.extend(sentence)

        return res

    def _t(
        self, sentence: str, include_tags: bool
    ) -> list[str] | list[tuple[str, str]]:
        tokens: list[str] = self._tokenizer.tokenize(sentence, False, False)
        if not include_tags:
            return tokens

        return nltk.pos_tag(tokens, tagset="universal", lang=self._language)
