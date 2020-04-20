from display import HAlign
from display.static_text import StaticText

class ServiceStatus(StaticText):
    """Render some static text"""
    def __init__(self, width, height, font, departure, fixed_text="Exp 00:00", halign=HAlign.RIGHT):
        super().__init__(width, height, font, fixed_text=fixed_text, halign=halign)
        self.departure  = departure

    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, departure):
        self.__departure = departure
        text = ""
        if departure:
            if departure["status"] == "CANCELLED":
                text = "Cancelled"
            else:
                if departure["aimed_departure_time"] == departure["expected_departure_time"]:
                    text = "On time"
                elif isinstance(departure["expected_departure_time"], str):
                    text = 'Exp ' + departure["expected_departure_time"]
        # print("ServiceStatus, setting text to \"{}\"".format(text))
        self.text = text
