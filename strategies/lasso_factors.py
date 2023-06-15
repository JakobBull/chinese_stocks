"""
Example strategy that just creates evenly weighted baskets of all available stocks at any time.

"""
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

from strategies.portfolio_selection import PortfolioSelection


class StrategyLassoFactors:

    def __init__(self, args=None) -> None:
        self.alpha = args[0]

    def train(self, stocks, source_data, train_dates):
        models = {}
        scalers = {}
        for stock in stocks:
            stock_data = source_data[(source_data['date'].isin(train_dates)) & (source_data['order_book_id'] == stock)]
            if len(stock_data) == 0:
                print(f"Stock {stock} does not have sufficient training data.")
                models[stock] = None
                scalers[stock] = None
            else:
                stock_data = stock_data.drop(['Unnamed: 0', 'order_book_id', 'date'], axis=1)
                scaler = StandardScaler()
                stock_data = scaler.fit_transform(stock_data)
                labels = stock_data[1:, -1]
                stock_data = stock_data[:-1, :-1]
                lasso = Lasso(alpha=self.alpha)  # You can adjust the regularization parameter 'alpha' as needed
                lasso.fit(stock_data, labels)
                models[stock] = lasso
                scalers[stock] = scaler
        return models, scalers

    def test(self, stocks, source_data, test_dates, models, scalers):
        predictions = {}
        labels = {}
        for stock in stocks:
            if models[stock] and scalers[stock]:
                stock_data = source_data[(source_data['date'].isin(test_dates)) & (source_data['order_book_id'] == stock)]
                if len(stock_data) == 0:
                    print(f"Stock {stock} does not have sufficient test data.")
                    predictions[stock] = None
                    labels[stock] = None
                else:
                    dates = stock_data['date'][1:]
                    stock_data = stock_data.drop(['Unnamed: 0', 'order_book_id', 'date'], axis=1)
                    stock_data = scalers[stock].transform(stock_data)
                    label = stock_data[1:, -1]
                    stock_data = stock_data[:-1, :-1]
                    prediction = models[stock].predict(stock_data)
                    #remap labels and predictions
                    total_labels = np.concatenate((stock_data, label[:, np.newaxis]), axis=1)
                    labels[stock] = {date: label for (date, label) in zip(dates, scalers[stock].inverse_transform(total_labels)[:, -1])}

                    total_predictions = np.concatenate((stock_data, prediction[:, np.newaxis]), axis=1)
                    predictions[stock] = {date: value for (date, value) in zip(dates, scalers[stock].inverse_transform(total_predictions)[:, -1])}
            else:
                predictions[stock] = None
                labels[stock] = None
        return predictions, labels

    def compose_portfolio(self, predictions,  stds):
        position = {}
        pf_selection = PortfolioSelection()
        return pf_selection.select_single_position(predictions, stds)
    
    def estimate_variance(self, source_data, train_dates):
        df = source_data[(source_data['date'].isin(train_dates))]
        return df.groupby("order_book_id").apply(lambda x: x["exret"].tail(12).std()).to_dict()

    def execute(self, source_data, train_dates, test_dates):
        models = {}
        scalers = {}
        positions = {}
        labels = {}
        portfolio = {}

        #get a set of all stocks
        stocks = set(source_data['order_book_id'])

        models, scalers = self.train(stocks, source_data, train_dates)
        stds = self.estimate_variance(source_data, train_dates)
        predictions, labels = self.test(stocks, source_data, test_dates, models, scalers)
        for date_time in test_dates:
            prediction_samples = {key: value[date_time] if (value and date_time in value.keys()) else None for (key, value) in predictions.items()}
            prediction_samples = {key: value for (key, value) in prediction_samples.items() if (value)}
            portfolio[date_time] = self.compose_portfolio(prediction_samples, stds)
        return portfolio

if __name__ == "__main__":
    X = pd.read_csv("data_reduced.csv")
    X=X.dropna()
    X.date = pd.to_datetime(X.date)

    train_dates = list(X.date[:int(0.8*len(X))])
    test_dates = list(X.date[int(0.8*len(X)-12):])
    s = StrategyLassoFactors([0.1])
    a = s.execute(X, train_dates, test_dates)
    print('hi')
