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
            if language == Language.English_GB:
                assert st.syllabify("hello") == ["hello"]
            elif language == Language.English_US:
                assert st.syllabify("hello") == ["hel", "lo"]
        elif language.family() == Language.German:
            assert st.syllabify("hallo") == ["hal", "lo"]
        elif language.family() == Language.Turkish:
            assert st.syllabify("merhaba") == ["mer", "ha", "ba"]

    def test_count_syllables(self, st, language):
        if language.family() == Language.English:
            if language == Language.English_GB:
                assert st.count_syllables("hello") == 1
                assert st.count_syllables("hello world", tokenize=True) == 2
            elif language == Language.English_US:
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


class TestReadability:
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

        return backends

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
    def st(self, available_backends, language):
        if not available_backends:
            pytest.skip("No supported backends available")
        SmoothText.prepare(backend=available_backends[0], languages=[language])
        return SmoothText(language=language, backend=available_backends[0])

    # Test Flesch Reading Ease
    def test_flesch_reading_ease(self, st, language):
        if language.family() == Language.English:
            # Very easy text
            text = "The cat sat on the mat."
            score = st.flesch_reading_ease(text)
            assert 116 <= score <= 117

            # More complex text
            text = "The intricate mechanisms of quantum physics challenge our fundamental understanding of reality."
            score = st.flesch_reading_ease(text)

            if language == Language.English_GB:
                assert 18 <= score <= 19
            elif language == Language.English_US:
                assert 4 <= score <= 5
        elif language.family() == Language.Turkish:
            pytest.skip("Flesch Reading Ease is primarily for English")

    # Test Ateşman (Turkish)
    def test_atesman(self, st, language):
        if language.family() == Language.Turkish:
            # Simple text
            text = "Kedi masada uyuyor."
            score = st.atesman(text)
            assert 83 <= score <= 84

            # Complex text
            text = "Kuantum fiziğinin karmaşık mekanizmaları, gerçekliği anlamamızı zorlaştırıyor."
            score = st.atesman(text)
            assert 8 <= score <= 9
        else:  # English family
            pytest.skip("Ateşman is only for Turkish texts")

    # Test Flesch-Kincaid Grade Level
    def test_flesch_kincaid_grade(self, st, language):
        if language.family() == Language.English:
            # Elementary level text
            text = "The dog ran fast. The cat jumped high."
            score = st.flesch_kincaid_grade(text)
            assert -3 <= score <= -2

            # Advanced level text
            text = "The quantum mechanical phenomena exhibit intrinsic probabilistic behavior."
            score = st.flesch_kincaid_grade(text)
            assert 22 <= score <= 23
        else:
            pytest.skip("Flesch-Kincaid Grade is primarily for English")

    # Test Bezirci-Yılmaz (Turkish)
    def test_bezirci_yilmaz(self, st, language):
        if language.family() == Language.Turkish:
            # Simple text
            text = "Çocuk parkta oynuyor."
            score = st.bezirci_yilmaz(text)
            assert 1 <= score <= 2

            # Complex text
            text = "Kuantum mekaniğindeki olasılıksal davranışlar, mikroskobik seviyedeki belirsizlikleri açıklıyor."
            score = st.bezirci_yilmaz(text)
            assert 22 <= score <= 23
        else:
            pytest.skip("Bezirci-Yılmaz is only for Turkish texts")

    # Test with emojis
    def test_readability_with_emojis(self, st, language):
        if language.family() == Language.English:
            text = "I love 🐈 and 🐕! They are amazing pets."
            regular_score = st.flesch_reading_ease(text, demojize=False)
            demojized_score = st.flesch_reading_ease(text, demojize=True)
            assert regular_score != demojized_score
        elif language.family() == Language.Turkish:
            text = "Ben 🐈 ve 🐕 severim! Harika dostlardır."
            regular_score = st.atesman(text, demojize=False)
            demojized_score = st.atesman(text, demojize=True)
            assert regular_score != demojized_score

    # Test generic compute_readability
    def test_compute_readability(self, st, language):
        if language.family() == Language.English:
            text = "This is a simple test sentence."
            formula = ReadabilityFormula.Flesch_Reading_Ease
            score = st.compute_readability(text, formula)
            assert score > 0

            # Test invalid formula for language
            formula = ReadabilityFormula.Atesman
            score = st.compute_readability(text, formula)
            assert score == 0
        elif language.family() == Language.German:
            text = "Dies ist ein einfacher Testsatz."
            formula = ReadabilityFormula.Flesch_Reading_Ease
            score = st.compute_readability(text, formula)
            assert score > 0

            # Test invalid formula for language
            formula = ReadabilityFormula.Atesman
            score = st.compute_readability(text, formula)
            assert score == 0
        elif language.family() == Language.Turkish:
            text = "Bu basit bir test cümlesidir."
            formula = ReadabilityFormula.Atesman
            score = st.compute_readability(text, formula)
            assert score > 0

            # Test invalid formula for language
            formula = ReadabilityFormula.Flesch_Kincaid_Grade
            score = st.compute_readability(text, formula)
            assert score == 0

    # Add German Flesch test
    def test_german_flesch_reading_ease(self, st, language):
        if language.family() == Language.German:
            # Simple text
            text = "Der Hund läuft schnell."
            score = st.flesch_reading_ease(text)
            assert 117 <= score <= 118

            # Complex text
            text = "Die quantenmechanischen Phänomene zeigen ein intrinsisch probabilistisches Verhalten."
            score = st.flesch_reading_ease(text)
            assert -26 <= score <= -25
        else:
            pytest.skip("German Flesch is only for German texts")

    def test_wiener_sachtextformel(self, st, language):
        if language.family() == Language.German:
            text = "Ein mittelkomplexer deutscher Beispieltext zur Analyse."

            score1 = st.wiener_sachtextformel_1(text)
            score2 = st.wiener_sachtextformel_2(text)
            score3 = st.wiener_sachtextformel_3(text)
            score4 = st.wiener_sachtextformel_4(text)

            scores = {score1, score2, score3, score4}
            assert len(scores) == 4

            for score in scores:
                assert 13 <= score <= 18
        else:
            pytest.skip("Wiener Sachtextformel is only for German texts")
