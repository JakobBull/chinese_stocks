"""
Example strategy that just creates evenly weighted baskets of all available stocks at any time.

"""

import pandas
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

class StrategyLassoFactors:

    def __init__(self, args=None) -> None:
        self.args = args

    def train(self, stocks, source_data, train_dates):
        models = {}
        for stock in tqdm(stocks):
            stock_data = source_data[(source_data['date'] in train_dates) & (source_data['order_book_id'] == stock)]
            if not stock_data:
                print(f"Stock {stock} does not have sufficient training data.")
            labels = stock_data['exret']
            stock_data = stock_data.drop('exret')
            lasso = Lasso(alpha=1.0)  # You can adjust the regularization parameter 'alpha' as needed
            lasso.fit(stock_data, labels)
            models[stock] = lasso
        return models



    def execute(self, source_data, train_dates, test_dates):
        positions = {}

        #get a set of all stocks
        stocks = set(source_data['order_book_id'])

        source_data = source_data[source_data['date'].isin(test_dates)]

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        for date in test_dates:
            available_stocks = source_data.loc[source_data['date'] == date, 'order_book_id'].tolist()
            positions[date] = {stock: 1/len(available_stocks) for stock in available_stocks}
        return positions
