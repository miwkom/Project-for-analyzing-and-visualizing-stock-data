import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, start_date, end_date, filename=None):
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        if period is None:
            filename = f"{ticker}_{start_date.date()}_{end_date.date()}_stock_price_chart.png"
        else:
            filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")


def create_and_save_rsi_plot(data, ticker, period, filename=None):
    """
    Строит график индекса Relative Strength Index (RSI) за 14 дней.
    """
    plt.figure(figsize=(10, 6))

    rsi = calculate_rsi(data)

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, rsi.values, label='RSI')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return

    plt.title("RSI")
    plt.xlabel("Дата")
    plt.ylabel("Индекс")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_RSI.png"

    plt.savefig(filename)
    print(f"Индикатор RSI за 14 дней сохранен как {filename}")


def create_and_save_macd_plot(data, ticker, period,filename=None):
    """
    Строит график индекса Moving Average Convergence Divergence (MACD).
    """
    plt.figure(figsize=(10, 6))

    macd, signal = calculate_macd(data)

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, macd.values, label='MACD')
            plt.plot(dates, signal.values, label='Signal')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return

    plt.title("MACD")
    plt.xlabel("Дата")
    plt.ylabel("Индекс")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_MACD.png"

    plt.savefig(filename)
    print(f"Индикатор MACD сохранен как {filename}")


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций за заданный период.
    """
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            closing_prices = data.Close.values
            average_price = closing_prices.mean()
            print(f"Средняя цена закрытия акций за период: {average_price}")
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")


def notify_if_strong_fluctuations(data, threshold=2.0):
    """
    Отправляет уведомление, если разница между максимальным и минимальным значениями цены закрытия превышает порог.
    """
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            closing_prices = data.Close.values
            max_price = closing_prices.max()
            min_price = closing_prices.min()
            if max_price - min_price > threshold:
                print(
                    f"Внимание! Разница между максимальным и минимальным значениями цены закрытия превышает порог {threshold}.")
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")


def export_data_to_csv(data, filename='stock_data'):
    """
    Экспортирует данные в CSV-файл.
    """
    data.to_csv(filename + '.cvs', index=False)
    print(f"Данные экспортированы в файл {filename}.csv")


def calculate_rsi(data, period=14):
    """
    Рассчитывает индекс относительной силы (RSI) за определенный период.
    """
    index = data['Close'].diff()
    up, down = index.copy(), index.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    roll_up = up.rolling(window=period).mean()
    roll_down = down.abs().rolling(window=period).mean()

    rsi = 100.0 - (100.0 / (1.0 + roll_up / roll_down))
    return rsi


def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Рассчитывает схождение и расхождение скользящих средних (MACD) для заданных быстрых и медленных периодов.
    """
    fast = data['Close'].ewm(span=fast_period, adjust=False, min_periods=fast_period).mean()
    slow = data['Close'].ewm(span=slow_period, adjust=False, min_periods=slow_period).mean()
    macd = fast - slow
    signal = macd.ewm(span=signal_period, adjust=False, min_periods=signal_period).mean()
    return macd, signal
