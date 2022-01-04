from typing import overload, Union


class RenderCore:

    # gradient from `Onigiri` channel
    GRADIENT = '.:!/r(l1Z4H9W8$@'

    def __init__(self, max_: int = 256):
        self.max = max_

    def render_matrix(self, matrix: list[list[int]]):
        result = ''

        for line_x in matrix:
            for y in line_x:
                result += self.convert(y, self.max)
                result += ' '

            result += '\n'

        return result

    @overload
    def convert(self, value: str, max_: int = 255) -> int:
        pass

    @overload
    def convert(self, value: Union[int, float], max_: int = 255) -> str:
        pass

    def convert(self, value: Union[int, str, float], max_: int = 255) -> Union[int, str]:
        if isinstance(value, (int, float)):
            normalized = value / max_
            index_float = normalized * (self.GRADIENT.__len__() - 1)
            index = int(round(index_float))

            result = self.GRADIENT[index]

        elif isinstance(value, str):
            index = self.GRADIENT.index(value)
            normalized = (index + 1) / len(self.GRADIENT)

            result = int(normalized * max_)

        else:
            raise TypeError(f"Can't convert type `{type(value)}`")

        return result
