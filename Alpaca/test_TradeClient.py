import unittest

from alpaca.trading.enums import OrderSide
from functions.Trade import Trade
from internals.Config import Config
from Alpaca.TradeClient import TradeClient


class TestTradeClient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.config = Config()
        self.trade_client = TradeClient()

    def test_get_all_assets(self):
        assets = self.trade_client.get_all_assets()
        self.assertNotIsInstance(assets, str)
        self.assertGreater(len(assets), 0)
        print(f"Total Assets: {len(assets)}")

    def test_make_trade(self):

        msg = self.trade_client.make_trade(
            "AAPL",
            1,
            OrderSide.SELL,
            200,
            300,
        )
        self.assertFalse(isinstance(msg, str))
        trade_db = Trade()
        assert not isinstance(msg, str)
        print(msg.id)
        err = trade_db.save_trade_locally(
            str(msg.id),
            symbol="AAPL",
            price=250,
            position="SELL",
            profit_limt=200,
            stop_loss=300,
            reason="XYz",
        )
        print(err)

    def test_get_active_trades(self):
        active_trades = self.trade_client.get_active_trades()
        self.assertIsInstance(active_trades, list)
        self.assertNotIsInstance(active_trades, str)
        print(f"Account: Total Active Trades: {len(active_trades)}")

    def test_get_active_trades_for_asset(self):
        active_trades = self.trade_client.get_active_trades_for_asset("AAPL")
        self.assertIsInstance(active_trades, list)
        self.assertNotIsInstance(active_trades, str)
        print(f"Account: Total Active Trades for 'APPL': {len(active_trades)}")
        print(print(active_trades))
