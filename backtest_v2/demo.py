from backtest import backtest
import numpy as np
from scipy.optimize import minimize


'''
strat_function(preds, prices) - user specified mapping from past n days of price and analyst data to weights.
Returns: An array of asset weightings. The maximum weighting is 1, and the minimum is -1. The weights must sum to between -1 and 1. 

Refer to test datasets for the shape of input data. Both preds and prices will be 2 dimensional arrays, with number of columns equal to number of assets + 1.
Number of days equal to number of rows. The first column will be date data.

Your strategy function needs to work with this data to geenrate portfolio weights.


'''
def strat_function(preds, prices, last_weights): 
        # Pass in multiple preds
    # IMPLEMENTATION OF MARKOWITZ MODEL
    class Markowitz:
        def __init__(self):
            # data_seen[0] = actual prices seen
            # data_seen[i] = predictions seen from analyst i for i in [1..3]
            self.data_seen = [np.ones((0,9)) for _ in range(2)]
            self.dOM = 20 # The trading day of the current month, 0 <= dOM < 21
            self.log_returns = np.ones((0,9))
        
        def eval(self, asset_prices, asset_price_predictions_1):
            # input  : series prices and predictions for a day
            # output : weight vector for asset allocation
            for ind, data in enumerate([asset_prices, asset_price_predictions_1]): self.data_seen[ind] =  data
            self.dOM = (self.dOM + 1) % 21
            if self.data_seen[0].shape[0] <= 1: return np.ones((9,))/9
            self.log_returns = np.log(self.data_seen[0][:-1]/self.data_seen[0][1:])
            return self.calc_weights()
        
        def calc_weights(self):
            # output : (9,) array of l1 normalized weights
            er = self.calc_er()
            cov = self.calc_cov()
            f = lambda w : (er @ w) / np.sqrt(w.T @ cov @ w)
            cons = ({'type':'eq', 'fun': lambda w : np.sum(w)-1}, {'type':'ineq', 'fun': lambda w : 1-np.max(np.abs(w))})
            res = minimize(f, np.array([1, 1, 1, 1, 1, 1, 1, 1, 1]), constraints=cons)
            weights = res.x.T
            print(weights)
            if any([abs(w) > 1 for w in weights]): return np.ones(9)/9
            return weights / np.sum(weights)

        def calc_er(self):
            # output : (1,9) expected log return array
            pred = np.mean([self.data_seen[i][-1] for i in range(1,2)], axis=0)
            hist = self.data_seen[0][-1]
            # calculates end of month price as a weighted average of current price
            # and average predicted end of month price (weights change over month)
            pred_eom = (self.dOM / 21)*hist + (1-self.dOM/21)*pred
            returns = pred_eom / hist
            return np.log(returns.astype('float64') ** -(21-self.dOM)) # normalize returns to daily

        def calc_cov(self):
            # output : (9,9) covariance matrix of log asset returns
            return np.cov(self.log_returns.T)

    model = Markowitz()
    return model.eval(prices, preds)

'''
Running the backtest - starting portfolio value of 10000, reading in data from these two locations.
'''
backtest(strat_function, 10000, '../test_datasets/Actual.csv', '../test_datasets/averaged.csv')

