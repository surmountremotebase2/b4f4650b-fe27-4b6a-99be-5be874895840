from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Consider these tickers for the strategy
        self.tickers = ["TQQQ", "SQQQ"]
        
    @property
    def interval(self):
        # Update frequency - daily might make sense for this strategy
        return "1day"

    @property
    def assets(self):
        # Operate on TQQQ and SQQQ
        return self.tickers

    def rma(self, prices, length=14):
        """Calculate the Running Moving Average (Simplified version)."""
        return prices.rolling(window=length, min_periods=1).mean()

    def run(self, data):
        tqqq_data = data["ohlcv"]["TQQQ"]
        sqqq_data = data["ohlcv"]["SQQQ"]

        # Assume data contains closing prices and volumes, among others
        tqqq_prices = [d["close"] for d in tqqq_data]
        sqqq_prices = [d["close"] for d in sqqq_data]

        if not tqqq_prices or not sqqq_prices:
            return TargetAllocation({})

        # Calculate RSI and RMA ribbon for TQQQ and SQQQ
        tqqq_rsi = RSI("TQQQ", tqqq_data, 14)
        sqqq_rsi = RSI("SQQQ", sqqq_data, 14)

        # Assuming pandas is available for simplicity in calculating RMA
        import pandas as pd

        tqqq_df = pd.DataFrame(tqqq_prices, columns=["close"])
        sqqq_df = pd.DataFrame(sqqq_prices, columns=["close"])

        tqqq_rma_ribbon = self.rma(tqqq_df["close"], 14)  # Using 14-day for the RMA ribbon
        sqqq_rma_ribbon = self.rma(sqqq_df["close"], 14)

        current_tqqq_price = tqqq_prices[-1]
        current_sqqq_price = sqqq_prices[-1]

        # Define allocations based on condition checks
        allocation = {}

        # If TQQQ RSI is below 30 (oversold), consider buying TQQQ
        if tqqq_rsi[-1] < 30 and current_tqqq_price > tqqq_rma_ribbon.iloc[-1]:
            allocation["TQQQ"] = 0.5  # Assign half allocation to TQQQ

        # Conversely, if SQQQ RSI is above 70 (overbought), consider buying SQQQ
        elif sqqq_rsi[-1] > 70 and current_sqqq_price > sqqq_rma_ribbon.iloc[-1]:
            allocation["SQQQ"] = 0.5  # Allocating to SQQQ in anticipation of a downward trend in NASDAQ

        # Add logic for holding or adjusting based on the strategy description
        # This simplistic approach doesn't directly factor in the KNN model aspect or the detailed risk/reward ratio management but illustrates strategy initiation based on indicators.
        
        return TargetAllocation(allocation)