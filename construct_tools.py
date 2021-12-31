from typing import Union, Literal

from field_tools import MapObject, Field, Coordinates
from field_tools.field import OutOfField
from copy import copy


def fill(field: Field,
         obj: MapObject,
         scope: Union[tuple[Coordinates, Coordinates], list[list[int]]]) -> None:

    def normalize_range(*args):
        return tuple(sorted(args))

    def insert(x__, y__):
        c__ = copy(obj)
        c__.coordinates = Coordinates(x__, y__)
        field.add(c__)

    if isinstance(scope, tuple):
        scope_1, scope_2 = scope
        x_range = normalize_range(scope_1.x, scope_2.x)
        y_range = normalize_range(scope_1.y, scope_2.y)
        print(x_range, y_range)
        for x in range(*x_range):
            for y in range(*y_range):
                insert(x, y)

    elif isinstance(scope, list):
        for x, x_line in enumerate(scope):
            for y, y_val in enumerate(x_line):
                if y_val:
                    try:
                        insert(x, y)
                    except OutOfField:
                        pass

    else:
        raise ValueError

    return None
