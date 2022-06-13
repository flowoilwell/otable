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
        ORow(['name', 'legs'], [dog, dog], ['name', 'legs'])

    def test_len(self):
        """The length of the row reflects the width of the table."""
        columns = [OColumn('name', objects=animals), OColumn('legs', objects=animals)]
        table = OTable(columns)
        row = table[1]
        self.assertEqual(len(row), len(columns))
