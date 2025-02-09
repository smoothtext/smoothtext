import pytest
from smoothtext.readability import ReadabilityFormula
from smoothtext.language import Language

def test_formula_supports_correct_languages():
    # Test English formulas
    assert ReadabilityFormula.Flesch_Reading_Ease.supports(Language.English)
    assert ReadabilityFormula.Flesch_Kincaid_Grade.supports(Language.English)
    assert ReadabilityFormula.Flesch_Kincaid_Grade_Simplified.supports(Language.English)
    
    # Test German formulas
    assert ReadabilityFormula.Flesch_Reading_Ease.supports(Language.German)
    assert ReadabilityFormula.Wiener_Sachtextformel.supports(Language.German)
    assert ReadabilityFormula.Wiener_Sachtextformel_1.supports(Language.German)
    assert ReadabilityFormula.Wiener_Sachtextformel_2.supports(Language.German)
    assert ReadabilityFormula.Wiener_Sachtextformel_3.supports(Language.German)
    assert ReadabilityFormula.Wiener_Sachtextformel_4.supports(Language.German)
    
    # Test Turkish formulas
    assert ReadabilityFormula.Atesman.supports(Language.Turkish)
    assert ReadabilityFormula.Bezirci_Yilmaz.supports(Language.Turkish)

    # Test with language variants
    assert ReadabilityFormula.Flesch_Reading_Ease.supports(Language.English_GB)
    assert ReadabilityFormula.Wiener_Sachtextformel.supports(Language.German_DE)
    assert ReadabilityFormula.Atesman.supports(Language.Turkish_TR)

def test_formula_rejects_wrong_languages():
    # English formulas should not support other languages
    assert not ReadabilityFormula.Flesch_Reading_Ease.supports(Language.Turkish)
    assert not ReadabilityFormula.Flesch_Kincaid_Grade.supports(Language.Turkish)
    assert not ReadabilityFormula.Flesch_Kincaid_Grade.supports(Language.German)
    
    # German formulas should not support other languages
    assert not ReadabilityFormula.Wiener_Sachtextformel.supports(Language.English)
    assert not ReadabilityFormula.Wiener_Sachtextformel.supports(Language.Turkish)
    assert not ReadabilityFormula.Wiener_Sachtextformel_3.supports(Language.English)
    
    # Turkish formulas should not support other languages
    assert not ReadabilityFormula.Atesman.supports(Language.English)
    assert not ReadabilityFormula.Bezirci_Yilmaz.supports(Language.English)
    assert not ReadabilityFormula.Atesman.supports(Language.German)

def test_formula_supports_with_invalid_language():
    # Test with None and invalid language values
    assert not ReadabilityFormula.Flesch_Reading_Ease.supports(None)  # type: ignore
    assert not ReadabilityFormula.Wiener_Sachtextformel.supports(None)  # type: ignore
    assert not ReadabilityFormula.Atesman.supports(None)  # type: ignore
