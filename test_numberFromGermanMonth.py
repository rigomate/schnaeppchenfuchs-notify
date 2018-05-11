from unittest import TestCase

from germanMonth import NumberFromGermanMonth


class TestNumberFromGermanMonth(TestCase):
    def test_NumberFromGermanMonth(self):
        self.assertEqual(NumberFromGermanMonth("Januar"), 1)
