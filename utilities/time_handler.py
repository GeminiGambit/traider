'''Definition of the TimeHandler class'''

import datetime as DT
import pandas as PD

class TimeHandler:

	starttime = DT.time(hour=8, minute=0)
	endtime = DT.time(hour=16, minute=0)
	timeframe = 'intraday'

	def __init__(self, timeframe = timeframe):
		inittime = DT.datetime.now()
		self.startdate = "%d-01-01 %d:%d:00" % (inittime.year, self.starttime.hour, self.starttime.minute)
		self.enddate = inittime
		self.datetimes = PD.date_range(self.startdate, self.enddate, freq='T')

def test_run():
	timehandler = TimeHandler()
	print timehandler.datetimes

if __name__ == "__main__":
	test_run()
		
