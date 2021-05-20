class Allocation:
    def __init__(self, symbol, percent):
        self.symbol = symbol
        self.percent = percent

    def get_api_format(self):
        return {
            'symbol': self.symbol,
            'percent': self.percent
        }
