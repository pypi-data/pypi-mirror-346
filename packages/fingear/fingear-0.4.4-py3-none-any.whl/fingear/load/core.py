# prices
from .yahoo import load_candles as load_candles_yahoo
from .tinkoff import load_candles as load_candles_tinkoff

# dividends
from .tinkoff import load_dividend as load_dividend_tinkoff

# bonds
from .tinkoff import load_bond_coupons as load_bond_coupons_tinkoff
from .tinkoff import load_bond_info as load_bond_info_tinkoff

# exchange rates
from .cbrf import load_exchange_rate as load_exchange_rate_cbrf
from .yahoo import load_exchange_rate as load_exchange_rate_yahoo

import pandas as pd
    

def load_candles(ticker, start, end, interval, core='tinkoff'):
    if core == 'tinkoff':
        return load_candles_tinkoff(ticker, start, end, interval)
    elif core == 'yahoo':
        return load_candles_yahoo(ticker, start, end, interval)
    
def load_asset_price(ticker, start, end, interval, core='tinkoff'):
    candles = load_candles(ticker, start, end, interval, core=core)
    candles = candles[['datetime', 'close']]
    candles.columns = ['dttm', 'price']
    candles.sort_values('dttm', inplace=True)
    return candles

def load_single_price(ticker, date, core='tinkoff'):
    start = pd.to_datetime(date)-pd.DateOffset(days=30) # Тут если не торговались, то грузим раньше
    end = pd.to_datetime(date)+pd.DateOffset(days=1)
    candles = load_candles(ticker, start, end, 'day', core=core)
    price = candles.tail(1)['close'].values[0]
    return price



### DIVIDENDS

def load_dividend(ticker, start, end, core='tinkoff'):
    if core == 'tinkoff':
        return load_dividend_tinkoff(ticker, start, end)
    else:
        raise NotImplementedError
    


### BOND

def load_bond_info(ticker, core='tinkoff'):
    if core == 'tinkoff':
        return load_bond_info_tinkoff(ticker)
    else:
        raise NotImplementedError
    

def load_bond_coupons(ticker, start, end, core='tinkoff'):
    if core == 'tinkoff':
        return load_bond_coupons_tinkoff(ticker, start, end)
    else:
        raise NotImplementedError
    

### RATES

def load_exchange_rate(currency, start, end, interval, core='tinkoff'):
    if core == 'cbrf':
        return load_exchange_rate_cbrf(currency, start, end, interval)
    elif core == 'yahoo':
        return load_exchange_rate_yahoo(currency, start, end, interval)
    elif core == 'tinkoff':
        return NotImplementedError
    else:
        raise NotImplementedError