"""Table data types backed by objects."""

import collections.abc
import termtables
from typing import Iterable, Sequence, TypeVar, cast, overload

T = TypeVar('T')


class OColumn(collections.abc.MutableSequence[T]):
    """A sequence that exposes an attribute from a sequence of objects."""

    __slots__ = ('attribute', 'objects', 'name')

    attribute: str
    objects: list[object]
    name: str

    def __init__(self, name: str, objects: list[object], attribute: str | None = None):
        self.name = name
        self.objects = objects[:]
        if attribute is None:
            self.attribute = name
        else:
            self.attribute = attribute

    @overload
    def __getitem__(self, item: int) -> T:  # pragma: nocover
        ...

    @overload
    def __getitem__(self, item: slice) -> collections.abc.MutableSequence[T]:  # pragma: nocover
        ...

    # Implementation of above signatures.
    def __getitem__(self, item: int | slice) -> T | Sequence[T]:
        if isinstance(item, slice):
            return OColumn(
                name=self.name,
                objects=self.objects.__getitem__(item),
                attribute=self.attribute,
            )
        result: T | Sequence[T] = getattr(self.objects[item], self.attribute)
        return result

    @overload
    def __setitem__(self, item: int, value: T) -> None:  # pragma: nocover
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:  # pragma: nocover
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


class ORow(collections.abc.MutableSequence[T]):
    """A sequence that exposes a set of attributes from objects as a sequence."""

    __slots__ = ('attributes', 'objects', 'names')

    attributes: list[str]
    objects: list[object]
    names: list[str]

    def __init__(
        self, names: Sequence[str], objects: Sequence[object], attributes: Sequence[str]
    ):
        self.names = list(names)
        self.objects = list(objects)
        self.attributes = list(attributes)

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> collections.abc.MutableSequence[T]:
        ...

    # Implementation of above signatures.
    def __getitem__(self, item: int | slice) -> T | Sequence[T]:
        if isinstance(item, slice):
            raise ValueError('slicing rows is not supported')
        assert isinstance(item, int)
        return cast(T, getattr(self.objects[item], self.attributes[item]))

    def __getattr__(self, name: str) -> T:
        if name in self.names:
            index = self.names.index(name)
            return cast(T, getattr(self.objects[index], self.attributes[index]))
        raise AttributeError

    @overload
    def __setitem__(self, item: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:
        ...

    # Implementation of above signatures.
    def __setitem__(self, index: int | slice, value: T | Iterable[T]) -> None:
        if isinstance(index, slice):
            raise ValueError('slicing rows is not supported')
        assert isinstance(index, int)

        setattr(self.objects[index], self.attributes[index], value)

    @overload
    def __delitem__(self, index: int) -> None:
        ...

    @overload
    def __delitem__(self, index: slice) -> None:
        ...

    # Implementation of above signatures.
    def __delitem__(self, index: int | slice) -> None:
        raise ValueError('deleting items from rows is not supported')

    def __len__(self) -> int:
        return len(self.objects)

    def insert(self, index: int, value: T) -> None:
        raise RuntimeError('inserts are not allowed')

    def __repr__(self) -> str:
        values = []
        for obj, attribute in zip(self.objects, self.attributes):
            values.append(getattr(obj, attribute))
        return repr(values)


class OTable(collections.abc.Sequence[T]):
    """A collection of columns backed by objects but accessible as a list of lists."""

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
        objects = [column.objects[item] for column in self.columns]
        names = [column.name for column in self.columns]
        attributes = [column.attribute for column in self.columns]
        return ORow(names, objects, attributes)

    def __len__(self) -> int:
        return len(self.columns[0])

    def column_names(self) -> list[str]:
        """The names of the columns in table order."""
        return list(column.name for column in self.columns)

    def __repr__(self) -> str:
        return str(termtables.to_string(list(self), header=self.column_names()))
