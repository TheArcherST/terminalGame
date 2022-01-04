from typing import Union, overload, TypeVar

from render.geometry.point import BasePoint, point_able, number_alias
from render.geometry.coordinates import Coordinates


T = TypeVar('T')


class Vector(BasePoint):
    @overload
    def __init__(self, *, obj: point_able):
        pass

    @overload
    def __init__(self,
                 x: Union[number_alias, Coordinates, tuple[number_alias, number_alias]],
                 y: Union[number_alias, Coordinates, tuple[number_alias, number_alias]]):

        pass

    def __init__(self,
                 x: Union[number_alias, Coordinates, tuple[number_alias, number_alias]] = None,
                 y: Union[number_alias, Coordinates, tuple[number_alias, number_alias]] = None,
                 obj: point_able = None):

        if obj is not None:
            x, y = obj

        elif isinstance(x, (Coordinates, tuple)) and isinstance(y, (Coordinates, tuple)):
            origin_x, origin_y = x
            target_x, target_y = y
            x, y = (target_x - origin_x, target_y - origin_y)

        else:
            pass

        super().__init__(x, y)

    def len(self):
        result = (self.x ** 2 + self.y ** 2) ** 0.5

        return result

    def __abs__(self):
        return self.len()

    def __str__(self):
        return '{' + str(self.x) + ', ' + str(self.y) + '}'

    __repr__ = __str__
