"""Table data types backed by objects."""

import collections.abc
import termtables
from typing import Iterable, Sequence, TypeVar, cast, overload

T = TypeVar('T')


class OColumn(collections.abc.MutableSequence[T]):
    """A sequence that exposes an attribute from a sequence of objects."""

    __slots__ = ('attribute', 'objects')

    attribute: str
    objects: list[object]

    def __init__(self, attribute: str, objects: list[object]):
        self.objects = objects[:]
        self.attribute = attribute

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> collections.abc.MutableSequence[T]:
        ...

    # Implementation of above signatures.
    def __getitem__(self, item: int | slice) -> T | Sequence[T]:
        if isinstance(item, slice):
            return OColumn(
                attribute=self.attribute,
                objects=self.objects.__getitem__(item),
            )
        result: T | Sequence[T] = getattr(self.objects[item], self.attribute)
        return result

    @overload
    def __setitem__(self, item: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:
        ...

    # Implementation of above signatures.
    def __setitem__(self, index: int | slice, value: T | Iterable[T]) -> None:
        if isinstance(index, int):
            index = slice(index, index + 1)
            value = [cast(T, value)]
        else:
            value = list(cast(Iterable[T], value))

        assert isinstance(index, slice)
        if index.start is None:
            start = 0
        else:
            start = index.start

        if index.stop is None:
            stop = len(self)
        else:
            stop = index.stop

        if index.step is None:
            step = 1
        else:
            step = index.step

        if len(value) != len(range(start, stop, step)):
            # The number of items being set must match the number of items in the slice.
            raise ValueError('cardinality mismatch')

        for item_index, item_value in zip(range(start, stop, step), value):
            setattr(self.objects[item_index], self.attribute, item_value)

    @overload
    def __delitem__(self, index: int) -> None:
        ...

    @overload
    def __delitem__(self, index: slice) -> None:
        ...

    # Implementation of above signatures.
    def __delitem__(self, index: int | slice) -> None:
        self.objects.__delitem__(index)

    def __len__(self) -> int:
        return len(self.objects)

    def insert(self, index: int, value: T) -> None:
        raise RuntimeError('inserts are not allowed')


class OTable(collections.abc.Sequence[T]):
    """A collection of columns backed by objects but accessable as a list of lists."""

    __slots__ = ('columns',)

    columns: Sequence[OColumn[T]]

    def __init__(self, columns: Sequence[OColumn[T]]):
        assert len(columns) > 0, 'at least one column required'
        self.columns = columns[:]

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> collections.abc.MutableSequence[T]:
        ...

    # Implementation of above signatures.
    def __getitem__(self, item: int | slice) -> T | Sequence[T]:
        if isinstance(item, slice):
            raise ValueError('slicing tables is not supported')
        return [column[item] for column in self.columns]

    def __len__(self) -> int:
        return len(self.columns[0])

    def column_names(self) -> list[str]:
        """The names of the columns in table order."""
        return list(column.attribute for column in self.columns)

    def __repr__(self) -> str:
        return str(termtables.to_string(self, header=self.column_names()))
