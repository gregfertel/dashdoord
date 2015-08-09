import requests, datetime
from geopy.distance import vincenty

def get_citibike_data():
	json_data = requests.get("http://www.citibikenyc.com/stations/json").json()
	return json_data['stationBeanList']

def get_citibike_availability(data, latitude, longitude):
	for i in range(len(data)):
		data[i]['distance'] = round(vincenty((latitude, longitude), (data[i]['latitude'], data[i]['longitude'])).miles, 2)
	closest_stations = sorted(data, key = lambda k: k['distance'])[:4]
	return closest_stations