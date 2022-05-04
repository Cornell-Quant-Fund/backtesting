import numpy as np
from numpy import absolute, linalg
import pandas as pd
import scipy
import math
import matplotlib.pyplot as plt

class Account():
    '''
    __init__(self, starting_val) - Initializes the account object

    :argument: starting_val - The amount of initial liquid cash the account has on hand
    
    Returns:
    The Account object
    '''
    def __init__(self, starting_val): 
        self.absolute_values = []
        self.start_val = starting_val
        self.yesterday_prices = []
        self.weights = []

    '''
    update(self, weights, caps) - Updates the liquid (total) value of the portfolio given current data 

    :argument: weights - Np array that contains that fraction of the whole company that your portfolio owns stocks of (i.e. if 
    you portfolio owns 10% of company A, index 0, then weights[0] = 0.1)

    :argument: caps - Np array that contains the market capitalization of the companies that your portfolio owns stocks of. 
    Prices have a one-to-one relation with the weights array.

    Returns:
    Nothing, updates internal account value
    '''
    def update(self, weights, prices):
        if len(self.yesterday_prices) == 0:
            self.absolute_values.append(self.start_val)
        else:
            self.absolute_values.append(self.absolute_values[-1] * (1 + np.dot(weights,((prices - self.yesterday_prices) / self.yesterday_prices))))
        self.yesterday_prices = prices
        self.weights.append(weights)

    '''
    calc_deltas(self) - Calculates the percent change of account value day-to-day 

    Returns: 
    An 1D Np array of size n-1 from n days of trading where index i gives the percent change of account value from day i to i+1
    '''
    def calc_deltas(self):
        return np.array([(val - self.absolute_values[idx - 1]) / self.absolute_values[idx - 1] for idx, val in enumerate(self.absolute_values[1:], start=1)])

    '''
    daily_sharpe(self) - Calculates the sharpe ratio of portfolio trading history

    Returns:
    Returns the sharpe ratio as an integer
    '''
    def daily_sharpe(self):
        return np.mean(self.calc_deltas() / np.std(self.calc_deltas()))
        
    '''
    max_drawdown(self) - Returns the peak trough / peak value of portfolio trading history

    Returns:
    A positive float smaller or equal to 1
    '''
    def max_drawdown(self):
        max_drawdown = 0
        for idx, val in enumerate(self.absolute_values):
            for day in self.absolute_values[idx + 1:]:
                if (val - day) / val >= max_drawdown:
                    max_drawdown = (val - day) / val
        return max_drawdown
        
    '''
    calmar(self) - Returns the calmar ratio

    Returns:
    The average rate of return divided by the max drawdown
    '''
    def calmar(self):
        return np.average(self.calc_deltas()) / self.max_drawdown()

    '''
    returns(self) - Returns the absolute profit of the portfolio, based on the initial starting value

    Returns:
    Returns a tuple composed of two positive floats, the first valye is the absolute profit and the the second value
    is the percentile profit. Both are based on starting value.
    '''
    def returns(self):
        total_return = self.absolute_values[-1] - self.start_val
        perc_return = (total_return / self.start_val) * 100.0
        return total_return, perc_return
        

class Strategy():
    '''
    __init__(self,strategy) - Initializes a strategy object

    :argument: strategy - A function that takes 2 arguments, both 2D arrays where each column is 1 day. The first argument
    is price_info, the market capitalization of companies, and the second is analyst_info, filled with user-defined values
    where index is respectively the same with price_info (i.e. price_info[i][j] is about the same company and day as
    analyst_info[i][j]). The function should returns a 1D NP array that details the fractional amount of the total company
    the portfolio should be in possesion of (i.e. if we associate index 0 with company A then if the returned array has 0.1 in 
    index 0 then that means the portfolio should hold 10% of company A)

    Returns:
    The strategy object
    '''
    def __init__ (self, strategy): 
        self.strategy_function = strategy 
    '''
    allocations(self, analyst_info, price_info) - Allocates stock to the portfolio based on the strategy and 2 day info

    :argument: analyst_info - 2D NP array where each column is one day and each entry is filled with some user-defined analyst 
    info that the user-provided strategy can 

    :argumemt: price_info - 

    Returns:
    1D Array
    '''
    def allocations(self, analyst_info, price_info, prev_weights):
        return self.strategy_function(price_info, analyst_info, prev_weights)

def read_data(price_location, view_location):
    prices = pd.read_csv(price_location).to_numpy()[:, 1:]
    views = pd.read_csv(view_location).to_numpy()[:, 1:]
    return prices, views

def backtest(strat_function, starting_value, prices_location, views_location):
    prices, views = read_data(prices_location, views_location)
    acc = Account(starting_value)
    strat = Strategy(strat_function)    
    for ind, (price, view) in enumerate(zip(prices, views)): 
        if ind == 0:
            prev_weights = list(np.zeros(len(prices[0]))) 
        else:
            prev_weights = acc.weights[-1]
        acc.update(strat.allocations(prices[0: ind  + 1], views[0: ind + 1], prev_weights), price)

    sharpe = acc.daily_sharpe()
    max_drawdown = acc.max_drawdown()
    calmar = acc.calmar()
    total_return, percent_return = acc.returns()
        

    print(f'Sharpe: {sharpe}')
    print(f'Max Drawdon: {max_drawdown}')
    print(f'Total Return: {total_return}')
    print(f'Percent Return: {percent_return}')
    plt.plot(acc.absolute_values)
    plt.xlabel = "Time"
    plt.ylabel = "Portfolio Value"
    plt.show()
        