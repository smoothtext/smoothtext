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

### Python Version

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

|                                                           Method                                                           |                             Description                             |
|:--------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------:|
| [`compute_readability`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.compute_readability) | Computes the readability score of a text using a specified formula. |

#### English

|                                                                       Method                                                                       |                                                                                                                                                           Formula                                                                                                                                                           |                                                                                                                                                     Authors                                                                                                                                                      |                                                       Notes                                                        |
|:--------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------:|
|     [`automated_readability_index`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.automated_readability_index)     |                                                                                          [Automated Readability Index](https://scholar.google.com/scholar?&q=Senter+R.+J.%2C+Smith+E.+A.+%281967%29+Automated+Readability+Index.)                                                                                           |                                                                                         [Smith & Senter, 1967](https://scholar.google.com/scholar?&q=Senter+R.+J.%2C+Smith+E.+A.+%281967%29+Automated+Readability+Index)                                                                                         |                                                         -                                                          |
|             [`flesch_reading_ease`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.flesch_reading_ease)             |                                                                                                        [Flesch Reading Ease](https://scholar.google.com/scholar?q=Flesch%2C+R.+(1948).+A+new+readability+yardstick.)                                                                                                        |                                                                                                      [Flesch, 1948](https://scholar.google.com/scholar?q=Flesch%2C+R.+(1948).+A+new+readability+yardstick.)                                                                                                      |                                                         -                                                          |
|            [`flesch_kincaid_grade`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.flesch_kincaid_grade)            |      [Flesch-Kincaid Grade](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.)       | [Kincaid et al., 1975](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.) |                                                         -                                                          |
| [`flesch_kincaid_grade_simplified`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.flesch_kincaid_grade_simplified) | [Flesch-Kincaid Grade Simplified](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.) | [Kincaid et al., 1975](https://scholar.google.com/scholar?q=Kincaid%2C+J.+P.%2C+Fishburne+Jr%2C+R.+P.%2C+Rogers%2C+R.+L.%2C+%26+Chissom%2C+B.+S.+%281975%29.+Derivation+of+new+readability+formulas+%28automated+readability+index%2C+fog+count+and+flesch+reading+ease+formula%29+for+navy+enlisted+personnel.) | Essentially, the same as `Flesch-Kincaid Grade`. However, the output will be rounded due to the constant rounding. |
|              [`gunning_fog_index`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.flesch_reading_ease)              |                                                                                                     [Gunning Fog Index](https://scholar.google.com/scholar?q=Gunning%2C+R.+%281952%29.+The+technique+of+clear+writing.)                                                                                                     |                                                                                                 [Gunning, 1952](https://scholar.google.com/scholar?q=Gunning%2C+R.+%281952%29.+The+technique+of+clear+writing.)                                                                                                  |                                                         -                                                          |

**Notes:**

- Although SmoothText supports both **US English** and **GB English**, formulas work best with **US English**.

#### German

|                                                             Method                                                             |                                                                                                                    Formula                                                                                                                    |                                                                                                                      Authors                                                                                                                      | Notes                                                                                  |
|:------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------|
|                [`amstad`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.amstad)                |                                                     [Flesch Reading Ease](https://scholar.google.com/scholar?q=Amstad%2C+T.+%281978%29.+Wie+verst%C3%A4ndlich+sind+unsere+Zeitungen%3F.)                                                      |                                                           [Amstad, 1978](https://scholar.google.com/scholar?q=Amstad%2C+T.+%281978%29.+Wie+verst%C3%A4ndlich+sind+unsere+Zeitungen%3F.)                                                           | German adaptation of `Flesch Reading Ease`.                                            |
| [`wiener_sachtextformel`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.wiener_sachtextformel) | [Wiener Sachtextformel](https://scholar.google.com/scholar?q=Bamberger%2C+R.%2C+%26+Vanecek%2C+E.+%281984%29.+Lesen%E2%80%93Verstehen%E2%80%93Lernen%E2%80%93Schreiben+%5BReading%E2%80%93Understanding%E2%80%93Learning%E2%80%93Writing%5D.) | [Bamberger & Vanecek, 1984](https://scholar.google.com/scholar?q=Bamberger%2C+R.%2C+%26+Vanecek%2C+E.+%281984%29.+Lesen%E2%80%93Verstehen%E2%80%93Lernen%E2%80%93Schreiben+%5BReading%E2%80%93Understanding%E2%80%93Learning%E2%80%93Writing%5D.) | German adaptation of `Flesch-Kincaid Grade`. All versions (1 through 4) are supported. |

#### Russian

|                                                   Method                                                   |                                                                                                                                                                                                       Formula                                                                                                                                                                                                        |                                                                                                                                                                                                          Authors                                                                                                                                                                                                           | Notes                                       |
|:----------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------|
| [`matskovskiy`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.matskovskiy) | [Matskovskiy](https://scholar.google.com/scholar?q=M.+S.+Matskovskiy%2C+Problemy+chitabelnosti+pechatnogo+teksta+%5Bthe+problems+of+typed+text+readability%5D%2C+Smyslovoe+vospriyatie+rechevogo+soobshcheniya+%28v+usloviyakh+massovoy+kommunikatsii%29%5BSemantic+Perception+of+Verbal+Communication+%28in+the+Conditions+of+Mass+Communication%29%5D.+Moscow%2C+IYa+AN+SSSR+Publ+%281976%29%2C+126%E2%80%93+142.) | [Matskovskiy, 1976](https://scholar.google.com/scholar?q=M.+S.+Matskovskiy%2C+Problemy+chitabelnosti+pechatnogo+teksta+%5Bthe+problems+of+typed+text+readability%5D%2C+Smyslovoe+vospriyatie+rechevogo+soobshcheniya+%28v+usloviyakh+massovoy+kommunikatsii%29%5BSemantic+Perception+of+Verbal+Communication+%28in+the+Conditions+of+Mass+Communication%29%5D.+Moscow%2C+IYa+AN+SSSR+Publ+%281976%29%2C+126%E2%80%93+142.) | German adaptation of `Flesch Reading Ease`. |

#### Turkish

|                                                      Method                                                      |                                                                                                                                                 Formula                                                                                                                                                 |                                                                                                                                                     Authors                                                                                                                                                     | Notes                                         |
|:----------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------|
|        [`atesman`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.atesman)        |                                                                            [Ateşman](https://scholar.google.com/scholar?q=Ate%C5%9Fman%2C+E.+%281997%29.+T%C3%BCrk%C3%A7ede+okunabilirli%C4%9Fin+%C3%B6l%C3%A7%C3%BClmesi.)                                                                             |                                                                             [Ateşman, 1997](https://scholar.google.com/scholar?q=Ate%C5%9Fman%2C+E.+%281997%29.+T%C3%BCrk%C3%A7ede+okunabilirli%C4%9Fin+%C3%B6l%C3%A7%C3%BClmesi.)                                                                              | Turkish adaptation of `Flesch Reading Ease`.  |
| [`bezirci_yilmaz`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.bezirci_yilmaz) | [Bezirci-Yılmaz](https://scholar.google.com/scholar?q=Bezirci%2C+B.%2C+%26+Y%C4%B1lmaz%2C+A.+E.+%282010%29.+Metinlerin+okunabilirli%C4%9Finin+%C3%B6l%C3%A7%C3%BClmesi+%C3%BCzerine+bir+yazilim+k%C3%BCt%C3%BCphanesi+ve+T%C3%BCrk%C3%A7e+i%C3%A7in+yeni+bir+okunabilirlik+%C3%B6l%C3%A7%C3%BCt%C3%BC.) | [Bezirci & Yılmaz, 2010](https://scholar.google.com/scholar?q=Bezirci%2C+B.%2C+%26+Y%C4%B1lmaz%2C+A.+E.+%282010%29.+Metinlerin+okunabilirli%C4%9Finin+%C3%B6l%C3%A7%C3%BClmesi+%C3%BCzerine+bir+yazilim+k%C3%BCt%C3%BCphanesi+ve+T%C3%BCrk%C3%A7e+i%C3%A7in+yeni+bir+okunabilirlik+%C3%B6l%C3%A7%C3%BCt%C3%BC.) | Turkish adaptation of `Flesch-Kincaid Grade`. |

### Sentencizing, Tokenization, and Syllabification

SmoothText can extract sentences, words, or syllables from texts.

|                                                            Method                                                            |                                     Description                                      |
|:----------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|
|                                                      **Sentence Level**                                                      |                                                                                      |
|           [`sentencize`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.sentencize)           |                Splits text into sentences using language-aware rules                 |
|      [`count_sentences`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.count_sentences)      |                  Returns the number of sentences found in the text                   |
|                                                        **Word Level**                                                        |                                                                                      |
|             [`tokenize`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.tokenize)             | Extracts word tokens from text; can group by sentences with the split_sentences flag |
|          [`count_words`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.count_words)          |                  Counts the number of alphanumeric words in a text                   |
|     [`word_frequencies`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.word_frequencies)     |         Returns a dictionary of word frequencies with optional lemmatization         |
|                                                      **Syllable Level**                                                      |                                                                                      |
|            [`syllabify`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.syllabify)            |      Splits words into syllables; can be applied to words, tokens, or sentences      |
|      [`count_syllables`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.count_syllables)      |           Counts syllables in words or text using language-specific rules            |
| [`syllable_frequencies`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.syllable_frequencies) |    Returns a dictionary mapping syllable counts to frequency in the analyzed text    |
|                                                     **Character Level**                                                      |                                                                                      |
|     [`count_consonants`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.count_consonants)     |                  Counts the number of consonant characters in text                   |
|         [`count_vowels`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.count_vowels)         |                    Counts the number of vowel characters in text                     |
|                                                      **Emoji Handling**                                                      |                                                                                      |
|             [`demojize`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.demojize)             |     Converts emoji characters to their text descriptions with custom delimiters      |
|        [`remove_emojis`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.remove_emojis)        |                        Removes all emoji characters from text                        |

**Notes**
- `count_syllables` is likely to produce more accurate results in comparison to the `syllabify` method.
- At the moment, lemmatization is only supported for English with the `Stanza` as the backend. Other languages and 
backends will ignore the lemmatization flag.

| Language |      Sentencizing       |      Tokenization       |          Syllabification          |
|:--------:|:-----------------------:|:-----------------------:|:---------------------------------:|
| English  | ✔<br>(`NLTK`, `Stanza`) | ✔<br>(`NLTK`, `Stanza`) | ✔<br>(`CMU Dictionary`, `Pyphen`) |
|  German  | ✔<br>(`NLTK`, `Stanza`) | ✔<br>(`NLTK`, `Stanza`) |          ✔<br>(`Pyphen`)          |
| Russian  | ✔<br>(`NLTK`, `Stanza`) | ✔<br>(`NLTK`, `Stanza`) |          ✔<br>(`Pyphen`)          |
| Turkish  | ✔<br>(`NLTK`, `Stanza`) | ✔<br>(`NLTK`, `Stanza`) |      ✔<br>(_Custom formula_)      |

`Pyphen` may not produce accurate results sometimes. Thus, whenever possible, custom syllabification formulas or
dictionaries are preferred.

### Reading Time

SmoothText can calculate how long would a text take to read. The reading time is calculated based on the average reading
speed of an adult.

|                                                           Method                                                           |              Description               |
|:--------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------:|
|  [`reading_aloud_time`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.reading_aloud_time)  | Calculates the reading time of a text. |
|        [`reading_time`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.reading_time)        | Calculates the reading time of a text. |
| [`silent_reading_time`](https://smoothtext.github.io/smoothtext.html#smoothtext.smoothtext.SmoothText.silent_reading_time) |  Calculates the silent reading time.   |

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

### Other Features

Refer to the documentation for a complete list of available methods.

## Inconsistencies

### Backend Related Inconsistencies

- NLTK and Stanza have different tokenization rules. This may cause differences in the number of tokens/sentences
  between the two backends.

### Language Related Inconsistencies

- The syllabification of words may differ within the same language variant. For example, the word "hello" has two
  syllables in American English but one in British English. See the code snippet below.
  - To avoid this as much as possible, CMUdict is used for English as the default syllabification method. However, it may
    not be available in some cases. In such cases, Pyphen will be used as a fallback.

```Python
from pyphen import Pyphen

us = Pyphen(lang="en_US")
print(us.inserted("hello"))
# Output: 'hel-lo'

gb = Pyphen(lang="en_GB")
print(gb.inserted("hello"))
# Output: 'hello'
```

## Documentation

See [here](https://smoothtext.github.io/) for API documentation.

## License

SmoothText has an MIT license. See [LICENSE](./LICENSE).
