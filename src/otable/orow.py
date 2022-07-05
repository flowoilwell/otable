"""Table data types backed by objects."""

import collections.abc
from .ocolumn import OColumn
from typing import Any, Iterable, Sequence, TypeVar, cast, overload

T = TypeVar('T')


class ORow(collections.abc.MutableSequence[T]):
    """A sequence that exposes a set of attributes from objects as a sequence."""

    # The MutableSequence base class does two things, it provides type information about
    # the methods, and it provides implementations of most of the interface that depend
    # on the few methods implemented here.

    __slots__ = ('columns', 'objects')

    columns: Sequence[OColumn[Any]]
    objects: Sequence[object]

    def __init__(self, columns: Sequence[OColumn[Any]], objects: Sequence[object]):
        """Initialize the object.

        :param columns: The columns of the objects to expose.
        :param objects: The objects who's values are exposed.
        """
        self.columns = tuple(columns)
        self.objects = tuple(objects)

    @property
    def names(self) -> Sequence[str]:
        """Fetch the column names."""
        return tuple(column.name for column in self.columns)

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
            raise ValueError('slicing rows is not supported')
        assert isinstance(item, int)
        getter = self.columns[item].getter
        obj = self.objects[item]
        return cast(T, getter(obj))

    def __getattr__(self, name: str) -> T:
        if name in self.names:
            index = self.names.index(name)
            return self[index]
        raise AttributeError

    @overload
    def __setitem__(self, item: int, value: T) -> None:  # pragma: nocover
        ...

    @overload
    def __setitem__(self, item: slice, value: Iterable[T]) -> None:  # pragma: nocover
        ...

    # Implementation of above signatures.
    def __setitem__(self, index: int | slice, value: T | Iterable[T]) -> None:
        if isinstance(index, slice):
            raise ValueError('slicing rows is not supported')
        assert isinstance(index, int)

        obj = self.objects[index]
        setter = self.columns[index].setter
        setter(obj, value)

    @overload
    def __delitem__(self, index: int) -> None:  # pragma: nocover
        ...

    @overload
    def __delitem__(self, index: slice) -> None:  # pragma: nocover
        ...

    # Implementation of above signatures.
    def __delitem__(self, index: int | slice) -> None:
        raise RuntimeError('deleting from rows is not supported')

    def __len__(self) -> int:
        return len(self.objects)

    def insert(self, index: int, value: T) -> None:
        """Insert new values.  Not supported!"""
        raise RuntimeError('inserts are not allowed')

    def __repr__(self) -> str:
        values = []
        for obj, column in zip(self.objects, self.columns):
            values.append(column.getter(obj))
        return repr(values)
