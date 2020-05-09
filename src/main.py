import os
import sys
import time
import json
import argparse
import logging
logging.basicConfig()
logging.getLogger('display.calling_at').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

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
from display.animated_viewport import AnimatedViewport

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

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(usage="%(prog)s [OPTION]")
    parser.add_argument("-g", "--gif", action='store_true')
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    try:

        config = loadConfig()

        apiConfig = config["transportApi"]

        font = makeFont("Dot Matrix Regular.ttf", 10)
        fontBold = makeFont("Dot Matrix Bold.ttf", 10)
        fontBoldTall = makeFont("Dot Matrix Bold Tall.ttf", 10)
        fontBoldLarge = makeFont("Dot Matrix Bold.ttf", 20)

        screenWidth = 256
        screenHeight = 64

        regulator = framerate_regulator(fps=70)

        if args.gif:
            from luma.emulator.device import gifanim
            device = gifanim(width=screenWidth, height=screenHeight, scale=1,
                mode='RGB', filename='uk_trains.gif')
        else:
            serial = spi()
            device = ssd1322(serial, mode="1", rotate=2)

        animatedViewport = AnimatedViewport(device, width=screenWidth, height=screenHeight)

        fetcher = DataFetcher(config["journey"], apiConfig, interval=config["refreshTime"])
        fetcher.start()

        signage = None

        # loop timing
        start_time = datetime.today().timestamp()

        cycle_count = 0

        # Wait for the first data to load
        while not fetcher.ready:
            time.sleep(0.5)

        while True:
            with regulator:
                if fetcher.has_changed:
                    logger.debug("New data received")
                    animatedViewport.stop()
                if animatedViewport.stopped:
                    logger.debug("Updating signage with new data")
                    # Make sure we are displaying the correct signage
                    if fetcher.is_out_of_hours():
                        if not isinstance(signage, OutOfHoursSignage):
                            logger.debug("out of hours, constructing new OutOfHoursSignage")
                            signage = OutOfHoursSignage(device, animatedViewport, font, fontBold, fontBoldTall, fontBoldLarge)
                    else:
                        if not isinstance(signage, DepartureSignage):
                            logger.debug("normal hours, constructing new DepartureSignage")
                            signage = DepartureSignage(device, animatedViewport, font, fontBold, fontBoldTall, fontBoldLarge)

                    data = (fetcher.departures, fetcher.destination_stations, fetcher.station_name)
                    signage.update(data)
                    animatedViewport.run()
                    if args.gif and cycle_count >= 2:
                        print("Exiting after {} animation cycles".format(cycle_count))
                        sys.exit()
                    cycle_count += 1

                animatedViewport.refresh()
            time_now = datetime.today().timestamp()
            time_diff = time_now - start_time
            if time_diff > 10:
                # at least 10 seconds have elapsed
                logger.debug("FPS {}".format(regulator.effective_FPS()))
                start_time = time_now

    except KeyboardInterrupt:
        pass
    except ValueError as err:
        print(f"Error: {err}")
    except KeyError as err:
        print(f"Error: Please ensure the {err} environment variable is set")

if __name__ == "__main__":
    main()
