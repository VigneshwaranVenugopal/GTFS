# GTFS
Looking Bus Project 

This program creates an api to display first three bus (routes) given 'stopid'

Query Schema
1 -> Populate(), populates the gtfs files into dictionaries
2 -> calender_dates_today(), returns all service_id's working current day of the week
3 -> gettrips_from_serviceid(), returns all trips that that has the above service_id's
4 -> tripid_from_stopid - returns all the trips with Time greater than current time using the filtered list
5 -> get_routeid() - returns function returns the 3 trips from the given stop id
