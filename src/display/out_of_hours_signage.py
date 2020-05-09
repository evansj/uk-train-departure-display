from display.signage import Signage
from display.static_text import StaticText
from display.clock import Clock
from display import HAlign
from display.animation_mixin import AnimationMixin

from luma.core.render import canvas

class OutOfHoursSignage(AnimationMixin, Signage):
    def __init__(self, device, viewport, font, fontBold, fontBoldTall, fontBoldLarge):
        super().__init__(device, viewport, font, fontBold, fontBoldTall, fontBoldLarge)

        with canvas(device) as draw:
            # construct all the areas of display
            # Top line - Welcome
            welcomeTo = StaticText(self.width, 10, self.fontBold, "Welcome to", halign=HAlign.CENTER)
            self.stationName = StaticText(self.width, 10, self.fontBold, None, halign=HAlign.CENTER)
            dots = StaticText(self.width, 10, self.fontBold, ".  .  .")
            rowTime = Clock(self.width, 14, self.fontBoldLarge, self.fontBoldTall)
            viewport.add_hotspot(welcomeTo, (0, 0))
            viewport.add_hotspot(self.stationName, (0, 12))
            viewport.add_hotspot(dots, (0, 24))
            viewport.add_hotspot(rowTime, (0, 50))

    def update(self, data):
        departures, destinations, departureStation = data
        self.stationName.text = departureStation
        # This class doesn't animate so it's always ready to load new data
        self.end()
