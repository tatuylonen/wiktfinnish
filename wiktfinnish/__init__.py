# This file defines the public exports from the wiktfinnish module.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE.

from wiktfinnish.formnames import COMP_FORMS, CASE_FORMS, POSSESSIVE_FORMS
from wiktfinnish.formnames import VERB_FORMS, CLITIC_FORMS
from wiktfinnish.formnames import all_forms_list, all_forms_iter
from wiktfinnish.inflect import inflect, inflect_nominal, inflect_verbal
from wiktfinnish.inflect import add_clitic

__all__ = (
    "COMP_FORMS",
    "CASE_FORMS",
    "POSSESSIVE_FORMS",
    "VERB_FORMS",
    "CLITIC_FORMS",
    "all_forms_list",
    "all_forms_iter",
    "inflect",
    "inflect_nominal",
    "inflect_verbal",
    "add_clitic",
)
