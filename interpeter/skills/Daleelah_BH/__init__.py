import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import requests
import datetime
import os

table = 'oph_table_v0'

dCast = 'CAST (\"Date\" AS TEXT)'  # inside the select statement

date = str(datetime.datetime.now())
date = date[:10]  # like: "2019-06-27"

today = date


BigPlayerDic = {
	'baker hughes': 'BH',
	'baker': 'BH'  # todo: find correct short name
}

cityDecoder = {
	'DMMM':"Dammam"
}
operationDecoder = {
	'OTH' : "Other"
}




def field_locator_intent_func(*args, **kwargs):
	sql = ('select operatingHours from {table} where '.format(table))
	sql += ('date={today}'.format(today))
	result = sendQuery(sql)

	#print("field locator intent function executed!")
	return {'field_name':'Harad00', 'field_distance':'5km'}


def production_Intent_func(*args,**kwargs):
	sql = 'Select (operatingHours-24) from {table} where '.format(table=table)
	sql+= 'date = {today}'.format(today=today)

	return {'hours':'اي شي'}

	#result = sendQuery('select operating_hours from tablename where date = {date}') # loss = 24 - result


def number_of_active_rigsfunc(*args, **kwargs):
    print("active rigs intent function executed!")
    # import datetime
    engine_answer = args[0].get('field_keyword', None)
    print(engine_answer)
    sql_query = \
    "SELECT COUNT(DISTINCT well) FROM {table_name} \
      WHERE Date >= '{first_date}' AND Date < '{second_date}'".format(**
      {
          'table_name' : table,
          'first_date' : '20181220 00:00:00.000',
          'second_date': '20181220 23:59:59.999',
      })

    query_res = sendQuery(sql_query)

    # date = datetime.datetime.now()  # the format of this needs to be changed
    # result = sendQuery('select count (distinct Level_0) from tablename where date = {date};'.format(date))
	# todo: format the sql output to match the answer format
    count = query_res.get("rows")[0]["count"]
    return {"number_of_active_rig":count}



def product_line_intent_func(*args, **kwargs):

	field_name = args[0].get("field_name",None)
	BigPlayer = args[0].get("BigPlayer",None)
	BigPlayer = 'baker hughes'

	if(field_name):
		pass
	else:
		field_name = 'DMMM' # todo: should be changed to shortcuts only

	if(BigPlayer):
		try:
			BigPlayer = BigPlayerDic[BigPlayer]
		except:
			BigPlayer = 'BH'
	else:
		BigPlayer = "BH"

	entries = {'selection': dCast+', \"BigPlayer\",\"ProdLine\"',
				'table': table,
	            'where': '\"Date\" ='+ '\''+today+'\'' + 'and' + ' \"BigPlayer\" = '+BigPlayer + " and ",
				'field': field_name}


	sql = 'select {selection} from {table} where {where} fieled = {field}'.format(**entries)

	resultDic = sendQuery(sql)
	for row in resultDic:
		print(row)

	ProdLine = 'drilling'
	result = {'ProdLine':ProdLine} # todo: should be replaced with bottom 2 lines
	# result = sendQuery(sql)
	# result = json.loads(result)

	prodLine_keyword = result['ProdLine']

	return {'product_line':prodLine_keyword,'field_name':field_name}


def operating_hours_func(*args, **kwargs):
	field_name = args[0].get("field_name", None)
	BigPlayer = args[0].get("big_player1", None)

	if (field_name is not None):
		pass
	else:
		field_name = 'HMYM'  # default val. todo: should be changed to shortcuts only

	entries = {'selection': '(OperatingHours-24)',
				'table': table,
				'field': field_name,
				'column': 'field',
	           'BigPlayer': BigPlayerDic[BigPlayer]}

	sql = 'select {selection} from {table} where {column} = {field} and ' \
	      '\"BigPlayer\" = {BigPlayer} and '.format(**entries)
	sql += 'date = {today}'.format(today=today)

	result = '15'  # todo: should be replaced with bottom 2 lines
	# result = sendQuery(sql)
	# result = json.loads(result)
	time  = int(result)  # the query returns a number
	#print(sql, ' is sql')
	return {"time": time}


mapper = {
    "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": product_line_intent_func,
    "TimeOfOperationIntent": operating_hours_func,
	"ProductionIntent":production_Intent_func
}


def sendQuery(sql_string):
	# api-endpoint
	URL = 'http://localhost:3001/db'
	#sql = "select * from oph_table_v0 limit 10"

	# defining a params dict for the parameters to be sent to the API
	PARAMS = {'q':sql_string}

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