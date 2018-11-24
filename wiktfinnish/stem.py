# Encoding and decoding declensions and conjugations into a string.
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

from wiktfinnish.inflect import word_to_aae


def encode_paradigm(args):
    """Encodes conjugation/declination into a stem and a string.  Returns
    (None, None) for exception templates that can't be encoded; otherwise
    returns (stem, coding)."""
    assert "template_name" in args

    name = args["template_name"]
    if name in ("fi-decl", "fi-conj", "fi-conj-table"):
        return None, None

    i0 = args.get("i", "1") == "0"
    e0 = args.get("e", "1") == "0"
    par_sg_a = args.get("par_sg_a", "")
    ill_sg_vowel = args.get("ill_sg_vowel", "")
    ill_sg_vowel2 = args.get("ill_sg_vowel2", "")
    stem = args.get("1", "")

    if (args.get("4") or args.get("5")) and name != "fi-conj-kumajaa":
        arg2 = args.get("2", "")
        arg3 = args.get("3", "")
        if arg3 == "(')" or arg3 == "'":
            arg3 = ""
        elif arg3 == "’":
            arg3 = ""
        if arg2 == "’":
            arg2 = "'"
        while arg2 and arg3 and arg2[0] == arg3[0]:
            stem += arg2[0]
            arg2 = arg2[1:]
            arg3 = arg3[1:]
        gradation = "{}-{}".format(arg2, arg3)
    else:
        gradation = ""

    end_vowel = ""
    if name.endswith("-dot"):
        end_vowel = args.get("2", "")

    end_part = None
    if "5" in args and name != "fi-conj-kumajaa":
        end_part = args.get("4", "")
        ae = args.get("5", "")
    elif "4" in args:
        ae = args.get("4", "")
    elif "3" in args:
        ae = args.get("3", "")
    else:
        ae = args.get("2", "")
    if not stem:
        ae = ""
    else:
        aeref = word_to_aae(stem + (end_part or ""))
        if ae == aeref:
            ae = ""

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
    if ill_sg_vowel:
        parts.append("J" + ill_sg_vowel)
    if ill_sg_vowel2:
        parts.append("K" + ill_sg_vowel2)
    if end_vowel:
        parts.append("F" + end_vowel)
    if end_part is not None:
        parts.append("H" + end_part)
    if ae:
        parts.append("A" + ae)

    return stem, "".join(parts)


def decode_paradigm(stem, coding, pos=None):
    """Decodes stem and encoded conjugation/declension into arguments
    for generating word forms."""
    mode = None
    part = []
    args = {}
    ae = None
    if stem:
        args["1"] = stem
    if pos:
        args["pos"] = pos
    for ch in coding + "X":
        if not ch.isupper():
            part.append(ch)
            continue
        v = "".join(part)
        part = []
        if mode == "N":
            args["template_name"] = "fi-decl-" + v
        elif mode == "V":
            args["template_name"] = "fi-conj-" + v
        elif mode == "G":
            args["2"], args["3"] = v.split("-")
        elif mode == "I":
            args["i"] = "0"
        elif mode == "E":
            args["e"] = "0"
        elif mode == "P":
            args["par_sg_a"] = v
        elif mode == "J":
            args["ill_sg_vowel"] = v
        elif mode == "K":
            args["ill_sg_vowel2"] = v
        elif mode == "F":
            assert args["template_name"].endswith("-dot")
            args["2"] = v
        elif mode == "H":
            args["4"] = v
        elif mode == "A":
            ae = v
        elif mode == "X":
            break
        elif mode is None:
            pass
        else:
            print("Unhandled mode in decode:", s, mode)
            assert False
        mode = ch

    if args.get("1"):
        if not ae:
            ae = word_to_aae(args.get("1", "") + args.get("4", ""))
        if "4" in args:
            args["5"] = ae
        elif "3" in args:
            args["4"] = ae
        elif "2" in args:
            args["3"] = ae
        elif "2" not in args:
            args["2"] = ae

    return args
