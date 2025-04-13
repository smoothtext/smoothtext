#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from abc import abstractmethod
import re

from ..backend import Backend
from ..language import Language

import pyphen
from unidecode import unidecode


def _asciify(text: str) -> str:
    return unidecode(string=text, errors="replace", replace_str="?")


def _is_consonant(c: str) -> bool:
    return c in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTUVWXY"


def _is_vowel(c: str) -> bool:
    return c in "aeiouAEIOU"


def _is_consonant_ru(c: str) -> bool:
    return c in "бвгджзклмнпрстфхцчшщ"


def _is_vowel_ru(c: str) -> bool:
    return c in "аеёиоуыэюя"


class SyllabifierBase:
    @abstractmethod
    def syllabify(self, token: str) -> list[str]:
        pass

    @abstractmethod
    def count(self, token: str) -> int:
        pass


class SyllabifierPyphenBase(SyllabifierBase):
    def __init__(self, language: str):
        self.__pyphen = pyphen.Pyphen(lang=language)

    def syllabify(self, token: str) -> list[str]:
        return self.__pyphen.inserted(token).split("-")

    def count(self, token: str) -> int:
        # If the token is empty, return 0.
        if not token:
            return 0

        has_alnum: bool = False
        for c in token:
            if c.isalnum():
                has_alnum = True
                break

        if not has_alnum:
            return 0

        return len(self.syllabify(token))


class SyllabifierEng(SyllabifierBase):
    def __init__(self, backend: Backend, language: Language):
        super().__init__()

        if Backend.NLTK == backend:
            from nltk.corpus import cmudict

            self.__cmudict = cmudict.dict()
        else:
            import cmudict

            self.__cmudict = cmudict.dict()

        if Language.English_GB == language:
            self.__pyphen = pyphen.Pyphen(lang="en_GB")
        elif Language.English_US == language:
            self.__pyphen = pyphen.Pyphen(lang="en_US")
        else:
            self.__pyphen = pyphen.Pyphen(lang="en")

    def syllabify(self, token: str) -> list[str]:
        # Get the syllables of the token using Pyphen.
        p_syllables = self.__pyphen.inserted(token)
        p_syllables = p_syllables.split("-") if p_syllables else [token]

        # If the token is not in the CMU dictionary, return the Pyphen result.
        token_l = token.lower()
        if token_l not in self.__cmudict:
            return p_syllables

        # Get the syllables of the token using the CMU dictionary.
        phonemes = self.__cmudict[token_l][0]
        syllables = []
        current = []

        for phoneme in phonemes:
            phoneme_clean = re.sub(r"\d+", "", phoneme)
            current.append(phoneme_clean)

            if re.search(r"[AEIOUYaeiouy]", phoneme_clean):
                syllables.append("".join(current))
                current = []

        if current:
            syllables.append("".join(current))

        if "".join(syllables).lower() != token_l:
            return p_syllables

        if not syllables or len(syllables) > len(p_syllables):
            return p_syllables

        return syllables

    def count(self, token: str) -> int:
        # If the token is empty, return 0.
        if not token:
            return 0

        has_alnum: bool = False
        for c in token:
            if c.isalnum():
                has_alnum = True
                break

        if not has_alnum:
            return 0

        # If the token contains a hyphen, count the syllables of each part.
        if "-" in token:
            return sum([self.count(t) for t in token.split("-")])

        # First, try to syllabify the token using the CMU dictionary.
        token_l = token.lower()
        if token_l in self.__cmudict:
            syllables = self.__cmudict[token_l][0]
            return sum(1 for phoneme in syllables if phoneme[-1].isdigit())

        # If the token is not in the CMU dictionary, use Pyphen.
        return len(self.__pyphen.positions(token)) + 1


class SyllabifierGer(SyllabifierPyphenBase):
    def __init__(self):
        super().__init__(language="de_DE")


class SyllabifierRus(SyllabifierPyphenBase):
    def __init__(self):
        super().__init__(language="ru_RU")


class SyllabifierTur(SyllabifierBase):
    def syllabify(self, token: str) -> list[str]:
        syllables: list[str] = []

        if not token:
            return syllables

        token_: str = _asciify("".join(c if c.isalnum() else " " for c in token))
        if len(token_) != len(token):
            raise UnicodeError(f"Invalid syllable token: {token}.")

        previous: int = len(token_)
        index: int = len(token_) - 1
        while index >= 0:
            c = token_[index]

            if " " == c:
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

    def count(self, token: str) -> int:
        # If the token is empty, return 0.
        if not token:
            return 0

        # Convert the token to ASCII.
        token = _asciify(text=token)

        # If the token contains a hyphen, count the syllables of each part.
        if "-" in token:
            return sum([self.count(t) for t in token.split("-")])

        # Basic vowel-counting should be enough for Turkish.
        num_vowels: int = 0
        for c in token:
            if _is_vowel(c):
                num_vowels += 1

        # If no vowels are found, return 1 if the token contains an alphanumeric character.
        if 0 == num_vowels:
            for c in token:
                if c.isalnum():
                    return 1

        return num_vowels


def _create_syllabifier(backend: Backend,
                        language: Language) -> SyllabifierEng | SyllabifierGer | SyllabifierRus | SyllabifierTur | None:
    language = language.family()

    if Language.English == language:
        return SyllabifierEng(backend=backend, language=language)

    if Language.German == language:
        return SyllabifierGer()

    if Language.Russian == language:
        return SyllabifierRus()

    if Language.Turkish == language:
        return SyllabifierTur()

    return None
