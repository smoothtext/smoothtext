#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from abc import abstractmethod


class TokenizerBase:
    @abstractmethod
    def sentencize(self, text: str) -> list[str]:
        pass

    @abstractmethod
    def tokenize(self, text: str, split_sentences: bool) -> list[str]:
        pass


class NLTKTokenizer(TokenizerBase):
    def __init__(self, language: str) -> None:
        import nltk

        self.__punkt_tokenizer = nltk.PunktTokenizer(language)
        self.__word_tokenizer = nltk.NLTKWordTokenizer()

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


class StanzaTokenizer(TokenizerBase):
    def __init__(self, language: str) -> None:
        import stanza

        self.__nlp = stanza.Pipeline(
            lang=language,
            processors="tokenize",
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
