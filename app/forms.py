from wtforms import TextField, Form

class MainForm(Form):
	subway = TextField('Enter your subway station', id='subway_station')
	address = TextField('Enter your address', id='address')