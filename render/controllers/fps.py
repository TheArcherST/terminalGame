from abc import abstractmethod
from datetime import datetime, timedelta


class BaseFpsController:
    @abstractmethod
    def __init__(self, max_fps: int = 30):
        self.max_fps = max_fps

        pass

    @abstractmethod
    def updates_notify(self) -> None:
        pass

    @abstractmethod
    def render_notify(self, render_time: datetime) -> None:
        pass

    @property
    @abstractmethod
    def is_render_need(self) -> bool:
        pass


class FpsController(BaseFpsController):
    """Fps controller object

    Just helper for RenderEngine, cant render
    something itself.

    Note: object not evaluating fps value, fps
    very not stable. This implementation made
    special for this game to impact that's
    performance.

    """

    def __init__(self, max_fps: int = 30):
        """ FpsController initialization """

        self.max_fps = max_fps

        self.last_render = datetime.now()

        self.unresolved_notifies = 0
        self._current_renders = 0

        self._last_update = datetime.now()

    def updates_notify(self) -> None:
        """Updates notify method

        Notify about changes that engine must render

        :return: None
        """

        self.unresolved_notifies += 1

        self._punch_update()

    def render_notify(self, render_time: datetime) -> None:
        """Render notify method

        Notify that render finished

        """

        self.last_render = render_time
        self.unresolved_notifies = 0
        self._current_renders += 1

        self._punch_update()

    @property
    def is_render_need(self) -> bool:
        """Render is need property

        :return: bool

        """

        self._punch_update()

        fps_lost = self.max_fps - self._current_renders
        s_before_update = 1 - (datetime.now() - self._last_update).total_seconds()
        lost_under_normal_use = (
                self.max_fps / s_before_update
        )

        result = (self.unresolved_notifies >= 1
                  and fps_lost >= lost_under_normal_use)

        return result

    def _punch_update(self):
        """Punch update method

        Update if need. (updates must going every 1 second)

        """
        diff = datetime.now() - self._last_update

        if diff.total_seconds() >= 1:
            self._current_renders = 0
