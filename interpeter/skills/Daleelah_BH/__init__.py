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
    'schlumberger': '\'SLB\'',
    'halliburton': '\'HAL\'',
    'weatherford' : '\'WTF\''

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
    colomn = args[0].get("field_keyword", None)
    companyname = args[0].get("company_name", "")
    print('here +++++++++++++++++++++++++++++++')
    print(companyname)
    print('here +++++++++++++++++++++++++++++++')
    coldic = {
        "rig": '\"Rig\"',
        "rigs": '\"Rig\"',
        "wells": 'well',
        "wellbore": 'wellbore',
        "wellbores": 'wellbore',
        "fields": 'field',
        "services": '\"Service\"',
        "product line": '\"ProdLine\"',
        "product lines": '\"ProdLine\"',
    }

    select_SQL = coldic.get(colomn, '\"Rig\"')  # get the name of the wanted column through the dic and defulte is rig
    company_name = BigPlayerDic.get(companyname, "")  # get the name of the wanted company through the dic and the defulte is all
    where_SQL = ""

    if select_SQL == '\"Rig\"':
        active_thing = 'rigs'
    else:
        active_thing = colomn
    if company_name != "":
        where_SQL = ' AND \"BigPlayer\" = ' + company_name


    print("active rigs intent function executed!")
    # import datetime
    engine_answer = args[0].get('field_keyword', None)
    print(engine_answer)
    start_date, end_date, answer = time_period_calc(args[0])
    sql_query = \
        "SELECT COUNT(DISTINCT {select_SQL}) FROM {table_name} \
          WHERE \"Date\" >= '{first_date}' AND \"Date\" < '{second_date}'".format(**
                                                                                          {
                                                                                              'table_name': table,
                                                                                              'first_date': start_date,
                                                                                              'second_date': end_date,
                                                                                              'select_SQL': select_SQL,
                                                                                          })
    sql_query += where_SQL
    print(sql_query)
    query_res = sendQuery(sql_query)
    print(query_res)
    print("start date is: ", start_date, ", end date=", end_date)
    # date = datetime.datetime.now()  # the format of this needs to be changed
    # result = sendQuery('select count (distinct Level_0) from tablename where date = {date};'.format(date))
    # todo: format the sql output to match the answer format
    count = query_res.get("rows")[0]["count"]
    # if not args[0].get("period_kwd", None):
    #     count = 201
    return {"number_of_active_rig": count, "optional": answer, "active_thing": active_thing,
            "company_name": 'for ' + companyname}


def compare_efficiency_func(*args,**kwargs):
    response = args[0]
    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''

    big_player1_kwd = response.get('big_player1_kwd'.lower(), "baker hughes")
    big_player2_kwd = response.get('big_player2_kwd'.lower(), "others")
    fancy = "after my calculations, it turns out that"

    big_player1_id = BigPlayerDic.get(big_player1_kwd.lower(), "BH")
    big_player2_id = BigPlayerDic.get(big_player1_kwd.lower(), None)



    eff_1 = _get_efficiency(big_player1_id, response=response)
    eff_2 = _get_efficiency(big_player2_id, response=response) or None
    winner = big_player1_kwd  # temp
    looser = big_player2_kwd
    compare = "higher"

    if eff_2 is None: # compare to all big players
        for company in BigPlayerDic:
            companyID = BigPlayerDic[company]
            if _get_efficiency(companyID) > eff_1:
                winner = big_player2_kwd
                looser = big_player1_kwd
                compare = "lower"
                eff_2 = _get_efficiency(companyID)
        if compare == "higher":  # no body is better than player_1
            eff_2 = " better than all others big player's "
    else:
        if eff_1 < eff_2:
            winner = big_player2_kwd
            looser = big_player1_kwd
            compare = "lower"

    eff_1 = str(eff_1)
    eff_2 = str(eff_2)


    return {"fancy":fancy , "big_player1_kwd":big_player1_kwd, "big_player2_kwd":big_player2_kwd,
            "compare":compare, "eff_bigPlayer_1":eff_1,"eff_bigPlayer_1":eff_2}


def non_productive_time_func(*args, **kwargs):
    response = args[0]
    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''

    failure_kwd = response.get('failure_kwd', "")
    BigPlayer_name = response.get("BigPlayer", "baker hughes")
    time_kwd = response.get("time_kwd", "time")
    total_kwd = response.get("time_kwd", "total")  # may be changed

    BigPlayerID = BigPlayerDic.get(BigPlayer_name, "BH")  # default BH

    q = "\""
    selection = "select " + "SUM(" + q + "Hrs" + q + ") "
    formation = "from " + loss_table + " "
    wheration = "where " + q + "BigPlayer" + q + "=" + BigPlayerID + " and " + date

    sql = selection + formation + wheration
    loss_number = 1
    # loss_number = sendQuery(sql) # todo: uncomment this line when connected to DB
    loss_number = str(loss_number)
    loss_hours = loss_number + " hours"

    print(sql)

    return {"big_player": BigPlayer_name, "failure_kwd": failure_kwd,
            "time_kwd": time_kwd, "total_kwd": total_kwd, "loss_hours": loss_hours}


def _get_efficiency(BigPlayerID,response,passed_date = None):

    date = None
    if passed_date is None:
        start_date, end_date, tail_answer = time_period_calc(response)
        date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    else:
        date = passed_date

    table = loss_table
    q = "\""
    selection = "SELECT " + "SUM(" + q + "OperatingHours" + q + ") "
    formation = "from " + table + " "
    wheration = "where " + q + "BigPlayer" + q + "=" + BigPlayerID + " and " + date + " "

    sql_1 = selection + formation + wheration

    working_hours = sendQuery(sql_1)  # todo: uncomment when connected to the DB
    working_hours = working_hours['rows'][0]['sum']

    q = "\""
    selection = "select " + "SUM(" + q + "Hrs" + q + ") "
    formation = "from " + loss_table + " "
    wheration = "where " + q + "BigPlayer" + q + "=" + BigPlayerID + " and " + date + " "

    sql_2 = selection + formation + wheration
    print(sql_2)
    loss_time = sendQuery(sql_2)  # todo: uncomment when connected to the DB
    loss_time = loss_time['rows'][0]['sum']

    efficiency = (working_hours - loss_time) / working_hours

    return efficiency


def production_efficiency_fuc(*args, **kwargs):
    #todo:  validate _getEffiencey() and replace the redundant code here
    response = args[0]
    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    date = '\"Date\" >= \'2019-01-01\' AND \"Date\" < \'2019-07-04\''
    # field name
    failure_kwd = response.get('failure_kwd', "")
    BigPlayer_name = response.get("big_player_kwd", "baker hughes")
    total_kwd = response.get("time_kwd", "total")  # may be changed
    fancy = "according to my calculations,"

    BigPlayerID = BigPlayerDic.get(BigPlayer_name.upper(), "BH")
    print(BigPlayerID, ' is id')

    q = "\""
    selection = "SELECT " + "SUM(" + q + "OperatingHours" + q + ") "
    formation = "from " + table + " "
    wheration = "where " + q + "BigPlayer" + q + "=" + BigPlayerID + " and " + date + " "

    sql_1 = selection + formation + wheration
    print(sql_1, " is sql 1")
    working_hours = sendQuery(sql_1)  # todo: uncomment when connected to the DB
    print(working_hours)
    working_hours = working_hours['rows'][0]['sum']
    q = "\""
    selection = "select " + "SUM(" + q + "Hrs" + q + ") "
    formation = "from " + loss_table + " "
    wheration = "where " + q + "BigPlayer" + q + "=" + BigPlayerID + " and " + date + " "

    sql_2 = selection + formation + wheration
    print(sql_2)
    loss_time = 6
    loss_time = sendQuery(sql_2)  # todo: uncomment when connected to the DB
    loss_time = loss_time['rows'][0]['sum']

    efficiency = (working_hours - loss_time) / working_hours

    efficiency *= 100
    print(sql_1)

    efficiency = str(efficiency)
    if (len(efficiency) > 6):
        efficiency = efficiency[:6]

    return {"total_kwd": total_kwd, "big_player_kwd": BigPlayer_name, "field_name_kwd": '',
            "fancy": "according to my information from the database,", "tail_kwd": tail_answer,
            "eff_reslut": efficiency}


def top_producing_fields_func(eng_response):
    start_date, end_date, date_answer = time_period_calc(eng_response)
    sql_str = "SELECT field,\"Name_new\", count(distinct well) as count \
          FROM ( \
              SELECT * FROM interns_view \
              WHERE \"Date\" >= '{}' AND \"Date\" < '{}' \
                ) AS something group by field,\"Name_new\" order by count DESC".format(start_date, end_date)
    res = sendQuery(sql_str)
    field_list = res.get("rows")
    field_list_len = len(field_list)
    answer = "According to the data, " + date_answer + ", the top producing fields are: "
    for i in range(10):
        if i > field_list_len: break
        fld = field_list[i]
        answer += fld.get("Name_new", "Unknown name")
        answer += " has" + fld.get("count", "Unknown name") + " wells "
    return {'optional' : answer}


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

    # if BigPlayer is not None:
    #     try:
    #         BigPlayer = BigPlayerDic[BigPlayer]
    #     except:
    #         BigPlayer = "\'BH\'"
    # else:
    #     BigPlayer = "\'BH\'"

    BigPlayer_name = 'baker hughes'  # default for now
    BigPlayer = BigPlayerDic[BigPlayer_name]
    short_name = cityDecoder[field_name]

    entries = {'selection': '\"BigPlayer\",\"CategoryName\" , \"Name_new\", well',
               'table': table,
               'where': date_1 + 'and' + ' \"BigPlayer\" = ' + BigPlayer + " and",
               'field': short_name}

    sql = 'select {selection} from {table} where {where} field = {field} limit 3'.format(**entries)

    print(sql)
    print("&&&")
    resultDic = sendQuery(sql)
    print(resultDic)
    answer = ''
    answer += "According to the data " + tail_answer
    answer += ' here are sample wells in ' + field_name + ', ' + BigPlayer_name + ' are working on the following wells: '

    for row in resultDic['rows']:
        short_name = row['well']
        well_id = short_name.split('_')[1]  # the numbers
        well_name = field_name + " " + well_id
        process = row['CategoryName']

        if well_name == '':
            well_name = 'unknown'
        if process == '':
            process = 'unknown'

        answer += well_name + ' is doing ' + process + ". "

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
    time = int(result)  # the query returns a number
    # print(sql, ' is sql')
    return {"time": time}


def most_active_func(*args, **kwargs):
    start_date, end_date, tail_answer = time_period_calc(args[0])
    MA = args[0].get("MostActiveIntent", None)
    order = "desc"
    if MA in ["least", "lowest",  "min"]:
        order = "asc"
    target_date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    text = '\"BigPlayer\",count(DISTINCT \"Rig\") as num '
    entries = {'selection': text,
               'table': table,
               'group': '\"BigPlayer\"'}

    sql = 'select {selection} from {table} where '.format(**entries)
    sql += '{target_date} '.format(target_date=target_date)
    sql += 'group by {group} '.format(**entries)
    sql += 'order by num {order} limit 1'.format(order=order)
    print(sql)

    bigplayer = 'BH'
    number = 100
    result = sendQuery(sql)
    # result = json.loads(result)
    print(result)
    bigplayer = result['rows'][0]['BigPlayer']
    number = result['rows'][0]['num']
    print(sql, ' is sql')

    return {"big_player": bigplayer, "number": number}


def list_rigs_in_filed_func(*args, **kwargs):
    field_name = "Dammam"
    field_name = args[0].get("field_name", None)
    start_date, end_date, tail_answer = time_period_calc(args[0])
    target_date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    entries = {'selection': 'DISTINCT \"Rig\"',
               'table': table,
               'target': field_name.lower()}

    sql = 'select {selection} from {table} where lower(\"Name_new\") = \'{target}\' AND '.format(**entries)
    sql += '{target_date}'.format(target_date=target_date)
    print(sql)
    listOfRigs = ''
    result = sendQuery(sql)
    print(result)
    for row in result['rows']:
        listOfRigs += row['Rig'] + ", "
    listOfRigs = listOfRigs[:-2]

    return {"rig_names": listOfRigs}


def status_of_well_func(*args, **kwargs):
    well_name = args[0].get("field_name", "DMMM129")
    entries = {'selection': 'DISTINCT \"Rig\"',
               'table': table}

    sql = 'select {selection} from {table} where lower(\"Name_new\") = \'{target}\' AND '.format(**entries)
    print(sql)

    result = sendQuery(sql)
    print(result)

    if result['rowCount'] == 0:
        answer = "the are no activety on " + well_name
    else:
        print('')

    return {"answer": answer}


def non_productive_location_func(*args, **kwargs):
    response = args[0]
    failure_kwd = response.get("failure_kwd","productive")
    big_player_kwd = response.get("big_player_kwd","baker hughes")

    BigPlayer_name = response.get("big_player_kwd", "baker hughes")


    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''


    BigPlayerID = BigPlayerDic.get(BigPlayer_name, "BH")  # default BH

    q = "\""

    selection = "select count(well),field "
    formation = "from " + loss_table + " "
    wheration =  "where " + date + " and " + q+"BigPlayer"+q +"="+big_player_kwd
    group = " group by field "
    order = "order by count(well) desc"


    sql_1= selection + formation + wheration + group + order
    # each fields how many non productive wells today
    print(sql_1 , " is sql_1")

    fancy = "According to the information I have, "
    locations = ""

    return {"fancy":fancy,"tail_kwd":tail_answer,"locations":locations}


def empty_hours_func (*args, **kwargs):
    print(" in empty hours")
    response = args[0]
    print(response)
    big_player_kwd = response.get("big_player_kwd", "baker hughes")
    hours_kwd = response.get("hours_kwd")
    field_name_kwd = response.get("field_name_kwd","\'MRJN\'")
    field_name_kwd= "\'" + field_name_kwd.upper() + "\'"

    start_date, end_date, tail_answer = time_period_calc(args[0])
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''


    BigPlayerID = BigPlayerDic.get(big_player_kwd, "\'BH\'")  # default BH

    fancy = "according to my calculations"
    q = "\""

    selection = "select " + "sum(" + q + "Hrs" + q + ")"
    formation = "from " + loss_table + " "
    wheration = "where " + date + " and " + q + "BigPlayer" + q + "=" + BigPlayerID
    location  = " and " + " field =" + field_name_kwd
    if location is None:
        location = " "

    sql = selection + formation + wheration + location

    print (sql , " empty hours sql")

    if location is not None:
        location = "in " + field_name_kwd + " field"

    result = sendQuery(sql)
    number = result['rows'][0]['sum']
    number = str(number) + " hours"


    return { "fancy": fancy, "timing": tail_answer,
            "big_player_kwd": big_player_kwd, "result": result,"field_name_kwd":location,
             "result":number}

def well_detial_summary_func(*args, **kwargs):
    response = args[0]

    well_name = response.get('well_name')
    hole_section_rmt = '###?'
    fancy2 = 'according to the data i have'
    fancy = 'from the information i have'

    table = 'hazard_table_v1'
    start_date, end_date, what_day = time_period_calc(response)
    date = '\"Date\" >= \'' + start_date + '\' AND \"Date\" < \'' + end_date + '\''
    
    q = '\"'
    table = 'hazard_table_v1'
    k = '\''


    selection = 'select ' + '\"Date\"'
    formation = ' from ' + table
    wheration = ' where ' + ' lower(well) ' + '=' +k+well_name+k
    orderby = ' order by "Date" desc limit 1 '

    sql_0 = selection + formation + wheration + orderby
    date = sendQuery(sql_0)
    print(sql_0, ' is sql_0')
    print(date, ' date is YY')
    date = date['rows'][0]['Date']
    time_index = date.index('T')
    date = date[:time_index]
    date = '\'' + date +'\''
    #date = '\'2019-02-12\''
    date = '\"Date\"= ' + date
    
    print(date,' is date')

    
    # sql for num of wellbore:
    selection = 'select ' + 'count(wellbore)'
    formation = ' from ' + table
    wheration = ' where '+ date + 'and ' + ' lower(well) ' + '=' + k+well_name+k

    sql_1 = selection + formation + wheration
    welbore_count = sendQuery(sql_1)['rows'][0]['count']


    column = 'mod_htable_From'
    selection = 'select ' + 'max('+ q+column+q +'),' + 'min('+ q+column+q +'),'
    formation = ' from ' + table
    wheration = 'where '+ date + 'and ' + 'lower(well) = ' + k+well_name+k

    sql_2 = selection + formation + wheration
    period = sendQuery(sql_2)
    start_time = '0000'
    end_time = '2030'
    sq = '\''
    # todo: from period extract start_time and end_time

    column = q+'htable_Hole_depth:Start'+q
    selection = 'select ' + column
    formation = ' from ' + table
    wheration = ' where '+ date+ ' and ' + ' lower(well) =' + k+well_name+k 
                # + ' and ' + q+'mod_htable_From'+q + '=' + k +  start_time + k
    sql_3 = selection + formation + wheration
    print(sql_3 , ' is sql 3')
    start_depth = sendQuery(sql_3)['rows'][0]['htable_Hole_depth:Start']
    print(start_depth,' is the start depth')
  
    column = q+'Hole_depth_End'+q
    selection = ' select ' + column
    formation = ' from ' + table
    wheration = ' where'+ date + ' and ' + ' lower(well) =' + k+well_name+k 
                # + ' and ' + q+'mod_htable_From'+q + '=' + k +end_date + k
    sql_4 = selection + formation + wheration
    end_depth = sendQuery(sql_4)['rows'][0]['Hole_depth_End']
    print(end_depth, ' end_depth')
    

    column = q+'htable_Phase'+q
    selection = 'select ' + column
    formation = ' from ' + table
    wheration = ' where '+ date + ' and ' + ' lower(well) =' + k+well_name+k 
                # + ' and ' + q+'mod_htable_From'+q + '=' + end_date
    sql_5 = selection + formation + wheration
    print(sql_5 , ' is sql_5')
    phase = sendQuery(sql_5)['rows'][0]['htable_Phase']
    print(phase, ' is phase')
          
    
    so_basically = None
    if start_date == end_date:
        so_basically = 'so basically, there was no additional drilling in the well'
    else:
        so_basically = 'so basically, the extra depth drilled is ' + str(abs(int(start_depth)-int(end_depth)))
    


    return {
            "hole_section_rmt":'a very nice hole section',
            "fancy2":fancy2, "fancy":fancy,
            "what_day":what_day,
            "phase":phase,"well_bore_num":welbore_count,"start_depth":start_depth
            ,"end_depth":end_depth,"so_basically":so_basically}




mapper = {
    # "FieldLocatorIntent": field_locator_intent_func,
    "NumberOfActiveRigsIntent": number_of_active_rigsfunc,
    "FieldStatusIntent": product_line_intent_func,
    "TimeOfOperationIntent": operating_hours_func,
    "ProductionIntent": production_Intent_func,
    "NoneProductiveTimeIntent": non_productive_time_func,
    "productionEfficiencyIntent": production_efficiency_fuc,
    "MostActiveIntent": most_active_func,
    "RigListerIntent": list_rigs_in_filed_func,
    "TopProducingFieldsIntent": top_producing_fields_func,
    "LocationOfNoneProductiveTime": non_productive_location_func,
    "EmptyHoursIntent": empty_hours_func,
    "StatusOfWellIntent": status_of_well_func,
    "WellDetailSummaryIntent":well_detial_summary_func
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
    return data


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