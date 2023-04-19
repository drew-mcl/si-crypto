This code calls the get_kraken_ohlcv function to retrieve the OHLCV data for the specified symbol (e.g., "XXBTZUSD" for Bitcoin/USD), and then passes that data to the hft_system function to perform the trading strategy. The resulting trades and final account balance are printed to the console, along with the results of the backtest. You can modify the symbol, account_balance, risk_tolerance, stop_loss_level, and take_profit_level variables to suit your needs.



It looks like there is a KeyError due to the 'profit' key missing in some trades. One possible reason for this KeyError is that the loop in the hft_system function may finish without closing a long_position, so the last trade in the trades list will not have an exit_time, exit_price, or profit key. To fix this issue, you can close the last trade with the last available price if the loop ends with an open long_position.

To understand why there are only a few trades, let's break down the important parameters and conditions:

interval=15: The algorithm fetches OHLCV data with a 15-minute interval, which means it checks for trade opportunities every 15 minutes.
window=14: The moving average is calculated using a 14-period window, which means it takes into account the last 14 data points (in this case, the last 3.5 hours) to calculate the average.
stop_loss_level=0.02 and take_profit_level=0.04: These levels define the conditions under which a trade is closed, with stop_loss being 2% below the entry price and take_profit being 4% above the entry price.


If you would like the algorithm to perform more trades, you can experiment with the following adjustments:

Decrease the interval parameter to make trading decisions more frequently.
Change the window parameter to use a different period for the moving average calculation.
Adjust the stop_loss_level and take_profit_level parameters to make the exit conditions less strict.



sudo apt-get install build-essential libssl-dev libffi-dev
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure
make
sudo make install

pip install TA-Lib
