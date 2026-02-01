#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/


from __future__ import annotations
from enum import Enum
import importlib
import logging
import threading

from .locale import Locale, LocaleLike
from .language import Language

_BackendLock = threading.Lock()


class Backend(Enum):
    """
    Enum representing the supported NLP backends.

    Attributes:
        NLTK (str): The NLTK backend.
        SpaCy (str): The SpaCy backend.
        Stanza (str): The Stanza backend.
    """

    NLTK = "nltk"
    SpaCy = "spacy"
    Stanza = "stanza"

    def is_ready(self, locale: LocaleLike) -> bool:
        """
        Check if the backend is ready for use with the specified locale.

        Args:
            locale (LocaleLike): The locale to check readiness for.

        Returns:
            bool: True if the backend is ready, False otherwise.

        Example:
            ```python
            >>> Backend.NLTK.is_ready("en-US")
            True
            ```
        """
        from .internal.backend.installer import _backend_status

        global _BackendLock

        locale_: Locale | None = Locale(locale)
        if locale_ is None:
            logging.error(f"[SmoothText.Backend] Invalid locale provided: {locale}")
            return False
        else:
            with _BackendLock:
                return _backend_status(self, locale_)

    @property
    def is_installed(self) -> bool:
        """
        Check if the backend library is installed and importable.

        Returns:
            bool: True if the backend is installed, False otherwise.

        Example:
            ```python
            >>> Backend.NLTK.is_installed
            True
            ```
        """
        global _BackendLock

        with _BackendLock:
            try:
                importlib.import_module(self.value)
                return True
            except ImportError:
                return False

    @staticmethod
    def list(installed: bool | None = None) -> list[Backend]:
        """
        List available backends.

        Args:
            installed (bool | None): If True, return only installed backends.
                                     If False, return only uninstalled backends.
                                     If None, return all backends.

        Returns:
            list[Backend]: A list of Backend enums matching the criteria.

        Example:
            ```python
            >>> Backend.list(installed=True)
            [<Backend.NLTK: 'nltk'>, <Backend.SpaCy: 'spacy'>]
            ```
        """
        return [
            backend
            for backend in Backend
            if installed is None or backend.is_installed == installed
        ]

    @staticmethod
    def parse(backend: BackendLike) -> Backend | None:
        """
        Parse a backend-like object into a Backend enum.

        Args:
            backend (BackendLike): The backend to parse (string or Backend enum).

        Returns:
            Backend | None: The Backend enum if successful, None otherwise.

        Example:
            ```python
            >>> Backend.parse("spacy")
            <Backend.SpaCy: 'spacy'>
            ```
        """
        if isinstance(backend, Backend):
            return backend

        if isinstance(backend, str):
            backend = backend.lower()
            for b in Backend:
                if b.value == backend:
                    return b

        return None

    @staticmethod
    def prepare(backend: BackendLike, locale: LocaleLike, **kwargs: object) -> bool:
        """
        Prepare the backend for a specific locale by downloading/installing necessary resources.

        Args:
            backend (BackendLike): The backend to prepare.
            locale (LocaleLike): The locale for which resources are needed.
            **kwargs: Additional arguments passed to the backend installer.

        Returns:
            bool: True if preparation was successful, False otherwise.

        Example:
            ```python
            >>> Backend.prepare(Backend.NLTK, Language.English)
            True
            ```
        """
        global _BackendLock

        backend: Backend | None = Backend.parse(backend)
        if backend is None:
            logging.error(f"[SmoothText.Backend] Invalid backend provided: {backend}")
            return False

        locale: Locale | None = Locale.parse(locale)
        if locale is None:
            logging.error(f"[SmoothText.Backend] Invalid locale provided: {locale}")
            return False

        if not backend.is_installed:
            logging.error(
                f"[SmoothText.Backend] Backend '{backend.value}' is not installed."
            )
            return False

        with _BackendLock:
            from .internal.backend.installer import _backend_install

            return _backend_install(backend, locale, **kwargs)

    @staticmethod
    def auto(locale: LocaleLike | None = None) -> Backend | None:
        """
        Automatically select the best available backend based on the environment and locale.

        Args:
            locale (LocaleLike | None): The locale to consider for backend selection.

        Returns:
            Backend | None: The selected Backend, or None if no suitable backend is found.

        Example:
            ```python
            >>> Backend.auto(Language.English)
            <Backend.NLTK: 'nltk'>
            ```
        """
        if locale is not None:
            locale: Locale | None = Locale.parse(locale)
            if locale is None:
                logging.error(f"[SmoothText.Backend] Invalid locale provided: {locale}")

        language: Language | None = None if locale is None else locale.language

        available: list[Backend] = Backend.list(installed=True)
        if not available:
            logging.error("[SmoothText.Backend] No backend is installed.")
            return None

        if Backend.Stanza in available:
            import torch

            if torch.cuda.is_available():
                return Backend.Stanza

        if Backend.SpaCy in available:
            import spacy

            if spacy.prefer_gpu() and language != Language.Turkish:
                return Backend.SpaCy

        if Backend.NLTK in available:
            if language == Language.English or len(available) == 1:
                return Backend.NLTK

        return available[0]


BackendLike = Backend | str
""" The type of a backend-like object. """
