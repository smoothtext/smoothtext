#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .base import TokenizerBase
from .nltk import TokenizerNLTK
from .spacy import TokenizerSpaCy
from .stanza import TokenizerStanza

from smoothtext.backend import Backend
from smoothtext.locale import Locale


def get_tokenizer(backend: Backend, locale: Locale) -> TokenizerBase:
    if backend == Backend.NLTK:
        return TokenizerNLTK(locale)

    if backend == Backend.SpaCy:
        return TokenizerSpaCy(locale)

    if backend == Backend.Stanza:
        return TokenizerStanza(locale)

    raise ValueError(f"Unsupported backend: {backend}")
