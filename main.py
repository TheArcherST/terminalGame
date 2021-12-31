from field_tools import Field, Coordinates
from gameplay import Gameplay, Game
from objects import Mate, Flower, Brick, map_data
from construct_tools import fill


field = Field(30, 10)

mate = Mate(Coordinates(3, 5), field)

fill(field,
     Brick(Coordinates(0, 0)),
     list(map_data.data))

game = Game(field, mate)
gameplay = Gameplay(game, (4, 4))
gameplay.run()
