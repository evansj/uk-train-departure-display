from display.signage import Signage
from display.static_text import StaticText
from display.departure_line import DepartureLine
from display.station_list import StationList
from display.clock import Clock

from luma.core.render import canvas

class DepartureSignage(Signage):
    def __init__(self, device, viewport, font, fontBold, fontBoldTall, fontBoldLarge):
        super().__init__(device, viewport, font, fontBold, fontBoldTall, fontBoldLarge)

        self.departures = []
        with canvas(device) as draw:
            # construct all the areas of display
            # Top line - next train
            line = DepartureLine(self.width, self.height, self.font, self.fontBold, None, bold=True)
            viewport.add_hotspot(line, (0, 0))
            self.departures.append(line)

            # Second line - destinations for next train
            self.callingAt = StaticText(self.width, self.height, font, fixed_text="Calling at: ")
            self.callingAt.setFixedWidth(draw)
            viewport.add_hotspot(self.callingAt, (0, 12))

            self.station_list = StationList(self.width - self.callingAt.width, self.height, font, None, interval=0.02)
            self.station_list.width = self.width - self.callingAt.width
            viewport.add_hotspot(self.station_list, (self.callingAt.width, 12))

            # Third and fourth lines - subsequent trains
            line = DepartureLine(self.width, self.height, self.font, self.fontBold, None)
            viewport.add_hotspot(line, (0, 24))
            self.departures.append(line)
            line = DepartureLine(self.width, self.height, self.font, self.fontBold, None)
            viewport.add_hotspot(line, (0, 36))
            self.departures.append(line)
            self.clock = Clock(self.width, 14, self.fontBoldLarge, self.fontBoldTall)
            viewport.add_hotspot(self.clock, (0, 50))

    def update(self, data):
        departures, destinations, departureStation = data

        for i, departureLine in enumerate(self.departures):
            try:
                departureLine.departure = departures[i]
            except IndexError:
                departureLine.departure = None

        if len(departures) > 0:
            self.callingAt.text = "Calling at: "
        else:
            self.callingAt.text = ""
        self.station_list.destinations = destinations
