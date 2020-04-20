import threading
import time
import requests
import json
from open import isRun

class DataFetcher(object):
    """Fetch data on a background thread"""
    def __init__(self, journeyConfig, apiConfig, interval=120):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval      = interval
        self.journeyConfig = journeyConfig
        self.apiConfig     = apiConfig
        self.appId         = apiConfig["appId"]
        self.apiKey        = apiConfig["apiKey"]
        self.demo          = apiConfig["demo"]
        self.out_of_hours  = False
        self.changed       = False

        # These variables contain the data to render
        self.departures           = []
        self.destination_stations = []
        self.station_name         = ""

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Loop to load data """
        while True:
            print('Refreshing data')
            changed = False

            out_of_hours = self.is_out_of_hours()
            if self.out_of_hours != out_of_hours:
                changed = True

            departures, station_name = self.loadDeparturesForStation()
            if len(departures) == 0:
                destination_stations = []
            else:
                destination_stations = self.loadDestinationsForDeparture(departures[0]["service_timetable"]["id"])

            if self.departures != departures:
                self.departures = departures
                changed = True
            if self.station_name != station_name:
                self.station_name = station_name
                changed = True
            if self.destination_stations != destination_stations:
                self.destination_stations = destination_stations
                changed = True

            self.changed = self.changed or changed

            time.sleep(self.interval)

    def abbrStation(self, inputStr):
        dict = self.journeyConfig['stationAbbr']
        for key in dict.keys():
            inputStr = inputStr.replace(key, dict[key])
        return inputStr

    def hasChanged(self):
        changed = self.changed
        self.changed = False
        return changed

    def is_out_of_hours(self):
        runHours = [int(x) for x in self.apiConfig['operatingHours'].split('-')]
        return not isRun(runHours[0], runHours[1]) == False

    def loadDeparturesForStation(self):
        print("loadDeparturesForStation() demo={}".format(self.demo))
        if self.demo:
            with open('src/demo/departures.json', 'r') as departureData:
                data = json.load(departureData)

        else:
            if self.journeyConfig["departureStation"] == "":
                raise ValueError(
                    "Please set the journey.departureStation property in config.json")

            if self.appId == "" or self.apiKey == "":
                raise ValueError(
                    "Please complete the transportApi section of your config.json file")

            departureStation = self.journeyConfig["departureStation"]
            if self.out_of_hours:
                return [], journeyConfig['outOfHoursName']
            else:
                URL = f"http://transportapi.com/v3/uk/train/station/{departureStation}/live.json"

                PARAMS = {'app_id': self.appId,
                        'app_key': self.apiKey,
                        'calling_at': self.journeyConfig["destinationStation"]}

                print("Fetching online data")
                r = requests.get(url=URL, params=PARAMS)

                data = r.json()

        #apply abbreviations / replacements to station names (long stations names dont look great on layout)
        #see config file for replacement list
        for item in data["departures"]["all"]:
            item['origin_name'] = self.abbrStation(item['origin_name'])
            item['destination_name'] = self.abbrStation(item['destination_name'])

        if "error" in data:
            raise ValueError(data["error"])

        return data["departures"]["all"], data["station_name"]


    def loadDestinationsForDeparture(self, timetableUrl):
        print("loadDestinationsForDeparture() demo={}".format(self.demo))
        if self.demo:
            with open('src/demo/destinations.json', 'r') as destinationData:
                data = json.load(destinationData)
        else:
            if self.out_of_hours:
                return []
            else:
                print("Fetching online data")
                r = requests.get(url=timetableUrl)
                data = r.json()

        #apply abbreviations / replacements to station names (long stations names dont look great on layout)
        #see config file for replacement list
        foundDepartureStation = False

        for item in list(data["stops"]):
            if item['station_code'] == self.journeyConfig['departureStation']:
                foundDepartureStation = True

            if foundDepartureStation == False:
                data["stops"].remove(item)
                continue

            item['station_name'] = self.abbrStation(item['station_name'])

        if "error" in data:
            raise ValueError(data["error"])

        departureDestinationList = list(map(lambda x: x["station_name"], data["stops"]))[1:]

        if len(departureDestinationList) == 1:
            departureDestinationList[0] = departureDestinationList[0] + ' only.'

        return departureDestinationList
