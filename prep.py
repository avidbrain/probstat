from pathlib import Path
import pickle
import pandas as pd

datadir = 'finam'
file_mask = '*_15*_*.csv'
save_file = 'moex.pkl'

datafiles = Path(datadir).glob(file_mask)


def from_csv(csv_file):
    raw_df = pd.read_csv(csv_file, header=None)
    target_df = pd.DataFrame({
        'Date': pd.to_datetime(raw_df.iloc[:, 2], format='%Y%m%d').dt.date,
        'Ticker': raw_df.iloc[:, 0],
        'Close': raw_df.iloc[:, 7],
    }).set_index('Date')
    target_df['MA200'] = target_df.rolling(window=200)['Close'].mean()
    target_df['MA10'] = target_df.rolling(window=10)['Close'].mean()
    return target_df


moex_df = pd.concat(from_csv(fl) for fl in datafiles if fl.is_file())

with open(save_file, 'wb') as file:
    pickle.dump(moex_df, file)
