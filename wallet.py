

class Wallet:
	
	currency = 'USD'
	
	def __init__(self, total_funds, investment_ratio):
		self.total_funds = total_funds
		self.investment_funds = total_funds * investment_ratio
	
