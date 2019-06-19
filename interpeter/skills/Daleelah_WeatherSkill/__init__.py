
import json
import sys
from adapt.intent import IntentBuilder

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


weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherType")\
    .require("Location")\
    .build()



def getEntities():
    return {
        "WeatherKeyword" : weather_keyword,
        "Location" : locations,
        "WeatherType": weather_types
    }

def getRegexEntities():
    return {}

def getMap():
    return {
        weather_intent.name : printing
    }
def printing():
    print("I'm inside weather intent")


def getIntents():
    return [weather_intent]

def getTxt():
    return "HEY FROM HELLO"


if __name__ == "__main__":
    print(getIntents())