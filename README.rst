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

    from dataclasses import dataclass
    from otable import OColumn

    @dataclass
    class Animal:
        """An animal with some number of legs."""

        name: str
        legs: int

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


Names and attributes
--------------------

Lets say we have objects that represent an animal's human friend.

.. code:: python

    @dataclass
    class HumanFriend:
        """An animal's human friend."""

        name: str

Instances of ``HumanFriend`` have an attribute ``name``, but for the column name we
might want to use "friend" instead of "name" which has already been used to name another
column.  In that case, we can specify an ``attribute`` when constructing the column
which will be read.

.. code:: python

    alice = HumanFriend('Alice')
    bob = HumanFriend('Bob')

    friends = OColumn('friend', [alice, bob, alice], attribute='name')

    table = OTable(columns=(names, legs, friends))

The table reflects the ``name`` of each columns (not the ``attribute``).

>>> table.column_names()
['name', 'legs', 'friend']


Table rendering
---------------

Tables provide a nice ``__repr__`` for displaying themselves.

>>> table
┌────────┬──────┬────────┐
│ name   │ legs │ friend │
╞════════╪══════╪════════╡
│ Ralf   │ 4    │ Alice  │
├────────┼──────┼────────┤
│ Simon  │ 0    │ Bob    │
├────────┼──────┼────────┤
│ Tripod │ 3    │ Alice  │
└────────┴──────┴────────┘


Accessing values
-----------------

Values in tables can be accessed as column indexes.

>>> row = table[1]
>>> row[2]
'Bob'

The values can also be accessed by name.

>>> row.friend
'Bob'


Mutating tables
---------------

Values in tables can be changed (and they change the values in the constituent columns
which change the values in the underlying objects).

Note how changing one row can affect other rows because the underlying objects are
mutated.

>>> table
┌────────┬──────┬────────┐
│ name   │ legs │ friend │
╞════════╪══════╪════════╡
│ Ralf   │ 4    │ Alice  │
├────────┼──────┼────────┤
│ Simon  │ 0    │ Bob    │
├────────┼──────┼────────┤
│ Tripod │ 3    │ Alice  │
└────────┴──────┴────────┘
>>> table[2][2] = 'Charlie'
>>> table
┌────────┬──────┬─────────┐
│ name   │ legs │ friend  │
╞════════╪══════╪═════════╡
│ Ralf   │ 4    │ Charlie │
├────────┼──────┼─────────┤
│ Simon  │ 0    │ Bob     │
├────────┼──────┼─────────┤
│ Tripod │ 3    │ Charlie │
└────────┴──────┴─────────┘
