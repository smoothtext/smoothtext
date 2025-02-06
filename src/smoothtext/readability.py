#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from . import Language

from enum import Enum


class ReadabilityFormula(Enum):
    """
    Enumeration of readability formulas supported by SmoothText.

    This enum defines various readability formulas that can be used to assess
    text complexity in different languages. Each formula is designed for specific
    languages and provides different metrics for text readability.

    Attributes:
        Atesman: Turkish readability formula developed by Ateşman.
                Scores range from 0 (hardest) to 100 (easiest).
        Bezirci_Yilmaz: Turkish readability formula by Bezirci and Yılmaz.
                       Provides grade-level assessment for Turkish texts.
        Flesch_Reading_Ease: Classic English readability formula.
                            Scores range from 0 (hardest) to 100 (easiest).
        Flesch_Kincaid_Grade: English grade-level assessment formula.
                             Indicates US grade level required to understand the text.
        Flesch_Kincaid_Grade_Simplified: Simplified version of Flesch-Kincaid Grade.
                                       Uses reduced parameters for grade-level assessment.
    """

    # Formulas for Turkish.
    Atesman = "Ateşman"
    Bezirci_Yilmaz = "Bezirci-Yılmaz"

    # Formulas for English.
    Flesch_Reading_Ease = "Flesch Reading Ease"
    Flesch_Kincaid_Grade = "Flesch-Kincaid Grade"
    Flesch_Kincaid_Grade_Simplified = "Flesch-Kincaid Grade Simplified"

    # Formula-Language Supports.
    def supports(self, language: Language) -> bool:
        """
        Determines if the formula supports the specified language.

        Args:
            language (Language): The language to check for formula support.

        Returns:
            bool: True if the formula supports the specified language, False otherwise.
        """
        if Language.English == language.family():
            return self in [
                ReadabilityFormula.Flesch_Reading_Ease,
                ReadabilityFormula.Flesch_Kincaid_Grade,
                ReadabilityFormula.Flesch_Kincaid_Grade_Simplified,
            ]

        if Language.Turkish == language.family():
            return self in [
                ReadabilityFormula.Atesman,
                ReadabilityFormula.Bezirci_Yilmaz,
            ]

        return False
