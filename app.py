from flask import Flask,request,make_response,jsonify
import sqlite3
import csv
from datetime import datetime
from operator import itemgetter
import json


app = Flask(__name__)

routes_list = []
trips_list = []
stop_times_list = []
calendar_dates_list = []

def populate():
    with open('input/routes.txt', 'r') as f:
        reader = csv.reader(f)
        global routes_list
        routes_list= list(reader)
        routes_list.pop(0)

    with open('input/trips.txt', 'r') as f:
        reader = csv.reader(f)
        global trips_list
        trips_list = list(reader)
        trips_list.pop(0)

    with open('input/stop_times.txt', 'r') as f:
        reader = csv.reader(f)
        global stop_times_list
        stop_times_list = list(reader)
        stop_times_list.pop(0)

    with open('input/calendar.txt', 'r') as f:
        reader = csv.reader(f)
        global calendar_dates_list
        calendar_dates_list = list(reader)
        calendar_dates_list.pop(0)







#Returns service id of the bus in current date
def calender_afterday():
    service_id = []
    for row in calendar_dates_list:
        start = datetime.strptime(row[8], '%Y%m%d')
        end = datetime.strptime(row[9], '%Y%m%d')
        if(start <= datetime.today() <= end):
            if((datetime.now().weekday() == 0 and row[1] == '1') or
                    (datetime.now().weekday() == 1 and row[2] == '1') or
                    (datetime.now().weekday() == 2 and row[3] == '1') or
                    (datetime.now().weekday() == 3 and row[4] == '1') or
                    (datetime.now().weekday() == 4 and row[5] == '1') or
                    (datetime.now().weekday() == 5 and row[6] == '1') or
                    (datetime.now().weekday() == 6 and row[7] == '1') ):
                service_id.append(int(row[0]))
    return service_id


def gettrips_from_serviceid(service):
    trips_from_serviceid = []
    for row2 in trips_list:
        if(int(row2[1]) in service):
            trips_from_serviceid.append(row2)
    return trips_from_serviceid

#Return trip_id, start/end time, remaining_time in sorted order
def tripid_from_stopid(stop_id):
    trip_id_result = []
    for row in stop_times_list:
        if(row[3] == stop_id):
            if(int(row[1].strip().split(':')[0])<24):
                cur1Time = datetime.combine(datetime.now().date(), datetime.strptime(row[1].strip(), '%H:%M:%S').time())
                if(cur1Time>datetime.now()):
                    dup2 = cur1Time-datetime.now()
                    row.append(dup2.total_seconds())
                    trip_id_result.append(row)
    return sorted(trip_id_result,key=itemgetter(9))

def get_routeid(stopid):
    populate()
    result = {}
    final_serviceid_calendarlist = calender_afterday()
    stop_times_trip_details = tripid_from_stopid(str(stopid))
    trips = gettrips_from_serviceid(final_serviceid_calendarlist)
    count = 0
    for row1 in stop_times_trip_details:
        for row2 in routes_list:
            for row3 in trips:
                if (int(row3[0]) == int(row2[0]) and int(row1[0])==int(row3[2])):
                    count+=1
                    if(count>3):
                        break
                    result[str(count)] = {}
                    result[str(count)] ['stopid'] = str(row1[3])
                    result[str(count)] ['routeid'] = str(row2[0])
                    result[str(count)] ['tripid'] = str(row1[0])
                    result[str(count)] ['arrivalTime'] = str(row1[1])
                    result[str(count)] ['remainingTime'] = str(row1[9])
                    result[str(count)] ['routename'] = str(row2[3])
            if count >3:
                break
        if count>3:
            break
    return result


@app.route('/stoproute')
def approute():
    args = request.args.get('stopid')
    return json.dumps(get_routeid(str(args)))


if __name__ == '__main__':
    app.run()
