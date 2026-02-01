#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from ...backend import Backend
from ...language import Language
from ...locale import Locale

import logging
from threading import Lock


_BackendInstallLock = Lock()
_BackendInstallStat: dict[
    Backend, bool | dict[Locale, str] | dict[Locale, dict[str, bool | str | None]]
] = {
    Backend.NLTK: False,
    Backend.SpaCy: {},
    Backend.Stanza: {},
}


def _backend_install_nltk(locale: Locale, **kwargs: object) -> bool:
    if Backend.NLTK not in _BackendInstallStat:
        _BackendInstallStat[Backend.NLTK] = False

    if _BackendInstallStat[Backend.NLTK]:
        return True

    import nltk

    args: dict[str, bool | str] = {
        "download_dir": "",
        "quiet": True,
        "force": False,
        "prefix": "[nltk_data] ",
    }

    for arg in kwargs:
        if arg not in args:
            logging.warning(
                f"[SmoothText.Backend] Invalid argument '{arg}' for NLTK downloader. Ignoring..."
            )
            del kwargs[arg]
        elif not isinstance(kwargs[arg], type(args[arg])):
            logging.warning(
                f"[SmoothText.Backend] Invalid type for argument '{arg}'. Expected {type(args[arg])}, got {type(kwargs[arg])}."
            )
            return False
        else:
            args[arg] = kwargs[arg]

    download_dir: str | None = None
    if args["download_dir"]:
        download_dir = args["download_dir"]

    packages: list[str] = ["punkt", "punkt_tab", "stopwords", "universal_tagset"]

    if locale.language == Language.English:
        packages.append("averaged_perceptron_tagger_eng")
    elif locale.language == Language.Russian:
        packages.append("averaged_perceptron_tagger_rus")

    for pkg in packages:
        try:
            nltk.download(
                info_or_id=pkg,
                download_dir=download_dir,
                quiet=args["quiet"],
                force=args["force"],
                prefix=args["prefix"],
                halt_on_error=True,
                raise_on_error=True,
                print_error_to=None,
            )
        except Exception as e:
            logging.error(
                f"[SmoothText.Backend] Failed to download NLTK package '{pkg}'. Error: {e}"
            )
            return False

    return True


def _backend_install_spacy(locale: Locale, **kwargs: object) -> bool:
    if Backend.SpaCy not in _BackendInstallStat:
        _BackendInstallStat[Backend.SpaCy] = {}

    if locale.language == Language.Turkish:
        logging.error(
            "[SmoothText.Backend] spaCy does not support Turkish. Please use NLTK or Stanza instead."
        )
        return False

    models: dict[Language, str] = {
        Language.English: "en_core_web_sm",
        Language.German: "de_core_news_sm",
        Language.Russian: "ru_core_news_sm",
    }

    args: dict[str, bool | str] = {
        "model": "",
        "direct": False,
        "sdist": False,
        "custom_url": "",
    }

    for arg in kwargs:
        if arg not in args:
            logging.warning(
                f"[SmoothText.Backend] Invalid argument '{arg}' for spaCy downloader. Ignoring..."
            )
            del kwargs[arg]
        elif not isinstance(kwargs[arg], type(args[arg])):
            logging.warning(
                f"[SmoothText.Backend] Invalid type for argument '{arg}'. Expected {type(args[arg])}, got {type(kwargs[arg])}."
            )
            return False
        else:
            args[arg] = kwargs[arg]

    if not args["custom_url"]:
        args["custom_url"] = None

    if locale in _BackendInstallStat[Backend.SpaCy]:
        if (
            not args["model"]
            or args["model"] == _BackendInstallStat[Backend.SpaCy][locale]
        ):
            return True

    if not args["model"]:
        args["model"] = models[locale.language]

    import spacy

    installed = spacy.util.get_installed_models()
    if args["model"] not in installed:
        try:
            spacy.cli.download(**args)
        except Exception as e:
            logging.error(
                f"[SmoothText.Backend] Failed to download spaCy model '{args['model']}'. Error: {e}"
            )
            return False

    _BackendInstallStat[Backend.SpaCy][locale] = args["model"]

    return True


def _backend_install_stanza(locale: Locale, **kwargs: object) -> bool:
    args: dict[str, str] = {
        "model_dir": "",
        "package": "",
        "resources_url": "",
        "resources_branch": "",
        "resources_version": "",
        "model_url": "",
    }

    for arg in kwargs:
        if arg not in args:
            logging.warning(
                f"[SmoothText.Backend] Invalid argument '{arg}' for stanza downloader. Ignoring..."
            )
        elif not isinstance(kwargs[arg], type(args[arg])):
            logging.warning(
                f"[SmoothText.Backend] Invalid type for argument '{arg}'. Expected {type(args[arg])}, got {type(kwargs[arg])}."
            )
            return False
        else:
            args[arg] = kwargs[arg]

    args = {k: v for k, v in args.items() if v}
    args["logging_level"] = "FATAL"
    args["verbose"] = False
    args["proxies"] = None
    args["download_json"] = True

    if locale in _BackendInstallStat[Backend.Stanza]:
        args_ = _BackendInstallStat[Backend.Stanza][locale]
        if args_ == args:
            return True

    try:
        import stanza

        stanza.download(
            lang=locale.language.alpha2,
            **args,
        )

        _BackendInstallStat[Backend.Stanza][locale] = args
    except Exception as e:
        logging.error(
            f"[SmoothText.Backend] Failed to download stanza model for locale '{locale.language}, {locale.language_variant}'. Error: {e}"
        )
        return False

    return True


def _backend_install(backend: Backend, locale: Locale, **kwargs: object) -> bool:
    with _BackendInstallLock:
        _installer = {
            Backend.NLTK: _backend_install_nltk,
            Backend.SpaCy: _backend_install_spacy,
            Backend.Stanza: _backend_install_stanza,
        }[backend]

        return _installer(locale, **kwargs)


def _backend_status(backend: Backend, locale: Locale) -> bool:
    with _BackendInstallLock:
        if backend == Backend.NLTK:
            return backend in _BackendInstallStat and _BackendInstallStat[backend]

        if backend == Backend.SpaCy:
            return (
                backend in _BackendInstallStat
                and locale in _BackendInstallStat[backend]
            )

        if backend == Backend.Stanza:
            return (
                backend in _BackendInstallStat
                and locale in _BackendInstallStat[backend]
            )

        return False


def _backend_model(backend: Backend, locale: Locale) -> dict | str | None:
    with _BackendInstallLock:
        if backend == Backend.SpaCy:
            if (
                backend not in _BackendInstallStat
                or locale not in _BackendInstallStat[backend]
            ):
                return None

            return _BackendInstallStat[backend][locale]

        if backend == Backend.Stanza:
            if (
                backend not in _BackendInstallStat
                or locale not in _BackendInstallStat[backend]
            ):
                return None

            return _BackendInstallStat[backend][locale]

        return None
