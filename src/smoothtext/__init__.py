#  SmoothText - https://github.com/smoothtext
#
#  Copyright (c) 2025. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .backend import Backend
from .language import Language
from .readability import ReadabilityFormula
from .smoothtext import SmoothText

from importlib.metadata import version

__version__ = tuple(map(int, version("smoothtext").split(".")))

for module in (Backend, Language, ReadabilityFormula, SmoothText):
    for attr in dir(module):
        if callable(getattr(module, attr)):
            if not attr.startswith("_"):
                globals()[attr] = getattr(module, attr)
