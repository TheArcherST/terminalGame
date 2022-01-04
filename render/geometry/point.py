from typing import Union, overload, Iterable, Iterator, TypeVar
from copy import copy

T = TypeVar('T')

number_alias = Union[int, float]
point_able = Iterable[number_alias]


class BasePoint:
    """
    Coordinates object
    """

    @overload
    def __init__(self, obj: point_able):
        pass

    @overload
    def __init__(self, x: number_alias, y: number_alias):
        pass

    def __init__(self,
                 x: number_alias = None,
                 y: number_alias = None,
                 obj: point_able = None):

        if obj is not None:
            x, y = obj

        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[number_alias]:
        return iter((self.x, self.y))

    def __sub__(self: T, other: Union[point_able]) -> T:
        result = copy(self)

        other_x, other_y = other

        result.x -= other_x
        result.y -= other_y

        return result

    def __add__(self: T, other: Union[point_able]) -> T:
        result = copy(self)

        other_x, other_y = other

        result.x += other_x
        result.y += other_y

        return result

    def __mul__(self: T, other: number_alias) -> T:
        result = copy(self)

        result.x *= other
        result.y *= other

        return result

    def __str__(self):
        return f'({self.x}, {self.y})'

    __repr__ = __str__
