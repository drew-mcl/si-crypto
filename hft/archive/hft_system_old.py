#!/usr/bin/env python3

import krakenex
import pandas as pd
import numpy as np

# Define a function to get OHLCV data from Kraken API
def get_kraken_ohlcv(pair='XXBTZUSD', interval=15, since=None):
    k = krakenex.API()
    ohlc_data = k.query_public('OHLC', {'pair': pair, 'interval': interval, 'since': since})
    df = pd.DataFrame(ohlc_data['result'][pair], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['close'] = df['close'].astype(float)  # <-- add this line
    df.set_index('time', inplace=True)
    return df

def calculate_moving_average(data, window=14):
    return data['close'].rolling(window=window).mean().iloc[-1].astype(float)

def position_sizing(account_balance, risk_tolerance):
    return account_balance * risk_tolerance

def calculate_stop_loss(entry_price, stop_loss_level):
    return entry_price - entry_price * stop_loss_level

def calculate_take_profit(entry_price, take_profit_level):
    return entry_price + entry_price * take_profit_level

def hft_system(symbol, account_balance, risk_tolerance, stop_loss_level, take_profit_level):
    # Get data and calculate the moving average
    data = get_kraken_ohlcv(pair=symbol, interval=15, since=None)
    data['MA'] = calculate_moving_average(data)

    long_position = False
    trades = []

    for index, row in data.iterrows():
        price = row['close']
        ma = row['MA']
        
        if not long_position and price > ma:
            long_position = True
            entry_price = price
            entry_time = row.name.to_pydatetime()
            
            stop_loss = calculate_stop_loss(entry_price, stop_loss_level)
            take_profit = calculate_take_profit(entry_price, take_profit_level)
            position_size = position_sizing(account_balance, risk_tolerance)

            trade = {
                "entry_time": entry_time,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "position_size": position_size
            }
            trades.append(trade)
        
        elif long_position:
            if price <= stop_loss or price >= take_profit:
                long_position = False
                exit_price = price
                exit_time = row.name.to_pydatetime()

                trade = trades[-1]
                trade["exit_time"] = exit_time
                trade["exit_price"] = exit_price
                trade["profit"] = (exit_price - entry_price) * trade["position_size"]

                account_balance += trade["profit"]

    return trades, account_balance

def backtest(trades):
    total_trades = len(trades)
    winning_trades = 0
    losing_trades = 0
    total_profit = 0

    total_trades = len(trades)
    winning_trades = sum(1 for trade in trades if trade["profit"] > 0)
    losing_trades = total_trades - winning_trades
    win_rate = winning_trades / total_trades
    average_win = np.mean([trade["profit"] for trade in trades if trade["profit"] > 0])
    average_loss = np.mean([trade["profit"] for trade in trades if trade["profit"] < 0])
    risk_reward_ratio = abs(average_win / average_loss)


    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {winning_trades}")
    print(f"Losing Trades: {losing_trades}")
    print(f"Win Rate: {win_rate * 100:.2f}%")
    print(f"Average Win: {average_win:.2f}")
    print(f"Average Loss: {average_loss:.2f}")
    print(f"Risk/Reward Ratio: {risk_reward_ratio:.2f}")
    print(f"Total Profit: {total_profit:.2f}")


if __name__ == "__main__":
    symbol = "XXBTZUSD"  # Symbol to trade
    account_balance = 10000  # Starting account balance
    risk_tolerance = 0.01  # Risk tolerance, e.g., 0.01 for 1% risk per trade
    stop_loss_level = 0.02  # 2% stop loss
    take_profit_level = 0.04  # 4% take profit

    trades, final_account_balance = hft_system(symbol, account_balance, risk_tolerance, stop_loss_level, take_profit_level)
    print(f"Initial account balance: {account_balance}")
    print(f"Final account balance: {final_account_balance}")
    print(f"Total profit/loss: {final_account_balance - account_balance}")
    
    backtest(trades)
