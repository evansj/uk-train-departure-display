from luma.core.virtual import viewport
from display.animation_mixin import AnimationMixin

import logging
logger = logging.getLogger(__name__)

class AnimatedViewport(viewport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._animated_hotspots = []

    def add_hotspot(self, hotspot, xy):
        super().add_hotspot(hotspot, xy)
        if isinstance(hotspot, AnimationMixin):
            logger.debug("Adding animated hotspot {} at {}".format(hotspot, xy))
            self._animated_hotspots.append((hotspot, xy))

    def remove_hotspot(self, hotspot, xy):
        super().remove_hotspot(hotspot, xy)
        self._animated_hotspots.remove((hotspot, xy))

    @property
    def running(self):
        """Returns True while any animation is running or can run"""
        for hotspot in self._animated_hotspots:
            if hotspot[0].running:
                return True
        return False

    @property
    def stopped(self):
        """The opposite of running"""
        return not self.running

    def stop(self):
        """The main coordinator method calls this when it wants animations to stop at the end of their current cycle"""
        for hotspot in self._animated_hotspots:
            hotspot[0].stop()

    def run(self):
        """The main coordinator method calls this when it wants animations to run"""
        for hotspot in self._animated_hotspots:
            hotspot[0].run()
