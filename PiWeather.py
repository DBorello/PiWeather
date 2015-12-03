import time
import requests

class WUnderground():
	def __init__(self):
		self.Station = ''
		self.GetLocal()

	def GetLocal(self):
		r = requests.get('http://api.wunderground.com/api/d567171cf9081060/geolookup/q/autoip.json')
		data = r.json()
		self.Station = data['location']['nearby_weather_stations']['pws']['station'][0]['id']

	def GetWeather(self):
		r = requests.get('http://stationdata.wunderground.com/cgi-bin/stationlookup?station={0:s}&units=english&v=2.0&format=json&_={1:i}'.format(self.Station,round(time.time()*1000,0)))
		data = r.json
		print(r.json)

Weather = WUnderground()
Weather.GetWeather()