class Allocation:
    def __init__(self, symbol, percent):
        self._symbol = symbol
        self._percent = percent
    
    def get_api_format(self):
        return {
            'symbol': self._symbol,
            'percent': self._percent
        }
