#!/bin/bash

echo "Service start"

demo=${demo:-false}

# if [ ! -f config.json ]; then
  echo "Generating config.json"
  cp config.sample.json config.json
  jq .journey.departureStation=\""${departureStation}"\" config.json | sponge config.json
  jq .journey.destinationStation=\""${destinationStation}"\" config.json | sponge config.json
  jq .journey.outOfHoursName=\""${outOfHoursName}"\" config.json | sponge config.json
  jq .refreshTime="${refreshTime}" config.json | sponge config.json
  jq .transportApi.demo="${demo}" config.json | sponge config.json
  jq .transportApi.appId=\""${transportApi_appId}"\" config.json | sponge config.json
  jq .transportApi.apiKey=\""${transportApi_apiKey}"\" config.json | sponge config.json
  jq .transportApi.operatingHours=\""${transportApi_operatingHours}"\" config.json | sponge config.json
# fi

# cat config.json

python ./src/main.py
