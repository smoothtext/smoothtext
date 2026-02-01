#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .amstad import _amstad
from .atesman import _atesman
from .automated_readability_index import _automated_readability_index
from .bezirci_yilmaz import _bezirci_yilmaz
from .coleman_liau_index import _coleman_liau_index
from .cetinkaya_uzun import _cetinkaya_uzun
from .dale_chall import _dale_chall
from .flesch_kincaid_grade import (
    _flesch_kincaid_grade,
    _flesch_kincaid_grade_simplified,
)
from .flesch_reading_ease import _flesch_reading_ease
from .gunning_fog_index import _gunning_fog_index
from .matskovskiy import _matskovskiy
from .smog_index import _smog_index
from .wiener_sachtextformel import (
    _wiener_sachtextformel,
    _wiener_sachtextformel_1,
    _wiener_sachtextformel_2,
    _wiener_sachtextformel_3,
    _wiener_sachtextformel_4,
)
from ..tokenizer.base import TokenizerBase
from ..syllabifier.base import SyllabifierBase
from ...readability_formula import ReadabilityFormula

_R: dict[ReadabilityFormula, callable] = {
    ReadabilityFormula.Amstad: _amstad,
    ReadabilityFormula.Atesman: _atesman,
    ReadabilityFormula.Automated_Readability_Index: _automated_readability_index,
    ReadabilityFormula.Bezirci_Yilmaz: _bezirci_yilmaz,
    ReadabilityFormula.Coleman_Liau_Index: _coleman_liau_index,
    ReadabilityFormula.Cetinkaya_Uzun: _cetinkaya_uzun,
    ReadabilityFormula.Dale_Chall: _dale_chall,
    ReadabilityFormula.Flesch_Reading_Ease: _flesch_reading_ease,
    ReadabilityFormula.Flesch_Kincaid_Grade: _flesch_kincaid_grade,
    ReadabilityFormula.Flesch_Kincaid_Grade_Simplified: _flesch_kincaid_grade_simplified,
    ReadabilityFormula.Gunning_Fog_Index: _gunning_fog_index,
    ReadabilityFormula.Matskovskiy: _matskovskiy,
    ReadabilityFormula.Smog_Index: _smog_index,
    ReadabilityFormula.Wiener_Sachtextformel: _wiener_sachtextformel,
    ReadabilityFormula.Wiener_Sachtextformel_1: _wiener_sachtextformel_1,
    ReadabilityFormula.Wiener_Sachtextformel_2: _wiener_sachtextformel_2,
    ReadabilityFormula.Wiener_Sachtextformel_3: _wiener_sachtextformel_3,
    ReadabilityFormula.Wiener_Sachtextformel_4: _wiener_sachtextformel_4,
}


def _R_(
    formula: ReadabilityFormula,
    text: str,
    tokenizer: TokenizerBase,
    syllabifier: SyllabifierBase,
) -> float:
    return _R.get(formula)(text, tokenizer, syllabifier)
