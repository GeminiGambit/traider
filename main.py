import portfolio as pf
import wallet as wt
import sys as SYS
import os as OS

cwd = OS.getcwd()
SYS.path.insert(1, OS.path.join(cwd, "utilities"))
import data_handler as dh

def main():
	wallet1 = wt.Wallet(2000, 0.5)
	portfolio = pf.PortFolio(wallet1)
	print "target_asset set to %d %s\n" % (portfolio.get_max_price(), portfolio.wallet.currency)

	data_handler = dh.DataHandler('intraday')
	data_handler.extract_symbols_list()
	#data_handler.symbols = ["MSFT","AAPL","GOOG","CSCO","ZYNE"]

	data_handler.get_symbols_within_range(portfolio.get_max_price())

	print "%d symbols within price range %d %s"%(len(data_handler.symbols_within_range), portfolio.get_max_price(), portfolio.wallet.currency)
	print data_handler.symbols_within_range
	

if __name__ == "__main__":
	print globals()
	main()
