from typing import Union, Optional, Literal
from math import cos, sin, acos, asin, degrees, radians

from render.algebra.fraction import Fraction
from render.geometry.point import number_alias
from render.geometry.vector import Vector
from ..exceptions import NoSolution


def sin_(degrees_: number_alias):
    return sin(radians(degrees_))


def asin_(radians_: number_alias):
    return degrees(asin(radians_))


def cos_(degrees_: number_alias):
    return cos(radians(degrees_))


def acos_(radians_: number_alias):
    return degrees(acos(radians_))


class JournalEntry:
    def __init__(self,
                 status: Literal['success', 'error'],
                 name: str,
                 exception: Optional[Exception] = None):
        self.status = status
        self.name = name
        self.exception = exception

    def __str__(self):
        return f"JournalEntry(status={self.status}, name={self.name}, exception=...)"

    __repr__ = __str__


class ResolveJournal:
    def __init__(self, process_name: str):
        self.process_name = process_name

        self.journal: list[JournalEntry] = []
        self.is_resolved = False

    def report_error(self, msg: str, e: Exception):
        self.journal.append(
            JournalEntry('error', msg, e)
        )

    def report_success(self, msg: str):
        self.journal.append(
            JournalEntry('success', msg)
        )

    def report_resolve(self):
        self.is_resolved = True

    def render(self) -> str:
        result = str()

        if self.is_resolved:
            status = 'success'
        else:
            status = 'error'

        barrier = '=' * 6
        title = f'\n{barrier} Process `{self.process_name}` : {status} {barrier}\n'
        result += title

        for num, i in enumerate(self.journal):
            result += '\n'
            result += (f'Step {num + 1}\n'
                       + f"Step {num + 1}".__len__() * "-"
                       + f'\n{i.name} : {i.status}')
            if i.exception is not None:
                result += f'\nException : `{i.exception}`'
            result += '\n'

        result += f'\n{len(title) * "="}\n'

        return result

    def __str__(self):
        return self.render()

    def __repr__(self):
        return repr(self.journal)


class Triangle:
    """Triangle object

    You can create triangle by data what you
    have, if you try to get another elements,
    triangle.resolve method will be called.

    """

    def __init__(self,
                 A: number_alias = None,
                 a: Union[Vector, number_alias] = None,
                 B: number_alias = None,
                 b: Union[Vector, number_alias] = None,
                 C: number_alias = None,
                 c: Union[Vector, number_alias] = None):

        if isinstance(a, Vector):
            a = a.len()
        if isinstance(b, Vector):
            b = b.len()
        if isinstance(c, Vector):
            c = c.len()

        self._A: number_alias = A
        self._a: number_alias = a
        self._B: number_alias = B
        self._b: number_alias = b
        self._C: number_alias = C
        self._c: number_alias = c

    def __str__(self):
        return (
            f'Triangle('
            f'A={self._A}, B={self._B}, C={self._C}, '
            f'a={self._a}, b={self._b}, c={self._c}'
            f')'
        )

    __repr__ = __str__

    @property
    def is_resolved(self):
        return (self._known_angles == 3) & (self._known_vectors == 3)

    def resolve(self) -> ResolveJournal:
        """Resolve method

        Triangle resolving automatically, but you can
        use this function to control efficiency.

        :return: None
        """

        journal = ResolveJournal(f'Resolve triangle `{self}`')

        name = 'Try complete angles'
        try:
            self._try_complete_angles()
        except NoSolution as e:
            journal.report_error(name, e)
        else:
            journal.report_success(name)

        if self.is_resolved:
            journal.report_resolve()
            return journal

        # SIN THEOREM

        name = 'Try resolve by sine theorem'
        try:
            self._try_sine_theorem()
        except NoSolution as e:
            journal.report_error(name, e)
        else:
            journal.report_success(name)

        if self.is_resolved:
            journal.report_resolve()
            return journal

        # COS THEOREM

        name = 'Try resolve by cos theorem'
        try:
            self._try_cos_theorem()
        except NoSolution as e:
            journal.report_error(name, e)
        else:
            journal.report_success(name)

        if self.is_resolved:
            journal.report_resolve()
            return journal
        else:
            raise NoSolution(journal)

    @property
    def A(self) -> number_alias:
        if self._A is None:
            self.resolve()

        return self._A

    @property
    def a(self) -> number_alias:
        if self._a is None:
            self.resolve()

        return self._a

    @property
    def B(self) -> number_alias:
        if self._B is None:
            self.resolve()

        return self._B

    @property
    def b(self) -> number_alias:
        if self._b is None:
            self.resolve()

        return self._b

    @property
    def C(self) -> number_alias:
        if self._C is None:
            self.resolve()

        return self._C

    @property
    def c(self) -> number_alias:
        if self._c is None:
            self.resolve()

        return self._c

    @property
    def _known_angles(self) -> int:
        return len(list(filter(
            lambda x: x is not None, (self._A, self._B, self._C)
        )))

    @property
    def _known_vectors(self) -> int:
        return len(list(filter(
            lambda x: x is not None, (self._a, self._b, self._c)
        )))

    def _try_complete_angles(self):
        try:
            if self._A is None:
                self._A = 180 - self._B - self._C
            elif self._B is None:
                self._B = 180 - self._A - self._C
            elif self._C is None:
                self._C = 180 - self._A - self._B
            else:
                pass
        except TypeError:
            raise NoSolution("Cant evaluate third angle")

    def _try_sine_theorem(self):

        """Sine theorem

        Note: in `a`, `b`, `c` you must give this vector's length

        """

        A = self._A
        a = self._a
        B = self._B
        b = self._b
        C = self._C
        c = self._c

        if A is not None:
            A = sin_(A)
        if B is not None:
            B = sin_(B)
        if C is not None:
            C = sin_(C)

        fraction_1 = Fraction(a, A)
        fraction_2 = Fraction(b, B)
        fraction_3 = Fraction(c, C)

        fractions = [fraction_1, fraction_2, fraction_3]
        resolved = list(filter(lambda x: not x.is_need_resolve, fractions))
        unresolved = list(filter(lambda x: x.is_need_resolve, fractions))

        if len(resolved) < 1:
            raise NoSolution("Less than 1 resolved fraction")

        work_fraction = resolved[0]

        # try to resolve
        try:
            for i in unresolved:
                i.to_proportion(work_fraction).resolve()
        except ValueError as e:
            raise NoSolution('Error while trying resolve proportion', e)

        self._A = asin_(fraction_1.denominator)
        self._a = fraction_1.numerator

        self._B = asin_(fraction_2.denominator)
        self._b = fraction_2.numerator

        self._C = asin_(fraction_3.denominator)
        self._c = fraction_3.numerator

        return None

    def _try_cos_theorem(self):
        # a**2 = b**2 + c**2 - 2 * b * c * cosA
        # b**2 = a**2 + c**2 - 2 * a * c * cosB
        # c**2 = a**2 + b**2 - 2 * a * b * cosC
        # And we can calc it if know:
        # b, c, A
        # a, c, B
        # a, b, C

        # cosA = (b ** 2 + c ** 2 - a ** 2) / 2 * b * c
        # cosB = (a ** 2 + c ** 2 - b ** 2) / 2 * a * c
        # cosC = (a ** 2 + b ** 2 - c ** 2) / 2 * a * b
        # And we can calc it if know:
        # a, b, c

        def calc_1(a: number_alias, b: number_alias, angle: number_alias):
            return (a ** 2 + b ** 2 - 2 * a * b * cos_(angle)) ** 0.5

        def calc_2(a: number_alias, b: number_alias, c: number_alias):
            res = acos_((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            return res

        cases_1 = (
            ((self._b, self._c, self._A), '_a'),
            ((self._a, self._c, self._B), '_b'),
            ((self._a, self._b, self._C), '_c')
        )

        for i in cases_1:
            data_set, result_label = i
            try:
                result = calc_1(*data_set)
            except TypeError:
                pass
            else:
                self.__dict__.__setitem__(result_label, result)

        if (
                self._a is not None
                and self._b is not None
                and self._c is not None
        ):

            self._A = calc_2(self._b, self._c, self._a)
            self._B = calc_2(self._a, self._c, self._b)
            self._C = calc_2(self._a, self._b, self._c)

        if not self.is_resolved:
            raise NoSolution('All in theorem tried, but triangle not resolved')
