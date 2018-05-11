from unittest import TestCase

from firestick import NumberFromGermanMonth


class TestNumberFromGermanMonth(TestCase):
    def test_NumberFromGermanMonth(self):
        self.assertEqual(NumberFromGermanMonth("Januar"), 1)
