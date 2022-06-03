==================
OTable and OColumn
==================

An OTable is an ordered set of OColumns.

An OColumn is a sequence of objects (hence the "O" in "OColumn") with one of their
attributes exposed as if that attribute were a value in a sequence.  For example, we
might have parallel lists of animal names and their respective number of legs.

.. code:: python

    names = ['Ralf', 'Simon', 'Tripod']
    legs = [4, 0, 3]

If we instead wanted an API similar to normal Python lists, but with objects backing the
values, we can do that with OColumns.

.. code:: python

    from otable import OColumn

    class Animal:
        """An animal with some number of legs."""

        def __init__(self, name: str, legs: int):
            self.name = name
            self.legs = legs

    dog = Animal(name='Ralf', legs=4)
    snake = Animal(name='Simon Snakerson', legs=0)
    cat = Animal(name='Tripod', legs=3)

    animals = [dog, snake, cat]

    names = OColumn('name', animals)
    legs = OColumn('legs', animals)

Now we can access the attributes as if they were simple values in lists.

    >>> names[1]
    'Simon Snakerson'
    >>> legs[1]
    0

Any modifications to the values in the columns are passed on to the underlying objects.

    >>> names[1] = 'Simon'
    >>> names[1]
    'Simon'
    >>> snake.name
    'Simon'


OTable
======

Columns are great, but most use cases call for many parallel columns.  In those cases
multiple OColumns can be tied together as an OTable.

The easiest way to build an OTable is to pass it a sequence of OColumns.

.. code:: python

    from otable import OTable

    table = OTable(columns=(names, legs))

Now that we have our table, we can interrogate it.  Indexing a table returns a row.

    >>> table[0]
    ['Ralf', 4]

Iterating over a table gives us the rows.

    >>> list(table)
    [['Ralf', 4], ['Simon', 0], ['Tripod', 3]]

Column names can also be retrieved.

    >>> table.column_names()
    ['name', 'legs']

Tables provide a nice ``__repr__`` for displaying themselves.

    >>> table
    ┌────────┬──────┐
    │ name   │ legs │
    ╞════════╪══════╡
    │ Ralf   │ 4    │
    ├────────┼──────┤
    │ Simon  │ 0    │
    ├────────┼──────┤
    │ Tripod │ 3    │
    └────────┴──────┘
