import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import requests
import os





table = 'oph_table_v0'

def field_locator_intent_func(*args, **kwargs):
    print("field locator intent function executed!")
    return {'field_name':'Harad00', 'field_distance':'5km'}

def production_Intent_func(*args,**kwargs):
	return {'hours':'20',}
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



def field_status_intent_func(*args, **kwargs):
    print("field status intent function executed!")
    return {"status_situation" :"not good due to difficulty"}

def operating_hours_func(*args, **kwargs):
    print("operating hours intent function executed!")
    return {"time": '10'}

def most_active_rig_func(*args, **kwargs):
    print("most active rig intent function executed!")
    return {"big_player2": 'BHGE'}


mapper = {
    "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": field_status_intent_func,
    "TimeOfOperationIntent": operating_hours_func,
    "MostActiveIntent": most_active_rig_func,
	"ProductionIntent":production_Intent_func
}


def sendQuery(sql_string):

	# api-endpoint
	URL = "http://localhost/d/sql.php"

	#filter = 'Level_0,category,company,operatinghours,personnelonLocHrs,date,well,wellbore,depart,Rig,field,Longitude,Latituide,BigPlayer,ProdLine'

	# defining a paramsgit reset --hard origin/<branch_name> dict for the parameters to be sent to the API
	PARAMS = {'q' : sql_string} # e.g.: SELECT * FROM get_well_view

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

