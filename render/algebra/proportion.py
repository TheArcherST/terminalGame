from typing import TYPE_CHECKING, Optional

from render.geometry.point import number_alias

if TYPE_CHECKING:
    from render.algebra.fraction import Fraction


class Proportion:
    def __init__(self,
                 fraction_1: 'Fraction',
                 fraction_2: 'Fraction'):

        self.fraction_1 = fraction_1
        self.fraction_2 = fraction_2

    def resolve(self) -> Optional[number_alias]:
        fraction_1 = self.fraction_1
        fraction_2 = self.fraction_2

        try:
            if fraction_1.numerator is None:
                fraction_1.numerator = fraction_1.denominator * fraction_2.numerator / fraction_2.denominator
                result = fraction_1.numerator

            elif fraction_1.denominator is None:
                fraction_1.denominator = fraction_1.numerator * fraction_2.denominator / fraction_2.numerator
                result = fraction_1.denominator

            elif fraction_2.denominator is None:
                fraction_2.denominator = fraction_2.numerator * fraction_1.denominator / fraction_1.denominator
                result = fraction_2.denominator

            elif fraction_2.numerator is None:
                fraction_2.numerator = fraction_1.numerator * fraction_2.denominator / fraction_1.numerator
                result = fraction_2.numerator
            else:
                result = None
        except TypeError:
            raise ValueError("Cant resolve proportion with 2 or more unknown values")

        return result
