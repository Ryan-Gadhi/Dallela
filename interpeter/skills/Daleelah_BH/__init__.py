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

dCast = 'CAST (\"Date\" AS TEXT)'  # inside the select statement

date = str(datetime.datetime.now())
date = date[:10]  # like: "2019-06-27"

today = date

BigPlayerDic = {
    'baker hughes': '\'BH\'',
    'baker': '\'BH\'',  # todo: find correct short name
    'BH': 'baker hughes',
    '\"BH\"': 'baker hughes'
}

cityDecoder = {
    "Dammam": '\'DMMM\'',
    "dammam": '\'DMMM\''

}
operationDecoder = {
    'OTH': "Other"
}


def field_locator_intent_func(*args, **kwargs):
    sql = ('select operatingHours from {table} where '.format(table))
    sql += ('date={today}'.format(today))
    result = sendQuery(sql)

    # print("field locator intent function executed!")
    return {'field_name': 'Harad00', 'field_distance': '5km'}


def time_period_calc(response):
    print(response)
    monthes = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }

    start_date = datetime.date.today()  # today's date
    end_date = start_date + datetime.timedelta(days=1)
    answer = "today"
    if "month_kwd" in response:
        print('Month detected')
        month = monthes.get(response.get("month_kwd"))
        year = int(
            response.get("n_kwd", start_date.year))  # graps the year, if not mentioned assumes it is the current year
        start_date = datetime.datetime(year, month, 1)
        end_date = start_date + relativedelta(months=+1)
        answer = "in " + str(month) + " " + str(year)

    period = response.get('period_kwd', None)

    if period:  # going back in date
        # end_date = start_date
        n_period = int(response.get('n_kwd', 1))

    if period == 'yesterday':
        start_date = start_date - datetime.timedelta(days=1)
        answer = "yesterday"
    elif period in ['week', 'weeks']:
        start_date = start_date - relativedelta(weeks=+n_period)
        answer = str(n_period) + " " + period + " ago"
    elif period in ['month', 'months']:
        start_date = start_date - relativedelta(months=+n_period)
        answer = str(n_period) + " " + period + " ago"
    elif period in ['year', 'years']:
        start_date = start_date - relativedelta(years=+n_period)
        answer = str(n_period) + " " + period + " ago"
    elif period in ['day', 'days']:
        start_date = start_date - relativedelta(days=+n_period)
        answer = str(n_period) + " " + period + " ago"

    end_date = start_date + datetime.timedelta(days=1)

    print(start_date, end_date)
    return str(start_date), str(end_date), answer


def production_Intent_func(*args, **kwargs):
    sql = 'Select (operatingHours-24) from {table} where '.format(table=table)
    sql += 'date = {today}'.format(today=today)

    return {'hours': 'اي شي'}

    # result = sendQuery('select operating_hours from tablename where date = {date}') # loss = 24 - result


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
                                                                                          'table_name': table,
                                                                                          'first_date': start_date,
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
    return {"number_of_active_rig": count, "optional": answer}


def product_line_intent_func(*args, **kwargs):
    field_name = args[0].get("field_name", None)
    BigPlayer_name = args[0].get("BigPlayer", None)
    start_date, end_date, tail_answer = time_period_calc(args[0])

    # date_1 = ' \"Date\" >= \'2019-06-01\' AND \"Date\" < \'2019-07-02\''
    date_1 = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    if field_name is not None:
        print(field_name + ' is field name')
    else:
        # field_name = '\'DMMM\''  # default todo: should be changed to shortcuts only
        field_name = 'dammam'  # default for now

    if BigPlayer_name is not None:
        print(BigPlayer_name)
    else:
        BigPlayer_name = 'baker hughes'

        entries = {'selection': 'ProductLine',
                   'table': table,
                   'field': field_name,
                   'column': 'field'}

        sql = 'select {selection} from {table} where {column} = {field} and '.format(**entries)
        sql += 'date = {today}'.format(today=today)

        result = {'ProdLine': 'drilling'}  # todo: should be replaced with bottom 2 lines
        # result = sendQuery(sql)
        # result = json.loads(result)

        prodLine_keyword = result['ProdLine']

        return {'product_line': prodLine_keyword, 'field_name': field_name}


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
    time = int(result)  # the query returns a number
    # print(sql, ' is sql')
    return {"time": time}


def most_active_func(*args, **kwargs):
    start_date, end_date, tail_answer = time_period_calc(args[0])
    target_date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    entries = {'selection': '\"BigPlayer\",count(DISTINCT \"Rigs\") as num ',
               'table': table,
               'group': '\"BigPlayer\"'}

    sql = 'select {selection} from {table} group by {group} and '.format(**entries)
    sql += 'date = {target_date}'.format(target_date=target_date)
    sql += 'order by num desc limit 1'

    bigplayer = 'BH'  # todo: should be replaced with bottom 2 lines
    number = 100
    # result = sendQuery(sql)
    # result = json.loads(result)
    # bigplayer, number = result[rows][0][]
    # print(sql, ' is sql')

    return {"big_player": bigplayer, "number": number}


def list_rigs_in_filed_func(*args, **kwargs):
    entries = {'selection': 'DISTINCT \"Rigs\"',
               'table': table,
               'target': ''}

    sql = 'select {selection} from {table} where \"Name_new\"={target}'.format(**entries)
    sql += 'date = {today}'.format(today=today)
    sql += 'order by num desc limit 1'

    listOfRigs = 'k k k k  kk'
    # result = sendQuery(sql)
    # result = json.loads(result)
    # for row in result['rows']:
    #     listOfRigs += ", " + row
    # print(sql, ' is sql')

    return {"rig_names": listOfRigs}


mapper = {
    "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": product_line_intent_func,
    "TimeOfOperationIntent": operating_hours_func,
    "ProductionIntent": production_Intent_func,
    "RigListerIntent": list_rigs_in_filed_func,
    "MostActiveIntent": most_active_func
}


def sendQuery(sql_string):
    # api-endpoint
    URL = 'http://localhost:3001/db'
    # sql = "select * from oph_table_v0 limit 10"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'q': sql_string}

    # sending get request and saving the response as response object
    r = requests.post(URL, data=PARAMS)
    # extracting data in json format
    data = r.json()

    # return data
    return {}


# You can create a skill both with a json or manually

class fieldLocatorSkill(Skill):  # @Ryan, recom: having a skill passed is confusing. since it is not used
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
