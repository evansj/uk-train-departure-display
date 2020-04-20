from display import HAlign
from display.static_text import StaticText

class Destination(StaticText):
    """Render the destination"""
    def __init__(self, width, height, font, departure, fixed_text=None, halign=HAlign.LEFT):
        super().__init__(width, height, font, fixed_text=fixed_text, halign=halign)
        self.departure  = departure

    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, departure):
        self.__departure = departure

        if departure:
            departureTime = departure["aimed_departure_time"]
            destinationName = departure["destination_name"]
            self.text = f"{departureTime}  {destinationName}"
        else:
            self.text = ""
