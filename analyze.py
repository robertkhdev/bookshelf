
from typing import List
import matplotlib.pyplot as plt


def ensure_int(num):
    if isinstance(num, str):
        num = int(num.replace(',', ''))
    return num


def convert_price_string(price_str: str) -> float:
    price_str = price_str.replace('$', '')
    try:
        price = float(price_str)
        return price
    except:
        return None


def plot_price_histogram(raw_data: List[str]):
    data = [convert_price_string(x) for x in raw_data if convert_price_string(x) is not None]
    plt.hist(data)
    plt.show(block=False)


def plot_ratings_reviews(raw_data: List[List]):

    def clean_row(row):
        try:
            row[1] = ensure_int(row[1])
            row[0] = float(row[0])
            return row
        except ValueError:
            return None

    data = [clean_row(d) for d in raw_data if clean_row(d) is not None]
    data = list(zip(*data))
    plt.scatter(data[0], data[1])
    plt.show(block=False)