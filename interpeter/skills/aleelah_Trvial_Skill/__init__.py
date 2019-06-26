
import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import os 


def trivialFunc():
    print("TrivialSkills function executed")

#maps intents to functions       
mapper = {
    "TrivialIntent" : trivialFunc
}

# You can create a skill both with a json or manually
class trivialSkill(Skill):
    def __init__(self):
        super().__init__()
        
        #load functions from dictionary to handler
        for handler in self.handlers:
            handler.func = mapper.get(handler.intent.name, None) #if it has no function set None
        







def getSkill():
    return trivialSkill()

