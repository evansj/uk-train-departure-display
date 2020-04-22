import os
import sys
import time
import json

from datetime import datetime, timedelta
from timeloop import Timeloop
from PIL import ImageFont, Image

from data_fetcher import DataFetcher
from display import HAlign
from display.clock import Clock
from display.static_text import StaticText
from display.departure_line import DepartureLine
from display.departure_signage import DepartureSignage
from display.out_of_hours_signage import OutOfHoursSignage

from luma.core.interface.serial import spi
from luma.oled.device import ssd1322
from luma.core.virtual import viewport
from luma.core.sprite_system import framerate_regulator

from open import isRun

def loadConfig():
    """Read and parse the config file"""
    with open('config.json', 'r') as jsonConfig:
        data = json.load(jsonConfig)
        return data

def makeFont(name, size):
    """Returns a TrueType font for the given name and size"""
    font_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'fonts',
            name
        )
    )
    return ImageFont.truetype(font_path, size)

try:
    config = loadConfig()

    apiConfig = config["transportApi"]

    serial = spi()
    device = ssd1322(serial, mode="1", rotate=2)
    font = makeFont("Dot Matrix Regular.ttf", 10)
    fontBold = makeFont("Dot Matrix Bold.ttf", 10)
    fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
    fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 20)

    widgetWidth = 256
    widgetHeight = 64

    regulator = framerate_regulator(fps=60)

    virtualViewport = viewport(device, width=widgetWidth, height=widgetHeight)

    fetcher = DataFetcher(config["journey"], apiConfig, interval=config["refreshTime"])
    fetcher.start()

    signage = None

    # loop timing
    # start_time = datetime.today().timestamp()

    while True:
        with regulator:
            if fetcher.hasChanged():
                print("New data received")
                # Make sure we are displaying the correct signage
                if fetcher.is_out_of_hours():
                    if not isinstance(signage, OutOfHoursSignage):
                        print("out of hours, constructing new OutOfHoursSignage")
                        signage = OutOfHoursSignage(device, virtualViewport, font, fontBold, fontBoldTall, fontBoldLarge)
                else:
                    if not isinstance(signage, DepartureSignage):
                        print("normal hours, constructing new DepartureSignage")
                        signage = DepartureSignage(device, virtualViewport, font, fontBold, fontBoldTall, fontBoldLarge)

                data = (fetcher.departures, fetcher.destination_stations, fetcher.station_name)
                signage.update(data)

            virtualViewport.refresh()
        # time_now = datetime.today().timestamp()
        # time_diff = time_now - start_time
        # if time_diff > 10:
            # at least 10 seconds have elapsed
            # print("FPS {}".format(regulator.effective_FPS()))
            # start_time = time_now

except KeyboardInterrupt:
    pass
except ValueError as err:
    print(f"Error: {err}")
except KeyError as err:
    print(f"Error: Please ensure the {err} environment variable is set")
