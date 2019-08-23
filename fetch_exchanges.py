from time import time
from datetime import datetime
import ccxt

cryptocurrencies = ccxt.kraken()
cryptocurrencies.load_markets(True)

seconds_back = 3 * 60


def update_data_points(data_points, symbol):
    fetched = cryptocurrencies.fetch_ticker(symbol)
    millis = fetched['timestamp']
    exchange = (fetched['bid'] + fetched['ask']) / 2

    data_points.append((millis, exchange))

    timestamp = int(round((time() - seconds_back) * 1000))
    while len(data_points) >= 1 and data_points[0][0] < timestamp:
        data_points.pop(0)

    return data_points
