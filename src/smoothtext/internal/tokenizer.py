#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from abc import abstractmethod
from collections import Counter


class TokenizerBase:
    @abstractmethod
    def sentencize(self, text: str) -> list[str]:
        pass

    @abstractmethod
    def tokenize(self, text: str, split_sentences: bool) -> list[str]:
        pass

    @abstractmethod
    def word_frequencies(self, text: str, lemmatize: bool) -> dict[str, int]:
        pass


class NLTKTokenizer(TokenizerBase):
    def __init__(self, language: str) -> None:
        import nltk

        self.__punkt_tokenizer = nltk.PunktTokenizer(language)
        self.__word_tokenizer = nltk.NLTKWordTokenizer()
        self.__lemmatizer = nltk.stem.WordNetLemmatizer()

    def sentencize(self, text: str) -> list[str]:
        return self.__punkt_tokenizer.tokenize(text)

    def tokenize(self, text: str, split_sentences: bool) -> list[str]:
        return (
            self.__word_tokenizer.tokenize(text)
            if not split_sentences
            else [
                self.__word_tokenizer.tokenize(sentence)
                for sentence in self.sentencize(text)
            ]
        )

    def word_frequencies(self, text: str, lemmatize: bool) -> dict[str, int]:
        tokens: list[str] = self.tokenize(text, split_sentences=False)
        tokens = [
            token if any(char.isalpha() for char in token) else None for token in tokens
        ]
        tokens = [token.lower() for token in tokens if token is not None]

        if lemmatize:
            tokens = [self.__lemmatizer.lemmatize(token) for token in tokens]

        return Counter(tokens)


class StanzaTokenizer(TokenizerBase):
    @staticmethod
    def processors(language: str) -> str:
        p: str = "tokenize, pos, lemma"
        if "ru" != language:
            p += ", mwt"

        return p

    def __init__(self, language: str) -> None:
        import stanza

        self.__nlp = stanza.Pipeline(
            lang=language,
            processors=StanzaTokenizer.processors(language),
            package=None,
            download_method=stanza.DownloadMethod.NONE,
        )

    def sentencize(self, text: str) -> list[str]:
        doc = self.__nlp(text)
        return [sentence.text for sentence in doc.sentences]

    def tokenize(self, text: str, split_sentences: bool) -> list[str]:
        return (
            [
                token.text
                for sentence in self.__nlp(text).sentences
                for token in sentence.tokens
            ]
            if not split_sentences
            else [
                [token.text for token in sentence.tokens]
                for sentence in self.__nlp(text).sentences
            ]
        )

    def word_frequencies(self, text: str, lemmatize: bool) -> dict[str, int]:
        doc = self.__nlp(text)

        if lemmatize:
            tokens = [
                word.lemma for sentence in doc.sentences for word in sentence.words
            ]
        else:
            tokens = [
                word.text.lower()
                for sentence in doc.sentences
                for word in sentence.words
            ]

        tokens = [
            token if any(char.isalpha() for char in token) else None for token in tokens
        ]
        tokens = [token for token in tokens if token is not None]

        return Counter(tokens)
