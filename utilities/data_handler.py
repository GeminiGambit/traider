'''Definition of the DataHandler class'''

import pandas as PD
import numpy as NP
import os as OS

import datetime as DT
import time_handler as th
cwd = OS.getcwd()


class DataHandler:

	timehandler = th.TimeHandler()
	#NASDAQ composite index
	ref_symbol = "^IXIQ"

	def __init__(self):
		self.data_dir = OS.path.join(cwd,"data/%s"%self.timehandler.timeframe)
		self.symbols_file = OS.path.join(cwd, "symbols.csv")
		self.symbols = []
		self.symbols_within_range = []
		self.target_symbols = []
		self.within_range_dataframe_close = PD.DataFrame()
		self.within_range_dataframe_volume = PD.DataFrame()
		self.data_threshold = 0

	def extract_symbols_list(self):
		with open(self.symbols_file,'r') as sf:
			sf.readline()
			lines = sf.readlines()
			for line in lines:
				line = line.split(",")
				self.symbols.append(line[0].strip('"'))
		print "Retrieved %d symbols from %s\n" % (len(self.symbols), self.symbols_file)

	def symbol_to_path(self,symbol):
		path = OS.path.join(cwd,"%s/%s.csv"%(self.data_dir,symbol))
		return path

	def get_dataframe_for_symbol(self,symbol,column):
		#print "\nAttempting to read %s"%self.symbol_to_path(symbol)
		try:
			dataframe = PD.read_csv(self.symbol_to_path(symbol), na_values=NP.nan, usecols=['timestamp',column], engine='c', verbose=False)
			#print "dataframe %d %d"% (dataframe.shape[0], dataframe.shape[1])
			return dataframe

		except:
			#print "Pandas.read_csv() failed for symbol %s" % symbol
			exit

	def join_dataframes(self, dataframe1, dataframe2, column, symbol):
		dataframe2 = dataframe2.rename(columns={column:symbol})
		dataframe2 = dataframe2.set_index('timestamp')
		dataframe1 = dataframe1.join(dataframe2,how='outer')
		#dataframe1.dropna(axis=0, how='any', inplace=True)
		return dataframe1

	def get_closing_price(self,dataframe):
		return dataframe.values[0][1]

	def get_symbols_within_range(self, max_price):
		for symbol in self.symbols:
			try:
				dataframe_close = self.get_dataframe_for_symbol(symbol, 'close')
				closing_price = self.get_closing_price(dataframe_close)
				#print "Closing_price %f"%closing_price
				if closing_price <= max_price:
					self.symbols_within_range.append((symbol, closing_price, dataframe_close.shape[0]))
					'''self.within_range_dataframe_close = self.join_dataframes(self.within_range_dataframe_close, dataframe_close, 'close', symbol)
					dataframe_volume = self.get_dataframe_for_symbol(symbol, 'volume')
					self.within_range_dataframe_volume = self.join_dataframes(self.within_range_dataframe_volume, dataframe_volume, 'volume', symbol)'''
			except:
				continue

	def get_data_threshold(self):
		max_entry = 0
		for entry in self.symbols_within_range:
			if (entry[2] > max_entry):
				max_entry = entry[2]
		print "Max data points %d" % max_entry
		self.data_threshold = int(0.8 * max_entry)

	def extract_sufficient_data_symbols(self):
		self.get_data_threshold()
		self.target_symbols = [entry for entry in self.symbols_within_range if entry[2] > self.data_threshold]
		print "%d symbols meet data threshold of %d\n" %(len(self.target_symbols), self.data_threshold)

	def get_dataframes(self):
		for entry in self.target_symbols:
			symbol = entry[0]
			data_frame_close = self.get_dataframe_for_symbol(symbol, 'close')
			self.within_range_dataframe_close = self.join_dataframes(self.within_range_dataframe_close, data_frame_close, 'close', symbol)
			data_frame_volume = self.get_dataframe_for_symbol(symbol, 'volume')
			self.within_range_dataframe_volume = self.join_dataframes(self.within_range_dataframe_volume, data_frame_volume, 'volume', symbol)

	
