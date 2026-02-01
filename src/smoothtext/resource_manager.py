#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from functools import lru_cache
from importlib import resources
from threading import Lock

from .readability_formula import ReadabilityFormula

_ResourcesLock: Lock = Lock()
_Resources: dict[ReadabilityFormula, list[str]] = {}


class ResourceManager:
    """
    Resource manager for readability formulas.
    """

    @staticmethod
    @lru_cache(maxsize=None)
    def get_dale_chall_wordlist() -> list[str]:
        """
        Returns the Dale-Chall wordlist.
        """
        with _ResourcesLock:
            if ReadabilityFormula.Dale_Chall not in _Resources:
                with resources.path(
                    "smoothtext.internal.resources", "dale_chall_wordlist.txt"
                ) as path:
                    _Resources[ReadabilityFormula.Dale_Chall] = path.read_text(
                        encoding="utf-8"
                    ).splitlines()

            return _Resources[ReadabilityFormula.Dale_Chall]

    @staticmethod
    def set_dale_chall_wordlist(wordlist: list[str]) -> None:
        """
        Sets a custom Dale-Chall wordlist.
        """
        with _ResourcesLock:
            _Resources[ReadabilityFormula.Dale_Chall] = wordlist
