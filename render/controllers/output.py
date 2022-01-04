import os
from abc import abstractmethod


class BaseOutputController:
    @abstractmethod
    def set(self, text: str):
        """Set method

        Set output text

        """

        pass

    @abstractmethod
    def refresh(self):
        """Refresh method

        Refresh output (clear all)

        """

        pass


class TerminalOutput(BaseOutputController):
    def __init__(self):
        self.current_text = None

    def set(self, text: str):
        self.clear()
        self.current_text = text

        print(text, end='')

    def refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear(self):
        for _ in reversed(self.current_text or ''):
            if _ == '\n':
                literal = '\033[A'
            else:
                literal = '\b'

            print('', end=literal)
