import yfinance as yf
import pprint
import sys
import time
import csv
from typing import List, Mapping, Tuple


def parser(file_dir: str) -> Mapping[str, int]:
    """
    Takes in a directory to a csv file containing the Finra Equity Short Interest Data Format
    See: https://www.finra.org/finra-data/browse-catalog/equity-short-interest/data
    :param file_dir: the directory to the file
    :return: a mapping of stocks to ticker
    """
    file = open(file_dir)
    reader = csv.DictReader(file).reader
    tickers = {}
    for index, line in enumerate(reader):
        if index == 0:
            continue
        symbol = line[2]
        current_short = int(line[4])
        tickers[symbol] = current_short

    return tickers


def ticker_scraper(tickers: Mapping[str, int], top: int | None = None) -> List[Tuple[str, float, int, int]]:
    """
    Given a list of tickers, returns its current short interest percentage.
    It does this by going to yfinance to extract the current floats

    :param tickers: a mapping of tickers to their respective floats shorted
    :param top: Top is by default None. Change this to any int to get the top "top" tickers that has a high short
                interest percentage
    :return: returns a list of tickers in descending order (i.e., highest to lowest short interest)
    """
    rankings = []
    limit = 1.805
    for index, ticker in enumerate(tickers):
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            float_shares = stock_info["floatShares"]
            percent_short_interest = tickers[ticker] / int(float_shares)
            rankings.append((ticker, percent_short_interest, float_shares, tickers[ticker]))
            time.sleep(limit)
        except Exception as e:
            print(e)

    rankings.sort(key=lambda x: x[1], reverse=True)
    if top is not None:
        rankings = rankings[:top]

    return rankings


def main():
    filename = "example.csv"
    tickers = parser(filename)
    rankings = ticker_scraper(tickers, 50)

    padding = 18
    print("Stock".ljust(padding) +
          "Float".ljust(padding) +
          "Short Percentage".ljust(padding) +
          "Floats Shorted".ljust(padding))

    print("-" * padding * 4)
    for rank in rankings:
        stock, percentage, floats, floats_shorted = rank
        print(stock.ljust(17) +
              str(floats).ljust(17) +
              (str(round(percentage * 100, 2)) + " %").ljust(17) +
              str(floats_shorted).ljust(17))


if __name__ == "__main__":
    main()
