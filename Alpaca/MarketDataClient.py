from datetime import datetime, timedelta
from sys import base_prefix
from alpaca.data import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestTradeRequest
from alpaca.data.timeframe import TimeFrame
from colorama import Fore
from internals.Config import Config


from helpers import Singleton


@Singleton
class MarketDataClient:

    def __init__(self) -> None:
        self.config = Config()
        self.config.validate_config()

        self.client = None
        self.__initialize()
        assert self.client is not None

    def get_asset_price(self, symbol=""):
        print(Fore.LIGHTWHITE_EX + f"⏳ Getting Price for '{symbol}'")
        assert self.client is not None
        try:
            # trade_request = StockLatestTradeRequest(symbol_or_symbols=symbol)
            trade_request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            latest_trade = self.client.get_stock_latest_quote(trade_request)
            if latest_trade == {}:
                print(Fore.YELLOW + f"🟠 No price data found for '{symbol}'.")
                return f"No price data found for '{symbol}'. Please try another asset."
            else:
                try:
                    bid_price = latest_trade[symbol].bid_price
                    ask_price = latest_trade[symbol].ask_price
                    base_price = (bid_price + ask_price) / 2
                    print(Fore.GREEN + f"🟢 Price for '{symbol}': {base_price}")
                    return base_price
                except Exception as e:
                    print(Fore.RED + f"🔴 Exception: {e}")
                    print(Fore.RED + str(latest_trade))
                    return latest_trade
        except Exception as e:
            return f"🔴 Error: Getting the price for given asset. {e}"

    def get_asset_history_week(self, symbol):
        assert self.client is not None
        end = datetime.now()
        start = end - timedelta(days=7)
        try:
            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Hour,
                start=start,
                end=end,
                feed="iex",
            )
            bars = self.client.get_stock_bars(request)
            if bars and bars.data:
                return bars.data
            else:
                return f"🔴 Error: Unable to get asset history.\n Returned Data: {bars}"
        except Exception as e:
            return f"🔴 Error: Unable to get asset history.\n{e}"

    def __initialize(self):
        print(Fore.LIGHTWHITE_EX + "⏳ Initializing Market Data Client...")
        try:
            self.client = StockHistoricalDataClient(
                self.config.Alpaca_API_Key_ID, self.config.Alpaca_API_Key_Secret
            )
            bars = self.get_asset_history_week("AAPL")
            if bars and not isinstance(bars, str) and bars["AAPL"]:
                print(Fore.GREEN + "🟢 Successfully connected to Market Data Client.")
                return
            else:
                print(
                    Fore.RED
                    + f"🔴 Unable to Initialize Historical Data Client. No Bars were returned.\n{bars}"
                )
                self.client = None

        except Exception as e:
            print(
                Fore.RED
                + "🔴 Unable to establish connection to Alpaca Historical Data Client."
            )
            print(Fore.RED + str(e))
            self.client = None
