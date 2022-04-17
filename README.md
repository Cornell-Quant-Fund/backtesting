# backtesting
A prototype back-testing framework. 

# How to Use: 
1. Refer to demo.py for an example. strat_function is a user-specified mapping from the past n-days of price and user data to portfolio weightings. 
2. Inputs to start_function will be of arrays shape (num_days, num_assets) for both price and user data.
3. Pass strat_function into the backtest function, along with a starting cash value and the price and data directories. 

# Current Scope:
As is right now, this engine has support for any technical analysis based strategy, as well as strategies with indicators derived from some auxillary data source.
Looking to include strategy visualizations and trend lines, as well as a breakdown of asset weightings over time. 
