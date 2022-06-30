"""Table data types backed by objects."""

import collections.abc
import termtables
from .ocolumn import OColumn
from .orow import ORow
from typing import Sequence, TypeVar, overload

T = TypeVar('T')


class OTable(collections.abc.Sequence[T]):
    """A collection of columns backed by objects but accessible as a list of lists."""

    # The Sequence base class does two things, it provides type information about the
    # methods, and it provides implementations of most of the interface that depend on
    # the few methods implemented here.

    __slots__ = ('columns',)

    columns: Sequence[OColumn[T]]

    def __init__(self, columns: Sequence[OColumn[T]]):
        """Initialize the object.

        :param columns: The columns that comprise the table.
        """
        assert len(columns) > 0, 'at least one column required'
        self.columns = columns[:]

    @overload
    def __getitem__(self, item: int) -> T:  # pragma: nocover
        ...

    @overload
    def __getitem__(
        self, item: slice
    ) -> collections.abc.MutableSequence[T]:  # pragma: nocover
        ...

    # Implementation of above signatures.
    def __getitem__(self, item: int | slice) -> T | Sequence[T]:
        if isinstance(item, slice):
            raise ValueError('slicing tables is not supported')
        objects = [column.objects[item] for column in self.columns]
        return ORow(self.columns, objects)

    def __len__(self) -> int:
        return len(self.columns[0])

    def column_names(self) -> list[str]:
        """Return the names of the columns in table order."""
        return list(column.name for column in self.columns)

    def __repr__(self) -> str:
        return str(termtables.to_string(list(self), header=self.column_names()))
