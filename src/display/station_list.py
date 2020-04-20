from display import HAlign
from display.static_text import StaticText
# from PIL import Image, ImageDraw

class StationList(StaticText):
    """Render a list of stations"""
    def __init__(self, width, height, font, destinations=None, halign=HAlign.LEFT):
        super().__init__(width, height, font, halign=halign)
        self.destinationText = None
        self.image = None
        self.x = 0
        self.y = 0
        self.destinations = destinations

    @property
    def destinations(self):
        return self.__destinations

    @destinations.setter
    def destinations(self, destinations):
        self.__destinations = destinations
        if destinations and len(destinations) > 0:
            destinationText = ", ".join(destinations)
        else:
            destinationText = ""
        # destinationText = ". . . . . . . . . . . . . . . ."
        if self.destinationText != destinationText:
            self.totalWidth = None
            self.destinationText = destinationText

    def should_redraw(self):
        return True

    def update(self, draw):
        if not self.totalWidth:
            size = draw.textsize(self.destinationText, self.font)
            self.totalWidth = size[0]
        # if not self.image:
        #     self.image = Image.new(draw.mode, self.size)
        #     imDraw = ImageDraw.Draw(self.image)
        #     imDraw.text((0,0), text=self.destinationText, width=self.width, font=self.font, fill="yellow")
        #     del imDraw

        pos = (self.x, self.y)
        # print("\"{}\" at {}".format(self.destinationText, pos))
        draw.text(pos, text=self.destinationText, width=self.width, font=self.font, fill="yellow")
        # draw.
        self.x -= 1
        if self.x + self.totalWidth < 0:
            self.x = 0

