from flask import Flask,request,make_response,jsonify
import csv
from datetime import datetime
from datetime import timedelta
from operator import itemgetter
import json
import  time


app = Flask(__name__)

def populate():
    with open('input/routes.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global routes_list
        routes_list= list(reader)
        f.seek(0)
        next(reader)
        global routes_dict
        routes_dict = {rows[0]: rows for rows in reader}

    with open('input/trips.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global trips_list
        trips_list = list(reader)
        f.seek(0)
        next(reader)
        global trips_id_dict
        global trips_dict
        trips_id_dict = {}
        trips_dict = {}
        for rows in trips_list:
            trips_id_dict.setdefault(rows[1], []).append(rows[2])
            trips_dict.setdefault(rows[2], [] ).append(rows)

    with open('input/stop_times.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global stop_times_list
        stop_times_list = list(reader)
        f.seek(0)
        next(reader)
        global stop_times_dict
        stop_times_dict = {}
        for row in stop_times_list:
            stop_times_dict.setdefault(row[0], {})
            stop_times_dict[row[0]].setdefault(row[3], [])
            stop_times_dict[row[0]][row[3]].append(row[1])
            stop_times_dict[row[0]][row[3]].append(row[2])

    with open('input/calendar.txt', 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header:
            next(reader)
        global calendar_dates_list
        calendar_dates_list = list(reader)
        f.seek(0)
        next(reader)
        global calendar_dict
        calendar_dict = {'monday':[], 'tuesday':[], 'wednesday':[], 'thursday':[], 'friday':[], 'saturday':[], 'sunday':[] }
        for row in calendar_dates_list:
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











#Returns service id of the bus in current date
def calender_dates_today():
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
    trips_from_serviceid = []
    for services in service:
        trips_from_serviceid = trips_from_serviceid + trips_id_dict.get(services)
    return trips_from_serviceid

#Return trip_id, start/end time, remaining_time in sorted order
def tripid_from_stopid(stop_id,trips):
    trip_id_result = []
    count = 0
    now = datetime.now()

    for trip in trips:
        if stop_id in stop_times_dict[trip]:
            arrivaltime = stop_times_dict[trip][stop_id][0].strip()
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
                dup2 = curTime - now
                templist = []
                templist.append(stop_id)
                templist.append(trip)
                templist.append(arrivaltime)
                templist.append(dup2.total_seconds())
                trip_id_result.append(templist)
    return sorted(trip_id_result, key=itemgetter(2))

def get_routeid(stopid):
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
