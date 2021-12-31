import datetime
from typing import Optional
from game import Game
import time
from threading import Thread
from field_tools.field import Collision, OutOfField
from game_render import GameRenderEngine, printer

from pynput import keyboard


class Gameplay:
    def __init__(self, game: Game, size: tuple[int, int]):
        self.game = game
        self.size = size
        self.render_engine = GameRenderEngine(self.game, self.size)

    def keyboard_listen_flow(self) -> None:
        with keyboard.Listener(on_press=self.key_handler) as listener:
            listener.join()

    def key_handler(self, key):
        player = self.game.player

        try:
            if key == keyboard.Key.up or str(key) == "'w'":
                player.move(-1, 0)
            elif key == keyboard.Key.down or str(key) == "'s'":
                player.move(1, 0)
            elif key == keyboard.Key.right or str(key) == "'d'":
                player.move(0, 1)
            elif key == keyboard.Key.left or str(key) == "'a'":
                player.move(0, -1)
            elif str(key) == "'\\x12'":
                printer.clear_all()
                self.render_engine.refresh_request()
            elif key == keyboard.Key.esc:
                self.render_engine.is_alive = False
                exit(0)

        except (Collision, OutOfField):
            pass

    @staticmethod
    def enum_string_field(field: str, row_spaces: int = 1):
        res = str()
        lines = field.split('\n')
        x_len = round(len(lines[0]) / 2)
        head = '  ' + (' ' * row_spaces).join(map(str, range(x_len)))
        res += head
        for num, i in enumerate(field.split('\n')):
            if not i:
                continue
            res += f'\n{num} {i}'

        return res

    @staticmethod
    def post_init():
        printer.clear_all()

    def run(self) -> None:
        """
        Run game in current thread
        """

        flow1 = Thread(target=self.render_engine.render_flow)
        flow2 = Thread(target=self.keyboard_listen_flow)

        flows = [flow1, flow2]

        for i in flows:
            i.start()

        time.sleep(0.1)
        self.post_init()

        for i in flows:
            i.join()
