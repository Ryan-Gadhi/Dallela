
import json
import sys
from adapt.intent import IntentBuilder
from base import Skill, Handler
import os 


def weatherFunc(*args, **kwargs):
    print("Weather intent function executed!")
    return {'deg':'50', 'unit':'C'}

#maps intents to functions       
mapper = {
    "WeatherIntent" : weatherFunc
}

# You can create a skill both with a json or manually
class weatherSkill(Skill):
    def __init__(self):
        super().__init__()
        
        #load functions from dictionary to handler
        for handler in self.handlers:
            handler.func = mapper.get(handler.intent.name, None) #if it has no function set None
        







def getSkill():
    return weatherSkill()

