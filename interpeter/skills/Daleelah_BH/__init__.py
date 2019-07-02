import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import requests
import datetime
import os
import datetime
from dateutil.relativedelta import relativedelta

table = 'interns_view'
loss_table = 'npt_table_v0'

dCast = 'CAST (\"Date\" AS TEXT)'  # inside the select statement

date = str(datetime.datetime.now())
date = date[:10]  # like: "2019-06-27"

today = date

BigPlayerDic = {
    'baker hughes': '\'BH\'',
    'baker': '\'BH\'',  # todo: find correct short name
    'BH' : 'baker hughes',
    '\"BH\"' : 'baker hughes'
}

cityDecoder = {
    "Dammam":'\'DMMM\'',
    "dammam":'\'DMMM\''

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

def time_period_calc(response):
    print(response)
    monthes = {
        'january' : 1,
        'february' : 2,
        'march' : 3,
        'april' : 4,
        'may' : 5,
        'june' : 6,
        'july' : 7,
        'august' : 8,
        'september' : 9, 
        'october' : 10,
        'november' : 11,
        'december' : 12
    }


   
    start_date = datetime.date.today() #today's date
    end_date = start_date + datetime.timedelta(days=1)
    answer = "today"
    if "month_kwd" in response:
        print('Month detected')
        month = monthes.get(response.get("month_kwd"))
        year = int(response.get("n_kwd", start_date.year)) #graps the year, if not mentioned assumes it is the current year
        start_date = datetime.datetime(year, month, 1)
        end_date = start_date + relativedelta(months=+1)
        answer = "in " + str(month) + " " + str(year)
    
    period = response.get('period_kwd', None)
    
    if period: # going back in date
        # end_date = start_date
        n_period = int(response.get('n_kwd', 1))

    if period == 'yesterday':
        start_date = start_date - datetime.timedelta(days=1)
        answer = "yesterday" 
    elif period in ['week','weeks']:
        start_date = start_date - relativedelta(weeks=+n_period)
        answer = str(n_period) + " " + period + " ago"
    elif period in ['month','months']:
        start_date = start_date - relativedelta(months=+n_period)
        answer = str(n_period) + " " + period + " ago"
    elif period in ['year','years']:
        start_date = start_date - relativedelta(years=+n_period)
        answer = str(n_period) + " " + period + " ago"
    elif period in ['day', 'days']:
        start_date = start_date - relativedelta(days=+n_period)
        answer = str(n_period) + " " + period + " ago"
    
    end_date = start_date + datetime.timedelta(days=1)

         
    


    print(start_date, end_date)
    return str(start_date), str(end_date), answer

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
    start_date, end_date, answer = time_period_calc(args[0])
    sql_query = \
    "SELECT COUNT(DISTINCT well) FROM {table_name} \
      WHERE \"Date\" >= '{first_date}' AND \"Date\" < '{second_date}'".format(** 
      {
          'table_name' : table,
          'first_date' : start_date,
          'second_date': end_date,
      })

    query_res = sendQuery(sql_query)
    print(sql_query)
    print(query_res)
    print("start date is: ", start_date, ", end date=", end_date)    
    # date = datetime.datetime.now()  # the format of this needs to be changed
    # result = sendQuery('select count (distinct Level_0) from tablename where date = {date};'.format(date))
	# todo: format the sql output to match the answer format
    count = query_res.get("rows")[0]["count"]
    # if not args[0].get("period_kwd", None):
    #     count = 201
    return {"number_of_active_rig":count, "optional" : answer}


def non_productive_time_func(*args, **kwargs):
    response = args[0]
    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' +start_date+ '\' AND \"Date\" < \''+ end_date + '\''


    failure_kwd = response.get('failure_kwd',"")
    BigPlayer_name = response.get("BigPlayer", "baker hughes")
    time_kwd = response.get("time_kwd", "time")
    total_kwd = response.get("time_kwd", "total") # may be changed

    BigPlayerID = BigPlayerDic.get(BigPlayer_name,"BH") # default BH

    q = "\""
    selection = "select "+"SUM("+q+"Hrs"+q+") "
    formation = "from "+loss_table+ " "
    wheration = "where "+q+"BigPlayer"+q+"="+BigPlayerID+" and " + date

    sql = selection + formation + wheration
    loss_number = 1
    #loss_number = sendQuery(sql) # todo: uncomment this line when connected to DB
    loss_number = str(loss_number)
    loss_hours = loss_number + " hours"

    print(sql)


    return {"big_player":BigPlayer_name,"failure_kwd":failure_kwd,
            "time_kwd":time_kwd,"total_kwd" : total_kwd,"loss_hours":loss_hours}

def production_efficiency_fuc(*args,**kwargs):
    response = args[0]
    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    # field name
    failure_kwd = response.get('failure_kwd', "")
    BigPlayer_name = response.get("BigPlayer", "baker hughes")
    total_kwd = response.get("time_kwd", "total")  # may be changed
    fancy = "according to my calculations,"

    BigPlayerID = BigPlayerDic.get(BigPlayer_name,"BH")

    q = "\""
    selection = "SELECT "+ "SUM("+q+"OperatingHours"+q+") "
    formation = "from "+ table + " "
    wheration = "where "+ q+"BigPlayer"+q+"="+ BigPlayerID+" and "+date+ " "

    sql_1 = selection + formation + wheration
    working_hours = 20
    #working_hours = sendQuery(sql_1) # todo: uncomment when connected to the DB

    q = "\""
    selection = "select "+"SUM("+q+"Hrs"+q+") "
    formation = "from "+loss_table+ " "
    wheration = "where "+q+"BigPlayer"+q+"="+BigPlayerID+" and " + date

    sql_2 = selection + formation+ wheration
    print(sql_2)
    loss_time = 6
    #loss_time = sendQuery(sql_2) # todo: uncomment when connected to the DB

    efficiency = loss_time/working_hours
    efficiency = str (efficiency)

    print(efficiency + ' :is eff')

    efficiency = working_hours
    print(sql_1)

    return {"total_kwd":total_kwd,"big_player_kwd":BigPlayer_name,"field_name_kwd":''}




def product_line_intent_func(*args, **kwargs):
    field_name = args[0].get("field_name", None)
    BigPlayer_name = args[0].get("BigPlayer", None)
    start_date, end_date, tail_answer = time_period_calc(args[0])



    #date_1 = ' \"Date\" >= \'2019-06-01\' AND \"Date\" < \'2019-07-02\''
    date_1 = '\"Date\" >= \'' +start_date+ '\' AND \"Date\" < \''+ end_date + '\''
    if field_name is not None:
        print(field_name + ' is field name')
    else:
        #field_name = '\'DMMM\''  # default todo: should be changed to shortcuts only
        field_name = 'dammam' # default for now

    if BigPlayer_name is not None:
        print(BigPlayer_name)
    else:
        BigPlayer_name = 'baker hughes'

    # if BigPlayer is not None:
    #     try:
    #         BigPlayer = BigPlayerDic[BigPlayer]
    #     except:
    #         BigPlayer = "\'BH\'"
    # else:
    #     BigPlayer = "\'BH\'"

    BigPlayer_name = 'baker hughes' # default for now
    BigPlayer = BigPlayerDic[BigPlayer_name]
    short_name = cityDecoder[field_name]

    entries = {'selection':'\"BigPlayer\",\"CategoryName\" , \"Name_new\", well',
               'table': table,
               'where': date_1 + 'and' + ' \"BigPlayer\" = ' + BigPlayer + " and",
               'field': short_name}

    sql = 'select {selection} from {table} where {where} field = {field} limit 3'.format(**entries)

    print(sql)
    print("&&&")
    resultDic = sendQuery(sql)
    print(resultDic)
    answer = '' 
    answer +=  "According to the data " + tail_answer
    answer += ' here are sample wells in ' + field_name + ', ' + BigPlayer_name + ' are working on the following wells: '

    for row in resultDic['rows']:
        short_name = row['well']
        well_id = short_name.split('_')[1] # the numbers
        well_name = field_name + " " + well_id
        process = row['CategoryName']

        if well_name == '':
            well_name = 'unknown'
        if process == '':
            process = 'unknown'


        answer += well_name+ ' is doing ' + process + ". "
    
    return {"answer": answer}


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
    "ProductionIntent":production_Intent_func,
    "NoneProductiveTimeIntent":non_productive_time_func,
     "productionEfficiencyIntent":production_efficiency_fuc
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
    return data



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