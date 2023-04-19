#!/usr/bin/env python3

import krakenex
import pandas as pd
import numpy as np
import talib
from typing import List, Dict, Tuple

class TradingStrategy:
    def __init__(self, symbol: str, account_balance: float, risk_tolerance: float, stop_loss_level: float, take_profit_level: float):
        self.symbol = symbol
        self.account_balance = account_balance
        self.risk_tolerance = risk_tolerance
        self.stop_loss_level = stop_loss_level
        self.take_profit_level = take_profit_level

    def get_kraken_ohlcv(self, interval: int = 15, since: int = None) -> pd.DataFrame:
        k = krakenex.API()
        ohlc_data = k.query_public('OHLC', {'pair': self.symbol, 'interval': interval, 'since': since})
        df = pd.DataFrame(ohlc_data['result'][self.symbol], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['close'] = df['close'].astype(float)
        df.set_index('time', inplace=True)
        return df

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        data['MA'] = data['close'].rolling(window=14).mean()
        data['RSI'] = talib.RSI(data['close'], timeperiod=14)
        macd, macd_signal, macd_hist = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        data['MACD_Hist'] = macd_hist
        return data

    def calculate_stop_loss(self, entry_price: float) -> float:
        return entry_price - entry_price * self.stop_loss_level

    def calculate_take_profit(self, entry_price: float) -> float:
        return entry_price + entry_price * self.take_profit_level

    def position_sizing(self) -> float:
        return self.account_balance * self.risk_tolerance

    def evaluate_trades(self, data: pd.DataFrame) -> Tuple[List[Dict], float]:
        long_position = False
        trades = []

        for index in range(33, len(data)):
            row = data.iloc[index]

            price = row['close']
            ma = row['MA']
            rsi = row['RSI']
            macd_hist_current = row['MACD_Hist']

            if not long_position and price > ma and rsi < 30 and macd_hist_current > data['MACD_Hist'].iloc[index - 1]:
                long_position = True
                entry_price = price
                entry_time = row.name.to_pydatetime()

                stop_loss = self.calculate_stop_loss(entry_price)
                take_profit = self.calculate_take_profit(entry_price)
                position_size = self.position_sizing()

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

                    self.account_balance += trade["profit"]

        return trades, self.account_balance

    def backtest(self, trades: List[Dict]) -> None:
        total_trades = len(trades)
        
        if total_trades == 0:
            print("No trades executed.")
            return

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

if __name__ == "__main__":
    symbol = "XXBTZUSD"  # Symbol to trade
    account_balance = 10000  # Starting account balance
    risk_tolerance = 0.01  # Risk tolerance, e.g., 0.01 for 1% risk per trade
    stop_loss_level = 0.02  # 2% stop loss
    take_profit_level = 0.04  # 4% take profit

    strategy = TradingStrategy(symbol, account_balance, risk_tolerance, stop_loss_level, take_profit_level)
    data = strategy.get_kraken_ohlcv()
    data = strategy.calculate_indicators(data)
    trades, final_account_balance = strategy.evaluate_trades(data)
    strategy.backtest(trades)

    print(f"Initial account balance: {account_balance}")
    print(f"Final account balance: {final_account_balance}")
    print(f"Total profit/loss: {final_account_balance - account_balance}")

