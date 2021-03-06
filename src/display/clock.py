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
        self.lastDrawnChars    = [None] * 8

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
    def buildCache(self, mode):
        if not self.cachedLargeDigits:
            self.cachedLargeDigits, self.largeDigitSize = self.createDigitImages(mode, self.minutesFont, range(10))
            self.cachedSmallDigits, self.smallDigitSize = self.createDigitImages(mode, self.secondsFont, range(10))
            self.cachedLargeColon,  self.largeColonSize = self.createImage(mode, self.minutesFont, ":")
            self.cachedSmallColon,  self.smallColonSize = self.createImage(mode, self.secondsFont, ":")
            self.largeDigitWidth = self.largeDigitSize[0]
            self.smallDigitWidth = self.smallDigitSize[0]
            self.largeColonWidth = self.largeColonSize[0]
            self.smallColonWidth = self.smallColonSize[0]
            # Calculate the overall width needed for the clock
            self.width = (2* self.largeDigitWidth) + self.largeColonWidth + \
                         (2* self.largeDigitWidth) + \
                         self.smallColonWidth + (2* self.smallDigitWidth)

    def createDigitImages(self, mode, font, range):
        images = []
        sizeImage = Image.new(mode, (50, 50))
        draw = ImageDraw.Draw(sizeImage)
        size = draw.textsize("0", font)
        for digit in range:
            digitImage = Image.new(mode, size)
            draw = ImageDraw.Draw(digitImage)
            # need to draw it in the centre, so we need its size
            dSize = draw.textsize(str(digit), font)
            pos = ((size[0] - dSize[0]) // 2, 0)
            draw.text(pos, text=str(digit), font=font, fill="yellow")
            images.append(digitImage)

        # print("Generated {} digit images, size {}".format(len(images), size))
        return images, size

    def createImage(self, mode, font, str):
        # Measure the text
        sizeImage = Image.new(mode, (50, 50))

        draw = ImageDraw.Draw(sizeImage)
        size = draw.textsize(str, font)
        del draw
        del sizeImage

        # Create a new image large enough
        strImage = Image.new(mode, size)
        draw = ImageDraw.Draw(strImage)

        # Draw the text into the image
        draw.text((0,0), text=str, font=font, fill="yellow")

        # print("Generated an image for \"{}\", size {}".format(str, size))
        return strImage, size

    def getClockChars(self, t):
        hours   = [int(digit) for digit in str("{:02d}".format(t.hour))]
        minutes = [int(digit) for digit in str("{:02d}".format(t.minute))]
        seconds = [int(digit) for digit in str("{:02d}".format(t.second))]
        return hours + [":"] + minutes + [":"] + seconds

    def getClockCharImages(self, chars):
        # All of the images we are going to draw to the display
        return [
            self.cachedLargeDigits[chars[0]],
            self.cachedLargeDigits[chars[1]],
            self.cachedLargeColon,
            self.cachedLargeDigits[chars[3]],
            self.cachedLargeDigits[chars[4]],
            self.cachedSmallColon,
            self.cachedSmallDigits[chars[6]],
            self.cachedSmallDigits[chars[7]]
        ]

    def paste_into(self, image, xy):
        # image is the whole screen. xy is the top left corner of the clock row
        self.buildCache(image.mode)

        t = datetime.now().time()
        self.secondsDrawn = t.second

        chars = self.getClockChars(t)
        # print("hmsChars={}".format(chars))
        charImages = self.getClockCharImages(chars)
        # print("charImages={}".format(charImages))

        # Calculate x pos of first digit
        x = xy[0] + ((image.width - self.width) // 2)
        base = xy[1] + charImages[0].height
        for i, c in enumerate(charImages):
            # Only repaint changed digits:
            if chars[i] != self.lastDrawnChars[i]:
                # Everything sits on the baseline
                y = base - c.height
                image.paste(c, (x, y))
            x += c.width

        # Remember what we drew
        self.lastDrawnChars = chars
