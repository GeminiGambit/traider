import pandas as pd
import numpy as np
import wallet

class PortFolio:
	
	def __init__(self, wallet):
		self.wallet = wallet
		self.symbols_space = []
		self.target_assets = []
	
	def get_max_price(self):
		return (self.wallet.investment_funds * 0.02)
	
	def stock_selector(self, mean):
		df_target_assets = pd.DataFrame()
