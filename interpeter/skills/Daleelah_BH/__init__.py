import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import interpeter.skills.Daleelah_BH.DatabaseConnection
import os

def field_locator_intent_func(*args, **kwargs):
    print("field locator intent function executed!")
    return {'field_name':'Harad00', 'field_distance':'5km','field_status':'drilling'}

def field_status_intent_fucn():
     sendQuery("")

mapper = {
    "FieldLocatorIntent" : field_locator_intent_func,
    "FieldStatusIntent" : field_status_intent_fucn
}



# You can create a skill both with a json or manually
class fieldLocatorSkill(Skill):
    def __init__(self):
        super().__init__()

        #load functions from dictionary to handler
        for handler in self.handlers:
            handler.func = mapper.get(handler.intent.name, None) #if it has no function set None







def getSkill():
    return fieldLocatorSkill()

