import portfolio as pf
import wallet as wt
import sys as SYS
import os as OS

cwd = OS.getcwd()
SYS.path.insert(1, OS.path.join(cwd, "utilities"))
import data_handler as dh
import technical_indicators as ti

def main():
	wallet1 = wt.Wallet(2000.0, 0.5)
	portfolio = pf.PortFolio(wallet1)
	print "target_asset set to %d %s\n" % (portfolio.get_max_price(), portfolio.wallet.currency)

	datahandler = dh.DataHandler()
	datahandler.extract_symbols_list()
	#datahandler.symbols = ["MSFT","AAPL","GOOG","CSCO","ZYNE"]

	datahandler.get_symbols_within_range(portfolio.get_max_price())

	print "\n%d symbols within price range %d %s"%(len(datahandler.symbols_within_range), portfolio.get_max_price(), portfolio.wallet.currency)
	print datahandler.symbols_within_range
	print datahandler.within_range_dataframe_close
	print datahandler.within_range_dataframe_volume

if __name__ == "__main__":
	print globals()
	main()
