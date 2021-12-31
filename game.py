from field_tools import Field, MapObject


class Game:
    def __init__(self, field: Field, player: MapObject):
        self.field = field
        self.player = player
