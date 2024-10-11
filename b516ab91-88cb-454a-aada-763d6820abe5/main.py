from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Since the NASDAQ 100 Index itself may not be directly tradable or have RSI,
        # we use TQQQ (3x leveraged NASDAQ 100 ETF) as a proxy to trade based on the index's momentum.
        self.tickers = ["TQQQ", "SQQQ"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Setting interval to 5 minutes for RSI calculation
        return "5min"

    def run(self, data):
        # Initialize allocations for both TQQQ and SQQQ to zero
        allocation_dict = {"TQQQ": 0, "SQQQ": 0}

        # Calculate the RSI for TQQQ as a proxy for NASDAQ 100 index
        rsi_value = RSI("TQQQ", data["ohlcv"], length=14) # standard period is 14

        if rsi_value:
            current_rsi = rsi_value[-1]  # Get the most recent RSI value

            # Check for the oversold condition to buy TQQQ
            if current_rsi < 30:  # RSI below 30 is typically considered oversold
                log("TQQQ is oversold. Buying opportunity.")
                allocation_dict["TQQQ"] = 1  # Full allocation to TQQQ

            # Check for the overbought condition to buy SQQQ
            elif current_rsi > 70:  # RSI above 70 is typically considered overbought
                log("TQQQ is overbought. Buying SQQQ as a hedge.")
                allocation_dict["SQQQ"] = 1  # Full allocation to SQQQ

        # Return the allocation dict wrapped in a TargetAllocation object
        return TargetAllocation(allocation_dict)