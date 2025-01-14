#  SmoothText - https://smoothtext.tugrulgungor.me/
#
#  Copyright (c) 2025 - present. All rights reserved.
#  Tuğrul Güngör - https://tugrulgungor.me
#
#  Distributed under the MIT License.
#  https://opensource.org/license/mit/

from .formula import ReadabilityFormula
from .language import Language
from .smoothtext import SmoothText

__version__ = (0, 0, 13)

for attribute in dir(ReadabilityFormula):
    if callable(getattr(ReadabilityFormula, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(ReadabilityFormula, attribute)

for attribute in dir(Language):
    if callable(getattr(Language, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(Language, attribute)

for attribute in dir(SmoothText):
    if callable(getattr(SmoothText, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(SmoothText, attribute)
