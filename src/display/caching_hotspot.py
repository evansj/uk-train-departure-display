import time

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
                self.buildCache()
            else:
                self.clearCache()

    def buildCache(self):
        pass

    def clearCache(self):
        pass
