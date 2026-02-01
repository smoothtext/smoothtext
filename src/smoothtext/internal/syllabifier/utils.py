#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .base import SyllabifierBase
from .en import SyllabifierEnGB, SyllabifierEnUS
from .de import SyllabifierDe
from .ru import SyllabifierRu
from .tr import SyllabifierTr

from smoothtext.language import Language
from smoothtext.language_variant import LanguageVariant
from smoothtext.locale import Locale


def get_syllabifier(locale: Locale) -> SyllabifierBase:
    if LanguageVariant.English_GB == locale.language_variant:
        return SyllabifierEnGB()

    if LanguageVariant.English_US == locale.language_variant:
        return SyllabifierEnUS()

    if LanguageVariant.German_DE == locale.language_variant:
        return SyllabifierDe()

    if Language.Russian == locale.language:
        return SyllabifierRu()

    if Language.Turkish == locale.language:
        return SyllabifierTr()

    raise ValueError(
        f"Unsupported language or language variant: {locale.language} / {locale.language_variant}"
    )
