import unittest

from alpaca.trading.enums import OrderSide
from colorama import Fore, init
from functions.Trade import Trade
from internals.Config import Config
from Alpaca.TradeClient import TradeClient

init(autoreset=True)


class TestTradeClient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        try:
            super().__init__(methodName)
            self.config = Config()
            self.trade_client = TradeClient()
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_get_all_assets(self):
        try:
            assets = self.trade_client.get_all_assets()
            self.assertNotIsInstance(assets, str)
            self.assertGreater(len(assets), 0)
            print(f"Total Assets: {len(assets)}")
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_make_trade(self):

        try:
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
            msg = trade_db.save_trade_locally(
                str(msg.id),
                symbol="AAPL",
                price=250,
                position="SELL",
                profit_limit=200,
                stop_loss=300,
                reason="XYz",
            )
            if msg.startswith("Error"):
                raise Exception(msg)
            print(Fore.GREEN + msg)

        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_get_active_trades_for_asset(self):
        try:
            active_trades = self.trade_client.get_active_trades_for_asset("AAPL")
            self.assertIsInstance(active_trades, list)
            self.assertNotIsInstance(active_trades, str)
            print(f"Account: Total Active Trades for 'APPL': {len(active_trades)}")
            print(print(active_trades))
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")
