import json, os, sys, datetime, logging, time
import flask
from app import app
import forms
import weather, subway, citibike
import subway_status
import requests

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

ADDRESS = "303 Graham Avenue, Brooklyn, NY 11211"
LATITUDE = 40.7131728
LONGITUDE = -73.94442019999997
# SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# json_url = os.path.join(SITE_ROOT, "static", "all_stations.json")

# with app.open_resource('static/all_stations.json') as f:
#     STATION_DICTS = json.loads(f.read())
# station_url = 'https://mtaapi.herokuapp.com/stations'
# STATION_DICTS = requests.get(station_url).json()['result']
# STATIONS = {x['name']: x['id'][:-1] for x in STATION_DICTS}

# @app.route('/_autocomplete', methods=['GET'])
# def autocomplete():
#     return flask.Response(json.dumps(STATION_DICTS), mimetype='application/json')


#@app.route('/start', methods=['GET', 'POST'])
#def start():
#    if flask.request.args.get('address') and flask.request.args.get('subway'):
#        return "WOO"
#    else:
#        form = forms.MainForm(flask.request.form)
#        return flask.render_template("start.html", form=form)


@app.route('/crypto')
def crypto_api():
    url = 'https://api.coinmarketcap.com/v1/ticker/'
    resp = requests.get(url)
    data = resp.json()
    prices = {}
    for x in data:
        formatted_price = '${:,.2f}'.format(float(x['price_usd']))
        percent_change = x['percent_change_24h']
        prices[x['name']] = {'price': formatted_price, 'change': percent_change}
    return json.dumps(prices)

@app.route('/weatherwidget')
def weather_widget():
    address = flask.request.args.get('address')
    if not address:
        address = "NEW YORK"
    theme = flask.request.args.get('theme')
    if theme != 'dark':
        theme = 'pure'
    if flask.request.args.get('size') == 'full':
        template = "weatherwidgetfull.html"
    else:
        template = "weatherwidget.html"
    theme = flask.request.args.get('theme')
    if theme == 'dark':
        color = '#000000'
    else:
        theme = 'pure'
        color = 'rgba(255, 255, 255, 0)'

    return flask.render_template(template, address=address.upper(), theme=theme)


@app.route('/weatherwidgetfull')
def weather_widget_full():
    address = flask.request.args.get('address')
    if not address:
        address = "NEW YORK"
    theme = flask.request.args.get('theme')
    if theme == 'dark':
        color = '#000000'
    else:
        theme = 'pure'
        color = 'rgba(255, 255, 255, 0)'

    return flask.render_template("weatherwidgetfull.html", address=address.upper(), theme=theme, color=color)

"""@app.route('/subway')
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
    return json.dumps(subways)"""

@app.route('/subway')
def subway_api(station_id=None):
    if not station_id:
        station_id = flask.request.args.get('station_id')
    if station_id:
        return subway.get_realtime_subway_elixir(station_id)
    else:
        response = app.response_class(
            response=json.dumps({'error': 'missing station_id parameter'}),
            status=422,
            mimetype='application/json'
            )
        return response

@app.route('/subway_status/<route>')
def subway_status_view(route):
    return json.dumps(subway_status.get_subway_status(route))

@app.route('/citibike')
def citibike_api(latitude=None, longitude=None):
    if not latitude and not longitude:
        latitude = float(flask.request.args.get('latitude'))
        longitude = float(flask.request.args.get('longitude'))
    citibike_data = citibike.get_citibike_data()
    station_info = citibike.get_citibike_availability(citibike_data, latitude, longitude)
    return json.dumps(station_info)



@app.route('/')
@app.route('/index')
def page():
    address = flask.request.args.get('address') or flask.request.cookies.get('address')
    subway_choice = flask.request.args.get('subway') or flask.request.cookies.get('subway')
    print address, subway_choice
    latitude = flask.request.cookies.get('latitude')
    longitude = flask.request.cookies.get('longitude')
    if not address or not subway_choice:
        form = forms.MainForm(flask.request.form)
        return flask.render_template("start.html", form=form)
    elif not latitude and not longitude:
        resp = flask.make_response(flask.redirect('/'))
        resp.set_cookie('address', address)
        resp.set_cookie('subway', flask.request.args.get('subway'))
        (latitude, longitude) = weather.get_latitude_longitude(address)
        resp.set_cookie('latitude', str(latitude))
        resp.set_cookie('longitude', str(longitude))
        return resp
    directions = {}
    directions[STATIONS[subway_choice] + 'N'] = 'Manhattan'
    directions[STATIONS[subway_choice] + 'S'] = 'Rockaway Parkway'

    time_updated = datetime.datetime.now()
    # running off local computer, otherwise would need to convert from UTC to EST here
    display_time = time_updated - datetime.timedelta(hours=0)
    #directions = {"L11N":"Manhattan", "L11S":"Rockaway Parkway"}

    
    embed_src = weather.get_forecast_embed_url("", latitude, longitude, address)

    # Update Plotly
    graph_intensity = False
    """weather_data = weather.get_forecast_data(latitude, longitude)
    plot_url = weather.update_plot(weather_data['minutely'])
    if max([minute['precipIntensity'] for minute in weather_data['minutely']]) > 0.005:
        graph_intensity = True"""
    # Get Citibike Info
    print STATIONS[subway_choice]
    subways = json.loads(subway_api(STATIONS[subway_choice]))
    station_info = json.loads(citibike_api(latitude, longitude))
    return flask.render_template("site.html", embed_src = embed_src, 
        graph_intensity=graph_intensity, 
        time=datetime.datetime.strftime(display_time, "%I:%M:%S %p"), 
        subways=subways, subway_station_name=subway_choice, 
        directions=directions, station_info=station_info, 
        latitude=latitude, longitude=longitude, colors=subway.COLORS)