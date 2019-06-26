import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import requests
import datetime
import os

table = 'pb_0'
today = datetime.datetime.now()  	# todo: reformat the time to match time in the db table





def field_locator_intent_func(*args, **kwargs):
	sql = ('select operatingHours from {table} where '.format(table))
	sql += ('date={today}'.format(today))
	result = sendQuery(sql)

	print("field locator intent function executed!")
	return {'field_name':'Harad00', 'field_distance':'5km'}


def production_Intent_func(*args,**kwargs):
	sql = 'Select (operatingHours-24) from {table} where '.format(table)
	sql+= 'date = {today}'.format(today)
	result = sendQuery(sql)

	return {'hours':'66'}
	#result = sendQuery('select operating_hours from tablename where date = {date}') # loss = 24 - result


def number_of_active_rigsfunc(*args, **kwargs):
	sql = 'select count(distinct name) from {table} where '.format(table)
	sql+= 'date = {today}'.format(today)
	result = sendQuery(sql)

	print("active rigs intent function executed!")
	return {"number_of_active_rig":'300'}


def product_line_intent_func(*args, **kwargs):
	field = 'taken from json question' #todo: how to figure this out?

	sql = 'select ProdLine from {table} where name={field} and '
	sql+= 'date = {today}'.format(today)
	result = sendQuery(sql)

	print("field status intent function executed!")
	return {"status_situation" :"not good due to difficulty"}


def operating_hours_func(*args, **kwargs):
	sql = ('select operatingHours from {table} where '.format(table))
	sql += ('date={today}'.format(today))
	result = sendQuery(sql)

	print("operating hours intent function executed!")
	return {"time": '10'}

def most_active_rig_func(*args, **kwargs):
    print("most active rig intent function executed!")
    return {"big_player2": 'BHGE'}


mapper = {
    "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": product_line_intent_func,
    "TimeOfOperationIntent": operating_hours_func,
    "MostActiveIntent": most_active_rig_func,
	"ProductionIntent":production_Intent_func
}


def sendQuery(text):

	# api-endpoint
	URL = "localhost:3001/db"

	#filter = 'Level_0,category,company,operatinghours,personnelonLocHrs,date,well,wellbore,depart,Rig,field,Longitude,Latituide,BigPlayer,ProdLine'

	sql = text
	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'q': sql} # e.g.: SELECT * FROM get_well_view

	# sending get request and saving the response as response object
	r = requests.post(url = URL, params = PARAMS)

	# extracting data in json format
	data = r.json()
	return data  # dictionary needs to be handled



# You can create a skill both with a json or manually

class fieldLocatorSkill(Skill):
    def __init__(self):
        super().__init__()

        #load functions from dictionary to handler
        for handler in self.handlers:
            handler.func = mapper.get(handler.intent.name, None) #if it has no function set None



def getSkill():
    return fieldLocatorSkill()

