"""Tests for OTable and related code."""

import unittest
from otable import OColumn


class Animal:
    """An animal with some number of legs."""

    def __init__(self, name: str, legs: int):
        """Initiate an instance.

        :param name: The animal's name.
        :param legs: How many legs the animal has.
        """
        self.name = name
        self.legs = legs


dog = Animal('Ralf', legs=4)
snake = Animal('Simon', legs=0)
cat = Animal('Tripod', legs=3)

animals = [dog, snake, cat]


class TestOColumn(unittest.TestCase):
    """Tests for the OColumn class."""

    def test_creation(self):
        """Creating an OColumn instance works."""
        OColumn([], 'attribute')

    def test_len(self):
        """The length of the column reflects the length of the underlying sequence."""
        names = OColumn('name', objects=animals)
        self.assertEqual(len(names), len(animals))

    def test_getting_slice(self):
        """The columns can be sliced and return new columns."""
        names = OColumn('name', objects=animals)
        sliced = names[:2]
        # The result is an OColumn.
        self.assertIsInstance(sliced, OColumn)
        # The result is a different instance than the original OColumn.
        self.assertIsNot(names, sliced)
        # The expected values are present.
        self.assertEqual(list(sliced), ['Ralf', 'Simon'])

    def test_setting_slice(self):
        """The columns can be assigned by a slice."""
        names = OColumn('name', objects=animals)
        names[:2] = ['Fred', 'Sam']
        # The expected values are present.
        self.assertEqual(list(names), ['Fred', 'Sam', 'Tripod'])

    def test_deleting_slice(self):
        """The columns can be deleted by a slice."""
        names = OColumn('name', objects=animals)
        del names[:2]
        # The expected values are present.
        self.assertEqual(list(names), ['Tripod'])
