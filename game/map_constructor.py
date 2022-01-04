import copy

from render.map import Map, MapObject, Coordinates


class Mask:
    def __init__(self,
                 matrix: list[list[bool]]):

        self.matrix = matrix

    @classmethod
    def parse(cls,
              string: str,
              vertical_divisor: str = '\n',
              horizontal_divisor: str = ' ',
              skip_chars: tuple[str] = ('.', )):

        matrix = []

        for y_line in string.split(vertical_divisor):
            if not y_line:
                continue
            tmp = []
            for value in y_line.split(horizontal_divisor):
                if value == '':
                    continue

                tmp.append(value not in skip_chars)

            matrix.append(tmp)

        result = cls(matrix)

        return result


class ConstructMap(Map):
    def add_by_mask(self, obj: MapObject, mask: Mask) -> None:

        for y, y_line in enumerate(mask.matrix):
            for x, value in enumerate(y_line):
                if value:
                    obj = copy.copy(obj)
                    obj.coordinates = Coordinates(x, y)
                    self.add(obj)

        return None
