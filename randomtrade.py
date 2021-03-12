import pickle
import pandas as pd
from common import *

moex_file = 'moex.pkl'
save_file = 'random.pkl'


def get_trade(df, setup):
    trade_history = []
    inposition = False
    nsec = 0  # number of securities at hand

    for date, row in df.iterrows():
        ticker, price, *_ = row
        rday = date.weekday()
        if rday == setup['random_day']:
            if inposition:  # SELL
                trade_history.append((date, rday, ticker, -nsec, price))
                inposition = False
                nsec = 0
            else:  # BUY
                nsec = int(setup['tradecash'] / price)
                inposition = True
                trade_history.append((date, rday, ticker, nsec, price))

    even_len = len(trade_history) // 2 * 2
    return pd.DataFrame(
        trade_history[:even_len],
        columns=('Date', 'RDay', 'Ticker', 'NSec', 'Price'))


with open(moex_file, 'rb') as file:
    moex_df = pickle.load(file)


random_frames = []
for random_day in trade_setup['random_days']:
    setup = trade_setup.copy()
    setup['random_day'] = random_day
    for ticker in moex_df['Ticker'].unique():
        ticker_df = get_ticker_df(ticker, moex_df, trade_start)
        random_frames.append(get_trade(ticker_df, setup))

random_df = pd.concat(random_frames)

with open(save_file, 'wb') as file:
    pickle.dump(random_df, file)
