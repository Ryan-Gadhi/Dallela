
import json
import sys
from adapt.intent import IntentBuilder
from base import Skill, Handler

# TODO: each intent should be in a separate JOSN file
weather_keyword = [
    "weather"
]

weather_types = [
    "snow",
    "rain",
    "wind",
    "sleet",
    "sun"
]

locations = [
    "Seattle",
    "San Francisco",
    "Tokyo"
]

entities = {
            "WeatherKeyword" : weather_keyword,
            "Location" : locations,
            "WeatherType": weather_types
}


weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()


def weatherFunc():
    print("Weather intent function executed!")
       
class weatherSkill(Skill):
    def __init__(self):
        super().__init__( 
            [Handler(weather_intent, weatherFunc, "")],
            entities,
            [],
            "WeatherSkill")
        







def getSkill():
    return weatherSkill()