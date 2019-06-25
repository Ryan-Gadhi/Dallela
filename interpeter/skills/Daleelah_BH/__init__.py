import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import os



def field_locator_intent_func(*args, **kwargs):
    print("field locator intent function executed!")

    return {'field_name':'Harad00', 'field_distance':'5km'}

def production_Intent_func(*args,**kwargs):
	result = sendQuery('select operating_hours from tablename where date = {date}') # loss = 24 - result

def number_of_active_rigsfunc(*args, **kwargs):
    print("active rigs intent function executed!")
    import datetime

    date = datetime.datetime.now()  # the format of this needs to be changed
    result = sendQuery('select count (distinct Level_0) from tablename where date = {date};'.format(date))

	# todo: format the sql output to match the answer format
    return {"number_of_active_rig":'300'}



def field_status_intent_func(*args, **kwargs):
    print("field status intent function executed!")
    return {"number_of_active_rig":'300'}


mapper = {
    "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": field_status_intent_func
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

