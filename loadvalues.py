import sqlite3
import csv
import os


if os.path.exists('example.db'):
    os.remove('example.db')

f = open('input/agency.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)

sql = sqlite3.connect('example.db')
cur = sql.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS agency
            (agency_id real,agency_name text,agency_url text,
            agency_timezone text,agency_lang text,agency_phone text,agency_fare_url text)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO agency VALUES (?, ?, ?, ?, ?, ?, ?)", row)

f.close()

f = open('input/calendar.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS calendar
            (service_id real,monday real,tuesday real,wednesday real,
            thursday real,friday real,saturday real,sunday real,start_date text,end_date text)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO calendar VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
f.close()

f = open('input/calendar_dates.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS calendar_dates
            (service_id real,date real,exception_type text)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO calendar_dates VALUES (?, ?, ?)", row)
f.close()

f = open('input/feed_info.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS feed_info
            (feed_publisher_name text,feed_publisher_url text,feed_lang text,
            feed_start_date real,feed_end_date real,feed_version real)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO feed_info VALUES (?, ?, ?, ?, ?, ?)", row)
f.close()

f = open('input/routes.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS routes
            (route_id real,agency_id real,route_short_name real,route_long_name text,route_desc text,route_type text,
            route_url text,route_color text,route_text_color text)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO routes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
f.close()


f = open('input/shapes.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS shapes
            (shape_id real,shape_pt_lat real,shape_pt_lon real,shape_pt_sequence real,shape_dist_traveled real)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO shapes VALUES (?, ?, ?, ?, ?)", row)
f.close()

f = open('input/stop_times.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS stop_times
            (trip_id real,arrival_time text,departure_time text,stop_id real,stop_sequence real,
            stop_headsign real,pickup_type real,drop_off_type real,shape_dist_traveled real)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO stop_times VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
f.close()

f = open('input/stops.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS stops
            (stop_id real,stop_code real,stop_name text,stop_desc text,stop_lat real,stop_lon real,zone_id real,
            stop_url text,location_type text,parent_station text,stop_timezone text,wheelchair_boarding text)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO stops VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
f.close()


f = open('input/trips.txt', 'r')  # open the csv data file
next(f, None)  # skip the header row
reader = csv.reader(f)
cur.execute('''CREATE TABLE IF NOT EXISTS trips
            (route_id real,service_id real,trip_id real,trip_headsign text,trip_short_name text,
            direction_id real,block_id real,shape_id real,wheelchair_accessible real,bikes_allowed real)''')
for row in reader:
    cur.execute("INSERT OR REPLACE INTO trips VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
f.close()

sql.commit()
sql.close()