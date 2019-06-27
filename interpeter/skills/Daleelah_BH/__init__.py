import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import requests
import datetime
import os

table = 'oph_table_v0'
#today = datetime.datetime.now()  # todo: reformat the time to match time in the db table
today ='2017-12-08T21:00:00.000Z' # temporary

BigPlayerDic = {
	'baker hughes' : 'BH',
	'schlumberger' : 'SG'  # todo: find correct short name
}


def field_locator_intent_func(*args, **kwargs):
	sql = ('select operatingHours from {table} where '.format(table))
	sql += ('date={today}'.format(today))
	result = sendQuery(sql)

	print("field locator intent function executed!")
	return {'field_name':'Harad00', 'field_distance':'5km'}


def production_Intent_func(*args,**kwargs):
	sql = 'Select (operatingHours-24) from {table} where '.format(table=table)
	sql+= 'date = {today}'.format(today=today)

	return {'hours':'اي شي'}
	# entries = {'selection': 'ProductLine',
	# 			'table': table,
	# 			'field':field_name,
	# 			'column':'field'}

	#result = sendQuery(sql)
	#return {'hours':'66'}

	#result = sendQuery('select operating_hours from tablename where date = {date}') # loss = 24 - result


def number_of_active_rigsfunc(*args, **kwargs):
	sql = 'select count(distinct name) from {table} where '.format(table)
	sql += 'date = {today}'.format(today)
	result = sendQuery(sql)

	entries = {'selection': 'ProductLine',
	           'table': table,
	           'field': 'dammam',
	           'column': 'field'}

	sql = 'select {selection} from {table} where {column} = {field} and '.format(**entries)
	sql += 'date = {today}'.format(today=today)

	print("active rigs intent function executed!")
	return {"number_of_active_rig":'300'}


def product_line_intent_func(*args, **kwargs):
	field_name = args[0].get("field_name",None)
	print(field_name, ' is field_name')
	if(field_name):
		pass
	else:
		field_name = 'dammam' # todo: should be changed to shortcuts only



	entries = {'selection': 'ProductLine',
				'table': table,
				'field':field_name,
				'column':'field'}

	sql = 'select {selection} from {table} where {column} = {field} and '.format(**entries)
	sql += 'date = {today}'.format(today=today)


	result = {'ProdLine':'drilling'} # todo: should be replaced with bottom 2 lines
	# result = sendQuery(sql)
	# result = json.loads(result)

	prodLine_keyword = result['ProdLine']

	return {'product_line':prodLine_keyword,'field_name':field_name}


def operating_hours_func(*args, **kwargs):
	field_name = args[0].get("field_name", None)
	BigPlayer = args[0].get("big_player", None)


	if (field_name is not None):
		pass
	else:
		field_name = 'dammam'  # default val. todo: should be changed to shortcuts only

	entries = {'selection': 'OperatingHours',
				'table': table,
				'field': field_name,
				'column': 'field',
	           'BigPlayer': BigPlayerDic[BigPlayer]}

	sql = 'select {selection} from {table} where {column} = {field} and ' \
	      '{BigPlayer}'.format(**entries)
	sql += 'date = {today}'.format(today=today)

	result = {'temporary':'well'}  # todo: should be replaced with bottom 2 lines
	# result = sendQuery(sql)
	# result = json.loads(result)

	return {"time": '10'}


mapper = {
    "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": product_line_intent_func,
    "TimeOfOperationIntent": operating_hours_func,
    "MostActiveIntent": most_active_rig_func,
	"ProductionIntent":production_Intent_func
}


def sendQuery(sql):
	# api-endpoint
	URL = 'http://localhost:3001/db'
	#sql = "select * from oph_table_v0 limit 10"

	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'q':sql}

	# sending get request and saving the response as response object
	r = requests.post(URL,data=PARAMS)
	# extracting data in json format
	data = r.json()

	#return data
	return {}




# You can create a skill both with a json or manually

class fieldLocatorSkill(Skill): # @Ryan, recom: having a skill passed is confusing. since it is not used
    def __init__(self):
        super().__init__()
        # load functions from dictionary to handler
        for handler in self.handlers:
            handler.func = mapper.get(handler.intent.name, None)  # if it has no function set None



def getSkill():
    return fieldLocatorSkill()  # @Ryan, returns a skill object that was just assigned a bunch of functions

if __name__ == '__main__':
	print(today)
	pass
#
# result = product_line_intent_func()
# print(result)