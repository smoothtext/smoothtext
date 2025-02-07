# SmoothText

---

[![Tests](https://github.com/smoothtext/smoothtext/actions/workflows/main.yml/badge.svg)](https://github.com/smoothtext/smoothtext/actions)
[![license](https://img.shields.io/github/license/smoothtext/smoothtext.svg)](https://github.com/smoothtext/smoothtext/blob/main/LICENSE)
[![versions](https://img.shields.io/pypi/pyversions/smoothtext.svg)](https://github.com/smoothtext/smoothtext)
[![pypi](https://img.shields.io/pypi/v/smoothtext.svg)](https://pypi.org/project/smoothtext/)
[![downloads](https://static.pepy.tech/personalized-badge/smoothtext?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/smoothtext/)

---

## Introduction

SmoothText is a Python library for calculating readability scores of texts and statistical information for texts in multiple languages.

The design principle of this library is to ensure high accuracy.

## Requirements

Python 3.10 or higher.

### External Dependencies

|                     Library                      |  Version   |           License            | Notes                   |
|:------------------------------------------------:|:----------:|:----------------------------:|-------------------------|
|          [NLTK](https://www.nltk.org/)           | `>=3.9.1`  |         `Apache 2.0`         | Conditionally optional. |
| [Stanza](https://stanfordnlp.github.io/stanza/)  | `>=1.10.1` |         `Apache 2.0`         | Conditionally optional. |
| [CMUdict](https://pypi.org/project/cmudict/)  | `>=1.0.32` |         `GPLv3+`         | Required if `Stanza` is the selected backend. |
| [Unidecode](https://pypi.org/project/Unidecode/) | `>=1.3.8`  |         `GNU GPLv2`          | Required.               |
|    [Pyphen](https://github.com/Kozea/Pyphen)     | `>=0.17.0` | `GPL 2.0+/LGPL 2.1+/MPL 1.1` | Required.               |

Either NLTK or Stanza must be installed and used with the SmoothText library.

## Features

### Readability Analysis

SmoothText can calculate readability scores of text in the following languages, using the following formulas.

| Formula/Language                                                                                                                                                                                                                             | English |                                                                                                                                Turkish                                                                                                                                |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [Flesch Reading Ease](https://scholar.google.com/scholar?as_sdt=0%2C5&q=A+New+Readability+Yardstick+R+Flesch&btnG=)                                                                                                                          |    ✔    |                                                          ✔ [Ateşman](https://scholar.google.com/scholar?as_sdt=0%2C5&q=T%C3%BCrk%C3%A7ede+Okunabilirli%C4%9Fin+%C3%96l%C3%A7%C3%BClmesi+Ate%C5%9Fman&btnG=)                                                           |
| [Flesch-Kincaid Grade](https://scholar.google.com/scholar?as_sdt=0%2C5&q=Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel&btnG=)            |    ✔    | ✔ [Bezirci-Yılmaz](https://scholar.google.com/scholar?as_sdt=0%2C5&q=Metinlerin+okunabilirli%C4%9Finin+%C3%B6l%C3%A7%C3%BClmesi+%C3%BCzerine+bir+yazilim+k%C3%BCt%C3%BCphanesi+ve+T%C3%BCrk%C3%A7e+i%C3%A7in+yeni+bir+okunabilirlik+%C3%B6l%C3%A7%C3%BCt%C3%BC&btnG=) |
| [Flesch-Kincaid Grade Simplified](https://scholar.google.com/scholar?as_sdt=0%2C5&q=Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel&btnG=) |    ✔    |                                                                                                                                   ❌                                                                                                                                   |

Notes:

- **Ateşman** is the Turkish adaptation of **Flesch Reading Ease**.
- **Bezirci-Yılmaz** is the Turkish adaptation of **Flesch-Kincaid Grade**.

### Sentencizing, Tokenizing, and Syllabifying

SmoothText can extract sentences, words, or syllables from texts.

### Reading Time

SmoothText can calculate how long would a text take to read.

## Installation

You can install SmoothText via `pip`.

```Python
pip install smoothtext
```

## Usage

### Importing and Initializing the Library

SmoothText comes with four submodules: `Backend`, `Language`, `ReadabilityFormula` and `SmoothText`.

```Python
from smoothtext import Backend, Language, ReadabilityFormula, SmoothText
```

#### Instancing

SmoothText was not designed to be used with static methods. Thus, an instance must be created to access its methods.

When creating an instance, the language and the backend to be used with it can be specified.

The following will create a new SmoothText instance configured to be used with the English language (by default, the United Kingdom variant) using NLTK as the backend.

```Python
st = SmoothText('en', 'nltk')
```

Once an instance is created, its backend cannot be changed, but its working language can be changed at any time.

```Python
st.language = 'tr' # Now configured to work with Turkish.
st.language = 'en-us' # Switching back to English, but to the United States variant.
```

#### Readying the Backends

When an instance is created, the instance will first attempt to import and download the required backend/language data. To avoid this, and to prepare the required packages in advance, we can use the static `SmoothText.prepare()` method.

```Python
SmoothText.prepare('nltk', 'en,tr') # Preparing NLTK to be used with English and Turkish
```

### Computing Readability Scores

Each language has its own set of readability formulas. When computing the readability score of a text in a language, one of the supporting formulas must be used. Using SmoothText, there are three ways to perform this calculation.

```Python
text: str = 'Forrest Gump is a 1994 American comedy-drama film directed by Robert Zemeckis.' # https://en.wikipedia.org/wiki/Forrest_Gump

# Generic computation method
st.compute_readability(text, ReadabilityFormula.Flesch_Reading_Ease)

# Using instance as a callable for generic computation
st(text, ReadabilityFormula.Flesch_Reading_Ease)

# Specific formula method
st.flesch_reading_ease(text)
```

### Tokenizing and Calculating Text Statistics

SmoothText is designed to work with sentences, words/tokens, and syllables.

```Python
text = 'This is a test sentence. This is another test sentence. This is a third test sentence.'

st.count_sentences(text)
# Output: 3

st.count_words(text)
# Output: 14

st.count_syllables(text)
# Output: 21
```

### Other Features

Refer to the documentation for a complete list of available methods.

## Documentation

See [here](https://smoothtext.github.io/) for API documentation.

## License

SmoothText has an MIT license. See [LICENSE](./LICENSE).
