#  SmoothText - https://smoothtext.tugrulgungor.me/
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .backend import Backend
from .formula import ReadabilityFormula
from .language import Language
from .smoothtext import SmoothText

__version__ = SmoothText.version

for module in (Backend, ReadabilityFormula, Language, SmoothText):
    for attr in dir(module):
        if callable(getattr(module, attr)):
            if not attr.startswith("_"):
                globals()[attr] = getattr(module, attr)
