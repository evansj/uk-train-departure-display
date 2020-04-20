from luma.core.virtual import hotspot
from display import HAlign

class StaticText(hotspot):
    """Render some static text"""
    def __init__(self, width, height, font, text="", fixed_text=None, halign=HAlign.LEFT):
        super().__init__(width, height)
        self.font       = font
        self.__text     = None
        self.text       = text
        self.fixed_text = fixed_text
        self.halign     = halign
        self.dirty      = True

    def __str__(self):
        return "StaticText(width={}, height={}, text={})".format(self.width, self.height, self.text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        if self.__text != text:
            # print("The text \"{}\" is different to \"{}\", setting dirty=True".format(self.__text, text))
            self.__text = text
            self.dirty  = True

    def should_redraw(self):
        return self.dirty

    def measure(self, draw):
        return draw.textsize(self.fixed_text or self.text, self.font)

    def setFixedWidth(self, draw):
        """Set the width of this widget to its current width"""
        size = self.measure(draw)
        self.width = size[0]

    def update(self, draw):
        if self.halign == HAlign.CENTER:
            size = draw.textsize(self.text, self.font)
            x = (self.width - size[0]) // 2 # floor division so we don't get pixel fractions
        elif self.halign == HAlign.RIGHT:
            size = draw.textsize(self.text, self.font)
            x = self.width - size[0]
        else:
            x = 0

        y = 0
        pos = (x, y)
        draw.text(pos, text=self.text, font=self.font, fill="yellow")
        # print("Wrote \"{}\" at {}, {}".format(self.text, pos, self.halign))
        self.dirty = False
