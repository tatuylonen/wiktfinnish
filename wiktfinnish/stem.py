# Encoding and decoding declensions and conjugations into a string.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

from wiktfinnish.inflect import word_to_aae
from wiktfinnish import nounspecs, verbspecs


# We use a character from the Unicode private use area to separate the parts.
# This should not occur in normal text.
# SEPARATOR = "\ue612"
SEPARATOR = "|"  # XXX for now for readability of data files

# Declensions for which we store ill-sg vowel in stem
ILL_SG_DECLS = ("fi-decl-parfait", "fi-decl-rosé")


def encode_paradigm(args):
    """Encodes conjugation/declination into a stem and a string.  Returns
    (None, None) for exception templates that can't be encoded; otherwise
    returns (stem, coding).  Verbal encodings start with V and nominal
    encodings with N."""
    assert "template_name" in args

    # Get template name and map it to canonical name
    name = args["template_name"]
    if name in nounspecs.decl_name_map:
        name = nounspecs.decl_name_map[name]

    # Exception paradigms cannot be encoded using this function
    if name in ("fi-decl", "fi-decl-pron", "fi-conj", "fi-conj-table"):
        return None, None

    # Get the number of arguments for the declension/conjugation.
    if name.startswith("fi-decl"):
        decl = nounspecs.noun_decls.get(name)
    else:
        decl = verbspecs.verb_conjs.get(name)
    if decl is None:
        print("UNRECOGNIZED DECLENSION", name, args)
        return None, None

    # We do not process compound word declensions for words that inflect
    # from multiple locations here.
    split = decl.get("split")
    if split is not None:
        return None, None  # Compound word declension

    # Get various parameters from the arguments.
    nargs = decl["nargs"]
    i0 = args.get("i", "1") == "0"
    e0 = args.get("e", "1") == "0"
    par_sg_a = args.get("par_sg_a", "")
    ill_sg_vowel = args.get("ill_sg_vowel", "")
    ill_sg_vowel2 = args.get("ill_sg_vowel2", "")
    stem = args.get("1", "")

    # Encode consonant gradation.  Note that we must save the indication
    # that there is gradation.
    gradation = None
    if nargs >= 4:
        arg2 = args.get("2", "")
        arg3 = args.get("3", "")
        if arg3 == "(')" or arg3 == "'":
            arg3 = ""
        elif arg3 == "’":
            arg3 = ""
        if arg2 == "’":
            arg2 = "'"
        # while (arg2 and arg3 and arg2[0] == arg3[0] and
        #        arg2[0] not in "kpt"):
        #     stem += arg2[0]
        #     arg2 = arg2[1:]
        #     arg3 = arg3[1:]
        if arg2 or arg3:
            gradation = "{}-{}".format(arg2, arg3)

    # End vowel is the final vowel in dot stems.  It generally depends
    # on the preceding letter.
    end_vowel = ""
    if name.endswith("-dot"):
        end_vowel = args.get("2", "")

    # Get the part after gradation, if any.
    end_part = ""
    if nargs == 5:
        end_part = args.get("4", "")

    # Determine the final a/ä argument.
    ae = args.get(str(nargs), "")
    if not ae:
        ae = word_to_aae(stem + end_vowel + end_part)

    # If no consonant gradation but there is an end part, move the end
    # part to the stem.  This reduces the number of distinct paradigm
    # encodings without loss of generality.
    if not gradation and end_part:
        stem += end_part
        end_part = ""

    # Encode final end_part/end_vowel and ae in stem
    assert not (end_part and end_vowel)
    if nargs in (3, 5) or name in ILL_SG_DECLS:
        stem += SEPARATOR + (end_part or end_vowel or
                             ill_sg_vowel + ill_sg_vowel2)
    if nargs > 1:
        stem += SEPARATOR + ae
    elif nargs == 0:
        stem = ""

    # Now encode it into a string.  Verbal encodings begin with a V
    # and nominal encodings with a N.
    parts = []
    if name.startswith("fi-decl-"):
        parts.append("N" + name[8:])
    else:
        assert name.startswith("fi-conj-")
        parts.append("V" + name[8:])
    if gradation:
        parts.append("G" + gradation)
    if i0:
        parts.append("I")
    if e0:
        parts.append("E")
    if par_sg_a:
        parts.append("P" + par_sg_a)

    paradigm = "".join(parts)

    return stem, paradigm


def decode_paradigm(stem, paradigm, pos=None):
    """Decodes stem and encoded conjugation/declension into arguments
    for generating word forms.  Returns None if stem or paradigm are
    invalid (or incompatible)."""
    assert isinstance(stem, str)
    assert isinstance(paradigm, str)
    assert pos is None or isinstance(pos, str)
    mode = None
    part = []
    args = {}
    ae = None
    end_vowel = ""

    # Set part-of-speech if given.
    if pos:
        args["pos"] = pos

    # Parse the coded paradigm.
    name = None
    for ch in paradigm + "X":
        if not ch.isupper():
            part.append(ch)
            continue
        v = "".join(part)
        part = []
        if mode == "N":
            name = "fi-decl-" + v
        elif mode == "V":
            name = "fi-conj-" + v
        elif mode == "G":
            args["2"], args["3"] = v.split("-")
        elif mode == "I":
            args["i"] = "0"
        elif mode == "E":
            args["e"] = "0"
        elif mode == "P":
            args["par_sg_a"] = v
        elif mode == "X":
            break
        elif mode is None:
            pass
        else:
            print("Unhandled mode in decode:", paradigm, mode)
            return None
        mode = ch

    # Save template name in args.
    args["template_name"] = name

    # Get the number of arguments for the declension/conjugation.
    if name.startswith("fi-decl"):
        decl = nounspecs.noun_decls.get(name)
    else:
        decl = verbspecs.verb_conjs.get(name)
    if decl is None:
        return None
    nargs = decl["nargs"]

    # Parse parts of the stem.
    parts = stem.split("|")
    end = ""
    if nargs == 3:
        if len(parts) != 3:
            return None
        stem, args["2"], ae = parts  # end_vowel
    elif nargs == 5:
        if len(parts) != 3:
            return None
        stem, args["4"], ae = parts  # end_part
    elif name in ILL_SG_DECLS:
        if len(parts) != 3:
            return None
        stem, vowels, ae = parts  # end_part
        if vowels:
            args["ill_sg_vowel"] = vowels[0]
        if len(vowels) > 1:
            args["ill_sg_vowel2"] = vowels[1]
    elif nargs <= 1:
        if len(parts) != 1:
            return None
        stem = parts[0]
        ae = "a"
    else:
        if len(parts) != 2:
            return None
        stem, ae = parts

    # ae should always be a/ä
    if ae not in "aä":
        return None

    # Save stem and final a/ä if the declension/conjugation has args.
    if nargs > 1:
        args["1"] = stem
        args[str(nargs)] = ae

    return args


def valid_unknown_stem(stem, paradigm):
    """Checks whether the given stem is valid for the paradigm.  This is
    intended for unknown paradigms, and may return False for some exceptional
    known words."""
    if paradigm is None:
        if stem is None:
            return False
        if len(stem) < 1:
            return False
        if stem.find(SEPARATOR) >= 0:
            return False
        return True

    # Try to decode the paradigm
    args = decode_paradigm(stem, paradigm)
    if args is None:
        return False

    # Get the declension/conjugation info
    name = args["template_name"]
    if paradigm.startswith("N"):
        decl = nounspecs.noun_decls[name]
    else:
        decl = verbspecs.verb_conjs[name]

    # If it is an internal one (i.e., not productive), don't use for unknown
    if decl.get("internal", False):
        return False  # This paradigm is not productive

    # Check if stem length meets minimum length for the declension
    min_stem_len = decl.get("min-stem-len", 0)
    if len(args.get("1", "")) < min_stem_len:
        return False  # Stem too short

    # If the declension takes no arguments, stem should be empty
    if decl.get("nargs", 0) == 0 and len(stem) > 0:
        return False  # Step specified when no args expected

    return True
