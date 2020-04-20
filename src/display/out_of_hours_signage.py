from display.signage import Signage
from display.static_text import StaticText
from display.clock import Clock

from luma.core.render import canvas

class OutOfHoursSignage(Signage):
    def __init__(self, device, viewport, font, fontBold, fontBoldTall, fontBoldLarge):
        super().__init__(device, viewport, font, fontBold, fontBoldTall, fontBoldLarge)

        # with canvas(device) as draw:
            #     welcomeTo = StaticText(width, 10, fontBold, "Welcome to", halign=HAlign.CENTER)
#     stationName = StaticText(width, 10, fontBold, departureStation, halign=HAlign.CENTER)
#     dots = StaticText(width, 10, fontBold, ".  .  .")

#     if len(virtualViewport._hotspots) > 0:
#         for hotspot, xy in virtualViewport._hotspots:
#             print("Removing hotspot {} at location {}".format(hotspot, xy))
#             virtualViewport.remove_hotspot(hotspot, xy)

#     rowTime = Clock(width, 14, fontBoldLarge, fontBoldTall) #snapshot(width, 14, renderTime, interval=0.25)

#     virtualViewport.add_hotspot(welcomeTo, (0, 0))
#     virtualViewport.add_hotspot(stationName, (0, 12))
#     virtualViewport.add_hotspot(dots, (0, 24))
#     virtualViewport.add_hotspot(rowTime, (0, 50))
