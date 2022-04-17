from backtest import backtest
import numpy as np
from scipy.optimize import minimize

'''
strat_function(preds, prices) - user specified mapping from past n days of price and analyst data to weights.
Returns: An L1 normalized array of asset weightings.
'''



# Pass in multiple preds

# IMPLEMENTATION OF MARKOWITZ MODEL
class Markowitz:
    def __init__(self):
        # data_seen[0] = actual prices seen
        # data_seen[i] = predictions seen from analyst i for i in [1..3]
        self.data_seen = [np.ones((0,9)) for _ in range(4)]
        self.dOM = 20 # The trading day of the current month, 0 <= dOM < 21
        self.log_returns = np.ones((0,9))
    
    def eval(self, asset_prices, asset_price_predictions_1, 
        asset_price_predictions_2, asset_price_predictions_3):
        # input  : series prices and predictions for a day
        # output : weight vector for asset allocation
        for ind, data in enumerate([asset_prices, asset_price_predictions_1, asset_price_predictions_2, asset_price_predictions_3]): self.data_seen[ind] = np.vstack([self.data_seen[ind], data])
        self.dOM = (self.dOM + 1) % 21
        if self.data_seen[0].shape[0] <= 1: return np.ones((9,))/9
        self.log_returns = np.log(self.data_seen[-1]/self.data_seen[-2])
        return self.calc_weights()
    
    def calc_weights(self):
        # output : (9,) array of l1 normalized weights
        er = self.calc_er()
        cov = self.calc_cov()
        f = lambda w : (er @ w) / np.sqrt(w.T @ cov @ w)
        cons = ({'type':'eq', 'fun': lambda w : np.sum(w)-1}, {'type':'ineq', 'fun': lambda w : 1-np.max(np.abs(w))})
        res = minimize(f, np.array([1, 0, 0, 0, 0, 0, 0, 0, 0]), constraints=cons)
        weights = res.x.T
        if any([abs(w) > 1 for w in weights]): return np.ones(9)/9
        return weights / np.sum(weights)

    def calc_er(self):
        # output : (1,9) expected log return array
        pred = np.mean([self.data_seen[i][-1] for i in range(1,4)], axis=0)
        hist = self.data_seen[0][-1]
        # calculates end of month price as a weighted average of current price
        # and average predicted end of month price (weights change over month)
        pred_eom = (self.dOM / 21)*hist + (1-self.dOM/21)*pred
        returns = pred_eom / hist
        return np.log(returns ** -(21-self.dOM)) # normalize returns to daily

    def calc_cov(self):
        # output : (9,9) covariance matrix of log asset returns
        return np.cov(self.log_returns.T)

model = Markowitz()
def strat_function(preds, prices): return model.eval(prices[-1], preds[-1], preds[-1], preds[-1])

'''
Running the backtest - starting portfolio value of 10000, reading in data from these two locations.
'''
backtest(strat_function, 10000, '../test_datasets/Actual.csv', '../test_datasets/Predicted Testing Data Analyst 1.csv')

