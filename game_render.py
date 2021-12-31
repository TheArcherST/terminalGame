import time

from field_tools import Coordinates
from game import Game
import os
import sys
from datetime import datetime
from typing import Optional
from time import sleep


def clear_atty():
    os.system('cls' if os.name == 'nt' else 'clear')


class TerminalFrame:
    def __init__(self):
        self.current_text = None

    def set(self, text: str):
        self.clear()
        self.current_text = text
        print(text, end='')

    def clear_all(self):
        clear_atty()

    def clear(self):
        for _ in reversed(self.current_text or ''):
            if _ == '\n':
                literal = '\033[A'
            else:
                literal = '\b'

            print(literal, end='')


printer = TerminalFrame()


class GameRenderEngine:
    def __init__(self, game: Game, vision_scope: tuple[int, int], fps: int = 9):
        self.game = game
        self.vision_scope = vision_scope
        self.frame = TerminalFrame()
        self.current_fps_score = 0
        self.unresolved_updates = 0
        self.last_render: Optional[datetime] = None
        self.fps = fps
        self.max_fps = fps
        self.last_fps_edit = datetime.now()

        self.is_alive = False

    def process_render(self):
        first = Coordinates(self.game.player.coordinates.x - self.vision_scope[1],
                            self.game.player.coordinates.y - self.vision_scope[0])
        second = Coordinates(self.vision_scope[1] + self.game.player.coordinates.x,
                             self.vision_scope[0] + self.game.player.coordinates.y)
        res = self.game.field.render((first, second))
        res = self.post_rendering(res)

        self.frame.set(res)

        self.current_fps_score += 1
        self.unresolved_updates = 0
        self.last_render = datetime.now()

    def post_rendering(self, render_result: str):
        res = ''
        for num, i in enumerate(render_result.split('\n')):
            if num == 2:
                i += f' {self.fps} fps'

            res += i + '\n'

        return res

    def update_notify(self, force: bool = False):
        self.unresolved_updates += 1

        if force:
            self.process_render()

    def upd_unresolved_updates(self):
        self.unresolved_updates += self.game.field.current_changes
        self.game.field.current_changes = 0

    def render_flow(self):
        self.is_alive = True

        while self.is_alive:
            sleep(0.01)  # max fps is 100

            self.upd_unresolved_updates()

            self.last_fps_edit = datetime.now()

            if self.unresolved_updates == 0:
                self.fps -= 1
            else:
                self.fps += 1

            if self.fps > self.max_fps:
                self.fps = self.max_fps
            if self.fps < 1:
                self.fps = 1

            if self.last_render:
                diff = (datetime.now() - self.last_render).total_seconds()
                if diff >= 1 / self.fps:
                    self.process_render()
            else:
                self.process_render()
        else:
            printer.clear_all()
