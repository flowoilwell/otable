"""Table data types backed by objects."""

import collections.abc
import termtables
from typing import Any, Sequence


class OColumn(collections.abc.MutableSequence[Any]):
    """A sequence that exposes an attribute from a sequence of objects."""

    __slots__ = ('attribute', 'objects')

    attribute: str
    objects: list[object]

    def __init__(self, attribute: str, objects: list[object]):
        self.objects = objects
        self.attribute = attribute

    def __getitem__(self, item: Any) -> Any:
        return getattr(self.objects[item], self.attribute)

    def __setitem__(self, index: Any, value: Any) -> None:
        setattr(self.objects[index], self.attribute, value)

    def __delitem__(self, index: Any) -> None:
        del self.objects[index]

    def __len__(self) -> int:
        return len(self.objects)

    def insert(self, index: Any, value: Any) -> None:
        raise RuntimeError('inserts are not allowed')


class OTable(collections.abc.Sequence[Any]):
    """A collection of columns backed by objects but accessable as a list of lists."""

    __slots__ = ('columns', 'columns_by_name')

    def __init__(self, columns: Sequence[OColumn]):
        assert len(columns) > 0, 'at least one column required'
        self.columns = columns
        self.columns_by_name = dict((column.attribute, column) for column in columns)

    def __getitem__(self, item: Any) -> Any:
        """Fetch a row of data by index."""
        row = []
        for column in self.columns:
            row.append(column[item])
        return row

    def __len__(self) -> int:
        return len(self.columns[0])

    def column_names(self) -> list[str]:
        """The names of the columns in table order."""
        return list(self.columns_by_name.keys())

    def __repr__(self) -> str:
        return str(termtables.to_string(self, header=self.column_names()))
