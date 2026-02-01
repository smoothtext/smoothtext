#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from typing import Final

from ...language_variant import LanguageVariant

# Mapping of LanguageVariant enum to (country code, lowercase name)
LanguageVariantConstants: Final[dict[LanguageVariant, tuple[str, str]]] = {
    LanguageVariant.English_GB: ("en", LanguageVariant.English_GB.value.lower()),
    LanguageVariant.English_US: ("en", LanguageVariant.English_US.value.lower()),
    LanguageVariant.German_DE: ("de", LanguageVariant.German_DE.value.lower()),
    LanguageVariant.Russian_RU: ("ru", LanguageVariant.Russian_RU.value.lower()),
    LanguageVariant.Turkish_TR: ("tr", LanguageVariant.Turkish_TR.value.lower()),
}
