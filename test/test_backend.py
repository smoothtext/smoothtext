import pytest
from unittest.mock import patch
from smoothtext.backend import Backend


@pytest.fixture
def all_backends():
    """Fixture providing all available backends"""
    return [Backend.NLTK, Backend.Stanza]


def test_backend_values(all_backends):
    """Test that values() returns all defined backends"""
    assert Backend.values() == all_backends


@pytest.mark.parametrize(
    "input_backend,expected",
    [
        (Backend.NLTK, Backend.NLTK),
        ("nltk", Backend.NLTK),
        ("NLTK", Backend.NLTK),
        ("stanza", Backend.Stanza),
        ("invalid", None),
        (None, None),
        (123, None),
    ],
)
def test_backend_parse(input_backend, expected):
    """Test backend parsing with various input types"""
    assert Backend.parse(input_backend) == expected


@pytest.mark.parametrize(
    "backend_name,import_succeeds,expected",
    [
        ("nltk", True, True),
        ("stanza", True, True),
        ("nltk", False, False),
        ("invalid", False, False),
    ],
)
def test_backend_is_supported(backend_name, import_succeeds, expected):
    """Test backend support checking with mocked imports"""
    with patch("importlib.import_module") as mock_import:
        if import_succeeds:
            mock_import.return_value = True
        else:
            mock_import.side_effect = ImportError

        assert Backend.is_supported(backend_name) == expected


def test_list_supported_empty():
    """Test list_supported when no backends are available"""
    with patch("importlib.import_module", side_effect=ImportError):
        assert Backend.list_supported() == []


def test_list_supported_partial():
    """Test list_supported when only some backends are available"""

    def mock_import(name):
        if name == "nltk":
            return True
        raise ImportError

    with patch("importlib.import_module", side_effect=mock_import):
        supported = Backend.list_supported()
        assert len(supported) == 1
        assert Backend.NLTK in supported
        assert Backend.Stanza not in supported


def test_list_supported_all():
    """Test list_supported when all backends are available"""
    with patch("importlib.import_module", return_value=True):
        supported = Backend.list_supported()
        assert len(supported) == len(Backend.values())
        assert all(backend in supported for backend in Backend.values())


def test_backend_enum_values():
    """Test that Backend enum has the expected values"""
    assert Backend.NLTK.value == "NLTK"
    assert Backend.Stanza.value == "Stanza"
