from display import HAlign
from luma.core.virtual import hotspot
from display.destination import Destination

class DepartureLine(hotspot):
    """
    Render a departure line

    HH:MM Destination Station       Plat 88     On time
    """
    def __init__(self, width, height, font, fontBold, departure, bold=False):
        super().__init__(width, height)
        self.font        = font
        self.fontBold    = fontBold
        self.bold        = bold

        self.statusText      = None
        self.platformText    = None
        self.destinationText = None
        self.statusWidth     = None
        self.platformWidth   = None
        self.dirty           = True
        self.departure       = departure

    def __str__(self):
        return "DepartureLine(width={}, height={})".format(self.width, self.height)

    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, departure):
        self.__departure = departure
        self.status(departure)
        self.platform(departure)
        self.destination(departure)

    def status(self, departure):
        text = None
        if departure:
            if departure["status"] == "CANCELLED":
                text = "Cancelled"
            else:
                if departure["aimed_departure_time"] == departure["expected_departure_time"]:
                    text = "On time"
                elif isinstance(departure["expected_departure_time"], str):
                    text = 'Exp ' + departure["expected_departure_time"]
        if text != self.statusText:
            self.statusText = text
            self.dirty = True

    def platform(self, departure):
        text = None
        if departure:
            if departure["mode"] == "bus":
                text = "BUS"
            else:
                text = "Plat " + departure["platform"]
        if text != self.platformText:
            self.platformText = text
            self.dirty = True

    def destination(self, departure):
        text = None
        if departure:
            departureTime = departure["aimed_departure_time"]
            destinationName = departure["destination_name"]
            text = f"{departureTime}  {destinationName}"
        if text != self.destinationText:
            self.destinationText = text
            self.dirty = True

    def should_redraw(self):
        return self.dirty

    def update(self, draw):
        # Calculate some fixed widths
        if not self.statusWidth:
            self.statusWidth, h = draw.textsize("Exp 00:00", self.font)
        if not self.platformWidth:
            self.platformWidth, h = draw.textsize("Plat 88", self.font)

        # Destination
        if self.destinationText:
            # print("\"{}\" at {}, width={}".format(self.destinationText, (0, 0), self.width - self.statusWidth - self.platformWidth))
            draw.text(
                (0, 0),
                text=self.destinationText,
                font=self.fontBold if self.bold else self.font,
                width=self.width - self.statusWidth - self.platformWidth,
                fill="yellow")
        # Platform
        if self.platformText:
            # print("\"{}\" at {}, width={}".format(self.platformText, (self.width - self.statusWidth - self.platformWidth, 0), self.statusWidth))
            draw.text(
                (self.width - self.statusWidth - self.platformWidth, 0),
                text=self.platformText,
                font=self.font,
                width=self.platformWidth,
                fill="yellow")
        # Status
        if self.statusText:
            # This needs to be right aligned
            size = draw.textsize(self.statusText, self.font)
            x = self.width - size[0]
            # print("\"{}\" at {}, width={}".format(self.statusText, (x, 0), self.statusWidth))
            draw.text(
                (x, 0),
                text=self.statusText,
                font=self.font,
                width=self.statusWidth,
                fill="yellow")
        self.dirty = False
