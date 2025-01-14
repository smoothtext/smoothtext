#  SmoothText - https://smoothtext.tugrulgungor.me/
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from enum import Enum


class ReadabilityFormula(Enum):
    """
    Readability formulas supported by SmoothText.

    Attributes:
        Atesman: Ateşman formula.
        Bezirci_Yilmaz: Bezirci-Yılmaz formula.
        Flesch_Reading_Ease: Flesch Reading Ease formula.
        Flesch_Kincaid_Grade: Flesch-Kincaid Grade formula.
        Flesch_Kincaid_Grade_Simplified: Simplified version of the Flesch-Kincaid Grade formula.
    """

    Atesman = 'Atesman'
    Bezirci_Yilmaz = 'Bezirci-Yilmaz'
    Flesch_Reading_Ease = 'Flesch Reading Ease'
    Flesch_Kincaid_Grade = 'Flesch-Kincaid Grade'
    Flesch_Kincaid_Grade_Simplified = 'Flesch-Kincaid Grade Simplified'
