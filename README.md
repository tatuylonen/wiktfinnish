# Wiktfinnish

This is a Python module for inflecting Finnish words (verb inflection,
comparatives, cases, possessive suffixes, clitics) using
Wiktionary-compatible declensions and conjugations.

## Overview

This Python module is intended for generating inflected forms of
Finnish words in Wiktionary.  It is most conveniently used with
dictionaries extracted using the
[wiktextract](https://github.com/tatuylonen/wiktextract).  The
intention is that this module can be used to generate the complete set
of inflected forms for any Finnish word in Wiktionary - including
comparisons, possessive suffixes, clitics, and nominally inflected
verb forms.

## Getting started

### Installing

To install ``wiktwikfinnish``, use ``pip3`` (or ``pip``, as
appropriate), or clone the repository and install from the source:

```
git clone https://github.com/tatuylonen/wiktfinnish.git
cd wiktfinnish
python3 setup.py install
```

This will install the ``wiktfinnish`` package.

Note that this software has currently only been tested with Python 3.
Back-porting to Python 2.7 should not be difficult; it just hasn't
been tested yet.  Please report back if you test and make this work
with Python 2.

### Running tests

This package includes tests written using the ``unittest`` framework.
They can be run using, for example, ``nose``, which can be installed
using ``pip3 install nose``.

To run the tests, just use the following command in the top-level directory:
```
nosetests
```

## Usage

### Generating an inflected word form

The basic way to generate an inflected word form is to use the following
code snippet.

```
import wiktfinnish

results = wiktfinnish.inflect(name, args, form)
```

The ``inflect`` function returns a list of strings, which are the
alternative forms generated for that word form.  The preferred, or
most common form should be first in the list and rare/archaic examples
later.

The name and arguments specify the conjugation/declension for the word.  That includes specifying the word to be inflected.  See below for details.

The form is a 5-tuple ``(verbform, comparison, case, possessive,
clitic)``, that specifies the inflected form to be generated.  It is described in detail below.

### Specifying the conjugation/declension

In the API, each word to be inflection must be specified by a
conjugation (verbs) or declination (nominals) specification.  The
specification is basically the arguments of the ``{{fi-decl-xyx}}`` or
`{{fi-conj-xyz}}`` template from Wiktionary, encoded into a Python
dictionary.  In the API, this template will be called ``args``.
Additionally, the API requies the name of the template to be supplied
as the ``name`` argument.  These are readily available in the proper
format if the dictionary has been extracted using ``wiktextract`` (see
below).

### Specifying the desired word form

The desired word form is specified by a 5-tuple ``(verbform,
comparison, case, possessive, clitic)``, where any unused components
must be empty strings.

Generally, finite verb forms only have the ``verbform`` part specified
and other parts empty.  Nouns, pronouns, adjectives, and numerals
always have the ``verbform`` and ``comparison`` parts empty.
Adjectives (and some verb forms) may also use ``comparison``.  The
``possessive`` specifies a possessive suffix, and they are mostly used
with nouns.  The ``clitic`` is specifies any clitics to be attached at
the end of the word, and can be used with any part-of-speech.

### Verb form names

The following values are allowed for ``verbform``, in addition to the
empty string.  The list of valid verb form names can be found in
``wiktfinnish.VERB_FORMS``.  (There may still be some changes coming
in how case endings are handled for infinitives.)

```
    pres-1sg
    pres-2sg
    pres-3sg
    pres-1pl
    pres-2pl
    pres-3pl
    pres-1sg-neg
    pres-2sg-neg
    pres-3sg-neg
    pres-1pl-neg
    pres-2pl-neg
    pres-3pl-neg
    pres-pass
    pres-pass-neg
    past-1sg
    past-2sg
    past-3sg
    past-1pl
    past-2pl
    past-3pl
    past-1sg-neg
    past-2sg-neg
    past-3sg-neg
    past-1pl-neg
    past-2pl-neg
    past-3pl-neg
    past-pass
    past-pass-neg
    cond-1sg
    cond-2sg
    cond-3sg
    cond-1pl
    cond-2pl
    cond-3pl
    cond-1sg-neg
    cond-2sg-neg
    cond-3sg-neg
    cond-1pl-neg
    cond-2pl-neg
    cond-3pl-neg
    cond-pass
    cond-pass-neg
    impr-2sg
    impr-3sg
    impr-1pl
    impr-2pl
    impr-3pl
    impr-2sg-neg
    impr-3sg-neg
    impr-1pl-neg
    impr-2pl-neg
    impr-3pl-neg
    impr-pass
    impr-pass-neg
    potn-1sg
    potn-2sg
    potn-3sg
    potn-1pl
    potn-2pl
    potn-3pl
    potn-1sg-neg
    potn-2sg-neg
    potn-3sg-neg
    potn-1pl-neg
    potn-2pl-neg
    potn-3pl-neg
    potn-pass
    potn-pass-neg
    pres-part
    pres-pass-part
    past-part
    past-pass-part
    agnt-part
    nega-part
    inf1
    inf1-long
    inf2-ine
    inf2-pass-ine
    inf2-ins
    inf3-ine
    inf3-ela
    inf3-ill
    inf3-ade
    inf3-abe
    inf3-ins
    inf3-pass-ins
    inf4-nom
    inf4-par
    inf5
```

### Comparison names

Adjectives, participles, and some other adverbs accept comparisons.
The normal positive form is marked by the empty string.  ``comp``
indicates comparative, and ``sup`` indicates superlative form.  The
list of valid comparison names (including the empty string) can be
found in ``wiktfinnish.COMP_FORMS``.

### Case names

Nouns, pronouns, adjectives, numerals, and various verb forms
(especially participles) accept case endings.  The following names are
used to specify both case ending and number.  The ``acc-sg`` and
``acc-pl`` values are only valid for certain pronouns.  For all other
parts of speech, one of ``nom-sg``, ``nom-pl``, ``gen-sg``, or
``gen-pl`` should be used instead.  The list of valid case+number
values can be found in ``wiktfinnish.CASE_FORMS``.

```
    nom-sg     - nominative (singular)
    acc-sg     - accusative
    gen-sg     - genitive
    ptv-sg     - partitive
    ine-sg     - inessive
    ela-sg     - elative
    ill-sg     - illative
    ade-sg     - adessive
    abl-sg     - ablative
    all-sg     - allative
    ess-sg     - essive
    tra-sg     - translative
    ins-sg     - instructive
    abe-sg     - abessive
    cmt-sg     - comitative
    nom-pl     - nominative (plural)
    acc-pl     - etc.
    gen-pl
    ptv-pl
    ine-pl
    ela-pl
    ill-pl
    ade-pl
    abl-pl
    all-pl
    ess-pl
    tra-pl
    ins-pl
    abe-pl
    cmt-pl
```

### Possessive suffixes

The following values are used for possessive suffixes.  The empty
string indicates that no possessive suffix is to be attached.  Note
that for the third person, the ``3x`` value is used for both singular
and plural, as the forms are always the same.  The list of valid
possessive forms (including the empty string) can be found in
``wiktfinnish.POSSESSIVE_FORMS``.

```
   1s       - first person singular
   2s	    - second person singular
   3x	    - third person (singular or plural)
   1p	    - first person plural
   2p	    - second person plural
```

### Clitics

There is a fixed set of clitics that can be attached.  In practice,
however, more clitics may be used in spoken language and there are
various other alternations.  The following values can be used for
clitics, in addition to the empty string, which signifies no clitic.
The list of valid clitic values (including the empty string) can be
found in ``wiktfinnish.CLITIC_FORMS``.

```
    kO
    kin
    kAAn
    pA
    s
    kA
    hAn
    kOhAn
    pAhAn
    pAs
    kOs
    kinkO
    kAAnkO
    kinkOhAn
```

### Iterating over all possible word forms

Functions are also provided for iterating over all valid 5-tuples
indicating word forms.  These are useful if one wants to generate all
possible forms of a word.  The following code snippet iterates over
all adjective forms:

```
import wiktfinnish

for verbform, comp, case, poss, clitic in wiktfinnish.all_forms_iter("adj"):
    print(verbform, comp, case, poss, clitic)
```

The ``all_forms_iter`` function takes as a mandatory argument a
part-of-speech (as returned by the ``wiktextract`` module, see below),
including "noun", "adj", "verb", "num", "pron", "adv", etc.  It can
also take the following optional keyword arguments (more will likely
be added later) to restrict the forms that are enumerated:

* ``comparable``: if True (default), include comparison forms (for adjectives, adverbs)
* ``transitive``: if True (default), include agent participle (forms that are only valid for verbs with an agent)
* ``no_clitics``: if True, don't include forms with clitics (default is to include them)

### Fast way of obtaining list of possible forms for a part-of-speech

There is also a cached version of the iterator that returns a sequence
containing all valid forms for the given part-of-speech and keyword
arguments.  It takes the same arguments (including keyword arguments)
as the iterator, but instead of returning an iterator returns a list.
This function is also much faster and caches its results for maximum
performance.

```
import wiktfinnish

lst = wiktfinnish.all_forms_list("verb")
```

#### Standard vs. colloquial Finnish

Currently this generates forms according to standard written Finnish.  The
intention is to generate spoken language / colloquial forms for
standard Finnish in the future, as well as possibly some dialectical
forms.  However, that is not yet implemented.

## Contributing

The official repository of this project is on
[github](https://github.com/tatuylonen/wiktfinnish).

Please email to ylo at clausal.com if you wish to contribute or have
patches or suggestions.

## License

Copyright (c) 2018 [Tatu Ylonen](https://ylonen.org).  This package is
free for both commercial and non-commercial use.  It is licensed under
the MIT license.  See the file
[LICENSE](https://github.com/tatuylonen/wiktfinnish/blob/master/LICENSE)
for details.

Credit and linking to the project's website and/or citing any future
papers on the project would be highly appreciated.
