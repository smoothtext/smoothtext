# SmoothText

---

[![PyPI](https://img.shields.io/pypi/v/smoothtext.svg)](https://pypi.org/project/smoothtext/)

## Introduction

`SmoothText` is a Python library for calculating readability scores of texts and statistical information for texts in
multiple languages.

The design principle of this library is to ensure high accuracy.

## Requirements

### External Dependencies

|                     Library                      |  Version  |   License    | Notes                                                                  |
|:------------------------------------------------:|:---------:|:------------:|------------------------------------------------------------------------|
| [Unidecode](https://pypi.org/project/Unidecode/) | `>=1.3.8` | `GNU GPLv2`  | Required.                                                              |
|          [NLTK](https://www.nltk.org/)           | `>=3.9.1` | `Apache 2.0` | Optional, but temporarily Required until other backends are supported. |

## Features

### Readability Analysis

SmoothText can calculate readability scores of text in the following languages, using the following formulas.

| Formula/Language                                                                                                                                                                                                                             | English |                                                                                                                                Turkish                                                                                                                                |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [Flesch Reading Ease](https://scholar.google.com/scholar?as_sdt=0%2C5&q=A+New+Readability+Yardstick+R+Flesch&btnG=)                                                                                                                          |    ✔    |                                                          ✔ [Ateşman](https://scholar.google.com/scholar?as_sdt=0%2C5&q=T%C3%BCrk%C3%A7ede+Okunabilirli%C4%9Fin+%C3%96l%C3%A7%C3%BClmesi+Ate%C5%9Fman&btnG=)                                                           |
| [Flesch-Kincaid Grade](https://scholar.google.com/scholar?as_sdt=0%2C5&q=Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel&btnG=)            |    ✔    | ✔ [Bezirci-Yılmaz](https://scholar.google.com/scholar?as_sdt=0%2C5&q=Metinlerin+okunabilirli%C4%9Finin+%C3%B6l%C3%A7%C3%BClmesi+%C3%BCzerine+bir+yazilim+k%C3%BCt%C3%BCphanesi+ve+T%C3%BCrk%C3%A7e+i%C3%A7in+yeni+bir+okunabilirlik+%C3%B6l%C3%A7%C3%BCt%C3%BC&btnG=) |
| [Flesch-Kincaid Grade Simplified](https://scholar.google.com/scholar?as_sdt=0%2C5&q=Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel&btnG=) |    ✔    |                                                                                                                                   ❌                                                                                                                                   |

Notes:

- **Ateşman** is the Turkish adaptation of **Flesch Reading Ease**. The two can be used interchangeably in the module.
- **Bezirci-Yılmaz** is the Turkish adaptation of **Flesch-Kincaid Grade**. The two can be used interchangeably in the
  module.
- **Flesch-Kincaid Grade Simplified** is essentially the same formula with as **Flesch-Kincaid Grade**, except that its
  constants are different.

### Sentencizing, Tokenizing, and Syllabifying

SmoothText can extract sentences, words, or syllables from texts.

### Reading Time

SmoothText can calculate how long would a text take to read.

## Installation

You can install `SmoothText` via `pip`.

```python
pip install smoothtext
```

## Usage

### Importing and Initializing the Library

`SmoothText` comes with three submodules: `Language`, `ReadabilityFormula` and `SmoothText`.

```Python
from smoothtext import Language, ReadabilityFormula, SmoothText
```

Before using, the library must be initialized with a static function. The following will set
[NLTK](https://www.nltk.org/) as the backend, and automatically download all the resources for the supported languages.

```Python
SmoothText.setup(backend='nltk')
```

### Instancing

`SmoothText` is expected to be used with `SmoothText` class instances.

```Python
st = SmoothText('en')
```

Now, an instance is accessible via `st`, and it is ready to work with English texts.

### Calculating Readability Scores

See the following [text](https://en.wikipedia.org/wiki/Forrest_Gump). Now, we will analyze it.

```Python
text = "Forrest Gump is a 1994 American comedy-drama film directed by Robert Zemeckis."
```

For English, we have two available formulas: `Flesch Reading Ease` and `Flesch-Kincaid Grade`. We can either call the
`compute_readability` function, or use the instance as a callable. Either way, we are expected to pass the formula.

```python
score_1 = st.compute_readability(text, ReadabilityFormula.Flesch_Reading_Ease)
score_2 = st(text, ReadabilityFormula.Flesch_Kincaid_Grade)

print(score_1, score_2)
# Output is: 25.455000000000013 12.690000000000001
```

## Documentation

See [here](https://smoothtext.tugrulgungor.me/) for API documentation.

## Roadmap

`SmoothText` is still in its early stages. The immediate tasks include adding more languages and backends.
