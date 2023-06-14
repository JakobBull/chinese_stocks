import pandas as pd
from portfolio import Portfolio
from strategies.nfixedbaskets import StrategyNFixedBaskets
from strategies.lasso_factors import StrategyLassoFactors

import warnings

warnings.filterwarnings('ignore')

X = pd.read_csv("data_reduced.csv")
X=X.dropna()
X.date = pd.to_datetime(X.date)
X

portfolio_2 = Portfolio()
portfolio_2.run(StrategyLassoFactors, X, args=[0.1])