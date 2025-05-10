"""Ordered set implementation."""

from __future__ import annotations

from typing import Dict, Iterable, Iterator, Optional, TypeVar

T = TypeVar("T")


class OrderedSet(Iterable[T]):
    """Set which maintains order of elements after insertion, explicit None is filtered."""

    def __init__(self, iterable: Iterable[T] = ()) -> None:  # type: ignore
        self._dict: Dict[T, None] = {key: None for key in iterable if key is not None}

    def __iter__(self) -> Iterator[T]:
        return (key for key in self._dict)

    def __contains__(self, element: T) -> bool:
        return element in self._dict

    def __len__(self) -> int:
        return len(self._dict)

    def __getitem__(self, position: int) -> T:
        return list(self._dict.keys())[position]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{[str(key) for key in self._dict.keys()]}"  # noqa: SIM118

    def __eq__(self, other: object) -> bool:
        if isinstance(other, list):
            return list(self._dict.keys()) == other
        assert isinstance(other, type(self))
        return self._dict.keys() == other._dict.keys()

    def __hash__(self) -> int:
        return hash(frozenset(self._dict.keys()))

    def add(self, item: Optional[T]) -> None:
        """Add item to set."""
        if item is not None:
            self._dict[item] = None

    def remove(self, item: T) -> None:
        """Remove item from set, ignore if not exists."""
        self._dict.pop(item, None)

    def union(self, other: OrderedSet) -> OrderedSet[T]:
        """Return union of two sets."""
        assert isinstance(other, type(self))
        new_dict = self._dict.copy()
        new_dict.update(other._dict)  # pylint:disable=protected-access # (ok within same class)  # noqa: SLF001
        return OrderedSet[T](new_dict)

    def difference(self, other: OrderedSet) -> OrderedSet[T]:
        """Return difference of two sets."""
        assert isinstance(other, type(self))
        result = OrderedSet[T](self._dict.copy())
        for item in other:
            result.remove(item)
        return result

    def intersection(self, other: OrderedSet) -> OrderedSet[T]:
        """Return intersection of two sets."""
        assert isinstance(other, type(self))
        result = {key: None for key in self._dict if key in other}
        return OrderedSet[T](result)
