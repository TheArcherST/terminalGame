from typing import Optional

from render.algebra.proportion import Proportion
from render.geometry.point import number_alias


class Fraction:
    def __init__(self, x: Optional[number_alias], y: Optional[number_alias]):
        self.numerator = x
        self.denominator = y

    def __iter__(self):
        return iter((self.numerator, self.denominator))

    def to_proportion(self, other: 'Fraction'):
        result = Proportion(self, other)

        return result

    @property
    def is_need_resolve(self):
        return (self.numerator is None) or (self.denominator is None)

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

    __repr__ = __str__
