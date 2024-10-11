from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Initializing with two tickers that are inverses of each other (TQQQ for bullish, SQQQ for bearish NASDAQ 100 movements)
        self.tickers = ["TQQQ", "SQQQ"]
        
    @property
    def interval(self):
        # Using daily data for the strategy to make decisions based on the end-of-day market summary
        return "1day"

    @property
    def assets(self):
        # The strategy will involve trading on TQQQ and SQQQ
        return self.tickers

    def run(self, data):
        # Check if the needed data is present
        if "ohlcv" not in data:
            log("Required OHLCV data is missing.")
            return TargetAllocation({})
        
        allocations = {}
        
        # Calculate RSI for both assets to determine overbought or oversold conditions
        for ticker in self.tickers:
            ohlcv_data = data["ohlcv"][ticker]
            prices = pd.Series([item["close"] for item in ohlcv_data])
            
            # Ensure there's enough data to calculate RSI
            if len(prices) >= 14:  # RSI typically uses a 14-day period as standard
                rsi = RSI(ticker, ohlcv_data, 14)[-1]  # Obtain the latest RSI value
                
                # Logic for deciding the allocation
                if ticker == "TQQQ" and rsi < 30:
                    # TQQQ is oversold, consider buying
                    allocations[ticker] = 0.5  # Allocating a fixed fraction for simplicity
                elif ticker == "SQQQ" and rsi > 70:
                    # SQQQ is overbought, suggesting a bearish outlook for the market, consider buying as a hedge
                    allocations[ticker] = 0.5
        
        # Check if allocations dict is empty, which means neither condition was met
        if not allocations:
            log("No trade signal based on the current RSI readings for TQQQ and SQQQ.")
            return TargetAllocation({})
        
        return TargetAllocation(allocations)