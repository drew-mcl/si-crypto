class TradingStrategy:
    def __init__(self, symbol: str, account_balance: float):
        self.symbol = symbol
        self.account_balance = account_balance

    def calculate_sma(self, data: pd.DataFrame, window: int) -> pd.Series:
        return data['close'].rolling(window=window).mean()

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        data['SMA20'] = self.calculate_sma(data, 20)
        data['SMA50'] = self.calculate_sma(data, 50)
        return data

    def evaluate_trades(self, data: pd.DataFrame) -> Tuple[List[Dict], float]:
        long_position = False
        trades = []

        for index in range(50, len(data)):
            row = data.iloc[index]
            prev_row = data.iloc[index - 1]

            price = row['close']
            sma20 = row['SMA20']
            sma50 = row['SMA50']
            prev_sma20 = prev_row['SMA20']
            prev_sma50 = prev_row['SMA50']

            if not long_position and sma20 > sma50 and prev_sma20 <= prev_sma50:
                long_position = True
                entry_price = price
                entry_time = row.name.to_pydatetime()

                trade = {
                    "entry_time": entry_time,
                    "entry_price": entry_price,
                }
                trades.append(trade)

            elif long_position and sma20 < sma50 and prev_sma20 >= prev_sma50:
                long_position = False
                exit_price = price
                exit_time = row.name.to_pydatetime()

                trade = trades[-1]
                trade["exit_time"] = exit_time
                trade["exit_price"] = exit_price
                trade["profit"] = exit_price - entry_price

                self.account_balance += trade["profit"]

        return trades, self.account_balance