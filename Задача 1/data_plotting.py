import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None):
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
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")

def calculate_and_display_average_price(data):
    '''
    Вычисляет и выводит среднюю цену закрытия акций за заданный период.
    '''
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            closing_prices = data.Close.values
            average_price = closing_prices.mean()
            print(f"Средняя цена закрытия акций за период: {average_price}")
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")


def notify_if_strong_fluctuations(data, threshold=2.0):
    '''
    Отправляет уведомление, если разница между максимальным и минимальным значениями цены закрытия превышает порог.
    '''
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            closing_prices = data.Close.values
            max_price = closing_prices.max()
            min_price = closing_prices.min()
            if max_price - min_price > threshold:
                print(f"Внимание! Разница между максимальным и минимальным значениями цены закрытия превышает порог {threshold}.")
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")


def export_data_to_csv(data, filename='stock_data.csv'):
    '''
    Экспортирует данные в CSV-файл.
    '''
    data.to_csv(filename, index=False)
    print(f"Данные экспортированы в файл {filename}")