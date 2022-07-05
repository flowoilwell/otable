"""Tests for OTable and related code."""

import unittest
from otable import OColumn, ORow, OTable


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


class TestORow(unittest.TestCase):
    """Tests for the ORow class."""

    def test_creation(self):
        """Creating an ORow instance works."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        ORow(columns, [dog, dog])

    def test_len(self):
        """The length of the row reflects the width of the table."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        table = OTable(columns)
        row = table[1]
        self.assertEqual(len(row), len(columns))

    def test_get_slice(self):
        """Reading a slice of a row is not supported."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        row = ORow(columns, [dog, dog])
        with self.assertRaisesRegex(ValueError, 'slicing rows is not supported'):
            row[1:2]

    def test_set_slice(self):
        """Writing a slice of a row is not supported."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        row = ORow(columns, [dog, dog])
        with self.assertRaisesRegex(ValueError, 'slicing rows is not supported'):
            row[1:2] = None

    def test_del(self):
        """Deleting a slice of a row is not supported."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        row = ORow(columns, [dog, dog])
        error = (RuntimeError, 'deleting from rows is not supported')
        with self.assertRaisesRegex(*error):
            del row[1:2]

    def test_bad_name(self):
        """Accessing an attribute that does not exist generates an AttributeError."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        row = ORow(columns, [dog, dog])
        with self.assertRaises(AttributeError):
            row.does_not_exist

    def test_insert(self):
        """Inserting into a row is not permitted."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        row = ORow(columns, [dog, dog])
        with self.assertRaisesRegex(RuntimeError, 'inserts are not allowed'):
            row.insert(0, 'Jennifer')
