
import json
import sys
from adapt.intent import IntentBuilder

hello_keyword = [
    "Hello",
    "Hey", 
    "Hi"
]

howareyou_keyword = [
    "How are you",
    "What is up",
    "How is it going",
    "What is new",
    "What is going on",
    "How are things",
    "How is life",
    "How is your day",
    "How have you been",
    "How do you do"
]

good_keyword = [
    "Good morning",
    "Good afternoon",
    "Good night"
]


def hello_intent_func():
    print("Hello, i'm a function executed for a hello intendt")

def howareyou_intent_func():
    print("I'm good what 'bout you ?: executed from howareyouintent")

hello_intent = IntentBuilder("HelloIntent")\
    .require("HelloKeyword")\
    .build()

howareyou_intent = IntentBuilder("HowareyouIntent")\
    .optionally("HelloKeyword")\
    .optionally("GoodKeyword")\
    .require("HowareyouKeyword")\
    .build()

def getMap():
    return {
        hello_intent.name: hello_intent_func,
        howareyou_intent.name: howareyou_intent_func
    }
    
def getEntities():
    return {
        "HelloKeyword" : hello_keyword,
        "HowareyouKeyword" : howareyou_keyword,
        "GoodKeyword" : good_keyword
    }

def getRegexEntities():
    return {}


def getIntents():
    return [hello_intent, howareyou_intent]


if __name__ == "__main__":
    print(getIntents())