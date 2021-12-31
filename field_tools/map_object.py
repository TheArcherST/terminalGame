from typing import Union, TYPE_CHECKING
from dataclasses import dataclass
from copy import copy

from .render_core import RenderCore


if TYPE_CHECKING:
    from .field import Field


@dataclass
class Coordinates:
    x: int
    y: int

    def __sub__(self, other):
        result = copy(self)

        if isinstance(other, Coordinates):
            result.x = self.x - other.x
            result.y = self.y - other.x
        elif isinstance(other, int):
            result.x -= other
            result.y -= other
        else:
            return NotImplemented

        return result

    def __add__(self, other: Union['Coordinates', int]) -> 'Coordinates':
        result = copy(self)

        if isinstance(other, Coordinates):
            result.x += other.x + self.x
            result.y = other.y + self.y
        elif isinstance(other, int):
            result.x += other
            result.y += other
        else:
            return NotImplemented

        return result


class MapObject:
    def __init__(self,
                 coordinates: Union[Coordinates, tuple[int, int]],
                 texture: list[list[int]],
                 field: 'Field' = None):

        self.coordinates = coordinates
        self.texture = texture
        self.field = field

        if field is not None:
            field.add(self)

    def render(self, core: 'RenderCore' = None) -> str:
        if core is None:
            core = RenderCore()

        result = core.render_matrix(self.texture)

        return result

    def move(self, on_x: int, on_y: int):
        self.field.move(self,
                        Coordinates(
                            self.coordinates.x + on_x,
                            self.coordinates.y + on_y
                        ))
