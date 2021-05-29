from shrimpy.strategy import *


class Portfolio:
    def __init__(self, name: str,
                 rebalance_period: int,
                 strategy: Strategy,
                 strategy_trigger: str,
                 rebalance_threshold: int,
                 max_spread=10,
                 max_slippage=10):
        
        if strategy.is_dynamic:
            strategy: DynamicStrategy
        else:
            strategy: StaticStrategy
        
        self._name = name
        self._strategy_trigger = strategy_trigger
        self._rebalance_period = rebalance_period
        self._rebalance_threshold = rebalance_threshold
        self._strategy = strategy.get_api_format()
        self._max_spread = max_spread
        self._max_slippage = max_slippage
    
    def __get_rebalance_period(self):
        return self.__rebalance_period
    
    def __set_rebalance_period(self, value):
        if self._strategy_trigger == 'threshold':
            self.__rebalance_period = 0
        else:
            self.__rebalance_period = value
    
    _rebalance_period = property(__get_rebalance_period, __set_rebalance_period)
    
    def __get_rebalance_threshold(self):
        return self.__rebalance_threshold
    
    def __set_rebalance_threshold(self, value):
        if self._strategy_trigger == 'interval':
            self.__rebalance_threshold = 100
        else:
            self.__rebalance_threshold = value
    
    _rebalance_threshold = property(__get_rebalance_threshold, __set_rebalance_threshold)
    
    def get_api_format(self):
        return {
            'name': self._name,
            'rebalancePeriod': self.__rebalance_period,
            'strategy': self._strategy,
            'strategyTrigger': self._strategy_trigger,
            'rebalanceThreshold': self.__rebalance_threshold,
            'maxSpread': self._max_spread,
            'maxSlippage': self._max_slippage
        }
