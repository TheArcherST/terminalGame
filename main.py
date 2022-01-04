from game import Game, ConstructMap, Mask

from render.render import RenderEngine
from render.core import RenderCore
from render.controllers.fps import FpsController
from render.controllers.output import TerminalOutput
from render.map import MapObject


MAP = """
@ @ @ @ @ . . . @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @  
@ . . . @ . . . @ . . . . . . . . . . . . . . . . @ . . . @ 
@ . . . @ . . . @ . . . . . . . . . . . . . . . . @ . . . @ 
@ . . . . . . . @ @ @ @ @ @ @ @ @ @ . . @ @ . . . @ . . . @ 
@ . . . . . . . . . . . . . . . . . . . . @ . . . @ . . . @ 
@ . . . . . . . . . . . . . . . . . . . . @ . . . @ @ . . @ 
@ . . . @ . . . @ @ @ @ . . @ @ @ @ . . @ @ . . . . @ . . @ 
@ . . . @ . . . @ . . . . . @ . . . . . . @ . . . . . . . @ 
@ . . . @ . . . @ . . . . . @ . . . . . . @ . . . . . . . @ 
@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
"""


def main():
    render_core = RenderCore()
    fps_controller = FpsController(10)
    output_controller = TerminalOutput()

    render_engine = RenderEngine(
        render_core=render_core,
        fps_controller=fps_controller,
        output_controller=output_controller
    )

    construct_map = ConstructMap(10, 30, render_engine)
    player = MapObject(construct_map, (1, 1), 100, True)

    brick = MapObject(construct_map, texture=int(render_core.convert('@')))
    brick_mask = Mask.parse(MAP)

    construct_map.add_by_mask(brick, brick_mask)

    game = Game(construct_map, player)
    game.run()


if __name__ == '__main__':
    main()
