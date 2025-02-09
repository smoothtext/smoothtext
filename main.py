

from smoothtext import Language, ReadabilityFormula, SmoothText

st = SmoothText(backend='nltk', language=Language.English_US)

print(st.count_syllables('hello'))