# Tests for miscellaneous functions related to Finnish inflection
#
# Copyright (c) 2018 Tatu Ylonen.  See LICENSE and https://ylonen.org

import unittest
from wiktfinnish import inflect, add_clitic, last_char_to_vowel, word_to_aae

class MiscTests(unittest.TestCase):

    def test_clitic(self):
        self.assertEqual(add_clitic(["talo"], "__dummy__"),
                         ["talo"])
        self.assertEqual(add_clitic(["talo"], "kin"),
                         ["talokin"])
        self.assertEqual(add_clitic(["talo"], "kAAn"),
                         ["talokaan"])
        self.assertEqual(add_clitic(["talo"], "kAAn"),
                         ["talokaan"])
        self.assertEqual(add_clitic(["talo"], "kAAn"),
                         ["talokaan"])
        self.assertEqual(add_clitic(["yö"], "kAAn"),
                         ["yökään"])

    def test_vowel(self):
        self.assertEqual(last_char_to_vowel("SAK"), "o")
        self.assertEqual(last_char_to_vowel("SIA"), "a")
        self.assertEqual(last_char_to_vowel("YK"), "o")
        self.assertEqual(last_char_to_vowel("ky"), "y")
        self.assertEqual(last_char_to_vowel("LOB"), "e")
        self.assertEqual(last_char_to_vowel("MQ"), "u")

    def test_aae(self):
        self.assertEqual(word_to_aae("talo"), "a")
        self.assertEqual(word_to_aae("TALO"), "a")
        self.assertEqual(word_to_aae("yö"), "ä")
        self.assertEqual(word_to_aae("YÖ"), "ä")
        self.assertEqual(word_to_aae("olympia"), "a")
        self.assertEqual(word_to_aae("talviyö"), "ä")
        self.assertEqual(word_to_aae("tiili"), "ä")
        self.assertEqual(word_to_aae("veli"), "ä")
