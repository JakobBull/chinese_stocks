
"""
Example strategy that just creates evenly weighted baskets of all available stocks at any time.

"""

import pandas as pd
from tqdm import tqdm

class StrategyNFixedBaskets:

    def __init__(self, args=None) -> None:
        self.args = args

    def execute(self, source_data, train_dates, test_dates):
        positions = {}
        source_data = source_data[source_data['date'].isin(test_dates)]
        for date in tqdm(test_dates):
            available_stocks = source_data.loc[source_data['date'] == date, 'order_book_id'].tolist()
            positions[date] = {stock: 1/len(available_stocks) for stock in available_stocks}
        return positions

if __name__ == "__main__":
    X = pd.read_csv("test_data.csv")
    X=X.dropna()
    X.date = pd.to_datetime(X.date)

    train_dates = list(X.date[:int(0.8*len(X))])
    test_dates = list(X.date[int(0.8*len(X)-12):])
    s = StrategyNFixedBaskets()
    print(s.execute(X, train_dates, test_dates))