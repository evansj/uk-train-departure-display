# Code investigation

## Operation

Transport API returns data containing all services from the home station to the destination station. It is then called again to get all of the stops for the first service. Stops before the home station are removed from the list.

### trains#loadDeparturesForStation

Returns a tuple containing the `departures.all` array from the transport api, and the name of the home station.

### trains#loadDestinationsForDeparture

Returns an array of station names. If there is only one entry in the array it is modified to append the string " only.".

e.g.

```json
["Bicester North", "London Marylebone"]

["London Marylebone only."]
```


## Transport API

### loadDeparturesForStation

Raw data:

```json
{
    "date": "2020-04-19",
    "time_of_day": "15:27",
    "request_time": "2020-04-19T15:27:30+01:00",
    "station_name": "Banbury",
    "station_code": "BAN",
    "departures": {
        "all": [
            {
                "mode": "train",
                "service": "25530004",
                "train_uid": "C78635",
                "platform": "3",
                "operator": "CH",
                "operator_name": "Chiltern Railways",
                "aimed_departure_time": "16:07",
                "aimed_arrival_time": "16:03",
                "aimed_pass_time": null,
                "origin_name": "Birmingham Moor Street",
                "destination_name": "London Marylebone",
                "source": "Network Rail",
                "category": "XX",
                "service_timetable": {
                    "id": "http://transportapi.com/v3/uk/train/service/train_uid:C78635/2020-04-19/timetable.json?app_id=APP_ID&app_key=APP_KEY&live=true"

                },
                "status": "LATE",
                "expected_arrival_time": "16:03",
                "expected_departure_time": "16:07",
                "best_arrival_estimate_mins": 35,
                "best_departure_estimate_mins": 39
            },
            {
                "mode": "train",
                "service": "25530004",
                "train_uid": "C78632",
                "platform": "3",
                "operator": "CH",
                "operator_name": "Chiltern Railways",
                "aimed_departure_time": "17:04",
                "aimed_arrival_time": "17:03",
                "aimed_pass_time": null,
                "origin_name": "Birmingham Moor Street",
                "destination_name": "London Marylebone",
                "source": "Network Rail",
                "category": "XX",
                "service_timetable": {
                    "id": "http://transportapi.com/v3/uk/train/service/train_uid:C78632/2020-04-19/timetable.json?app_id=APP_ID&app_key=APP_KEY&live=true"

                },
                "status": "ON TIME",
                "expected_arrival_time": "17:03",
                "expected_departure_time": "17:04",
                "best_arrival_estimate_mins": 95,
                "best_departure_estimate_mins": 96
            }
        ]
    }
}
```

### loadDestinationsForDeparture

Raw data:

```json
{
    "service": "25530004",
    "train_uid": "C78635",
    "headcode": "7116",
    "toc": {
        "atoc_code": "CH"
    },
    "train_status": "P",
    "origin_name": "Birmingham Moor Street",
    "destination_name": "London Marylebone",
    "stop_of_interest": null,
    "date": "2020-04-19",
    "time_of_day": null,
    "mode": "train",
    "request_time": "2020-04-19T15:31:49+01:00",
    "category": "XX",
    "operator": "CH",
    "operator_name": "Chiltern Railways",
    "stops": [
        {
            "station_code": "BMO",
            "tiploc_code": "BHAMMRS",
            "station_name": "Birmingham Moor Street",
            "stop_type": "LO",
            "platform": "4",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "15:15",
            "aimed_arrival_date": null,
            "aimed_arrival_time": null,
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": null,
            "expected_departure_time": null,
            "expected_arrival_date": null,
            "expected_arrival_time": null,
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": null
        },
        {
            "station_code": "SOL",
            "tiploc_code": "SOLIHUL",
            "station_name": "Solihull",
            "stop_type": "LI",
            "platform": null,
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "15:24",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "15:23",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": null,
            "expected_departure_time": null,
            "expected_arrival_date": null,
            "expected_arrival_time": null,
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": null
        },
        {
            "station_code": "DDG",
            "tiploc_code": "DORIDGE",
            "station_name": "Dorridge",
            "stop_type": "LI",
            "platform": "1",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "15:29",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "15:28",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": null,
            "expected_departure_time": null,
            "expected_arrival_date": null,
            "expected_arrival_time": null,
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": null
        },
        {
            "station_code": "WRP",
            "tiploc_code": "WARWPWY",
            "station_name": "Warwick Parkway",
            "stop_type": "LI",
            "platform": "1",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "15:39",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "15:38",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "15:39",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "15:38",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "WRW",
            "tiploc_code": "WARWICK",
            "station_name": "Warwick",
            "stop_type": "LI",
            "platform": null,
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "15:42",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "15:42",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "15:42",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "15:42",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "LMS",
            "tiploc_code": "LMNGTNS",
            "station_name": "Leamington Spa",
            "stop_type": "LI",
            "platform": "3",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "15:46",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "15:46",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "15:46",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "15:46",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "BAN",
            "tiploc_code": "BNBR",
            "station_name": "Banbury",
            "stop_type": "LI",
            "platform": "3",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "16:07",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "16:03",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "16:07",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "16:03",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "BCS",
            "tiploc_code": "BCSTN",
            "station_name": "Bicester North",
            "stop_type": "LI",
            "platform": "2",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "16:19",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "16:18",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "16:19",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "16:18",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "HDM",
            "tiploc_code": "HADMATP",
            "station_name": "Haddenham & Thame Parkway",
            "stop_type": "LI",
            "platform": "2",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "16:31",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "16:30",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "16:31",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "16:30",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "PRR",
            "tiploc_code": "PRINRIS",
            "station_name": "Princes Risborough",
            "stop_type": "LI",
            "platform": "2",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "16:39",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "16:38",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "16:39",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "16:38",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "HWY",
            "tiploc_code": "HWYCOMB",
            "station_name": "High Wycombe",
            "stop_type": "LI",
            "platform": "3",
            "aimed_departure_date": "2020-04-19",
            "aimed_departure_time": "16:48",
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "16:48",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": "2020-04-19",
            "expected_departure_time": "16:48",
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "16:48",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        },
        {
            "station_code": "MYB",
            "tiploc_code": "MARYLBN",
            "station_name": "London Marylebone",
            "stop_type": "LT",
            "platform": "2",
            "aimed_departure_date": null,
            "aimed_departure_time": null,
            "aimed_arrival_date": "2020-04-19",
            "aimed_arrival_time": "17:15",
            "aimed_pass_date": null,
            "aimed_pass_time": null,
            "expected_departure_date": null,
            "expected_departure_time": null,
            "expected_arrival_date": "2020-04-19",
            "expected_arrival_time": "17:15",
            "expected_pass_date": null,
            "expected_pass_time": null,
            "status": "ON TIME"
        }
    ]
}
```
