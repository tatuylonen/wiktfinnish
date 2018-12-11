# This file defines the public exports from the wiktfinnish module.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

from wiktfinnish.formnames import COMPARATIVE_FORMS, CASE_FORMS
from wiktfinnish.formnames import POSSESSIVE_FORMS, VERB_FORMS, CLITIC_FORMS
from wiktfinnish.formnames import all_forms_list, all_forms_iter
from wiktfinnish.inflect import inflect
from wiktfinnish.inflect import add_clitic
from wiktfinnish.inflect import last_char_to_vowel, last_char_to_aou
from wiktfinnish.inflect import word_to_aae
from wiktfinnish.stem import encode_paradigm, decode_paradigm, valid_unknown_stem, is_exceptional, is_compound_declension, is_guessable, paradigm_nargs


__all__ = (
    "inflect",
    "add_clitic",
    "COMPARATIVE_FORMS",
    "CASE_FORMS",
    "POSSESSIVE_FORMS",
    "VERB_FORMS",
    "CLITIC_FORMS",
    "all_forms_list",
    "all_forms_iter",
    "last_char_to_vowel",
    "last_char_to_aou",
    "word_to_aae",
    "endode_paradigm",
    "decode_paradigm",
    "valid_unknown_stem",
    "is_exceptional",
    "is_compound_declension",
    "is_guessable",
    "paradigm_nargs",
)
