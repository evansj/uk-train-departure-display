from display.signage import Signage
from display.static_text import StaticText
from display.departure_line import DepartureLine
from display.calling_at import CallingAt
from display.clock import Clock
from display.animation_mixin import AnimationMixin

from luma.core.render import canvas

import logging
logger = logging.getLogger(__name__)

class DepartureSignage(AnimationMixin, Signage):
    def __init__(self, device, viewport, font, fontBold, fontBoldTall, fontBoldLarge):
        super().__init__(device, viewport, font, fontBold, fontBoldTall, fontBoldLarge)

        self.departures = []
        line_height = 12
        clock_line_height = 14
        xPos = 0
        yPos = 0
        with canvas(device) as draw:
            # construct all the areas of display
            # Top line - next train
            line = DepartureLine(self.width, line_height, self.font, self.fontBold, None, bold=True)
            viewport.add_hotspot(line, (xPos, yPos))
            self.departures.append(line)

            yPos += line_height

            # Second line - destinations for next train
            self.calling_at = CallingAt(self.width, line_height, device.mode, font, None, interval=0.02)
            viewport.add_hotspot(self.calling_at, (xPos, yPos))

            yPos += line_height

            # Third and fourth lines - subsequent trains
            line = DepartureLine(self.width, line_height, self.font, self.fontBold, None)
            viewport.add_hotspot(line, (xPos, yPos))
            self.departures.append(line)

            yPos += line_height

            line = DepartureLine(self.width, line_height, self.font, self.fontBold, None)
            viewport.add_hotspot(line, (xPos, yPos))
            self.departures.append(line)

            # the clock sits on the baseline
            self.clock = Clock(self.width, clock_line_height, self.fontBoldLarge, self.fontBoldTall)
            viewport.add_hotspot(self.clock, (xPos, 50))

    def update(self, data):
        departures, destinations, departureStation = data

        for i, departureLine in enumerate(self.departures):
            try:
                departureLine.departure = departures[i]
            except IndexError:
                departureLine.departure = None

        logger.debug("DepartureSignage updating calling_at.destinations")
        self.calling_at.destinations = destinations

