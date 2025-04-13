import pytest
from smoothtext import SmoothText, Backend, Language, ReadabilityFormula


class TestTokenization:
    @pytest.fixture(scope="class")
    def available_backends(self):
        backends = []
        try:
            import nltk

            backends.append(Backend.NLTK)
        except ImportError:
            pass

        try:
            import stanza

            backends.append(Backend.Stanza)
        except ImportError:
            pass

        if not backends:
            pytest.skip("No supported backends available")
        return backends

    @pytest.fixture(params=["nltk", "stanza"])
    def backend(self, request, available_backends):
        backend = Backend.parse(request.param)
        if backend not in available_backends:
            pytest.skip(f"{backend} backend not available")
        return backend

    @pytest.fixture(
        params=[
            Language.English,
            Language.English_GB,
            Language.English_US,
            Language.German,
            Language.Turkish,
            Language.Turkish_TR,
        ]
    )
    def language(self, request):
        return request.param

    @pytest.fixture
    def st(self, backend, language):
        SmoothText.prepare(backend=backend, languages=[language])
        return SmoothText(language=language, backend=backend)

    # Sentence level tests
    def test_sentencize(self, st, language):
        if language.family() == Language.English:
            text = "This is a test. This is another test!"
            expected = ["This is a test.", "This is another test!"]
        elif language.family() == Language.German:
            text = "Dies ist ein Test. Dies ist noch ein Test!"
            expected = ["Dies ist ein Test.", "Dies ist noch ein Test!"]
        elif language.family() == Language.Turkish:
            text = "Bu bir test. Bu başka bir test!"
            expected = ["Bu bir test.", "Bu başka bir test!"]

        assert st.sentencize(text) == expected

    def test_count_sentences(self, st, language):
        if language.family() == Language.English:
            text = "I am going home. The sky is blue. Today is a beautiful day!"
        elif language.family() == Language.German:
            text = " gehe nach Hause. Der Himmel ist blau. Heute ist ein schöner Tag!"
        elif language.family() == Language.Turkish:
            text = "Ben eve gidiyorum. Gökyüzü mavi. Bugün güzel bir gün!"

        assert st.count_sentences(text) == 3

    # Word level tests
    def test_tokenize(self, st, language):
        if language.family() == Language.English:
            text = "Hello world!"
            expected = ["Hello", "world", "!"]
        elif language.family() == Language.German:
            text = "Hallo Welt!"
            expected = ["Hallo", "Welt", "!"]
        elif language.family() == Language.Turkish:
            text = "Merhaba dünya!"
            expected = ["Merhaba", "dünya", "!"]

        assert st.tokenize(text, split_sentences=False) == expected

    def test_tokenize_with_sentences(self, st, language):
        if language.family() == Language.English:
            text = "Hello world! Goodbye now."
            expected = [["Hello", "world", "!"], ["Goodbye", "now", "."]]
        elif language.family() == Language.German:
            text = "Hallo Welt! Auf Wiedersehen."
            expected = [["Hallo", "Welt", "!"], ["Auf", "Wiedersehen", "."]]
        elif language.family() == Language.Turkish:
            text = "Merhaba dünya! Hoşça kal."
            expected = [["Merhaba", "dünya", "!"], ["Hoşça", "kal", "."]]

        assert st.tokenize(text, split_sentences=True) == expected

    def test_count_words(self, st, language):
        if language.family() == Language.English:
            text = "Hello world! This is a test."
        elif language.family() == Language.German:
            text = "Hallo Welt! Dies ist ein Test."
        elif language.family() == Language.Turkish:
            text = "Merhaba dünya! Bu bir test metnidir."

        assert st.count_words(text) == 6

    # Syllable level tests
    def test_syllabify(self, st, language):
        if language.family() == Language.English:
            assert st.syllabify("perfectionist") == ["per", "fec", "tion", "ist"]
        elif language.family() == Language.German:
            assert st.syllabify("hallo") == ["hal", "lo"]
        elif language.family() == Language.Turkish:
            assert st.syllabify("merhaba") == ["mer", "ha", "ba"]

    def test_count_syllables(self, st, language):
        if language.family() == Language.English:
            assert st.count_syllables("hello") == 2
            assert st.count_syllables("hello world", tokenize=True) == 3
        elif language.family() == Language.Turkish:
            assert st.count_syllables("merhaba") == 3
            assert st.count_syllables("merhaba dünya", tokenize=True) == 5

    # Character level tests
    def test_count_consonants(self, st):
        assert st.count_consonants("hello") == 3
        assert st.count_consonants("world") == 4

    def test_count_vowels(self, st):
        assert st.count_vowels("hello") == 2
        assert st.count_vowels("world") == 1

    def test_demojize(self, st, language):
        if language.family() == Language.English:
            text = "I love 🐈"
            expected = "I love (cat)"
        elif language.family() == Language.German:
            text = "Ich liebe 🐈"
            expected = "Ich liebe (katze)"
        elif language.family() == Language.Turkish:
            text = "Ben 🐈 severim"
            expected = "Ben (kedi) severim"

        assert st.demojize(text) == expected

    def test_language_variants(self, available_backends):
        """Test that language variants are properly handled"""
        if not available_backends:
            pytest.skip("No supported backends available")

        # Test English variants
        st_eng = SmoothText(language=Language.English, backend=available_backends[0])
        st_gb = SmoothText(language=Language.English_GB, backend=available_backends[0])
        st_us = SmoothText(language=Language.English_US, backend=available_backends[0])

        assert st_eng.language.family() == Language.English
        assert st_gb.language.family() == Language.English
        assert st_us.language.family() == Language.English

        # Test German variants
        st_de = SmoothText(language=Language.German, backend=available_backends[0])
        st_de_de = SmoothText(
            language=Language.German_DE, backend=available_backends[0]
        )

        assert st_de.language.family() == Language.German
        assert st_de_de.language.family() == Language.German

        # Test Turkish variants
        st_tr = SmoothText(language=Language.Turkish, backend=available_backends[0])
        st_tr_tr = SmoothText(
            language=Language.Turkish_TR, backend=available_backends[0]
        )

        assert st_tr.language.family() == Language.Turkish
        assert st_tr_tr.language.family() == Language.Turkish
