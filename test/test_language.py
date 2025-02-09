import pytest
from smoothtext.language import Language


def test_language_codes():
    # Base languages
    assert Language.English.alpha2() == "en"
    assert Language.English.alpha3() == "eng"
    assert Language.Turkish.alpha2() == "tr"
    assert Language.Turkish.alpha3() == "tur"
    assert Language.German.alpha2() == "de"
    assert Language.German.alpha3() == "deu"

    # English variants
    assert Language.English_GB.alpha2() == "en"
    assert Language.English_GB.alpha3() == "eng"
    assert Language.English_US.alpha2() == "en"
    assert Language.English_US.alpha3() == "eng"

    # German variants
    assert Language.German_DE.alpha2() == "de"
    assert Language.German_DE.alpha3() == "deu"

    # Turkish variants
    assert Language.Turkish_TR.alpha2() == "tr"
    assert Language.Turkish_TR.alpha3() == "tur"


def test_language_family():
    # English family
    assert Language.English.family() == Language.English
    assert Language.English_GB.family() == Language.English
    assert Language.English_US.family() == Language.English

    # German family
    assert Language.German.family() == Language.German
    assert Language.German_DE.family() == Language.German

    # Turkish family
    assert Language.Turkish.family() == Language.Turkish
    assert Language.Turkish_TR.family() == Language.Turkish


def test_language_parse():
    # Test English variants
    assert Language.parse("English") == Language.English_US  # Default to US
    assert Language.parse("en") == Language.English_US
    assert Language.parse("eng") == Language.English_US
    assert Language.parse("en-GB") == Language.English_GB
    assert Language.parse("en_GB") == Language.English_GB
    assert Language.parse("eng-GB") == Language.English_GB
    assert Language.parse("eng_GB") == Language.English_GB
    assert Language.parse("en-US") == Language.English_US
    assert Language.parse("en_US") == Language.English_US
    assert Language.parse("English (Great Britain)") == Language.English_GB
    assert Language.parse("English (United States)") == Language.English_US

    # Test German variants
    assert Language.parse("German") == Language.German_DE  # Default to DE
    assert Language.parse("de") == Language.German_DE
    assert Language.parse("deu") == Language.German_DE
    assert Language.parse("de-DE") == Language.German_DE
    assert Language.parse("de_DE") == Language.German_DE
    assert Language.parse("deu-DE") == Language.German_DE
    assert Language.parse("deu_DE") == Language.German_DE
    assert Language.parse("German (Germany)") == Language.German_DE

    # Test Turkish variants
    assert Language.parse("Turkish") == Language.Turkish_TR  # Default to TR
    assert Language.parse("tr") == Language.Turkish_TR
    assert Language.parse("tur") == Language.Turkish_TR
    assert Language.parse("tr-TR") == Language.Turkish_TR
    assert Language.parse("tr_TR") == Language.Turkish_TR
    assert Language.parse("tur-TR") == Language.Turkish_TR
    assert Language.parse("tur_TR") == Language.Turkish_TR
    assert Language.parse("Turkish (Türkiye)") == Language.Turkish_TR

    # Test case insensitivity
    assert Language.parse("EN-us") == Language.English_US
    assert Language.parse("en-Us") == Language.English_US
    assert Language.parse("TR-tr") == Language.Turkish_TR
    assert Language.parse("DE-de") == Language.German_DE

    # Test invalid inputs
    assert Language.parse("invalid") is None
    assert Language.parse("en-FR") is None  # Invalid country code
    assert Language.parse("") is None
    assert Language.parse(None) is None


def test_language_parse_multiple():
    # Test parsing single values (order doesn't matter here)
    assert set(Language.parse_multiple("en")) == {Language.English_US}
    assert set(Language.parse_multiple(Language.Turkish_TR)) == {Language.Turkish_TR}

    # Test parsing comma-separated string
    assert set(Language.parse_multiple("en,tr")) == {
        Language.English_US,
        Language.Turkish_TR,
    }

    # Test parsing list of values
    result = set(Language.parse_multiple(["en", "tr"]))
    expected = {Language.English_US, Language.Turkish_TR}
    assert result == expected

    # Test handling invalid values (convert to set to ignore order)
    result = set(Language.parse_multiple("en,invalid,tr"))
    expected = {Language.English_US, Language.Turkish_TR}
    assert result == expected

    result = set(Language.parse_multiple(["en", None, "tr"]))
    expected = {Language.English_US, Language.Turkish_TR}
    assert result == expected

    # Test parsing with variants
    assert set(Language.parse_multiple("en-GB,en-US")) == {
        Language.English_GB,
        Language.English_US,
    }
    assert set(Language.parse_multiple("en,tr-TR")) == {
        Language.English_US,
        Language.Turkish_TR,
    }

    # Test with mixed separators
    assert set(Language.parse_multiple(["en_GB", "en-US"])) == {
        Language.English_GB,
        Language.English_US,
    }


def test_language_values():
    # Test that values() returns all supported languages
    assert set(Language.values()) == {
        Language.English,
        Language.English_GB,
        Language.English_US,
        Language.German,
        Language.German_DE,
        Language.Turkish,
        Language.Turkish_TR,
    }


def test_language_string_representation():
    # Test base languages
    assert str(Language.English) == "English"
    assert str(Language.Turkish) == "Turkish"
    assert str(Language.German) == "German"

    # Test variants
    assert str(Language.English_GB) == "English (Great Britain)"
    assert str(Language.English_US) == "English (United States)"
    assert str(Language.Turkish_TR) == "Turkish (Türkiye)"
    assert str(Language.German_DE) == "German (Germany)"
