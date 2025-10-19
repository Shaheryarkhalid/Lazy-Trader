from datetime import date, datetime, timedelta
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import GetAssetsRequest
from alpaca.data.requests import StockBarsRequest


class TradeClient:
    def __init__(self, config) -> None:
        self.config = config
        self.client = None

        self.__initialize_client()

        assert self.client != None

    def __initialize_client(self):
        assert self.config.Alpaca_API_Key_ID != None
        assert self.config.Alpaca_API_Key_ID != ""

        assert self.config.Alpaca_API_Key_Secret != None
        assert self.config.Alpaca_API_Key_Secret != ""

        self.client = TradingClient(
            self.config.Alpaca_API_Key_ID, self.config.Alpaca_API_Key_Secret
        )

    def get_all_assets(self):
        assert self.client != None
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
        try:
            assets = self.client.get_all_assets(search_params)
            assets = [{"name": asset.name, "symbol": asset.symbol} for asset in assets]
        except Exception as e:
            return f"Error: Unable to get assets:\n{e}"
        return assets

    def get_past_week_performance(self, symbol):
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            start=datetime(date.today() - timedelta(days=7)),
            end=datetime(date.today()),
        )
