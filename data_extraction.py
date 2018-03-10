from alpha_vantage.timeseries import TimeSeries as Ts
import argparse as Ap
import sys
import csv
import os
import requests
import tqdm

cwd = os.getcwd()
symbols_url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"

class CmdLineArgs:
	def __init__(self):
		self.usl = False
		self.dt = 'full'
cargs = CmdLineArgs()

def parse_cmdline():
	parser = Ap.ArgumentParser()
	parser.add_argument('--update-symbols-list',action='store_true')
	parser.add_argument('--data-type',type=str,nargs=1,choices=['intra','daily','full'],default='full')
	args = parser.parse_args()
	cargs.usl = args.update_symbols_list
	cargs.dt = args.data_type[0]

def update_symbols_list_online():
	try:
		response = requests.get(symbols_url, stream=True)
		tmpfile = os.path.join(cwd,"Newlist.csv")
		with open(tmpfile,"w") as sf:
			for data in tqdm(response.iter_content()):
				sf.write(data)
	except:
			os.remove(tmpfile)
			print "HTTP request for updating symbols list has failed"
			print "Try updating later"

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
			try:
				data, meta_data = ts.get_intraday(symbol= symbol, interval='1min', outputsize='full')
				csvdata=list(data)
				writer.writerows(csvdata)
			except requests.exceptions.ConnectionError as e:
				print "HTTP request for symbol %s has failed, %s" %(symbol, e)
				continue

def get_daily_data(ts, symbols):
	daily_dir = os.path.join(cwd,"data/daily")
	if not os.path.isdir(daily_dir):
		os.mkdir(daily_dir)
	for symbol in symbols:
		with open(symbol_to_path(symbol,'daily'),'w') as fp:
			writer = csv.writer(fp)
			try:
				data, meta_data = ts.get_daily(symbol= symbol, outputsize='full')
				csvdata=list(data)
				writer.writerows(csvdata)
			except requests.exceptions.ConnectionError as e:
				print "HTTP request for symbol %s has failed, %s" %(symbol, e)
				continue

if __name__ == "__main__":
	print "Data acquisition\nCurrent working dir: %s\n"%cwd
	print "Parsing command line\n"
	parse_cmdline()
	data_dir = os.path.join(cwd,"data/")
	if not os.path.isdir(data_dir):
		os.mkdir(data_dir)

	if cargs.usl:
		print "Updating symbols list"
		update_symbols_list_online()
		#symbols_file = os.path.join(cwd, "symbols.csv")
		#extract_symbols_list(symbols_file, symbols)
	symbols=["MSFT","AAPL","GOOG"]

	try:
		ts = Ts(key='MH4A705KCOPRMBUB', output_format='csv',indexing_type='date')
	finally:
		"Alpha_Vantage TimeSeries call denied. Exiting"
		exit

	if cargs.dt == 'intra' or cargs.dt == 'full':
		print "Getting intraday data"
		get_intraday_data(ts, symbols)
	if cargs.dt == 'daily' or cargs.dt == 'full':
		print "\nGetting daily data"
		get_daily_data(ts, symbols)
