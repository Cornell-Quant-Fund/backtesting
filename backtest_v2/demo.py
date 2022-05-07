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

    prices = np.array(prices)
    signal = prices[:, -1][-1]
    if signal == -1:
        return [0, 1, 0]
    if signal == 1:
        return [0, 0, 0]
    if signal == 0:
        return last_weights

    

'''
Running the backtest - starting portfolio value of 10000, reading in data from these two locations.
'''
backtest(strat_function, 10000, '../test_datasets/SEDG-ENPH-Signal.csv', '../test_datasets/SEDG-ENPH-Signal.csv', True, "log.csv")

