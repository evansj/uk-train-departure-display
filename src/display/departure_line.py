from display import HAlign
from display.static_text import StaticText
from display.service_status import ServiceStatus
from display.platform import Platform
from display.destination import Destination

class DepartureLine(object):
    """
    Render a departure line

    HH:MM Destination Station       Plat 88     On time
    """
    def __init__(self, width, height, font, fontBold, departure, bold=False):
        self.width       = width
        self.height      = height
        self.font        = font
        self.fontBold    = fontBold
        self.bold        = bold
        self.status      = None
        self.platform    = None
        self.destination = None
        self.departure   = departure

    def __str__(self):
        return "DepartureLine(width={}, height={})".format(self.width, self.height)

    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, departure):
        self.__departure = departure
        if self.status:
            self.status.departure = departure
        if self.platform:
            self.platform.departure = departure
        if self.destination:
            self.destination.departure = departure

    def setViewport(self, viewport, y, draw):
        self.__viewport = viewport
        width = viewport.width
        # print("viewport.width {}".format(width))

        # Create new objects for status, platform and destination
        status     = ServiceStatus(width, 10, self.font, self.departure)
        status.setFixedWidth(draw)
        # print("status.width {}".format(status.width))
        platform   = Platform(width, 10, self.font, self.departure)
        platform.setFixedWidth(draw)
        # print("platform.width {}".format(platform.width))

        destinationFont = self.fontBold if self.bold else self.font
        destinationWidth = width - status.width - platform.width - 5
        # print("destinationWidth {}".format(destinationWidth))
        destination = Destination(destinationWidth, 10, destinationFont, self.departure)
        # print("destination.width {}".format(destination.width))

        # print("{} destination {}".format(y, destination.text))
        # print("{} status {}".format(y, status.text))
        # print("{} platform {}".format(y, platform.text))

        viewport.add_hotspot(destination, (0, y))
        viewport.add_hotspot(status, (width - status.width, y))
        viewport.add_hotspot(platform, (width - status.width - platform.width, y))

        # Remember the status, platform and destination for future updates
        self.status      = status
        self.platform    = platform
        self.destination = destination
