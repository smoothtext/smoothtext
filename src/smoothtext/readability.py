#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

"""
Readability formulas module for SmoothText.

This module provides an enumeration of various readability formulas that can
be used to assess text complexity in different languages. Each formula is
designed for specific languages and provides different metrics for text
readability.

Examples:
    >>> from smoothtext import ReadabilityFormula
    >>> formula = ReadabilityFormula.Flesch_Reading_Ease
    >>> print(formula.value)
    Flesch Reading Ease
    >>> print(formula.supports(Language.English))
    True
    >>> print(formula.supports(Language.Turkish))
    False
"""

from . import Language

from enum import Enum
from typing import Union


class ReadabilityFormula(Enum):
    """
    Enumeration of readability formulas supported by SmoothText.

    This enum defines various readability formulas that can be used to assess
    text complexity in different languages. Each formula is designed for specific
    languages and provides different metrics for text readability.

    Attributes:
        # English Formulas
        Automated_Readability_Index: English readability formula developed by the US Army.
        Flesch_Reading_Ease: Classic English readability formula.
                            Scores range from 0 (hardest) to 100 (easiest).
        Flesch_Kincaid_Grade: English grade-level assessment formula.
                             Indicates US grade level required to understand the text.
        Flesch_Kincaid_Grade_Simplified: Simplified version of Flesch-Kincaid Grade.
                                       Uses reduced parameters for grade-level assessment.
        Gunning_Fog_Index: English readability formula developed by Robert Gunning.

        # German Formulas
        Wiener_Sachtextformel: Alias for Wiener_Sachtextformel_3 (general purpose formula).
        Wiener_Sachtextformel_1: First variant of Wiener Sachtextformel.
                                Optimized for narrative texts.
        Wiener_Sachtextformel_2: Second variant of Wiener Sachtextformel.
                                Optimized for scientific texts.
        Wiener_Sachtextformel_3: Third variant of Wiener Sachtextformel.
                                General purpose formula.
        Wiener_Sachtextformel_4: Fourth variant of Wiener Sachtextformel.
                                Alternative general purpose formula.

        # Russian Formulas
        Matskovskiy: Russian readability formula developed by Matskovskiy.
                    Provides grade-level assessment for Russian texts.

        # Turkish Formulas
        Atesman: Turkish readability formula developed by Ateşman.
                Scores range from 0 (hardest) to 100 (easiest).
        Bezirci_Yilmaz: Turkish readability formula by Bezirci and Yılmaz.
                       Provides grade-level assessment for Turkish texts.
    """

    # Formulas for English.
    Automated_Readability_Index = "Automated Readability Index"
    Flesch_Reading_Ease = "Flesch Reading Ease"
    Flesch_Kincaid_Grade = "Flesch-Kincaid Grade"
    Flesch_Kincaid_Grade_Simplified = "Flesch-Kincaid Grade Simplified"
    Gunning_Fog_Index = "Gunning Fog Index"

    # Formulas for German.
    Amstad = "Amstad"
    Wiener_Sachtextformel = "Wiener Sachtextformel"
    Wiener_Sachtextformel_1 = "Wiener Sachtextformel 1"
    Wiener_Sachtextformel_2 = "Wiener Sachtextformel 2"
    Wiener_Sachtextformel_3 = "Wiener Sachtextformel 3"
    Wiener_Sachtextformel_4 = "Wiener Sachtextformel 4"

    # Formulas for Russian.
    Matskovskiy = "Matskovskiy"

    # Formulas for Turkish.
    Atesman = "Ateşman"
    Bezirci_Yilmaz = "Bezirci-Yılmaz"

    # Formula-Language Supports.
    def supports(self, language: Union["Language", str, None]) -> bool:
        """
        Determines if the formula supports the specified language.

        Args:
            language: The language to check support for.
                Can be either a Language enum value or a string identifier.

        Returns:
            bool:
                - True if the formula supports the specified language.
                - False if the formula does not support the language.
        """
        from . import Language

        if isinstance(language, str):
            language = Language.parse(language)

        if not isinstance(language, Language):
            return False

        return self in language.readability_formulas()
