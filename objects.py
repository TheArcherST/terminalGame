import random

from field_tools import Coordinates, MapObject, Field
import json
from attrdict import AttrDict


with open('data.json') as fs:
    data = AttrDict(json.load(fs))
with open('map.json') as fs:
    map_data = AttrDict(json.load(fs))

VIEW = data.view


class Mate(MapObject):
    def __init__(self, coordinates: Coordinates, field: Field = None):
        super().__init__(coordinates, VIEW.mate, field)


class Flower(MapObject):
    def __init__(self, coordinates: Coordinates, field: Field = None):
        super().__init__(coordinates, VIEW.flower, field)


class Brick(MapObject):
    def __init__(self, coordinates: Coordinates, field: Field = None):
        super().__init__(coordinates, VIEW.brick, field)
