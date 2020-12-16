# shrimpy-python

The official python library for the Shrimpy Developer API https://developers.shrimpy.io/docs. The library is currently only python3 compatible.

## Installation

```bash
pip install shrimpy-python
```

## Quick Start

All requests are synchronous. For a comprehensive API usage guide, please see https://developers.shrimpy.io/docs.

If you would like to use the async/await style similar to our Node.js library, consider using the ```asyncio``` python library to wrap the synchronous requests provided here.

```python
import shrimpy

public_key = 'bea8edb348af226...'
secret_key = 'df84c39fb49026dcad9d99...'
client = shrimpy.ShrimpyApiClient(public_key, secret_key)
ticker = client.get_ticker('bittrex')
```

## Public Endpoints

The clients for both the public and authenticated endpoints are identical. Please note that if you attempt to use the authenticated endpoints without keys, it will fail.

* [`get_supported_exchanges`](https://developers.shrimpy.io/docs/#get-supported-exchanges)

```python
supported_exchanges = client.get_supported_exchanges()
```

* [`get_exchange_assets`](https://developers.shrimpy.io/docs/#get-exchange-assets)

```python
exchange_assets = client.get_exchange_assets('bittrex')
```

* [`get_trading_pairs`](https://developers.shrimpy.io/docs/#get-trading-pairs)

```python
trading_pairs = client.get_trading_pairs('bittrex')
```

### Market Data Methods

* [`get_ticker`](https://developers.shrimpy.io/docs/#get-ticker)

```python
ticker = client.get_ticker('bittrex')
```

* [`get_orderbooks`](https://developers.shrimpy.io/docs/#get-order-books)

```python
orderbooks = client.get_orderbooks(
    'bittrex',  # exchange
    'XLM',      # base_symbol
    'BTC',      # quote_symbol
    10          # limit
)
```

* [`get_candles`](https://developers.shrimpy.io/docs/#get-candles)

```python
candles = client.get_candles(
    'bittrex',  # exchange
    'XLM',      # base_trading_symbol
    'BTC',      # quote_trading_symbol
    '15m'       # interval
)
```

## Authenticated Endpoints

As mentioned above, please use the provided Shrimpy API keys to access the authenticated endpoints. Endpoints such as user management require the master api key, while endpoints such as trading will work with either a master api key or a user api key.

### User Management Methods

* [`list_users`](https://developers.shrimpy.io/docs/#list-users)

```python
users = client.list_users()
```

* [`get_user`](https://developers.shrimpy.io/docs/#get-a-user)

```python
user = client.get_user(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8' # user_id
)
```

* [`create_user`](https://developers.shrimpy.io/docs/#creating-a-user)

```python
create_user_response = client.create_user(
    'mycustomname' # (optional) name
)
user_id = create_user_response['id']
```

* [`name_user`](https://developers.shrimpy.io/docs/#naming-a-user)

```python
client.name_user(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    'mycustomname' # name
)
```

* [`remove_user`](https://developers.shrimpy.io/docs/#removing-a-user)

```python
client.remove_user(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
)
```

### User API Keys Methods

* [`get_api_keys`](https://developers.shrimpy.io/docs/#get-api-keys)

```python
public_user_keys = client.get_api_keys(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8' # user_id
)
```

* [`create_api_keys`](https://developers.shrimpy.io/docs/#create-api-keys)

```python
user_api_keys = client.create_api_keys(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8' # user_id
)
```

* [`delete_api_keys`](https://developers.shrimpy.io/docs/#delete-api-keys)

```python
client.delete_api_keys(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',                            # user_id
    '51ac18b7d208f59b3c88acbb1ecefe6ba6be6ea4edc07e7a2450307ddc27ab80' # public_key
)
```

* [`get_api_key_permissions`](https://developers.shrimpy.io/docs/#get-api-key-permissions)

```python
permissions = client.get_api_key_permissions(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',                            # user_id
    '51ac18b7d208f59b3c88acbb1ecefe6ba6be6ea4edc07e7a2450307ddc27ab80' # public_key
)
```

* [`set_api_key_permissions`](https://developers.shrimpy.io/docs/#set-api-key-permissions)

```python
client.set_api_key_permissions(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',                             # user_id
    '51ac18b7d208f59b3c88acbb1ecefe6ba6be6ea4edc07e7a2450307ddc27ab80', # public_key
    True,                                                               # enable account methods
    False                                                               # enable trading methods
)
```

### Account Methods

* [`list_accounts`](https://developers.shrimpy.io/docs/#list-accounts)

```python
accounts = client.list_accounts(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8' # user_id
)
```

* [`get_account`](https://developers.shrimpy.io/docs/#get-an-account)

```python
account = client.get_account(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # exchange_account_id
)
```

* [`link_account`](https://developers.shrimpy.io/docs/#link-an-exchange-account)

```python
link_account_response = client.link_account(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',                             # user_id
    'binance',                                                          # exchange
    'GOelL5FT6TklPxAzICIQK25aqct52T2lHoKvtcwsFla5sbVXmeePqVJaoXmXI6Qd', # public_key (a.k.a. apiKey)
    'SelUuFq1sF2zGd97Lmfbb4ghITeziKo9IvM5NltjEdffatRN1N5vfHXIU6dsqRQw',  # private_key (a.k.a. secretKey
    'mypassphrase'                                                       # (optional)passphrase - required for exchanges with passphrases like CoinbasePro
)
account_id = link_account_response['id']
```

* [`unlink_account`](https://developers.shrimpy.io/docs/#unlink-an-exchange-account)

```python
client.unlink_account(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    456                                     # account_id
)
```

* [`get_ip_whitelist_addresses`](https://developers.shrimpy.io/docs/#get-ip-whitelist-addresses)

```python
ip_addresses = client.get_ip_whitelist_addresses(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8' # user_id
)
```

### Trading Methods

* [`create_trade`](https://developers.shrimpy.io/docs/#creating-a-trade)

```python
create_trade_response = client.create_trade(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # account_id
    'BTC',                                  # from_symbol
    'ETH',                                  # to_symbol
    '0.01'                                  # amount of from_symbol
)
trade_id = create_trade_response['id']
```

* [`get_trade_status`](https://developers.shrimpy.io/docs/#get-trade-status)

```python
trade = client.get_trade_status(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # exchange_account_id
    '72dff099-54c0-4a32-b046-5c19d4f55758'  # trade_id
)
```

* [`list_active_trades`](https://developers.shrimpy.io/docs/#list-active-trades)

```python
active_trades = client.list_active_trades(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # exchange_account_id
)
```

### Balance Methods

* [`get_balance`](https://developers.shrimpy.io/docs/#get-balance)

```python
balance = client.get_balance(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # account_id
)
```

* [`get_total_balance_history`](https://developers.shrimpy.io/docs/#get-total-balance-history)

```python
total_balance_history = client.get_total_balance_history(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # account_id
)
```

### Asset Management Methods

* [`rebalance`](https://developers.shrimpy.io/docs/#rebalancing)

```python
client.rebalance(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # account_id
)
```

* [`get_rebalance_period`](https://developers.shrimpy.io/docs/#get-the-rebalance-period)

```python
rebalance_period_hours = client.get_rebalance_period(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # account_id
)
```

* [`set_rebalance_period`](https://developers.shrimpy.io/docs/#set-the-rebalance-period)

```python
client.set_rebalance_period(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # account_id
    24                                      # rebalance_period in hours
)
```

* [`get_strategy`](https://developers.shrimpy.io/docs/#get-the-strategy)

```python
strategy = client.get_strategy(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # account_id
)
```

* [`set_strategy`](https://developers.shrimpy.io/docs/#set-the-strategy)

```python
client.set_strategy(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',   # user_id
    123,                                      # account_id
    {
        'isDynamic': False,
        'allocations': [
            { 'symbol': 'BTC', 'percent': '50' },
            { 'symbol': 'ETH', 'percent': '50' }
        ]
    }                                         # strategy
)
```

* [`clear_strategy`](https://developers.shrimpy.io/docs/#clear-the-strategy)

```python
client.clear_strategy(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',   # user_id
    123                                       # account_id
)
```

* [`allocate`](https://developers.shrimpy.io/docs/#allocating)

```python
client.allocate(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8',    # user_id
    123,                                       # account_id
    {
        'isDynamic': False,
        'allocations': [
            { 'symbol': 'USDT', 'percent': '100' }
        ]
    }                                          # strategy
)
```

### Limit Order Methods

* [`place_limit_order`](https://developers.shrimpy.io/docs/#place-a-limit-order)

```python
place_limit_order_response = client.place_limit_order(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # account_id
    'BTC',                                  # base_symbol
    'ETH',                                  # quote_symbol
    '0.01',                                 # quantity of base_symbol
    '0.026',                                # price
    'SELL',                                 # side
    'IOC',                                  # time_in_force
)
limit_order_id = place_limit_order_response['id']
```

* [`get_limit_order_status`](https://developers.shrimpy.io/docs/#get-limit-order-status)

```python
order = client.get_limit_order_status(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # account_id
    '8c2a9401-eb5b-48eb-9ae2-e9e02c174058'  # order_id
)
```

* [`list_open_orders`](https://developers.shrimpy.io/docs/#list-open-orders)

```python
orders = client.list_open_orders(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123                                     # account_id
)
```

* [`cancel_limit_order`](https://developers.shrimpy.io/docs/#cancel-a-limit-order)

```python
order = client.cancel_limit_order(
    '701e0d16-1e9e-42c9-b6a1-4cada1f395b8', # user_id
    123,                                    # account_id
    '8c2a9401-eb5b-48eb-9ae2-e9e02c174058'  # order_id
)
```

### Analytics Methods

* [`get_backtest_assets`](https://developers.shrimpy.io/docs/#get-backtest-assets)

```python
backtest_assets = client.get_backtest_assets(
    'kucoin' # exchange
)
```

* [`run_backtest`](https://developers.shrimpy.io/docs/#run-backtest)

```python
backtest_results = client.run_backtest(
    'binance',                                       # exchange
    10,                                              # rebalance_period in hours
    '0.1',                                           # fee in percent
    '2018-05-19T00:00:00.000Z',                      # start_time
    '2018-11-02T00:00:00.000Z',                      # end_time
    '5000',                                          # initial_value in USD
    [
        { 'symbol': "BTC", 'percent': '50' },
        { 'symbol': "ETH", 'percent': '50' }
    ]                                                # allocations
)
```

### Insight Methods

* [`get_asset_dominance`](https://developers.shrimpy.io/docs/#get-asset-dominance)

```python
asset_dominance = client.get_asset_dominance()
```

* [`get_asset_popularity`](https://developers.shrimpy.io/docs/#get-asset-popularity)

```python
asset_popularity = client.get_asset_popularity()
```

### Historical Methods

* [`get_historical_count`](https://developers.shrimpy.io/docs/#get-historical-count)

```python
count = client.get_historical_count(
    'trade',
    'Bittrex',
    'LTC',
    'BTC',
    '2019-05-19T01:00:00.000Z',
    '2019-05-20T02:00:00.000Z'
)
```

* [`get_historical_instruments`](https://developers.shrimpy.io/docs/#get-historical-instruments)

```python
instruments = client.get_historical_instruments()
bittrex_instruments = client.get_historical_instruments('Bittrex')
```

* [`get_historical_trades`](https://developers.shrimpy.io/docs/#get-historical-trades)

```python
trades = client.get_historical_trades(
    'Bittrex',
    'LTC',
    'BTC',
    '2019-05-19T00:00:00.000Z',
    '2019-05-20T00:00:00.000Z',
    100
)
```

* [`get_historical_orderbooks`](https://developers.shrimpy.io/docs/#get-historical-orderbooks)

```python
orderbooks = client.get_historical_orderbooks(
    'Bittrex',
    'LTC',
    'BTC',
    '2019-05-19T00:00:00.000Z',
    '2019-05-20T00:00:00.000Z',
    100
)
```

* [`get_historical_candles`](https://developers.shrimpy.io/docs/#get-historical-candles)

```python
candles = client.get_historical_candles(
    'Bittrex',
    'LTC',
    'BTC',
    '2019-05-19T00:00:00.000Z',
    '2019-05-20T00:00:00.000Z',
    100,
    '1m'
)
```

### Management Methods

* [`get_status`](https://developers.shrimpy.io/docs/#get-status)

```python
status = client.get_status()
```

* [`get_credits`](https://developers.shrimpy.io/docs/#get-credits)

```python
usage = client.get_credits()
```

* [`get_usage`](https://developers.shrimpy.io/docs/#get-usage)

```python
usage = client.get_usage()
```

## Websocket

Users can access the Shrimpy websocket feed using the [`ShrimpyWsClient`](https://github.com/shrimpy-dev/shrimpy-python/blob/master/shrimpy/shrimpy_ws_client.py) class. A handler must be
passed in on subscription that is responsible for processing incoming messages from the websocket
stream. It is recommended that you simply send the message to another processing thread from your custom
handler to prevent blocking the incoming message stream.

The client handles pings to the Shrimpy server based on the [`API Documentation`](https://developers.shrimpy.io/docs/#websocket)

```python
import shrimpy


public_key = '6d73c2464a71b94a81aa7b13d...'
private_key = 'e6238b0de3cdf19c7861f8e8f5d137ce7113ac1e884b191a14bbb2...'

# This is a sample handler, it simply prints the incoming message to the console
def error_handler(err):
    print(err)


# This is a sample handler, it simply prints the incoming message to the console
def handler(msg):
    print(msg)


api_client = shrimpy.ShrimpyApiClient(public_key, private_key)
raw_token = api_client.get_token()
client = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])

subscribe_data = {
    "type": "subscribe",
    "exchange": "coinbasepro",
    "pair": "ltc-btc",
    "channel": "orderbook"
}

# Start processing the Shrimpy websocket stream!
client.connect()
client.subscribe(subscribe_data, handler)

# Once complete, stop the client
client.disconnect()
```
