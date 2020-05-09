import time
import logging
logger = logging.getLogger(__name__)

from PIL import Image, ImageDraw
from luma.core.virtual import hotspot

class CachingHotspot(hotspot):
    """A hotspot which can build a cache of image(s)"""
    def __init__(self, width, height, mode, font, text=None):
        super().__init__(width, height)
        self.mode = mode
        self.font = font
        self._text = None
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if self._text != text:
            self._text = text
            if text:
                logger.debug("CachingHotspot calling build_cache() because text has changed")
                self.build_cache()
            else:
                logger.debug("CachingHotspot calling clear_cache() because text=None")
                self.clear_cache()

    def build_cache(self):
        pass

    def clear_cache(self):
        pass
