"""
SmoothText - A Python library for natural language text analysis and readability scoring.

This module provides functionality for:
- Text tokenization (sentences and words)
- Syllable counting and syllabification
- Multiple readability formula calculations (Flesch, Ateşman, etc.)
- Reading time estimation
- Support for multiple languages and backend engines

All functionality is exposed through the SmoothText class which handles the preparation
of required resources and provides a consistent API across different backends.
"""

#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from . import Backend
from . import Language
from . import ReadabilityFormula
from .internal.syllabifier import (
    SyllabifierEng,
    SyllabifierGer,
    SyllabifierTur,
    _is_consonant,
    _is_vowel,
    _asciify,
)
from .internal.tokenizer import NLTKTokenizer, StanzaTokenizer

import emoji
from emoji.unicode_codes import load_from_json as load_emoji_codes
import math
import logging

_Prepared: dict[Backend, dict[Language, bool]] = {}


def _prepare(
    backend: Backend, language: Language, skip_downloads: bool, **backend_kwargs
) -> None:
    language = language.family()

    logging.debug(f"Preparing backend {backend} for language {language}...")

    if backend not in _Prepared:
        _Prepared[backend] = {}

    backend_languages = _Prepared[backend]
    if language in backend_languages:
        downloaded = backend_languages[language]
        if downloaded or not skip_downloads:
            logging.debug(
                f"Backend {backend} already prepared for language {language}. Skipping..."
            )
            return

        logging.debug(
            f"Backend {backend} already prepared for language {language} but download required..."
        )

    if skip_downloads:
        _Prepared[backend][language] = False
        logging.debug(
            f"Skipping downloads for backend {backend} and marking language {language} as prepared."
        )
        return

    if Backend.NLTK == backend:
        was_downloaded = False
        for language in backend_languages:
            if backend_languages[language]:
                was_downloaded = True
                break

        if was_downloaded:
            logging.debug(f"NLTK data already downloaded. Skipping...")
        else:
            import nltk

            for package in ("cmudict", "punkt", "punkt_tab"):
                if not nltk.download(package, **backend_kwargs):
                    logging.error("Failed to download NLTK data. Exiting...")
                    return

    elif Backend.Stanza == backend:
        import stanza

        stanza.download(lang=language.alpha2(), processors="tokenize", **backend_kwargs)

    _Prepared[backend][language] = True


class SmoothText:
    """
    Main class for text analysis and readability scoring.

    The SmoothText class provides methods for:
    - Text tokenization and counting (sentences, words, syllables)
    - Readability scoring using various formulas
    - Reading time estimation
    - Language-specific text processing
    - Emoji handling

    Supported backends:
    - NLTK
    - Stanza

    Supported languages:
    - English
    - German
    - Turkish

    Examples:
        >>> st = SmoothText(language="en", backend="nltk")
        >>> score = st.flesch_reading_ease("This is a test sentence.")
        >>> time = st.reading_time("Some text to analyze")
    """

    # Constants for Flesh Reading East & Ateşman.
    __constants: dict[Language, tuple[float, float, float]] = {
        Language.English: (206.835, 1.015, 84.6),
        Language.German: (180.0, 1.0, 58.5),
        Language.Turkish: (198.825, 2.61, 40.175),
    }

    # Reading speed in words per minute. Unused, kept for reference.
    __reading_speed: tuple[float, float] = (238.0, 183.0)

    # # # # #
    # Setup #
    # # # # #
    @staticmethod
    def prepare(
        backend: Backend | str | None = None,
        languages: Language | list[Language] | str | list[str] | None = None,
        skip_downloads: bool = False,
        silence_downloaders: bool = True,
        **backend_kwargs,
    ) -> None:
        """
        Prepare the required resources for text analysis.

        This method downloads and initializes the necessary language models and data
        for the specified backend and languages. It must be called before using any
        text analysis functionality.

        Args:
            backend: The backend engine to use (NLTK or Stanza)
            languages: Language(s) to prepare resources for
            skip_downloads: If True, skip downloading models even if not present
            silence_downloaders: If True, suppress download progress output
            **backend_kwargs: Additional arguments passed to backend downloaders

        Raises:
            RuntimeError: If preparation fails or no valid backends are found

        Examples:
            SmoothText.prepare(backend="nltk", languages=["en"])
        """

        # Languages.
        if languages is None:
            languages = Language.values()
        else:
            languages = Language.parse_multiple(languages)
            if 0 == len(languages):
                logging.warning("No languages to enable. Defaulting to all languages.")
                languages = Language.values()

        # Backend.
        if backend is None:
            backends = Backend.list_supported()
            if 0 == len(backends):
                logging.error("No backends to prepare. Exiting...")
                return

            backend = backends[0]
            logging.info(f"No backend specified. Defaulting to {backend}.")
        else:
            backend = Backend.parse(backend)
            if backend is None:
                logging.warning("No valid backend to prepare. Exiting...")

            if not Backend.is_supported(backend):
                logging.warning(f"Backend {backend} not supported. Exiting...")
                return

        # Feedback.
        logging.debug(f"Preparing {backend} for {languages}...")

        # Download backend data.
        if silence_downloaders:
            if Backend.NLTK == backend:
                if "quiet" not in backend_kwargs:
                    backend_kwargs["quiet"] = True
            elif Backend.Stanza == backend:
                if "verbose" not in backend_kwargs:
                    backend_kwargs["verbose"] = False

                if "logging_level" not in backend_kwargs:
                    backend_kwargs["logging_level"] = logging.FATAL

        for language in languages:
            _prepare(backend, language, skip_downloads, **backend_kwargs)

    @staticmethod
    def is_ready(backend: Backend | str, language: Language | str) -> bool:
        """
        Check if the backend is ready for the specified language.

        :param backend: Backend to check.
        :param language: Language to check.
        :return: True if the backend is ready for the language, False otherwise.
        """

        return backend in _Prepared and language in _Prepared[backend]

    # # # # # # # #
    # Properties  #
    # # # # # # # #
    # Backend
    @property
    def backend(self) -> Backend:
        """
        Get the backend of the SmoothText instance.

        :return: Backend of the SmoothText instance.
        """

        return self.__backend

    def __configure_backend(self, backend: Backend) -> None:
        if Backend.NLTK == backend:
            self.__tokenizer = NLTKTokenizer(self.__language.family().value.lower())

        if Backend.Stanza == backend:
            self.__tokenizer = StanzaTokenizer(self.__language.alpha2())

    # Language
    @property
    def language(self) -> Language:
        """
        Get the language of the SmoothText instance.

        :return: Language of the SmoothText instance.
        """

        return self.__language

    @language.setter
    def language(self, language: Language | str) -> None:
        """
        Set the language of the SmoothText instance.

        :param language: Language to set.
        :return: None
        """

        language = Language.parse(language)
        if language is None:
            logging.fatal("Invalid language.")

        # TODO: Requires improvement.
        SmoothText.prepare(
            backend=self.__backend,
            languages=language,
            skip_downloads=False,
            silence_downloaders=True,
        )

        self.__configure_language(language)

    def __configure_language(self, language: Language) -> None:
        # English
        if Language.English == language:
            language = Language.English_US

        if Language.English == language.family():
            self.__syllabifier = SyllabifierEng(self.__backend, language)

        # German
        if Language.German == language:
            language = Language.German_DE

        if Language.German == language.family():
            self.__syllabifier = SyllabifierGer()

        # Turkish
        if Language.Turkish == language:
            language = Language.Turkish_TR

        if Language.Turkish == language.family():
            self.__syllabifier = SyllabifierTur()

        # Constants
        self.__language = language
        self._constants = SmoothText.__constants[self.__language.family()]

        # Backend
        self.__configure_backend(self.__backend)

    # # # # # # #
    # Operators #
    # # # # # # #
    # Constructor.
    def __init__(
        self,
        language: Language | str | None = None,
        backend: Backend | str | None = None,
    ) -> None:
        # Find backend and language.
        backend = Backend.parse(backend)
        language = Language.parse(language)

        if backend is None and language is None:
            raise RuntimeError("Both backend and language are invalid. Exiting...")

        # TODO: Requires improvement.
        SmoothText.prepare(
            backend=backend,
            languages=language,
            skip_downloads=False,
            silence_downloaders=True,
        )

        # Initialize.
        self.__backend = backend
        self.__configure_language(language)

    # Call.
    def __call__(self, *args, **kwargs):
        return self.compute_readability(*args, **kwargs)

    # # # # # # # # #
    # Tokenization  #
    # # # # # # # # #
    # Sentence level.
    def sentencize(self, text: str) -> list[str]:
        """
        Split text into sentences using the configured backend tokenizer.

        Args:
            text: Input text to split into sentences

        Returns:
            list[str]: List of sentences found in the text

        Examples:
            >>> sentences = st.sentencize("This is a test. Another sentence.")
            >>> # Returns: ["This is a test.", "Another sentence."]
        """
        return self.__tokenizer.sentencize(text)

    def count_sentences(self, text: str) -> int:
        """
        Count the number of sentences in the input text.

        Args:
            text: Input text to analyze

        Returns:
            int: Number of sentences detected

        Examples:
            >>> count = st.count_sentences("This is one. This is two.")
            >>> # Returns: 2
        """
        return len(self.sentencize(text))

    # Word level.
    def tokenize(
        self, text: str, split_sentences: bool = False
    ) -> list[str] | list[list[str]]:
        """
        Tokenize text into words using the configured backend tokenizer.

        Args:
            text: Input text to tokenize
            split_sentences: If True, return tokens grouped by sentences

        Returns:
            list[str]: List of tokens if split_sentences=False
            list[list[str]]: List of sentences containing lists of tokens if split_sentences=True

        Examples:
            >>> tokens = st.tokenize("Hello world!")
            >>> # Returns: ["Hello", "world", "!"]
            >>>
            >>> sent_tokens = st.tokenize("Hi there. Bye now.", split_sentences=True)
            >>> # Returns: [["Hi", "there", "."], ["Bye", "now", "."]]
        """
        return self.__tokenizer.tokenize(text, split_sentences)

    @staticmethod
    def __filter_words(tokens: list[str]) -> list[str]:
        return [word for word in tokens if any(c.isalnum() for c in word)]

    @staticmethod
    def __count_words(tokens: list[str]) -> int:
        num_words: int = 0

        for token in tokens:
            for c in token:
                if c.isalnum():
                    num_words += 1
                    break

        return num_words

    def count_words(self, text: str) -> int:
        """
        Count the number of words in the text. This function counts the number of alphanumeric tokens retrieved from the
        tokenize method.

        Args:
            text: Input text to count words from

        Returns:
            int: Number of alphanumeric words found

        Examples:
            >>> count = st.count_words("Hello, world!")  # Returns: 2
        """
        tokens = self.tokenize(text, False)
        return SmoothText.__count_words(tokens)

    # Syllable level.
    def syllabify(
        self, word: str, tokenize: bool = False, sentencize: bool = False
    ) -> list[str] | list[list[str]] | list[list[list[str]]]:
        """
        Split words into syllables using language-specific rules.

        This method can operate on single words, lists of words, or lists of sentences containing words. However, for
        simple counting, it is recommended to use the count_syllables method as it is more efficient and accurate. This
        method will keep punctuation marks as separate tokens.

        Args:
            word: Input word or text to syllabify
            tokenize: If True, split input into words first
            sentencize: If True, split input into sentences first

        Returns:
            list[str]: List of syllables for a single word
            list[list[str]]: List of words with their syllables if tokenize=True
            list[list[list[str]]]: List of sentences containing words with syllables if sentencize=True

        Examples:
            >>> syllables = st.syllabify("hello")
            >>> # Returns: ["hel", "lo"]

            >>> word_syllables = st.syllabify("hello world", tokenize=True)
            >>> # Returns: [["hel", "lo"], ["world"]]
        """
        if not tokenize and not sentencize:
            return self.__syllabifier.syllabify(word)

        tokens = self.tokenize(text=word, split_sentences=sentencize)
        if not sentencize:
            res: list[list[str]] = []

            for token in tokens:
                res.append(self.__syllabifier.syllabify(token))

            return res
        else:
            res: list[list[list[str]]] = []
            for sentence in tokens:
                words: list[list[str]] = []

                for token in sentence:
                    words.append(self.__syllabifier.syllabify(token))

                res.append(words)

            return res

    def count_syllables(self, word: str, tokenize: bool = True) -> int:
        """
        Count the number of syllables in a word or text.

        Args:
            word: Input word or text to analyze
            tokenize: If True, tokenize input text and count syllables for each word

        Returns:
            int: Total number of syllables found

        Examples:
            >>> count = st.count_syllables("hello")  # Returns: 2
            >>> count = st.count_syllables("hello world", tokenize=True)  # Returns: 3
        """
        if tokenize or " " in word:
            tokens: list[str] = self.tokenize(text=word, split_sentences=False)
            return sum(
                [self.count_syllables(word=token, tokenize=False) for token in tokens]
            )

        return self.__syllabifier.count(word.lower().strip())

    def syllable_frequencies(self, text: str) -> dict[int, int]:
        frequencies: dict[int, int] = {}

        tokens: list[str] = self.tokenize(text=text, split_sentences=False)

        for token in tokens:
            token = token.lower().strip()
            syllables: int = self.__syllabifier.count(token)

            if 0 == syllables:
                continue

            if syllables not in frequencies:
                frequencies[syllables] = 0

            frequencies[syllables] += 1

        return frequencies

    # Character level.
    @staticmethod
    def count_consonants(text: str) -> int:
        """
        Count the number of consonants in the text after converting to ASCII.

        Args:
            text: Input text to analyze

        Returns:
            int: Number of consonant characters found

        Examples:
            >>> count = st.count_consonants("hello")  # Returns: 3
        """
        count: int = 0

        text = _asciify(text)
        for c in text:
            if _is_consonant(c):
                count += 1

        return count

    @staticmethod
    def count_vowels(text: str) -> int:
        """
        Count the number of vowels in the text after converting to ASCII.

        Args:
            text: Input text to analyze

        Returns:
            int: Number of vowel characters found

        Examples:
            >>> count = st.count_vowels("hello")  # Returns: 2
        """
        count: int = 0

        text = _asciify(text)
        for c in text:
            if _is_vowel(c):
                count += 1

        return count

    def demojize(self, text: str, delimiters: tuple[str, str] = ("(", ")")) -> str:
        """
        Convert emoji characters to their text descriptions.

        Args:
            text: Input text containing emojis
            delimiters: Tuple of (open, close) delimiters to wrap emoji descriptions

        Returns:
            str: Text with emojis replaced by their descriptions

        Examples:
            >>> text = st.demojize("I love 🐈")
            >>> # Returns: "I love (cat)"
        """
        _emojis: list[str] = emoji.distinct_emoji_list(text)
        if 0 == len(_emojis):
            return text

        for _emoji in _emojis:
            _str = (
                delimiters[0]
                + emoji.demojize(
                    string=_emoji,
                    delimiters=("", ""),
                    language=self.__language.alpha2(),
                ).replace("_", " ")
                + delimiters[1]
            )

            text = text.replace(_emoji, _str)

        return text

    # # # # # # # #
    # Readability #
    # # # # # # # #
    # Helpers.
    @staticmethod
    def __test_formula_langauge(
        formula: ReadabilityFormula, language: Language
    ) -> bool:
        if not formula.supports(language):
            logging.warning(
                f"Language and readability formula mismatch. {formula} cannot be used to measure the readability of texts in {language}."
            )

            return False

        return True

    def __compute_1(self, text: str) -> tuple[float, float]:
        # This method returns:
        #   - average word syllables
        #   - average sentence length

        total_words: int = 0
        total_syllables: int = 0
        num_sentences: int = 0

        # Tokenize the text into words and sentences.
        sentences: list[list[str]] = self.tokenize(text=text, split_sentences=True)

        # Perform calculations.
        for sentence in sentences:
            words: list[str] = SmoothText.__filter_words(sentence)

            if 0 == len(words):
                continue

            num_sentences += 1
            total_words += len(words)
            for word in words:
                total_syllables += self.count_syllables(word=word, tokenize=False)

        # Check if no valid sentences were found. This avoids division by zero.
        if 0 == num_sentences:
            return 0.0, 0.0

        # Return the result.
        return (float(total_syllables) / float(total_words)), (
            float(total_words) / float(num_sentences)
        )

    def __compute_2(self, text: str) -> tuple[float, float, int, dict[int, int]]:
        # This method returns:
        #   - average word syllables
        #   - average sentence length
        #   - number of sentences
        #   - syllable frequencies

        total_words: int = 0
        total_syllables: int = 0
        num_sentences: int = 0
        syllable_frequencies: dict[int, int] = {3: 0, 4: 0, 5: 0, 6: 0}

        # Tokenize the text into words and sentences.
        sentences: list[list[str]] = self.tokenize(text=text, split_sentences=True)

        # Perform calculations.
        for sentence in sentences:
            words: list[str] = SmoothText.__filter_words(sentence)

            if 0 == len(words):
                continue

            num_sentences += 1
            total_words += len(words)
            for word in words:
                word_syllable_count = self.count_syllables(word=word, tokenize=False)
                total_syllables += word_syllable_count

                if 3 <= word_syllable_count:
                    if word_syllable_count > 6:
                        word_syllable_count = 6

                    syllable_frequencies[word_syllable_count] += 1

        # Check if no valid sentences were found. This avoids division by zero.
        if 0 == num_sentences:
            return 0.0, 0.0, 0, {}

        # Return the result.
        return (
            (float(total_syllables) / float(total_words)),
            (float(total_words) / float(num_sentences)),
            num_sentences,
            syllable_frequencies,
        )

    def __compute_3(self, text: str) -> tuple[float, float, float, float]:
        # This method returns:
        #   - average sentence length
        #   - percentage of words with at least six characters
        #   - percentage of words with single syllables
        #   - percentage of words with at least three syllables

        total_words: int = 0
        num_sentences: int = 0

        num_long_words: int = 0
        num_mono_syllable_words: int = 0
        num_multi_syllable_words: int = 0

        # Tokenize the text into words and sentences.
        sentences: list[list[str]] = self.tokenize(text=text, split_sentences=True)

        # Perform calculations.
        for sentence in sentences:
            words: list[str] = SmoothText.__filter_words(sentence)

            if 0 == len(words):
                continue

            num_sentences += 1
            total_words += len(words)

            for word in words:
                word = word.lower().strip()
                if 6 <= len(word):
                    num_long_words += 1

                word_syllable_count = self.__syllabifier.count(word)
                if 1 == word_syllable_count:
                    num_mono_syllable_words += 1
                elif 3 <= word_syllable_count:
                    num_multi_syllable_words += 1

        # Check if no valid sentences were found. This avoids division by zero.
        if 0 == num_sentences:
            return 0.0, 0.0, 0.0, 0.0

        print(
            f"$$$$$$$$$$$$$$$$$ {total_words} {num_sentences} {num_long_words} {num_mono_syllable_words} {num_multi_syllable_words}"
        )

        # Return the result.
        return (
            float(total_words) / float(num_sentences),
            float(num_long_words) / float(total_words) * 100.0,
            float(num_mono_syllable_words) / float(total_words) * 100.0,
            float(num_multi_syllable_words) / float(total_words) * 100.0,
        )

    # Flesch Reading Ease & Ateşman.
    def __flesch_reading_ease(self, text: str) -> float:
        avg_word_syllables, avg_sentence_length = self.__compute_1(text)
        return (
            self._constants[0]
            - (self._constants[1] * avg_sentence_length)
            - (self._constants[2] * avg_word_syllables)
        )

    def flesch_reading_ease(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Flesch Reading Ease score for the text.
        The score typically ranges between 0-100, though scores outside this range are possible.
        Higher scores indicate easier readability.

        Score ranges:
        90-100: Very easy
        80-89: Easy
        70-79: Fairly easy
        60-69: Standard
        50-59: Fairly difficult
        30-49: Difficult
        0-29: Very difficult

        Args:
            text: Input text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Flesch Reading Ease score (higher = easier to read)

        Examples:
            >>> score = st.flesch_reading_ease("Simple text is easy to read.")
        """
        if not SmoothText.__test_formula_langauge(
            ReadabilityFormula.Flesch_Reading_Ease, self.__language
        ):
            return 0.0

        if demojize:
            text = self.demojize(text)

        return self.__flesch_reading_ease(text=text)

    def atesman(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Ateşman readability score for Turkish text.
        The score typically ranges between 0-100, though scores outside this range are possible.
        Higher scores indicate easier readability.

        Score ranges:
        90-100: Very easy
        70-89: Easy
        50-69: Medium difficulty
        30-49: Difficult
        1-29: Very difficult

        Args:
            text: Input Turkish text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Ateşman readability score (higher = easier to read)

        Examples:
            >>> score = st.atesman("Basit bir Türkçe metin.")
        """
        if not SmoothText.__test_formula_langauge(
            ReadabilityFormula.Atesman, self.__language
        ):
            return 0.0

        if demojize:
            text = self.demojize(text)

        return self.__flesch_reading_ease(text=text)

    # Flesch-Kincaid Grade +Simplified.
    def __flesch_kincaid_grade(self, text: str) -> float:
        avg_word_syllables, avg_sentence_length = self.__compute_1(text)
        return (0.39 * avg_sentence_length) + (11.8 * avg_word_syllables) - 15.9

    def flesch_kincaid_grade(self, text: str, demojize: bool = False) -> float:
        if not SmoothText.__test_formula_langauge(
            ReadabilityFormula.Flesch_Kincaid_Grade, self.__language
        ):
            return 0.0

        if demojize:
            text = self.demojize(text)

        return self.__flesch_kincaid_grade(text=text)

    def __flesch_kincaid_grade_simplified(self, text: str) -> float:
        avg_word_syllables, avg_sentence_length = self.__compute_1(text)
        return (0.4 * avg_sentence_length) + (12.0 * avg_word_syllables) - 16.0

    def flesch_kincaid_grade_simplified(
        self, text: str, demojize: bool = False
    ) -> float:
        if not SmoothText.__test_formula_langauge(
            ReadabilityFormula.Flesch_Kincaid_Grade_Simplified, self.__language
        ):
            return 0.0

        if demojize:
            text = self.demojize(text)

        return self.__flesch_kincaid_grade_simplified(text=text)

    # Wiener Sachtextformel
    def __wiener_sachtextformel(self, text: str, version: int) -> float:
        SL, IW, ES, MS = self.__compute_3(text)

        if 1 == version:
            return 0.1935 * MS + 0.1672 * SL + 0.1297 * IW - 0.0327 * ES - 0.875

        if 2 == version:
            return 0.2007 * MS + 0.1682 * SL + 0.1373 * IW - 2.779

        if 3 == version:
            return 0.2963 * MS + 0.1905 * SL - 1.1144

        if 4 == version:
            return 0.2744 * MS + 0.2656 * SL - 1.693

        return 0.0

    def wiener_sachtextformel(
        self, text: str, demojize: bool = False, version: int = 3
    ) -> float:
        """
        Calculate Wiener Sachtextformel readability score for German text.
        The score takes into account sentence length and frequency of words with different lengths.
        Higher scores indicate more difficult text.

        Score ranges:
        4-5: Very easy
        6-8: Easy
        9-11: Average
        12-14: Difficult
        15+: Very difficult

        Args:
            text: Input German text to analyze
            demojize: If True, convert emojis to text before scoring
            version: Wiener Sachtextformel version to use (1-4)

        Returns:
            float: Wiener Sachtextformel readability score (higher = more difficult)

        Examples:
            >>> score = st.wiener_sachtextformel("Deutscher Textbeispiel.")
            >>> score = st.wiener_sachtextformel("Deutscher Textbeispiel.", version=3)
        """
        if not SmoothText.__test_formula_langauge(
            ReadabilityFormula.Wiener_Sachtextformel, self.__language
        ):
            return 0.0

        if demojize:
            text = self.demojize(text)

        return self.__wiener_sachtextformel(text=text, version=version)

    def wiener_sachtextformel_1(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Wiener Sachtextformel readability score for German text.
        The score takes into account sentence length and frequency of words with different lengths.
        Higher scores indicate more difficult text.

        Args:
            text: Input German text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Wiener Sachtextformel readability score (higher = more difficult)

        Examples:
            >>> score = st.wiener_sachtextformel_1("Deutscher Textbeispiel.")
        """
        return self.wiener_sachtextformel(text=text, demojize=demojize, version=1)

    def wiener_sachtextformel_2(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Wiener Sachtextformel readability score for German text.
        The score takes into account sentence length and frequency of words with different lengths.
        Higher scores indicate more difficult text.

        Args:
            text: Input German text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Wiener Sachtextformel readability score (higher = more difficult)

        Examples:
            >>> score = st.wiener_sachtextformel_2("Deutscher Textbeispiel.")
        """
        return self.wiener_sachtextformel(text=text, demojize=demojize, version=2)

    def wiener_sachtextformel_3(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Wiener Sachtextformel readability score for German text.
        The score takes into account sentence length and frequency of words with different lengths.
        Higher scores indicate more difficult text.

        Args:
            text: Input German text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Wiener Sachtextformel readability score (higher = more difficult)

        Examples:
            >>> score = st.wiener_sachtextformel_3("Deutscher Textbeispiel.")
        """
        return self.wiener_sachtextformel(text=text, demojize=demojize, version=3)

    def wiener_sachtextformel_4(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Wiener Sachtextformel readability score for German text.
        The score takes into account sentence length and frequency of words with different lengths.
        Higher scores indicate more difficult text.

        Args:
            text: Input German text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Wiener Sachtextformel readability score (higher = more difficult)

        Examples:
            >>> score = st.wiener_sachtextformel_4("Deutscher Textbeispiel.")
        """
        return self.wiener_sachtextformel(text=text, demojize=demojize, version=4)

    # Bezirci-Yılmaz
    def __bezirci_yilmaz(self, text: str) -> float:
        _, avg_sentence_length, num_sentences, syllable_frequencies = self.__compute_2(
            text
        )

        score: float = 0.0
        score += (float(syllable_frequencies.get(3, 0)) / float(num_sentences)) * 0.84
        score += (float(syllable_frequencies.get(4, 0)) / float(num_sentences)) * 1.5
        score += (float(syllable_frequencies.get(5, 0)) / float(num_sentences)) * 3.5
        score += (float(syllable_frequencies.get(6, 0)) / float(num_sentences)) * 26.25

        return math.sqrt(avg_sentence_length * score)

    def bezirci_yilmaz(self, text: str, demojize: bool = False) -> float:
        """
        Calculate Bezirci-Yılmaz readability score for Turkish text.
        The score takes into account sentence length and frequency of words with 3+ syllables.
        Higher scores indicate more difficult readability.

        Args:
            text: Input Turkish text to analyze
            demojize: If True, convert emojis to text before scoring

        Returns:
            float: Bezirci-Yılmaz readability score (higher = more difficult)

        Examples:
            >>> score = st.bezirci_yilmaz("Türkçe metin örneği.")
        """
        if not SmoothText.__test_formula_langauge(
            ReadabilityFormula.Bezirci_Yilmaz, self.__language
        ):
            return 0.0

        if demojize:
            text = self.demojize(text)

        return self.__bezirci_yilmaz(text=text)

    # Generic.
    def compute_readability(
        self, text: str, formula: ReadabilityFormula, demojize: bool = False
    ) -> float:
        """
        Calculate readability score using the specified formula.

        Args:
            text: Input text to analyze
            formula: ReadabilityFormula to use for scoring
            demojize: If True, convert emojis to text descriptions before scoring

        Returns:
            float: Readability score (higher scores generally indicate easier readability)

        Examples:
            >>> score = st.compute_readability(text, ReadabilityFormula.Flesch_Reading_Ease)
        """
        # TODO Might reduce the number of ifs.
        if not formula.supports(self.__language):
            logging.warning(
                f"Language and readability formula mismatch. {formula} cannot be used to measure the readability of texts in {self.__language}."
            )
            return 0.0

        # Basic transformations.
        if demojize:
            text = self.demojize(text=text)

        # Redirections.
        if (
            ReadabilityFormula.Atesman == formula
            or ReadabilityFormula.Flesch_Reading_Ease == formula
        ):
            return self.__flesch_reading_ease(text=text)

        if ReadabilityFormula.Bezirci_Yilmaz == formula:
            return self.__bezirci_yilmaz(text=text)

        if ReadabilityFormula.Flesch_Kincaid_Grade == formula:
            return self.__flesch_kincaid_grade(text=text)

        if ReadabilityFormula.Flesch_Kincaid_Grade_Simplified == formula:
            return self.__flesch_kincaid_grade_simplified(text=text)

        if ReadabilityFormula.Wiener_Sachtextformel == formula:
            return self.__wiener_sachtextformel(text=text, version=3)

        if ReadabilityFormula.Wiener_Sachtextformel_1 == formula:
            return self.__wiener_sachtextformel(text=text, version=1)

        if ReadabilityFormula.Wiener_Sachtextformel_2 == formula:
            return self.__wiener_sachtextformel(text=text, version=2)

        if ReadabilityFormula.Wiener_Sachtextformel_3 == formula:
            return self.__wiener_sachtextformel(text=text, version=3)

        if ReadabilityFormula.Wiener_Sachtextformel_4 == formula:
            return self.__wiener_sachtextformel(text=text, version=4)

        return 0.0

    # # # # # # # # #
    # Reading Time  #
    # # # # # # # # #
    def __reading_time(
        self, text: str, words_per_minute: float, round_up: bool
    ) -> float:
        seconds: float = float(self.count_words(text=text)) / words_per_minute * 60.0
        return math.ceil(seconds) if round_up else seconds

    def reading_time(
        self, text: str, words_per_minute: float, round_up: bool = True
    ) -> float:
        """
        Calculate estimated reading time for the text.

        Args:
            text: Input text to analyze
            words_per_minute: Reading speed in words per minute
            round_up: If True, round result up to nearest second

        Returns:
            float: Estimated reading time in seconds

        Examples:
            >>> time = st.reading_time("Some text to read", words_per_minute=200)
        """
        if 1.0 > words_per_minute:
            words_per_minute = 1.0

        return self.__reading_time(
            text=text, words_per_minute=words_per_minute, round_up=round_up
        )

    def silent_reading_time(
        self, text: str, words_per_minute: float = 238.0, round_up: bool = True
    ) -> float:
        """
        Calculate estimated silent reading time using default reading speed.
        Default speed is 238 WPM based on research averages.

        Args:
            text: Input text to analyze
            words_per_minute: Optional custom reading speed
            round_up: If True, round result up to nearest second

        Returns:
            float: Estimated silent reading time in seconds
        """
        return self.reading_time(
            text=text, words_per_minute=words_per_minute, round_up=round_up
        )

    def reading_aloud_time(
        self, text: str, words_per_minute: float = 183.0, round_up: bool = True
    ) -> float:
        """
        Calculate estimated reading aloud time using default speaking speed.
        Default speed is 183 WPM based on research averages.

        Args:
            text: Input text to analyze
            words_per_minute: Optional custom speaking speed
            round_up: If True, round result up to nearest second

        Returns:
            float: Estimated speaking time in seconds
        """
        return self.reading_time(
            text=text, words_per_minute=words_per_minute, round_up=round_up
        )
