# Tests for grammatical form names.
#
# Copyright (c) 2018 Tatu Ylonen.  See https://ylonen.org

import unittest
import wiktfinnish

class TestDecode(unittest.TestCase):

    def test_comp_forms(self):
        lst = wiktfinnish.COMPARATIVE_FORMS
        assert isinstance(lst, (list, tuple, set))
        for x in lst:
            assert isinstance(x, str)
        assert "" in lst
        assert "comp" in lst
        assert "sup" in lst

    def test_case_forms(self):
        lst = wiktfinnish.CASE_FORMS
        assert isinstance(lst, (list, tuple, set))
        for x in lst:
            assert isinstance(x, str)
        assert "" in lst
        assert "nom-pl" in lst
        assert "ill-pl" in lst
        assert "acc-sg" in lst
        assert "acc-pl" in lst

    def test_poss_forms(self):
        lst = wiktfinnish.POSSESSIVE_FORMS
        assert isinstance(lst, (list, tuple, set))
        for x in lst:
            assert isinstance(x, str)
        assert "" in lst
        assert "1s" in lst
        assert "2p" in lst
        assert "3x" in lst
        assert "3p" not in lst

    def test_clitic_forms(self):
        lst = wiktfinnish.CLITIC_FORMS
        assert isinstance(lst, (list, tuple, set))
        for x in lst:
            assert isinstance(x, str)
        assert "" in lst
        assert "kO" in lst
        assert "pAhAn" in lst

    def test_clitic_forms(self):
        lst = wiktfinnish.VERB_FORMS
        assert isinstance(lst, (list, tuple, set))
        for x in lst:
            assert isinstance(x, str)
        assert "" in lst
        assert "pres-1sg" in lst
        assert "past-part" in lst

    def test_iter_noun(self):
        cnt = 0
        for form in wiktfinnish.all_forms_iter("noun"):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp == ""
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        assert cnt > 1000 and cnt < 3000

    def test_iter_adj(self):
        cnt = 0
        num_comp = 0
        for form in wiktfinnish.all_forms_iter("adj"):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp in wiktfinnish.COMPARATIVE_FORMS
            if comp != "":
                num_comp += 1
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        assert cnt > 3000 and cnt < 9000
        assert num_comp > 0
        for form in wiktfinnish.all_forms_iter("adj", no_comp=True):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp == ""
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        for form in wiktfinnish.all_forms_iter("adj", no_comp=True,
                                               no_clitic=True):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp == ""
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic == ""
        num_comp = 0
        for form in wiktfinnish.all_forms_iter("adj", no_clitic=True):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp in wiktfinnish.COMPARATIVE_FORMS
            if comp != "":
                num_comp += 1
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic == ""
        assert num_comp > 0

    def test_iter_verb(self):
        cnt = 0
        num_comp = 0
        for form in wiktfinnish.all_forms_iter("verb"):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform != "" and vform in wiktfinnish.VERB_FORMS
            assert comp in wiktfinnish.COMPARATIVE_FORMS
            if comp != "":
                num_comp += 1
            assert case == "" or case in wiktfinnish.CASE_FORMS
            assert poss == "" or poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        assert cnt > 10000 and cnt < 50000
        assert num_comp > 0

    def test_iter_adv(self):
        cnt = 0
        num_comp = 0
        for form in wiktfinnish.all_forms_iter("adv"):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp in wiktfinnish.COMPARATIVE_FORMS
            if comp != "":
                num_comp += 1
            assert case == ""
            assert poss == ""
            assert clitic in wiktfinnish.CLITIC_FORMS
        assert cnt >= len(wiktfinnish.COMPARATIVE_FORMS)
        assert cnt <= (len(wiktfinnish.COMPARATIVE_FORMS) *
                       len(wiktfinnish.CLITIC_FORMS))
        assert num_comp > 1

    def test_iter_bogus(self):
        lst = list(wiktfinnish.all_forms_iter("bogus-nonex"))
        assert lst == [("", "", "", "", "")]

    def test_list_verb(self):
        x = list(wiktfinnish.all_forms_iter("verb"))
        xx = wiktfinnish.all_forms_list("verb")
        assert list(sorted(x)) == list(sorted(xx))
        y = wiktfinnish.all_forms_list("verb", no_comp=True)
        assert len(x) > len(y)
        for form in y:
            assert form in x
        y = wiktfinnish.all_forms_list("verb", no_case=True)
        assert len(x) > len(y)
        for form in y:
            assert form in x
        y = wiktfinnish.all_forms_list("verb", no_poss=True)
        assert len(x) > len(y)
        # In this case, some of the forms may not be in x
        y = wiktfinnish.all_forms_list("verb", no_clitic=True)
        assert len(x) > len(y)
        for form in y:
            assert form in x

    def test_list_adj(self):
        x = wiktfinnish.all_forms_list("adj")
        assert isinstance(x, (list, tuple))
        y = wiktfinnish.all_forms_list("adj", no_comp=True)
        assert isinstance(y, (list, tuple))
        assert len(x) > len(y)
        for form in y:
            assert form in x
        z = wiktfinnish.all_forms_list("adj", no_comp=True, no_case=True)
        assert len(y) > len(z)
        for form in z:
            assert form in y

    def test_list_noun(self):
        x = wiktfinnish.all_forms_list("noun")
        y = wiktfinnish.all_forms_list("noun", no_case=True)
        assert len(x) > len(y)
        for form in y:
            assert form in x
        z = wiktfinnish.all_forms_list("noun", no_case=True, no_poss=True)
        assert len(y) > len(z)
        for form in z:
            assert form in y
