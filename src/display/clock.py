from luma.core.virtual import hotspot
from datetime import datetime

class Clock(hotspot):
    """Render the clock"""
    def __init__(self, width, height, minutesFont, secondsFont):
        super().__init__(width, height)
        self.minutesFont       = minutesFont
        self.secondsFont       = secondsFont
        self.secondsDrawn      = None
        self.hoursMinutesWidth = None
        self.secondsWidth      = None

    def __str__(self):
        return "Clock(width={}, height={})".format(self.width, self.height)

    def should_redraw(self):
        """
        Return True if the seconds value has changed since the last time we drew
        """
        t = datetime.now().time()
        return self.secondsDrawn != t.second

    def update(self, draw):
        if self.hoursMinutesWidth is None:
            self.hoursMinutesWidth, h1 = draw.textsize("00:00", self.minutesFont)
            self.secondsWidth, h2 = draw.textsize(":00", self.secondsFont)
            self.hmPosition = ((self.width - self.hoursMinutesWidth - self.secondsWidth) / 2, 0)
            self.secPosition = (((self.width - self.hoursMinutesWidth - self.secondsWidth) / 2) + self.hoursMinutesWidth, 5)

        t = datetime.now().time()
        self.secondsDrawn = t.second
        draw.text(self.hmPosition, text="{:02d}:{:02d}".format(t.hour, t.minute),
                font=self.minutesFont, fill="yellow")
        draw.text(self.secPosition, text=":{:02d}".format(t.second),
                font=self.secondsFont, fill="yellow")
