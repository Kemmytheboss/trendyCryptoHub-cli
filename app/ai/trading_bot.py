class TradingBot:
    def __init__(self, ma_short=5, ma_long=20):
        self.ma_short = ma_short
        self.ma_long = ma_long


    def moving_average(self, prices, window):
        if len(prices) < window:
        return None
        return sum(prices[-window:]) / window


    def combined_signal(self, prices):
        ma_s = self.moving_average(prices, self.ma_short)
        ma_l = self.moving_average(prices, self.ma_long)
        if ma_s is None or ma_l is None:
        return {'signal': 'HOLD'}
        if ma_s > ma_l:
        return {'signal': 'BUY'}
        elif ma_s < ma_l:
        return {'signal': 'SELL'}
        return {'signal': 'HOLD'}


    def backtest(self, prices, initial_capital=1000.0, fee_pct=0.001):
        cash = initial_capital
        position = 0.0
        trades = []
        last_signal = 'HOLD'
        equity_curve = []
        for i, p in enumerate(prices):
            signal = self.combined_signal(prices[:i+1])['signal']
            if signal == 'BUY' and last_signal != 'BUY' and cash > 0:
                amount = cash / p
                amount_after_fee = amount * (1 - fee_pct)
                position += amount_after_fee
                cash = 0
                trades.append({'type': 'buy', 'price': p, 'index': i, 'position': amount_after_fee})
            elif signal == 'SELL' and last_signal != 'SELL' and position > 0:
                proceeds = position * p
                proceeds_after_fee = proceeds * (1 - fee_pct)
                cash += proceeds_after_fee
                trades.append({'type': 'sell', 'price': p, 'index': i, 'position': position})
                position = 0
                last_signal = signal
                equity_curve.append(cash + position * p)
                final_value = cash + position * prices[-1]
            return {
                'initial_capital': initial_capital,
                'final_value': final_value,
                'total_return_pct': ((final_value - initial_capital) / initial_capital) * 100,
                'trades': trades,
                'equity_curve': equity_curve
                }