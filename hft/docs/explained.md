Fetches historical OHLCV (Open, High, Low, Close, Volume) data for a given trading pair from the Kraken cryptocurrency exchange using its API.

Implements a simple High-Frequency Trading (HFT) system that uses a combination of indicators such as Moving Average, Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD) to make trading decisions.

The HFT system takes long positions when the price is above the moving average, RSI is below 30, and MACD histogram is increasing. It closes the position when the price reaches the stop loss or take profit levels.

The script calculates position sizing based on the account balance and risk tolerance and determines stop loss and take profit levels as a percentage of the entry price.

It backtests the trading strategy, providing performance metrics such as the number of trades, winning trades, losing trades, win rate, average win, average loss, risk/reward ratio, and total profit.