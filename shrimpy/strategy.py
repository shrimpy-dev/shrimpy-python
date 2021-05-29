from shrimpy.allocation import Allocation


class Strategy:
    def __init__(self, is_dynamic: bool):
        self._is_dynamic = is_dynamic
    
    @property
    def is_dynamic(self):
        return self._is_dynamic


class StaticStrategy(Strategy):
    
    def __init__(self, allocations: list = Allocation):
        super().__init__(False)
        self._allocations = allocations
    
    def get_api_format(self):
        return {
            'isDynamic': self._is_dynamic,
            'allocations': [a.get_api_format() for a in self._allocations]
        }


class DynamicStrategy(Strategy):
    
    def __init__(self, excluded_symbols: list,
                 included_symbols: list,
                 top_asset_count: int,
                 top_asset_offset: int,
                 min_percent: int,
                 max_percent: int,
                 is_equal_weight: bool,
                 is_square_root_weight: bool):
        super().__init__(True)
        self._excluded_symbols = excluded_symbols
        self._included_symbols = included_symbols
        self._top_asset_count = top_asset_count
        self._top_asset_offset = top_asset_offset
        self._min_percent = min_percent
        self._max_percent = max_percent
        self._is_equal_weight = is_equal_weight
        self._is_square_root_weight = is_square_root_weight
    
    def get_api_format(self):
        return {
            'isDynamic': self._is_dynamic,
            'excludedSymbols': self._excluded_symbols,
            'includedSymbols': self._included_symbols,
            'topAssetCount': self._top_asset_count,
            'topAssetOffset': self._top_asset_offset,
            'minPercent': str(self._min_percent),
            'maxPercent': str(self._max_percent),
            'isEqualWeight': self._is_equal_weight,
            'isSquareRootWeight': self._is_square_root_weight
            
        }
