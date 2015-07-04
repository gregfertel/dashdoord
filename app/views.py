import json, os, sys, datetime, logging
import flask
from app import app
import weather, subway

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
@app.route('/index')
def page():
    address = "303 Graham Avenue, Brooklyn, NY 11211"
    (latitude, longitude) = weather.get_latitude_longitude(address)
    
    embed_src = weather.get_forecast_embed_url("#B08B71", latitude, longitude, "303 Graham Avenue, Brooklyn, NY")

    # Update Plotly
    graph_intensity = False
    weather_data = weather.get_forecast_data(latitude, longitude)
    plot_url = weather.update_plot(weather_data['minutely'])
    if max([minute['precipIntensity'] for minute in weather_data['minutely']]) > 0.005:
        graph_intensity = True

    # Get Subway Info
    subways = {"L11N":[], "L11S":[]}
    directions = {"L11N":"Manhattan", "L11S":"Rockaway Parkway"}
    time_updated = datetime.datetime.now()
    for train in subways:
        subways[train] = [int(round((x - time_updated).seconds/60.0, 0)) for x in subway.get_realtime_subway(train) if x >= time_updated]

    return flask.render_template("site.html", embed_src = embed_src, plot_url = plot_url, 
        graph_intensity = graph_intensity, feels_like = weather_data['current']['apparentTemperature'], 
        time=datetime.datetime.strftime(time_updated, "%I:%M:%S %p"), 
        subways = subways, directions = directions)