import yfinance as yf
import pprint
import sys
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
        current_short = line[4]
        tickers[symbol] = current_short

    return tickers


def ticker_scraper(tickers: Mapping[str, float], top: int | None = None) -> List[Tuple[str, int]]:
    """
    Given a list of tickers, returns its current short interest percentage.
    It does this by going to yfinance to extract the current floats

    :param tickers: a mapping of tickers to their respective floats shorted
    :param top: Top is by default None. Change this to any int to get the top "top" tickers that has a high short
                interest percentage
    :return: returns a list of tickers in descending order (i.e., highest to lowest short interest)
    """
    rankings = []

    return rankings


def main():
    filename = "example.csv"
    tickers = parser(filename)
    ranking = ticker_scraper(tickers, 50)

    print("I am in main")


if __name__ == "__main__":
    main()
