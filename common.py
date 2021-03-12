import datetime

trade_start = datetime.date(2017, 3, 1)
trade_setup = {
    'profitability': 0.07,
    'allowed_loss': -0.003,
    'random_days': (0, 1, 2, 3, 4),
    'tradecash': 1000000
}


def get_ticker_df(ticker, source_df, start_date):
    return (
        source_df
            .query('Ticker==@ticker')
            .dropna()
            .loc[start_date:]
            .sort_values(by='Date')
    )

