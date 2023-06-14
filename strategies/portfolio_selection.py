from strategies.utils import get_sharpe

class PortfolioSelection:

    def __init__(self) -> None:
        pass

    def select_single_position(self, predicted_returns: dict, predicted_stds: dict, n_stocks:int=50):
        predicted_stds = {key: value if (value and value > 0) else 1 for (key, value) in predicted_stds.items()}
        predicted_stds = {key: value for (key, value) in predicted_stds.items() if key in predicted_returns.keys()}
        sharpe_ratios = [[key, value] for (key, value) in 
                         zip(predicted_returns.keys(), get_sharpe(predicted_returns.values(), predicted_stds.values()))]
        sharpe_ratios = sorted(sharpe_ratios, reverse=True, key=lambda x: x[1])
        top = sharpe_ratios[:n_stocks]
        positive_top = [i for i in top if i[1] > 0]
        total_weights = sum([i[1] for i in positive_top])
        portfolio = {i[0]: i[1]/total_weights for i in positive_top}
        return portfolio

    def execute(self, returns, stds, n_stocks):
        pass
        
    
