import portfolio as pf
import wallet as wt

def main():
	wallet1 = wt.Wallet(10000, 0.5)
	pf1 = pf.PortFolio(wallet1)
	print "target_asset set to %d %s" % (pf1.get_mean_target(), pf1.wallet.currency)
	

if __name__ == "__main__":
	main()
