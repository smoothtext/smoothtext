#  SmoothText - https://github.com/smoothtext/smoothtext
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .backend import Backend
from .language import Language
from .language_variant import LanguageVariant
from .locale import Locale
from .readability_formula import ReadabilityFormula
from .resource_manager import ResourceManager
from .smoothtext import SmoothText

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "Backend",
    "Language",
    "LanguageVariant",
    "Locale",
    "ReadabilityFormula",
    "ResourceManager",
    "SmoothText",
]
