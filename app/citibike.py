import requests, datetime
from geopy.distance import vincenty
import requests_cache
requests_cache.install_cache('my_cache', backend='memory', expire_after=180)

def get_citibike_data():
	url = "http://www.citibikenyc.com/stations/json"
	response = requests.get(url)
	json_data = response.json()
	return json_data['stationBeanList']

def get_citibike_availability(data, latitude, longitude):
	for i in range(len(data)):
		data[i]['distance'] = round(vincenty((latitude, longitude), (data[i]['latitude'], data[i]['longitude'])).miles, 2)
	closest_stations = sorted(data, key = lambda k: k['distance'])[:4]
	return closest_stations