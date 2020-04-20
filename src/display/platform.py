from display import HAlign
from display.static_text import StaticText

class Platform(StaticText):
    """Render some static text"""
    def __init__(self, width, height, font, departure, fixed_text="Plat 88", halign=HAlign.LEFT):
        super().__init__(width, height, font, fixed_text=fixed_text, halign=halign)
        self.departure  = departure

    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, departure):
        self.__departure = departure

        if departure:
            if departure["mode"] == "bus":
                self.text = "BUS"
            else:
                self.text = "Plat " + departure["platform"]
        else:
            self.text = ""
