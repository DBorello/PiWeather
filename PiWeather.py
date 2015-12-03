import time
import requests

class WUnderground():
	def __init__(self):
		pass

	def GetLocal(self):
		r = requests.get('http://api.wunderground.com/api/d567171cf9081060/geolookup/q/autoip.json')
		data = r.json()
		print(data)

Weather = WUnderground()
Weather.GetLocal()