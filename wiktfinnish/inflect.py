# Code for generating Finnish word forms from Wiktionary-compatible
# declension/conjugation entries.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

import re
from wiktfinnish import nounspecs
from wiktfinnish import verbspecs
from wiktfinnish import formnames

# Set of all valid conjugation and declension names.  This is used in
# assertions.
CONJ_DECL_NAMES = (set(nounspecs.decl_name_map) |
                   set(nounspecs.noun_decls) |
                   set(verbspecs.verb_conjs))

# Special character used in pattern processing.  This is chosen from a
# Unicode private use area and should not appear in data.
EMPTY_CHAR = "\uf8ff"

# Mapping of conjugation argument names for fi-conj (it uses different
# argument names than fi-conj-table, the other conjugation used for
# irregular cases).
argument_name_map = {
    # For fi-conj
    "pres-1sg-neg": ["pres_conn"],
    "pres-2sg-neg": ["pres_conn"],
    "pres-3sg-neg": ["pres_conn"],
    "pres-1pl-neg": ["pres_conn"],
    "pres-2pl-neg": ["pres_conn"],
    "pres-3pl-neg": ["pres_conn"],
    "pres-pass-neg": ["pres_pass_conn"],
    "past-1sg-neg": ["past_part"],
    "past-2sg-neg": ["past_part"],
    "past-3sg-neg": ["past_part"],
    "past-1pl-neg": ["past_part_pl"],
    "past-2pl-neg": ["past_part_pl"],
    "past-3pl-neg": ["past_part_pl"],
    "past-pass-neg": ["past_pass_part"],
    "cond-3sg": ["cond_conn"],
    "cond-1sg-neg": ["cond_conn"],
    "cond-2sg-neg": ["cond_conn"],
    "cond-3sg-neg": ["cond_conn"],
    "cond-1pl-neg": ["cond_conn"],
    "cond-2pl-neg": ["cond_conn"],
    "cond-3pl-neg": ["cond_conn"],
    "cond-pass-neg": ["cond_pass_conn"],
    "impr-2sg": ["pres_conn"],
    "impr-2sg-neg": ["pres_conn"],
    "impr-3sg-neg": ["impr_conn"],
    "impr-1pl-neg": ["impr_conn"],
    "impr-2pl-neg": ["impr_conn"],
    "impr-3pl-neg": ["impr_conn"],
    "impr-pass-neg": ["impr_pass_conn"],
    "potn-1sg-neg": ["potn_conn"],
    "potn-2sg-neg": ["potn_conn"],
    "potn-3sg-neg": ["potn_conn"],
    "potn-1pl-neg": ["potn_conn"],
    "potn-2pl-neg": ["potn_conn"],
    "potn-3pl-neg": ["potn_conn"],
    "potn-pass-neg": ["potn_pass_conn"],
    # Note: these verbs may not have inf1 (see discussion win Wiktionary:kutiaa)
    "inf1-long": ["inf1_longa"],
    "inf2-ine": ["inf2_ines"],
    "inf2-pass-ine": ["inf2_pass_ines"],
    "inf2-ins": ["inf2_inst"],
    "inf3-ine": ["inf3_ines"],
    "inf3-ela": ["inf3_elat"],
    "inf3-ill": ["inf3_illa"],
    "inf3-ade": ["inf3_ades"],
    "inf3-abe": ["inf3_inst"],
    "inf3-ins": ["inf3_inst"],
    "inf3-pass-ins": ["inf3_pass_inst"],
    "inf4-nom": ["inf4_nomi"],
    "inf4-par": ["inf4_part"],

    # For fi-decl-pron and fi-decl
    "nom-sg": ["1s", "word"],
    "gen-sg": ["2s"],
    "ptv-sg": ["3s", "par_sg"],
    "acc-sg": ["4s"],
    "ine-sg": ["5s"],
    "ela-sg": ["6s"],
    "ill-sg": ["7s"],
    "ade-sg": ["8s"],
    "abl-sg": ["9s"],
    "all-sg": ["10s"],
    "ess-sg": ["11s"],
    "tra-sg": ["12s"],
    "ins-sg": ["13s"],
    "abe-sg": ["14s"],
    "cmt-sg": ["15s", "com_pl"],
    "nom-pl": ["1p"],
    "gen-pl": ["2p"],
    "ptv-pl": ["3p", "par_pl"],
    "acc-pl": ["4p"],
    "ine-pl": ["5p"],
    "ela-pl": ["6p"],
    "ill-pl": ["7p"],
    "ade-pl": ["8p"],
    "abl-pl": ["9p"],
    "all-pl": ["10p"],
    "ess-pl": ["11p"],
    "tra-pl": ["12p"],
    "ins-pl": ["13p"],
    "abe-pl": ["14p"],
    "cmt-pl": ["15p", "com_pl"],
    # superessive "a1s": "siellä",
    # delative "a2s": "sieltä",
    # sublative "a3s": "sinne",
    # lative "a4s": "siis",
    # temporal "a5s": "silloin",
    # causative "a6s": "siten",
    # multiplicative a7s
    # distributive a8s
    # temp.dist. a9s
    # prolative a10s
    # situative a11s
    # oppositive a12s
}


def needs_aou(word):
    """Returns true if the characters in the word suggest "a", "o", or "u"
    due to vowel harmony."""
    return re.search("([aouAOU])[^yäöYÄÖ]*$", word)


def word_to_aae(word):
    """Returns "a" or "ä" based on vowel harmony."""
    if needs_aou(word):
        return "a"
    return "ä"


def last_char_to_vowel(word):
    """Intended for abbreviations, returns the vowel for illative etc based
    on how the last character is pronounced in Finnish."""
    assert isinstance(word, str)
    # We iterate over characters of the word, because the last might be a
    # punctuation, perhaps.
    for last in reversed(word):
        last = last.lower()
        for ch, prev in (("e", "eébcçdgptvwz"),
                         ("o", "ohk"),
                         ("ä", "äflmnrsx"),
                         ("i", "ij"),
                         ("u", "uq"),
                         ("y", "yü")):
            if last in prev:
                return ch
    return "e"


def last_char_to_aou(word):
    """Intended for abbreviations, returns "a" or "ä" based on vowel harmony
    for the last char."""
    assert isinstance(word, str)
    ch = last_char_to_vowel(word)
    if ch in "aou":
        return "a"
    return "ä"


def process_template(template, args, ill_sg_vowel=None):
    """Processes a single inflection template.  This handles certain special
    characters in the template.  See nounspecs.py for a description of the
    special characters."""
    parts = []
    delparts = []
    for x in template:
        if x.isdigit():
            k = int(x)
            if k in args:
                v = args[k]
            else:
                v = args.get(x, "")
            if x == "9":
                if "par_sg_a" in args:
                    parts.append(args["par_sg_a"])
                else:
                    assert delparts
                    parts.append(delparts[-1])
            if x == "3" and not v:
                # XXX what exactly was this kludge for...?  I'm not sure if
                # this is now handled by other means (default value for last
                # argument).
                v = EMPTY_CHAR
            for y in v:
                parts.append(y)
        elif x == "@":
            if ill_sg_vowel is not None:
                parts.append(ill_sg_vowel)
            else:
                p = "".join(parts + delparts)
                m = re.search(r"([aeiouyåäöAEIOUYÅÄÖ])"
                              r"[^aeiouyåäöAEIOUYÅÄÖ]*$",
                              p)
                if m:
                    parts.append(m.group(1).lower())
                else:
                    m = re.search(r"[éÉ]"
                                  r"[^aeiouyåäöAEIOUYÅÄÖ]*$",
                                  p)
                    if m:
                        parts.append("e")
                    else:
                        ch = last_char_to_vowel(p[-1])
                        parts.append(ch)
        elif x == "A":
            a = args.get("par_sg_a", None)
            if a:
                parts.append(a)
            else:
                p = "".join(parts + delparts)
                parts.append(word_to_aae(p))
        elif x == "O":
            p = "".join(parts + delparts)
            if needs_aou(p):
                parts.append("o")
            else:
                parts.append("ö")
        elif x == "U":
            p = "".join(parts + delparts)
            if needs_aou(p):
                parts.append("u")
            else:
                parts.append("y")
        elif x == "D":
            p = "".join(parts)
            if p and p[-1] in "rnml":
                parts.append(p[-1])
            else:
                parts.append("d")
        elif x == "-":
            # Drop last, move to delparts so it counts for gradation
            p = parts.pop()
            delparts.append(p)
        elif x == "/":
            # Drop second to last
            p = parts.pop()
            parts.pop()
            parts.append(p)
        else:
            parts.append(x)
    v = "".join(parts)
    if v.find(EMPTY_CHAR) >= 0:
        for ch in "aeiouyäöAEIOUYÄÖ":
            v = re.sub("([aeiouyäöAEIOUYÄÖ]" + ch + ")" + EMPTY_CHAR +
                       "(" + ch + ")", r"\1'\2", v)
        v = re.sub(EMPTY_CHAR, "", v)
    return v


def add_possessive(results, form, poss):
    """Adds a possessive suffix to each result."""
    if not poss:
        return results

    # Add possessive suffix
    suffixes = nounspecs.possessive_suffixes[poss]
    if isinstance(suffixes, str):
        suffixes = [suffixes]
    results2 = []
    for suffix in suffixes:
        for v in results:
            parts = list(x for x in v)
            if suffix[0] != "@":
                for x in suffix:
                    if x == "A":
                        p = "".join(parts)
                        m = re.search("([aouAOU])[^yäöYÄÖ]*$", p)
                        if m:
                            parts.append("a")
                        else:
                            parts.append("ä")
                    else:
                        parts.append(x)
                v = "".join(parts)
            else:
                if form not in (
                        "ine-sg", "ine-pl", "ela-sg", "ela-pl",
                        "all-sg", "all-pl", "ade-sg", "ade-pl",
                        "abl-sg", "abl-pl", "tra-sg", "tra-pl",
                        "ess-sg", "ess-pl", "abe-sg", "abe-pl",
                        "ptv-sg", "ptv-pl", "cmt-sg", "cmt-pl",
                        "inf1-long", "inf2-ine", "inf3-ine",
                        "inf3-ela", "inf3-ade",
                        "inf3-abe", "inf4-nom", "inf4-par",
                        "inf5"):
                    continue
                if len(v) > 2 and v[-2] == v[-1]:
                    continue
                v += v[-1]
                v += suffix[1:]
            if v:
                results2.append(v)
    return results2


def add_clitic(results, clitic):
    """Adds a clitic to the results."""
    if not clitic:
        return results

    results2 = []
    for v in results:
        args = {"1": v}
        ret = process_template("1" + clitic, args)
        if ret:
            results2.append(ret)
    return results2


def clean_exception(v):
    """Cleans an exception value from various extra stuff that we don't want
    in the result."""
    v = re.sub(r"\[\[[^]|]*\|([^]]*)\]\]", r"\1", v)
    v = re.sub(r"\[\[", "", v)
    v = re.sub(r"\]\]", "", v)
    v = re.sub(r"``+", "", v)
    v = re.sub(r"''+", "", v)
    v = re.sub(r"(?is)<sup>.*?</sup>", "", v)
    v = re.sub(r"<[^>]*>", "", v)
    v = re.sub(r"\s+", " ", v)
    return v.strip()


def inflect_using(decls, name, args, form, use_poss, use_clitic):
    """Inflects the word indicated by the declension/conjugation specification
    into the form ``form`` using the inflection type ``name`` and
    type specifications in ``decls``.  ``use_poss`` indicates whether
    a possessive suffix or clitic follows, and ``use_clitic`` indicates
    whether a clitic follows.  This function is used for both nominals
    and verbs."""
    # Map some legacy declension names that are redirects in wiktionary
    if name in nounspecs.decl_name_map:
        name = nounspecs.decl_name_map[name]

    # Look up the inflection data for the declension/conjugation
    decl = decls.get(name, None)
    if decl is None:
        print("Unrecognized declension/conjugation name:", name)
        return []

    # Default last argument to a/ä if it does not exist (it is missing from
    # various declensions in Wikipedia)
    nargs = decl.get("nargs", None)
    if nargs:
        if nargs not in args and str(nargs) not in args:
            #print("Template {}, does not have expected arg {}: {}"
            #      "".format(name, nargs, args))
            args = args.copy()
            args[nargs] = word_to_aae(args.get(1) or args.get("1") or "")
        else:
            # Some templates, e.g., Uusikaarepyy, have more arguments than
            # are used by the template, and the expectation seems to be that
            # the last one is the ae argument and the others are merged into
            # the stem.
            for i in range(nargs + 1, 20):
                if i not in args and str(i) not in args:
                    break
            i -= 1
            if i > nargs:
                # This declension has more arguments than it takes
                #print("DECLENSION HAS TOO MANY ARGS:", name, args)
                if nargs == 2 and not decl.get("ignore-extra-args", False):
                    stem = ""
                    for j in range(1, i):
                        stem += args.get(j) or args.get(str(j)) or ""
                    aae = args.get(i) or args.get(str(i)) or ""
                    if aae not in ("a", "ä"):
                        stem += aae
                        aae = word_to_aae(stem)
                    args = args.copy()
                    for j in range(1, i + 1):
                        try:
                            del args[j]
                        except KeyError:
                            pass
                        try:
                            del args[str(j)]
                        except KeyError:
                            pass
                    args[1] = stem
                    args[2] = aae

    results = []

    # Check if it is a declension for compound words that inflect from multiple
    # locations.
    if "split" in decl and (form != "nom-sg" or "word" not in args):
        split = decl["split"]
        assert isinstance(split, (list, tuple))
        assert len(split) % 2 == 0
        space = args.get("space", " ")
        for i in range(0, len(split), 2):
            last_part = i == len(split) - 2
            start = split[i]
            new_name = split[i + 1]
            end = 100 if last_part else split[i + 2]
            new_args = {}
            for x, v in args.items():
                if isinstance(x, int):
                    if x < start or x >= end:
                        continue
                    new_args[x - start + 1] = v
                elif isinstance(x, str) and x.isdigit():
                    x = int(x)
                    if x < start or x >= end:
                        continue
                    new_args[x - start + 1] = v
                elif (x in ("par_sg_a", "ill_sg_vowel", "ill_sg_vowel2") and
                      not last_part):
                    # Put ill_sg_a only in last one (KLUDGE!)
                    pass
                else:
                    new_args[x] = v
            ret = inflect_using(decls, new_name, new_args, form,
                                last_part and use_poss,
                                last_part and use_clitic)
            if not results:
                results.extend(ret)
            else:
                new_results = []
                for x in results:
                    for y in ret:
                        new_results.append(x + space + y)
                results = new_results
        return results

    def add_exception(v):
        # Some exception forms contain [[...]] or multiple words.
        # Use the last word (for verb combinations) and clean up
        # the value.
        if name != "fi-decl-pron":
            v = re.sub(r"\b(minun|sinun|hänen|meidän|teidän|heidän)\b", "", v)
        v = re.sub(r"\(\*\)", "", v)
        v = clean_exception(v)
        if v.startswith("/") or v.endswith("/"):
            return  # Happens with some loan words, e.g. college
        # Some cases, at least some fi-decl-pron, have multiple alternatives
        # separated by commas.
        for v in v.split(","):
            v = v.strip()
            # Some values, esp. verbal, show the whole verb chain, with the
            # actual form the last word.
            if v.find(" ") >= 0:
                v = v.split(" ")[-1]
            # Some entries mark rare forms with parenthesis (others have
            # superscript "rare").
            if v.startswith("(") and v.endswith(")"):
                v = v[1:-1]
            # Some entries mark non-existent values with a dash (a special
            # unicode dash is also used).
            if not v or v == "-" or v == "–":  # Latter is unicode (long dash?)
                return
            # If a possessive is added, some forms need to be transformed a bit.
            if use_poss and form in ("tra-sg", "tra-pl"):
                if not v.endswith("ksi"):
                    #print("EXCEPTION for tra not ending with i:",
                    #      name, args, form, use_poss)
                    continue
                v = v[:-1] + "e"
            elif use_poss and form in ("inf5", "inf1-long", "cmt-sg", "cmt-pl"):
                if v[-2:] in ("an", "en", "in", "on", "un", "yn", "än", "ön"):
                    v = v[:-2]
                elif v.endswith("nsa") or v.endswith("nsä"):
                    v = v[:-3]
            elif use_poss and form in ("gen-sg", "gen-pl", "ill-sg", "ill-pl",
                                       "ins-pl", "nom-pl"):
                if v[-1] in ("n", "t"):
                    v = v[:-1]
            elif use_poss and form in ("inf4-nom",):
                if v.endswith("nen"):
                    v = v[:-3] + "se"

            # Add the value to the results.
            results.append(v)

    formarg = re.sub("-", "_", form)
    v = args.get(formarg, None)
    if v is not None:
        # Exception defined for this form
        if v:
            add_exception(v)
            for i in range(2, 5):
                v = args.get(formarg + str(i), None)
                if v:
                    add_exception(v)
    elif (form in argument_name_map and
          any(x in args for x in argument_name_map[form])):
        for formarg in argument_name_map[form]:
            v = args.get(formarg, None)
            if v:
                add_exception(v)
    else:
        templates = False
        if use_clitic and not use_poss:
            # Try to find special clitic-only template (used for abbreviations)
            templates = decl.get(form + "-clitic", False)
        if templates is False and use_poss:
            # Try -poss template first if possessive suffix
            templates = decl.get(form + "-poss", False)
        if templates is False:
            # Otherwise just use the default template
            templates = decl.get(form, None)
        if not templates:
            return []
        if isinstance(templates, str):
            templates = [templates]

        # Kludge to handle certain words with two vowel choices in ill-sg
        if form == "ill-sg":
            ill_sg_vowel = args.get("ill_sg_vowel", None)
            ill_sg_vowel2 = args.get("ill_sg_vowel2", None)
        else:
            ill_sg_vowel = None
            ill_sg_vowel2 = None

        # Generate word forms for each template
        for template in templates:
            v = process_template(template, args, ill_sg_vowel=ill_sg_vowel)
            if v:
                results.append(v)
            # Kludge to handle certain words with two vowel choices in ill-sg
            if ill_sg_vowel2 is not None:
                v = process_template(template, args, ill_sg_vowel=ill_sg_vowel2)
                if v:
                    results.append(v)
    return results


def inflect_nominal(name, args, form, comp="", poss="",
                    clitic="", force_n=False):
    """Inflects the word whose declension/conjugation information is in
    ``args`` to the form indicated by ``form``.  ``poss`` indicates
    optional possessive suffix form(s).  Returns None if the
    form is invalid for the word."""

    if name not in nounspecs.noun_decls and name not in nounspecs.decl_name_map:
        print("inflect_nominal: unrecognized declension", name, "for", args)
        return []
    assert form in formnames.CASE_FORMS
    assert comp in formnames.COMP_FORMS
    assert poss in formnames.POSSESSIVE_FORMS
    assert isinstance(clitic, str)

    # If the word only occurs in singular/plural, refuse to generate forms
    # that conflict with that.
    if not force_n and "n" in args:
        n = args["n"].strip()
        if n in ("p", "pl", "Pl", "plural", "Plural"):
            if form.endswith("-sg"):
                return []
        if n in ("s", "sg", "Sg", "singular", "Singular"):
            if form.endswith("-pl"):
                return []
    # Another way to mark that only singulars are generated
    if not force_n and args.get("nopl", "0") != "0":
        if form.endswith("-pl"):
            return []
    # A third way to mark that only plurals are generated
    if not force_n and args.get("nosg", "0") != "0":
        if form.endswith("-sg"):
            return []

    # In comitative, force possessive suffix if not adj and none provided
    if args.get("pos") not in ("adj", "pron", "num"):
        if form == "cmt-pl" and not poss:
            poss = "3x"

    # Only allow comparison for forms treated as adjectives.
    if comp != "" and args.get("pos") != "adj":
        print("Comparative/superlative without pos=adj:", args)
        comp = ""

    # Inflect the word for comparison and case
    if comp != "":
        # Inflect using comparison and case
        results1 = inflect_using(nounspecs.noun_decls, name, args, comp,
                                 False, False)
        results = []
        for x in results1:
            if comp == "comp":
                assert x.endswith("mpi")
                x = x[:-3]
                name = "fi-decl-vanhempi"
            else:
                assert comp == "sup"
                assert x.endswith("in")
                x = x[:-2]
                name = "fi-decl-sisin"
            args = {"1": x, "2": word_to_aae(x)}
            ret = inflect_using(nounspecs.noun_decls, name, args, form,
                                poss != "", clitic != "")
            results.extend(ret)
    else:
        # Inflect using case only
        results = inflect_using(nounspecs.noun_decls, name, args, form,
                                poss != "", clitic != "")

    # Handle i=0 for nominative singular
    if form == "nom-sg" and args.get("i") == "0" and not poss:
        results2 = []
        for v in results:
            assert v.endswith("i")
            results2.append(v[:-1])
        results = results2

    # Handle e=1 for nominative singular
    if form == "nom_sg" and args.get("e", "0") == "1":
        results2 = []
        for v in results:
            results2.append(v + "e")
        results = results2

    # Add possessive suffix
    results = add_possessive(results, form, poss)

    # Add any clitic or other suffix.
    results = add_clitic(results, clitic)
    return results


def inflect_verbal(name, args, form, comp="", case="",
                   poss="", clitic=""):
    """Inflects the word whose declension/conjugation information is in
    ``args`` to the form indicated by ``form``.  ``poss`` indicates
    optional possessive suffix form(s).  Returns None if the
    form is invalid for the word."""
    if name not in verbspecs.verb_conjs:
        print("inflect_verbal: unrecognized verb conjucation", name, "for",
              args)
        return []
    assert form in formnames.VERB_FORMS
    assert poss in formnames.POSSESSIVE_FORMS
    assert comp in formnames.COMP_FORMS
    assert isinstance(clitic, str)

    if not poss and form in ("inf1-long", "agnt-part", "inf5"):
        poss = "3x"
    if form in ("pres-part", "pres-pass-part",
                "past-part", "past-pass-part", "agnt-part",
                "nega-part"):
        if not case:
            case = "nom-sg"
    elif case and case != "nom-sg":
        print("Case not allowed for", form)
        case = None

    # Default fi-conj-kumajaa to arg2 "a" (needed for "vipajaa")
    if name == "fi-conj-kumajaa" and "2" not in args and 2 not in args:
        args = args.copy()
        args[2] = "a"

    # Inflect the form using templates.
    results = inflect_using(verbspecs.verb_conjs, name, args, form,
                            case != "nom_sg" or poss != "", clitic != "")

    if case:
        results2 = []
        for v in results:
            if form in ("pres-part", "pres-pass-part", "agnt-part"):
                name = "fi-decl-koira"
                args = {"1": v[:-1], "2": "", "3": "",
                        "4": word_to_aae(v),
                        "pos": "adj"}
            elif form == "past-part":
                name = "fi-decl-kuollut"
                args = {"1": v[:-2], "2": word_to_aae(v),
                        "pos": "adj"}
            elif form == "past-pass-part":
                name = "fi-decl-valo"
                if v.endswith("ttu") or v.endswith("tty"):
                    args = {"1": v[:-3], "2": "tt", "3": "t",
                            "4": "u" if needs_aou(v) else "y",
                            "5": word_to_aae(v),
                            "pos": "adj"}
                else:
                    if v[-3] in "rnml":
                        weak = v[-3]
                    else:
                        weak = "d"
                    args = {"1": v[:-2], "2": "t", "3": weak,
                            "4": "u" if needs_aou(v) else "y",
                            "5": word_to_aae(v),
                            "pos": "adj"}
            else:
                assert form == "nega-part"
                name = "fi-decl-onneton"
                args = {"1": v[:-3], "2": word_to_aae(v),
                        "pos": "adj"}
            ret = inflect_nominal(name, args, case, comp=comp,
                                  poss=poss, clitic=clitic)
            results2.extend(ret)
        return results2
    else:
        # Add possessive suffix
        results = add_possessive(results, form, poss)
        # Add any clitic or other suffix.
        results = add_clitic(results, clitic)
        return results


def inflect(name, args, form, force_n=False):
    """This is a generic Finnish word inflection function.  This inflects
    a word of class ``name``, having conjugation/declension arguments ``args``
    into the form indicated by ``form``.  The form is indicated by
    (vform, comp, case, poss, clitic).  This returns a list of
    inflected forms, the most preferred one first.  If ``force_n`` is
    True, generates requested number regardless of limitations specified in
    ``args``."""
    if name not in CONJ_DECL_NAMES:
        print("UNDEFINED DECLENSION/CONJUGATION:", name, conj)
        return []
    assert isinstance(args, dict)
    assert isinstance(form, (list, tuple))
    assert len(form) == 5
    vform, comp, case, poss, clitic = form
    if vform:
        return inflect_verbal(name, args, vform, comp=comp, case=case,
                              poss=poss, clitic=clitic)
    if not case:
        case = "nom-sg"
    return inflect_nominal(name, args, case, comp=comp, poss=poss,
                           clitic=clitic, force_n=force_n)
