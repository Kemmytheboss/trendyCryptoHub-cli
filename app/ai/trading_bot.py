import math

class TradingBot:
    def __init__(self, ema_short=8, ema_long=21, rsi_period=14,
                 take_profit=0.06, stop_loss=0.03):
        self.ema_short = ema_short
        self.ema_long = ema_long
        self.rsi_period = rsi_period
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    # -------------------- EMA --------------------
    def ema(self, prices, window):
        if len(prices) < window:
            return None
        k = 2 / (window + 1)
        ema_val = prices[0]
        for price in prices[1:]:
            ema_val = price * k + ema_val * (1 - k)
        return ema_val

    # -------------------- RSI --------------------
    def rsi(self, prices, period):
        if len(prices) < period + 1:
            return None
        gains = []
        losses = []
        for i in range(1, period + 1):
            diff = prices[-i] - prices[-i - 1]
            if diff > 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 1
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # -------------------- Signal Logic --------------------
    def combined_signal(self, prices):
        ema_s = self.ema(prices, self.ema_short)
        ema_l = self.ema(prices, self.ema_long)
        rsi_val = self.rsi(prices, self.rsi_period)

        if ema_s is None or ema_l is None or rsi_val is None:
            return "HOLD"

        # Buy only when trend is strong AND RSI confirms
        if ema_s > ema_l and rsi_val < 60:
            return "BUY"

        # Sell when trend weakens OR RSI overheated
        if ema_s < ema_l or rsi_val > 70:
            return "SELL"

        return "HOLD"

    # -------------------- Backtest --------------------
    def backtest(self, prices, initial_capital=1000, fee_pct=0.001):
        print(i, p, signal, cash, position)
        cash = initial_capital
        position = 0
        entry_price = None
        trades = []
        equity_curve = []
        last_signal = "HOLD"

        for i, p in enumerate(prices):
            signal = self.combined_signal(prices[:i+1])
            # ---------------- BUY ----------------
            if signal == "BUY" and last_signal != "BUY" and cash > 0:
                amount = cash / p
                amount_after_fee = amount * (1 - fee_pct)
                position = amount_after_fee
                entry_price = p
                cash = 0

                trades.append({"type": "BUY", "price": p, "index": i})
                last_signal = "BUY"

            # ---------------- EXIT TRADE (SELL) ----------------
            if position > 0:
                # Stop loss
                if p <= entry_price * (1 - self.stop_loss):
                    proceeds = position * p
                    cash = proceeds * (1 - fee_pct)
                    trades.append({"type": "SL", "price": p, "index": i})
                    position = 0
                    last_signal = "SELL"

                # Take profit
                elif p >= entry_price * (1 + self.take_profit):
                    proceeds = position * p
                    cash = proceeds * (1 - fee_pct)
                    trades.append({"type": "TP", "price": p, "index": i})
                    position = 0
                    last_signal = "SELL"

            # Regular SELL signal
            if signal == "SELL" and position > 0 and last_signal == "BUY":
                proceeds = position * p
                cash = proceeds * (1 - fee_pct)
                trades.append({"type": "SELL", "price": p, "index": i})
                position = 0
                last_signal = "SELL"

            equity_curve.append(cash + position * p)

        # Final forced close
        final_value = cash + position * prices[-1]
        if position > 0:
            trades.append({"type": "SELL-FINAL", "price": prices[-1], "index": len(prices)-1})

        return {
            "initial_capital": initial_capital,
            "final_value": final_value,
            "total_return_pct": round((final_value - initial_capital) / initial_capital * 100, 2),
            "trades": trades,
            "equity_curve": equity_curve
        }
