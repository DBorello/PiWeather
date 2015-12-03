import time
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

class WUnderground():
	def __init__(self):
		self.Station = ''
		self.Current = {'Temp': 0, 'Humidity': 0, 'Precip': 0, 'Pressure': 30, 'Wind': 0}
		self.GetLocal()

	def GetLocal(self):
		r = requests.get('http://api.wunderground.com/api/d567171cf9081060/geolookup/q/autoip.json')
		data = r.json()
		logging.debug('Raw geoip response',data)
		self.Station = data['location']['nearby_weather_stations']['pws']['station'][0]['id']
		logging.info('Using geolocation station: ',self.Station)

	def GetWeather(self):
		r = requests.get('http://stationdata.wunderground.com/cgi-bin/stationlookup?station={0:s}&units=english&v=2.0&format=json&_={1:d}'.format(self.Station,int(round(time.time()*1000,0))))
		data = r.json()
		logging.debug('Raw weather response',data)

		StationData = data['stations'][data['stations'].keys()[0]]

		self.Current['Temp'] = StationData['temperature']
		self.Current['Humidity'] = StationData['humidity']
		self.Current['Precip'] = StationData['precip_today']
		self.Current['Pressure'] = StationData['pressure']
		self.Current['Wind'] =  StationData['wind_speed']

		logging.info('Recieved weather: ',str(Current))

		return self.Current




Weather = WUnderground()
Current = Weather.GetWeather()