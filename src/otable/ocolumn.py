"""Table data types backed by objects."""

import collections.abc
from operator import attrgetter
from typing import Any, Callable, Iterable, Sequence, TypeVar, cast, overload


def attrsetter(name: str) -> Callable[[Any, Any], None]:
    """Create an attribute setter; analogous to operator.attrgetter."""

    def setter(obj: Any, value: Any) -> None:
        setattr(obj, name, value)

    return setter


T = TypeVar('T')


class OColumn(collections.abc.MutableSequence[T]):
    """A sequence that exposes an attribute from a sequence of objects."""

    # The MutableSequence base class does two things, it provides type information about
    # the methods, and it provides implementations of most of the interface that depend
    # on the few methods implemented here.

    # pylint: disable=assigning-non-slot

    # The above is because pylint erroneously reports that the "getter" and "setter"
    # attributes are not listed in the __slots__ definition below, but that's not true.

    __slots__ = ('name', 'objects', 'getter', 'setter')

    objects: list[T]
    name: str

    def __init__(
        self,
        name: str,
        objects: Sequence[T],
        attribute: str | None = None,
        getter: Callable[[T], Any] | None = None,
        setter: Callable[[T, Any], None] | None = None,
    ):
        """Initialize the object.

        :param name: The name of the value exposed in the column; normally singular.
        :param objects: The objects whos values are exposed.
        :param attribute: The attribute of the objects that contain the values to expose
            in the column.  If not provided, the value of "name" is used.
        :param getter: a function that will extract the column value from an object
        :param setter: a function that will impute a column value into an object
        """
        self.name = name
        self.objects = list(objects)
        if attribute is not None:
            attribute_name = attribute
        else:
            attribute_name = name

        if getter is not None:
            self.getter = getter
        else:
            self.getter = attrgetter(attribute_name)

        if setter is not None:
            self.setter = setter
        else:
            self.setter = attrsetter(attribute_name)

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
                getter=self.getter,
                setter=self.setter,
            )
        result: T | Sequence[T] = self.getter(self.objects[item])
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
            self.setter(self.objects[item_index], item_value)

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
