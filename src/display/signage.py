class Signage(object):
    pass

    def __init__(self, device, viewport, font, fontBold, fontBoldTall, fontBoldLarge, height=10, tallHeight=14):
        self.stationRenderCount = 0
        self.pauseCount         = 0
        self.device             = device
        self.viewport           = viewport
        self.font               = font
        self.fontBold           = fontBold
        self.fontBoldTall       = fontBoldTall
        self.fontBoldLarge      = fontBoldLarge
        self.width              = self.viewport.width
        self.height             = height
        self.tallHeight         = tallHeight

        if len(viewport._hotspots) > 0:
            for hotspot, xy in viewport._hotspots:
                print("Removing hotspot {} at location {}".format(hotspot, xy))
                viewport.remove_hotspot(hotspot, xy)

    def update(self, data):
        pass

