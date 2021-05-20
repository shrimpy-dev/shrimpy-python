class Strategy:
    def __init__(self, is_dynamic):
        self._is_dynamic = is_dynamic


class StaticStrategy(Strategy):

    def __init__(self, allocations):
        super(StaticStrategy, self).__init__(False)
        self._allocations = allocations

    """Returns dictionary keyed according to shrimpy allocations type"""

    def get_api_format(self):
        allocations = [a.get_allocation() for a in self._allocations]
        return {
            'isDynamic': self._is_dynamic,
            'allocations': allocations
        }


class DynamicStrategy(Strategy):

    def __init__(self, excluded_symbols, top_asset_count, min_percent, max_percent, is_equal_weight):
        super(DynamicStrategy, self).__init__(True)
        self._excluded_symbols = excluded_symbols
        self._top_asset_count = top_asset_count
        self._min_percent = min_percent
        self._max_percent = max_percent
        self._is_equal_weight = is_equal_weight

    def get_api_format(self):
        return {
            'isDynamic': self._is_dynamic,
            'excludedSymbols': self._excluded_symbols,
            'topAssetCount': self._top_asset_count,
            'minPercent': str(self._min_percent),
            'maxPercent': str(self._max_percent),
            'isEqualWeight': self._is_equal_weight
        }
