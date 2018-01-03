import urllib2, datetime, requests, json
import nyct_subway_pb2
from google.transit import gtfs_realtime_pb2 

API_KEY = "a27db90d779ca74d641c367e47ddad2a"
FEED_ID = 2
CLIENT_ID = '65a0b73ea161e22c90b89413b91c0750'
COLORS = {
    'A': '#0039A6', 'C': '#0039A6', 'E': '#0039A6',
    'B': '#FF6319', 'D': '#FF6319', 'F': '#FF6319', 'M': '#FF6319',
    'G': '#6CBE45', 'J': '#996633', 'Z': '#996633', 'L': '#A7A9AC',
    'N': '#FCCC0A', 'Q': '#FCCC0A', 'R': '#FCCC0A', 'S': '#808183',
    '1': '#EE352E', '2': '#EE352E', '3': '#EE352E', 
    '4': '#00933C', '5': '#00933C', '6': '#00933C', '7': '#B933AD'
}

def get_realtime_subway(train, feed_id=FEED_ID, key=API_KEY):
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


def get_realtime_subway_elixir(station_id, client_id=CLIENT_ID):
    url = "http://app-ex-mta.herokuapp.com/times/%s?client_id=%s" % (station_id, client_id)
    response = requests.get(url)
    data = response.json()
    return json.dumps(data)


