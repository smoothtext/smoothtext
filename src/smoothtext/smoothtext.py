#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

import logging

from .backend import Backend, BackendLike
from .language import Language
from .locale import Locale, LocaleLike
from .readability_formula import ReadabilityFormula
from .text_statistics import TextStatistics
from .internal.backend.installer import _backend_status
from .internal.readability.r import _R_
from .internal.tokenizer.base import TokenizerBase
from .internal.tokenizer.utils import get_tokenizer
from .internal.syllabifier.base import SyllabifierBase
from .internal.syllabifier.utils import get_syllabifier


class SmoothText:
    """
    Main class for SmoothText. It provides methods for tokenization, syllabification, readability, and text statistics.

    Args:
        backend (BackendLike): The backend to use.
        locale (LocaleLike): The locale to use.
    """

    def _prepare(self) -> None:
        if not _backend_status(self._backend, self._locale):
            Backend.prepare(self._backend, self._locale)

        self._tokenizer: TokenizerBase = get_tokenizer(self._backend, self._locale)
        self._syllabifier: SyllabifierBase = get_syllabifier(self._locale)

    def __init__(self, backend: BackendLike, locale: LocaleLike) -> None:
        """
        Initialize the SmoothText instance.

        Args:
            backend (BackendLike): The backend to use.
            locale (LocaleLike): The locale to use.

        Raises:
            ValueError: If the provided backend or locale is invalid.
        """
        backend_: Backend | None = Backend.parse(backend)
        if backend_ is None:
            raise ValueError(f"[SmoothText] Invalid backend provided: {backend}")

        locale_: Locale | None = Locale.parse(locale)
        if locale_ is None:
            raise ValueError(f"[SmoothText] Invalid locale provided: {locale}")

        self._backend = backend_
        self._locale = locale_
        self._prepare()

    def __call__(self, text: str, formula: ReadabilityFormula) -> float:
        """
        Compute the readability of the text using the provided formula.

        Args:
            text (str): The text to compute the readability of.
            formula (ReadabilityFormula): The formula to use.

        Returns:
            float: The readability of the text.
        """
        return self.compute_readability(text, formula)

    @property
    def backend(self) -> Backend:
        """
        Get the current backend.

        Returns:
            Backend: The current backend.
        """
        return self._backend

    @backend.setter
    def backend(self, backend: BackendLike) -> None:
        """
        Set the backend.

        Args:
            backend (BackendLike): The backend to set.

        Raises:
            ValueError: If the provided backend is invalid.
        """
        backend_: Backend | None = Backend.parse(backend)
        if backend_ is None:
            raise ValueError(f"Invalid backend provided: {backend}")

        self._backend = backend_
        self._prepare()

    @property
    def locale(self) -> Locale:
        """
        Get the current locale.

        Returns:
            Locale: The current locale.
        """
        return self._locale

    @locale.setter
    def locale(self, locale: LocaleLike) -> None:
        """
        Set the locale.

        Args:
            locale (LocaleLike): The locale to set.

        Raises:
            ValueError: If the provided locale is invalid.
        """
        locale_: Locale | None = Locale.parse(locale)
        if locale_ is None:
            raise ValueError(f"Invalid locale provided: {locale}")

        self._locale = locale_
        self._prepare()

    def sentencize(self, text: str) -> list[str]:
        """
        Sentencize the text.

        Args:
            text (str): The text to sentencize.

        Returns:
            list[str]: The sentencized text.
        """
        if not text:
            return []

        return self._tokenizer.sentencize(text)

    def tokenize(
        self,
        text: str,
        sentencize: bool = False,
        words: bool = False,
        remove_punct: bool = False,
        include_tags: bool = False,
    ) -> (
        list[str]
        | list[tuple[str, str]]
        | list[list[str]]
        | list[list[tuple[str, str]]]
    ):
        """
        Tokenize the text.

        Args:
            text (str): The text to tokenize.
            sentencize (bool): Whether to sentencize the text.
            words (bool): Whether to split tokens into words.
            remove_punct (bool): Whether to remove punctuation-only tokens.
            include_tags (bool): Whether to include tags in the tokens.

        Returns:
            list[str] | list[tuple[str, str]] | list[list[str]] | list[list[tuple[str, str]]]: The tokenized text.
        """
        if not text:
            return []

        if (
            include_tags
            and self.backend == Backend.NLTK
            and self.locale.language not in (Language.English, Language.Russian)
        ):
            include_tags = False
            logging.warning(
                "[SmoothText] include_tags cannot be True if backend is NLTK and language is not English or Russian. include_tags will be set to False."
            )

        if not words and include_tags:
            words = True
            logging.warning(
                "[SmoothText] words cannot be False if include_tags is True. words will be set to True."
            )

        return self._tokenizer.tokenize(
            text, sentencize, words, remove_punct, include_tags
        )

    def syllabify(self, word_or_text: str) -> list[str] | list[list[str]]:
        """
        Syllabifies a word or text.

        Args:
            word_or_text (str): The word or text to syllabify.

        Returns:
            list[str] | list[list[str]]: The syllabified word or text. If the input is a word, returns a list of syllables. If the input is a text, returns a list of lists of syllables.
        """
        tokens: list[str] = self.tokenize(
            text=word_or_text, sentencize=False, words=False
        )

        if not tokens:
            return []

        syllables: list[list[str]] = []
        for token in tokens:
            syllables.append(self._syllabifier.syllabify(token))

        return syllables[0] if len(syllables) == 1 else syllables

    def amstad(self, text: str) -> float:
        """
        Compute the readability of the text using the Amstad formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Amstad)

    def atesman(self, text: str) -> float:
        """
        Compute the readability of the text using the Ateşman formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Atesman)

    def automated_readability_index(self, text: str) -> float:
        """
        Compute the readability of the text using the Automated Readability Index formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(
            text, ReadabilityFormula.Automated_Readability_Index
        )

    def bezirci_yilmaz(self, text: str) -> float:
        """
        Compute the readability of the text using the Bezirci-Yılmaz formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Bezirci_Yilmaz)

    def cetinkaya_uzun(self, text: str) -> float:
        """
        Compute the readability of the text using the Çetinkaya-Uzun formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Cetinkaya_Uzun)

    def coleman_liau_index(self, text: str) -> float:
        """
        Compute the readability of the text using the Coleman-Liau Index formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Coleman_Liau_Index)

    def dale_chall(self, text: str) -> float:
        """
        Compute the readability of the text using the Dale-Chall formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Dale_Chall)

    def flesch_kincaid_grade(self, text: str) -> float:
        """
        Compute the readability of the text using the Flesch-Kincaid Grade formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Flesch_Kincaid_Grade)

    def flesch_kincaid_grade_simplified(self, text: str) -> float:
        """
        Compute the readability of the text using the simplified Flesch-Kincaid Grade formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(
            text, ReadabilityFormula.Flesch_Kincaid_Grade_Simplified
        )

    def flesch_reading_ease(self, text: str) -> float:
        """
        Compute the readability of the text using the Flesch Reading Ease formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Flesch_Reading_Ease)

    def gunning_fog_index(self, text: str) -> float:
        """
        Compute the readability of the text using the Gunning Fog Index formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Gunning_Fog_Index)

    def matskovskiy(self, text: str) -> float:
        """
        Compute the readability of the text using the Matskovskiy formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Matskovskiy)

    def smog_index(self, text: str) -> float:
        """
        Compute the readability of the text using the SMOG Index formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Smog_Index)

    def wiener_sachtextformel(self, text: str) -> float:
        """
        Compute the readability of the text using the Wiener Sachtextformel formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(text, ReadabilityFormula.Wiener_Sachtextformel)

    def wiener_sachtextformel_1(self, text: str) -> float:
        """
        Compute the readability of the text using the Wiener Sachtextformel (version 1) formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(
            text, ReadabilityFormula.Wiener_Sachtextformel_1
        )

    def wiener_sachtextformel_2(self, text: str) -> float:
        """
        Compute the readability of the text using the Wiener Sachtextformel (version 2) formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(
            text, ReadabilityFormula.Wiener_Sachtextformel_2
        )

    def wiener_sachtextformel_3(self, text: str) -> float:
        """
        Compute the readability of the text using the Wiener Sachtextformel (version 3) formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(
            text, ReadabilityFormula.Wiener_Sachtextformel_3
        )

    def wiener_sachtextformel_4(self, text: str) -> float:
        """
        Compute the readability of the text using the Wiener Sachtextformel (version 4) formula.

        Args:
            text (str): The text to compute the readability of.

        Returns:
            float: The readability score of the text.
        """
        return self.compute_readability(
            text, ReadabilityFormula.Wiener_Sachtextformel_4
        )

    def compute_readability(self, text: str, formula: ReadabilityFormula) -> float:
        """
        Compute the readability of the text using the given formula.

        Args:
            text (str): The text to compute the readability of.
            formula (ReadabilityFormula): The formula to use.

        Returns:
            float: The readability score of the text.
        """
        if not text:
            return 0.0

        if not formula.supports(self._locale):
            logging.warning(
                f"Formula {formula} is not intended for {self._locale} locale. "
                f"The result may not be accurate."
            )

        return _R_(formula, text, self._tokenizer, self._syllabifier)

    def compute_readability_all(
        self, text: str, language_specific: bool = True
    ) -> dict[ReadabilityFormula, float]:
        """
        Compute the readability of the text using all formulas.

        Args:
            text (str): The text to compute the readability of.
            language_specific (bool): Whether to use language-specific formulas. If False, all formulas are used.

        Returns:
            dict[ReadabilityFormula, float]: The readability of the text for each formula.
        """
        formulas: list[ReadabilityFormula] = []

        for formula in ReadabilityFormula:
            if formula.supports(self._locale) or not language_specific:
                formulas.append(formula)

        return {
            formula: self.compute_readability(text, formula) for formula in formulas
        }

    def compute_text_statistics(
        self, text: str, words: bool = False, remove_punct: bool = True
    ) -> TextStatistics:
        """
        Compute the text statistics.

        Args:
            text (str): The text to compute the statistics of.
            words (bool): Whether to split tokens into words.
            remove_punct (bool): Whether to remove punctuation.

        Returns:
            TextStatistics: The text statistics.
        """
        sentences: list[list[str]] = self.tokenize(
            text, sentencize=True, words=words, remove_punct=remove_punct
        )

        statistics: TextStatistics = TextStatistics()
        statistics.num_sentences = len(sentences)

        statistics.syllable_frequencies = {}
        statistics.word_frequencies = {}

        for sentence in sentences:
            statistics.num_words += len(sentence)

            for word in sentence:
                word_syllable_count: int = self._syllabifier.count(word=word)
                statistics.num_syllables += word_syllable_count

                statistics.syllable_frequencies[word_syllable_count] = (
                    statistics.syllable_frequencies.get(word_syllable_count, 0) + 1
                )

                statistics.word_frequencies[word] = (
                    statistics.word_frequencies.get(word, 0) + 1
                )

        statistics.syllable_frequencies = dict(
            sorted(statistics.syllable_frequencies.items(), key=lambda x: x[0])
        )

        return statistics
