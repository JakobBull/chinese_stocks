import numpy as np
import pandas as pd

"""
Portfolio to generate portfolio objects.

Usage:
Instantiate object and then use the run() method, which takes as arguments a strategy object and the data. Optional args also supported
Refer to example for usage. Models are evaluated automatically (successful evaluation confirmed with output 'Activated.')
You can use the self attribute to access a dataframe that includes the portfolio at a given time and the stats attribute for a quick performance overview.

"""
class Portfolio:

    def  __init__(self):
        self.dates = []
        self.positions = {}
        self.valid_stocks = {}
        self.stats = {}
        self.data = pd.DataFrame(columns=['date','positions', 'n_positions', 'return'])
        self.component_returns = {}

    def set_valid_stocks(self, valid_stocks):
        self.valid_stocks = valid_stocks

    def change_position(self, date, position, error=10e-6):
        if date not in self.dates:
            self.dates.append(date)
        if abs(sum(position.values()) - 1) < error:
            if all(key in self.valid_stocks[date] for key in position.keys()):
                self.positions[date] = position
            else:
                for key in position.keys():
                    if key not in self.valid_stocks[date]:
                        if position[key] > 0:
                            print(f'Stock {key} not defined at date {date}.')
        else:
            print("The total position weighting is:",  sum(position.values()))
            print("The position weighting does not add to 1.")

    def well_defined(self):
        nones = not all(self.positions.values())

        if nones:
            for key, value in self.positions.items():
                if not value:
                    print(f"Please define a portfolio position for {key}")
        else:
            print("Portfolio well defined.")
            self.is_well_defined = True

    def activate(self):
        if not self.is_well_defined:
            print("Please make sure the portfolio is well defined first by calling Portfolio.well_defined().")
        else:
        
            #based on the positions at any given date, reweigh portfolio and calculate the portfolio return, write new row with return and key info to data DataFrame
            for date in self.dates[1:]:
                month_positions = self.positions[date]
                month_returns = {position: float(self.source_data.groupby(['order_book_id', 'date'])['exret'].get_group((position, date))) for position in month_positions.keys()}
                month_position_returns = {key: (month_positions[key] * month_returns[key]) for key in month_positions.keys()}
                total_return = np.array(list(month_position_returns.values())).sum()
                row_data = [date, self.positions[date], len(self.positions[date]), total_return]
                self.data = self.data.append(pd.Series(row_data, index=self.data.columns), ignore_index=True)
                self.component_returns[date] = month_position_returns

            #Calculate various portfolio statistics such as standard deviations and Sharpe ratio
            self.data['std'] = self.data['return'].rolling(12).std()
            self.data['Sharpe'] = self.data['return'].div(self.data['std'])
            self.data = self.data.iloc[12:, :]
            self.stats["Portfolio Rate of Return"] = (np.prod(self.data['return']+1) - 1)/(len(self.data['return'])/12)
            self.stats["Portfolio std"] = self.data['return'].std()*np.sqrt((len(self.data['return'])/12))
            self.stats["Portfolio Sharpe"] = self.stats["Portfolio Rate of Return"]/self.stats["Portfolio std"]
            print("Activated.")

    def implement_strategy(self, positions):
        for date, position in positions.items():
            self.change_position(date, position)

    def train_test_split(self, train_test_split=0.7):
        dates = sorted(list(set(self.source_data.date)))
        self.train_dates = dates[:int(len(dates)*train_test_split)]
        #Note the overlap,this is only used to calculate std rolling average
        self.test_dates = dates[int(len(dates)*train_test_split)-12:]

    def run(self, strategy_method, source_data, args=None):
        self.source_data = source_data
        self.set_valid_stocks({date: list(self.source_data.groupby("date")["order_book_id"].get_group(date)) for date in set(self.source_data.date)})
        self.train_test_split()
        self.strategy = strategy_method(args)
        self.portfolio = self.strategy.execute(source_data, self.train_dates, self.test_dates)
        self.implement_strategy(self.portfolio)
        self.well_defined()
        self.activate()
        self.stats['Mean Portfolio Size'] = np.mean([len(value) for value in self.portfolio.values()])
