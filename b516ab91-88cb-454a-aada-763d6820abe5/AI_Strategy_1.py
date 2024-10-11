from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log
import numpy as np  # Assuming pandas_ta supports numpy operations

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Tickers for the ETFs tracking NASDAQ 100
        self.tickers = ["TQQQ", "SQQQ"]

    @property
    def interval(self):
        # Daily interval for analysis
        return "1day"

    @property
    def assets(self):
        # Assets the strategy will trade
        return self.tickers

    def run(self, data):
        # Initialize allocation with no positions
        allocation_dict = {"TQQQ": 0, "SQQQ": 0}
        
        # Check if we have enough data points
        if 'ohlcv' not in data or len(data['ohlcv']) < 50:  # Assuming 50 days for a substantial EMA ribbon and RSI calculation
            return TargetAllocation(allocation_dict)
        
        # Calculate EMA ribbons for trend identification
        ema_ribbon = [EMA("TQQQ", data['ohlcv'], period) for period in range(5, 55, 5)]  # 10 EMA lines from 5 to 50 periods
        # Calculate RSI for overbought and oversold signals
        rsi = RSI("TQQQ", data['ohlcv'], 14)  # Using 14 periods for RSI
        
        # Decide on the action based on the current trend and RSI levels, simplified example
        if ema_ribbon[-1][-1] > ema_ribbon[0][-1] and rsi[-1] < 30:
            # Trend is upwards and stock is oversold
            allocation_dict["TQQQ"] = 0.67  # Invest 2/3 in TQQQ, assuming 1:2 risk/reward
            allocation_dict["SQQQ"] = 0  # No investment in SQQQ
            
        elif ema_ribbon[-1][-1] < ema_ribbon[0][-1] and rsi[-1] > 70:
            # Trend is downwards and stock is overbought
            allocation_dict["TQQQ"] = 0  # No investment in TQQQ
            allocation_dict["SQQQ"] = 0.33  # Invest 1/3 in SQQQ, assuming 1:2 risk/reward
        
        # Log the decision for analysis
        log(f'Trading decision made at: {str(data["ohlcv"][-1]["TQQQ"]["date"])}')
        
        return TargetAllocation(allocation_dict)