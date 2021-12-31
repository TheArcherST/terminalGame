from typing import Optional

from .map_object import MapObject, Coordinates
from .render_core import RenderCore

from datetime import datetime


class Collision(Exception):
    pass


class OutOfField(Exception):
    pass


class Field:
    def __init__(self, width: int, height: int):
        self.cells: list[list[Optional[MapObject]]] = [[None for _ in range(width)] for _ in range(height)]
        self.current_changes = 0

    def render(self, scope: tuple[Coordinates, Coordinates], core: 'RenderCore' = None) -> str:
        if core is None:
            core = RenderCore()

        matrix = self._empty_matrix

        def normalize_range(*args):
            return tuple(sorted(args))

        scope_1, scope_2 = scope
        x_range = normalize_range(scope_1.x, scope_2.x)
        y_range = normalize_range(scope_1.y, scope_2.y)

        for x in range(*x_range):
            for y in range(*y_range):

                try:
                    cell = self.cells[x][y]
                except IndexError:
                    continue

                if cell is None:
                    continue

                matrix = self._write_texture(matrix, cell.texture, Coordinates(x, y))

        result = core.render_matrix(matrix)

        return result

    @staticmethod
    def _write_texture(matrix: list[list[int]],
                       texture: list[list[int]],
                       to: Coordinates) -> list[list[int]]:

        for texture_x in range(len(texture)):
            for texture_y in range(len(texture[0])):
                x = to.x + texture_x
                y = to.y + texture_y

                try:
                    if x < 0 or y < 0:
                        raise IndexError

                    matrix[x][y] = texture[texture_x][texture_y]
                except IndexError:
                    pass

        return matrix

    def add(self, obj: MapObject) -> None:
        if obj.coordinates.x < 0 or obj.coordinates.y < 0:
            raise OutOfField

        try:
            if self.cells[obj.coordinates.x][obj.coordinates.y] is None:

                self.cells[obj.coordinates.x][obj.coordinates.y] = obj
                self.current_changes += 1

            else:
                raise Collision
        except IndexError:
            raise OutOfField

    def move(self, obj: MapObject, to: Coordinates):
        self.remove(obj)

        old_position = obj.coordinates
        obj.coordinates = to
        try:
            self.add(obj)
        except (Collision, OutOfField) as e:
            obj.coordinates = old_position
            self.add(obj)

            raise e

    def remove(self, obj) -> None:
        for x, i in enumerate(self.cells):
            if obj in i:
                y = i.index(obj)

                self.cells[x][y] = None
                self.current_changes += 1

                return None
        raise KeyError

    @property
    def _empty_matrix(self) -> list[list[int]]:
        result = []

        for _ in range(self.cells.__len__()):
            result.append([0] * self.cells[0].__len__())

        return result
