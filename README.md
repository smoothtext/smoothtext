# SmoothText

---

[![Tests](https://github.com/smoothtext/smoothtext/actions/workflows/main.yml/badge.svg)](https://github.com/smoothtext/smoothtext/actions)
[![license](https://img.shields.io/github/license/smoothtext/smoothtext.svg)](https://github.com/smoothtext/smoothtext/blob/main/LICENSE)
[![versions](https://img.shields.io/pypi/pyversions/smoothtext.svg)](https://github.com/smoothtext/smoothtext)
[![pypi](https://img.shields.io/pypi/v/smoothtext.svg)](https://pypi.org/project/smoothtext/)
[![downloads](https://static.pepy.tech/personalized-badge/smoothtext?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/smoothtext/)

---

## Introduction

SmoothText is a Python library for calculating readability scores of texts and statistical information for texts in
multiple languages.

The design principle of this library is to ensure high accuracy.

## Requirements

Python 3.10 or higher.

### External Dependencies

|                     Library                      |  Version   |           License            | Notes                                         |
|:------------------------------------------------:|:----------:|:----------------------------:|-----------------------------------------------|
|          [NLTK](https://www.nltk.org/)           | `>=3.9.1`  |         `Apache 2.0`         | Conditionally optional.                       |
| [Stanza](https://stanfordnlp.github.io/stanza/)  | `>=1.10.1` |         `Apache 2.0`         | Conditionally optional.                       |
|   [CMUdict](https://pypi.org/project/cmudict/)   | `>=1.0.32` |           `GPLv3+`           | Required if `Stanza` is the selected backend. |
| [Unidecode](https://pypi.org/project/Unidecode/) | `>=1.3.8`  |         `GNU GPLv2`          | Required.                                     |
|    [Pyphen](https://pypi.org/project/pyphen/)    | `>=0.17.0` | `GPL 2.0+/LGPL 2.1+/MPL 1.1` | Required.                                     |
|     [emoji](https://pypi.org/project/emoji/)     | `>=2.14.1` |            `BSD`             | Required.                                     |

Either NLTK or Stanza must be installed and used with the SmoothText library.

## Features

### Readability Analysis

SmoothText can calculate readability scores of text in the following languages, using the following formulas.

#### English

|                                                                                                                                                           Formula                                                                                                                                                           |                                                                                                                                                     Authors                                                                                                                                                      | Notes                                                                                                              |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------|
|                                                                                          [Automated Readability Index](https://scholar.google.com/scholar?&q=Senter+R.+J.%2C+Smith+E.+A.+%281967%29+Automated+Readability+Index.)                                                                                           |                                                                                         [Smith & Senter, 1967](https://scholar.google.com/scholar?&q=Senter+R.+J.%2C+Smith+E.+A.+%281967%29+Automated+Readability+Index)                                                                                         | -                                                                                                                  |
|                                                                                                        [Flesch Reading Ease](https://scholar.google.com/scholar?q=Flesch%2C+R.+(1948).+A+new+readability+yardstick.)                                                                                                        |                                                                                                      [Flesch, 1948](https://scholar.google.com/scholar?q=Flesch%2C+R.+(1948).+A+new+readability+yardstick.)                                                                                                      | -                                                                                                                  |
|      [Flesch-Kincaid Grade](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.)       | [Kincaid et al., 1975](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.) | -                                                                                                                  |
| [Flesch-Kincaid Grade Simplified](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.) | [Kincaid et al., 1975](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.) | Essentially, the same as `Flesch-Kincaid Grade`. However, the output will be rounded due to the constant rounding. |

**Notes:**

- Formulas work best with **US English**. However, SmoothText supports both **US English** and **GB English**.

#### German

|                                                                                                                    Formula                                                                                                                    |                                                                                                                      Authors                                                                                                                      | Notes                                                                                  |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------|
|                                                     [Flesch Reading Ease](https://scholar.google.com/scholar?q=Amstad%2C+T.+%281978%29.+Wie+verst%C3%A4ndlich+sind+unsere+Zeitungen%3F.)                                                      |                                                           [Amstad, 1978](https://scholar.google.com/scholar?q=Amstad%2C+T.+%281978%29.+Wie+verst%C3%A4ndlich+sind+unsere+Zeitungen%3F.)                                                           | German adaptation of `Flesch Reading Ease`.                                            |
| [Wiener Sachtextformel](https://scholar.google.com/scholar?q=Bamberger%2C+R.%2C+%26+Vanecek%2C+E.+%281984%29.+Lesen%E2%80%93Verstehen%E2%80%93Lernen%E2%80%93Schreiben+%5BReading%E2%80%93Understanding%E2%80%93Learning%E2%80%93Writing%5D.) | [Bamberger & Vanecek, 1984](https://scholar.google.com/scholar?q=Bamberger%2C+R.%2C+%26+Vanecek%2C+E.+%281984%29.+Lesen%E2%80%93Verstehen%E2%80%93Lernen%E2%80%93Schreiben+%5BReading%E2%80%93Understanding%E2%80%93Learning%E2%80%93Writing%5D.) | German adaptation of `Flesch-Kincaid Grade`. All versions (1 through 4) are supported. |

#### Turkish

|                                                                                                                                                 Formula                                                                                                                                                 |                                                                                                                                                     Authors                                                                                                                                                     | Notes                                         |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------|
|                                                                            [Ateşman](https://scholar.google.com/scholar?q=Ate%C5%9Fman%2C+E.+%281997%29.+T%C3%BCrk%C3%A7ede+okunabilirli%C4%9Fin+%C3%B6l%C3%A7%C3%BClmesi.)                                                                             |                                                                             [Ateşman, 1997](https://scholar.google.com/scholar?q=Ate%C5%9Fman%2C+E.+%281997%29.+T%C3%BCrk%C3%A7ede+okunabilirli%C4%9Fin+%C3%B6l%C3%A7%C3%BClmesi.)                                                                              | Turkish adaptation of `Flesch Reading Ease`.  |
| [Bezirci-Yılmaz](https://scholar.google.com/scholar?q=Bezirci%2C+B.%2C+%26+Y%C4%B1lmaz%2C+A.+E.+%282010%29.+Metinlerin+okunabilirli%C4%9Finin+%C3%B6l%C3%A7%C3%BClmesi+%C3%BCzerine+bir+yazilim+k%C3%BCt%C3%BCphanesi+ve+T%C3%BCrk%C3%A7e+i%C3%A7in+yeni+bir+okunabilirlik+%C3%B6l%C3%A7%C3%BCt%C3%BC.) | [Bezirci & Yılmaz, 2010](https://scholar.google.com/scholar?q=Bezirci%2C+B.%2C+%26+Y%C4%B1lmaz%2C+A.+E.+%282010%29.+Metinlerin+okunabilirli%C4%9Finin+%C3%B6l%C3%A7%C3%BClmesi+%C3%BCzerine+bir+yazilim+k%C3%BCt%C3%BCphanesi+ve+T%C3%BCrk%C3%A7e+i%C3%A7in+yeni+bir+okunabilirlik+%C3%B6l%C3%A7%C3%BCt%C3%BC.) | Turkish adaptation of `Flesch-Kincaid Grade`. |

### Sentencizing, Tokenizing, and Syllabifying

SmoothText can extract sentences, words, or syllables from texts.

### Reading Time

SmoothText can calculate how long would a text take to read.

### Counting Frequency of Words

SmoothText can count the frequency of (lemmatized) words.

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

The following will create a new SmoothText instance configured to be used with the English language (by default, the
United States variant) using NLTK as the backend.

```Python
st = SmoothText('en', 'nltk')
```

Once an instance is created, its backend cannot be changed, but its working language can be changed at any time.

```Python
st.language = 'tr'  # Now configured to work with Turkish.
st.language = 'en-gb'  # Switching back to English, but to the United Kingdom variant.
```

#### Readying the Backends

When an instance is created, the instance will first attempt to import and download the required backend/language data.
To avoid this, and to prepare the required packages in advance, we can use the static `SmoothText.prepare()` method.

```Python
SmoothText.prepare('nltk', 'en,tr')  # Preparing NLTK to be used with English and Turkish
```

### Computing Readability Scores

Each language has its own set of readability formulas. When computing the readability score of a text in a language, one
of the supporting formulas must be used. Using SmoothText, there are three ways to perform this calculation.

```Python
text: str = 'Forrest Gump is a 1994 American comedy-drama film directed by Robert Zemeckis.'  # https://en.wikipedia.org/wiki/Forrest_Gump

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

## Inconsistencies

### Backend Related Inconsistencies

- NLTK and Stanza have different tokenization rules. This may cause differences in the number of tokens/sentences
  between the two backends.

### Language Related Inconsistencies

- The syllabification of words may differ within the same language variant. For example, the word "hello" has two
  syllables in American English but one in British English.

## Documentation

See [here](https://smoothtext.github.io/) for API documentation.

## License

SmoothText has an MIT license. See [LICENSE](./LICENSE).
