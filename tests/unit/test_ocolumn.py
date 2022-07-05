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


class TestOColumn(unittest.TestCase):
    """Tests for the OColumn class."""

    def setUp(self):  # noqa: D102 (Missing docstring in public method)
        dog = Animal('Ralf', legs=4)
        snake = Animal('Simon', legs=0)
        cat = Animal('Tripod', legs=3)

        self.animals = [dog, snake, cat]

    def test_creation(self):
        """Creating an OColumn instance works."""
        OColumn('attribute', [])

    def test_len(self):
        """The length of the column reflects the length of the underlying sequence."""
        names = OColumn('name', objects=self.animals)
        self.assertEqual(len(names), len(self.animals))

    def test_getting_slice(self):
        """The columns can be sliced and return new columns."""
        names = OColumn('name', objects=self.animals)
        sliced = names[:2]
        # The result is an OColumn.
        self.assertIsInstance(sliced, OColumn)
        # The result is a different instance than the original OColumn.
        self.assertIsNot(names, sliced)
        # The expected values are present.
        self.assertEqual(list(sliced), ['Ralf', 'Simon'])

    def test_setting_slice(self):
        """The columns can be assigned by a slice."""
        names = OColumn('name', objects=self.animals)
        names[:2] = ['Fred', 'Sam']
        # The expected values are present.
        self.assertEqual(list(names), ['Fred', 'Sam', 'Tripod'])

    def test_deleting_slice(self):
        """The columns can be deleted by a slice."""
        names = OColumn('name', objects=self.animals)
        del names[:2]
        # The expected values are present.
        self.assertEqual(list(names), ['Tripod'])

    def test_slice_with_start_index(self):
        """Columns can be sliced with just a start index."""
        names = OColumn('name', objects=self.animals)
        self.assertEqual(list(names[1:]), ['Simon', 'Tripod'])

    def test_slice_with_stop_index(self):
        """Columns can be sliced with just a stop index."""
        names = OColumn('name', objects=self.animals)
        self.assertEqual(list(names[:1]), ['Ralf'])

    def test_slice_with_step(self):
        """Columns can be sliced with a step."""
        names = OColumn('name', objects=self.animals)
        self.assertEqual(list(names[::2]), ['Ralf', 'Tripod'])

    def test_assign_slice_with_step(self):
        """Columns can be assigned with a step."""
        names = OColumn('name', objects=self.animals)
        names[::2] = ['Joe', 'Trip']
        self.assertEqual(list(names), ['Joe', 'Simon', 'Trip'])

    def test_assign_mismatched_slice(self):
        """A value assigned to a slice must have the same cardinality as the slice."""
        names = OColumn('name', objects=self.animals)
        with self.assertRaisesRegex(ValueError, 'cardinality mismatch'):
            names[1:2] = ['Joe', 'Trip']

    def test_insert(self):
        """Inserting into a column is not permitted."""
        names = OColumn('name', objects=self.animals)
        with self.assertRaisesRegex(RuntimeError, 'inserts are not allowed'):
            names.insert(0, 'Jennifer')
