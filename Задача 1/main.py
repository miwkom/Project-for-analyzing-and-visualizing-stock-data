import data_download as dd
import data_plotting as dplt
from datetime import datetime


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца); если требуются конкретные даты, оставьте это поле пустым: ")

    if period == '':
        start_date = input("Введите дату начала в формате YYYY-MM-DD (например, '2022-01-01'): ")
        end_date = input("Введите дату окончания в формате YYYY-MM-DD (например, '2022-12-31'): ")
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        period = None
    else:
        start_date = None
        end_date = None

    style = change_of_style()
    rsi_confirmation = input("Нужно рассчитать индикатор RSI? (Y/N): ")
    macd_confirmation = input("Нужно рассчитать индикатор MACD? (Y/N): ")
    threshold = float(input("Введите порог для оповещения о сильных изменениях цены (например, 2.0): "))
    filename_csv = input(f"Введите имя файла для экспорта данных в CSV (например, '{ticker}_data'): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, style, ticker, period, start_date, end_date)

    if rsi_confirmation.lower() == 'y':
        dplt.create_and_save_rsi_plot(stock_data, style, ticker, period, start_date, end_date)
    else:
        print("Индикатор RSI не будет рассчитан.")

    if macd_confirmation.lower() == 'y':
        dplt.create_and_save_macd_plot(stock_data, style, ticker, period, start_date, end_date)
    else:
        print("Индикатор MACD не будет рассчитан.")

    dplt.calculate_and_display_std_dev(stock_data)

    dplt.calculate_and_display_average_price(stock_data)

    dplt.notify_if_strong_fluctuations(stock_data, threshold)

    dplt.export_data_to_csv(stock_data, filename_csv)


def change_of_style():
    """
    Изменение стиля графиков в matplotlib
    """
    style_list = ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic',
     'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright',
     'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid',
     'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel',
     'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid',
     'tableau-colorblind10']

    while True:
        style = input(
            'Введите название стиля (для вызова полного списка введите "all"). '
            'Оставьте поле пустым для использования стандартного стиля: ')

        if style in style_list:
            print(f'Изменение стиля на {style}')
            return style
        elif style == '':
            print('Используется стиль по умолчанию.')
            return 'classic'
        elif style.lower() == 'all':
            print('Список доступных стилей:')
            for style_name in style_list:
                print(style_name)
        else:
            print('Неизвестный стиль. Пожалуйста, попробуйте еще раз.')


if __name__ == "__main__":
    main()
