import pickle
import numpy as np
import pandas as pd
from common import *

moex_file = 'moex.pkl'
save_file = 'trade.pkl'


def get_trade(df, setup):
    f_inposition, f_needtrade, f_pricedrop = 4, 2, 1
    status = 0
    trade_history = []
    nsec = 0  # number of securities at hand
    stoploss, limit_price = 0.0, np.inf

    for date, row in df.iterrows():
        ticker, price, *_ = row
        if status & f_inposition:
            if status & f_needtrade or price < stoploss:  # SELL!
                trade_history.append((date, ticker, -nsec, price))
                status, nsec, stoploss, limit_price = 0, 0, 0.0, np.inf
            elif price > limit_price:  # sell on the next cycle
                status ^= f_needtrade
        elif status & f_needtrade:  # BUY !
            nsec = int(setup['tradecash'] / price)
            trade_history.append((date, ticker, nsec, price))
            status = f_inposition
            limit_price = price * (1 + setup['profitability'])
            stoploss = price * (1 + setup['allowed_loss'])
        elif price < row['MA200']:
            status = 0
        elif status & f_pricedrop:  # watch for the bounce
            if price > row['MA10']:  # buy on the next cycle
                status = f_needtrade
        else:  # watch for the price drop below MA10
            if price < row['MA10']:
                status = f_pricedrop

    even_len = len(trade_history) // 2 * 2
    return pd.DataFrame(
        trade_history[:even_len],
        columns=('Date', 'Ticker', 'NSec', 'Price'))


with open(moex_file, 'rb') as file:
    moex_df = pickle.load(file)

trade_df = pd.concat(map(
    lambda ticker: get_trade(
        get_ticker_df(ticker, moex_df, trade_start),
        trade_setup),
    moex_df['Ticker'].unique()
))

with open(save_file, 'wb') as file:
    pickle.dump(trade_df, file)
