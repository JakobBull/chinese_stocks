
"""
Example strategy that just creates evenly weighted baskets of all available stocks at any time.

"""
class StrategyNFixedBaskets:

    def __init__(self, args=None) -> None:
        self.args = args

    def execute(self, source_data, train_dates, test_dates):
        positions = {}
        source_data = source_data[source_data['date'].isin(test_dates)]
        for date in test_dates:
            available_stocks = source_data.loc[source_data['date'] == date, 'order_book_id'].tolist()
            positions[date] = {stock: 1/len(available_stocks) for stock in available_stocks}
        return positions
