from typing import overload

from ..geometry.vector import Vector, Coordinates
from ..geometry.triangle import Triangle
from ..geometry.point import number_alias


class LineFunc:
    """Line func object

    Note: without coff b:
    `y = k * x`

    """

    @overload
    def __init__(self, *,
                 k: number_alias):
        pass

    @overload
    def __init__(self, *,
                 A: Coordinates = None,
                 B: Coordinates = None):

        pass

    def __init__(self, *,
                 k: number_alias = None,
                 A: Coordinates = None,
                 B: Coordinates = None):

        if k is None:
            k = self.get_line_func_k(A, B)

        self.k = k

    def is_segment_intersect(self, first: Coordinates, second: Coordinates) -> bool:
        y_1 = self.evaluate(first.x)
        y_2 = self.evaluate(second.x)

        result = (
                (y_1 == first.y or y_2 == second.y)
                or (y_1 < first.y and y_2 > second.y)
                or (y_1 > first.y and y_2 < second.y)
        )

        return result

    def evaluate(self, x: number_alias):
        return x * self.k

    @staticmethod
    def get_line_func_k(A: 'Coordinates',
                        B: 'Coordinates') -> number_alias:

        """Get line func k

        Function can find k of 'y = kx' by two func coordinates

        """

        triangle = Triangle(c=Vector(A, B),
                            C=90,
                            A=45,
                            B=45)

        try:
            k = triangle.a / triangle.b
        except ZeroDivisionError:
            k = 0

        n1 = A
        n2 = B
        if n1.y < n2.y:
            n1, n2 = n2, n1
        if n1.x < n2.x:
            k = -k

        return k
