from alpha_vantage.timeseries import TimeSeries as Ts
import csv
import os

cwd = os.getcwd()

def symbol_to_path(symbol,timeframe):
	path = os.path.join(cwd,"data/%s/%s.csv"%(timeframe,symbol))
	print path
	return path
	

def get_intraday_data(ts, symbols):
	intraday_dir = os.path.join(cwd,"data/intraday")
	if not os.path.isdir(intraday_dir):
		os.mkdir(intraday_dir)
	for symbol in symbols:
		with open(symbol_to_path(symbol,'intraday'),'w') as fp:
			writer = csv.writer(fp)
			data, meta_data = ts.get_intraday(symbol= symbol, interval='1min', outputsize='full')
			csvdata=list(data)
			writer.writerows(csvdata)	

def get_daily_data(ts, symbols):
	daily_dir = os.path.join(cwd,"data/daily")
	if not os.path.isdir(daily_dir):
		os.mkdir(daily_dir)
	for symbol in symbols:
		with open(symbol_to_path(symbol,'daily'),'w') as fp:
			writer = csv.writer(fp)
			data, meta_data = ts.get_daily(symbol= symbol, outputsize='full')
			csvdata=list(data)
			writer.writerows(csvdata)

if __name__ == "__main__":
	print "Data acquisition \n Current working dir: %s\n"%cwd

	ts = Ts(key='MH4A705KCOPRMBUB', output_format='csv',indexing_type='date')
	print "Targetted symbols:\n"
	symbols = ['AAPL','GOOG','MSFT','CSCO']
	print symbols
	print "Getting intraday data"
	get_intraday_data(ts, symbols)
	print "Getting daily data"
	get_daily_data(ts, symbols)
