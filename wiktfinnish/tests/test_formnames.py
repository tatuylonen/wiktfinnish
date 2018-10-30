import unittest
import wiktfinnish

class TestForms(unittest.TestCase):

    def test_comp_forms(self):
        lst = wiktfinnish.COMP_FORMS
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
        assert "" not in lst
        assert "nom-sg" in lst
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
            assert comp in wiktfinnish.COMP_FORMS
            if comp != "":
                num_comp += 1
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        assert cnt > 3000 and cnt < 9000
        assert num_comp > 0
        for form in wiktfinnish.all_forms_iter("adj", comparable=False):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp == ""
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        for form in wiktfinnish.all_forms_iter("adj", comparable=False,
                                               no_clitics=True):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp == ""
            assert case in wiktfinnish.CASE_FORMS
            assert poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic == ""
        num_comp = 0
        for form in wiktfinnish.all_forms_iter("adj", no_clitics=True):
            cnt += 1
            vform, comp, case, poss, clitic = form
            assert vform == ""
            assert comp in wiktfinnish.COMP_FORMS
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
            assert comp in wiktfinnish.COMP_FORMS
            if comp != "":
                num_comp += 1
            assert case == "" or case in wiktfinnish.CASE_FORMS
            assert poss == "" or poss in wiktfinnish.POSSESSIVE_FORMS
            assert clitic in wiktfinnish.CLITIC_FORMS
        print(cnt)
        assert cnt > 10000 and cnt < 17000
        assert num_comp > 0

    def test_iter_adv(self):
        cnt = 0
        num_comp = 0
        for form in wiktfinnish.all_forms_iter("adv"):
            cnt += 1
            vform, comp, case, poss, clitic = form
            print(form)
            assert vform == ""
            assert comp in wiktfinnish.COMP_FORMS
            if comp != "":
                num_comp += 1
            assert case == ""
            assert poss == ""
            assert clitic in wiktfinnish.CLITIC_FORMS
        print(cnt)
        assert cnt >= len(wiktfinnish.COMP_FORMS)
        assert cnt <= len(wiktfinnish.COMP_FORMS)*len(wiktfinnish.CLITIC_FORMS)
        assert num_comp > 1

    def test_iter_bogus(self):
        lst = list(wiktfinnish.all_forms_iter("bogus-nonex"))
        assert lst == [("", "", "", "", "")]

    def test_list_noun(self):
        x = list(wiktfinnish.all_forms_iter("verb"))
        y = wiktfinnish.all_forms_list("verb")
        assert list(sorted(x)) == list(sorted(y))
        x = list(wiktfinnish.all_forms_iter("adj", comparable=False))
        y = wiktfinnish.all_forms_list("adj", comparable=False)
        assert isinstance(y, (list, tuple))
        z = wiktfinnish.all_forms_list("adj")
        assert list(sorted(x)) == list(sorted(y))
        assert x != z
