#  SmoothText - https://smoothtext.tugrulgungor.me/
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/
import pyphen

from . import Backend
from . import Language
from . import ReadabilityFormula

import importlib
import math
import os
from pyphen import Pyphen
from types import ModuleType
from unidecode import unidecode


def _is_consonant(c: str) -> bool:
    return c in 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTUVWXY'


def _is_vowel(c: str) -> bool:
    return c in 'aeiouAEIOU'


def _asciify(text: str) -> str:
    return unidecode(string=text, errors='replace', replace_str='?')


_Constants: dict[Language, tuple[float, float, float, float, float]] = {
    Language.English: (206.835, 1.015, 84.6, 238.0, 183.0),
    Language.Turkish: (198.825, 2.61, 40.175, 238.0, 183.0),
}


class SmoothText:
    """
    Smooth Text class.
    """

    # Public static fields.
    version: tuple[int, int, int] = (0, 0, 16)

    # Private static fields.
    _languages: list[Language] = []
    _backend: ModuleType | None = None
    _backend_type: Backend | None = None

    # Setup
    @staticmethod
    def setup(backend: None | Backend | str = None,
              languages: Language | list[Language] | str | list[str] | None = None, skip_downloads: bool = False,
              **kwargs) -> None:
        """
        Global setup function for the SmoothText class.
        :param backend: Backend to use. Must be one of the following: `NLTK`, 'Stanza'. If `None`, the value is imported from the
        environment variable `SMOOTHTEXT_BACKEND`.
        :param languages: Language or languages to enable. This can be a single language code/name or a list of language
        codes/names (e.g., `['English', 'Turkish']`). Only the resources for the specified languages will be imported.
        If `None` or empty, all the supported languages are imported.
        :param skip_downloads: If `True`, backend data is not downloaded. Default is False.
        :param kwargs: Additional keyword arguments to pass to the backend's data downloader function.
        :return: `None`. This function does not return anything but might raise exceptions.
        """

        # Languages
        if languages is None:
            languages = Language.values()
        elif isinstance(languages, str):
            languages = languages.split(',')
        elif isinstance(languages, Language):
            languages = [languages]

        for i in range(len(languages)):
            languages[i] = Language.parse(languages[i])

        SmoothText._languages = languages

        # Backend
        if backend is None:
            backend = os.environ.get('SMOOTHTEXT_BACKEND')

        backend = Backend.parse(backend)

        if not Backend.is_supported(backend):
            raise RuntimeError(f"Backend {backend} is not supported.")

        if Backend.NLTK == backend:
            try:
                nltk = importlib.import_module('nltk')

                if not skip_downloads:
                    if not nltk.download('punkt_tab', **kwargs):
                        raise ImportError('Could not download NLTK data.')

                globals()['nltk'] = nltk
                SmoothText._backend = nltk
            except ModuleNotFoundError:
                raise ModuleNotFoundError('NLTK is not installed.')

        if Backend.Stanza == backend:
            try:
                stanza = importlib.import_module('stanza')

                if not skip_downloads:
                    for l in languages:
                        print('stanza.download', l)
                        stanza.download(lang=l.alpha2(), **kwargs)

                SmoothText._stanza = stanza
            except ModuleNotFoundError:
                raise ModuleNotFoundError('Stanza is not installed.')

        SmoothText._backend_type = backend

    # Constructor
    def __init__(self, language: Language | str | None = None):
        """
        Default constructor for the SmoothText class.
        :param language: Default language to use.
        """

        if SmoothText._backend_type is None or 0 == len(SmoothText._languages):
            raise Exception('Call SmoothText.setup() first.')

        if language is None:
            language = SmoothText._languages[0]
        else:
            language = Language.parse(language)

        self._set_language(language)

    # Instance language.
    @property
    def language(self) -> Language:
        """
        Getter for the current language.
        :return: Current language.
        """

        return self._language

    @language.setter
    def language(self, language: Language | str) -> None:
        """
        Setter for the current language.
        :param language: New language.
        """

        self._set_language(Language.parse(language))

    def _set_callbacks(self) -> None:
        if SmoothText._backend_type == Backend.NLTK:
            self._sentencize = self._sentencize_nltk
            self._tokenize = self._tokenize_nltk
        elif SmoothText._backend_type == Backend.Stanza:
            self._backend = self._stanza.Pipeline(lang=self._language.alpha2(), processors='tokenize',
                                                  verbose=False,
                                                  download_method=self._stanza.DownloadMethod.REUSE_RESOURCES)

            self._sentencize = self._sentencize_stanza
            self._tokenize = self._tokenize_stanza

        if Language.English == self.language:
            self._syllable_tokenizer = self._syllabify_eng
            self._syllable_helper = pyphen.Pyphen(lang='en')
        elif Language.Turkish == self.language:
            self._syllable_tokenizer = self._syllabify_tur
            self._syllable_helper = None

    def _set_language(self, language: Language) -> None:
        if language not in SmoothText._languages:
            raise ValueError(f'Invalid language: {language}. Make sure the language was included in the setup.')

        self._language = language
        self._language_value = self._language.value.lower()

        self._constants = _Constants[self._language]

        return self._set_callbacks()

    # Sentence-based operations.
    def _sentencize_nltk(self, text: str) -> list[str]:
        return SmoothText._backend.sent_tokenize(text, self._language_value)

    def _sentencize_stanza(self, text: str) -> list[str]:
        sentences: list[str] = []

        doc = self._backend(text)
        for sentence in doc.sentences:
            sentences.append(sentence.text)

        return sentences

    def sentencize(self, text: str) -> list[str]:
        """
        Breaks down the `text` into sentences.
        :param text: Text to break down into sentences.
        :return: List of sentences.
        """

        return self._sentencize(text)

    def count_sentences(self, text: str) -> int:
        """
        Counts the number of sentences in the `text`.
        :param text: Text to be counted.
        :return: Number of sentences.
        """

        return len(self.sentencize(text))

    # Token/word-based operations.
    def _extract_words(self, text: str) -> list[str]:
        tokens: list[str] = self.tokenize(text)

        words: list[str] = []
        for token in tokens:
            for c in token:
                if c.isalnum():
                    words.append(token)
                    break

        return words

    def _tokenize_nltk(self, text: str) -> list[str]:
        return self._backend.word_tokenize(text, self._language_value)

    def _tokenize_stanza(self, text: str) -> list[str]:
        tokens: list[str] = []

        doc = self._backend(text)
        for sentence in doc.sentences:
            for token in sentence.tokens:
                tokens.append(token.text)

        return tokens

    def tokenize(self, text: str) -> list[str]:
        """
        Breaks down the `text` into tokens.
        :param text: Text to break down into tokens.
        :return: The list of tokens.
        """

        return self._tokenize(text)

    def count_words(self, text: str) -> int:
        """
        Counts the number of words in the `text`.
        :param text: Text to count words from.
        :return: Number of words.
        """

        tokens: list[str] = self.tokenize(text)

        count: int = 0
        for token in tokens:
            for c in token:
                if c.isalnum():
                    count += 1
                    break

        return count

    # Syllable-based operations.
    def _syllabify_eng(self, token: str) -> list[str]:
        return self._syllable_helper.inserted(word=_asciify(token), hyphen='\0').split('\0')

    @staticmethod
    def _syllabify_tur(token: str) -> list[str]:
        syllables: list[str] = []

        if 0 == len(token):
            return syllables

        token_: str = _asciify(''.join(c if c.isalnum() else ' ' for c in token))
        if len(token_) != len(token):
            raise UnicodeError(f'Invalid syllable token: {token}.')

        previous: int = len(token_)
        index: int = len(token_) - 1
        while index >= 0:
            c = token_[index]

            if ' ' == c:
                syllables.append(token[index])
                index -= 1
                previous -= 1
                continue

            if _is_vowel(c):
                if 0 == index:
                    syllables.append(token[0:previous])
                    previous = 0
                    break

                c2 = token_[index - 1]
                if _is_consonant(c2):
                    index -= 1

                syllables.append(token[index:previous])
                previous = index

            index -= 1

        if 0 != previous:
            syllables.append(token[0:previous])

        syllables.reverse()
        return syllables

    def syllabify(self, token: str, filter_words: bool = True) -> list[str] | list[list[str]]:
        """
        Breaks down the `token` into syllables.
        :param token: Token to syllabify.
        :param filter_words: If `True`, only return syllables that are part of alphanumeric words.
        :return: List of syllables.
        :remark: If token is in fact a list of tokens (phrase, sentence, etc.), each is syllabified separately.
        """

        syllables: list[list[str]] = []

        tokens: list[str] = self.tokenize(token)
        for token in tokens:
            token_syllables: list[str] = self._syllable_tokenizer(token)

            if filter_words:
                token_syllables = [s for s in token_syllables if s.isalnum()]

            if 0 == len(token_syllables):
                continue

            syllables.append(token_syllables)

        if 1 == len(syllables):
            return syllables[0]

        return syllables

    def count_syllables(self, text: str, filter_words: bool = True) -> int:
        """
        Counts the number of syllables in the `text`.
        :param text: Text to be counted.
        :param filter_words: If `True`, only count syllables that are part of alphanumeric words.
        :return: Number of syllables.
        """

        num_syllables: int = 0

        sentences: list[str] = self.sentencize(text)
        for sentence in sentences:
            tokens = self.tokenize(sentence)
            for token in tokens:
                num_syllables += len(self.syllabify(token, filter_words))

        return num_syllables

    # Letter-based operations.
    @staticmethod
    def count_vowels(text: str) -> int:
        """
        Counts the number of vowels in the `text`.
        :param text: Text to be counted.
        :return: Number of vowels.
        """

        count: int = 0

        text = _asciify(text)
        for c in text:
            if _is_vowel(c):
                count += 1

        return count

    @staticmethod
    def count_consonants(text: str) -> int:
        """
        Counts the number of consonants in the `text`.
        :param text: Text to be counted.
        :return: Number of consonants.
        """

        count: int = 0

        text = _asciify(text)
        for c in text:
            if _is_consonant(c):
                count += 1

        return count

    # Readability
    def _avg_syllables_and_words(self, sentences: list[str]) -> tuple[float, float, int]:
        total_words: int = 0
        total_syllables: int = 0
        num_sentences: int = 0

        for sentence in sentences:
            num_words = self.count_words(sentence)
            num_syllables = self.count_syllables(sentence, filter_words=True)

            if 0 != num_words and 0 != num_syllables:
                total_words += num_words
                total_syllables += num_syllables
                num_sentences += 1

        if 0 == num_sentences:
            return 0.0, 0.0, 0

        avg_word_syllables: float = float(total_syllables) / float(total_words)
        avg_sentence_length: float = float(total_words) / float(num_sentences)
        return avg_word_syllables, avg_sentence_length, num_sentences

    def _syllable_frequencies(self, sentences: list[str]) -> dict[int, int]:
        frequencies: dict[int, int] = {
            3: 0,
            4: 0,
            5: 0,
            6: 0
        }

        for sentence in sentences:
            syllables = self.syllabify(sentence, filter_words=True)
            if 0 == len(syllables):
                continue

            if isinstance(syllables[0], str):
                num_syllables: int = min(len(syllables), 6)
                if 3 <= num_syllables:
                    frequencies[num_syllables] += 1
            else:
                for group in syllables:
                    num_syllables: int = min(len(group), 6)
                    if 3 <= num_syllables:
                        frequencies[num_syllables] += 1

        return frequencies

    def _bezirci_yilmaz(self, sentences: list[str]) -> float:
        avg_word_syllables, avg_sentence_length, num_sentences = self._avg_syllables_and_words(sentences)
        syllable_frequencies = self._syllable_frequencies(sentences)

        score: float = 0.0
        score += (float(syllable_frequencies[3]) / float(num_sentences)) * 0.84
        score += (float(syllable_frequencies[4]) / float(num_sentences)) * 1.5
        score += (float(syllable_frequencies[5]) / float(num_sentences)) * 3.5
        score += (float(syllable_frequencies[6]) / float(num_sentences)) * 26.25

        return math.sqrt(avg_sentence_length * score)

    def _flesch_reading_ease(self, sentences: list[str]) -> float:
        avg_word_syllables, avg_sentence_length, _ = self._avg_syllables_and_words(sentences)
        return self._constants[0] - (self._constants[1] * avg_sentence_length) - (
                self._constants[2] * avg_word_syllables)

    def _flesch_kincaid_grade(self, sentences: list[str]) -> float:
        avg_word_syllables, avg_sentence_length, _ = self._avg_syllables_and_words(sentences)
        return (0.39 * avg_sentence_length) + (11.8 * avg_word_syllables) - 15.59

    def _flesch_kincaid_grade_simplified(self, sentences: list[str]) -> float:
        avg_word_syllables, avg_sentence_length, _ = self._avg_syllables_and_words(sentences)
        return (0.4 * avg_sentence_length) + (12.0 * avg_word_syllables) - 16.0

    def compute_readability(self, text: str, formula: ReadabilityFormula) -> float:
        """
        Computes the readability score of the `text` using `formula`.
        :param text: Text to compute the readability score of.
        :param formula: `ReadabilityFormula` to use.
        :return: Readability score.
        """

        sentences: list[str] = self.sentencize(text)

        if ReadabilityFormula.Atesman == formula or ReadabilityFormula.Flesch_Reading_Ease == formula:
            return self._flesch_reading_ease(sentences)

        if Language.Turkish == self._language:
            if ReadabilityFormula.Bezirci_Yilmaz == formula or ReadabilityFormula.Flesch_Kincaid_Grade == formula:
                return self._bezirci_yilmaz(sentences)

        if Language.English == self._language:
            if ReadabilityFormula.Flesch_Kincaid_Grade == formula or ReadabilityFormula.Bezirci_Yilmaz == formula:
                return self._flesch_kincaid_grade(sentences)

            if ReadabilityFormula.Flesch_Kincaid_Grade_Simplified == formula:
                return self._flesch_kincaid_grade_simplified(sentences)

        raise ValueError(
            f'Invalid language and formula pair: {self._language.value} and {formula.value} does not work together.')

    def __call__(self, text: str, formula: ReadabilityFormula) -> float:
        """
        Computes the readability score of the `text` using `formula`.
        :param text: Text to compute the readability score of.
        :param formula: `ReadabilityFormula` to use.
        :return: Readability score.
        """

        return self.compute_readability(text, formula)

    # Reading time
    def _reading_time(self, text: str, wpm: float, round_up: bool) -> float | int:
        seconds: float = float(self.count_words(text)) / wpm * 60.0
        if round_up:
            return int(math.ceil(seconds))

        return seconds

    def silent_reading_time(self, text: str, words_per_minute: float = 0.0, round_up: bool = False) -> float | int:
        """
        Computes the reading time of the `text` using `words_per_minute`.
        :param text: Text to compute the reading time of.
        :param words_per_minute: Number of words per minute. If lower than `1.0`, set to `238.0`.
        :param round_up: If `True`, the reading time is rounded up and returned as `int`.
        :return: Reading time in seconds.
        """

        return self._reading_time(text, _Constants[self._language][3] if words_per_minute < 1.0 else words_per_minute,
                                  round_up)

    def reading_aloud_time(self, text: str, words_per_minute: float = 0.0, round_up: bool = False) -> float | int:
        """
        Computes the reading time of the `text` using `words_per_minute`.
        :param text: Text to compute the reading time of.
        :param words_per_minute: Number of words per minute. If lower than `1.0`, set to `183.0`.
        :param round_up: If `True`, the reading time is rounded up and returned as `int`.
        :return: Reading time in seconds.
        """

        return self._reading_time(text, _Constants[self._language][4] if words_per_minute < 1.0 else words_per_minute,
                                  round_up)
