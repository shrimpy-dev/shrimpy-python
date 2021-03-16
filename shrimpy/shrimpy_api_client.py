import requests
import json
from urllib.parse import urlencode
from shrimpy.auth_provider import AuthProvider


class ShrimpyApiClient():
    """Authenticated access to the Shrimpy Developer API"""

    def __init__(self, key, secret, timeout=300):
        self.url = 'https://dev-api.shrimpy.io/v1/'
        self.auth_provider = None
        self.timeout = timeout
        if (key and secret):
            self.auth_provider = AuthProvider(key, secret)
        self.session = requests.Session()

    ##########
    # Public #
    ##########

    def get_supported_exchanges(self):
        endpoint = 'list_exchanges'
        return self._call_endpoint('get', endpoint)


    def get_exchange_assets(self, exchange):
        endpoint = 'exchanges/{}/assets'.format(exchange)
        return self._call_endpoint('GET', endpoint)

    
    def get_trading_pairs(self, exchange):
        endpoint = 'exchanges/{}/trading_pairs'.format(exchange)
        return self._call_endpoint('GET', endpoint)


    ###############
    # Market Data #
    ###############

    def get_ticker(self, exchange):
        endpoint = 'exchanges/{}/ticker'.format(exchange)
        return self._call_endpoint('GET', endpoint)


    def get_orderbooks(self, exchange, base_symbol=None, quote_symbol=None, limit=None):
        endpoint = 'orderbooks'

        params = {
            'exchange': exchange 
        }
        self._add_param_or_ignore(params, 'baseSymbol', base_symbol)
        self._add_param_or_ignore(params, 'quoteSymbol', quote_symbol)
        self._add_param_or_ignore(params, 'limit', limit)

        query_string = self._create_query_string(
            endpoint, 
            params
        )

        return self._call_endpoint('GET', query_string)


    def get_candles(self, exchange, base_trading_symbol, quote_trading_symbol, interval, start_time=None):
        endpoint = 'exchanges/{}/candles'.format(exchange)
        params = {
            'baseTradingSymbol': base_trading_symbol,
            'quoteTradingSymbol': quote_trading_symbol,
            'interval': interval
        }
        self._add_param_or_ignore(params, 'startTime', start_time)

        query_string = self._create_query_string(
            endpoint,
            params
        )

        return self._call_endpoint('GET', query_string)

    #########
    # Users #
    #########

    def list_users(self):
        endpoint = 'users'
        return self._call_endpoint('GET', endpoint)

    
    def get_user(self, user_id):
        endpoint = 'users/{}'.format(user_id)
        return self._call_endpoint('GET', endpoint)

    
    def create_user(self, name):
        endpoint = 'users'
        data = None

        if name is not None:
            data = {'name': name}

        return self._call_endpoint('POST', endpoint, data=data)

    
    def name_user(self, user_id, name):
        endpoint = 'users/{}/name'.format(user_id)
        data = { 'name': name }
        return self._call_endpoint('POST', endpoint, data=data)


    def remove_user(self, user_id):
        endpoint = 'users/{}'.format(user_id)
        return self._call_endpoint('DELETE', endpoint)


    # Deprecated
    def enable_user(self, user_id):
        endpoint = 'users/{}/enable'.format(user_id)
        return self._call_endpoint('POST', endpoint)


    # Deprecated
    def disable_user(self, user_id):
        endpoint = 'users/{}/disable'.format(user_id)
        return self._call_endpoint('POST', endpoint)

    
    #################
    # User API Keys #
    #################

    def get_api_keys(self, user_id):
        endpoint = 'users/{}/keys'.format(user_id)
        return self._call_endpoint('GET', endpoint)

    
    def create_api_keys(self, user_id):
        endpoint = 'users/{}/keys'.format(user_id)
        return self._call_endpoint('POST', endpoint)

    
    def delete_api_keys(self, user_id, public_key):
        endpoint = 'users/{}/keys/{}'.format(user_id, public_key)
        return self._call_endpoint('DELETE', endpoint)

    
    def get_api_key_permissions(self, user_id, public_key):
        endpoint = 'users/{}/keys/{}/permissions'.format(user_id, public_key)
        return self._call_endpoint('GET', endpoint)

    
    def set_api_key_permissions(self, user_id, public_key, account, trade):
        endpoint = 'users/{}/keys/{}/permissions'.format(user_id, public_key)
        data = {
            'account': account,
            'trade': trade
        }
        return self._call_endpoint('POST', endpoint, data=data)


    ############
    # Accounts #
    ############

    def list_accounts(self, user_id):
        endpoint = 'users/{}/accounts'.format(user_id)
        return self._call_endpoint('GET', endpoint)

    
    def get_account(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}'.format(user_id, exchange_account_id)
        return self._call_endpoint('GET', endpoint)

    
    def link_account(self, user_id, exchange, public_key, private_key, passphrase=None):
        endpoint = 'users/{}/accounts'.format(user_id)
        data = {
            'exchange': exchange,
            'publicKey': public_key,
            'privateKey': private_key
        }
        self._add_param_or_ignore(data, 'passphrase', passphrase)

        return self._call_endpoint('POST', endpoint, data=data)

    
    def unlink_account(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}'.format(user_id, exchange_account_id)
        return self._call_endpoint('DELETE', endpoint)

    
    def get_ip_whitelist_addresses(self, user_id):
        endpoint = 'users/{}/whitelist'.format(user_id)
        return self._call_endpoint('GET', endpoint)

    
    ###########
    # Trading #
    ###########

    def create_trade(self, user_id, exchange_account_id, 
        from_symbol, to_symbol, amount, smart_routing=None, max_spread_percent=None, max_slippage_percent=None
    ):
        endpoint = 'users/{}/accounts/{}/trades'.format(user_id, exchange_account_id)
        data = {
            'fromSymbol': from_symbol,
            'toSymbol': to_symbol,
            'amount': amount,
            'smartRouting': smart_routing,
            'maxSpreadPercent': max_spread_percent,
            'maxSlippagePercent': max_slippage_percent
        }

        return self._call_endpoint('POST', endpoint, data=data)

    
    def get_trade_status(self, user_id, exchange_account_id, trade_id):
        endpoint = 'users/{}/accounts/{}/trades/{}'.format(user_id, exchange_account_id, trade_id)
        return self._call_endpoint('GET', endpoint)


    def list_active_trades(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}/trades'.format(user_id, exchange_account_id)
        return self._call_endpoint('GET', endpoint)


    ## Balances
    
    def get_balance(self, user_id, exchange_account_id, date=None):
        endpoint = 'users/{}/accounts/{}/balance'.format(user_id, exchange_account_id)
        params = {}
        self._add_param_or_ignore(params, 'date', date)
        query_string = self._create_query_string(
            endpoint,
            params
        )
        return self._call_endpoint('GET', query_string)

    
    def get_total_balance_history(self, user_id, exchange_account_id, start_time=None, end_time=None):
        endpoint = 'users/{}/accounts/{}/total_balance_history'.format(user_id, exchange_account_id)
        params = {}
        self._add_param_or_ignore(params, 'startTime', start_time)
        self._add_param_or_ignore(params, 'endTime', end_time)
        query_string = self._create_query_string(
            endpoint,
            params
        )
        return self._call_endpoint('GET', query_string)


    ## Asset Management

    def rebalance(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}/rebalance'.format(user_id, exchange_account_id)
        return self._call_endpoint('POST', endpoint)

    
    def get_rebalance_period(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}/rebalance_period'.format(user_id, exchange_account_id)
        return self._call_endpoint('GET', endpoint)

    
    def set_rebalance_period(self, user_id, exchange_account_id, rebalance_period):
        endpoint = 'users/{}/accounts/{}/rebalance_period'.format(user_id, exchange_account_id)
        data = {
            'rebalancePeriod': rebalance_period
        }
        return self._call_endpoint('POST', endpoint, data=data)

    
    def get_strategy(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}/strategy'.format(user_id, exchange_account_id)
        return self._call_endpoint('GET', endpoint)

    
    def set_strategy(self, user_id, exchange_account_id, strategy):
        endpoint = 'users/{}/accounts/{}/strategy'.format(user_id, exchange_account_id)
        return self._call_endpoint('POST', endpoint, data=strategy)

    
    def clear_strategy(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}/strategy'.format(user_id, exchange_account_id)
        return self._call_endpoint('DELETE', endpoint)


    def allocate(self, user_id, exchange_account_id, strategy):
        endpoint = 'users/{}/accounts/{}/allocate'.format(user_id, exchange_account_id)
        return self._call_endpoint('POST', endpoint, data=strategy)


    ## Limit Order

    def place_limit_order(self, user_id, exchange_account_id,
        base_symbol, quote_symbol, amount, price, side, time_in_force
    ):
        endpoint = 'users/{}/accounts/{}/orders'.format(user_id, exchange_account_id)

        data = {
            'baseSymbol': base_symbol,
            'quoteSymbol': quote_symbol,
            'quantity': amount,
            'price': price,
            'side': side,
            'timeInForce': time_in_force
        }

        return self._call_endpoint('POST', endpoint, data=data)


    def get_limit_order_status(self, user_id, exchange_account_id, order_id):
        endpoint = 'users/{}/accounts/{}/orders/{}'.format(user_id, exchange_account_id, order_id)
        return self._call_endpoint('GET', endpoint)
    
    
    def list_open_orders(self, user_id, exchange_account_id):
        endpoint = 'users/{}/accounts/{}/orders'.format(user_id, exchange_account_id)
        return self._call_endpoint('GET', endpoint)

    
    def cancel_limit_order(self, user_id, exchange_account_id, order_id):
        endpoint = 'users/{}/accounts/{}/orders/{}'.format(user_id, exchange_account_id, order_id)
        return self._call_endpoint('DELETE', endpoint)


    #############    
    # Analytics #
    #############

    ## Backtest

    def get_backtest_assets(self, exchange, start_time=None, end_time=None):
        endpoint = 'analytics/backtest/{}/assets'.format(exchange)
        params = {}
        self._add_param_or_ignore(params, 'startTime', start_time)
        self._add_param_or_ignore(params, 'endTime', end_time)
        query_string = self._create_query_string(
            endpoint,
            params
        )
        return self._call_endpoint('GET', endpoint, query_string)

    
    def run_backtest(self, exchange, rebalance_period, fee, start_time, end_time,
        initial_value, allocations
    ):
        endpoint = 'analytics/backtest/{}/run'.format(exchange)
        data = {
            'rebalancePeriod': rebalance_period,
            'fee': fee,
            'startTime': start_time,
            'endTime': end_time,
            'initialValue': initial_value,
            'allocations': allocations
        }
        return self._call_endpoint('POST', endpoint, data=data)

     ## Predictions

    def get_predictions(self, exchange, base_trading_symbol, quote_trading_symbol):
        endpoint = 'analytics/predict'
        params = {
            'exchange':exchange,
            'baseTradingSymbol': base_trading_symbol,
            'quoteTradingSymbol': quote_trading_symbol
        }
        query_string = self._create_query_string(
            endpoint,
            params
        )
        return self._call_endpoint('GET', query_string)

    ## Insights

    def get_asset_dominance(self): 
        endpoint = 'insights/asset_dominance'
        return self._call_endpoint('GET', endpoint)

    
    def get_asset_popularity(self):
        endpoint = 'insights/asset_popularity'
        return self._call_endpoint('GET', endpoint)


    ##############
    # Historical #
    ##############

    def get_historical_trades(self, exchange, base_trading_symbol, quote_trading_symbol, start_time, end_time, limit):
        endpoint = 'historical/trades'
        params = {
            'exchange': exchange,
            'baseTradingSymbol': base_trading_symbol,
            'quoteTradingSymbol': quote_trading_symbol,
            'startTime': start_time,
            'endTime': end_time,
            'limit': limit
        }
        query_string = self._create_query_string(
            endpoint,
            params
        )

        return self._call_endpoint('GET', query_string)


    def get_historical_orderbooks(self, exchange, base_trading_symbol, quote_trading_symbol, start_time, end_time, limit):
        endpoint = 'historical/orderbooks'
        params = {
            'exchange': exchange,
            'baseTradingSymbol': base_trading_symbol,
            'quoteTradingSymbol': quote_trading_symbol,
            'startTime': start_time,
            'endTime': end_time,
            'limit': limit
        }
        query_string = self._create_query_string(
            endpoint,
            params
        )

        return self._call_endpoint('GET', query_string)


    def get_historical_candles(self, exchange, base_trading_symbol, quote_trading_symbol, start_time, end_time, limit, interval):
        endpoint = 'historical/candles'
        params = {
            'exchange': exchange,
            'baseTradingSymbol': base_trading_symbol,
            'quoteTradingSymbol': quote_trading_symbol,
            'startTime': start_time,
            'endTime': end_time,
            'limit': limit,
            'interval': interval
        }
        query_string = self._create_query_string(
            endpoint,
            params
        )

        return self._call_endpoint('GET', query_string)


    def get_historical_instruments(self, exchange=None, base_trading_symbol=None, quote_trading_symbol=None):
        endpoint = 'historical/instruments'
        params = {}
        self._add_param_or_ignore(params, 'exchange', exchange)
        self._add_param_or_ignore(params, 'baseTradingSymbol', base_trading_symbol)
        self._add_param_or_ignore(params, 'quoteTradingSymbol', quote_trading_symbol)
        query_string = self._create_query_string(
            endpoint,
            params
        )

        return self._call_endpoint('GET', query_string)


    def get_historical_count(self, data_type, exchange, base_trading_symbol, quote_trading_symbol, start_time, end_time):
        endpoint = 'historical/count'
        params = {
            'type': data_type,
            'exchange': exchange,
            'baseTradingSymbol': base_trading_symbol,
            'quoteTradingSymbol': quote_trading_symbol,
            'startTime': start_time,
            'endTime': end_time
        }
        query_string = self._create_query_string(
            endpoint,
            params
        )

        return self._call_endpoint('GET', query_string)


    ##############
    # Management #
    ##############

    def get_status(self):
        endpoint = 'management/status'

        return self._call_endpoint('GET', endpoint)


    def get_credits(self):
        endpoint = 'management/credits'

        return self._call_endpoint('GET', endpoint)


    # Deprecated
    def get_usage(self):
        endpoint = 'management/usage'

        return self._call_endpoint('GET', endpoint)


    #############
    # WebSocket #
    #############

    def get_token(self):
        endpoint = 'ws/token'

        return self._call_endpoint('GET', endpoint)


    ###########
    # Helpers #
    ###########

    def _call_endpoint(self, method, endpoint, params=None, data=None):
        url = self.url + endpoint
        if data is not None:
            data = json.dumps(data)

        api_request = self.session.request(
            method,
            url,
            params=params,
            data=data,
            auth=self.auth_provider,
            timeout=self.timeout
        )

        return api_request.json()

    def _create_query_string(self, endpoint, params):
        return endpoint + '?' + urlencode(params)

    def _add_param_or_ignore(self, params, key, value):
        if value is not None:
            params[key] = value

    

