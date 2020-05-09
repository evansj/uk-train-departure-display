import time

from PIL import Image, ImageDraw
from luma.core.virtual import hotspot
from display.caching_hotspot import CachingHotspot
from display.animation_mixin import AnimationMixin
import logging
logger = logging.getLogger(__name__)

class CallingAt(AnimationMixin, CachingHotspot):
    """Render a list of stations"""
    def __init__(self, width, height, mode, font, destinations=None, label="Calling at: ", interval=0.01):
        super().__init__(width, height, mode, font)
        self.last_updated = 0.0
        self.image = None
        self.labelImage = None
        self._label = None
        self.labelDirty = False
        self.scrollWidth = width
        self.label = label
        self.startPause = 1.0
        self.endPause = 1.0
        self.pausingSince = None
        self.first_x_pos = -self.width
        self.interval = interval or 0
        self.needs_scroll = False
        self.destinations = destinations

    def __str__(self):
        return "CallingAt(width={}, height={})".format(self.width, self.height)

    @property
    def destinations(self):
        return self.__destinations

    @destinations.setter
    def destinations(self, destinations):
        self.__destinations = destinations
        if destinations and len(destinations) > 0:
            # destinations = destinations[3:]
            if len(destinations) == 1: # one station, "a only."
                text = destinations[0] + " only."
            else: # >=2 stations: "a, b, c and d"
                text = " and ".join([", ".join(destinations[0:-1]), destinations[-1]])
        else:
            text = ""

        self.text = text

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if self._label != label:
            self._label = label
            if label:
                sizeImage = Image.new(self.mode, self.size)
                draw = ImageDraw.Draw(sizeImage)
                size = draw.textsize(self.label, self.font)
                self.labelImage = Image.new(self.mode, (size[0], self.height))
                draw = ImageDraw.Draw(self.labelImage)
                draw.text((0,0), text=self.label, font=self.font, fill="yellow")
                # Work out the width of the scrolling area of the display
                self.scrollWidth = self.width - self.labelImage.width
            else:
                self.scrollWidth = self.width
                self.labelImage = None
            self.labelDirty = True

    def should_redraw(self):
        if self.last_updated == 0.0 or self.labelDirty:
            needs_redraw = True
            # logger.debug("Needs redraw? {} self.last_updated={} self.labelDirty={}".format(needs_redraw, self.last_updated, self.labelDirty))
        elif self.stopped:
            needs_redraw = False
            # logger.debug("Needs redraw? False because self.stopped")
        else:
            needs_redraw = time.perf_counter() - self.last_updated > self.interval
            # logger.debug("Needs redraw? {}".format(needs_redraw))
        return needs_redraw

    def build_cache(self):
        self.last_updated = 0.0
        sizeImage = Image.new(self.mode, self.size)
        draw = ImageDraw.Draw(sizeImage)
        self.textSize = draw.textsize(self.text, self.font)
        # print("Calculated width {}".format(self.textSize))
        self.image = Image.new(self.mode, self.textSize)
        draw = ImageDraw.Draw(self.image)
        draw.text((0,0), text=self.text, font=self.font, fill="yellow")
        self.needs_scroll = self.textSize[0] > self.scrollWidth
        if self.needs_scroll:
            self.x = -self.scrollWidth
        else:
            self.x = 0
        self.first_x_pos = self.x
        logger.debug("Created {} \"{}\", needs_scroll={}".format(self.image, self.text, self.needs_scroll))

    def paste_into(self, image, xy):
        self.last_updated = time.perf_counter()

        # Write the label image
        if self.labelDirty:
            if self.labelImage:
                image.paste(self.labelImage, xy)
            self.labelDirty = False

        if not self.image:
            logger.debug("Not created cached image yet, returning")
            self.end()
            return

        # Crop the visible part of the text from the backing image
        visibleText = self.image.crop((self.x, 0, self.image.width, self.image.height))
        # Paste that cropped image onto the screen
        image.paste(visibleText, (xy[0] + self.labelImage.width, xy[1]))

        # Scroll the image if necessary, with a pause at the start and end of scrolling
        if self.needs_scroll:
            if self.x == self.first_x_pos:
                if self.pausingSince:
                    if self.last_updated - self.pausingSince > self.startPause:
                        if self.start():
                            logger.debug("{} starting animation".format(self))
                            self.x += 1
                            self.pausingSince = None
                        else:
                            logger.debug("Couldn't start animation because start() returned False")
                else:
                    self.pausingSince = self.last_updated
            elif self.x > (self.textSize[0] + 5):
                if self.pausingSince:
                    if self.last_updated - self.pausingSince > self.endPause:
                        self.x = self.first_x_pos
                        self.pausingSince = None
                        logger.debug("{} finished animation".format(self))
                        self.end()
                else:
                    self.pausingSince = self.last_updated
            else:
                self.x += 1
        else:
            logger.debug("Ending animation because we don't need scroll")
            self.end()
