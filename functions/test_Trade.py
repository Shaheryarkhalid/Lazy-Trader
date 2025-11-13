import unittest


from alpaca.trading.enums import OrderSide
from colorama import Fore, init

from functions.Trade import Trade
from internals.Config import Config

init(autoreset=True)


class TestTrade(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        try:

            super().__init__(methodName)
            self.config = Config()
            self.trade = Trade()
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_save_trade_locally(self):

        try:
            msg = self.trade.save_trade_locally(
                "abc-test-id",
                "APPL",
                250,
                OrderSide.SELL,
                200,
                300,
                "Looks good to me.",
            )
            self.assertTrue(msg.startswith("Success"))
            print(Fore.GREEN + msg)
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")

    def test_get_trades_from_db(self):
        try:
            trades = self.trade.get_trades_from_db("APPL")
            print(f"Database: Number of Trades for 'APPL': {len(trades)}")
        except Exception as e:
            print(Fore.RED + f"{e}")
            self.fail("")
