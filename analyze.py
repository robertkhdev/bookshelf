
from typing import List
import matplotlib.pyplot as plt


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
