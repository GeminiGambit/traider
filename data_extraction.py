from alpha_vantage.timeseries import TimeSeries as Ts
import csv
import os

cwd = os.getcwd()
symbols_url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"

def update_symbols_list_online():
	os.system("start \"\" http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download")

def extract_symbols_list(symbols_file,symbols):
	with open(symbols_file,'r') as sf:
		sf.readline()
		lines = sf.readlines()
		for line in lines:
			line = line.split(",")
			symbols.append(line[0].strip('"'))
	print "Retrieved %d symbols from %s\n" % (len(symbols), symbols_url)

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
	print "Data acquisition\nCurrent working dir: %s\n"%cwd
	data_dir = os.path.join(cwd,"data/")
	if not os.path.isdir(data_dir):
		os.mkdir(data_dir)

	print "Updating symbols list"
	symbols=[]
	#get_symbols_list_online()
	symbols_file = os.path.join(cwd, "symbols.csv")
	extract_symbols_list(symbols_file, symbols)

	ts = Ts(key='MH4A705KCOPRMBUB', output_format='csv',indexing_type='date')
	print "Getting intraday data"
	get_intraday_data(ts, symbols)
	print "Getting daily data"
	get_daily_data(ts, symbols)
