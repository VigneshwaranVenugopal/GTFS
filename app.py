"""
This program creates an api to display first three bus (routes) given 'stopid'

Query Schema
1 -> Populate(), populates the text files into dictionaries
2 -> calender_dates_today(), returns all service_id's working current day of the week
3 -> gettrips_from_serviceid(), returns all trips that that has the above service_id's
4 -> tripid_from_stopid - returns all the trips with Time greater than current time using the filtered list
5 -> get_routeid() - returns function returns the 3 trips from the given stop id
"""

import json
import time
import csv
from datetime import datetime
from datetime import timedelta
from operator import itemgetter
from flask import Flask,request,make_response,jsonify

__author__ = "Vigneshwaran Venugopal"
__copyright__ = "Copyright 2018, LookingBus Project"
__email__ = "vvenugopal@alumni.scu.edu"
__status__ = "Testing"

app = Flask(__name__)

def populate():
    # Saving 'routes.txt' in dictionary where 'key = route-id' and 'values = entire row'
    with open('input/routes.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global routes_dict
        routes_dict = {rows[0]: rows for rows in reader}

    # Saving 'trips.txt' in dictionary where 'key = trips_id' and 'values = entire row'
    with open('input/trips.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global trips_id_dict
        global trips_dict
        trips_id_dict = {}
        trips_dict = {}
        for rows in reader:
            trips_id_dict.setdefault(rows[1], []).append(rows[2])
            trips_dict.setdefault(rows[2], [] ).append(rows)

    # Saving 'stop_times.txt' in dictionary of dictionaries where 'key1 = route_id', 'key2 = trip_id' and 'values = time stamp'
    with open('input/stop_times.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global stop_times_dict
        stop_times_dict = {}
        for row in reader:
            stop_times_dict.setdefault(row[0], {})
            stop_times_dict[row[0]].setdefault(row[3], [])
            stop_times_dict[row[0]][row[3]].append(row[1])
            stop_times_dict[row[0]][row[3]].append(row[2])

    # Saving 'calendar.txt' in dictionary 'key1 = day os the week' and 'values = service_id's'
    with open('input/calendar.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global calendar_dict
        calendar_dict = {'monday':[], 'tuesday':[], 'wednesday':[], 'thursday':[], 'friday':[], 'saturday':[], 'sunday':[] }
        for row in reader:
            i = 0
            for days in row:
                i = i+1
                if days == '1' and i==1:
                    calendar_dict['monday'].append(row[0])
                if days == '1' and i==2:
                    calendar_dict['tuesday'].append(row[0])
                if days == '1' and i==3:
                    calendar_dict['wednesday'].append(row[0])
                if days == '1' and i==4:
                    calendar_dict['thursday'].append(row[0])
                if days == '1' and i==5:
                    calendar_dict['friday'].append(row[0])
                if days == '1' and i==6:
                    calendar_dict['saturday'].append(row[0])
                if days == '1' and i == 7:
                    calendar_dict['sunday'].append(row[0])


def calender_dates_today():
    '''
    :return: all service_id's working current day of the week
    '''
    if (datetime.now().weekday()==0):
        return calendar_dict['monday']
    if (datetime.now().weekday()==1):
        return calendar_dict['tuesday']
    if (datetime.now().weekday()==2):
        return calendar_dict['wednesday']
    if (datetime.now().weekday()==3):
        return calendar_dict['thursday']
    if (datetime.now().weekday()==4):
        return calendar_dict['friday']
    if (datetime.now().weekday()==5):
        return calendar_dict['saturday']
    if (datetime.now().weekday()==6):
        return calendar_dict['sunday']


def gettrips_from_serviceid(service):
    '''
    :param service: filtered service_id's from previous function
    :return: all trips that that has the above service_id's
    '''
    trips_from_serviceid = []
    for services in service:
        trips_from_serviceid = trips_from_serviceid + trips_id_dict.get(services)
    return trips_from_serviceid


def tripid_from_stopid(stop_id,trips):
    '''
    :param stop_id: for which we find the routes
    :param trips: filtered trips from 'gettrips_from_serviceid' function
    :return: All the trips with time greater than current time using the filtered trips list
    '''
    trip_id_result = []
    count = 0
    now = datetime.now()
    for trip in trips:
        if stop_id in stop_times_dict[trip]:
            arrivaltime = stop_times_dict[trip][stop_id][0].strip()
            #Parsing the 'arrivaltime' and 'seconds remaining' in 'datetime' format
            if(int(arrivaltime.split(':')[0])<24):
                curTime = datetime.combine(now.date(),
                                            datetime.strptime(arrivaltime, '%H:%M:%S').time())
            else:
                time = '%d:%d:%d' % (
                int(arrivaltime.split(':')[0]) % 24, int(arrivaltime.split(':')[1]),int(arrivaltime.split(':')[2]))
                curTime = datetime.combine(now.date() + timedelta(days=1),
                                            datetime.strptime(time, '%H:%M:%S').time())
            if curTime > now:
                count += 1
                if count > 3:
                    break
                #Append required rows to the final list
                dup2 = curTime - now
                curr_trip_details = []
                curr_trip_details.append(stop_id)
                curr_trip_details.append(trip)
                curr_trip_details.append(arrivaltime)
                curr_trip_details.append(dup2.total_seconds())
                trip_id_result.append(curr_trip_details)
    return sorted(trip_id_result, key=itemgetter(2))



def get_routeid(stopid):
    '''
    Function 'calender_dates_today' - returns all service_id's working current day of the week
    Function 'gettrips_from_serviceid' - returns all trips that that has the above service_id's
    Function 'tripid_from_stopid' - returns all the trips with Time greater than current time using the filtered list
    Current function returns the 3 trips from the given stop id
    '''
    start_time = time.time()
    result = {}
    serviceid_calendar_list = calender_dates_today()
    trips = gettrips_from_serviceid(serviceid_calendar_list)
    stop_times_trip_details = tripid_from_stopid(str(stopid),trips)
    count = 0
    for row1 in stop_times_trip_details:
        trip_details = trips_dict.get(row1[1])
        route_details = routes_dict.get(trip_details[0][0])
        count += 1
        result[str(count)] = {}
        result[str(count)]['stopid'] = str(row1[0])
        result[str(count)]['routeid'] = str(route_details[0])
        result[str(count)]['tripid'] = str(row1[1])
        result[str(count)]['arrivalTime'] = str(row1[2])
        result[str(count)]['remainingTime'] = str(row1[3])
        result[str(count)]['routename'] = str(route_details[3])
    print("--- %s seconds ---" % (time.time() - start_time))
    return result



populate()
print(get_routeid('5749'))

@app.route('/stoproute')
def approute():
    args = request.args.get('stopid')
    return json.dumps(get_routeid(str(args)))


if __name__ == '__main__':
    app.run()
