from pynput import keyboard
from time import sleep
from threading import Thread

from render.map import Map, MapObject
from render.exceptions import OutOfField, Collision


class Game:
    def __init__(self, map_: Map, player: MapObject):
        self.map = map_
        self.player = player

        self.is_alive = False

    def keyboard_listen_flow(self) -> None:
        with keyboard.Listener(on_press=self.key_handler) as listener:
            listener.join()

    def key_handler(self, key):
        player = self.player

        try:
            if key == keyboard.Key.up or str(key) == "'w'":
                player.move(0, -1)
            elif key == keyboard.Key.down or str(key) == "'s'":
                player.move(0, 1)
            elif key == keyboard.Key.right or str(key) == "'d'":
                player.move(1, 0)
            elif key == keyboard.Key.left or str(key) == "'a'":
                player.move(-1, 0)
            elif str(key) == "'\\x12'":
                self.map.render_engine.output_controller.refresh()
                self.map.render_engine.fps_controller.updates_notify()
            elif key == keyboard.Key.esc:
                exit(0)
        except (OutOfField, Collision):
            # action undo automatically
            pass
        finally:
            pass

    def tear_down(self):
        self.map.render_engine.tear_down()
        self.is_alive = False

        print('Game teared down')

    __del__ = tear_down

    def run(self) -> None:
        """
        Run game in current thread
        """

        def wrap_tear_down(func):
            def new(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                finally:
                    self.tear_down()
            return new

        flow1 = Thread(target=wrap_tear_down(self.keyboard_listen_flow))
        flow2 = Thread(target=wrap_tear_down(self.map.render_engine.render_flow),
                       args=[self.player, self.map])

        flows = [flow1, flow2]

        self.is_alive = True

        for i in flows:
            i.start()

        sleep(0.1)

        self.map.render_engine.output_controller.refresh()
        self.map.render_engine.process_render(self.player, self.map)
