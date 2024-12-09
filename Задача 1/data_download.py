import yfinance as yf


def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    data = yf.download(ticker, period=period, start=start_date, end=end_date)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

