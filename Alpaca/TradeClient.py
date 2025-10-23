from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass, OrderClass, TimeInForce
from alpaca.trading.requests import (
    GetAssetsRequest,
    GetOrdersRequest,
    MarketOrderRequest,
)

from helpers import Singleton


@Singleton
class TradeClient:

    def __init__(self, config) -> None:
        self.config = config
        self.config.validate_config()

        self.client = None
        self.__initialize()
        assert self.client is not None

    def make_trade(self, symbol, qty, side, profit, stop_loss):
        assert self.client is not None
        try:
            order_request = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=side,
                time_in_force=TimeInForce.DAY,
                order_class=OrderClass.BRACKET,
                take_profit={"limit_price": profit},
                stop_loss={"stop_price": stop_loss},
            )
            order = self.client.submit_order(order_request)
            return f"Successfully Placed bet for AAPL. {order}"
        except Exception as e:
            return f"Error: Trying to make a trade.\n{e}"

    def get_all_assets(self):
        assert self.client is not None
        request = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
        try:
            assets = self.client.get_all_assets(request)
            assets = [{"name": asset.name, "symbol": asset.symbol} for asset in assets]
        except Exception as e:
            return f"Error: unable to get assets:\n{e}"
        return assets

    def get_active_trades(self):
        assert self.client is not None
        try:
            activity = self.client.get_orders()
            return activity
        except Exception as e:
            return f"Error: Trying to get trade activity:\n{e}"

    def get_active_trades_for_asset(self, symbol):
        assert self.client is not None
        try:
            request = GetOrdersRequest(symbols=[symbol])
            activity = self.client.get_orders(request)
            return activity
        except Exception as e:
            return f"Error: Trying to get trade activity:\n{e}"

    def __initialize(self):
        print("Initializing Trading Client...")
        try:
            self.client = TradingClient(
                self.config.Alpaca_API_Key_ID, self.config.Alpaca_API_Key_Secret
            )
            account = self.client.get_account()
            print(
                "Successfully connected to Trading Client.",
                account.status,
            )
            return
        except Exception as e:
            print("Unable to establish connection to Alpaca Client.")
            print(e)
            self.client = None
