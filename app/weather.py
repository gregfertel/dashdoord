import requests, datetime
from geopy.geocoders import Nominatim
import plotly.plotly as py
from plotly.graph_objs import *

def get_time(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp))

address = "303 Graham Avenue, Brooklyn, NY 11211"
FORECAST_API_KEY = "44bac1ccdd1e4733a09c032afa4184b0"
PLOTLY_API_KEY = "9ftw3ypj23"
PLOTLY_USERNAME = "gfertel"

def get_latitude_longitude(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    (latitude, longitude) = (location.latitude, location.longitude)
    return (latitude, longitude)

def get_forecast_data(latitude, longitude, key=FORECAST_API_KEY):
    url = "https://api.forecast.io/forecast/%s/%s,%s" % (key, latitude, longitude)
    json_data = requests.get(url).json()
    minutely_data = json_data['minutely']['data']
    current_data = json_data['currently']
    return {'minutely':minutely_data, 'current':current_data}

# Generate Embed HTML
bedford_blue_hex = "#4F748E"
inverted_color = "#B08B71"
def get_forecast_embed_url(color, latitude, longitude, name):
    src="https://forecast.io/embed/#lat=%s&lon=%s&name=%s&color=%s" % (latitude, longitude, name, color)
    return src

def update_plot(minutely_data, filename="Rain_Intensity", key = PLOTLY_API_KEY, username = PLOTLY_USERNAME):
    py.sign_in(username, key)
    times = [get_time(minute['time']) for minute in minutely_data]
    intensity = [minute['precipIntensity'] for minute in minutely_data]
    data = Data([Scatter(x=times, y = intensity, fill='tozeroy',
        fillcolor = "rgba(176, 139, 113, 0.5)",
    line = {'color':"rgb(176, 139, 113)"}
    )])
    layout = Layout(
        xaxis = XAxis(
            showgrid=False,
            zeroline=True,
            ticks='',
            title="Time"),
        yaxis = YAxis(
            title="Rain Intensity",
            showgrid=False,
            showticklabels=False,
            range=[0, 0.1]))
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename="Rain_Intensity", auto_open=False)
    return plot_url