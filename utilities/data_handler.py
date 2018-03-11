'''Definition of the DataHandler class'''

import pandas as PD
import numpy as NP
import os as OS

cwd = OS.getcwd()

class DataHandler:

	def __init__(self, time_frame):
		self.data_dir = OS.path.join(cwd,"data/%s"%time_frame)
		self.symbols_file = OS.path.join(cwd, "symbols.csv")
		self.symbols = []
		self.symbols_within_range = []

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

	def get_dataframe_for_symbol(self,symbol):
		print "Attempting to read %s"%self.symbol_to_path(symbol)
		try:
			dataframe = PD.read_csv(self.symbol_to_path(symbol), na_values=NP.nan, usecols=['open'], engine='c', verbose=True)
			print "dataframe %d %d"% (dataframe.shape[0], dataframe.shape[1])
			return dataframe

		except:
			print "Pandas.read_csv() failed"
			exit

	def get_closing_price(self,dataframe):
		return dataframe.values[-1][0]

	def get_symbols_within_range(self, max_price):
		for symbol in self.symbols:
			try:
				dataframe = self.get_dataframe_for_symbol(symbol)
				closing_price = self.get_closing_price(dataframe)
				if closing_price <= max_price:
					self.symbols_within_range.append((symbol, closing_price))
			except:
				continue

	
