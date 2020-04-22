import time

from functools import reduce
from PIL import Image, ImageDraw
from luma.core.virtual import hotspot

class StationList(hotspot):
    """Render a list of stations"""
    def __init__(self, width, height, font, destinations=None, interval=0.01):
        super().__init__(width, height)
        self.font = font
        self.destinationText = None
        self.image = None
        self.startPause = 0.5
        self.endPause = 0.5
        self.pausingSince = None
        self.x = -self.width
        self.first_x_pos = -self.width
        self.interval = interval
        self.last_updated = 0.0
        self.destinations = destinations
        # self.update_times = []

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
            now = time.perf_counter()
            interval = now - self.last_updated
            should = interval > self.interval
            return should
            # if should:
            #     print("Redrawing after {} updates".format(self.update_times))
            #     self.update_times = []
            # else:
            #     self.update_times.append(interval)
            # return should
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
        # print("Pasted image {} cropped at x={} into {} at {}".format(visibleText, self.x, image, xy))
        # delete the cropped image we created
        del visibleText

        self.last_updated = time.perf_counter()

        # Implement the pause at the start and end of scrolling
        if self.x == self.first_x_pos:
            if self.pausingSince:
                if self.last_updated - self.pausingSince > self.startPause:
                    self.x += 1
                    self.pausingSince = None
            else:
                self.pausingSince = self.last_updated
        elif self.x > self.textSize[0]:
            if self.pausingSince:
                if self.last_updated - self.pausingSince > self.endPause:
                    self.x = self.first_x_pos
                    self.pausingSince = None
            else:
                self.pausingSince = self.last_updated
        else:
            self.x += 1
