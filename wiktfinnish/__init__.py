# This file defines the public exports from the wiktfinnish module.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

from wiktfinnish.formnames import COMP_FORMS, CASE_FORMS, POSSESSIVE_FORMS
from wiktfinnish.formnames import VERB_FORMS, CLITIC_FORMS
from wiktfinnish.formnames import all_forms_list, all_forms_iter
from wiktfinnish.inflect import inflect
from wiktfinnish.inflect import add_clitic
from wiktfinnish.inflect import last_char_to_vowel, last_char_to_aou
from wiktfinnish.inflect import word_to_aae


__all__ = (
    "inflect",
    "add_clitic",
    "COMP_FORMS",
    "CASE_FORMS",
    "POSSESSIVE_FORMS",
    "VERB_FORMS",
    "CLITIC_FORMS",
    "all_forms_list",
    "all_forms_iter",
    "last_char_to_vowel",
    "last_char_to_aou",
    "word_to_aae",
)
