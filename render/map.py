from typing import Optional, TypeVar, Union, overload

from .exceptions import OutOfField, Collision
from .geometry.point import point_able
from .render import RenderEngine
from .geometry.coordinates import Coordinates


T = TypeVar('T')


class Map:
    """ Map object """

    def __init__(self, height: int, width: int, render_engine: RenderEngine):
        self.height = height
        self.width = width

        self.objects: list[MapObject] = []
        self.render_engine = render_engine

    def add(self, obj: 'MapObject'):
        if obj.coordinates not in self:
            raise OutOfField()

        self.objects.append(obj)

    def check_object_insert(self, to__: point_able) -> Optional[Exception]:
        """Can insert object method

        Return None or Exception object

        """

        to__ = Coordinates(*to__)

        if to__ not in self:
            result = OutOfField("Can't move object: Out of field")

        elif self.expand_objects_on_map()[to__.y][to__.x] is not None:
            result = Collision("Can't move object: Collision")

        else:
            result = None

        return result

    def __contains__(self, item: Union['MapObject', point_able]) -> bool:
        if isinstance(item, MapObject):
            return self.objects.__contains__(item)
        else:
            x, y = item
            return (-1 < x < self.width) and (-1 < y < self.height)

    def expand_objects_on_map(self) -> list[list[Optional['MapObject']]]:
        result = self.get_empty_matrix()

        for i in self.objects:
            result[i.coordinates.y][i.coordinates.x] = i

        return result

    def get_empty_matrix(self, default: T = None) -> list[list[T]]:
        """Get empty matrix method

        Return empty (None) matrix of map's size

        """

        result = [[default for _ in range(self.width)]
                  for _ in range(self.height)]

        return result

    def move_notify(self):
        """Change notify

        Notify about any move, add, or remove

        """

        self.render_engine.fps_controller.updates_notify()


class MapObject:
    @overload
    def __init__(self,
                 map_: 'Map',
                 coordinates: Union[Coordinates, tuple[int, int]],
                 texture: int,
                 auto_add: bool = True):

        """ Real object """

        pass

    @overload
    def __init__(self,
                 map_: 'Map', *,
                 texture: int = None):

        """ Ephemeral object """

        pass

    def __init__(self,
                 map_: 'Map',
                 coordinates: Union[Coordinates, tuple[int, int]] = None,
                 texture: int = None,
                 auto_add: bool = True):

        if coordinates is not None:
            coordinates = Coordinates(*coordinates)

        self.map = map_
        self.coordinates: Optional[Coordinates] = coordinates
        self.texture = texture

        if auto_add and coordinates is not None:
            self.map.add(self)

    def move(self, on_x: int, on_y: int) -> Coordinates:

        if self.is_ephemeral:
            raise RuntimeError('Cant move ephemeral object')

        new_position = self.coordinates + (on_x, on_y)
        check_result = self.map.check_object_insert(new_position)

        if isinstance(check_result, Exception):
            raise check_result
        else:
            self.coordinates = new_position
            self.map.move_notify()

        return new_position

    @property
    def is_ephemeral(self):
        result = self.coordinates is None

        return result
