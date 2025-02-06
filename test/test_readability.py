import pytest
from smoothtext.readability import ReadabilityFormula
from smoothtext.language import Language

def test_formula_supports_correct_languages():
    # Test English formulas
    assert ReadabilityFormula.Flesch_Reading_Ease.supports(Language.English)
    assert ReadabilityFormula.Flesch_Kincaid_Grade.supports(Language.English)
    assert ReadabilityFormula.Flesch_Kincaid_Grade_Simplified.supports(Language.English)
    
    # Test Turkish formulas
    assert ReadabilityFormula.Atesman.supports(Language.Turkish)
    assert ReadabilityFormula.Bezirci_Yilmaz.supports(Language.Turkish)

def test_formula_rejects_wrong_languages():
    # English formulas should not support Turkish
    assert not ReadabilityFormula.Flesch_Reading_Ease.supports(Language.Turkish)
    assert not ReadabilityFormula.Flesch_Kincaid_Grade.supports(Language.Turkish)
    
    # Turkish formulas should not support English
    assert not ReadabilityFormula.Atesman.supports(Language.English)
    assert not ReadabilityFormula.Bezirci_Yilmaz.supports(Language.English)
