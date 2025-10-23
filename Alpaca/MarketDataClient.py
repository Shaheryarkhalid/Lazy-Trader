from datetime import datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from helpers import Singleton


@Singleton
class MarketDataClient:

    def __init__(self, config) -> None:
        self.config = config
        self.config.validate_config()

        self.client = None
        self.__initialize()
        assert self.client is not None

    def get_asset_history_week(self, asset_symbol):
        assert self.client is not None
        end = datetime.now()
        start = end - timedelta(days=7)
        try:
            request = StockBarsRequest(
                symbol_or_symbols=asset_symbol,
                timeframe=TimeFrame.Hour,
                start=start,
                end=end,
                feed="iex",
            )
            bars = self.client.get_stock_bars(request)
            if bars and bars.data:
                return bars.data
            else:
                return f"Error: Unable to get asset history.\n Returned Data: {bars}"
        except Exception as e:
            return f"Error: Unable to get asset history.\n{e}"

    def __initialize(self):
        print("Initializing Market Data Client...")
        try:
            self.client = StockHistoricalDataClient(
                self.config.Alpaca_API_Key_ID, self.config.Alpaca_API_Key_Secret
            )
            bars = self.get_asset_history_week("AAPL")
            if bars and not isinstance(bars, str) and bars["AAPL"]:
                print(
                    "Successfully connected to Market Data Client.",
                )
                return
            else:
                print(
                    f"Unablet to Initialize Historical Data Client. No Bars were returned.\n{bars}"
                )
                self.client = None

        except Exception as e:
            print("Unable to establish connection to Alpaca Historical Data Client.")
            print(e)
            self.client = None
