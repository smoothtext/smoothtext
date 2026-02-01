#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from typing import Final

from ...language import Language

# Mapping of Language enum to (ISO 639-1, ISO 639-2, lowercase name)
LanguageConstants: Final[dict[Language, tuple[str, str, str]]] = {
    Language.English: ("en", "eng", Language.English.value.lower()),
    Language.German: ("de", "deu", Language.German.value.lower()),
    Language.Russian: ("ru", "rus", Language.Russian.value.lower()),
    Language.Turkish: ("tr", "tur", Language.Turkish.value.lower()),
}
