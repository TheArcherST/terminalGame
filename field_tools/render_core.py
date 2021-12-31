from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .field import Coordinates


class RenderCore:

    # gradient from `Onigiri` channel
    GRADIENT = '.:!/r(l1Z4H9W8$@'

    def __init__(self, max_: int = 256):
        self.max = max_

    def render_matrix(self, matrix: list[list[int]]):
        result = ''

        for line_x in matrix:
            for y in line_x:
                result += self._color_to_symbol(y, self.max)
                result += ' '

            result += '\n'

        return result

    def _color_to_symbol(self, value: int, max_: int = 255):
        normalized = value / max_
        index_float = normalized * (self.GRADIENT.__len__() - 1)
        index = int(round(index_float))

        return self.GRADIENT[index]


def build_trace(from_: 'Coordinates', to: 'Coordinates') -> list['Coordinates']:
    """
    Build trace method (beta)

    Build trace to point. Use it to trace light
    while render. Returns trace points

    :param from_: from point
    :param to: to point
    :return: list of Coordinate object
    """

    def is_line(from__: 'Coordinates', to__: 'Coordinates'):
        tmp = from__ - to__
        return tmp.x == tmp.y
