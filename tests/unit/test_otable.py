import unittest
from otable import OColumn, OTable


class Animal:
    """An animal with some number of legs."""

    def __init__(self, name: str, legs: int):
        self.name = name
        self.legs = legs


dog = Animal('Ralf', legs=4)
snake = Animal('Simon', legs=0)
cat = Animal('Tripod', legs=3)

animals = [dog, snake, cat]


class TestOColumn(unittest.TestCase):
    """Tests for the OColumn class."""

    def test_creation(self):
        """ "Creating an OColumn instance works."""
        OColumn([], 'attribute')

    def test_len(self):
        """The length of the column reflects the length of the underlying sequence."""
        names = OColumn('name', objects=animals)
        self.assertEqual(len(names), len(animals))


class TestOTable(unittest.TestCase):
    """Tests for the OTable class."""

    def test_creation(self):
        """Creating an OTable instance works."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        OTable(columns)

    def test_len(self):
        """The length of the column reflects the length of the underlying sequence."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        table = OTable(columns)
        self.assertEqual(len(table), len(animals))
