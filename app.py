from flask import Flask,request,make_response,jsonify
import loadvalues
import sqlite3

loadvalues  #parsing and storing values in database
app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def findRoutes(args):
    con = sqlite3.connect('gtfs.db')
    con.row_factory = dict_factory
    cur = con.cursor()
    a= cur.execute('''select st.trip_id as TripID, r.route_id as RouteID,t.trip_headsign as HeadSign, strftime('%s', time(st.arrival_time)) - strftime('%s', time('now','localtime')) as RemainingSeconds, time(st.arrival_time) as Arrivaltime from stop_times st,trips t,routes r,calendar c where time(st.arrival_time)> time('now','localtime') and t.trip_id=st.trip_id and st.stop_id = ? and r.route_id=t.route_id and c.service_id=t.service_id and c.start_date<strftime('%Y%m%d', 'now', 'localtime') and c.end_date>strftime('%Y%m%d', 'now', 'localtime')
    and ((strftime('%w','now')=0 and c.sunday=1)or
    (strftime('%w','now')='1' and c.monday=1)or
    (strftime('%w','now')='2' and c.tuesday=1)or
    (strftime('%w','now')='3' and c.wednesday=1)or
    (strftime('%w','now')='4' and c.thursday=1)or
    (strftime('%w','now')='5' and c.friday=1)or
    (strftime('%w','now')='6' and c.saturday=1))
    order by RemainingSeconds limit 3;
     ''',(args,))
    result = a.fetchall()
    return result


@app.route('/stoproute')
def approute():
    args = request.args.get('stopid')
    return jsonify(findRoutes(args))


if __name__ == '__main__':
    app.run()
