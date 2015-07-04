import urllib2, datetime
import nyct_subway_pb2
from google.transit import gtfs_realtime_pb2 

API_KEY = "a27db90d779ca74d641c367e47ddad2a"
FEED_ID = 2

def get_realtime_subway(train, feed_id = FEED_ID, key = API_KEY):
    feed = gtfs_realtime_pb2.FeedMessage() 
    url = 'http://datamine.mta.info/mta_esi.php?key=%s&feed_id=%s' % (key, feed_id)
    response = urllib2.urlopen(url)
    feed.ParseFromString(response.read())
    arrival_times = []
    for thing in feed.entity:
        for stop_time_update in thing.trip_update.stop_time_update:
            if stop_time_update.stop_id == train:
                arrival_times.append(datetime.datetime.fromtimestamp(stop_time_update.arrival.time))
    return sorted(arrival_times)
