#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

"""
Backend module for SmoothText text processing library.

This module provides functionality to manage and validate different NLP backends
that can be used with SmoothText. It supports multiple NLP frameworks through
a unified interface, allowing users to switch between different implementations
based on their needs.

Examples:
    >>> from smoothtext.backend import Backend
    >>> Backend.is_supported('nltk')
    True
    >>> supported_backends = Backend.list_supported()
"""

from __future__ import annotations
from enum import Enum
import importlib


class Backend(Enum):
    """
    Enum representing NLP backends supported by SmoothText.

    This enum defines the available NLP processing backends and provides utility
    methods for backend validation and management. Each backend represents a
    different NLP framework that can be used for text processing tasks.

    Available backends:
        - NLTK: Natural Language Toolkit, suitable for basic NLP tasks
        - Stanza: Stanford NLP's Stanza, offering state-of-the-art accuracy

    Examples:
        >>> backend = Backend.parse('nltk')
        >>> if backend and Backend.is_supported(backend):
        ...     print(f"{backend.value} is available")
    """

    # # # # # # # #
    # Attributes  #
    # # # # # # # #
    NLTK = "NLTK"
    Stanza = "Stanza"

    # # # # # # # # # #
    # Static Methods  #
    # # # # # # # # # #
    @staticmethod
    def values() -> list[Backend]:
        """
        Returns a list of all available backend options.

        This method provides access to all defined backends, regardless of
        whether they are currently installed and supported in the environment.

        Returns:
            list[Backend]: A list containing all defined Backend enum values.

        Examples:
            >>> backends = Backend.values()
            >>> print([b.value for b in backends])
            ['NLTK', 'Stanza']
        """

        return [Backend.NLTK, Backend.Stanza]

    @staticmethod
    def parse(backend: Backend | str) -> Backend | None:
        """
        Converts a backend identifier to its corresponding Backend enum value.

        Args:
            backend (Union[Backend, str]): The backend identifier to parse.
                Can be either a Backend enum value or a string matching a
                backend name (case-insensitive).

        Returns:
            Optional[Backend]: The corresponding Backend enum value if valid,
            None if the input cannot be mapped to a valid backend.

        Examples:
            >>> Backend.parse('nltk')
            <Backend.NLTK>
            >>> Backend.parse('invalid')
            None
        """
        if isinstance(backend, Backend):
            return backend

        if not isinstance(backend, str):
            return None

        backend = backend.lower()
        return next(
            (
                candidate
                for candidate in Backend.values()
                if backend == candidate.value.lower()
            ),
            None,
        )

    @staticmethod
    def is_supported(backend: Backend | str) -> bool:
        """
        Verifies if a backend is installed and available for use.

        This method checks both if the backend is valid and if its required
        dependencies are installed in the current environment.

        Args:
            backend (Union[Backend, str]): The backend to check, either as
                a Backend enum value or a string identifier.

        Returns:
            bool: True if the backend is valid and its dependencies are
            installed, False otherwise.

        Examples:
            >>> Backend.is_supported('nltk')
            True  # If NLTK is installed
            >>> Backend.is_supported('invalid')
            False
        """
        try:
            backend = Backend.parse(backend)
            if backend is None:
                return False

            module_name = backend.value.lower()
            importlib.import_module(module_name)
            return True
        except (ImportError, ModuleNotFoundError):
            return False

    @staticmethod
    def list_supported() -> list[Backend]:
        """
        Retrieves all backends that are currently available for use.

        This method checks all defined backends and returns only those that
        have their dependencies properly installed in the current environment.

        Returns:
            list[Backend]: A list of Backend enum values representing the
            backends that are ready to use.

        Examples:
            >>> supported = Backend.list_supported()
            >>> print([b.value for b in supported])
            ['NLTK']  # If only NLTK is installed
        """
        return [
            backend for backend in Backend.values() if Backend.is_supported(backend)
        ]
