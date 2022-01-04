from typing import TYPE_CHECKING
from render.geometry.point import BasePoint

if TYPE_CHECKING:
    from render.geometry.vector import Vector


class Coordinates(BasePoint):
    @property
    def vec(self) -> 'Vector':
        return Vector(obj=self)
