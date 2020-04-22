from luma.core.virtual import hotspot
from datetime import datetime
from PIL import Image, ImageDraw

class Clock(hotspot):
    """Render the clock"""
    def __init__(self, width, height, minutesFont, secondsFont):
        super().__init__(width, height)
        self.minutesFont       = minutesFont
        self.secondsFont       = secondsFont
        self.secondsDrawn      = None
        self.cachedLargeDigits = None
        self.cachedSmallDigits = None
        self.cachedLargeColon  = None
        self.cachedSmallColon  = None
        self.largeDigitSize    = None
        self.smallDigitSize    = None
        self.largeColonSize    = None
        self.smallColonSize    = None
        self.largeDigitWidth   = None
        self.smallDigitWidth   = None
        self.largeColonWidth   = None
        self.smallColonWidth   = None

    def __str__(self):
        return "Clock(width={}, height={})".format(self.width, self.height)

    def should_redraw(self):
        """
        Return True if the seconds value has changed since the last time we drew
        """
        t = datetime.now().time()
        return self.secondsDrawn != t.second

    # We cache images for all digits and colons.
    # This seems like overkill but it is a lot faster to paste an image to the screen
    # than it is to write text to the screen
    def buildCache(self, image):
        if not self.cachedLargeDigits:
            self.cachedLargeDigits, self.largeDigitSize = self.createDigitImages(image, self.minutesFont, range(10))
            self.cachedSmallDigits, self.smallDigitSize = self.createDigitImages(image, self.secondsFont, range(10))
            self.cachedLargeColon,  self.largeColonSize = self.createImage(image, self.minutesFont, ":")
            self.cachedSmallColon,  self.smallColonSize = self.createImage(image, self.secondsFont, ":")
            self.largeDigitWidth = self.largeDigitSize[0]
            self.smallDigitWidth = self.smallDigitSize[0]
            self.largeColonWidth = self.largeColonSize[0]
            self.smallColonWidth = self.smallColonSize[0]
            # Calculate the overall width needed for the clock
            self.width = (2* self.largeDigitWidth) + self.largeColonWidth + \
                         (2* self.largeDigitWidth) + \
                         self.smallColonWidth + (2* self.smallDigitWidth)

    def createDigitImages(self, image, font, range):
        images = []
        draw = ImageDraw.Draw(image)
        size = draw.textsize("0", font)
        for digit in range:
            digitImage = Image.new(draw.mode, size)
            imDraw = ImageDraw.Draw(digitImage)
            # need to draw it in the centre, so we need its size
            dSize = draw.textsize(str(digit), font)
            pos = ((size[0] - dSize[0]) // 2, 0)
            imDraw.text(pos, text=str(digit), font=font, fill="yellow")
            images.append(digitImage)
            del imDraw
        del draw

        # print("Generated {} digit images, size {}".format(len(images), size))
        return images, size

    def createImage(self, image, font, str):
        # Measure the text
        draw = ImageDraw.Draw(image)
        size = draw.textsize(str, font)

        # Create a new image large enough
        strImage = Image.new(draw.mode, size)
        imDraw = ImageDraw.Draw(strImage)

        # Draw the text into the image
        imDraw.text((0,0), text=str, font=font, fill="yellow")
        del imDraw
        del draw

        # print("Generated an image for \"{}\", size {}".format(str, size))
        return strImage, size

    def paste_into(self, image, xy):
        # image is the whole screen. xy is the top left corner of the clock row
        self.buildCache(image)

        t = datetime.now().time()
        self.secondsDrawn = t.second

        hours   = [int(digit) for digit in str("{:02d}".format(t.hour))]
        minutes = [int(digit) for digit in str("{:02d}".format(t.minute))]
        seconds = [int(digit) for digit in str("{:02d}".format(t.second))]

        # Calculate x pos of first hour digit
        clockChars = [
            self.cachedLargeDigits[hours[0]],
            self.cachedLargeDigits[hours[1]],
            self.cachedLargeColon,
            self.cachedLargeDigits[minutes[0]],
            self.cachedLargeDigits[minutes[1]],
            self.cachedSmallColon,
            self.cachedSmallDigits[seconds[0]],
            self.cachedSmallDigits[seconds[1]]
        ]

        # Calculate x pos of first digit
        x = xy[0] + ((image.width - self.width) // 2)

        height = clockChars[0].height
        for c in clockChars:
            # Everything sits on the baseline
            y = xy[1] + (height - c.height)
            image.paste(c, (x, y))
            x += c.width
