import json, os, sys, datetime, logging, time
import flask
from app import app
import weather, subway, citibike

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

ADDRESS = "303 Graham Avenue, Brooklyn, NY 11211"
LATITUDE = 40.7131728
LONGITUDE = -73.94442019999997

@app.route('/subway')
def subway_api():
    display_time = datetime.datetime.now()
    # Get Subway Info
    subways = {"L11N":[], "L11S":[]}
    for train in subways:
        subway_success = False
        while not subway_success:
            try:
                realtime = subway.get_realtime_subway(train)
                subways[train] = [int(round((x - display_time).seconds/60.0, 0)) for x in realtime if x >= display_time]
                subway_success = True
            except:
                print "subway error: sleeping 5 seconds"
                time.sleep(5)
    return json.dumps(subways)

@app.route('/citibike')
def citibike_api(latitude=LATITUDE, longitude=LONGITUDE):
    citibike_data = citibike.get_citibike_data()
    station_info = citibike.get_citibike_availability(citibike_data, latitude, longitude)
    return json.dumps(station_info)



@app.route('/')
@app.route('/index')
def page():
    address = "303 Graham Avenue, Brooklyn, NY 11211"
    #(latitude, longitude) = weather.get_latitude_longitude(address)
    # latitude and longitude for 303 Graham Avenue, Brooklyn NY 11211
    latitude = 40.7131728
    longitude = -73.94442019999997

    time_updated = datetime.datetime.now()
    # running off local computer, otherwise would need to convert from UTC to EST here
    display_time = time_updated - datetime.timedelta(hours=0)
    directions = {"L11N":"Manhattan", "L11S":"Rockaway Parkway"}

    
    embed_src = weather.get_forecast_embed_url("#B08B71", latitude, longitude, "303 Graham Avenue, Brooklyn, NY")

    # Update Plotly
    graph_intensity = False
    """weather_data = weather.get_forecast_data(latitude, longitude)
    plot_url = weather.update_plot(weather_data['minutely'])
    if max([minute['precipIntensity'] for minute in weather_data['minutely']]) > 0.005:
        graph_intensity = True"""
    # Get Citibike Info
    subways = json.loads(subway_api())
    station_info = json.loads(citibike_api())
    return flask.render_template("site.html", embed_src = embed_src, 
        graph_intensity=graph_intensity, 
        time=datetime.datetime.strftime(display_time, "%I:%M:%S %p"), 
        subways=subways, directions=directions, station_info=station_info)