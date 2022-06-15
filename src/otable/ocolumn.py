"""Table data types backed by objects."""

import collections.abc
from typing import Iterable, Sequence, TypeVar, cast, overload

T = TypeVar('T')


class OColumn(collections.abc.MutableSequence[T]):
    """A sequence that exposes an attribute from a sequence of objects."""

    # The MutableSequence base class does two things, it provides type information about
    # the methods, and it provides implementations of most of the interface that depend
    # on the few methods implemented here.

    __slots__ = ('attribute', 'objects', 'name')

    attribute: str
    objects: list[object]
    name: str

    def __init__(
        self, name: str, objects: Sequence[object], attribute: str | None = None
    ):
        """Initialize the object.

        :param name: The name of the value exposed in the column; normally singular.
        :param objects: The objects whos values are exposed.
        :param attribute: The attribute of the objects that contain the values to expose
            in the column.  If not provided, the value of "name" is used.
        """
        self.name = name
        self.objects = list(objects)
        if attribute is None:
            self.attribute = name
        else:
            self.attribute = attribute

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
    def __delitem__(self, index: int) -> None:  # pragma: nocover
        ...

    @overload
    def __delitem__(self, index: slice) -> None:  # pragma: nocover
        ...

    # Implementation of above signatures.
    def __delitem__(self, index: int | slice) -> None:
        self.objects.__delitem__(index)

    def __len__(self) -> int:
        return len(self.objects)

    def insert(self, index: int, value: T) -> None:
        """Insert new values.  Not supported!"""
        raise RuntimeError('inserts are not allowed')
