import time

from datetime import datetime
from functools import reduce
from PIL import Image, ImageDraw
from luma.core.virtual import hotspot

class StationList(hotspot):
    """Render a list of stations"""
    def __init__(self, width, height, font, destinations=None, interval=0.1):
        super().__init__(width, height)
        self.font = font
        self.destinationText = None
        self.image = None
        self.startPause = 1.0
        self.endPause = 1.0
        self.startTime = None
        self.endTime = None
        self.x = -self.width
        self.first_x_pos = -self.width
        self.interval = interval
        self.last_updated = 0
        self.destinations = destinations

    @property
    def destinations(self):
        return self.__destinations

    @destinations.setter
    def destinations(self, destinations):
        self.__destinations = destinations
        if destinations and len(destinations) > 0:
            destinationText = ", ".join(destinations)
        else:
            destinationText = ""

        if self.destinationText != destinationText:
            self.textSize        = None
            self.image           = None
            self.destinationText = destinationText

    def should_redraw(self):
        if self.interval:
            return time.monotonic() - self.last_updated > self.interval
        else:
            return True

    def buildCache(self, image):
        if not self.image:
            draw = ImageDraw.Draw(image)
            if not self.textSize:
                self.textSize = draw.textsize(self.destinationText, self.font)
                # print("Calculated width {}".format(self.textSize))
            del draw
            self.image = Image.new(image.mode, self.textSize)
            draw = ImageDraw.Draw(self.image)
            draw.text((0,0), text=self.destinationText, font=self.font, fill="yellow")
            del draw
            # print("Created {}".format(self.image))

    def paste_into(self, image, xy):
        self.buildCache(image)

        # Crop the visible part of the text from the backing image
        visibleText = self.image.crop((self.x, 0, self.image.width, self.image.height))
        # Paste that cropped image onto the screen
        image.paste(visibleText, xy)
        # print("Pasted image {} into {} at {}".format(visibleText, image, xy))
        # delete the cropped image we created
        del visibleText

        # Implement the pause at the start and end of scrolling
        if self.textSize:
            now = datetime.today().timestamp()
            if self.x == self.first_x_pos:
                if self.startTime:
                    if now - self.startTime > self.startPause:
                        self.x += 1
                        self.startTime = None
                else:
                    self.startTime = now
            elif self.x > self.textSize[0]:
                if self.endTime:
                    if now - self.endTime > self.endPause:
                        self.x = self.first_x_pos
                        self.endTime = None
                else:
                    self.endTime = now
            else:
                self.x += 1
