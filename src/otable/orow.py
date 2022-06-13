"""Table data types backed by objects."""

import collections.abc
from typing import Iterable, Sequence, TypeVar, cast, overload

T = TypeVar('T')


class ORow(collections.abc.MutableSequence[T]):
    """A sequence that exposes a set of attributes from objects as a sequence."""

    # The MutableSequence base class does two things, it provides type information about
    # the methods, and it provides implementations of most of the interface that depend
    # on the few methods implemented here.
    

    __slots__ = ('attributes', 'objects', 'names')

    attributes: list[str]
    objects: list[object]
    names: list[str]

    def __init__(
        self, names: Sequence[str], objects: Sequence[object], attributes: Sequence[str]
    ):
        """Initialize the object.

        :param names: The names of the values exposed in the row; normally singular.
        :param objects: The objects who's values are exposed.
        :param attributes: The attributes of the objects to expose.
        """
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
        """Insert new values.  Not supported!"""
        raise RuntimeError('inserts are not allowed')

    def __repr__(self) -> str:
        values = []
        for obj, attribute in zip(self.objects, self.attributes):
            values.append(getattr(obj, attribute))
        return repr(values)
