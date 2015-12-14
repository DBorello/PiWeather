import configparser
import logging
import sys
import time

import pigpio
import requests

#logging.basicConfig(level=logger.INFO)
logger = logging.getLogger(__name__)


pi = pigpio.pi()

def main():
	#Load config
	config = configparser.ConfigParser()
	config.read('/boot/PiWeather.ini')

	#Setup logging
	ch = logging.StreamHandler()
	logger.setLevel(logging.getLevelName(config['General'].get('LogLevel','INFO')))
	ch.setLevel(logging.getLevelName(config['General'].get('LogLevel','INFO')))
	logger.addHandler(ch)

	#Parse config
	Gages = ParseConfig(config)

	Weather = WUnderground(config['WUnderground'].get('Station',None))
	Display = AnalogDisplay(Gages)

	while 1:
		try:
			Current = Weather.GetWeather()
			Display.UpdateGages(Current)
			time.sleep(60)
		except KeyboardInterrupt:
			Shutdown()

def ParseConfig(config):
	Gages = []
	for s in config.sections():
		if s == 'General':
			continue

		G = {'GPIO': config.get(s,'GPIO'), 'Min': config.get(s,'Min'), 'Max': config.get(s,'Max')}
		Gages.append(G)

	print Gages
	return Gages

def Shutdown():
	logger.info('Shutting down....')
	pi.stop()
	sys.exit(0)

class WUnderground():
	def __init__(self, Station=None):
		self.Station = Station

		self.Current = {'Temp': 0, 'Humidity': 0, 'Precip': 0, 'Pressure': 30, 'Wind': 0}
		logger.info('Using station: %s',self.Station)

	def GetWeather(self):
		try:
			r = requests.get('http://stationdata.wunderground.com/cgi-bin/stationlookup?station={0:s}&units=english&v=2.0&format=json&_={1:d}'.format(self.Station,int(round(time.time()*1000,0))))
			data = r.json()
			logger.debug('Raw weather response: %s',str(data))

			StationData = data['stations'][list(data['stations'].keys())[0]]

			self.Current['Temp'] = StationData['temperature']
			self.Current['Humidity'] = StationData['humidity']
			self.Current['Pressure'] = StationData['pressure']
			self.Current['Precip'] = StationData['precip_today']
			self.Current['Wind'] =  StationData['wind_speed']

			logger.info('Recieved weather: %s ',str(self.Current))
		except:
			logger.info('Failed to pull weather from WUnderground')
		return self.Current

class AnalogDisplay():
	def __init__(self, Gages):
		self.Gages = Gages
		self.DutyRange = 100
		self.Override = False
		self.OverrideTime = time.time()

		#Initialize output pins
		for G in self.Gages:
			pi.set_PWM_range(G['GPIO'], self.DutyRange) #PWM from 0-100


		#Initialize max button
		pi.set_mode(OverrideButton, pigpio.INPUT)
		pi.set_pull_up_down(OverrideButton, pigpio.PUD_DOWN)
		pi.callback(OverrideButton, pigpio.FALLING_EDGE, self.DoOverride)

		self.StartupAnimation()


	def UpdateGages(self,Current):
		if self.Override:
			logger.debug('In override mode, not updating gages')
			if time.time() - self.OverrideTime > 60:
				self.Override = False
			else:
				return

		for G in self.Gages:
			Reading = Current[G['Name']]
			Range = G['Max'] - G['Min']

			Output = (Reading - G['Min'])/Range
			Output = max(0,min(1,Output))
			Duty = Output*self.DutyRange

			logger.debug('Setting {} to {}'.format(G['Name'], Duty) )
			pi.set_PWM_dutycycle(G['GPIO'], Duty)

	def DoOverride(self, gpio, level, tick):
		logger.info('Doing override')
		self.Override = True
		self.OverrideTime = time.time()
		for G in self.Gages:
			pi.set_PWM_dutycycle(G['GPIO'], self.DutyRange)

	def StartupAnimation(self):
		for G in self.Gages:
			pi.set_PWM_dutycycle(G['GPIO'], self.DutyRange)
			time.sleep(0.5)
			pi.set_PWM_dutycycle(G['GPIO'], 0)


if __name__ == "__main__":
	main()
