# from django.test import TestCase
import unittest
import unittest.mock as mock

import markovify

from .models import Sentence as Sen
from betterbot.settings import TEXT_MODEL_JSON_FILE


@unittest.skip('blocked')
class SentenceTestCase(unittest.TestCase):
    """
    can't create test db, old migration that was run with --fake
    (corpus 0004_auto_20161214_1203) seems to be blocking it
    """
    def test_load_reconstituted_text_model(self):
        reconstituted_model = markovify.Text.from_json(TEXT_MODEL_JSON_FILE)
        self.assertTrue(reconstituted_model)

    def test_create_method(self):
        s = Sen.create()
        self.assertTrue(s)
