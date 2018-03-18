import portfolio as pf
import wallet as wt
import sys as SYS
import os as OS

cwd = OS.getcwd()
SYS.path.insert(1, OS.path.join(cwd, "utilities"))
import data_handler as dh
import plot_handler as ph
import technical_indicators as ti

def main():
	wallet1 = wt.Wallet(1000.0, 0.5)
	portfolio = pf.PortFolio(wallet1)
	print "target_asset set to %d %s\n" % (portfolio.get_max_price(), portfolio.wallet.currency)

	plothandler = ph.PlotHandler()

	datahandler = dh.DataHandler()
	datahandler.extract_symbols_list()
	#datahandler.symbols = ["MSFT","AAPL","GOOG","CSCO","VTVT","ZYNE","ZSAN","ZNGA"]

	datahandler.get_symbols_within_range(portfolio.get_max_price())

	print "\n%d symbols within price range %d %s"%(len(datahandler.symbols_within_range), portfolio.get_max_price(), portfolio.wallet.currency)
	print datahandler.symbols_within_range

	datahandler.extract_sufficient_data_symbols()
	print datahandler.target_symbols

	#datahandler.get_dataframes()
	print datahandler.within_range_dataframe_close
	print datahandler.within_range_dataframe_volume

if __name__ == "__main__":
	#print globals()
	main()
