#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .locale import LocaleLike


class ReadabilityFormula(Enum):
    """
    Enumeration of readability formulas supported by SmoothText.

    Attributes:
        Automated_Readability_Index (ReadabilityFormula): The Automated Readability Index formula.
        Coleman_Liau_Index (ReadabilityFormula): The Coleman-Liau Index formula.
        Dale_Chall (ReadabilityFormula): The Dale-Chall formula.
        Flesch_Kincaid_Grade (ReadabilityFormula): The Flesch-Kincaid Grade formula.
        Flesch_Kincaid_Grade_Simplified (ReadabilityFormula): The Flesch-Kincaid Grade Simplified formula.
        Flesch_Reading_Ease (ReadabilityFormula): The Flesch Reading Ease formula.
        Gunning_Fog_Index (ReadabilityFormula): The Gunning Fog Index formula.
        Smog_Index (ReadabilityFormula): The Smog Index formula.
        Amstad (ReadabilityFormula): The Amstad formula.
        Wiener_Sachtextformel (ReadabilityFormula): The Wiener Sachtextformel formula.
        Wiener_Sachtextformel_1 (ReadabilityFormula): The Wiener Sachtextformel 1 formula.
        Wiener_Sachtextformel_2 (ReadabilityFormula): The Wiener Sachtextformel 2 formula.
        Wiener_Sachtextformel_3 (ReadabilityFormula): The Wiener Sachtextformel 3 formula.
        Wiener_Sachtextformel_4 (ReadabilityFormula): The Wiener Sachtextformel 4 formula.
        Matskovskiy (ReadabilityFormula): The Matskovskiy formula.
        Atesman (ReadabilityFormula): The Atesman formula.
        Bezirci_Yilmaz (ReadabilityFormula): The Bezirci-Yılmaz formula.
        Cetinkaya_Uzun (ReadabilityFormula): The Çetinkaya-Uzun formula.
    """

    # Formulas for English.
    Automated_Readability_Index = "Automated Readability Index"
    Coleman_Liau_Index = "Coleman-Liau Index"
    Dale_Chall = "Dale-Chall"
    Flesch_Kincaid_Grade = "Flesch-Kincaid Grade"
    Flesch_Kincaid_Grade_Simplified = "Flesch-Kincaid Grade Simplified"
    Flesch_Reading_Ease = "Flesch Reading Ease"
    Gunning_Fog_Index = "Gunning Fog Index"
    Smog_Index = "Smog Index"

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
    Cetinkaya_Uzun = "Çetinkaya-Uzun"

    def supports(self, locale: LocaleLike) -> bool:
        """
        Check if the formula is supported for the given locale.

        Args:
            locale (LocaleLike): The locale to check.

        Returns:
            bool: True if the formula is supported for the given locale, False otherwise.
        """
        from .locale import Locale

        locale: Locale | None = Locale.parse(locale)
        if locale is None:
            return False

        return self in ReadabilityFormula.list(locale)

    @staticmethod
    def list(locale: LocaleLike | None = None) -> list[ReadabilityFormula]:
        """
        Get the list of supported readability formulas for the given locale.

        Args:
            locale (LocaleLike | None): The locale to get the list of supported readability formulas for. If None, returns the list of supported readability formulas for all locales.

        Returns:
            list[ReadabilityFormula]: The list of supported readability formulas for the given locale.
        """
        from .locale import Locale
        from .language import Language

        formulas: list[ReadabilityFormula] = []

        if locale is not None:
            locale: Locale | None = Locale.parse(locale)
            if locale is None:
                return formulas

        if locale is None or locale.language == Language.English:
            formulas.extend(
                [
                    ReadabilityFormula.Automated_Readability_Index,
                    ReadabilityFormula.Coleman_Liau_Index,
                    ReadabilityFormula.Dale_Chall,
                    ReadabilityFormula.Flesch_Kincaid_Grade,
                    ReadabilityFormula.Flesch_Kincaid_Grade_Simplified,
                    ReadabilityFormula.Flesch_Reading_Ease,
                    ReadabilityFormula.Gunning_Fog_Index,
                    ReadabilityFormula.Smog_Index,
                ]
            )

        if locale is None or locale.language == Language.German:
            formulas.extend(
                [
                    ReadabilityFormula.Amstad,
                    ReadabilityFormula.Wiener_Sachtextformel,
                    ReadabilityFormula.Wiener_Sachtextformel_1,
                    ReadabilityFormula.Wiener_Sachtextformel_2,
                    ReadabilityFormula.Wiener_Sachtextformel_3,
                    ReadabilityFormula.Wiener_Sachtextformel_4,
                ]
            )

        if locale is None or locale.language == Language.Russian:
            formulas.extend([ReadabilityFormula.Matskovskiy])

        if locale is None or locale.language == Language.Turkish:
            formulas.extend(
                [
                    ReadabilityFormula.Atesman,
                    ReadabilityFormula.Bezirci_Yilmaz,
                    ReadabilityFormula.Cetinkaya_Uzun,
                ]
            )

        return formulas
