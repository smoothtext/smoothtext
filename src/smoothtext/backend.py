#  SmoothText - https://smoothtext.tugrulgungor.me/
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from __future__ import annotations
from enum import Enum
import importlib


class Backend(Enum):
    """
    Backends supported by SmoothText.

    Attributes:
        NLTK: NLTK
        Stanza: Stanza
    """

    NLTK = 'NLTK'
    Stanza = 'Stanza'

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def values() -> list[Backend]:
        """
        Returns a list of available backends.
        :return: A list of available backends.
        """

        return [Backend.NLTK, Backend.Stanza]

    @staticmethod
    def parse(backend: Backend | str) -> Backend:
        """
        Parses a backend string into a Backend enum.
        :param backend: The backend string to parse.
        :return: The parsed backend.
        :exception ValueError: If the backend string is invalid.
        """

        if isinstance(backend, Backend):
            return backend

        backend = backend.lower()

        for candidate in Backend.values():
            if backend == candidate.value.lower():
                return candidate

        raise ValueError('Invalid backend.')

    @staticmethod
    def is_supported(backend: Backend | str) -> bool:
        """
        Checks if a backend is supported by SmoothText and is ready for use.
        :param backend: The backend to check.
        :return: `True` if the backend is supported, `False` otherwise.
        """

        try:
            backend = Backend.parse(backend)

            if Backend.NLTK == backend:
                importlib.import_module('nltk')
            elif Backend.Stanza == backend:
                importlib.import_module('stanza')

            return True
        except:
            return False

    @staticmethod
    def find_supported() -> list[Backend]:
        """
        Returns a list of supported backends.
        :return: A list of supported backends.

        """

        supported: list[Backend] = []

        for backend in Backend.values():
            if Backend.is_supported(backend):
                supported.append(backend)

        return supported
