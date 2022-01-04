from typing import TYPE_CHECKING
from time import sleep
from datetime import datetime

from render.controllers.fps import BaseFpsController
from render.controllers.output import BaseOutputController
from .core import RenderCore

if TYPE_CHECKING:
    from .map import Map, MapObject


class RenderEngine:
    def __init__(self,
                 render_core: RenderCore,
                 fps_controller: BaseFpsController,
                 output_controller: BaseOutputController):

        self.render_core = render_core
        self.fps_controller = fps_controller
        self.output_controller = output_controller

        self.is_alive = False

    def map_render(self, _player: 'MapObject', map_: 'Map') -> str:
        visible_objects: list['MapObject']
        visible_objects = map_.objects

        matrix: list[list[int]] = map_.get_empty_matrix(0)

        for i in visible_objects:
            color = matrix[i.coordinates.y][i.coordinates.x]
            matrix[i.coordinates.y][i.coordinates.x] = i.texture + color

        result = self.render_core.render_matrix(matrix)

        return result

    @staticmethod
    def post_rendering(map_render: str):
        return map_render + '\n'

    def process_render(self, player: 'MapObject', map_: 'Map') -> None:
        map_render = self.map_render(player, map_)
        render_result = self.post_rendering(map_render)

        self.fps_controller.render_notify(datetime.now())
        self.output_controller.set(render_result)

        return None

    def render_flow(self, player: 'MapObject', map_: 'Map'):
        timeout = min(0.1, 1 / self.fps_controller.max_fps)

        self.is_alive = True
        while self.is_alive:
            if self.fps_controller.is_render_need:
                self.process_render(player, map_)

            sleep(timeout)

    def tear_down(self):
        self.is_alive = False
        self.output_controller.refresh()
