# Definitions of names of inflected forms for Finnish.  This file also contains
# iterators for enumerating all 5-tuples for possible inflectional forms for
# any given part-of-speech.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

# Names of comparative forms for adjectives (the empty string means positive,
# or normal form).
COMPARATIVE_FORMS = (
    "",
    "comp",
    "sup",
    "manner",
    "comp-manner",
    "sup-manner")

# Names of Finnmish cases.  We combine case and number into the same name.
CASE_FORMS = (
    "",        # Placeholder when word/form does not inflect in case
    "nom-sg",
    "acc-sg",  # Used for certain pronouns only
    "gen-sg",
    "ptv-sg",
    "ine-sg",
    "ela-sg",
    "ill-sg",
    "ade-sg",
    "abl-sg",
    "all-sg",
    "ess-sg",
    "tra-sg",
    "ins-sg",
    "abe-sg",
    "nom-pl",
    "acc-pl",  # Used for certain pronouns only
    "gen-pl",
    "ptv-pl",
    "ine-pl",
    "ela-pl",
    "ill-pl",
    "ade-pl",
    "abl-pl",
    "all-pl",
    "ess-pl",
    "tra-pl",
    "abe-pl",
    "ins-pl",
    "cmt",
)

# Names of possessive suffixes.  The empty string means no possessive suffix.
# 3x means either plural or singular third person (they have the same form).
POSSESSIVE_FORMS = (
    "",
    "1s",
    "2s",
    "3x",
    "1p",
    "2p",
)

# Names of verb forms.
#
# XXX should perhaps combine some of the negative forms as they are usually
# (always?) identical.  Check whether they really are always.
VERB_FORMS = (
    "",            # Placeholder, for non-verbs only
    "pres-1sg",
    "pres-2sg",
    "pres-3sg",
    "pres-1pl",
    "pres-2pl",
    "pres-3pl",
    "pres-neg",
    "pres-pass",
    "pres-pass-neg",
    "past-1sg",
    "past-2sg",
    "past-3sg",
    "past-1pl",
    "past-2pl",
    "past-3pl",
    "past-pass",
    "cond-1sg",
    "cond-2sg",
    "cond-3sg-or-neg",
    "cond-1pl",
    "cond-2pl",
    "cond-3pl",
    "cond-pass",
    "cond-pass-neg",
    "impr-2sg",
    "impr-3sg",
    "impr-1pl",
    "impr-2pl",
    "impr-3pl",
    "impr-2sg-neg",
    "impr-neg",  # Note: impr-2sg-neg is distinct
    "impr-pass",
    "impr-pass-neg",
    "potn-1sg",
    "potn-2sg",
    "potn-3sg",
    "potn-1pl",
    "potn-2pl",
    "potn-3pl",
    "potn-neg",
    "potn-pass",
    "potn-pass-neg",
    "pres-part",
    "pres-pass-part",
    "past-part",
    "past-pass-part",
    "agnt-part",
    "nega-part",
    "inf1",
    "inf1-long",
    "inf2",
    "inf2-pass",
    "inf3",
    "inf3-pass",
    "inf4",
    "inf5",
)

# Names of all clitics and allowed clitic combinations.  The empty string
# means no clitic.
CLITIC_FORMS = ("",
                "kO",
                "kin",
                "kAAn",
                "pA",
                "s",
                "kA",
                "hAn",
                "kOhAn",
                "pAhAn",
                "pAs",
                "kOs",
                "kinkO",   # Last three aren't used in Finnish treebank
                "kAAnkO",
                #"kinkOhAn",
)

######################################################################
# The rest of file is about enumerating 5-tuples representing
# inflected forms.
######################################################################

# Cache of all forms for combinations of part-of-speech and other parameters
# restricting which forms are posible.
all_forms_cache = {}


def all_forms_list(*args, **kwargs):
    """Returns a list/tuple of all possible word form descriptors for the given
    part-of-speech and other restrictions.  This caches the result."""
    key = (args, tuple(sorted(kwargs.items())))
    if key in all_forms_cache:
        return all_forms_cache[key]
    forms = tuple(x for x in all_forms_iter(*args, **kwargs))
    all_forms_cache[key] = forms
    return forms


def all_forms_iter(pos, transitive=True,
                   no_comp=False, no_case=False, no_poss=False,
                   no_clitic=False):
    """Returns an iterator that iterates over all possible word form
    descriptors for the given part-of-speech and other parameters."""
    assert isinstance(pos, str)

    comp_forms = [""] if no_comp else COMPARATIVE_FORMS
    case_forms = ["nom-sg"] if no_case else list(x for x in CASE_FORMS if x)
    poss_forms = [""] if no_poss else POSSESSIVE_FORMS
    clitic_forms = [""] if no_clitic else CLITIC_FORMS

    if pos in ("noun", "name", "num", "letter", "pron-qnt", "pron-refl",
               "pron-interr", "postp", "prep", "digit"):
        for case in case_forms:
            for poss in poss_forms:
                if case in ("acc-sg", "acc-pl"):
                    continue
                for clitic in clitic_forms:
                    if clitic == "s" and pos != "pron-interr":
                        continue
                    if clitic == "kA":
                        continue
                    yield ("", "", case, poss, clitic)
    elif pos in ("pron", "pron-pers"):
        for case in case_forms:
            for clitic in clitic_forms:
                if clitic in ("s", "kA"):
                    continue
                yield ("", "", case, '', clitic)
    elif pos == "adj":
        for comp in comp_forms:
            if comp in ("manner", "comp-manner", "sup-manner"):
                for clitic in clitic_forms:
                    if clitic == "s":
                        continue
                    yield ("", comp, "", "", clitic)
            else:
                for case in case_forms:
                    if case in ("acc-sg", "acc-pl"):
                        continue
                    for poss in poss_forms:
                        for clitic in clitic_forms:
                            if clitic == "s":
                                continue
                            yield ("", comp, case, poss, clitic)
    elif pos == "verb":
        for vform in VERB_FORMS:
            if not vform:
                continue
            if not transitive and vform == "agnt-part":
                continue
            comps = [""]
            cases = [""]
            if vform in ("pres-part", "pres-pass-part",
                         "past-part", "past-pass-part",
                         "agnt-part", "nega-part"):
                cases = case_forms
            elif vform == "inf2":
                cases = ("ine-sg", "ins-sg")
            elif vform == "inf2-pass":
                cases = ("ine-sg",)
            elif vform == "inf3":
                cases = ("ine-sg", "ela-sg", "ill-sg", "ade-sg", "abe-sg",
                         "ins-sg")
            elif vform == "inf3-pass":
                cases = ("ins-sg",)
            elif vform == "inf4":
                # We treat the -minen noun derivative as inf4 and thus allow
                # full nominal inflection on inf4.
                cases = case_forms
            if vform in ("pres-part", "past-part",
                         "pres-pass-part", "past-pass-part",
                         "nega-part"):
                comps = comp_forms
            for comp in comps:
                if comp in ("manner", "comp-manner", "sup-manner"):
                    if vform not in ("pres-part", "pres-pass-part",
                                     "past-part", "past-pass-part",
                                     "nega-part"):
                        continue
                    for clitic in clitic_forms:
                        yield (vform, comp, "", "", clitic)
                    continue
                for case in cases:
                    if case in ("acc-sg", "acc-pl"):
                        continue  # Accusative used only for pronouns
                    posses = [""]
                    if (vform in ("inf1-long", "inf5", "agnt-part",
                                  "pres-pass-part",
                                  "past-part",
                                  "pres-part", "past-pass-part") or
                        (vform == "inf2" and case == "ine-sg") or
                        (vform == "inf3" and case in ("ine-sg", "ela-sg",
                                                      "ill-sg", "ade-sg",
                                                      "abe-sg",
                                                      "ins-sg")) or
                        vform == "inf4"):
                        posses = poss_forms
                    for poss in posses:
                        if (not no_poss and not poss and
                            vform in ("inf1-long", "inf5")):
                            continue
                        # XXX I think this is fully incorrect
                        #if (poss and case != "nom-sg" and
                        #    vform in ("pres-part", "past-pass-part")):
                        #    continue
                        for clitic in clitic_forms:
                            yield (vform, comp, case, poss, clitic)
    elif pos in ("conj", "intj", "suffix", "clitic", "punct"):
        yield ("", "", "", "", "")
    elif pos == "adv":
        for clitic in clitic_forms:
            yield ("", "", "", "", clitic)
            if pos == "adv":
                yield ("", "comp", "", "", clitic)
                yield ("", "sup", "", "", clitic)
    else:
        print("all_forms_iter: unimplemented pos:", pos)
        yield ("", "", "", "", "")
