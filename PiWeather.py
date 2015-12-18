import configparser
import logging
import pigpio
import requests
import sys
import time

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
	OverrideButton = int(config.get('General','OverrideButton'))

	#Initialize
	Display = AnalogDisplay(OverrideButton, Gages)

	while 1:
		try:
			Current = GetWeather(Gages)
			Display.UpdateGages(Current)
			time.sleep(15)
		except KeyboardInterrupt:
			Shutdown()

def ParseConfig(config):
	Gages = []
	for s in config.sections():
		if s == 'General':
			continue

		G = {'Station': s, 'GPIO': int(config.get(s,'GPIO')), 'Min': int(config.get(s,'Min')), 'Max': int(config.get(s,'Max'))}
		Gages.append(G)

	logger.info(Gages)
	return Gages

def Shutdown():
	logger.info('Shutting down....')
	pi.stop()
	sys.exit(0)


def GetWeather(Gages):
	Stations = ''
	Current = {}
	for G in Gages:
		Stations += G['Station'] + ','
		Current[G['Station']] = 0

	try:
		r = requests.get('http://stationdata.wunderground.com/cgi-bin/stationlookup?station={0:s}&units=english&v=2.0&format=json&_={1:d}'.format(Stations,int(round(time.time()*1000,0))))
		data = r.json()
		logger.debug('Raw weather response: %s',str(data))


		for G in Gages:
			Current[G['Station']] = float(data['stations'][G['Station']]['temperature'])
	except Exception, e:
		logger.info('Failed to pull weather from WUnderground for %s', Stations)
		logger.exception(e)

	return Current


class AnalogDisplay():
	def __init__(self, OverrideButton, Gages):
		self.OverrideButton = OverrideButton
		self.Gages = Gages
		self.DutyRange = 100
		self.Override = False
		self.OverrideTime = time.time()

		#Initialize output pins
		for G in self.Gages:
			pi.set_PWM_range(G['GPIO'], self.DutyRange) #PWM from 0-100


		#Initialize max button
		pi.set_mode(self.OverrideButton, pigpio.INPUT)
		pi.set_pull_up_down(self.OverrideButton, pigpio.PUD_DOWN)
		pi.callback(self.OverrideButton, pigpio.FALLING_EDGE, self.DoOverride)

		self.StartupAnimation()


	def UpdateGages(self, Current):
		if self.Override:
			logger.debug('In override mode, not updating gages')
			if time.time() - self.OverrideTime > 60:
				self.Override = False
			else:
				return

		s = ''
		for G in self.Gages:
			Reading = Current[G['Station']]
			Range = G['Max'] - G['Min']

			Output = (Reading - G['Min'])/Range
			Output = max(0,min(1,Output))
			Duty = Output*self.DutyRange

			s += '   ' + G['Station'] +  ' = ' + str(Reading)
			pi.set_PWM_dutycycle(G['GPIO'], Duty)

		logger.info(s)

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
